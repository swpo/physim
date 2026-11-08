"""b4 -- shared pieces of the round-4 study `bias` (track 1): learned level 1 from raw level-0 Flow-Lenia gliders.

The map (level-0 theory x inductive bias) -> emergent level-1 variables, for one level-0 theory (the gliders world,
vw1/port/aworld.py, unchanged, tracker 'jax'). Encoders read the raw level-0 state (2 x 128 x 128) and output c
numbers per 16-px block on the 8 x 8 block grid (64 c numbers):
  N<h>  local, translation-equivariant (stride 16, periodic), receptive field = block + h px halo (h = 0, 4, 8, 16),
        nonlinear: a linear window plus a zero-initialised nonlinear branch (pixel MLP -> window conv -> MLP)
  L<h>  the same window, linear only (the interpretable arm: is the learned window the block-mass window?)
  U     unconstrained control: dense map of the whole field (+ MLP residual), reshaped to the 8 x 8 x c grid
Objectives (the same heads for every encoder, so only the encoder bias varies):
  recon  autoencoder: each block's 2 x 16 x 16 content from its own latent (L: linear decoder)
  clos   closure: the whitened latent predicts its own future at h = 1, 4, 16 from 2 lags with a GLOBAL linear head
         (whitening is the collapse guard: unit covariance, relative ridge eps)
  local  local law: the same, with one shared LOCAL rule (3 x 3 neighbourhood, 2 lags, linear + MLP)
  pib    predictive bottleneck: whitened latent + N(0, 0.5^2) noise predicts the future level-0 block contents
         at h = 1, 4, 16 through a local head
  clos1 / clos16  (L arm only) closure at one horizon
Layout (two halves A, B for cross-fitting, as learned_phi2): per half J_CERT trajectories with fresh-noise branches
(test ticks 40/100/160/220, R_BR = 5 branches x TB = 16 ticks; replicate 0 = the base continuation) plus J_EXTRA
training-only trajectories. Phi fitted on one half is certified on the other half's test states.
"""
from __future__ import annotations

import json
import os
import sys
import time

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
VEC = os.path.abspath(os.path.join(HERE, "..", "..", ".."))          # research/alife/vecworld
PORT = os.path.join(VEC, "vw1", "port")
VW1 = os.path.join(VEC, "vw1")
CLOSURE_SCRIPTS = os.path.join(VEC, "vw1", "fresh", "closure", "scripts")
LPHI_DIR = os.path.join(VEC, "program", "track1", "learned_phi2")

TINY = os.environ.get("B4_TINY", "0") == "1"
SEEDS = {"A": 9701, "B": 9702}          # designer seeds (new); branch keys from seed + 50
HALVES = ("A", "B")
HZ = [1, 2, 4, 8, 16]                   # certification horizons
HTR = (1, 4, 16)                        # training horizons (clos, local, pib)
RF = (0, 4, 8, 16)                      # halo widths (px) of the local encoders
CS = (1, 2, 4)                          # latent channels per block
G, BS, NPIX = 8, 16, 128                # block grid, block size, field size
if TINY:
    J_CERT, J_EXTRA, T, TEST, TB, R_BR, CH, CB, BURN = 4, 1, 36, (18,), 16, 2, 6, 8, 2
    N_VAL_TRAJ = 1
else:
    J_CERT, J_EXTRA, T, TEST, TB, R_BR, CH, CB, BURN = 32, 32, 300, (40, 100, 160, 220), 16, 5, 10, 8, None
    N_VAL_TRAJ = 8
J_ALL = J_CERT + J_EXTRA


def setup_paths(closure: bool = False):
    """Port first (vw, aworld); optionally closure_lib (integrate/analyze) and lphi (learned_phi2)."""
    for p in (LPHI_DIR, CLOSURE_SCRIPTS, VW1, PORT) if closure else (VW1, PORT):
        if p not in sys.path:
            sys.path.insert(0, p)
    if closure:
        import closure_lib as CL  # noqa: F401
        import lphi as LP
        LP.TEST = list(TEST)
        LP.NJ = J_CERT
        LP.HZ = list(HZ)
        return CL, LP
    return None


def work_dir(*sub):
    w = os.environ.get("B4_WORK", os.path.join(HERE, "work"))
    p = os.path.join(w, *sub)
    os.makedirs(p, exist_ok=True)
    return p


def out_dir(*sub):
    o = os.environ.get("B4_OUT", os.path.join(HERE, "out"))
    p = os.path.join(o, *sub)
    os.makedirs(p, exist_ok=True)
    return p


def progress(msg):
    line = f"{time.strftime('%H:%M:%S')} {msg}"
    print(line, flush=True)
    try:
        with open(os.path.join(out_dir(), "progress.txt"), "a") as f:
            f.write(line + "\n")
    except OSError:
        pass


def deadline(kind: str) -> float:
    """Epoch seconds after which no new work of this kind starts ('train' | 'cert'); inf if unset."""
    v = os.environ.get({"train": "B4_TRAIN_DEADLINE", "cert": "B4_CERT_DEADLINE"}[kind])
    return float(v) if v else float("inf")


def jdump(obj, path):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(jsonable(obj), f, indent=1)
    os.replace(tmp, path)


def jsonable(o):
    import math
    import numpy as np
    if isinstance(o, dict):
        return {str(k): jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jsonable(v) for v in o]
    if isinstance(o, np.ndarray):
        return jsonable(o.tolist())
    if isinstance(o, np.floating):
        o = float(o)
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.bool_):
        return bool(o)
    if isinstance(o, float) and not math.isfinite(o):
        return None
    return o


# ----------------------------------------------------------------------------- the grid
def configs():
    """Training configs in priority order: (name, enc, h, obj, c). enc in N, L, U; h None for U."""
    out = []
    add = lambda e, h, o, c: out.append((f"{e}{'' if h is None else h}_{o}_c{c}", e, h, o, c))
    for o in ("clos", "recon", "local", "pib"):
        for h in RF:
            add("N", h, o, 1)
    for h in RF:
        for o in ("clos", "recon", "local"):
            add("L", h, o, 1)
    add("L", 8, "clos1", 1)
    add("L", 8, "clos16", 1)
    for o in ("clos", "recon", "local", "pib"):
        add("U", None, o, 1)
    for c in (2, 4):
        for o in ("clos", "recon", "local", "pib"):
            for h in RF:
                add("N", h, o, c)
        for o in ("clos", "recon", "local", "pib"):
            add("U", None, o, c)
        if c == 2:
            for h in RF:
                add("L", h, "clos", 2)
    if TINY:
        keep = {"N0_clos_c1", "N16_recon_c1", "N8_local_c1", "N4_pib_c1", "L8_recon_c1", "U_pib_c1", "N8_clos_c4",
                "U_local_c4", "L8_clos16_c1"}
        out = [x for x in out if x[0] in keep]
    return out


HAND = ("mass", "chan", "view", "tent", "objmass", "objfield")
RANDOM = (("rand8_c1", 8, 1), ("rand8_c4", 8, 4))   # untrained linear windows (2 seeds each)
