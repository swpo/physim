"""Wave-pinning crawler (percell=1: synthesis fixed per cell, so the protein total relaxes to Ncell; one cell per run) (20261025T1955-c22-wavepin-front-competition-claim/world.py, imported unchanged) with
polarity-protein turnover: protein is made in the cytosol at ksyn * S per unit cell area and both forms decay at
kdeg, so a cell's protein total relaxes to ksyn * S * area / kdeg instead of being fixed at C. S is a resource:
held at 1 (res=0), or a field that diffuses, is consumed by synthesis and regrows at kS (res=1).
Overrides: WORLD_P (also passed to the crawler: cut_t, cut_mode, cut_frac, ...)."""
import importlib.util, json, os
import numpy as np

_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "20261025T1955-c22-wavepin-front-competition-claim", "world.py")
_p = os.path.normpath(_p)
_spec = importlib.util.spec_from_file_location("wavepin_base", _p)
B = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(B)
Q = dict(ksyn=0.46, kdeg=0.2, percell=0, Ncell=6.0, res=0, DS=1.0, kS=0.5, ycons=1.0, S_fork=-1.0)
Q.update(json.loads(os.environ.get("WORLD_P", "{}")))
META = dict(B.META); META["name"] = "wavepin-crawler-synth"; META["channels"] = ["phi (cell)", "rho (polarity, inside)", "phi*rho", "S resource"]
META["mutation"] = "polarity protein made in the cytosol from a resource S (ksyn S) and degraded (kdeg): protein total no longer fixed"


def init(seed, size):
    s = B.init(seed, size)
    s["S"] = np.ones_like(s["phi"])
    return s


def step(s):
    s = B.step(s)
    dt = B.P["dt"]; inside = s["phi"] > 0.01
    S = s["S"]
    if Q["percell"]:   # per-cell synthesis: kdeg * Ncell per cell, spread over its area (protein total relaxes to Ncell)
        A = max((s["phi"] * inside).sum() * s["dx"] ** 2, 1e-6)
        syn = Q["kdeg"] * Q["Ncell"] / A * S * inside
    else:              # per-area synthesis: protein total relaxes to ksyn * S * area / kdeg
        syn = Q["ksyn"] * S * inside
    s["cyt"] = s["cyt"] + dt * (syn - Q["kdeg"] * s["cyt"]) * inside
    s["rho"] = s["rho"] * (1 - dt * Q["kdeg"])
    if Q["res"]:
        kS = 0.0 if (Q["S_fork"] >= 0 and s["t"] >= Q["S_fork"]) else Q["kS"]
        lap = (np.roll(S, 1, 0) + np.roll(S, -1, 0) + np.roll(S, 1, 1) + np.roll(S, -1, 1) - 4 * S) / s["dx"] ** 2
        s["S"] = np.clip(S + dt * (Q["DS"] * lap - Q["ycons"] * syn * s["phi"] + kS * (1 - S)), 0, None)
    return s


def fields(s):
    f = B.fields(s)
    return np.concatenate([f, s["S"][None]])


def damage(s, mask):
    return B.damage(s, mask)


polarity, cut, P = B.polarity, B.cut, B.P
rho_cyt = B.rho_cyt
