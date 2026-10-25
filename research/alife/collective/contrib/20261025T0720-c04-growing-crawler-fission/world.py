"""Phase-field crawling cell (Ziebert, Swaminathan & Aranson 2012; Lober et al. 2015).

    u_t = Du lap u - (1-u)(delta-u)u - alpha grad u . P
    P_t = Dp lap P - P/tau1 - t2 (1-u^2) P - beta grad u - gamma (grad u . P) P,  |P| < 1
    delta = d0 + mu (A_k - V_k) - sigma |P|^2

A_k is the area (integral of u) of the connected body k that the pixel belongs to (periodic
labelling of u > 0.02), V_k its target area. With GROW=0 V_k = V0 for every body: a body-wise
version of the classic global area constraint (identical for one cell).

With GROW=1 the target area is carried by a biomass field m that the cell makes from a
regrowing nutrient n and that is sealed inside the body (min-gate face mobility, fast decay
outside):  V_k = (integral of m over body k) / rho_m
    m_t = div(Dm min(g_i,g_j) grad m) + kup n u - lam m - dout (1-g) m,   g = [u > 1/2]
    n_t = Dn lap n + rn (1 - n) - kup n u
Diffusion is implicit spectral (periodic); reactions explicit Euler.
Parameters can be overridden for screening with WORLD_P='{"sigma":1.3}'.
"""
import json
import os

import numpy as np
from scipy import ndimage

P = dict(N=256, dx=0.5, dt=0.05, Du=1.0, Dp=0.2, tau1=10.0, t2=0.4, alpha=3.0, beta=1.0,
         gamma=0.5, sigma=0.6, d0=0.5, muA=5.0, R0=12.0, ncell=1, p0=0.8,
         GROW=0, rho_m=1.0, Dm=1.0, kup=0.02, lam=0.01, dout=0.5, Dn=4.0, rn=0.005, n0=1.0, kn=0.03, kappa=0.0, nstar=0.3, eta=0.0, LOCAL=0, Rt=12.0, ell=12.0, Vloc=1.0, kfed=0.0, nbar=0.5, dmin=0.15, lamOK=0.0, Mref=0.6,
         spf=100)
P.update(json.loads(os.environ.get("WORLD_P", "{}")))

META = {
    "name": "crawler",
    "family": "phase-field",
    "parent": None,
    "mutation": "Ziebert-Aranson crawling cell, body-wise area constraint",
    "size": (int(P["N"]), int(P["N"])),
    "steps_per_frame": int(P["spf"]),
    "dt": P["dt"],
    "channels": ["u (cell)", "|P| (actin polarization)", "V/V0 (body content)", "n (nutrient)"],
    "matter": [0],
    "threshold": 0.5,
    "smooth": 0.0,
    "periodic": True,
    "radial_channels": [0, 1, 2, 3],
}


def plabel(mask):
    """Connected components of mask on a periodic grid (4-connectivity)."""
    lab, n = ndimage.label(mask)
    if n == 0:
        return lab, 0
    parent = np.arange(n + 1)

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for a_arr, b_arr in ((lab[:, 0], lab[:, -1]), (lab[0, :], lab[-1, :])):
        both = (a_arr > 0) & (b_arr > 0)
        for a, b in set(zip(a_arr[both].tolist(), b_arr[both].tolist())):
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[max(ra, rb)] = min(ra, rb)
    roots = np.array([find(i) for i in range(n + 1)])
    uniq, inv = np.unique(roots, return_inverse=True)
    return inv[lab], len(uniq) - 1


def _grad(f, dx):
    return ((np.roll(f, -1, 1) - np.roll(f, 1, 1)) / (2 * dx),
            (np.roll(f, -1, 0) - np.roll(f, 1, 0)) / (2 * dx))


def _gate_div(f, g, D, dx):
    """div(D min(g_i, g_j) grad f) on faces."""
    out = np.zeros_like(f)
    for ax in (0, 1):
        fn = np.roll(f, -1, ax)
        gf = np.minimum(g, np.roll(g, -1, ax))
        flux = D * gf * (fn - f) / dx
        out += (flux - np.roll(flux, 1, ax)) / dx
    return out


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    dx = P["dx"]
    k = 2 * np.pi * np.fft.fftfreq(H, dx)
    KX, KY = np.meshgrid(2 * np.pi * np.fft.fftfreq(W, dx), k)
    K2 = KX ** 2 + KY ** 2
    y, x = np.mgrid[0:H, 0:W] * dx
    u = np.zeros((H, W))
    px = np.zeros((H, W))
    py = np.zeros((H, W))
    m = np.zeros((H, W))
    Ly, Lx = H * dx, W * dx
    centres = []
    for i in range(int(P["ncell"])):
        for _ in range(200):
            c = rng.random(2) * (Ly, Lx)
            if all(np.hypot(*(((c - d + (Ly / 2, Lx / 2)) % (Ly, Lx)) - (Ly / 2, Lx / 2))) > 3 * P["R0"]
                   for d in centres):
                break
        centres.append(c)
        ddy = (y - c[0] + Ly / 2) % Ly - Ly / 2
        ddx = (x - c[1] + Lx / 2) % Lx - Lx / 2
        r = np.hypot(ddx, ddy)
        ui = 0.5 * (1 - np.tanh((r - P["R0"]) / np.sqrt(8 * P["Du"])))
        th = rng.random() * 2 * np.pi
        inside = ui > 0.5
        px[inside] = P["p0"] * np.cos(th)
        py[inside] = P["p0"] * np.sin(th)
        u = np.maximum(u, ui)
    m = P["rho_m"] * (u > 0.5) * (1.0 if P["GROW"] else 0.0)
    n = np.full((H, W), P["n0"])
    dt = P["dt"]
    return {"u": u, "px": px, "py": py, "m": m, "n": n, "t": 0.0,
            "Lu": 1 / (1 + dt * P["Du"] * K2), "Lp": 1 / (1 + dt * P["Dp"] * K2),
            "Ln": 1 / (1 + dt * P["Dn"] * K2),
            "G": np.exp(-0.5 * K2 * P["ell"] ** 2) * 2 * np.pi * P["ell"] ** 2 / dx ** 2,
            "V0": np.pi * P["Rt"] ** 2, "rng": rng, "lab": None, "V": np.zeros(0)}


def _ifft(f, L):
    return np.real(np.fft.ifft2(np.fft.fft2(f) * L))


def step(s):
    u, px, py, m, n = s["u"], s["px"], s["py"], s["m"], s["n"]
    dx, dt = P["dx"], P["dt"]
    da = dx * dx
    gx, gy = _grad(u, dx)
    lab, nb = plabel(u > 0.02)
    idx = np.arange(1, nb + 1)
    if nb > 0:
        A = ndimage.sum(u, lab, index=idx) * da
        if P["GROW"]:
            # carry each body's content V across the step by u-weighted overlap: a split
            # shares V by area, a merge adds it, nothing is created or lost
            V = np.zeros(nb)
            if s.get("lab") is not None and len(s["V"]):
                plab, pV = s["lab"], s["V"]
                pA = ndimage.sum(u, plab, index=np.arange(1, len(pV) + 1))
                both = (plab > 0) & (lab > 0)
                w = np.bincount((plab[both] - 1) * nb + (lab[both] - 1), weights=u[both],
                                minlength=len(pV) * nb).reshape(len(pV), nb)
                V = (pV / np.maximum(pA, 1e-12)) @ w
            else:
                V = A.copy()
            upt = ndimage.sum(P["kup"] * n * u, lab, index=idx) * da
            V = V + dt * (upt - P["lam"] * V)
            n = _ifft(n + dt * (P["rn"] * (1 - n) - P["kn"] * n * u), s["Ln"])
            s["n"] = np.maximum(n, 0)
            s["V"], s["lab"] = V, lab
        else:
            V = np.full(nb, s["V0"])
        dev = np.concatenate([[0.0], A - V])[lab]
    else:
        dev = np.zeros_like(u)
        s["V"], s["lab"] = np.zeros(0), lab
    if P["LOCAL"]:
        M = _ifft(u, s["G"]) * da
        dev = M - P["Vloc"] * s["V0"]
        if P["kfed"] > 0:
            dev = dev - P["kfed"] * s["V0"] * (s["n"] - P["nbar"])
    if P["lamOK"] > 0:
        M = _ifft(u, s["G"]) * da
        ok = P["lamOK"] / s["V0"] * (M - P["Mref"] * s["V0"]) * (lab > 0)
    else:
        ok = 0.0
    pp = px * px + py * py
    delta = ok +  P["d0"] + P["muA"] / s["V0"] * dev - P["sigma"] * pp
    if P["kappa"] > 0:
        delta = delta + P["kappa"] * np.maximum(P["nstar"] - s["n"], 0.0)
    if P["LOCAL"]:
        delta = np.maximum(delta, P["dmin"])
    adv = gx * px + gy * py
    ru = -(1 - u) * (delta - u) * u - P["alpha"] * adv
    damp = 1 / P["tau1"] + P["t2"] * (1 - u * u)
    rpx = -damp * px - P["beta"] * gx - P["gamma"] * adv * px
    rpy = -damp * py - P["beta"] * gy - P["gamma"] * adv * py
    u = _ifft(u + dt * ru, s["Lu"])
    px = _ifft(px + dt * rpx, s["Lp"])
    py = _ifft(py + dt * rpy, s["Lp"])
    if P["eta"] > 0:
        rng = s["rng"]
        amp = P["eta"] * np.sqrt(dt) * u
        px = px + amp * rng.standard_normal(u.shape)
        py = py + amp * rng.standard_normal(u.shape)
    pm = np.sqrt(px * px + py * py)
    sc = np.minimum(1.0, 0.999 / np.maximum(pm, 1e-12))
    s["u"], s["px"], s["py"] = u, px * sc, py * sc
    s["t"] += dt
    return s


def fields(s):
    lab, V = s.get("lab"), s.get("V")
    if P["GROW"] and lab is not None and len(V):
        vmap = np.concatenate([[0.0], V / s["V0"]])[lab] * s["u"]
    else:
        vmap = np.zeros_like(s["u"])
    return np.stack([s["u"], np.sqrt(s["px"] ** 2 + s["py"] ** 2), vmap, s["n"]])


def damage(s, mask):
    s["u"][mask] = 0.0
    s["px"][mask] = 0.0
    s["py"][mask] = 0.0
    return s
