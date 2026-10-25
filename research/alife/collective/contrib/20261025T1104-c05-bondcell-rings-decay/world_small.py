"""bondcell: sporecell3-det whose membrane particles M form harmonic chain bonds.

New relative to sporecell3-det (whose M rings vanished once food was depleted, because every
membrane particle reverted to core when it lost its food neighbours):
  - every chem step, each M with < 2 bonds bonds to its nearest M within r_b that also has
    < 2 bonds (chains, at most 2 bonds per particle);
  - a bond pulls with k_b (r - r0); it breaks above r_break, at rate k_break, or when either
    end stops being M;
  - bonded M does not revert to core when food is scarce (bond_keep=1); it decays to food
    at k_mdec like any M;
  - optional: food is pushed out of bonded M within r_rep with strength k_rep (gating).
bonds=0 is the matched no-bond twin (identical chemistry and random streams).

Parent description follows.
sporecell2: membrane-coated particle cells that eat a food gas and reproduce by shedding spores.

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
    "name": "bondcell",
    "family": "particle",
    "parent": "threads/particle-life/worlds/sporecell3-det",
    "mutation": "membrane particles form harmonic chain bonds (<=2 per particle); bonded M does not revert to core",
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
    L=11.31, N=2000, frac_C=0.005, beta=0.3, R2=1.0, t_half=0.04, ff=10.0, rep=10.0,
    A=[[0.0, 0.0, 0.0, 0.0],
       [0.0, 1.0, 0.5, 1.0],
       [0.0, 1.0, 0.3, 1.0],
       [0.0, 1.0, 0.5, 1.0]],
    B=[[0.0] * 4] * 4,
    D=[0.2, 0.0, 0.0, 0.0],
    mu=0.1, seed_kind1=0.0, k_conf=1.0, k_cat1=0.065, gate_beta=0.0,
    k_lys=0.0, n_lys=3, k_det=0.05, n_det=60, d_det=1.5, dx_max=0.05,
    k_cat=0.03, r_cat=0.5, k_dec=0.01,
    k_diff=2.0, r_s=0.4, n_body=10, n_surf=35, n_bury=45, k_mdec=0.01,
    mrule="food", f_surf=4, f_bury=2,
    chem_every=5,
    bonds=1, r_b=0.35, k_b=20.0, r0=0.3, r_break=0.6, k_break=0.0, bond_keep=1, k_rep=0.0, r_rep=0.4, bury_revert=0, m_lim=4,
)
import json as _json, os as _os
P.update(_json.loads(_os.environ.get("WORLD_P", "{}")))  # screening override only


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


@nb.njit(cache=True)
def bond_forces(x, bA, bB, L, k_b, r0, F):
    N = x.shape[0]
    for i in range(N):
        for j in (bA[i], bB[i]):
            if j > i:
                dx = _wrap(x[j, 0] - x[i, 0], L)
                dy = _wrap(x[j, 1] - x[i, 1], L)
                q = np.sqrt(dx * dx + dy * dy)
                if q < 1e-9:
                    continue
                f = k_b * (q - r0)
                F[i, 0] += f * dx / q
                F[i, 1] += f * dy / q
                F[j, 0] -= f * dx / q
                F[j, 1] -= f * dy / q


@nb.njit(cache=True)
def food_repulsion(x, t, bA, L, r_rep, k_rep, F):
    """push food (type 0) away from bonded membrane particles."""
    nc, cs, order, start = build_cells(x, L, max(r_rep, 1e-3))
    N = x.shape[0]
    for i in range(N):
        if t[i] != 0:
            continue
        cx = int(x[i, 0] / cs) % nc
        cy = int(x[i, 1] / cs) % nc
        for oy in range(-1, 2):
            for ox in range(-1, 2):
                c = ((cy + oy) % nc) * nc + (cx + ox) % nc
                for k in range(start[c], start[c + 1]):
                    j = order[k]
                    if t[j] != 2 or bA[j] < 0:
                        continue
                    dx = _wrap(x[i, 0] - x[j, 0], L)
                    dy = _wrap(x[i, 1] - x[j, 1], L)
                    q = np.sqrt(dx * dx + dy * dy)
                    if q < r_rep and q > 1e-9:
                        f = k_rep * (1.0 - q / r_rep)
                        F[i, 0] += f * dx / q
                        F[i, 1] += f * dy / q


@nb.njit(cache=True)
def update_bonds(x, t, bA, bB, L, r_b, r_break, u, p_break):
    N = x.shape[0]
    # break
    for i in range(N):
        for slot in range(2):
            j = bA[i] if slot == 0 else bB[i]
            if j < 0:
                continue
            dx = _wrap(x[j, 0] - x[i, 0], L)
            dy = _wrap(x[j, 1] - x[i, 1], L)
            if t[i] != 2 or t[j] != 2 or dx * dx + dy * dy > r_break * r_break or (j > i and u[i] < p_break):
                if slot == 0:
                    bA[i] = -1
                else:
                    bB[i] = -1
                if bA[j] == i:
                    bA[j] = -1
                elif bB[j] == i:
                    bB[j] = -1
    # compact: keep bonds in slot A first
    for i in range(N):
        if bA[i] < 0 and bB[i] >= 0:
            bA[i] = bB[i]
            bB[i] = -1
    # form
    nc, cs, order, start = build_cells(x, L, r_b)
    for i in range(N):
        if t[i] != 2 or bB[i] >= 0:
            continue
        cx = int(x[i, 0] / cs) % nc
        cy = int(x[i, 1] / cs) % nc
        best = r_b * r_b
        bj = -1
        for oy in range(-1, 2):
            for ox in range(-1, 2):
                c = ((cy + oy) % nc) * nc + (cx + ox) % nc
                for k in range(start[c], start[c + 1]):
                    j = order[k]
                    if j == i or t[j] != 2 or bB[j] >= 0 or bA[i] == j:
                        continue
                    dx = _wrap(x[j, 0] - x[i, 0], L)
                    dy = _wrap(x[j, 1] - x[i, 1], L)
                    r2 = dx * dx + dy * dy
                    if r2 < best:
                        best = r2
                        bj = j
        if bj >= 0:
            if bA[i] < 0:
                bA[i] = bj
            else:
                bB[i] = bj
            if bA[bj] < 0:
                bA[bj] = i
            else:
                bB[bj] = i


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
            "H": size[0], "bA": np.full(N, -1, np.int64), "bB": np.full(N, -1, np.int64)}


def chemistry(s, Cn, dtc):
    """Kinds: gene g in {0, 1}; core type 1 + 2 g; membrane type 2 keeps its gene.
    Every random number is drawn on every call, so arms that differ only in parameters
    (e.g. selected vs neutral) consume identical random streams."""
    p, t, rng, g = s["p"], s["t"], s["rng"], s["g"]
    N = len(t)
    u = rng.random(N)
    u_mut = rng.random(N)
    u_lys = rng.random(N)
    u_conf = rng.random(N)
    u_det = rng.random(N)
    ang = rng.random(N) * 2 * np.pi
    nC = Cn[:, 1] + Cn[:, 3]
    body = nC + Cn[:, 2]
    new = t.copy()
    f = t == 0
    born = np.flatnonzero(f & (u < 1 - np.exp(-(p["k_cat"] * Cn[:, 1] + p["k_cat1"] * Cn[:, 3]) * dtc)))
    if len(born):
        par = nearest_of_type(s["x"], t, p["L"], born, 1, p["r_cat"])
        ok = par >= 0
        b, pa = born[ok], par[ok]
        gb = g[pa] ^ (u_mut[b] < p["mu"])
        g[b] = gb
        new[b] = 1 + 2 * gb
        s["clan"][b] = s["clan"][pa]
    c = (t == 1) | (t == 3)
    dec = c & (u < 1 - np.exp(-p["k_dec"] * dtc))
    new[dec] = 0
    lys = (t == 1) & ~dec & (Cn[:, 3] >= p["n_lys"]) & (u_lys < 1 - np.exp(-p["k_lys"] * dtc))
    new[lys] = 0
    dec = dec | lys
    own = np.where(t == 3, Cn[:, 3], Cn[:, 1])
    other = np.where(t == 3, Cn[:, 1], Cn[:, 3])
    flip = c & ~dec & (other > own) & (u_conf < 1 - np.exp(-p["k_conf"] * dtc))
    g[flip] ^= 1
    new[flip] = 1 + 2 * g[flip]
    # spore release: a surface core particle (partly filled neighbourhood) detaches at rate k_det
    det = c & ~dec & (body >= 3) & (body < p["n_det"]) & (u_det < 1 - np.exp(-p["k_det"] * dtc))
    if det.any():
        s["x"][det] = (s["x"][det] + p["d_det"] * np.column_stack([np.cos(ang[det]), np.sin(ang[det])])) % p["L"]
        s["v"][det] = 0
        s["n_det_events"] = s.get("n_det_events", 0) + int(det.sum())
    if p["k_diff"] > 0:
        pd = 1 - np.exp(-p["k_diff"] * dtc)
        m = t == 2
        mdec = m & (u < 1 - np.exp(-p["k_mdec"] * dtc))
        new[mdec] = 0
        nF = Cn[:, 0]
        conv = c & ~dec & (nF >= p["f_surf"]) & (body >= p["n_body"]) & (u > 1 - pd)
        if p["m_lim"] > 0:  # monolayer: a core particle already touching m_lim membrane particles stays core
            conv &= Cn[:, 2] < p["m_lim"]
        new[conv] = 2
        back = m & ~mdec & (nF < p["f_bury"]) & (u > 1 - pd)
        if p["bonds"] and p["bond_keep"]:
            back &= s["bA"] < 0
        if p["bury_revert"]:  # membrane buried inside a body reverts to core
            back |= m & ~mdec & (body >= p["n_bury"]) & (u > 1 - pd)
        new[back] = 1 + 2 * g[back]
    s["clan"][new == 0] = 0
    g[new == 0] = 0
    s["t"] = new


def step(s):
    """One step of length dt = META['dt']. Motion uses adaptive sub-steps so that no particle moves
    more than dx_max per sub-step (forces recomputed each sub-step); chemistry once per chem_every steps."""
    p = s["p"]
    dt = META["dt"]
    rcnt = max(p["r_cat"], p["r_s"])
    R2 = max(p["R2"], 1.0)
    fr_half = p["t_half"]
    F, Cn = forces(s["x"], s["t"], p["L"], s["A"], s["B"], p["beta"], R2, rcnt, 4, p["rep"])
    _extra(s, F)
    Dp = s["D"][s["t"]]
    if p["gate_beta"] > 0:
        Dp = Dp * np.exp(-p["gate_beta"] * Cn[:, 2])
    xi = s["rng"].standard_normal(s["x"].shape)  # one noise draw per step (unconditional)
    vtrial = s["v"] * 0.5 ** (dt / fr_half) + F * p["ff"] * dt
    dmax = float(np.abs(vtrial * dt).max()) if len(vtrial) else 0.0
    nsub = max(1, int(np.ceil(dmax / p["dx_max"])))
    h = dt / nsub
    for k in range(nsub):
        if k > 0:
            F, _ = forces(s["x"], s["t"], p["L"], s["A"], s["B"], p["beta"], R2, rcnt, 4, p["rep"])
            _extra(s, F)
        s["v"] = s["v"] * 0.5 ** (h / fr_half) + F * p["ff"] * h
        dx = s["v"] * h
        nd = float(np.abs(dx).max()) if len(dx) else 0.0
        if nd > p["dx_max"]:  # velocity grew inside the step: clip the displacement (rare) and log it
            dx *= p["dx_max"] / nd
            s["n_clip"] = s.get("n_clip", 0) + 1
        s["x"] = (s["x"] + dx + np.sqrt(2 * Dp * h)[:, None] * xi / np.sqrt(nsub)) % p["L"]
    s["max_sub_disp"] = max(s.get("max_sub_disp", 0.0), min(dmax / nsub, p["dx_max"]))
    s["nsub_hist"] = s.get("nsub_hist", {})
    s["nsub_hist"][nsub] = s["nsub_hist"].get(nsub, 0) + 1
    s["n"] += 1
    if s["n"] % p["chem_every"] == 0:
        chemistry(s, Cn, dt * p["chem_every"])
        ub = s["rng"].random(len(s["t"]))  # drawn in both arms
        if p["bonds"]:
            update_bonds(s["x"], s["t"], s["bA"], s["bB"], p["L"], p["r_b"], p["r_break"], ub,
                         1 - np.exp(-p["k_break"] * dt * p["chem_every"]))
    return s


def _extra(s, F):
    p = s["p"]
    if p["bonds"]:
        bond_forces(s["x"], s["bA"], s["bB"], p["L"], p["k_b"], p["r0"], F)
        if p["k_rep"] > 0:
            food_repulsion(s["x"], s["t"], s["bA"], p["L"], p["r_rep"], p["k_rep"], F)


def stats(s):
    t = s["t"]
    nb_ = int(((s["bA"] >= 0).sum() + (s["bB"] >= 0).sum()) // 2)
    return {"F": int((t == 0).sum()), "C": int(((t == 1) | (t == 3)).sum()), "M": int((t == 2).sum()), "bonds": nb_}


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
