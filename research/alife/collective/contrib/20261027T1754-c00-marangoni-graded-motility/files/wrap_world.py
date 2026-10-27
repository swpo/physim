"""Wrapper around c34's Marangoni rods (20261026T0505-c34-nematic-marangoni/world.py) for the bistability test.

It changes at most two things, set by the environment variable WRAP (JSON); WORLD_P still reaches the base world:
  "ramp":   [[t0, mar0], [t1, mar1], ...]  piecewise-linear Marangoni coefficient mar(t) (t = steps x dt);
            mar is held at the end values outside the breakpoints. Absent: mar stays at the base world's value.
  "snoise": eps >= 0, conserved (Dean-Kawasaki-like) noise on the surfactant s, added after every base step:
            each cell face carries a random transfer F = sqrt(2 Ds eps dt) sqrt(s_face) xi (xi ~ N(0,1) iid per face
            and step, s_face = mean of the two cells), s_i -= F, s_j += F, i.e. s <- s - div_FD(F) (dx = 1). In
            equilibrium var(s_cell) = eps s, so eps is the inverse number of molecules per unit s per cell. Each
            transfer is limited to a quarter of the donor cell's content, so s stays >= 0 and total s is conserved
            exactly; the fraction of limited transfers is counted and reported.
  "pnoise": eps >= 0, conserved Model-B noise on the body field phi: phi <- phi - sqrt(2 M eps dt) / dx^2 div_FD(xi),
            dealiased (optional arm; it can nucleate bodies in the metastable bath).
  "dump":   path of an .npz written at exit with, for every recorded frame, the flow (vx, vy) and s as float16,
            mar(t), and the noise bookkeeping. labkit calls fields() once per frame, so record k is frame k.
The noise uses its own generator, default_rng(seed + 7919), so the initial condition is the base world's for the seed.
"""
import atexit, importlib.util, json, os
import numpy as np
from numpy.fft import fft2, ifft2

BASE = "/home/user/physim/research/alife/collective/contrib/20261026T0505-c34-nematic-marangoni/world.py"
_spec = importlib.util.spec_from_file_location("c34_marangoni_base", BASE)
B = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(B)

CFG = json.loads(os.environ.get("WRAP", "{}"))
META = dict(B.META)
META["name"] = "active-nematic-marangoni-wrap"
META["mutation"] = "wrapper: mar(t) ramp and/or conserved surfactant / body noise (bistability test)"
P = B.P

_g = {"n": 0, "rng": None, "rec": [], "clip": 0.0, "added_abs": 0.0}


def mar_of_t(t):
    r = CFG.get("ramp")
    if not r:
        return P["mar"]
    ts = [a for a, _ in r]; ms = [b for _, b in r]
    return float(np.interp(t, ts, ms))


def init(seed, size):
    s = B.init(seed, size)
    _g["rng"] = np.random.default_rng(int(seed) + 7919)
    _g["n"] = 0
    if CFG.get("ramp"):
        P["mar"] = mar_of_t(0.0)
    return s


def _cons_noise(f, amp, mult, da, dx):
    """-amp * div_FD(mult_face * xi), dealiased; mult is a per-cell array (or None)."""
    rng = _g["rng"]
    xi_x = rng.standard_normal(f.shape); xi_y = rng.standard_normal(f.shape)
    if mult is not None:
        mx = np.sqrt(np.maximum(0.5 * (mult + np.roll(mult, -1, 1)), 0))
        my = np.sqrt(np.maximum(0.5 * (mult + np.roll(mult, -1, 0)), 0))
        xi_x *= mx; xi_y *= my
    div = (xi_x - np.roll(xi_x, 1, 1)) + (xi_y - np.roll(xi_y, 1, 0))
    d = -amp / dx ** 2 * ifft2(fft2(div) * da).real
    return d


def step(s):
    t = _g["n"] * P["dt"]
    if CFG.get("ramp"):
        P["mar"] = mar_of_t(t)
    s = B.step(s)
    dx = P["dx"]
    eps = float(CFG.get("snoise", 0.0))
    if eps > 0:
        sf = s["s"]; amp = np.sqrt(2 * P["Ds"] * eps * P["dt"]); rng = _g["rng"]
        d = np.zeros_like(sf); nlim = 0
        for ax in (1, 0):
            sj = np.roll(sf, -1, ax)
            F = amp * np.sqrt(np.maximum(0.5 * (sf + sj), 0)) * rng.standard_normal(sf.shape)
            Fc = np.clip(F, -0.25 * sj, 0.25 * sf)  # positive F moves mass from cell i to its neighbour j = i+1
            nlim += int((Fc != F).sum())
            d -= Fc; d += np.roll(Fc, 1, ax)
        _g["clip"] += nlim / (2.0 * sf.size)  # summed per step: mean over steps = fraction of limited transfers
        _g["added_abs"] += float(np.abs(d).sum())
        s["s"] = sf + d
    pe = float(CFG.get("pnoise", 0.0))
    if pe > 0:
        s["phi"] = s["phi"] + _cons_noise(s["phi"], np.sqrt(2 * P["M"] * pe * P["dt"]), None, s["da"], dx)
    _g["n"] += 1
    return s


def fields(s):
    if CFG.get("dump"):
        _g["rec"].append((_g["n"], P["mar"], s["vx"].astype(np.float16), s["vy"].astype(np.float16),
                          s["s"].astype(np.float16), float(s["s"].sum())))
    return B.fields(s)


def stats(s):
    d = B.stats(s); d["mar"] = round(float(P["mar"]), 3)
    return d


def _dump():
    path = CFG.get("dump")
    if not path or not _g["rec"]:
        return
    n, mar, vx, vy, sf, stot = zip(*_g["rec"])
    np.savez_compressed(path, n=np.array(n), mar=np.array(mar), vx=np.stack(vx), vy=np.stack(vy), s=np.stack(sf),
                        s_total=np.array(stot), dt=P["dt"], clip_frac=_g["clip"] / max(_g["n"], 1), added_abs=_g["added_abs"], cfg=json.dumps(CFG),
                        world_p=json.dumps({k: v for k, v in P.items() if isinstance(v, (int, float, str))}))


atexit.register(_dump)
