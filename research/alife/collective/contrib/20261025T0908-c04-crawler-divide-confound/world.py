"""Growing, dividing phase-field crawlers (Ziebert, Swaminathan & Aranson 2012 crawler + growth).

    u_t = Du lap u - (1-u)(delta-u)u - alpha grad u . P
    P_t = Dp lap P - P/tau1 - t2 (1-u^2) P - beta(n) grad u - gamma (grad u . P) P,  |P| < 1
    delta = d0 + muA/V0 (A_k - V_k) + lamOK/V0 (G_ell * u - Mref V0) [inside bodies] - sigma |P|^2
    beta(n) = beta max(1 + chi (n - nchi), 0.2)          (actin made faster where food is)
    n_t = Dn lap n + rn (1 - n) - kn n u                  (consumed, regrowing nutrient)
    dV_k/dt = kup int_k n u - lam V_k - c0 - shed (V_k/A_k) int_k max(-du, 0)/dt

Bodies k are periodic connected components of u > labth. A_k = int_k u; V_k is the body's
content (target area). V_k is carried from step to step by u-weighted overlap: each old body's
content is shared among its successors by overlap, merges add, and content disappears only with
a body that vanishes. Growth: uptake of the nutrient. Costs: linear decay, a fixed maintenance
c0 per body, and shedding of content in proportion to the u-mass the body retracts (motion
costs content). Division: the finite-range term (Gaussian kernel, ell ~ cell radius, an
Ohta-Kawasaki-like long-range inhibition applied only inside bodies) makes a body that has
grown well beyond ell tear into pieces. Motility: Ziebert-Aranson actin polarization with
the myosin terms gamma, sigma. Diffusion is implicit spectral (periodic), reactions explicit.
GROW=0, lamOK=0, chi=0, shed=0 with the original defaults gives the classic single crawler
(20261025T0641-c04-crawler-positive-control). Override with WORLD_P='{"lamOK":0}'.
"""
import json
import os

import numpy as np
from scipy import ndimage

P = dict(N=256, dx=0.5, dt=0.05, Du=1.0, Dp=0.2, tau1=10.0, t2=0.4, alpha=3.0, beta=1.0,
         gamma=0.5, sigma=0.6, d0=0.5, muA=5.0, R0=12.0, ncell=1, p0=0.8,
         GROW=0, rho_m=1.0, Dm=1.0, kup=0.02, lam=0.01, dout=0.5, Dn=4.0, rn=0.005, n0=1.0, kn=0.03, kappa=0.0, nstar=0.3, eta=0.0, LOCAL=0, Rt=12.0, ell=12.0, Vloc=1.0, kfed=0.0, nbar=0.5, dmin=0.15, lamOK=0.0, Mref=0.6, labth=0.02, c0=0.0, chi=0.0, nchi=0.5, shed=0.0, t_starve=-1.0, t_cut=-1.0, cut=0.2, bV=0, okclip=0,
         spf=100)
# claim parameters (20261025T0828-c04-crawler-divide-claim); the classic crawler is GROW=0, lamOK=0, chi=0
P.update({"GROW": 1, "kn": 0.03, "rn": 0.0015, "ell": 10, "labth": 0.2, "c0": 1.5, "kup": 0.04,
          "sigma": 1.3, "alpha": 4, "spf": 50, "lamOK": 2, "chi": 2, "shed": 0.5})
P.update(json.loads(os.environ.get("WORLD_P", "{}")))

META = {
    "name": "crawler-divide",
    "family": "phase-field",
    "parent": None,
    "mutation": "growth by uptake, finite-range area penalty (division), food-modulated actin, shedding on retraction",
    "size": (int(P["N"]), int(P["N"])),
    "steps_per_frame": int(P["spf"]),
    "dt": P["dt"],
    "channels": ["u (cell)", "|P| (actin polarization)", "V/V0 (body content)", "n (nutrient)"],
    "matter": [0],
    "threshold": 0.25,
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
    if P["t_starve"] >= 0 and s["t"] >= P["t_starve"] and not s.get("starved"):
        # fork: all food removed at once and no regrowth from now on
        s["n"][:] = 0.0
        s["starved"] = True
    u, px, py, m, n = s["u"], s["px"], s["py"], s["m"], s["n"]
    dx, dt = P["dx"], P["dt"]
    da = dx * dx
    gx, gy = _grad(u, dx)
    lab, nb = plabel(u > P["labth"])
    idx = np.arange(1, nb + 1)
    if nb > 0:
        A = ndimage.sum(u, lab, index=idx) * da
        if P["GROW"]:
            # carry each body's content V across the step by u-weighted overlap: a split
            # shares V by overlap, a merge adds it; content is lost only with a vanished body
            V = np.zeros(nb)
            if s.get("lab") is not None and len(s["V"]):
                plab, pV = s["lab"], s["V"]
                both = (plab > 0) & (lab > 0)
                w = np.bincount((plab[both] - 1) * nb + (lab[both] - 1), weights=u[both],
                                minlength=len(pV) * nb).reshape(len(pV), nb)
                # each old body's content goes to its successors in proportion to overlap
                V = (pV / np.maximum(w.sum(axis=1), 1e-12)) @ w
            else:
                V = A.copy()
            upt = ndimage.sum(P["kup"] * n * u, lab, index=idx) * da
            V = np.maximum(V + dt * (upt - P["lam"] * V - P["c0"]), 0.0)
            rn = 0.0 if s.get("starved") else P["rn"]
            n = _ifft(n + dt * (rn * (1 - n) - P["kn"] * n * u), s["Ln"])
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
        if P["okclip"]:
            ok = np.maximum(ok, 0.0)  # penalize only bodies larger than the kernel scale
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
    if P["chi"] != 0:
        beta = P["beta"] * np.maximum(1 + P["chi"] * (s["n"] - P["nchi"]), 0.2)
    else:
        beta = P["beta"]
    if P["bV"] and P["GROW"] and nb > 0:
        # actin is made from the cell's content: production scales with content density V/A
        beta = beta * np.concatenate([[0.0], np.clip(s["V"] / np.maximum(A, 1e-9), 0, 1)])[lab]
    if P["t_cut"] >= 0 and s["t"] >= P["t_cut"]:
        beta = beta * P["cut"]  # fork: actin production (the rim layer's source) cut
    rpx = -damp * px - beta * gx - P["gamma"] * adv * px
    rpy = -damp * py - beta * gy - P["gamma"] * adv * py
    u_new = _ifft(u + dt * ru, s["Lu"])
    if P["GROW"] and P["shed"] > 0 and nb > 0:
        # retraction sheds content: each body loses shed * (V/A) * (u-mass it retracted)
        ret = ndimage.sum(np.maximum(u - u_new, 0.0), lab, index=idx) * da
        s["V"] = np.maximum(s["V"] - P["shed"] * s["V"] / np.maximum(A, 1e-9) * ret, 0.0)
    u = u_new
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
