"""Flow-Lenia (Plantec et al. 2023), numpy re-implementation, with optional parameter localization.

Matter A (C channels) is never created or destroyed: the Lenia growth field U only sets a
velocity  F_c = (1 - alpha) grad U_c - alpha grad A_sum,  alpha = clip((A_c / theta)^n, 0, 1),
and reintegration tracking moves every cell's mass as a 2*sigma square to x + dt*F (clipped to
dd - sigma), splitting it over the cells it overlaps. Mass is conserved to round-off.

Parameter localization (CFG["localize"]): every cell carries the growth parameters (m, s, h of
every kernel). They travel with matter in the same reintegration step and are mixed where
matter from several sources lands in one cell ("avg" = mass weighted mean, "sample" = one
incoming parcel chosen with probability proportional to its mass). Growth is evaluated with
the parameters of the cell where it is evaluated.

fl_food mutation: an open metabolism with a conserved total. A second substance, food phi,
does not flow; it diffuses (D_food). Matter is made from food where matter already is
(eat = k_eat * phi * A_sum/(A_sum + K_eat), shared over channels in proportion to A_c) and every
channel decays back into food at rate k_dec. Sum(A) + sum(phi) is conserved to round-off,
so bodies must keep eating to persist, and can grow (and then divide) only by eating.

The whole model is configured by CFG; variants in this thread copy this file and change CFG.
"""
import numpy as np
import scipy.fft as sfft

META = {
    "name": "fl_forager_gene",
    "family": "flow-lenia",
    "parent": "flow-lenia/fl_forager + fork of the heritable-rate-allele protocol of active-droplets/ad5-evolve and autopoiesis/phase_trait (gene carried by matter, mutation during the run, neutral control)",
    "mutation": "every parcel carries a heritable uptake gene log g (eat *= g) and a genotype id, both moved with the matter by stochastic sampling; body-scale mutations log g += N(0, mut_size); gene_active=False is the neutral-marker control",
    "size": (128, 128),
    "steps_per_frame": 10,
    "dt": 0.2,
    "channels": ["low g", "high g", "food"],
    "matter": [0, 1],
    "smooth": 1.0, "threshold": 0.15,
}

CFG = {
    "C": 2, "k": 10, "rule_seed": 202, "dd": 5, "dt": 0.2, "sigma": 0.65, "n": 2, "theta": None,
    "R_scale": 1.0,           # multiplies the (R+15)*r kernel radius (overridden below)
    "localize": None,          # None | "avg" | "sample"
    "species": 1,              # number of random rules seeded (needs localize)
    "init": "patch",           # "patch": one random patch per species; "patches": several
    "patch": 40, "n_patches": 1,
    "mut_rate": 0.0,           # per-step probability of a mutation event (needs localize)
    "mut_size": 0.1,           # relative std of the mutation on (m, s, h)
    "R_scale": 0.4, "n_patches": 1, "patch": 12,
    "localize": "sample", "mut_rate": 0.004, "mut_size": 0.2, "mut_radius": 8,
    "gene_active": True,       # False: the gene is a neutral marker (same mutations, no effect)
    "cost": 0.0,               # maintenance trade-off: decay *= g**cost
    "food0": 0.1,              # initial food per cell
    "k_eat": 0.05, "K_eat": 0.3, "eat_n": 3, "k_dec": 0.002, "D_food": 0.2,
}

WORKERS = 2


def rfft2(x):
    return sfft.rfft2(x, axes=(-2, -1), workers=WORKERS)


def irfft2(X, shape):
    return sfft.irfft2(X, s=shape, axes=(-2, -1), workers=WORKERS)


def random_rule(rng, C, k):
    """Same priors as the reference implementation (FlowLenia/flowlenia.py)."""
    rule = {
        "R": rng.uniform(2, 25), "r": rng.uniform(0.2, 1, k),
        "m": rng.uniform(0.05, 0.5, k), "s": rng.uniform(0.001, 0.18, k), "h": rng.uniform(0.01, 1, k),
        "a": rng.uniform(0, 1, (k, 3)), "b": rng.uniform(0.001, 1, (k, 3)), "w": rng.uniform(0.01, 0.5, (k, 3)),
    }
    if C == 1:
        rule["c0"] = np.zeros(k, int)
        rule["c1"] = np.zeros(k, int)
    else:
        rule["c0"] = rng.integers(0, C, k)
        rule["c1"] = rng.integers(0, C, k)
    return rule


def kernels_fft(H, W, rule, R_scale=1.0):
    y = np.minimum(np.arange(H), H - np.arange(H))[:, None]
    x = np.minimum(np.arange(W), W - np.arange(W))[None, :]
    dist = np.sqrt(x ** 2 + y ** 2)
    Ks = []
    for i in range(len(rule["r"])):
        D = dist / ((rule["R"] + 15) * rule["r"][i] * R_scale)
        sig = 0.5 * (np.tanh(-(D - 1) * 10 / 2) + 1)
        kf = (rule["b"][i] * np.exp(-(D[..., None] - rule["a"][i]) ** 2 / rule["w"][i])).sum(-1)
        K = sig * kf
        Ks.append(K / K.sum())
    return rfft2(np.stack(Ks))


def sobel(A):
    """(..., H, W) -> (gy, gx), periodic Sobel (approx. 8 x central gradient)."""
    sy = np.roll(A, -1, -2) - np.roll(A, 1, -2)
    gy = 2 * sy + np.roll(sy, 1, -1) + np.roll(sy, -1, -1)
    sx = np.roll(A, -1, -1) - np.roll(A, 1, -1)
    gx = 2 * sx + np.roll(sx, 1, -2) + np.roll(sx, -1, -2)
    return gy, gx


def rt_targets(Fy, Fx, dt, dd, sigma):
    """Reintegration tracking: for every source cell, 9 target indices and overlap weights.

    Returns idx (9, H*W) flat target indices, w (9, H*W) weights summing to 1 per source.
    """
    H, W = Fy.shape
    ma = dd - sigma
    yy, xx = np.mgrid[0:H, 0:W]
    my = yy + np.clip(dt * Fy, -ma, ma)
    mx = xx + np.clip(dt * Fx, -ma, ma)
    ry, rx = np.round(my), np.round(mx)
    idx, w = [], []
    for oy in (-1, 0, 1):
        ty = ry + oy
        wy = np.clip(np.minimum(ty + 0.5, my + sigma) - np.maximum(ty - 0.5, my - sigma), 0, None)
        for ox in (-1, 0, 1):
            tx = rx + ox
            wx = np.clip(np.minimum(tx + 0.5, mx + sigma) - np.maximum(tx - 0.5, mx - sigma), 0, None)
            idx.append(((ty.astype(int) % H) * W + (tx.astype(int) % W)).ravel())
            w.append((wy * wx).ravel() / (4 * sigma * sigma))
    return np.stack(idx), np.stack(w)


def init(seed, size):
    H, W = size
    rng = np.random.default_rng(seed)
    C, k = CFG["C"], CFG["k"]
    rrng = np.random.default_rng(CFG["rule_seed"])
    # all species share kernels (geometry) of species 0; they differ in (m, s, h)
    rules = [random_rule(rrng, C, k) for _ in range(CFG["species"])]
    base = rules[0]
    Kf = kernels_fft(H, W, base, CFG["R_scale"])
    A = np.zeros((C, H, W))
    nP = 3 * k
    P = np.zeros((nP, H, W))
    founders = np.stack([np.concatenate([r["m"], r["s"], r["h"]]) for r in rules])
    lab = np.full((H, W), -1)
    npatch = CFG["n_patches"] * CFG["species"]
    L = CFG["patch"]
    for j in range(npatch):
        sp = j % CFG["species"]
        if npatch == 1:
            y0, x0 = (H - L) // 2, (W - L) // 2
        else:
            y0, x0 = rng.integers(0, H), rng.integers(0, W)
        ys = (np.arange(L) + y0) % H
        xs = (np.arange(L) + x0) % W
        A[:, ys[:, None], xs[None, :]] = rng.uniform(0, 1, (C, L, L))
        P[:, ys[:, None], xs[None, :]] = founders[sp][:, None, None]
        lab[ys[:, None], xs[None, :]] = sp
    P[:, lab < 0] = founders[0][:, None]
    P = np.zeros((2, H, W))  # P[0] = log g (uptake gene), P[1] = genotype id
    phi = np.full((H, W), float(CFG["food0"]))
    return {"A": A, "phi": phi, "P": P, "parents": [-1], "born": [0], "gval": [0.0], "Kf": Kf, "rule": base, "founders": founders, "rng": rng, "t": 0}


def growth(s):
    A, P, rule = s["A"], s["P"], s["rule"]
    C, H, W = A.shape
    k = len(rule["r"])
    Af = rfft2(A)
    Uk = irfft2(Af[rule["c0"]] * s["Kf"], (H, W))
    if False:  # rule parameters are global here; P holds the gene fields
        pass
    else:
        m, sg, h = rule["m"][:, None, None], rule["s"][:, None, None], rule["h"][:, None, None]
    G = (2 * np.exp(-((Uk - m) / np.maximum(sg, 1e-4)) ** 2 / 2) - 1) * h
    U = np.zeros((C, H, W))
    np.add.at(U, rule["c1"], G)
    return U


def step(s):
    A, P = s["A"], s["P"]
    C, H, W = A.shape
    U = growth(s)
    theta = CFG["theta"] or C
    gUy, gUx = sobel(U)
    gAy, gAx = sobel(A.sum(0))
    alpha = np.clip((A / theta) ** CFG["n"], 0, 1)
    Fy = gUy * (1 - alpha) - gAy * alpha
    Fx = gUx * (1 - alpha) - gAx * alpha
    N = H * W
    nA = np.zeros((C, N))
    loc = CFG["localize"]
    if loc:
        num = np.zeros((P.shape[0], N))
        den = np.zeros(N)
        all_idx, all_w, all_src = [], [], []
    for c in range(C):
        idx, w = rt_targets(Fy[c], Fx[c], CFG["dt"], CFG["dd"], CFG["sigma"])
        mass = w * A[c].ravel()[None]
        nA[c] = np.bincount(idx.ravel(), mass.ravel(), N)
        if loc == "avg":
            den += np.bincount(idx.ravel(), mass.ravel(), N)
            Pf = P.reshape(P.shape[0], -1)
            for q in range(P.shape[0]):
                num[q] += np.bincount(idx.ravel(), (mass * Pf[q][None]).ravel(), N)
        elif loc == "sample":
            all_idx.append(idx.ravel()); all_w.append(mass.ravel())
            all_src.append(np.broadcast_to(np.arange(N)[None], idx.shape).ravel())
    if loc == "avg":
        Pn = P.reshape(P.shape[0], -1).copy()
        ok = den > 1e-12
        Pn[:, ok] = num[:, ok] / den[ok]
        s["P"] = Pn.reshape(P.shape)
    elif loc == "sample":
        ti = np.concatenate(all_idx); wm = np.concatenate(all_w); src = np.concatenate(all_src)
        keep = wm > 1e-12
        ti, wm, src = ti[keep], wm[keep], src[keep]
        key = np.log(wm) - np.log(-np.log(s["rng"].uniform(1e-12, 1, wm.size)))
        order = np.lexsort((key, ti))
        last = np.r_[ti[order][1:] != ti[order][:-1], True]
        win_t, win_s = ti[order][last], src[order][last]
        Pn = P.reshape(P.shape[0], -1).copy()
        Pn[:, win_t] = P.reshape(P.shape[0], -1)[:, win_s]
        s["P"] = Pn.reshape(P.shape)
    s["A"] = nA.reshape(C, H, W)
    metabolism(s)
    if loc and CFG["mut_rate"] > 0 and s["rng"].uniform() < CFG["mut_rate"]:
        mutate(s)
    s["t"] += 1
    return s


def metabolism(s):
    A, phi = s["A"], s["phi"]
    As = A.sum(0)
    q = (As / CFG["K_eat"]) ** CFG["eat_n"]
    g = np.exp(s["P"][0])
    eat = CFG["k_eat"] * phi * q / (1 + q) * (g if CFG["gene_active"] else 1.0)
    eat = np.minimum(eat, 0.5 * phi)
    frac = A / np.maximum(As, 1e-12)
    dec = CFG["k_dec"] * A * ((g ** CFG["cost"]) if CFG["gene_active"] else 1.0)
    s["A"] = A + eat * frac - dec
    phi = phi - eat + dec.sum(0)
    D = CFG["D_food"]
    if D:
        phi = phi + D * (np.roll(phi, 1, 0) + np.roll(phi, -1, 0) + np.roll(phi, 1, 1) + np.roll(phi, -1, 1) - 4 * phi)
    s["phi"] = phi


def mutate(s):
    """A body-scale mutation: a disk around a mass-weighted random cell gets one new genotype per
    genotype hit, with log g shifted by one N(0, mut_size) draw (same draws in the neutral control)."""
    A, P, rng = s["A"].sum(0), s["P"], s["rng"]
    H, W = A.shape
    j = rng.choice(H * W, p=A.ravel() / A.sum())
    cy, cx = divmod(j, W)
    y = np.arange(H)[:, None]; x = np.arange(W)[None, :]
    dy = np.minimum(np.abs(y - cy), H - np.abs(y - cy)); dx = np.minimum(np.abs(x - cx), W - np.abs(x - cx))
    hit = (dy ** 2 + dx ** 2 <= CFG["mut_radius"] ** 2) & (A > 1e-3)
    d = CFG["mut_size"] * rng.standard_normal()
    gid = P[1].astype(int)
    for g in np.unique(gid[hit]):
        new = len(s["parents"])
        sel = hit & (gid == g)
        s["parents"].append(int(g)); s["born"].append(int(s["t"])); s["gval"].append(float(P[0][sel].mean() + d))
        P[1][sel] = new
        P[0][sel] += d


def fields(s):
    """Matter coloured by the gene: channel 0 = low g, channel 1 = high g (logistic in log g), then food."""
    A = s["A"].sum(0)
    w = 1 / (1 + np.exp(-s["P"][0] / 0.15))
    return np.stack([A * (1 - w), A * w, s["phi"]])


def damage(s, mask):
    s["A"][:, mask] = 0
    return s
