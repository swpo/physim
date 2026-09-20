
"""Predictive model for the laboratory world.

World: 2-D field with 4 channels, sampled by two poseable arrays plus 2 global
probes.

- device0: 13 sensors on a square-lattice plus (spacing 1)
- device1: 19 sensors on a hexagonal lattice (spacing 2)
- inject port p adds a narrow Gaussian (lambda ~ 1.125) into channel p at the
  injecting device origin. Extra state follows a 4 x 4 linear ODE.
- adjust u is cumulative: translation (u0,u1) and isotropic scale (u2)
- background: a moving Gaussian bump (advection in +y) plus a second weaker bump
"""

import os
import numpy as np
from numpy.linalg import inv
from scipy.linalg import expm
from scipy.interpolate import RBFInterpolator
from scipy.spatial import cKDTree

SLOTS = {"device0": 13, "device1": 19, "global": 2}

# ---- geometry ----
_SQRT3 = np.sqrt(3.0)
POS0 = np.array([
    [0.0, 1.0],
    [1.0, 0.0],
    [-2.0, 0.0],
    [-1.0, 1.0],
    [-1.0, 0.0],
    [-1.0, -1.0],
    [0.0, 0.0],
    [1.0, 1.0],
    [0.0, 2.0],
    [2.0, 0.0],
    [0.0, -1.0],
    [0.0, -2.0],
    [1.0, -1.0],
], dtype=float)

POS1 = np.array([
    [0.0, -4.0],
    [-2 * _SQRT3, 2.0],
    [-_SQRT3, 3.0],
    [_SQRT3, 3.0],
    [0.0, -2.0],
    [0.0, 4.0],
    [-_SQRT3, -1.0],
    [-2 * _SQRT3, 0.0],
    [-2 * _SQRT3, -2.0],
    [0.0, 2.0],
    [0.0, 0.0],
    [2 * _SQRT3, -2.0],
    [-_SQRT3, 1.0],
    [2 * _SQRT3, 2.0],
    [_SQRT3, -3.0],
    [_SQRT3, -1.0],
    [2 * _SQRT3, 0.0],
    [_SQRT3, 1.0],
    [-_SQRT3, -3.0],
], dtype=float)

# global: far sensors along +y / slightly off; distances from inject kernel
POSG = np.array([
    [0.0, 2.40],
    [0.15, 2.61],
], dtype=float)

ALPHA = 0.3345  # world translation per unit cumulative u_xy
LAM_INJ = 1.12547  # inject spatial Gaussian

# scale s(u2)
_U2_KNOTS = np.array([-1.0, -0.5, 0.0, 0.5, 1.0])
_S_KNOTS = np.array([0.50, 0.604, 1.0, 1.644, 2.685])

# linear extra dynamics  dx/dt = L x + B u
L = np.array([
    [-0.5498,  0.9774,  0.0923,  0.1510],
    [ 0.3136, -1.9424, -0.4198, -0.9818],
    [ 0.0000,  0.0000, -0.0050,  0.0000],
    [ 0.3174,  0.1126, -0.0014, -0.4222],
], dtype=float)

B = np.array([
    [ 0.4827,  0.0059, -0.0083, -0.0138],
    [-0.1185,  0.8192, -0.0136, -0.0092],
    [ 0.0016, -0.0043,  1.0000,  0.0000],
    [-0.0322,  0.0029,  0.0002,  0.9854],
], dtype=float)

_L_INV = inv(L)

# second bump (device1 slot 8 neighbourhood)
BUMP2_XY = np.array([-2 * _SQRT3, -2.0])
BUMP2_AMP = np.array([0.310, 1.20, 0.003, 0.530])  # extra on top of bg
BUMP2_LAM = 1.05
BUMP2_DECAY = 0.012  # 1/tau for amplitude

# noise scales (std ~ k * t)
_NOISE_K = np.array([3.2e-5, 1.6e-4, 5e-7, 5.5e-5])


def _load_baseline():
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "model_data.npz")
    if not os.path.isfile(path):
        path = "/workspace/model_data.npz"
    data = np.load(path)
    return data["base_t"], data["base_d0"], data["base_d1"], data["base_g"]


_BASE_T, _BASE_D0, _BASE_D1, _BASE_G = _load_baseline()


def _scale(u2):
    u2 = float(u2)
    if u2 <= _U2_KNOTS[0]:
        # s(-1)=0.5; geometric-ish extrapolation
        return 0.5 * (0.5 ** (-(u2 + 1.0)))
    if u2 >= _U2_KNOTS[-1]:
        ratio = _S_KNOTS[-1] / _S_KNOTS[-2]
        return _S_KNOTS[-1] * (ratio ** (u2 - 1.0))
    return float(np.interp(u2, _U2_KNOTS, _S_KNOTS))


def _pose(cum_u):
    """Return origin T (2,) and scale s from cumulative u (3,)."""
    T = ALPHA * np.asarray(cum_u[:2], dtype=float)
    s = _scale(cum_u[2])
    return T, s


def _sensor_world(device, cum_u):
    T, s = _pose(cum_u)
    if device == 0:
        return T + s * POS0
    if device == 1:
        return T + s * POS1
    return POSG.copy()  # global is world-fixed


def _blob_params(t):
    """Moving bump (ch0-centered). Quadratic fits from baseline."""
    t = float(t)
    cx = -0.005991 - 0.002897 * t + 0.000095 * t * t
    cy = -0.119875 + 0.027316 * t + 0.000039 * t * t
    A0 = 0.566534 - 0.000101 * t - 0.000004 * t * t
    lam0 = 0.441668 + 0.001275 * t - 0.000014 * t * t
    bg0 = -0.031222 + 0.000522 * t - 0.000002 * t * t
    A3 = 1.242 - 0.0012 * t
    lam3 = 0.510 + 0.0013 * t
    bg3 = -0.170 + 0.0017 * t
    A1 = 2.05
    lam1 = 1.13
    bg1 = -0.92
    return cx, cy, A0, lam0, bg0, A1, lam1, bg1, A3, lam3, bg3


def _field_blob(xy, t):
    """Smooth trend field at world points xy (N,2) -> (N,4)."""
    cx, cy, A0, lam0, bg0, A1, lam1, bg1, A3, lam3, bg3 = _blob_params(t)
    d2 = (xy[:, 0] - cx) ** 2 + (xy[:, 1] - cy) ** 2
    out = np.zeros((xy.shape[0], 4))
    out[:, 0] = A0 * np.exp(-lam0 * d2) + bg0
    # ch1: difference-of-Gaussians peak tracking the bump
    out[:, 1] = 636.0 * np.exp(-1.852 * d2) - 634.0 * np.exp(-1.862 * d2) - 0.95
    out[:, 2] = 0.003
    out[:, 3] = A3 * np.exp(-lam3 * d2) + bg3
    d2b = (xy[:, 0] - BUMP2_XY[0]) ** 2 + (xy[:, 1] - BUMP2_XY[1]) ** 2
    decay = np.exp(-BUMP2_DECAY * t)
    g2 = np.exp(-BUMP2_LAM * d2b) * decay
    out += g2[:, None] * BUMP2_AMP[None, :]
    return out


def _expm(mat):
    return expm(mat)


def _extra_state(t, t0, dur, amp, port):
    """4-vector extra amplitude at time t for one inject event."""
    if t <= t0 + 1e-12:
        return np.zeros(4)
    u = B[:, port] * float(amp)
    dt_on = min(max(t - t0, 0.0), dur)
    # s_on = L^{-1} (expm(L dt_on) - I) u
    e_on = _expm(L * dt_on)
    s = _L_INV @ (e_on - np.eye(4)) @ u
    if t > t0 + dur + 1e-12:
        s = _expm(L * (t - t0 - dur)) @ s
    return s


def _parse_actions(actions):
    """Respect list order at equal times (inject origin uses pose after prior adjusts)."""
    injects = []
    adjusts = []
    u_now = [np.zeros(3), np.zeros(3)]
    origins = []
    for a in actions:
        kind = a.get("kind")
        if kind == "adjust":
            dev = int(a["device"])
            du = np.asarray(a["u"], dtype=float).reshape(3)
            u_now[dev] = u_now[dev] + du
            adjusts.append((float(a["t"]), dev, du.copy()))
        elif kind == "inject":
            dev = int(a["device"])
            T, _s = _pose(u_now[dev])
            inj = {
                "t": float(a["t"]),
                "device": dev,
                "port": int(a["port"]),
                "amp": float(a["amp"]),
                "dur": float(a["dur"]),
            }
            injects.append(inj)
            origins.append(T.copy())
    return injects, adjusts, origins


def _cum_u_at(adjusts, device, t):
    """Cumulative u for device at time t (all adjusts with ta <= t)."""
    u = np.zeros(3)
    for ta, dev, du in adjusts:
        if dev != device:
            continue
        if ta <= t + 1e-12:
            u = u + du
    return u


def _is_default_pose(adjusts, device, t):
    u = _cum_u_at(adjusts, device, t)
    return np.max(np.abs(u)) < 1e-12


def _interp_baseline(sensor, t):
    """Linear interpolate stored default-pose baseline. t scalar."""
    t = float(t)
    tt = _BASE_T
    if sensor == "device0":
        arr = _BASE_D0
    elif sensor == "device1":
        arr = _BASE_D1
    else:
        arr = _BASE_G
    if t <= tt[0]:
        return arr[0].copy()
    if t >= tt[-1]:
        return arr[-1].copy()
    i = int(np.searchsorted(tt, t, side="right") - 1)
    i = max(0, min(i, len(tt) - 2))
    w = (t - tt[i]) / (tt[i + 1] - tt[i])
    return (1.0 - w) * arr[i] + w * arr[i + 1]


def _extras_at_points(xy, t, injects, origins):
    """Sum of extra Gaussians at world points xy (N,2) -> (N,4)."""
    N = xy.shape[0]
    out = np.zeros((N, 4))
    if not injects:
        return out
    for inj, xin in zip(injects, origins):
        s = _extra_state(t, inj["t"], inj["dur"], inj["amp"], inj["port"])
        d2 = (xy[:, 0] - xin[0]) ** 2 + (xy[:, 1] - xin[1]) ** 2
        g = np.exp(-LAM_INJ * d2)
        out += g[:, None] * s[None, :]
    return out


_DEFAULT_PTS = np.vstack([POS0, POS1])  # (32, 2)
_DEFAULT_TREE = cKDTree(_DEFAULT_PTS)


def _interp_world_background(xy, t):
    """Trend + residual RBF of default-pose baseline to world points xy (N,2)."""
    v0 = _interp_baseline("device0", t)
    v1 = _interp_baseline("device1", t)
    vals = np.hstack([v0, v1]).T  # 32,4
    trend_pts = _field_blob(_DEFAULT_PTS, t)
    resid = vals - trend_pts
    rbf = RBFInterpolator(_DEFAULT_PTS, resid, kernel="thin_plate_spline", smoothing=1e-3)
    pred_resid = rbf(xy)
    dist, _ = _DEFAULT_TREE.query(xy, k=1)
    w = np.clip(1.0 - dist / 3.5, 0.0, 1.0) ** 2
    return _field_blob(xy, t) + w[:, None] * pred_resid


def _measure(sensor, t, injects, origins, adjusts):
    if sensor == "global":
        xy = POSG
        extra = _extras_at_points(xy, t, injects, origins)
        base = _interp_baseline("global", t)
        return base + extra.T
    device = 0 if sensor == "device0" else 1
    default = _is_default_pose(adjusts, device, t)
    if default:
        xy = POS0 if device == 0 else POS1
        extra = _extras_at_points(xy, t, injects, origins)
        base = _interp_baseline(sensor, t)
        return base + extra.T
    u = _cum_u_at(adjusts, device, t)
    xy = _sensor_world(device, u)
    bg = _interp_world_background(xy, t)
    extra = _extras_at_points(xy, t, injects, origins)
    return (bg + extra).T


def predict(actions, queries, n_samples=64, seed=0):
    actions = list(actions) if actions else []
    queries = list(queries) if queries else []
    injects, adjusts, origins = _parse_actions(actions)

    rng = np.random.default_rng(seed)
    samples_out = []
    for q in queries:
        sensor = q["sensor"]
        times = list(q.get("t", []))
        nslot = SLOTS.get(sensor, 0)
        nT = len(times)
        mean = np.zeros((nT, 4, nslot), dtype=float)
        for i, t in enumerate(times):
            mean[i] = _measure(sensor, float(t), injects, origins, adjusts)
        # noise
        t_arr = np.array(times, dtype=float) if nT else np.zeros(0)
        sig = _NOISE_K.reshape(1, 4, 1) * np.maximum(t_arr, 0.0).reshape(nT, 1, 1)
        sig = np.broadcast_to(sig, (nT, 4, nslot))
        noise = rng.normal(0.0, 1.0, size=(n_samples, nT, 4, nslot)) * sig
        out = mean[None, ...] + noise
        # keep finite
        np.clip(out, -50.0, 50.0, out=out)
        samples_out.append(out)
    return {"samples": samples_out}
