"""sporecell: membrane-coated particle cells that eat a food gas and reproduce by shedding spores.

Eat-and-bud particle chemistry (particle life + closed particle chemistry).

Particles of three types in a periodic box (units: interaction range rmax = 1):
  F food   (diffusing gas, inert to forces except the hard core)
  C core   (self-attracting particle-life matter)
  M membrane (optional; C converts to M where it has few C neighbours)
Forces: Ventrella/Mohr particle life, f(q) = q/beta - 1 for q < beta, A[ti,tj] tent(q; beta, 1)
+ B[ti,tj] tent(q; 1, R2). Damped velocity, plus Brownian noise (D per type).
Chemistry (stochastic, every step, total particle number conserved):
  F -> C   at rate k_cat * (# C within r_cat)       (autocatalytic growth)
  C -> F   at rate k_dec                            (turnover / decay back to food)
  C -> M   if n_body <= #(C+M) within r_s < n_surf (partial neighbourhood = surface of a body)
  M -> C   if #(C+M) >= n_bury (buried) or < n_body (isolated)
  new C inherits the clan label of the nearest catalysing C (particle-level lineage)
  M -> F   at rate k_mdec
"""
import numpy as np
import numba as nb
from scipy import ndimage
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from scipy.spatial import cKDTree

nb.set_num_threads(min(2, nb.config.NUMBA_NUM_THREADS))

META = {
    "name": "sporecell-turnover",
    "family": "particle",
    "parent": "sporecell (committee r1 main experiment; dilution borrowed from the lab turnover convergence)",
    "mutation": "whole-cell dilution: each cell is removed at rate delta and its particles return as uniform food (deaths)",
    "size": (128, 128),
    "steps_per_frame": 50,
    "dt": 0.02,
    "channels": ["F food", "C core", "M membrane"],
    "matter": [1, 2],
    "smooth": 1.0,
    "periodic": True,
    "domain": (128, 128),
}

P = dict(
    L=16.0, N=4000, frac_C=0.005, beta=0.3, R2=2.5, t_half=0.04, ff=10.0, rep=10.0,
    A=[[0.0, 0.0, 0.0],
       [0.0, 1.0, 0.5],
       [0.0, 1.0, 0.3]],
    B=[[0.0, 0.0, 0.0],
       [0.0, -1.0, 0.0],
       [0.0, 0.0, 0.0]],
    D=[0.2, 0.0, 0.0],
    k_cat=0.05, r_cat=0.5, k_dec=0.01,
    k_diff=2.0, r_s=0.4, n_body=10, n_surf=35, n_bury=45, k_mdec=0.01,
    mrule="food", f_surf=4, f_bury=2,
    delta=0.0, dil_every=50,
    chem_every=5,
)


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


@nb.njit(cache=True)
def nearest_of_type(x, t, L, idx, typ, rc):
    """For each particle in idx, index of the nearest particle of type typ within rc (-1 if none)."""
    nc, cs, order, start = build_cells(x, L, rc)
    out = np.full(len(idx), -1, np.int64)
    for a in range(len(idx)):
        i = idx[a]
        cx = int(x[i, 0] / cs) % nc
        cy = int(x[i, 1] / cs) % nc
        best = rc * rc
        for oy in range(-1, 2):
            for ox in range(-1, 2):
                c = ((cy + oy) % nc) * nc + (cx + ox) % nc
                for k in range(start[c], start[c + 1]):
                    j = order[k]
                    if j == i or t[j] != typ:
                        continue
                    dx = _wrap(x[i, 0] - x[j, 0], L)
                    dy = _wrap(x[i, 1] - x[j, 1], L)
                    r2 = dx * dx + dy * dy
                    if r2 < best:
                        best = r2
                        out[a] = j
    return out


def init(seed, size, **over):
    p = dict(P)
    p.update(over)
    rng = np.random.default_rng(seed)
    N, L = p["N"], p["L"]
    x = rng.random((N, 2)) * L
    t = np.where(rng.random(N) < p["frac_C"], 1, 0).astype(np.int64)
    clan = np.where(t == 1, np.cumsum(t == 1), 0).astype(np.int64)
    return {"x": x, "t": t, "v": np.zeros((N, 2)), "rng": rng, "n": 0, "p": p, "clan": clan,
            "A": np.array(p["A"], float), "B": np.array(p["B"], float), "D": np.array(p["D"], float),
            "H": size[0]}


def chemistry(s, Cn, dtc):
    p, t, rng = s["p"], s["t"], s["rng"]
    u = rng.random(len(t))
    nC = Cn[:, 1]
    body = Cn[:, 1] + Cn[:, 2]
    new = t.copy()
    f = t == 0
    born = np.flatnonzero(f & (u < 1 - np.exp(-p["k_cat"] * nC * dtc)))
    if len(born):
        par = nearest_of_type(s["x"], t, p["L"], born, 1, p["r_cat"])
        ok = par >= 0
        new[born[ok]] = 1
        s["clan"][born[ok]] = s["clan"][par[ok]]
    c = t == 1
    dec = c & (u < 1 - np.exp(-p["k_dec"] * dtc))
    new[dec] = 0
    if p["k_diff"] > 0:
        pd = 1 - np.exp(-p["k_diff"] * dtc)
        m = t == 2
        mdec = m & (u < 1 - np.exp(-p["k_mdec"] * dtc))
        new[mdec] = 0
        if p["mrule"] == "food":  # membrane induced by contact with food (the outside)
            nF = Cn[:, 0]
            new[c & ~dec & (nF >= p["f_surf"]) & (body >= p["n_body"]) & (u > 1 - pd)] = 2
            new[m & ~mdec & (nF < p["f_bury"]) & (u > 1 - pd)] = 1
        else:  # membrane where the neighbourhood is only partly filled (geometric surface)
            new[c & ~dec & (body >= p["n_body"]) & (body < p["n_surf"]) & (u > 1 - pd)] = 2
            new[m & ~mdec & ((body >= p["n_bury"]) | (body < p["n_body"])) & (u > 1 - pd)] = 1
    s["clan"][new == 0] = 0
    s["t"] = new


def dilute(s, prob):
    """Remove whole cells (>= 15 linked matter particles) independently with probability prob."""
    m = np.flatnonzero(s["t"] > 0)
    if len(m) < 15:
        return
    L = s["p"]["L"]
    pr = cKDTree(s["x"][m] % L, boxsize=L).query_pairs(0.35, output_type="ndarray")
    g = coo_matrix((np.ones(len(pr)), (pr[:, 0], pr[:, 1])), shape=(len(m), len(m)))
    nc, lab = connected_components(g, directed=False)
    size = np.bincount(lab, minlength=nc)
    for k in np.flatnonzero(size >= 15):
        if s["rng"].random() < prob:
            idx = m[lab == k]
            s["t"][idx] = 0
            s["clan"][idx] = 0
            s["v"][idx] = 0
            s["x"][idx] = s["rng"].random((len(idx), 2)) * L
            s["deaths"] = s.get("deaths", 0) + 1


def step(s):
    p = s["p"]
    dt = META["dt"]
    rcnt = max(p["r_cat"], p["r_s"])
    F, Cn = forces(s["x"], s["t"], p["L"], s["A"], s["B"], p["beta"], max(p["R2"], 1.0), rcnt, 3, p["rep"])
    s["v"] = s["v"] * 0.5 ** (dt / p["t_half"]) + F * p["ff"] * dt
    noise = np.sqrt(2 * s["D"][s["t"]] * dt)[:, None] * s["rng"].standard_normal(s["x"].shape)
    s["x"] = (s["x"] + s["v"] * dt + noise) % p["L"]
    s["n"] += 1
    if s["n"] % p["chem_every"] == 0:
        chemistry(s, Cn, dt * p["chem_every"])
    if p["delta"] > 0 and s["n"] % p["dil_every"] == 0:
        dilute(s, p["delta"] * dt * p["dil_every"])
    return s


def fields(s):
    H, L = s["H"], s["p"]["L"]
    out = np.zeros((3, H, H), np.float32)
    ix = (np.floor(s["x"][:, 0] / L * H).astype(int)) % H
    iy = (np.floor(s["x"][:, 1] / L * H).astype(int)) % H
    for k in range(3):
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
    hit = mask[iy, ix] & (s["t"] > 0)
    s["t"][hit] = 0  # erased matter returns to food at the same place
    s["v"][hit] = 0
    return s
