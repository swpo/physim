"""vw.secret -- a high-entropy secret behind all real-world randomness (EXAM.md section 2).

VW-1 derives every key from a public salt and small integers (`world.make_key`). With the public
code and a guessed world seed, anyone can recompute every episode and exam start exactly, and fit
the hidden parameters noise path by noise path. Here every real-world key is instead

    key = threefry key whose 64-bit data are the first 8 bytes of HMAC-SHA256(secret, tag | parts)

so keys cannot be recomputed from public integers. Labels (reset seeds, item ids) go through the
same keyed hash: they name an episode, they are not keys.

Entropy. The secret has >= 128 bits (default 256, from os.urandom). Each derived threefry key has
64 bits of state (2 x uint32), so recovering one key by search costs ~2**64 simulations and reveals
nothing about any other key (HMAC is one-way). Namespaces ('episode', 'exam', 'clim', ...) are
separate HMAC tags, so no agent label can reach an exam key.

The designer may fix the secret (Secret.from_hex) to make a run reproducible; it is then held with
the hidden parameters, never published. Only `commitment()` (a SHA-256 of the secret) may be
published, so the secret can be revealed and checked after grading.
"""
from __future__ import annotations

import hashlib
import hmac
import os
import struct
from typing import Union

import jax
import numpy as np

_TAG = b"vw-secret/v1"
MIN_BITS = 128

Part = Union[int, str, bytes]


def _encode(parts) -> bytes:
    """Unambiguous encoding of a tuple of ints (>= 0, < 2**128), strings and bytes."""
    out = []
    for p in parts:
        if isinstance(p, bool):
            raise TypeError("secret: bool is not a valid key part")
        if isinstance(p, (int, np.integer)):
            p = int(p)
            if not 0 <= p < 2 ** 128:
                raise ValueError("secret: integer parts must lie in [0, 2**128)")
            out.append(b"i" + p.to_bytes(16, "big"))
        elif isinstance(p, str):
            b = p.encode("utf-8")
            out.append(b"s" + struct.pack(">I", len(b)) + b)
        elif isinstance(p, (bytes, bytearray)):
            out.append(b"b" + struct.pack(">I", len(p)) + bytes(p))
        else:
            raise TypeError(f"secret: key parts must be int, str or bytes, got {type(p).__name__}")
    return b"".join(out)


class Secret:
    """A >= 128-bit secret; derives JAX keys, labels and salted hashes by HMAC-SHA256."""

    def __init__(self, value: bytes | None = None, bits: int = 256):
        if value is None:
            if bits < MIN_BITS or bits % 8:
                raise ValueError(f"Secret: bits must be a multiple of 8 and >= {MIN_BITS}")
            value = os.urandom(bits // 8)
        value = bytes(value)
        if 8 * len(value) < MIN_BITS:
            raise ValueError(f"Secret: need at least {MIN_BITS} bits, got {8 * len(value)}")
        self._v = value

    @classmethod
    def from_hex(cls, s: str) -> "Secret":
        return cls(bytes.fromhex(s))

    def hex(self) -> str:
        """The secret itself (designer only: store it with the hidden parameters)."""
        return self._v.hex()

    @property
    def bits(self) -> int:
        return 8 * len(self._v)

    def __repr__(self) -> str:          # never print the value
        return f"Secret({self.bits} bits, commitment={self.commitment()[:12]}...)"

    # ---- derivations ----
    def digest(self, *parts: Part) -> bytes:
        return hmac.new(self._v, _TAG + _encode(parts), hashlib.sha256).digest()

    def key(self, *parts: Part) -> jax.Array:
        """A typed threefry PRNG key from (secret, parts)."""
        d = self.digest("key", *parts)
        return jax.random.wrap_key_data(np.frombuffer(d[:8], dtype=">u4").astype(np.uint32))

    def keys(self, n: int, *parts: Part) -> jax.Array:
        """n independent keys (a batch of shape (n,)) for members 0..n-1 under parts."""
        data = np.stack([np.frombuffer(self.digest("key", *parts, j)[:8], dtype=">u4").astype(np.uint32)
                         for j in range(int(n))])
        return jax.random.wrap_key_data(data)

    def label(self, *parts: Part, bits: int = 62) -> int:
        """A keyed integer label in [0, 2**bits) (e.g. an item id that reveals nothing)."""
        return int.from_bytes(self.digest("label", *parts)[:8], "big") >> (64 - bits)

    def rng(self, *parts: Part) -> np.random.Generator:
        """A numpy generator seeded from (secret, parts) (programs, item order, ...)."""
        d = self.digest("rng", *parts)
        return np.random.default_rng([int.from_bytes(d[i:i + 8], "big") for i in range(0, 32, 8)])

    def child(self, *parts: Part) -> "Secret":
        """An independent sub-secret (e.g. one per world, or 'exam' vs 'episodes')."""
        return Secret(self.digest("child", *parts))

    def salted_hash(self, data: bytes) -> str:
        """Identity hash of hidden material (e.g. theta bytes) that cannot be brute-forced
        from a coarse parameter grid without the secret."""
        return hmac.new(self._v, b"vw-identity" + bytes(data), hashlib.sha256).hexdigest()

    def commitment(self) -> str:
        """Public commitment to the secret (SHA-256); reveal hex() after grading to verify."""
        return hashlib.sha256(b"vw-commit" + self._v).hexdigest()
