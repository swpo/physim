"""Plain asymmetric particle life (Ventrella/Mohr force), random 5x5 matrix rng(102).

Screened from 12 random matrices (screens/s02b_plife_random_dense.png, m2): from uniform noise it
forms persistent cells with a shell of one type around a core of others. No chemistry, no noise.
"""
import numpy as np
import numba as nb
from scipy import ndimage

nb.set_num_threads(min(2, nb.config.NUMBA_NUM_THREADS))

META = {
    "name": "plife-m2",
    "family": "particle",
    "parent": "particle life (Mohr force, LITERATURE 2.3.2), random matrix screen",
    "mutation": "none (baseline); periodic box at ~21 particles per r_max^2",
    "size": (128, 128),
    "steps_per_frame": 25,
    "dt": 0.02,
    "channels": ["type 0", "type 1", "type 2", "type 3", "type 4"],
    "matter": None,
    "smooth": 1.0,
    "periodic": True,
    "domain": (128, 128),
}

P = dict(L=12.0, N=3000, K=5, beta=0.3, t_half=0.04, ff=10.0, rep=1.0,
         A=[[-0.68, 0.172, 0.648, -0.405, 0.37], [-0.072, 0.783, 0.13, 0.986, -0.515],
            [-0.781, -0.309, 0.558, 0.079, 0.849], [0.989, 0.844, -0.675, 0.18, 0.451],
            [0.838, -0.707, 0.225, -0.892, 0.486]])


@nb.njit(cache=True)
def build_cells(x, L, rc):
    nc = max(1, int(L // rc))
    cs = L / nc
    N = x.shape[0]
    cid = np.empty(N, np.int64)
    for i in range(N):
        cid[i] = (int(x[i, 1] / cs) % nc) * nc + int(x[i, 0] / cs) % nc
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


@nb.njit(cache=True)
def _tent(q, a, b):
    if q <= a or q >= b:
        return 0.0
    return 1.0 - abs(2.0 * q - a - b) / (b - a)


@nb.njit(cache=True, parallel=True)
def forces(x, t, L, A, B, beta, R2, rcnt, ntypes, rep):
    """Particle-life forces and neighbour-type counts within rcnt (rcnt <= R2)."""
    N = x.shape[0]
    nc, cs, order, start = build_cells(x, L, R2)
    F = np.zeros((N, 2))
    Cn = np.zeros((N, ntypes))
    r2max = R2 * R2
    rc2 = rcnt * rcnt
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
                    tj = t[j]
                    if r2 < rc2:
                        Cn[i, tj] += 1.0
                    q = np.sqrt(r2)
                    if q < beta:
                        f = rep * (q / beta - 1.0)
                    else:
                        f = A[ti, tj] * _tent(q, beta, 1.0) + B[ti, tj] * _tent(q, 1.0, R2)
                    F[i, 0] += f * dx / q
                    F[i, 1] += f * dy / q
    return F, Cn


def init(seed, size, **over):
    p = dict(P)
    p.update(over)
    rng = np.random.default_rng(seed)
    return {"x": rng.random((p["N"], 2)) * p["L"], "t": rng.integers(0, p["K"], p["N"]).astype(np.int64),
            "v": np.zeros((p["N"], 2)), "p": p, "A": np.array(p["A"], float), "B": np.zeros((p["K"], p["K"])),
            "H": size[0], "rng": rng}


def step(s):
    p, dt = s["p"], META["dt"]
    F, _ = forces(s["x"], s["t"], p["L"], s["A"], s["B"], p["beta"], 1.0, 0.1, p["K"], p["rep"])
    s["v"] = s["v"] * 0.5 ** (dt / p["t_half"]) + F * p["ff"] * dt
    s["x"] = (s["x"] + s["v"] * dt) % p["L"]
    return s


def fields(s):
    H, L, K = s["H"], s["p"]["L"], s["p"]["K"]
    out = np.zeros((K, H, H), np.float32)
    ix = (np.floor(s["x"][:, 0] / L * H).astype(int)) % H
    iy = (np.floor(s["x"][:, 1] / L * H).astype(int)) % H
    for k in range(K):
        m = s["t"] == k
        np.add.at(out[k], (iy[m], ix[m]), 1.0)
        out[k] = ndimage.gaussian_filter(out[k], 1.5, mode="wrap")
    return out


def particles(s):
    return np.column_stack([s["x"] / s["p"]["L"] * s["H"], s["t"]])


def damage(s, mask):
    H, L = s["H"], s["p"]["L"]
    ix = (np.floor(s["x"][:, 0] / L * H).astype(int)) % H
    iy = (np.floor(s["x"][:, 1] / L * H).astype(int)) % H
    keep = ~mask[iy, ix]
    for k in ("x", "t", "v"):
        s[k] = s[k][keep]
    return s
