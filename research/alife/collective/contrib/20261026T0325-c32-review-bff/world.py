"""BFF program soup (Aguera y Arcas et al. 2024, arXiv:2406.19108) as a labkit world (c30).

One internal step = one epoch of bff.Soup (random ordered pairs of 64-byte tapes are concatenated,
run as BFF code for up to 2^13 instructions, split; background mutation 0.00024 per byte). By default
the soup holds N = 4096 tapes, 32 of them planted copies of seeded.planted() (a hand-built
self-replicator); WORLD_P='{"planted": 0}' gives the spontaneous soup. fields(): the soup drawn as a
512 x 512 byte image (tape i occupies 64 consecutive pixels of row-major order); channel 0 = 1 where
the byte is one of the 10 BFF instructions, channel 1 = 1 where the tape is an exact copy of the
commonest tape in the soup, channel 2 = byte value / 255.
"""
import os, sys, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
from bff import Soup
from seeded import planted

META = {"name": "bff-soup", "family": "program-soup", "parent": None,
        "mutation": "new class: self-modifying BFF tapes interacting in a well-mixed soup",
        "size": (512, 512), "steps_per_frame": 25, "dt": 1.0,
        "channels": ["instruction", "commonest_tape", "byte"], "matter": [1],
        "threshold": 0.5, "smooth": 0.0, "periodic": False}
P = dict(N=4096, planted=32, mu=0.00024)
P.update(json.loads(os.environ.get("WORLD_P", "{}")))
INS = np.frombuffer(b"<>{}-+.,[]", np.uint8)


def init(seed, size=None):
    S = Soup(int(seed), N=int(P["N"]), mu=float(P["mu"]))
    if int(P["planted"]):
        S.soup[:int(P["planted"])] = planted()
    return S


def step(S):
    S.step()
    return S


def fields(S):
    b = S.soup.reshape(-1)[:512 * 512]
    if b.size < 512 * 512:
        b = np.r_[b, np.zeros(512 * 512 - b.size, np.uint8)]
    v = np.ascontiguousarray(S.soup).view(np.dtype((np.void, 64))).reshape(-1)
    u, inv, c = np.unique(v, return_inverse=True, return_counts=True)
    top = (inv.reshape(-1) == c.argmax()).repeat(64)[:512 * 512].astype(float)
    if top.size < 512 * 512:
        top = np.r_[top, np.zeros(512 * 512 - top.size)]
    return np.stack([np.isin(b, INS).astype(float).reshape(512, 512), top.reshape(512, 512), (b / 255.0).reshape(512, 512)])
