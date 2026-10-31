"""Privileged ablation variants of c53's fed vortices (controls only; never an agent-facing world).

The base world file is loaded from FV_BASE (default: c53's world.py) with the same WORLD_P overrides, and
step() is the base step with optional changes read from the overrides (all default off = the base step):

- ``sat_smooth`` (world units): the vorticity gain's saturation s uses |omega| smoothed by a periodic Gaussian
  of this standard deviation, so a thin neck inherits the gain of the body around it (eating is unchanged).
- ``fuel_smooth`` (world units): the growth term uses fuel smoothed by a periodic Gaussian (eating unchanged).
- ``grow_off``: no vorticity gain from fuel (k Y s term removed) while eating continues.
- ``body_gain``: inside every body (connected |omega| > ``body_thr``, periodic), the net gain (k Y s - mu) is
  replaced by its omega-weighted mean over the body, so each body's circulation budget per step is exactly the
  base world's while no part of a body grows or decays relative to another (no neck can starve); outside bodies
  the local gain is unchanged. Eating, fuel and advection are the base world's.
"""
from scipy import ndimage
import importlib.util, json, os
import numpy as np

_BASE = os.environ.get("FV_BASE", "/home/user/physim/research/alife/collective/contrib/20261027T0712-c53-fed-vortex-claim/world.py")
_spec = importlib.util.spec_from_file_location("fv_base_for_ablation", _BASE)
B = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(B)
ops = B.ops
META = dict(B.META, name="fed-vortices-ablation")
P = B.P
P.setdefault("sat_smooth", 0.0)
P.setdefault("fuel_smooth", 0.0)
P.setdefault("grow_off", 0.0)
P.setdefault("body_gain", 0.0)
P.setdefault("body_thr", 0.06)
fields = B.fields
_vel, _adv = B._vel, B._adv


def init(seed, size):
    return B.init(seed, size)


def _blur(f, sigma, s):
    k2 = s["kx"] ** 2 + s["ky"] ** 2
    return ops.irfft2(ops.rfft2(f) * np.exp(-0.5 * sigma ** 2 * k2), s["shape"])


def _plabel(mask):
    lab, n = ndimage.label(mask)
    if n == 0:
        return lab, 0
    parent = np.arange(n + 1)

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    for a, b in ((lab[0, :], lab[-1, :]), (lab[:, 0], lab[:, -1])):
        m = (a > 0) & (b > 0)
        for x, y in zip(a[m], b[m]):
            rx, ry = find(x), find(y)
            if rx != ry:
                parent[max(rx, ry)] = min(rx, ry)
    roots = np.array([find(i) for i in range(n + 1)])
    return roots[lab], n


def _body_mean(g, om, thr):
    lab, n = _plabel(np.abs(om) > thr)
    if n == 0:
        return g
    w = np.abs(om).ravel()
    num = np.bincount(lab.ravel(), weights=(g * np.abs(om)).ravel(), minlength=n + 1)
    den = np.bincount(lab.ravel(), weights=w, minlength=n + 1)
    mean = np.where(den > 0, num / np.where(den > 0, den, 1), 0.0)
    return np.where(lab > 0, mean[lab], g)


def step(s):
    q, dt, sh = s["par"], s["par"]["dt"], s["shape"]
    om, Y = s["om"], s["Y"]
    kF = q["kF"]
    if q["fork_t"] >= 0 and s["t"] >= q["fork_t"]:
        kF = 0.0
        if abs(s["t"] - q["fork_t"]) < dt / 2:
            Y = 0.0 * Y
    uy, ux = _vel(s)
    uy, ux = q["adv"] * uy, q["adv"] * ux
    w2 = om ** 2
    sat = w2 / (w2 + q["wi"] ** 2)
    eat = np.minimum(q["e"] * Y * sat * w2, Y / dt)
    gsat = sat
    if q.get("sat_smooth", 0) > 0:
        W = _blur(np.abs(om), q["sat_smooth"], s)
        gsat = W ** 2 / (W ** 2 + q["wi"] ** 2)
    Yg = _blur(Y, q["fuel_smooth"], s) if q.get("fuel_smooth", 0) > 0 else Y
    gain = 0.0 if q.get("grow_off", 0) else q["k"] * Yg * gsat
    net = gain - q["mu"]
    if q.get("body_gain", 0):
        net = _body_mean(net + 0.0 * om, om, q["body_thr"])
    nom = om + dt * (-_adv(om, uy, ux, s) + net * om)
    nY = Y + dt * (-_adv(Y, uy, ux, s) - eat + kF * (1 - Y))
    s["om"] = ops.irfft2(ops.rfft2(nom) * s["Lom"], sh)
    s["Y"] = np.clip(ops.irfft2(ops.rfft2(nY) * s["LY"], sh), 0, None)
    s["eat"] = eat
    s["t"] += dt
    return s
