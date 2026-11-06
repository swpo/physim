"""Shared helpers for the fresh VW-1 input analyses (key: inputs). Everything is simulated through
the VW-1 world (port/aworld.py: FlowLenia JAX level, Phi_coarse, Phi_objects = the VW-0 tracker as an
opaque VW-1 CoarseGrain) and its designer API; VW-0 analysis/drawing helpers are used read-only."""
import os
import sys

sys.dont_write_bytecode = True
PORT = "/home/user/evalwork/vecworld/vw1/port"
if PORT not in sys.path:
    sys.path.insert(0, PORT)
import _paths  # noqa: E402,F401

import numpy as np  # noqa: E402

ROOT = "/home/user/evalwork/vecworld/vw1/fresh/inputs"
RES = os.path.join(ROOT, "results")
MEDIA = os.path.join(ROOT, "media")
H = W = 128
HW = H * W
NC = 192          # Phi_coarse length
K = 12            # tracked slots
NF = 12           # features per slot
NS = 17           # slot-table columns in the tracker memory (NF + cy, cx, age, event, uid)


def mi(d, L):
    return (d + L / 2) % L - L / 2


def build_world(kind="both", seed=0):
    import aworld as AW
    specs, parts = AW.build(with_objects=(kind != "coarse"))
    w = AW.MapWorld(specs[kind], world_seed=seed)
    return w, parts, AW


def mem_parts(mem):
    """Batched tracker memory (B, 16593) -> (slot-label map (B, HW) int, slot table (B, K, NS))."""
    m = np.asarray(mem)
    return m[:, :HW].astype(int), m[:, HW:HW + K * NS].reshape(m.shape[0], K, NS)


def tracker_mem(ens, kind="both"):
    """Tracker memory of a batched ensemble of the 'both' world (pair: (coarse (), objects m))."""
    mem = ens.carry.mem[0]
    if kind == "both":
        mem = mem[1]
    return np.asarray(mem)


def matter(x):
    """Batched level-0 x (B, C, H, W) -> A_sum (B, HW)."""
    x = np.asarray(x)
    return x.sum(1).reshape(x.shape[0], -1)


def kick_np(A, u, C=2):
    """numpy transcription of flowlenia_jax.kick for one member (A (C, HW) flat, u (HW,)); used only
    to account for how much matter a command moves (the world itself applies the JAX kick)."""
    Af = A.reshape(C, -1)
    src, snk = u < 0, u > 0
    S = Af.sum(0)
    take = np.where(src, np.minimum(-u, np.maximum(S, 0.0)), 0.0)
    frac = np.where(src & (S > 0), take / np.maximum(S, 1e-300), 0.0)
    removed = Af * frac[None]
    pooled = removed.sum(1)
    w = np.where(snk, u, 0.0)
    ws = w.sum()
    zs = abs(u.sum()) <= 1e-9 * max(1.0, np.abs(u).sum())
    if zs:
        give = pooled[:, None] * (w / (ws if ws > 0 else 1.0))[None] if (ws > 0 and pooled.sum() > 0) else 0.0 * Af
    else:
        give = np.broadcast_to(w[None] / C, Af.shape)
    out = Af - removed + give
    out = np.where(src[None], np.maximum(out, 0.0), out)
    return out


def moved_matter(A, u):
    """Matter moved by command u (actuator basis) at state A (C, HW): half the L1 change."""
    return 0.5 * float(np.abs(kick_np(A, u) - A.reshape(2, -1)).sum())
