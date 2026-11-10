"""c5 -- shared pieces of the round-5 study `bias2` (track 1): two more rows of the map
(level-0 theory x inductive bias) -> emergent level-1 variables.

Round 4 (`../../round4/bias`) did one row, the Flow-Lenia gliders world (mass-conserving). Here the same reduced
grid runs on two level-0 theories in which nothing is conserved:
  vortex    the fed-vortex world with heredity (`../../track1/vortex_world`, unchanged): fields om (vorticity),
            Y (fuel), a, b (labels); 128^2; one world tick = 250 native steps = 5 time units; stirring-channel
            noise. Study tick = 1 world tick.
  membrane  the phase-membrane world (`../../track1/membrane_world`, unchanged): fields phi (phase), S (substrate),
            K (catalyst), L (links); 128^2; one world tick = 20 native steps = 10 time units; substrate-channel
            noise. Study tick = 4 world ticks = 40 time units (vw.stride), chosen from the CPU pilot cpilot.py
            (results/pilot_membrane.json): at 1-16 world ticks every block variable is almost perfectly persistent.
and, as an anchor judged with exactly the same code, on
  gliders   round 4's world (`../../../vw1/port/aworld.py`, 'coarse' spec, unchanged): fields c0, c1 (two matter
            channels whose sum is conserved); widths c = 1 only.
One world per process (env B5_WORLD). Encoders read the raw level-0 state (NCH x 128 x 128, standardised per field)
and output c numbers per 16-px block on the 8 x 8 block grid (64 c numbers):
  N<h>  local, translation-equivariant (stride 16, periodic), receptive field = block + h px halo (h = 0, 8),
        nonlinear: a linear window plus a zero-initialised nonlinear branch (pixel MLP -> window -> MLP)
  L<h>  the same window, linear only
  U     unconstrained control: dense map of the whole field (+ MLP residual), 64 c x 64 c whitening;
  Uc    the same dense encoder with the local encoders' per-channel (c x c) whitening
  Every encoder has the same training settings (steps, batch, learning-rate schedule, no weight decay).
Objectives: recon (each block's content from its own latent), clos (the whitened latent predicts itself at
h = 1, 4, 16 from 2 lags, global linear head), local (the same with one shared local rule on the 3 x 3
neighbourhood). Widths c = 1, 2. Two seeds, each fitted on both halves (cross-fitting as round 4).
Layout per half: J_CERT certification trajectories with fresh-noise branches (test ticks 40/100/160/220,
R_BR = 5 branches x TB = 16 ticks; the base continuation is replicate 0) plus J_EXTRA training-only trajectories.
"""
from __future__ import annotations

import importlib.util
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
WORLD_DIRS = {"vortex": os.path.join(VEC, "program", "track1", "vortex_world"),
              "membrane": os.path.join(VEC, "program", "track1", "membrane_world"), "gliders": PORT}

WORLD = os.environ.get("B5_WORLD", "vortex")
assert WORLD in WORLD_DIRS, WORLD
TINY = os.environ.get("B5_TINY", "0") == "1"
SEEDS = {"vortex": {"A": 9711, "B": 9712}, "membrane": {"A": 9721, "B": 9722},
         "gliders": {"A": 9731, "B": 9732}}[WORLD]                     # designer seeds (new; round 4 used 9701/9702)
HALVES = ("A", "B")
HZ = [1, 2, 4, 8, 16]                   # certification horizons (ticks)
HTR = (1, 4, 16)                        # training horizons (clos, local)
RF = (0, 8)                             # halo widths (px) of the local encoders
CS = (1,) if WORLD == "gliders" else (1, 2)    # latent channels per block
G, BS, NPIX = 8, 16, 128                # block grid, block size, field size
FIELDS = {"vortex": ("om", "Y", "a", "b"), "membrane": ("phi", "S", "K", "L"), "gliders": ("c0", "c1")}[WORLD]
NCH = len(FIELDS)                       # level-0 fields = encoder input channels (FIELDS order)
FLAT_ORDER = {"vortex": ("Y", "a", "b", "om"), "membrane": ("K", "L", "S", "phi"),
              "gliders": ("c0", "c1")}[WORLD]                           # vw.flat leaf order of the level-0 state
TICK_TIME = {"vortex": 5.0, "membrane": 10.0, "gliders": 1.0}[WORLD]   # time units per WORLD tick (gliders: ticks)
STRIDE = int(os.environ.get("B5_STRIDE", {"vortex": 1, "membrane": 4, "gliders": 1}[WORLD]))   # world ticks per STUDY tick
PILOT = os.environ.get("B5_PILOT", "0") == "1"       # small CPU look at the real world's time scales (hand designs only)
if TINY:
    J_CERT, J_EXTRA, T, TEST, TB, R_BR, CH, CB, BURN = 4, 0, 36, (18,), 16, 1, 6, 8, 4
elif PILOT:
    J_CERT, J_EXTRA, T, TEST, TB, R_BR, CH, CB, BURN = 8, 0, 120, (40, 80), 16, 3, 10, 8, 100
else:
    J_CERT, J_EXTRA, T, TEST, TB, R_BR, CH, CB, BURN = 32, 32, 300, (40, 100, 160, 220), 16, 5, 10, 8, 100
if WORLD == "gliders":
    BURN = 0                            # the gliders spec burns in inside its initial law (50 ticks), as round 4
elif WORLD == "membrane" and not TINY:
    BURN = 50                           # study ticks = 200 world ticks = 2,000 time units (cells formed, box means flat)
J_ALL = J_CERT + J_EXTRA
HSMOOTH = (0, 8) if TINY else (0, 4, 8, 16)   # hand-design windows: block mean (0), tents with a 4/8/16-px halo

# hand designs: c = 1 base features (each at every HSMOOTH window) and multi-channel designs (block means)
BASE1 = {"vortex": ("om", "absom", "ens", "Y", "a", "b", "lab", "dab", "kb"),
         "membrane": ("phi", "S", "K", "L", "wall", "phiK", "area"),
         "gliders": ("mass", "c0", "c1", "dc", "msq")}[WORLD]
MULTI = {"vortex": {"kinds": ("ka", "kb"), "absomY": ("absom", "Y"), "ab": ("a", "b"),
                    "pooled": ("om", "absom", "Y", "kb"), "fields": ("om", "Y", "a", "b")},
         "membrane": {"phiS": ("phi", "S"), "cells": ("phi1k", "phiK"), "KL": ("K", "L"),
                      "fields": ("phi", "S", "K", "L")},
         "gliders": {"fields": ("c0", "c1")}}[WORLD]
SFAX = {"vortex": ("om", "absom", "ens", "Y", "a", "b", "kb"),          # sfax features (no exact linear combinations)
        "membrane": ("phi", "S", "K", "L", "wall", "phiK", "area"), "gliders": ("c0", "c1", "msq")}[WORLD]
CLOSED = ("sfa_c1", "sfa_c2", "sfax_c1", "sfax_c2", "pca_c1")      # closed forms fitted on the other half
HAND_DOC = {
    "vortex": {"om": "vorticity", "absom": "|vorticity| (circulation magnitude; the vortex tracker's mass)",
               "ens": "vorticity^2 (enstrophy)", "Y": "fuel", "a": "label a", "b": "label b", "lab": "a + b",
               "dab": "b - a", "kb": "|om| b / (a + b + 1e-3) (label-weighted vorticity, kind b)",
               "ka": "|om| a-share (kind a)"},
    "membrane": {"phi": "phase (phi mass)", "S": "substrate", "K": "catalyst", "L": "links",
                 "wall": "4 phi (1 - phi)", "phiK": "phi clip(K, 0, 1)", "phi1k": "phi (1 - clip(K, 0, 1))",
                 "area": "1[phi > 0.5] (cell area)"},
    "gliders": {"mass": "c0 + c1 (conserved in total)", "c0": "matter channel 0", "c1": "matter channel 1",
                "dc": "c0 - c1", "msq": "(c0 + c1)^2"}}[WORLD]


def hand_names():
    """All hand / closed-form designs: [(name, c)]."""
    out = [(f"{f}_h{h}", 1) for f in BASE1 for h in HSMOOTH]
    out += [(k, len(v)) for k, v in MULTI.items()]
    out += [(k, int(k[-1])) for k in CLOSED]
    return out


def agree_targets():
    """Hand designs every certified Phi is compared with (per-block local readouts, both directions)."""
    return [f"{f}_h{h}" for f in BASE1 for h in (0, 8)] + list(MULTI) + ["sfa_c1", "sfax_c1"]


def _load_by_path(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def setup_paths(closure: bool = False, world: bool = False):
    """Put this checkout's vw first. closure: closure_lib (integrate/analyze) and lphi (learned_phi2), with the
    port's _paths loaded from this checkout (so the VW-0 estimator code comes from here, not from a second copy on
    the machine). world: the world's folder (its own _paths module; never together with closure)."""
    assert not (closure and world)
    for p in (VW1,):
        if p not in sys.path:
            sys.path.insert(0, p)
    import vw  # noqa: F401
    assert os.path.abspath(vw.__file__).startswith(VW1), vw.__file__
    if world:
        wd = WORLD_DIRS[WORLD]
        _load_by_path("_paths", os.path.join(wd, "_paths.py"))
        for p in (VW1, wd):                      # the world's _paths put another vw1 first; restore ours
            if p in sys.path:
                sys.path.remove(p)
            sys.path.insert(0, p)
        return None
    if closure:
        _load_by_path("_paths", os.path.join(PORT, "_paths.py"))
        for p in (LPHI_DIR, CLOSURE_SCRIPTS, VW1, PORT):
            if p in sys.path:
                sys.path.remove(p)
            sys.path.insert(0, p)
        import closure_lib as CL
        import lphi as LP
        assert os.path.abspath(CL.__file__).startswith(VEC) and os.path.abspath(LP.__file__).startswith(VEC)
        assert os.path.abspath(CL.AN.__file__).startswith(VEC), CL.AN.__file__
        LP.TEST = list(TEST)
        LP.NJ = J_CERT
        LP.HZ = list(HZ)
        return CL, LP
    return None


def work_dir(*sub):
    w = os.environ.get("B5_WORK", os.path.join(HERE, "work"))
    p = os.path.join(w, WORLD, *sub)
    os.makedirs(p, exist_ok=True)
    return p


def out_root():
    o = os.environ.get("B5_OUT", os.path.join(HERE, "out"))
    os.makedirs(o, exist_ok=True)
    return o


def out_dir(*sub):
    """$B5_OUT/<world>/..."""
    p = os.path.join(out_root(), WORLD, *sub)
    os.makedirs(p, exist_ok=True)
    return p


def progress(msg):
    line = f"{time.strftime('%H:%M:%S')} {msg}"
    print(line, flush=True)
    try:
        with open(os.path.join(out_root(), "progress.txt"), "a") as f:
            f.write(line + "\n")
    except OSError:
        pass


def deadline(kind: str) -> float:
    """Epoch seconds after which no new work of this kind starts ('sim' | 'train' | 'cert'); inf if unset."""
    v = os.environ.get({"sim": "B5_SIM_DEADLINE", "train": "B5_TRAIN_DEADLINE", "cert": "B5_CERT_DEADLINE"}[kind])
    return float(v) if v else float("inf")


def jdump(obj, path, indent=1):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(jsonable(obj), f, indent=indent, separators=(",", ":") if indent is None else None)
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
def cname(e, h, o, c):
    return f"{e}{'' if h is None else h}_{o}_c{c}"


ARMS = os.environ.get("B5_ARMS", "grid")   # "grid": the round-5 grid; "w": the follow-up job (see configs)


def configs():
    """Training configs in priority order: (name, enc, h, obj, c). enc in N, L, U, Uc; h None for U / Uc.
    B5_ARMS=w (follow-up job): closure with a global head at c = 1 for the encoders Lw / Nw (L / N trained on spatially
    whitened latents, so that the loss weights all 64 spatial modes equally instead of by their variance), plus the
    L / N closure configs again as references on the same simulated data."""
    out = []
    add = lambda e, h, o, c: out.append((cname(e, h, o, c), e, h, o, c))      # noqa: E731
    if ARMS == "w":
        for e in ("Lw", "Nw", "L", "N"):
            for h in RF:
                add(e, h, "clos", 1)
        if TINY:
            out = [x for x in out if x[0] in {"Lw0_clos_c1", "Nw8_clos_c1", "L0_clos_c1"}]
        return out
    assert ARMS == "grid", ARMS
    for c in CS:
        for e in ("N", "L"):
            for h in RF:
                for o in ("clos", "recon", "local"):
                    add(e, h, o, c)
        for o in ("clos", "recon", "local"):
            add("U", None, o, c)
        if c == 1:
            add("Uc", None, "clos", 1)
            add("Uc", None, "local", 1)
    if TINY:
        keep = {"N0_clos_c1", "N8_recon_c1", "N8_local_c2", "L0_local_c1", "L8_clos_c2", "L8_recon_c1", "U_clos_c1",
                "U_recon_c2", "Uc_local_c1"}
        out = [x for x in out if x[0] in keep]
    return out


RANDOM = (("rand0_c1", 0, 1), ("rand8_c1", 8, 1))   # untrained random linear windows (2 seeds each)
