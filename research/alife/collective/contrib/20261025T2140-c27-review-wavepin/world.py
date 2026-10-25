"""Wave-pinning phase-field crawler (Camley, Zhao, Li, Levine & Rappel, PRE 95, 012401, 2017).

    dphi/dt = (rho - rho*) |grad phi| + chi (lap phi - G'(phi)/eps^2),   G = 18 phi^2 (1-phi)^2
    d(phi rho)/dt = Pe^-1 div(phi grad rho) + phi f(rho, rho_cyt)
    f = -K rho (rho - 1/2)(rho - m rho_cyt)          (KIN=0, bistable wave-pinning kinetics)
    f = -Klin (rho - m rho_cyt / 2)                  (KIN=1, linear twin, no bistability)
    rho_cyt = (C - int rho phi) / int phi            (one well-mixed cytosolic pool)

rho is solved as d rho/dt = Pe^-1 div(phi~ grad rho)/phi~ - rho (dphi/dt)/phi~ + f with
phi~ = phi + 1e-4 (conservative flux form), semi-implicit spectral stabilisation for both
fields. Units: box L = 2.5, cell R0 = 1.

Damage (inside the world, so the undamaged twin is the same seed without it): at t = cut_t
erase an angular sector of fraction cut_frac about the cell centroid, centred on the
leading edge (cut_mode 'front', direction of the rho-weighted centroid offset) or on the
rear ('rear'). phi and rho are set to 0 in the sector and the erased protein leaves the cell:
C' = C - int_cut phi (rho + rho_cyt). Weak ongoing noise eta on rho inside the cell.
Overrides: WORLD_P='{"chi":0.2}'.
"""
import json
import os

import numpy as np
from scipy import ndimage

P = dict(N=256, L=5.0, dt=1e-3, chi=0.25, Pe_inv=0.3, K=500.0, rho_s=0.2, m=0.5, C=6.0,
         eps=0.1, R0=0.85, rho0=1.0, noise0=0.2, eta=2.0, KIN=0, Klin=125.0,
         ffrac=0.75, PER_BODY=1, cut_t=-1.0, cut_mode="front", cut_frac=0.3, spf=200)
P.update(json.loads(os.environ.get("WORLD_P", "{}")))

META = {
    "name": "wavepin-crawler-r2",
    "family": "crawler-phase-field",
    "parent": None,
    "mutation": "Camley et al. 2017 crawler at low contractility rho*=0.2 with weak noise eta=2 on rho; optional sector cut at cut_t (WORLD_P) and linear-kinetics twin (KIN=1)",
    "size": (int(P["N"]), int(P["N"])),
    "steps_per_frame": int(P["spf"]),
    "dt": P["dt"],
    "channels": ["phi (cell)", "rho (polarity, inside)", "phi*rho"],
    "matter": [0],
    "threshold": 0.5,
    "smooth": 0.0,
    "periodic": True,
    "radial_channels": [0, 1],
}


def _grad(f, dx):
    return ((np.roll(f, -1, 1) - np.roll(f, 1, 1)) / (2 * dx),
            (np.roll(f, -1, 0) - np.roll(f, 1, 0)) / (2 * dx))


def _divflux(rho, a, dx):
    """div(a grad rho) with face-averaged coefficient."""
    out = np.zeros_like(rho)
    for ax in (0, 1):
        af = 0.5 * (a + np.roll(a, -1, ax))
        fl = af * (np.roll(rho, -1, ax) - rho) / dx
        out += (fl - np.roll(fl, 1, ax)) / dx
    return out


def _lap(f, dx):
    return (np.roll(f, 1, 0) + np.roll(f, -1, 0) + np.roll(f, 1, 1) + np.roll(f, -1, 1) - 4 * f) / dx ** 2


def _ifft(f, L):
    return np.real(np.fft.ifft2(np.fft.fft2(f) * L))


def init(seed, size):
    s = _init(seed, size)
    da = s["dx"] ** 2
    s["cyt"] = np.full_like(s["phi"], (P["C"] - (s["rho"] * s["phi"]).sum() * da) / (s["phi"].sum() * da))
    return s


def _init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    dx = P["L"] / W
    y, x = (np.mgrid[0:H, 0:W] + 0.5) * dx
    cx, cy = P["L"] / 2, P["L"] / 2
    r = np.hypot(x - cx, y - cy)
    phi = 0.5 * (1 - np.tanh(3 * (r - P["R0"]) / P["eps"]))
    th = rng.random() * 2 * np.pi
    proj = ((x - cx) * np.cos(th) + (y - cy) * np.sin(th))
    inside = phi > 0.5
    front = proj > np.quantile(proj[inside], 1 - P["ffrac"])
    rho = np.where(front, P["rho0"], 0.0) + P["noise0"] * rng.standard_normal((H, W))
    rho = np.clip(rho, 0, None) * (phi > 0.05)
    k = 2 * np.pi * np.fft.fftfreq(W, dx)
    KX, KY = np.meshgrid(k, 2 * np.pi * np.fft.fftfreq(H, dx))
    K2 = KX ** 2 + KY ** 2
    dt = P["dt"]
    return {"phi": phi, "rho": rho, "t": 0.0, "C": P["C"], "dx": dx, "rng": rng, "cut_done": False,
            "Lphi": 1 / (1 + dt * P["chi"] * K2), "Lrho": 1 / (1 + dt * P["Pe_inv"] * K2),
            "K2": K2, "x": x, "y": y, "log": [], "cyt": None}


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


def update_cyt(s, phi_old, rho_old, cyt_old):
    """One well-mixed cytosolic pool per connected body (PER_BODY=1): each new body keeps the
    protein (bound + cytosolic) that the previous fields held on its support, so a body that
    splits shares its pool by content and separated bodies do not exchange protein."""
    da = s["dx"] ** 2
    if not P["PER_BODY"]:
        A = s["phi"].sum() * da
        s["cyt"] = np.full_like(s["phi"], (s["C"] - (s["rho"] * s["phi"]).sum() * da) / max(A, 1e-9))
        return
    lab, nb = plabel(s["phi"] > 0.01)
    olab, onb = s.get("lab"), s.get("nb", 0)
    if olab is None:
        olab, onb = plabel(phi_old > 0.01)
    s["lab"], s["nb"] = lab, nb
    if nb == 0:
        s["cyt"] = np.zeros_like(s["phi"])
        return
    idx = np.arange(1, nb + 1)
    # protein of each old body, handed to the new bodies in proportion to phi-weighted overlap
    Nj = ndimage.sum(phi_old * (rho_old + cyt_old), olab, np.arange(1, onb + 1)) if onb else np.zeros(0)
    both = (olab > 0) & (lab > 0)
    w = np.bincount((olab[both] - 1) * nb + (lab[both] - 1), weights=phi_old[both] + 1e-12,
                    minlength=onb * nb).reshape(onb, nb)
    tot = w.sum(1, keepdims=True)
    Nk = (Nj[:, None] * w / np.where(tot > 0, tot, 1)).sum(0) if onb else np.zeros(nb)
    Bk = ndimage.sum(s["phi"] * s["rho"], lab, idx)
    Ak = ndimage.sum(s["phi"], lab, idx)
    ck = np.maximum((Nk - Bk) / np.maximum(Ak, 1e-12), 0)
    s["cyt"] = np.concatenate([[0.0], ck])[lab]


def rho_cyt(s):
    """area-weighted mean cytosolic concentration (diagnostic)."""
    return float((s["cyt"] * s["phi"]).sum() / max(s["phi"].sum(), 1e-12))


def polarity(s):
    """centroid of phi, unit vector from it to the rho*phi centroid (periodic, via angles)."""
    L = P["L"]
    phi, q = s["phi"], s["phi"] * s["rho"]
    out = []
    for w in (phi, q):
        cs = []
        for X in (s["x"], s["y"]):
            a = 2 * np.pi * X / L
            cs.append((np.arctan2((w * np.sin(a)).sum(), (w * np.cos(a)).sum()) % (2 * np.pi)) * L / (2 * np.pi))
        out.append(np.array(cs))
    c, cq = out
    d = (cq - c + L / 2) % L - L / 2
    return c, d


def cut(s):
    L = P["L"]
    c, d = polarity(s)
    ang = np.arctan2(d[1], d[0])
    if P["cut_mode"] == "rear":
        ang += np.pi
    ddx = (s["x"] - c[0] + L / 2) % L - L / 2
    ddy = (s["y"] - c[1] + L / 2) % L - L / 2
    a = np.angle(np.exp(1j * (np.arctan2(ddy, ddx) - ang)))
    mask = (np.abs(a) < np.pi * P["cut_frac"]) & (np.hypot(ddx, ddy) < 1.0 * L / 2)
    if P["cut_mode"] == "polarity":
        # erase the whole polarity domain (rho > 0.3 inside the cell and its rim)
        mask = (s["rho"] > 0.3) & (s["phi"] > 1e-3)
    da = s["dx"] ** 2
    C0 = (s["phi"] * (s["rho"] + s["cyt"])).sum() * da
    rc = s["cyt"][mask]
    afrac = s["phi"][mask].sum() / s["phi"].sum()
    if P["cut_mode"] == "chem":
        # erase the membrane-bound polarity protein only; the cell's shape and cytosol stay
        mask = (s["rho"] > 0.3) & (s["phi"] > 1e-3)
        lost = (s["phi"][mask] * s["rho"][mask]).sum() * da
        afrac = 0.0
    else:
        lost = (s["phi"][mask] * (s["rho"][mask] + rc)).sum() * da
        s["phi"][mask] = 0.0
    s["C"] -= lost
    s["rho"][mask] = 0.0
    if P["cut_mode"] != "chem":
        s["cyt"][mask] = 0.0
    s["cut_info"] = {"t": s["t"], "mode": P["cut_mode"], "area_frac": float(afrac),
                     "protein_lost_frac": float(lost / C0)}
    s["cut_done"] = True
    return s


def step(s):
    if P["cut_t"] >= 0 and not s["cut_done"] and s["t"] >= P["cut_t"]:
        s = cut(s)
    phi, rho, dx, dt = s["phi"], s["rho"], s["dx"], P["dt"]
    gx, gy = _grad(phi, dx)
    gn = np.sqrt(gx * gx + gy * gy)
    eps2 = P["eps"] ** 2
    Gp = 36 * phi * (1 - phi) * (1 - 2 * phi)
    lap = _lap(phi, dx)
    dphi = (rho - P["rho_s"]) * gn + P["chi"] * (lap - Gp / eps2)
    if P.get("freeze", 0):
        dphi = 0 * dphi
        lap = 0 * lap
    rc = s["cyt"]
    if P["KIN"] == 0:
        f = -P["K"] * rho * (rho - 0.5) * (rho - P["m"] * rc)
    else:
        f = -P["Klin"] * (rho - 0.5 * P["m"] * rc)
    q = phi * rho
    # Camley et al. App. A: evolve q = phi rho, recover rho = q/phi (q where phi < 1e-4)
    dq = P["Pe_inv"] * _divflux(rho, phi, dx) + phi * f
    phi_n = phi if P.get("freeze", 0) else _ifft(phi + dt * (dphi - P["chi"] * lap), s["Lphi"])
    q_n = _ifft(q + dt * (dq - P["Pe_inv"] * _lap(q, dx)), s["Lrho"])
    phi_n = np.clip(phi_n, 0, 1)
    rho_n = np.where(phi_n >= 1e-4, q_n / np.maximum(phi_n, 1e-4), q_n)
    if P["eta"] > 0:
        rho_n = rho_n + P["eta"] * np.sqrt(dt) * s["rng"].standard_normal(rho.shape) * (phi > 0.5)
    phi_o, rho_o, cyt_o = s["phi"], s["rho"], s["cyt"]
    s["phi"] = phi_n
    s["rho"] = np.clip(rho_n, 0, None)
    update_cyt(s, phi_o, rho_o, cyt_o)
    s["t"] += dt
    return s


def fields(s):
    return np.stack([s["phi"], s["rho"] * (s["phi"] > 0.5), s["rho"] * s["phi"]])


def damage(s, mask):
    s["phi"][mask] = 0.0
    s["rho"][mask] = 0.0
    return s
