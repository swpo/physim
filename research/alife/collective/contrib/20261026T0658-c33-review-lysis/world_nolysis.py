"""sporecell2: membrane-coated particle cells that eat a food gas and reproduce by shedding spores.

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

nb.set_num_threads(min(2, nb.config.NUMBA_NUM_THREADS))

META = {
    "name": "sporecell2",
    "family": "particle",
    "parent": "sporecell-gene; gate forked from autopoiesis/fisim-beyond-laplacian (gated mobility)",
    "mutation": "majority-vote conformity of core kind (in-cell mutants erased, spores are the genetic bottleneck); per-kind catalysis rate; food mobility gated by membrane density D_F exp(-beta nM); short B shell",
    "size": (128, 128),
    "steps_per_frame": 50,
    "dt": 0.02,
    "channels": ["F food", "C0 core kind 0", "M membrane", "C1 core kind 1"],
    "matter": [1, 2, 3],
    "smooth": 1.0,
    "periodic": True,
    "domain": (128, 128),
}

P = dict(
    L=16.0, N=4000, frac_C=0.005, beta=0.3, R2=1.0, t_half=0.04, ff=10.0, rep=10.0,
    A=[[0.0, 0.0, 0.0, 0.0],
       [0.0, 1.0, 0.5, 1.0],
       [0.0, 1.0, 0.3, 1.0],
       [0.0, 1.0, 0.5, 1.0]],
    B=[[0.0] * 4] * 4,
    D=[0.2, 0.0, 0.0, 0.0],
    mu=0.002, seed_kind1=0.5, k_conf=1.0, k_cat1=0.035, gate_beta=0.0, k_lys=0.0, n_lys=3,
    k_cat=0.05, r_cat=0.5, k_dec=0.01,
    k_diff=2.0, r_s=0.4, n_body=10, n_surf=35, n_bury=45, k_mdec=0.01,
    mrule="food", f_surf=4, f_bury=2,
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
    """For each particle in idx, index of the nearest particle of type typ or typ+2 within rc (-1 if none)."""
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
                    if j == i or (t[j] != typ and t[j] != typ + 2):
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
    g0 = ((t == 1) & (rng.random(N) < p["seed_kind1"])).astype(np.int64)
    t = t + 2 * g0
    clan = np.where(t > 0, np.cumsum(t > 0), 0).astype(np.int64)
    return {"x": x, "t": t, "v": np.zeros((N, 2)), "rng": rng, "n": 0, "p": p, "clan": clan,
            "g": g0,
            "A": np.array(p["A"], float), "B": np.array(p["B"], float), "D": np.array(p["D"], float),
            "H": size[0]}


def chemistry(s, Cn, dtc):
    """Kinds: gene g in {0, 1}; a core particle has type 1 + 2 g. Membrane (type 2) keeps its gene."""
    p, t, rng, g = s["p"], s["t"], s["rng"], s["g"]
    u = rng.random(len(t))
    nC = Cn[:, 1] + Cn[:, 3]
    body = nC + Cn[:, 2]
    new = t.copy()
    f = t == 0
    born = np.flatnonzero(f & (u < 1 - np.exp(-(p["k_cat"] * Cn[:, 1] + p["k_cat1"] * Cn[:, 3]) * dtc)))
    if len(born):
        par = nearest_of_type(s["x"], t, p["L"], born, 1, p["r_cat"])
        ok = par >= 0
        b, pa = born[ok], par[ok]
        gb = g[pa] ^ (rng.random(len(b)) < p["mu"])
        g[b] = gb
        new[b] = 1 + 2 * gb
        s["clan"][b] = s["clan"][pa]
    c = (t == 1) | (t == 3)
    dec = c & (u < 1 - np.exp(-p["k_dec"] * dtc))
    new[dec] = 0
    if p["k_lys"] > 0:  # predation: kind-0 core touching >= n_lys kind-1 core lyses into food
        lys = (t == 1) & ~dec & (Cn[:, 3] >= p["n_lys"]) & (rng.random(len(t)) < 1 - np.exp(-p["k_lys"] * dtc))
        new[lys] = 0
        dec = dec | lys
    if p["k_conf"] > 0:  # majority vote: a core particle outnumbered by the other kind converts
        own = np.where(t == 3, Cn[:, 3], Cn[:, 1])
        other = np.where(t == 3, Cn[:, 1], Cn[:, 3])
        flip = c & ~dec & (other > own) & (rng.random(len(t)) < 1 - np.exp(-p["k_conf"] * dtc))
        g[flip] ^= 1
        new[flip] = 1 + 2 * g[flip]
    if p["k_diff"] > 0:
        pd = 1 - np.exp(-p["k_diff"] * dtc)
        m = t == 2
        mdec = m & (u < 1 - np.exp(-p["k_mdec"] * dtc))
        new[mdec] = 0
        nF = Cn[:, 0]
        new[c & ~dec & (nF >= p["f_surf"]) & (body >= p["n_body"]) & (u > 1 - pd)] = 2
        back = m & ~mdec & (nF < p["f_bury"]) & (u > 1 - pd)
        new[back] = 1 + 2 * g[back]
    s["clan"][new == 0] = 0
    g[new == 0] = 0
    s["t"] = new


def step(s):
    p = s["p"]
    dt = META["dt"]
    rcnt = max(p["r_cat"], p["r_s"])
    F, Cn = forces(s["x"], s["t"], p["L"], s["A"], s["B"], p["beta"], max(p["R2"], 1.0), rcnt, 4, p["rep"])
    s["v"] = s["v"] * 0.5 ** (dt / p["t_half"]) + F * p["ff"] * dt
    Dp = s["D"][s["t"]]
    if p["gate_beta"] > 0:  # gated mobility: food moves slowly where membrane is dense
        Dp = Dp * np.exp(-p["gate_beta"] * Cn[:, 2])
    noise = np.sqrt(2 * Dp * dt)[:, None] * s["rng"].standard_normal(s["x"].shape)
    s["x"] = (s["x"] + s["v"] * dt + noise) % p["L"]
    s["n"] += 1
    if s["n"] % p["chem_every"] == 0:
        chemistry(s, Cn, dt * p["chem_every"])
    return s


def fields(s):
    H, L = s["H"], s["p"]["L"]
    out = np.zeros((4, H, H), np.float32)
    ix = (np.floor(s["x"][:, 0] / L * H).astype(int)) % H
    iy = (np.floor(s["x"][:, 1] / L * H).astype(int)) % H
    for k in range(4):
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
