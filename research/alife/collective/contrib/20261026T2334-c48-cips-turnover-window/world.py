"""c48 (Q:fuel-powered-division): c40's layered CIPS world with the enzyme turnover charged to the fuel.
The active enzyme e inactivates at rate d into a diffusing inactive form i; i is reactivated only by the fuel,
at rate r F i, consuming y_r fuel per enzyme (e + i conserved; r set so the uniform bath is steady at e0, i0):
  de/dt = ... - d e + r F i        di/dt = Di lap i + d e - r F i        dF/dt = ... - y_r r F i
Control react_const=1: reactivation r Fs i with the constant bath fuel Fs (fuel-independent, pays no fuel).
Everything below is c40's text.

Catalysis-induced phase separation (CIPS) on a consumed, regrowing fuel: c40 defaults (repeated division).

Defaults (c40): cooperative catalysis n=2, kc=2, De=0.1, chi=3, DF=2, kF=0.2, e0=0.12, enzyme turnover d=0.003
(linearly stable bath: lsa growth rate -2e-3), started from a random field (std 0.03, correlation 16 px).
Amphiphile s (c40, 20261026T1100): ds/dt = Ds lap s - div(Ds chi_s s grad w) + ks_s cat - dec_s s, w = 4e(1-e),
made only by catalysis (so mostly by the bodies), one-way coupled (s does not act back on e, p or F).

e : enzyme, with uniform turnover: made everywhere at rate s0 = d*e0, lost at rate d*e
    (the turnover does not depend on F; c35's change to c23's world)
p : product of catalysis (decays)
F : fuel, consumed by catalysis, regrown toward 1 at rate kF (or held at 1: the reservoir)

  d e/dt = De lap e - div( chi e (1-e) grad p ) + d (e0 - e)        (drift up the product: a chemotactic
                                                           stand-in for Cotton et al.'s
                                                           Flory-Huggins cross-diffusion)
  d p/dt = Dp lap p + kc F e (1-p) - ks p
  d F/dt = DF lap F - y kc F e (1-p) + kF (1-F)

Cotton, Golestanian & Agudo-Canalejo (PRL 129, 158101, 2022): enzyme catalysis alone can phase
separate the enzyme; with fuel held by a reservoir the domains coarsen without end. Question
(Q:cips-fuel-limited-condensates): does a consumed fuel cap body size and make bodies split?
Numerics: periodic, dx=1, implicit spectral diffusion for all fields, explicit reactions,
conservative MUSCL volume-filling face flux for the enzyme drift (int e conserved exactly).
"""
import json
import os

import numpy as np

from labkit import ops

META = {
    "name": "cips-gene",
    "family": "catalysis-induced-phase-separation",
    "parent": "collective/contrib/20261026T1100-c40-cips-layered-divide-claim",
    "mutation": "c48: the enzyme turnover d(e0-e) replaced by inactivation -d e and fuel-powered reactivation r F i of a diffusing inactive enzyme i (consumes fuel); c40's layered world: an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying",
    "size": (192, 192),
    "steps_per_frame": 1000,
    "dt": 0.1,
    "channels": ["e", "p", "F", "s", "g1", "g2"],
    "matter": [0],
    "threshold": 0.5,
    "smooth": 1.0,
}

P = {
    "De": 0.1, "chi": 3.0, "kc": 2.0, "ks": 1.0, "DF": 2.0, "y": 1.0, "kF": 0.2,
    "Dp": 1.0,          # product diffusivity (1: c23 world)
    "n": 2.0,           # catalysis order in e (1: c23 world; 2: cooperative, e.g. a dimer-active enzyme)
    "d": 0.003,           # enzyme turnover rate (0: c23 world)
    "Lsc": 3.0,         # length scale in px: every diffusivity and chi multiplied by Lsc^2 (Lsc=1 is the question's dx=1 model)
    "hold": 0,          # 1: fuel held at 1 (reservoir, Cotton et al.)
    "e0": 0.12, "noise": 0.03, "dt": 0.1,
    "rf_len": 16.0,      # >0: initial noise is a smoothed random field with this correlation length (px)
    "plant_asp": 1.0,   # aspect ratio of the planted disk (x semi-axis = plant_r * plant_asp)
    "plant_r": 0.0,     # >0: mechanism test only, one planted enzyme disk (e=0.9) of this radius at the centre
    "ks_s": 1.0,        # amphiphile s made by catalysis at ks_s * cat (0: ablation of its only source)
    "Ds": 0.1,          # s diffusivity (times Lsc^2)
    "chi_s": 6.0,       # s adsorption: drift up grad w, w = 4 e (1-e) (interface indicator of the enzyme field)
    "dec_s": 0.02,      # s decay
    "fork_t": -1.0,     # time at which kF -> 0 everywhere (-1: never)
    "fork_d": -1.0,     # >=0: enzyme turnover rate after fork_t (control: 0 removes turnover with the fuel; -1: unchanged)
    "cut_t": -1.0, "cut_r": 0.0, "cut_y": 0.0, "cut_x": 0.0,   # local feed cut: kF=0 in a disk from cut_t
    # c48: fuel-powered turnover. The active enzyme e inactivates at rate d; the inactive form i is reactivated
    # by the fuel at rate r F i, which consumes y_r fuel per enzyme reactivated. e + i is conserved.
    "fuelturn": 1,      # 1: -d e + r F i (c48); 0: c40's d (e0 - e)
    "i0": 0.03,         # uniform inactive enzyme in the bath steady state (r is set from it: d e0 = r Fs i0)
    "Di": 1.0,          # inactive enzyme diffusivity (times Lsc^2); it does not drift up the product
    "y_r": 1.0,         # fuel consumed per enzyme reactivated
    "react_const": 0,   # 1: control, reactivation r Fs i with the bath steady fuel Fs (fuel-independent), no fuel consumed
    "react_const_t": -1.0,  # >=0: switch to the react_const control from this time on (for forks)
    # c48 gene: two variants g1, g2 of an autocatalytic label copied by the body's own catalysis, sealed inside bodies
    "gene": 1,
    "kg": 2.0,          # copying: kg * cat * g_k * (1 - g1 - g2) inside bodies (needs catalysis, hence fuel)
    "Dg": 0.05,         # label mobility inside bodies (times Lsc^2), min-gated: zero flux across every boundary face
    "dg": 0.002,        # label decay inside bodies
    "dg_out": 0.2,      # fast decay outside bodies
    "mu": 0.0,          # copying error: fraction of each kind's copies made as the other kind (reads no trait)
    "b2": 0.0,          # trait 2: enzyme inactivation rate inside a body multiplied by (1 + b2 * g2)
    "a2": 0.0,          # trait: catalysis rate inside a body multiplied by (1 + a2 * g2) (g2's effect; 0: neutral twin)
    "inoc_t": 1500.0,   # time at which every body (e>0.5) is inoculated with g1 = inoc_g
    "inoc_g": 0.3,
    "inoc_kind": 1,     # kind given to every body at inoc_t when inoc_mix=0 (1: g1, 2: g2)
    "inoc_mix": 0,      # 1: each body is inoculated with g1 or g2 by a fair coin (heredity test: kinds at seeding)
    "swap_T": 0.0,      # >0: mutation event every swap_T: a random pixel is drawn; if it lies in a body (e>0.5),
                        #     g1 and g2 are swapped in that whole body (symmetric, reads no trait); else nothing
    # c44 chemostat washout, trait-blind: every wash_T one random body (e>0.5 component, dilated 3 px) is removed;
    # c48: its excess enzyme is inactivated (moved into i in place), so e + i stays conserved; p, s, g1, g2 set to 0 there
    "wash_T": 0.0, "wash_t0": 6000.0, "wash_seed": 12345,
}
P.update(json.loads(os.environ.get("WORLD_P", "{}")))


def _faces(u, ax):
    up, um = np.roll(u, -1, ax), np.roll(u, 1, ax)
    d1, d2 = u - um, up - u
    slope = np.where(d1 * d2 > 0, 2 * d1 * d2 / (d1 + d2 + 1e-300), 0.0)
    return u + 0.5 * slope, np.roll(u - 0.5 * slope, -1, ax)


def vf_flux_div(e, p, chi):
    """div of chi e(1-e) grad p, conservative: face velocity chi (p_{i+1}-p_i), upwinded MUSCL e."""
    out = np.zeros_like(e)
    for ax in (-2, -1):
        vf = chi * (np.roll(p, -1, ax) - p)
        L, R = _faces(e, ax)
        flux = np.where(vf > 0, vf * L * (1 - R), vf * R * (1 - L))
        out += flux - np.roll(flux, 1, ax)
    return out


def up_flux_div(u, w, c):
    """div of c u grad w, conservative first-order upwind (face velocity c (w_{i+1}-w_i))."""
    out = np.zeros_like(u)
    for ax in (-2, -1):
        vf = c * (np.roll(w, -1, ax) - w)
        flux = np.where(vf > 0, vf * u, vf * np.roll(u, -1, ax))
        out += flux - np.roll(flux, 1, ax)
    return out


def gate_div(u, g, D):
    """sealed min-gated diffusion (TOOLBOX, membrane_evo): face mobility min(g_i, g_j), zero flux on boundary faces."""
    out = np.zeros_like(u)
    for ax in (0, 1):
        gf = np.minimum(g, np.roll(g, -1, ax))
        flux = D * gf * (np.roll(u, -1, ax) - u)
        out += flux - np.roll(flux, 1, ax)
    return out


def _ss_p(e, F, kc, ks):
    return kc * F * e / (kc * F * e + ks)


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    p_ = dict(P)
    xi = rng.standard_normal((H, W))
    if p_["rf_len"] > 0:
        # random field: white noise smoothed over rf_len px, rescaled to std 1 (still unstructured over the whole domain)
        from scipy.ndimage import gaussian_filter
        xi = gaussian_filter(xi, p_["rf_len"], mode="wrap")
        xi = (xi - xi.mean()) / xi.std()
    e = p_["e0"] + p_["noise"] * xi
    if p_["plant_r"] > 0:
        yy, xx = np.mgrid[0:H, 0:W]
        e = np.where((yy - H / 2) ** 2 + ((xx - W / 2) / p_["plant_asp"]) ** 2 < p_["plant_r"] ** 2, 0.9, e)
    e = np.clip(e, 0.0, 1.0)
    F = np.ones((H, W))
    if not p_["hold"]:
        # uniform steady state of the fuel for the mean enzyme
        Fs = 1.0
        for _ in range(200):
            pp = _ss_p(p_["e0"], Fs, p_["kc"], p_["ks"])
            Fs = p_["kF"] / (p_["kF"] + p_["y"] * p_["kc"] * p_["e0"] * (1 - pp)) if p_["kF"] > 0 else 0.0
        F = F * Fs
    p = _ss_p(e, F, p_["kc"], p_["ks"])
    L = ops.lap_symbol(H, W) * p_["Lsc"] ** 2     # all diffusion lengths scaled by Lsc
    dt = p_["dt"]
    yy, xx = np.mgrid[0:H, 0:W]
    Fs0 = float(F.mean())
    if p_["fuelturn"] and not p_["hold"]:
        # c48: exact uniform steady fuel with cooperative catalysis e0^n and the reactivation cost y_r d e0
        Fs0 = 1.0
        for _ in range(500):
            c0 = p_["kc"] * Fs0 * p_["e0"] ** p_["n"]
            pp = c0 / (c0 + p_["ks"])
            Fs0 = (p_["kF"] - p_["y_r"] * p_["d"] * p_["e0"]) / (
                p_["kF"] + p_["y"] * p_["kc"] * p_["e0"] ** p_["n"] * (1 - pp))
        F = np.full((H, W), Fs0)
        p = _ss_p(e ** p_["n"], F, p_["kc"], p_["ks"])
    r = p_["d"] * p_["e0"] / (Fs0 * p_["i0"]) if p_["i0"] > 0 else 0.0
    p_["r"], p_["Fs"] = r, Fs0
    return {"e": e, "p": p, "F": F, "s": np.zeros((H, W)), "t": 0.0, "i": np.full((H, W), p_["i0"]), "g1": np.zeros((H, W)), "g2": np.zeros((H, W)),
            "Li": 1.0 / (1 - dt * p_["Di"] * L),
            "Ls": 1.0 / (1 - dt * (p_["Ds"] * L - p_["dec_s"])), "shape": (H, W), "par": p_,
            "Le": 1.0 / (1 - dt * p_["De"] * L), "Lp": 1.0 / (1 - dt * (p_["Dp"] * L - p_["ks"])),
            "LF": 1.0 / (1 - dt * p_["DF"] * L), "yy": yy, "xx": xx}


def step(s):
    q, dt = s["par"], s["par"]["dt"]
    e, p, F = s["e"], s["p"], s["F"]
    sh = s["shape"]
    cat = q["kc"] * F * np.clip(e, 0, None) ** q["n"] * (1 - p)
    if q["gene"]:
        cat = cat * (1 + q["a2"] * s["g2"])
    dd = q["d"]
    if q["fork_d"] >= 0 and q["fork_t"] >= 0 and s["t"] >= q["fork_t"]:
        dd = q["fork_d"]
    fcost = 0.0
    if q["fuelturn"]:
        i = s["i"]
        const = q["react_const"] or (q["react_const_t"] >= 0 and s["t"] >= q["react_const_t"])
        react = q["r"] * (q["Fs"] if const else F) * i
        if dd != q["d"]:
            react = react * (dd / q["d"] if q["d"] > 0 else 0.0)
        dloc = dd * (1 + q["b2"] * s["g2"]) if q["gene"] and q["b2"] != 0 else dd
        turn = -dloc * e + react
        fcost = 0.0 if const else q["y_r"] * react   # the control pays no fuel
        s["i"] = ops.irfft2(ops.rfft2(i - dt * turn) * s["Li"], sh)
    else:
        turn = dd * (q["e0"] - e)
    e = e - dt * vf_flux_div(e, p, q["chi"] * q["Lsc"] ** 2) + dt * turn
    s["e"] = ops.irfft2(ops.rfft2(e) * s["Le"], sh)
    s["p"] = ops.irfft2(ops.rfft2(p + dt * cat) * s["Lp"], sh)
    ec = np.clip(s["e"], 0, 1)
    wi = 4 * ec * (1 - ec)
    sv = s["s"] - dt * up_flux_div(s["s"], wi, q["Ds"] * q["chi_s"] * q["Lsc"] ** 2) + dt * q["ks_s"] * cat
    s["s"] = ops.irfft2(ops.rfft2(sv) * s["Ls"], sh)
    if q["hold"]:
        s["F"] = F
    else:
        kF = q["kF"]
        if q["fork_t"] >= 0 and s["t"] >= q["fork_t"]:
            kF = 0.0
        if q["cut_t"] >= 0 and s["t"] >= q["cut_t"]:
            H, W = sh
            dy = (s["yy"] - q["cut_y"] + H / 2) % H - H / 2
            dx = (s["xx"] - q["cut_x"] + W / 2) % W - W / 2
            kF = kF * ((dy * dy + dx * dx) > q["cut_r"] ** 2)
        Fn = F + dt * (-q["y"] * cat - fcost + kF * (1 - F))
        s["F"] = ops.irfft2(ops.rfft2(Fn) * s["LF"], sh)
    if q["wash_T"] > 0 and s["t"] >= q["wash_t0"]:
        nw = int((s["t"] - q["wash_t0"]) // q["wash_T"])
        if nw >= s.get("n_wash", 0):
            s["n_wash"] = nw + 1
            from scipy import ndimage
            b = s["e"] > 0.5
            lab, n = ndimage.label(b)
            for a_, b_ in [(lab[0, :], lab[-1, :]), (lab[:, 0], lab[:, -1])]:
                for i_, j_ in zip(a_, b_):
                    if i_ and j_ and i_ != j_: lab[lab == j_] = i_
            ids = [k for k in np.unique(lab) if k]
            if ids:
                rng = s.setdefault("wrng", np.random.default_rng(q["wash_seed"]))
                k = ids[int(rng.integers(len(ids)))]
                m = ndimage.binary_dilation(lab == k, iterations=3)
                m = m | np.roll(ndimage.binary_dilation(np.roll(lab == k, (sh[0] // 2, sh[1] // 2), (0, 1)), iterations=3), (-(sh[0] // 2), -(sh[1] // 2)), (0, 1))
                bath = float(np.median(s["e"][~b])) if (~b).any() else q["e0"]
                ex = np.where(m, np.clip(s["e"] - bath, 0, None), 0.0)
                gm = float((s["g2"][lab == k]).mean()), float((s["g1"][lab == k]).mean())
                s["e"] = s["e"] - ex; s["i"] = s["i"] + ex
                for f in ("p", "s", "g1", "g2"):
                    s[f] = np.where(m, 0.0, s[f])
                s.setdefault("wash_log", []).append((round(s["t"]), int((lab == k).sum()), gm[1], gm[0]))
    if q["gene"]:
        inside = (s["e"] > 0.5).astype(float)
        if q["inoc_t"] >= 0 and s["t"] < q["inoc_t"] <= s["t"] + dt:
            if q["inoc_mix"]:
                from scipy import ndimage
                lab, n = ndimage.label(inside > 0)
                for a_, b_ in [(lab[0, :], lab[-1, :]), (lab[:, 0], lab[:, -1])]:
                    for i_, j_ in zip(a_, b_):
                        if i_ and j_ and i_ != j_: lab[lab == j_] = i_
                coin = np.random.default_rng(int(q.get("wash_seed", 0)) + 99).integers(0, 2, n + 1)
                kind = coin[lab]
                s["g1"] = np.where((inside > 0) & (kind == 0), q["inoc_g"], s["g1"])
                s["g2"] = np.where((inside > 0) & (kind == 1), q["inoc_g"], s["g2"])
            else:
                f = "g2" if q["inoc_kind"] == 2 else "g1"
                s[f] = np.where(inside > 0, q["inoc_g"], s[f])
        if q["swap_T"] > 0 and s["t"] >= q["inoc_t"]:
            ns = int((s["t"] - q["inoc_t"]) // q["swap_T"])
            if ns >= s.get("n_swap", 0):
                s["n_swap"] = ns + 1
                srng = s.setdefault("srng", np.random.default_rng(int(q.get("wash_seed", 0)) + 7))
                y, x = int(srng.integers(sh[0])), int(srng.integers(sh[1]))
                if inside[y, x] > 0:
                    from scipy import ndimage
                    lab, n = ndimage.label(inside > 0)
                    for a_, b_ in [(lab[0, :], lab[-1, :]), (lab[:, 0], lab[:, -1])]:   # periodic merge (c48 fix)
                        for i_, j_ in zip(a_, b_):
                            if i_ and j_ and i_ != j_: lab[lab == j_] = i_
                    m = lab == lab[y, x]
                    a, b = s["g1"].copy(), s["g2"].copy()
                    s["g1"] = np.where(m, b, a); s["g2"] = np.where(m, a, b)
                    s.setdefault("swap_log", []).append((round(s["t"]), y, x, int(m.sum())))
        g1, g2 = s["g1"], s["g2"]
        free = np.clip(1 - g1 - g2, 0, None)
        c1, c2 = q["kg"] * cat * g1 * free * inside, q["kg"] * cat * g2 * free * inside
        m = q["mu"]
        a1, a2_ = (1 - m) * c1 + m * c2, (1 - m) * c2 + m * c1
        dec = q["dg"] + q["dg_out"] * (1 - inside)
        D = q["Dg"] * q["Lsc"] ** 2
        s["g1"] = np.clip(g1 + dt * (gate_div(g1, inside, D) + a1 - dec * g1), 0, None)
        s["g2"] = np.clip(g2 + dt * (gate_div(g2, inside, D) + a2_ - dec * g2), 0, None)
    s["t"] += dt
    return s


def fields(s):
    return np.stack([s["e"], s["p"], s["F"], s["s"], s["g1"], s["g2"]])


def damage(s, mask):
    s["e"] = np.where(mask, 0.0, s["e"])
    return s
