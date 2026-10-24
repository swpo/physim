"""Shared particle engine for screening (periodic box, numba cell lists).

Promoted world.py files inline a copy of what they need so each stays forkable.
"""
import numpy as np
import numba as nb
nb.set_num_threads(min(2, nb.config.NUMBA_NUM_THREADS))
from scipy import ndimage


@nb.njit(cache=True)
def build_cells(x, L, rc):
    nc = max(1, int(L // rc))
    cs = L / nc
    N = x.shape[0]
    cid = np.empty(N, np.int64)
    for i in range(N):
        cx = int(x[i, 0] / cs) % nc
        cy = int(x[i, 1] / cs) % nc
        cid[i] = cy * nc + cx
    order = np.argsort(cid)
    start = np.zeros(nc * nc + 1, np.int64)
    for i in range(N):
        start[cid[i] + 1] += 1
    for c in range(nc * nc):
        start[c + 1] += start[c]
    return nc, cs, order, start


@nb.njit(cache=True)
def _wrap(d, L):
    if d > 0.5 * L:
        d -= L
    elif d < -0.5 * L:
        d += L
    return d


@nb.njit(cache=True, parallel=True)
def lenia_vel(x, t, L, w, muk, sgk, mug, sgg, crep, rc):
    """Multi-type Particle Lenia. U_i = sum_j w[ti,tj] exp(-((r-muk)/sgk)^2);
    v_i = -grad(R) + G'(U_i) grad U_i, G = exp(-((U-mug[ti])/sgg[ti])^2), R = crep/2 (1-r)_+^2."""
    N = x.shape[0]
    nc, cs, order, start = build_cells(x, L, rc)
    v = np.zeros((N, 2))
    U = np.zeros(N)
    rc2 = rc * rc
    for i in nb.prange(N):
        ti = t[i]
        cx = int(x[i, 0] / cs) % nc
        cy = int(x[i, 1] / cs) % nc
        u = 0.0
        gux = 0.0
        guy = 0.0
        rx = 0.0
        ry = 0.0
        for oy in range(-1, 2):
            for ox in range(-1, 2):
                c = ((cy + oy) % nc) * nc + (cx + ox) % nc
                for k in range(start[c], start[c + 1]):
                    j = order[k]
                    if j == i:
                        continue
                    dx = _wrap(x[i, 0] - x[j, 0], L)
                    dy = _wrap(x[i, 1] - x[j, 1], L)
                    r2 = dx * dx + dy * dy
                    if r2 > rc2:
                        continue
                    r = np.sqrt(r2) + 1e-9
                    tj = t[j]
                    m = muk[ti, tj]
                    s = sgk[ti, tj]
                    kk = w[ti, tj] * np.exp(-((r - m) / s) ** 2)
                    u += kk
                    g = kk * (-2.0 * (r - m) / (s * s)) / r
                    gux += g * dx
                    guy += g * dy
                    if r < 1.0:
                        f = crep[ti, tj] * (1.0 - r) / r
                        rx += f * dx
                        ry += f * dy
        G = np.exp(-((u - mug[ti]) / sgg[ti]) ** 2)
        dG = G * (-2.0 * (u - mug[ti]) / (sgg[ti] ** 2))
        v[i, 0] = rx + dG * gux
        v[i, 1] = ry + dG * guy
        U[i] = u
    return v, U


@nb.njit(cache=True, parallel=True)
def life_force(x, t, L, A, rmax, beta):
    """Asymmetric particle-life force (Ventrella/Mohr form). rmax scalar cutoff."""
    N = x.shape[0]
    nc, cs, order, start = build_cells(x, L, rmax)
    F = np.zeros((N, 2))
    r2max = rmax * rmax
    for i in nb.prange(N):
        ti = t[i]
        cx = int(x[i, 0] / cs) % nc
        cy = int(x[i, 1] / cs) % nc
        for oy in range(-1, 2):
            for ox in range(-1, 2):
                c = ((cy + oy) % nc) * nc + (cx + ox) % nc
                for k in range(start[c], start[c + 1]):
                    j = order[k]
                    if j == i:
                        continue
                    dx = _wrap(x[j, 0] - x[i, 0], L)
                    dy = _wrap(x[j, 1] - x[i, 1], L)
                    r2 = dx * dx + dy * dy
                    if r2 > r2max or r2 < 1e-12:
                        continue
                    r = np.sqrt(r2)
                    q = r / rmax
                    if q < beta:
                        f = q / beta - 1.0
                    else:
                        f = A[ti, t[j]] * (1.0 - abs(2.0 * q - 1.0 - beta) / (1.0 - beta))
                    F[i, 0] += f * dx / r
                    F[i, 1] += f * dy / r
    return F * rmax


@nb.njit(cache=True, parallel=True)
def type_counts(x, t, L, rc, ntypes):
    """Number of neighbours of each type within rc (excluding self)."""
    N = x.shape[0]
    nc, cs, order, start = build_cells(x, L, rc)
    C = np.zeros((N, ntypes))
    rc2 = rc * rc
    for i in nb.prange(N):
        cx = int(x[i, 0] / cs) % nc
        cy = int(x[i, 1] / cs) % nc
        for oy in range(-1, 2):
            for ox in range(-1, 2):
                c = ((cy + oy) % nc) * nc + (cx + ox) % nc
                for k in range(start[c], start[c + 1]):
                    j = order[k]
                    if j == i:
                        continue
                    dx = _wrap(x[i, 0] - x[j, 0], L)
                    dy = _wrap(x[i, 1] - x[j, 1], L)
                    if dx * dx + dy * dy < rc2:
                        C[i, t[j]] += 1.0
    return C


def raster(x, t, L, H, ntypes, sigma_px=1.5, weights=None):
    """Per-type density on an H x H periodic grid, Gaussian-blurred."""
    out = np.zeros((ntypes, H, H), np.float32)
    ix = (np.floor(x[:, 0] / L * H).astype(int)) % H
    iy = (np.floor(x[:, 1] / L * H).astype(int)) % H
    for k in range(ntypes):
        m = t == k
        np.add.at(out[k], (iy[m], ix[m]), 1.0 if weights is None else weights[m])
        if sigma_px > 0:
            out[k] = ndimage.gaussian_filter(out[k], sigma_px, mode="wrap")
    return out


@nb.njit(cache=True)
def _tent(q, a, b):
    if q <= a or q >= b:
        return 0.0
    return 1.0 - abs(2.0 * q - a - b) / (b - a)


@nb.njit(cache=True, parallel=True)
def life_force2(x, t, L, A, B, beta, R2):
    """Particle life with a second interaction shell: f(q) = core repulsion (q<beta)
    + A[ti,tj] tent(q; beta, 1) + B[ti,tj] tent(q; 1, R2). Units: rmax = 1."""
    N = x.shape[0]
    nc, cs, order, start = build_cells(x, L, R2)
    F = np.zeros((N, 2))
    r2max = R2 * R2
    for i in nb.prange(N):
        ti = t[i]
        cx = int(x[i, 0] / cs) % nc
        cy = int(x[i, 1] / cs) % nc
        for oy in range(-1, 2):
            for ox in range(-1, 2):
                c = ((cy + oy) % nc) * nc + (cx + ox) % nc
                for k in range(start[c], start[c + 1]):
                    j = order[k]
                    if j == i:
                        continue
                    dx = _wrap(x[j, 0] - x[i, 0], L)
                    dy = _wrap(x[j, 1] - x[i, 1], L)
                    r2 = dx * dx + dy * dy
                    if r2 > r2max or r2 < 1e-12:
                        continue
                    q = np.sqrt(r2)
                    tj = t[j]
                    if q < beta:
                        f = q / beta - 1.0
                    else:
                        f = A[ti, tj] * _tent(q, beta, 1.0) + B[ti, tj] * _tent(q, 1.0, R2)
                    F[i, 0] += f * dx / q
                    F[i, 1] += f * dy / q
    return F
