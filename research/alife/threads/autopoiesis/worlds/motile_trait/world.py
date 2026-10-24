"""Motile trait: protocells whose catalyst carries a heritable phoretic mobility mu.

Phase protocells (Allen-Cahn wall tilted by links, phi^2-gated mobility, fed substrate S). The
catalyst K carries two continuous traits as co-moving masses: Qm = mu K (phoretic mobility) and
Qt = tag K (a NEUTRAL tag with no effect, the drift control). Each cell (phi > 1/2 body, label
grown 3 px into its halo) moves with v = mu_cell <grad S>_cell, mu_cell = sum Qm / sum K.
Mutation: each step with probability p_mut a random site with K > 0.05 gets mu += +-delta_mu in a
disk of radius mut_r; independently, with the same probability, tag += +-delta_mu in another disk.
Optional toxic waste (forked from chemotaxis-motility toxforage): dw = Dw lap w + pw K - dw w,
extra catalyst decay kd w K.
"""
import numpy as np

META = {
    "name": "motile-trait",
    "family": "autopoiesis",
    "parent": "threads/autopoiesis/worlds/motile_kinds + phase_trait; waste toxicity from chemotaxis-motility/worlds/toxforage",
    "mutation": "phoretic mobility is a continuous heritable trait of the catalyst, with a neutral tag as drift control; optional toxic waste",
    "size": (128, 128),
    "steps_per_frame": 50,
    "dt": 1.0,
    "channels": ["S", "K catalyst", "mu (0..3)", "L link", "membrane (wall)", "w waste"],
    "matter": None,
    "smooth": 1.0,
    "periodic": True,
}

P = dict(DS=0.2, DK=0.1, DL=0.1, Dp=0.1, r=0.2, a=4.0, th=0.15, F=0.006, k=0.0649, b=0.05, dL=0.02,
         gate=1, gateK=1, nophase=0, noise_amp=0.3, noise_mean=0.5, noise_KL=0.5, dt=1.0, K0=0.5, kin="logistic", c=0.2, dK=0.02, nspots=4, R0=6, IC="spots", p_mut=0.002, mut_r=4, mu0=1.5, tag0=1.5, delta_mu=0.3, mu_max=5.0, Dw=0.05, pw=0.01, dw=0.005, kd=0.0, vclip=0.4)


def lap(u):
    return np.roll(u, 1, 0) + np.roll(u, -1, 0) + np.roll(u, 1, 1) + np.roll(u, -1, 1) - 4 * u


def mob_div(u, g, D):
    out = np.zeros_like(u)
    for ax in (0, 1):
        gf = 0.5 * (g + np.roll(g, -1, ax))
        flux = D * gf * (np.roll(u, -1, ax) - u)
        out += flux - np.roll(flux, 1, ax)
    return out


def upwind_div(rho, vy, vx):
    out = np.zeros_like(rho)
    for v, ax in ((vy, 0), (vx, 1)):
        vf = 0.5 * (v + np.roll(v, -1, ax))
        flux = vf * np.where(vf > 0, rho, np.roll(rho, -1, ax))
        out += flux - np.roll(flux, 1, ax)
    return out


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    S, K, L, phi = np.ones((H, W)), np.zeros((H, W)), np.zeros((H, W)), np.zeros((H, W))
    yy, xx = np.mgrid[0:H, 0:W]
    if P["IC"] == "spots":
        for _ in range(P["nspots"]):
            y, x = rng.integers(0, H), rng.integers(0, W)
            d2 = ((yy - y + H / 2) % H - H / 2) ** 2 + ((xx - x + W / 2) % W - W / 2) ** 2
            m = d2 <= 16
            S[m], K[m], L[m] = 0.5, P["K0"], 0.5
            phi = np.maximum(phi, 0.5 * (1 - np.tanh((np.sqrt(d2) - P["R0"]) / 1.5)))
    else:  # noise: smoothed random fields everywhere, no planted structure
        from scipy import ndimage
        n = ndimage.gaussian_filter(rng.standard_normal((H, W)), 3, mode="wrap")
        phi = np.clip(P["noise_mean"] + n / n.std() * P["noise_amp"], 0, 1)
        K = P["noise_KL"] * rng.random((H, W))
        L = P["noise_KL"] * rng.random((H, W))
    K += 0.01 * rng.random((H, W)) * phi
    return {"S": S, "K": K, "Qm": P["mu0"] * K, "Qt": P["tag0"] * K, "L": L, "phi": phi, "w": np.zeros((H, W)), "rng": np.random.default_rng(seed + 1000), "nmut": 0}


def cell_labels(phi):
    from scipy import ndimage
    lab, n = ndimage.label(phi > 0.5)
    for a, b in ((lab[0], lab[-1]), (lab[:, 0], lab[:, -1])):  # periodic: merge across edges
        for u, v in set(zip(a.tolist(), b.tolist())):
            if u and v and u != v:
                lab[lab == v] = u
    halo = phi > 0.05
    for _ in range(3):  # grow each body's label 3 px into its own halo
        grown = ndimage.grey_dilation(lab, size=3, mode="wrap")
        lab = np.where((lab == 0) & halo, grown, lab)
    return lab, n


def step(s):
    from scipy import ndimage
    S, K, L, phi, w = s["S"], s["K"], s["L"], s["phi"], s["w"]
    g = phi * phi
    auto = P["c"] * S * K * (1 - K) * phi
    prodL = P["b"] * K * S
    lim = np.minimum(1.0, 0.5 * S / np.maximum(P["dt"] * (auto + prodL), 1e-12))
    auto, prodL = auto * lim, prodL * lim
    h = P["dt"]
    dec = P["dK"] + P["kd"] * w
    rel = auto / np.maximum(K, 1e-9)  # per-capita growth: new catalyst inherits local traits
    s["S"] = np.maximum(S + h * (P["DS"] * lap(S) - auto - prodL + P["F"] * (1 - S)), 0)
    s["K"] = np.maximum(K + h * (mob_div(K, g, P["DK"]) + auto - dec * K), 0)
    for q in ("Qm", "Qt"):
        Q = s[q]
        s[q] = np.maximum(Q + h * (mob_div(Q, g, P["DK"]) + rel * Q - dec * Q), 0)
    s["L"] = np.maximum(L + h * (mob_div(L, g, P["DL"]) + prodL - P["dL"] * L), 0)
    s["w"] = w + h * (P["Dw"] * lap(w) + P["pw"] * K - P["dw"] * w)
    s["phi"] = np.clip(phi + h * P["Dp"] * lap(phi) + h * P["r"] * phi * (1 - phi) * (phi - 0.5 + P["a"] * (L - P["th"])), 0, 1)
    lab, n = cell_labels(s["phi"])
    if n:
        Sx = s["S"]
        gy = 0.5 * (np.roll(Sx, -1, 0) - np.roll(Sx, 1, 0))
        gx = 0.5 * (np.roll(Sx, -1, 1) - np.roll(Sx, 1, 1))
        idx = np.arange(1, n + 1)
        mu = ndimage.sum(s["Qm"], lab, idx) / np.maximum(ndimage.sum(s["K"], lab, idx), 1e-9)
        my = np.concatenate([[0.0], mu * ndimage.mean(gy, lab, idx)])
        mx = np.concatenate([[0.0], mu * ndimage.mean(gx, lab, idx)])
        vy = np.clip(my[lab], -P["vclip"], P["vclip"]); vx = np.clip(mx[lab], -P["vclip"], P["vclip"])
        for k_ in ("K", "Qm", "Qt", "L", "phi"):
            s[k_] = s[k_] - h * upwind_div(s[k_], vy, vx)
    rng = s["rng"]
    for q in ("Qm", "Qt"):
        if P["p_mut"] > 0 and rng.random() < P["p_mut"]:
            idx = np.flatnonzero(s["K"] > 0.05)
            if len(idx):
                H, W = K.shape
                y, x = divmod(int(rng.choice(idx)), W)
                yy = (np.arange(H)[:, None] - y + H // 2) % H - H // 2
                xx = (np.arange(W)[None, :] - x + W // 2) % W - W // 2
                m = yy ** 2 + xx ** 2 <= P["mut_r"] ** 2
                tr = s[q][m] / np.maximum(s["K"][m], 1e-9)
                tr = np.clip(tr + P["delta_mu"] * (1 if rng.random() < 0.5 else -1), 0, P["mu_max"])
                s[q][m] = s["K"][m] * tr
                s["nmut"] += 1
    return s


def fields(s):
    phi = s["phi"]
    mu = s["Qm"] / np.maximum(s["K"], 1e-9) * (s["K"] > 0.05)
    return np.stack([s["S"], s["K"], np.clip(mu / 3, 0, 1), s["L"], 4 * phi * (1 - phi), s["w"]]).astype(np.float32)


def matter(F):
    # an individual = the inside phase; recover phi >= 1/2 region from the channels
    return (F[1] + F[3] + F[4]).astype(np.float32)


def stats(s):
    from scipy import ndimage
    lab, n = ndimage.label(s["phi"] > 0.5)
    K = s["K"]
    out = {"cells": int(n), "nmut": s["nmut"]}
    for q, nm in (("Qm", "mu"), ("Qt", "tag")):
        out[nm] = round(float(s[q].sum() / max(K.sum(), 1e-9)), 3)
    return out


def damage(s, mask):
    """labkit gives a disk at the centroid of the largest component (only the interior of a
    walled cell, and mis-placed for cells wrapping the periodic edge). We use it only to pick
    the cell: take the phi > 1/2 component under the mask, compute its periodic centre and
    equivalent radius R, and reset to bath (S=1, catalysts=L=phi=0) a disk of radius 0.8 R
    centred 0.8 R from the cell centre along +x. That cuts the wall and ~30% of the cell; the
    erased fraction is stored in s["damage_frac"]."""
    from scipy import ndimage
    phi = s["phi"]
    H, W = phi.shape
    lab, n = ndimage.label(phi > 0.5)
    for ax in (0, 1):  # merge labels across the periodic edges
        a, b = (lab[0], lab[-1]) if ax == 0 else (lab[:, 0], lab[:, -1])
        for u, v in zip(a, b):
            if u and v and u != v:
                lab[lab == v] = u
    ids = lab[mask & (lab > 0)]
    if len(ids) == 0:
        return s
    cell = lab == np.bincount(ids).argmax()
    ys, xs = np.nonzero(cell)
    cy = np.angle(np.exp(2j * np.pi * ys / H).mean()) * H / (2 * np.pi) % H
    cx = np.angle(np.exp(2j * np.pi * xs / W).mean()) * W / (2 * np.pi) % W
    R = np.sqrt(cell.sum() / np.pi)
    yy, xx = np.mgrid[0:H, 0:W]
    dy = (yy - cy + H / 2) % H - H / 2
    dx = (xx - cx - 0.8 * R + W / 2) % W - W / 2
    hole = dy ** 2 + dx ** 2 <= (0.8 * R) ** 2
    s["damage_frac"] = float((hole & cell).sum() / cell.sum())
    s["S"][hole] = 1
    for k in ("K", "Qm", "Qt", "L", "phi"):
        s[k][hole] = 0
    return s
