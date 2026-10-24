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
    "name": "fl_predator",
    "family": "flow-lenia",
    "parent": "flow-lenia/fl_forager (prey and predator both use glider rule C2_r202)",
    "mutation": "two glider species with their own rules; predator matter converts prey matter it overlaps (mass-conserving), is drawn up a blurred prey field and decays to food; prey eat food",
    "size": (128, 128),
    "steps_per_frame": 40,
    "dt": 0.2,
    "channels": ["prey", "predator", "food"],
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
    "pred_rule": 202, "n_prey": 2, "n_pred": 2,
    "k_pred": 0.03, "K_pred": 0.3, "chase": 20.0, "chase_sigma": 12.0, "flee": 60.0, "k_dec_pred": 0.003,
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



def blur_fft(H, W, sigma):
    y = np.minimum(np.arange(H), H - np.arange(H))[:, None]
    x = np.minimum(np.arange(W), W - np.arange(W))[None, :]
    K = np.exp(-(x ** 2 + y ** 2) / (2 * sigma ** 2))
    return rfft2(K / K.sum())


def init(seed, size):
    H, W = size
    rng = np.random.default_rng(seed)
    rules = [random_rule(np.random.default_rng(CFG["rule_seed"]), 2, CFG["k"]),
             random_rule(np.random.default_rng(CFG["pred_rule"]), 2, CFG["k"])]
    Kf = [kernels_fft(H, W, r, CFG["R_scale"]) for r in rules]
    A = np.zeros((4, H, W))  # 0,1 prey channels; 2,3 predator channels
    L = CFG["patch"]
    for j in range(CFG["n_prey"] + CFG["n_pred"]):
        y0, x0 = rng.integers(0, H), rng.integers(0, W)
        ys = (np.arange(L) + y0) % H; xs = (np.arange(L) + x0) % W
        c = 0 if j < CFG["n_prey"] else 2
        A[c:c + 2, ys[:, None], xs[None, :]] = rng.uniform(0, 1, (2, L, L))
    return {"A": A, "phi": np.full((H, W), float(CFG["food0"])), "Kf": Kf, "rules": rules,
            "Kb": blur_fft(H, W, CFG["chase_sigma"]), "rng": rng, "t": 0}


def affinity(A2, rule, Kf):
    H, W = A2.shape[1:]
    Uk = irfft2(rfft2(A2)[rule["c0"]] * Kf, (H, W))
    G = (2 * np.exp(-((Uk - rule["m"][:, None, None]) / np.maximum(rule["s"][:, None, None], 1e-4)) ** 2 / 2) - 1) * rule["h"][:, None, None]
    U = np.zeros((2, H, W))
    np.add.at(U, rule["c1"], G)
    return U


def step(s):
    A = s["A"]
    _, H, W = A.shape
    prey, pred = A[0] + A[1], A[2] + A[3]
    U = np.concatenate([affinity(A[:2], s["rules"][0], s["Kf"][0]), affinity(A[2:], s["rules"][1], s["Kf"][1])])
    if CFG["chase"]:
        U[2:] += CFG["chase"] * irfft2(rfft2(prey) * s["Kb"], (H, W))[None]
    if CFG["flee"]:
        U[:2] -= CFG["flee"] * irfft2(rfft2(pred) * s["Kb"], (H, W))[None]
    N = H * W
    nA = np.zeros((4, N))
    for grp in (slice(0, 2), slice(2, 4)):  # pressure acts within each species
        Ag = A[grp]
        gAy, gAx = sobel(Ag.sum(0))
        gUy, gUx = sobel(U[grp])
        alpha = np.clip((Ag / 2) ** CFG["n"], 0, 1)
        Fy = gUy * (1 - alpha) - gAy * alpha
        Fx = gUx * (1 - alpha) - gAx * alpha
        for c in range(2):
            idx, w = rt_targets(Fy[c], Fx[c], CFG["dt"], CFG["dd"], CFG["sigma"])
            nA[grp.start + c] = np.bincount(idx.ravel(), (w * Ag[c].ravel()[None]).ravel(), N)
    s["A"] = nA.reshape(4, H, W)
    metabolism(s)
    s["t"] += 1
    return s


def metabolism(s):
    A, phi = s["A"], s["phi"]
    prey, pred = A[0] + A[1], A[2] + A[3]
    q = (prey / CFG["K_eat"]) ** CFG["eat_n"]
    eat = np.minimum(CFG["k_eat"] * phi * q / (1 + q), 0.5 * phi)
    fprey = A[:2] / np.maximum(prey, 1e-12)
    qp = (pred / CFG["K_pred"]) ** CFG["eat_n"]
    kill = np.minimum(CFG["k_pred"] * prey * qp / (1 + qp), 0.5 * prey)   # prey mass converted to predator
    fpred = np.where(pred > 1e-12, A[2:] / np.maximum(pred, 1e-12), 0.5)
    dprey = CFG["k_dec"] * A[:2]
    dpred = CFG["k_dec_pred"] * A[2:]
    A[:2] += (eat - kill) * fprey - dprey
    A[2:] += kill * fpred - dpred
    phi = phi - eat + dprey.sum(0) + dpred.sum(0)
    D = CFG["D_food"]
    phi = phi + D * (np.roll(phi, 1, 0) + np.roll(phi, -1, 0) + np.roll(phi, 1, 1) + np.roll(phi, -1, 1) - 4 * phi)
    s["A"], s["phi"] = np.maximum(A, 0), phi


def fields(s):
    A = s["A"]
    return np.stack([A[0] + A[1], A[2] + A[3], s["phi"]])


def damage(s, mask):
    s["A"][:, mask] = 0
    return s
