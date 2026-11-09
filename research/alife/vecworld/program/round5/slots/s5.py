"""s5 -- shared pieces of the round-5 study `slots` (track 1): an object-centric bias on raw Flow-Lenia gliders.

Question: do objects emerge from an objective plus an object-centric architecture, or does the tracker's
hand-written logic (vw.objects.BlobTracker) carry something the objective does not supply?

Every Phi here is a transducer (x_t, memory) -> (K = 12 slots x a few numbers, memory'): a deterministic causal
function of the level-0 history (fixed, non-random initialisation at tick 0; memory carried from tick to tick).
  trk        the tracker's object view (reference; 12 numbers per slot)
  km*        no learning: soft k-means on the matter field, centres carried over (moment readout)
  grid       no learning: 12 fixed regions (k-means with frozen centres; the Eulerian control, moment readout)
  sam_<obj>  slot attention with memory, MOMENT readout: only the masks are learned; each slot reports the
             moments of the matter under its mask in the tracker's own 12-number layout
  sac_<obj>  slot attention with memory, CODE readout: d = 6 learned numbers per slot
Objectives <obj>: rec (reconstruction control), set (closure: slots predict their own future, slot-slot interaction
allowed), self (local law: one shared rule per slot, own past only). Collapse guard for set / self: the error is
measured in the metric of the JOINT covariance of the 72 slot numbers (running estimate + relative ridge). That
metric stops slots from shrinking their numbers, but a direction whose variance falls below the ridge (an empty or
constant slot) drops out of the loss, so emptying slots lowers it; the '_dg' configs add the dead-direction term
(snets.closure_loss), under which a dead direction counts as unexplained and the mean predictor scores exactly 1.
Layout (cross-fitting as round4/bias): two halves A, B; per half J_CERT trajectories with fresh-noise branches
(test ticks, R_BR branches x TB ticks; replicate 0 = the base continuation) plus J_EXTRA training-only
trajectories. A Phi fitted on one half is certified on the other half.
"""
from __future__ import annotations

import json
import math
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

SIZE = os.environ.get("S5_SIZE", "full")          # tiny (code path) | dev (CPU pilot) | pilot (GPU pilot) | full
SEEDS = {"A": 9801, "B": 9802}                    # designer seeds (new); branch keys from seed + 50
HALVES = ("A", "B")
HZ = [1, 2, 4, 8, 16]                             # certification horizons
HTR = (1, 4, 16)                                  # training horizons (set, self)
K, NF, NS = 12, 12, 17                            # slots, tracker features per slot, tracker table columns
NPIX = 128
DC = 6                                            # numbers per slot of the code readout / of the loss sub-vector
MP6 = (1, 3, 4, 5, 6, 7)                          # mass, x_cos, x_sin, y_cos, y_sin, rg of the 12-number layout
M_MIN = 20.0                                      # the tracker's m_min (A_gliders): the presence scale
if SIZE == "tiny":
    J_CERT, J_EXTRA, T, TEST, TB, R_BR, CH, CB, BURN, N_VAL = 4, 2, 48, (24,), 16, 2, 8, 8, 2, 1
elif SIZE == "dev":
    J_CERT, J_EXTRA, T, TEST, TB, R_BR, CH, CB, BURN, N_VAL = 4, 2, 64, (40,), 16, 2, 8, 8, None, 1
elif SIZE == "pilot":
    J_CERT, J_EXTRA, T, TEST, TB, R_BR, CH, CB, BURN, N_VAL = 16, 32, 300, (40, 100, 160, 220), 16, 5, 10, 8, None, 4
else:
    J_CERT, J_EXTRA, T, TEST, TB, R_BR, CH, CB, BURN, N_VAL = 32, 64, 300, (40, 100, 160, 220), 16, 5, 10, 8, None, 8
J_ALL = J_CERT + J_EXTRA


def setup_paths(closure: bool = False):
    """Port first (vw, aworld); optionally closure_lib (integrate/analyze) and lphi (learned_phi2). closure_lib and
    lphi put absolute paths of the development container in front of sys.path; importing _paths, vw and analyze from
    THIS tree first keeps every module on the tree the job was archived from (checked)."""
    for p in (VW1, PORT):
        if p not in sys.path:
            sys.path.insert(0, p)
    import _paths  # noqa: F401
    if not closure:
        return None
    import vw  # noqa: F401
    import analyze  # noqa: F401
    for p in (LPHI_DIR, CLOSURE_SCRIPTS):
        if p not in sys.path:
            sys.path.insert(0, p)
    import closure_lib as CL
    import lphi as LP
    for m in (_paths, vw, analyze, CL, LP):
        assert os.path.abspath(m.__file__).startswith(VEC), f"{m.__name__} imported from {m.__file__}, not from {VEC}"
    LP.TEST = list(TEST)
    LP.NJ = J_CERT
    LP.HZ = list(HZ)
    CL.AN.HORIZONS = list(HZ)
    return CL, LP


def work_dir(*sub):
    w = os.environ.get("S5_WORK", os.path.join(HERE, "work"))
    p = os.path.join(w, *sub)
    os.makedirs(p, exist_ok=True)
    return p


def out_dir(*sub):
    o = os.environ.get("S5_OUT", os.path.join(HERE, "out"))
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
    v = os.environ.get({"train": "S5_TRAIN_DEADLINE", "cert": "S5_CERT_DEADLINE"}[kind])
    return float(v) if v else float("inf")


def jdump(obj, path):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(jsonable(obj), f, indent=1)
    os.replace(tmp, path)


def jsonable(o):
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
def learned_configs():
    """Learned encoders in priority order: dicts with name, readout ('mom' | 'code'), obj, geo (the k-means distance
    term in the attention; False = plain slot attention on content + absolute position), P (token size in px),
    stopcarry (no gradient through the carried memory), mem (carry the slots; False = the slots restart from the
    fixed initialisation at every tick, i.e. no memory), init_from (warm start of the encoder from that config).
    obj: 'set' | 'self' | 'rec' (s5 docstring), or 'sup': SUPERVISED imitation of the tracker's segmentation (a
    capacity control, not a candidate: can this architecture express the tracker's view at all?).
    dead: the dead-direction term is added to the closure / local-law loss (snets.closure_loss; '_dg' configs).
    Names: sa = geometric, sg = generic; m = moment readout, c = code readout; _ws = warm-started from sam_sup;
    _dg = with the dead-direction term. With S5_KEEP the configs run in the order S5_KEEP lists them (a warm-started
    config must come after the config it starts from)."""
    out = []

    def add(readout, obj, geo=True, P=4, stopcarry=False, mem=True, tag="", init_from=None, dead=False):
        nm = f"s{'a' if geo else 'g'}{'m' if readout == 'mom' else 'c'}_{obj}{tag}"
        out.append(dict(name=nm, readout=readout, obj=obj, geo=geo, P=P, stopcarry=stopcarry, mem=mem, init_from=init_from,
                        dead=dead))
    add("mom", "set")
    add("mom", "rec")
    add("mom", "sup")                                     # capacity control
    add("mom", "set", tag="_ws", init_from="sam_sup")     # does closure keep the tracker-like solution?
    add("code", "set")
    add("code", "rec")
    add("mom", "self")
    add("mom", "rec", tag="_ws", init_from="sam_sup")
    add("code", "rec", geo=False)                         # the classic slot-attention autoencoder (control)
    add("mom", "set", geo=False)                          # closure without the k-means prior
    add("code", "self")
    add("mom", "self", tag="_ws", init_from="sam_sup")
    add("mom", "set", stopcarry=True, tag="_sg")          # no backpropagation through the carried memory
    add("mom", "rec", mem=False, tag="_nomem")            # ablation: no memory (slots re-initialised every tick)
    add("mom", "rec", geo=False)
    add("code", "set", geo=False)
    add("mom", "set", tag="_dg", dead=True)               # closure / local law with the dead-direction term
    add("mom", "self", tag="_dg", dead=True)
    add("code", "set", tag="_dg", dead=True)
    add("mom", "set", tag="_ws_dg", init_from="sam_sup", dead=True)
    add("mom", "set", geo=False, tag="_dg", dead=True)
    if os.environ.get("S5_KEEP") or SIZE in ("tiny", "dev"):
        keep = os.environ.get("S5_KEEP", "sam_set_sg,sam_sup,sam_rec_ws,sgc_rec,sam_rec_nomem,sac_self").split(",")
        if os.environ.get("S5_KEEP_ORDER") == "1":
            unknown = [k for k in keep if k not in [c["name"] for c in out]]
            assert not unknown, f"S5_KEEP names unknown configs: {unknown}"
            out = sorted((c for c in out if c["name"] in keep), key=lambda c: keep.index(c["name"]))
        else:
            out = [c for c in out if c["name"] in keep]
    return out


def fixed_configs():
    """No-learning encoders: (name, kind, kwargs). kind 'km': soft k-means with carried centres
    (sigma = bandwidth in px, P = token size, prior = mass-proportional mixing weights); 'grid': frozen centres."""
    out = [("km_s6", "km", dict(sigma=6.0, P=4, prior=False)), ("km_s3", "km", dict(sigma=3.0, P=4, prior=False)),
           ("km_s6w", "km", dict(sigma=6.0, P=4, prior=True)), ("grid", "grid", dict(sigma=3.0, P=4, prior=False))]
    if SIZE in ("pilot", "full"):
        out.append(("km_s6_p1", "km", dict(sigma=6.0, P=1, prior=False)))
    return out


HAND = ("mass", "chan")                 # block views certified for reference (64 and 128 numbers)
