"""Shared setup for the curation checks of the fed vortices (c53) and phase_membrane.

Worlds are loaded fresh with parameter overrides; the initial state is rebuilt from the
world's own recipe (verified equal to ``init``), optionally rotated by 45 degrees (the white
draws are remapped by nearest neighbour, then the world's own isotropic smoothing is applied,
so the rotated field has no seams), and resampled to a finer grid at a fixed physical box.
Refined grids keep every coefficient in world units: fed vortices rescale nu, kY by s^2 and
hyper by s^4 (s = N/128; velocities are already in pixels per time); phase_membrane uses its
own ``scale`` option (diffusivities and drift x s^2) with dt lowered for explicit stability.
"""
from __future__ import annotations

import importlib.util
import json
import os
import sys

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import numpy as np
from scipy import ndimage

LAB = "/home/user/physim/research/alife"
if LAB not in sys.path:
    sys.path.insert(0, LAB)
PATHS = {
    "fv": f"{LAB}/collective/contrib/20261027T0712-c53-fed-vortex-claim/world.py",
    "pm": f"{LAB}/threads/autopoiesis/worlds/phase_membrane/world.py",
}
N0 = 128


def load(name, overrides=None):
    overrides = dict(overrides or {})
    old = os.environ.get("WORLD_P")
    os.environ["WORLD_P"] = json.dumps(overrides) if name == "fv" else "{}"
    try:
        spec = importlib.util.spec_from_file_location(f"cw_{name}_{abs(hash(json.dumps(overrides, sort_keys=True)))}",
                                                      PATHS[name])
        W = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(W)
    finally:
        if old is None:
            os.environ.pop("WORLD_P", None)
        else:
            os.environ["WORLD_P"] = old
    W.P.update(overrides)
    if hasattr(W, "ops"):
        W.ops.WORKERS = 1
    return W


def refine_overrides(name, N, dt=None):
    """Overrides for grid N at a fixed 128-unit box (and the world's dt unless given)."""
    s = N / N0
    if name == "fv":
        o = {"nu": 0.1 * s**2, "kY": 1.0 * s**2, "hyper": 0.005 * s**4}
        if dt is not None:
            o["dt"] = dt
        return o if s != 1 or dt is not None else {}
    o = {}
    if s != 1:
        o["scale"] = s
    if dt is not None:
        o["dt"] = dt
    return o


def rot_nn(a, deg=45.0):
    """Nearest-neighbour rotation of a periodic white field about the box centre (wrap)."""
    H, W = a.shape
    yy, xx = np.mgrid[0:H, 0:W].astype(float)
    cy, cx = (H - 1) / 2, (W - 1) / 2
    th = np.deg2rad(deg)
    # source point = R^-1 (x - c) + c
    sy = np.cos(th) * (yy - cy) - np.sin(th) * (xx - cx) + cy
    sx = np.sin(th) * (yy - cy) + np.cos(th) * (xx - cx) + cx
    iy = np.rint(sy).astype(int) % H
    ix = np.rint(sx).astype(int) % W
    return a[iy, ix]


def ic(name, seed, rot=0.0, W=None):
    """The world's own noise initial condition at 128^2 (rot: degrees, white draws remapped)."""
    W = W or load(name)
    rng = np.random.default_rng(seed)
    H = Wd = N0
    R = (lambda a: rot_nn(a, rot)) if rot else (lambda a: a)
    if name == "fv":
        ops, q = W.ops, dict(W.P)
        n = ops.fft_conv(R(rng.standard_normal((H, Wd))), ops.gauss_kernel(H, Wd, q["L"]))
        n = n - ops.fft_conv(n, ops.gauss_kernel(H, Wd, 4 * q["L"]))
        om = q["noise"] * n / n.std()
        Y = q["Y0"] * np.ones((H, Wd))
        st = {"om": om, "Y": Y}
    else:
        P = W.P
        n = ndimage.gaussian_filter(R(rng.standard_normal((H, Wd))), 3, mode="wrap")
        phi = np.clip(P["noise_mean"] + n / n.std() * P["noise_amp"], 0, 1)
        K = P["noise_K"] * R(rng.random((H, Wd)))
        L = P["noise_KL"] * R(rng.random((H, Wd)))
        K = K + 0.01 * R(rng.random((H, Wd))) * phi
        st = {"S": np.ones((H, Wd)), "K": K, "L": L, "phi": phi}
    return st


def area_matrix(n_out, n_in):
    """Periodic area-weighted resampling matrix (n_out x n_in) on [0, 1)."""
    M = np.zeros((n_out, n_in))
    for i in range(n_out):
        a, b = i / n_out, (i + 1) / n_out
        j0, j1 = int(np.floor(a * n_in)), int(np.ceil(b * n_in))
        for j in range(j0, j1):
            lo, hi = max(a, j / n_in), min(b, (j + 1) / n_in)
            if hi > lo:
                M[i, j % n_in] += (hi - lo) * n_out
    return M


_AM = {}


def restrict(f, n_out=N0):
    """Area average of a periodic field onto n_out^2 (exact box mean of each coarse cell)."""
    n = f.shape[-1]
    if n == n_out:
        return f
    key = (n_out, n)
    if key not in _AM:
        _AM[key] = area_matrix(n_out, n)
    M = _AM[key]
    return M @ f @ M.T


def fourier_resample(f, N):
    """Band-limited (Fourier) interpolation of a periodic field to N^2."""
    n = f.shape[0]
    if n == N:
        return f.copy()
    F = np.fft.fftshift(np.fft.fft2(f))
    G = np.zeros((N, N), complex)
    o = (N - n) // 2
    G[o:o + n, o:o + n] = F
    return np.real(np.fft.ifft2(np.fft.ifftshift(G))) * (N / n) ** 2


def start_state(name, seed, N=N0, dt=None, rot=0.0, extra=None):
    """(module, state) at grid N: the 128^2 initial condition, rotated and/or resampled."""
    o = refine_overrides(name, N, dt)
    o.update(extra or {})
    W = load(name, o)
    base = ic(name, seed, rot, W=load(name, extra))
    if not rot and N == N0 and not extra:
        ref = W.init(seed, (N0, N0))
        for k in base:
            assert np.array_equal(base[k], ref[k]), f"IC recipe differs from init for {k}"
    st = W.init(seed, (N, N))  # operators and parameters for this grid and dt
    for k, v in base.items():
        if N == N0:
            st[k] = v.copy()
        elif name == "fv" and k == "om":
            st[k] = fourier_resample(v, N)
        elif name == "fv":
            st[k] = np.full((N, N), float(v.mean())) if np.ptp(v) == 0 else np.clip(fourier_resample(v, N), 0, None)
        else:  # phase_membrane: periodic cubic spline (white K, L are rough), clipped to the world's ranges
            z = N / N0
            yy, xx = np.mgrid[0:N, 0:N].astype(float)
            src = [(yy + 0.5) / z - 0.5, (xx + 0.5) / z - 0.5]
            r = ndimage.map_coordinates(v, src, order=3, mode="grid-wrap")
            st[k] = np.clip(r, 0, 1) if k == "phi" else np.clip(r, 0, None)
    return W, st
