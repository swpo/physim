"""Particle catalysts in phase cells (hybrid): phase_membrane with the catalyst field K
replaced by discrete Brownian catalyst particles that carry a kind and a lineage label.

phi  Allen-Cahn inside phase, tilted by links L:  dphi = Dp lap phi + r phi(1-phi)(phi-1/2+a(L-th))
S    substrate, free diffusion, fed F(1-S); consumed by particle duplication and link making.
L    links, phi^2-gated diffusion + wall-adsorption drift chi (as phase_membrane); made by particles.
particles  each carries mass m of catalyst. K = gaussian_filter(m * counts, sig) is the catalyst
     density they make. Per step a particle at pixel p:
       duplicates with probability c S (1 - K) phi  (daughter copies kind and label; mutation mu),
       dies with probability dK,
       deposits link production b y_kind S m at p (y_kind = yield of its kind),
       takes a Brownian step sqrt(2 DK) N(0,1); a step to lower phi is accepted with prob
       (phi_new/phi_old)^2 (gate=1), so particles are reflected by the wall.
The field reference (Q:particle-catalysts-in-phase-cells) is phase_membrane itself. Matching:
logistic autocatalysis c S K (1-K) phi, decay dK, link production b K S.
A neighbour's field cannot overwrite a particle: kind changes only at duplication (mutation).
"""
import numpy as np
from scipy import ndimage

META = {
    "name": "pcell-swim",
    "family": "hybrid-particle-field",
    "parent": "threads/autopoiesis/worlds/phase_membrane",
    "mutation": "catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate",
    "size": (128, 128),
    "steps_per_frame": 50,
    "dt": 1.0,
    "channels": ["S", "K particles", "L link", "membrane (wall)"],
    "matter": [1, 2, 3],
    "smooth": 1.0,
    "periodic": True,
}

P = dict(DS=0.2, DK=0.1, DL=0.1, Dp=0.1, r=0.2, a=4.0, th=0.15, F=0.006, b=0.05, dL=0.02,
         c=0.2, dK=0.02, chi=2.0, m=0.2, sig=1.0, gate=1, noise_amp=0.2, noise_KL=0.1, noise_K=0.6,
         nkinds=1, y1=1.0, y2=1.0, y3=0.0, mu=0.0, mup=0.0, cy=0.0, tmut=0, f1init=-1.0, ytrait=0, y0=1.0, muy=0.0, sy=0.05, ymax=2.0, scale=1.0, zmark=0, muslip=2.2, slip_sig=12.0, vcap=0.4, Nmax=200000, twin=0)


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


def _faces(u, ax):
    """MUSCL (van Leer limited) left/right states at face i+1/2 (from kstrail / c05 phase-slipdiv)."""
    up, um = np.roll(u, -1, ax), np.roll(u, 1, ax)
    d1, d2 = u - um, up - u
    slope = np.where(d1 * d2 > 0, 2 * d1 * d2 / (d1 + d2 + 1e-300), 0.0)
    return u + 0.5 * slope, np.roll(u - 0.5 * slope, -1, ax)


def muscl_div(rho, vy, vx):
    out = np.zeros_like(rho)
    for v, ax in ((vy, 0), (vx, 1)):
        vf = 0.5 * (v + np.roll(v, -1, ax))
        Lf, Rf = _faces(rho, ax)
        flux = np.where(vf > 0, vf * Lf, vf * Rf)
        out += flux - np.roll(flux, 1, ax)
    return out


def yields():
    return np.array([P["y1"], P["y2"], P["y3"]][: max(1, int(P["nkinds"]))])


def init(seed, size):
    rng = np.random.default_rng(seed)
    H, W = size
    sc = P["scale"]  # resolution test: lengths x sc (grid given by --size), diffusivities x sc^2
    n = ndimage.gaussian_filter(rng.standard_normal((H, W)), 3 * sc, mode="wrap")
    phi = np.clip(n / n.std() * P["noise_amp"], 0, 1)
    L = P["noise_KL"] * rng.random((H, W))
    # catalyst: uniform random density in [0, noise_K] per pixel, as Poisson particle counts
    lam = P["noise_K"] * rng.random((H, W)) / P["m"]
    cnt = rng.poisson(lam)
    iy, ix = np.nonzero(cnt)
    rep = cnt[iy, ix]
    py = np.repeat(iy, rep) + rng.random(rep.sum())
    px = np.repeat(ix, rep) + rng.random(rep.sum())
    N = len(py)
    nk = max(1, int(P["nkinds"]))
    kind = rng.integers(0, nk, N).astype(np.int8) if nk > 1 else np.zeros(N, np.int8)
    if P["f1init"] >= 0:  # optional: set the initial kind-1 fraction (0 = monoculture of kind 0)
        kind = (rng.random(N) < P["f1init"]).astype(np.int8)
    s = {"S": np.ones((H, W)), "L": L, "phi": phi, "py": py, "px": px, "kind": kind,
         "lab": np.arange(N, dtype=np.int64), "uid": np.arange(N, dtype=np.int64), "next": N, "rng": rng, "t": 0,
         "births": np.zeros(nk, np.int64), "deaths": np.zeros(nk, np.int64), "flips": 0}
    s["y"] = np.full(N, P["y0"])  # continuous heritable link yield (used when ytrait=1)
    s["z"] = np.full(N, P["y0"])  # inert neutral marker (zmark=1): inherited and mutated like y, no effect
    s["K"] = density(s, H, W)
    return s


def density(s, H, W, w=None):
    iy = s["py"].astype(np.int64) % H
    ix = s["px"].astype(np.int64) % W
    c = np.bincount(iy * W + ix, weights=w, minlength=H * W).reshape(H, W) * P["m"]
    return ndimage.gaussian_filter(c, P["sig"] * P["scale"], mode="wrap") if P["sig"] > 0 else c


def step(s):
    S, L, phi, rng = s["S"], s["L"], s["phi"], s["rng"]
    H, W = S.shape
    py, px, kind = s["py"], s["px"], s["kind"]
    iy = py.astype(np.int64) % H
    ix = px.astype(np.int64) % W
    K = s["K"]
    Sp, Kp, php = S[iy, ix], K[iy, ix], phi[iy, ix]
    yk = yields()
    # per-particle yield: kind table, or the continuous trait (ytrait=1; ytrait=2 = neutral twin:
    # the trait is inherited and mutates identically but every particle acts with y0)
    if P["ytrait"] == 1:
        yp = s["y"]
    elif P["ytrait"] == 2:
        yp = np.full(len(py), P["y0"])
    else:
        yp = yk[kind]
    # optional trade-off: link yield costs replication, dup x (1 + cy (1 - y))
    cost = np.maximum(1 + P["cy"] * (1 - yp), 0) if P["cy"] else 1.0
    pdup = np.clip(P["c"] * cost * Sp * (1 - Kp) * php, 0, 1)
    u = rng.random(len(py))
    dup = u < pdup
    die = (u >= pdup) & (u < pdup + P["dK"])
    # substrate taken by duplication (mass m each) and link production (b y S m per particle)
    wprod = yp * P["m"]
    prodL_pt = np.bincount(iy * W + ix, weights=wprod, minlength=H * W).reshape(H, W)
    s2 = P["scale"] ** 2
    prodL_pt = ndimage.gaussian_filter(prodL_pt, P["sig"] * P["scale"], mode="wrap") if P["sig"] > 0 else prodL_pt
    prodL = P["b"] * prodL_pt * S
    dupS = np.bincount(iy[dup] * W + ix[dup], minlength=H * W).reshape(H, W) * P["m"]
    nsub = int(np.ceil(s2 * P["DS"] / 0.2))  # explicit diffusion stays below D dt / dx^2 = 0.2
    Sd = S
    for _ in range(nsub):
        Sd = Sd + s2 * P["DS"] / nsub * lap(Sd)
    s["S"] = np.maximum(Sd - dupS - prodL + P["F"] * (1 - S), 0)
    # births: daughter copies kind and label; optional mutation flips kind
    nk = len(yk)
    dk = kind[dup].copy()
    nf = min(nk, 2)  # mu flips between the two producer kinds 0 <-> 1 (or among all if nk == 2)
    if nk > 1 and P["mu"] > 0 and len(dk):
        fl = (rng.random(len(dk)) < P["mu"]) & (dk < nf)
        dk[fl] = (dk[fl] + 1) % nf
        s["flips"] += int(fl.sum())
    if nk >= 3 and P["mup"] > 0 and len(dk) and s["t"] >= P["tmut"]:  # mutation of a producer into the parasite kind 2
        fp = (rng.random(len(dk)) < P["mup"]) & (dk < 2)
        dk[fp] = 2
        s["pflips"] = s.get("pflips", 0) + int(fp.sum())
    s["births"] += np.bincount(kind[dup], minlength=nk)
    s["deaths"] += np.bincount(kind[die], minlength=nk)
    keep = ~die
    py = np.concatenate([py[keep], py[dup] + 0.3 * rng.standard_normal(dup.sum())])
    px = np.concatenate([px[keep], px[dup] + 0.3 * rng.standard_normal(dup.sum())])
    kind = np.concatenate([kind[keep], dk])
    lab = np.concatenate([s["lab"][keep], s["lab"][dup]])
    yd = s["y"][dup].copy()
    if P["muy"] > 0 and len(yd):
        fm = rng.random(len(yd)) < P["muy"]
        yd[fm] = np.clip(yd[fm] + P["sy"] * rng.standard_normal(fm.sum()), 0, P["ymax"])
        s["ymut"] = s.get("ymut", 0) + int(fm.sum())
    yy = np.concatenate([s["y"][keep], yd])
    zd = s["z"][dup].copy()
    if P["zmark"] and P["muy"] > 0 and len(zd):
        fz = rng.random(len(zd)) < P["muy"]
        zd[fz] = np.clip(zd[fz] + P["sy"] * rng.standard_normal(fz.sum()), 0, P["ymax"])
    zz = np.concatenate([s["z"][keep], zd])
    nd = int(dup.sum())
    uid = np.concatenate([s["uid"][keep], np.arange(s["next"], s["next"] + nd, dtype=np.int64)])
    s["next"] += nd
    # Brownian step with phi^2 reflection gate
    sd = np.sqrt(2 * P["DK"] * s2)
    ny = py + sd * rng.standard_normal(len(py))
    nx = px + sd * rng.standard_normal(len(px))
    if P["gate"]:
        p0 = phi[py.astype(np.int64) % H, px.astype(np.int64) % W]
        p1 = phi[ny.astype(np.int64) % H, nx.astype(np.int64) % W]
        acc = np.where(p1 >= p0, 1.0, (p1 / np.maximum(p0, 1e-9)) ** 2)
        ok = rng.random(len(py)) < acc
        py, px = np.where(ok, ny, py) % H, np.where(ok, nx, px) % W
    else:
        py, px = ny % H, nx % W
    if len(py) > P["Nmax"]:  # safety cap: random cull (never expected)
        sel = rng.choice(len(py), int(P["Nmax"]), replace=False)
        py, px, kind, lab, uid, yy, zz = py[sel], px[sel], kind[sel], lab[sel], uid[sel], yy[sel], zz[sel]
    s["py"], s["px"], s["kind"], s["lab"], s["uid"], s["y"], s["z"] = py, px, kind, lab, uid, yy, zz
    # links: as phase_membrane
    g = phi * phi
    adv = 0.0
    if P["chi"]:
        w = 4 * phi * (1 - phi)
        vy = s2 * P["DL"] * P["chi"] * g * 0.5 * (np.roll(w, -1, 0) - np.roll(w, 1, 0))
        vx = s2 * P["DL"] * P["chi"] * g * 0.5 * (np.roll(w, -1, 1) - np.roll(w, 1, 1))
        adv = upwind_div(L, vy, vx)
    s["L"] = np.maximum(L + mob_div(L, g, s2 * P["DL"]) - adv + prodL - P["dL"] * L, 0)
    s["phi"] = np.clip(phi + s2 * P["Dp"] * lap(phi) + P["r"] * phi * (1 - phi) * (phi - 0.5 + P["a"] * (L - P["th"])), 0, 1)
    if P["muslip"]:  # label-free phoretic slip (c05 phase-slipdiv): v = mu G[phi^2 grad S] / G[phi^2] phi^2
        ph = s["phi"]; g2 = ph * ph; Sx = s["S"]
        gy = 0.5 * (np.roll(Sx, -1, 0) - np.roll(Sx, 1, 0))
        gx = 0.5 * (np.roll(Sx, -1, 1) - np.roll(Sx, 1, 1))
        sg = P["slip_sig"] * P["scale"]
        den = ndimage.gaussian_filter(g2, sg, mode="wrap") + 1e-3
        vy = P["muslip"] * ndimage.gaussian_filter(g2 * gy, sg, mode="wrap") / den * g2
        vx = P["muslip"] * ndimage.gaussian_filter(g2 * gx, sg, mode="wrap") / den * g2
        sp = np.hypot(vy, vx)
        cap = np.minimum(1.0, P["vcap"] / np.maximum(sp, 1e-12))
        vy, vx = vy * cap, vx * cap
        s["L"] = np.maximum(s["L"] - muscl_div(s["L"], vy, vx), 0)
        s["phi"] = np.clip(s["phi"] - muscl_div(ph, vy, vx), 0, 1)
        iy = s["py"].astype(np.int64) % H; ix = s["px"].astype(np.int64) % W  # particles ride the same flow
        s["py"] = (s["py"] + vy[iy, ix]) % H
        s["px"] = (s["px"] + vx[iy, ix]) % W
        s["vmax"] = float(sp.max())
    s["K"] = density(s, H, W)
    s["t"] += 1
    return s


def fields(s):
    phi = s["phi"]
    return np.stack([s["S"], s["K"], s["L"], 4 * phi * (1 - phi)]).astype(np.float32)


def particles(s):
    return np.stack([s["px"], s["py"], s["y"] if P["ytrait"] else s["kind"].astype(np.float64)], 1)


def stats(s):
    lab, n = ndimage.label(s["phi"] > 0.5)
    return {"N": int(len(s["py"])), "L": round(float(s["L"].sum()), 1), "cells": int(n),
            "births": s["births"].tolist(), "deaths": s["deaths"].tolist(), "flips": s["flips"]}


def damage(s, mask):
    H, W = mask.shape
    hit = mask[s["py"].astype(np.int64) % H, s["px"].astype(np.int64) % W]
    for k in ("py", "px", "kind", "lab", "uid", "y", "z"):
        s[k] = s[k][~hit]
    s["S"][mask] = 1
    s["L"][mask] = 0
    s["phi"][mask] = 0
    s["K"] = density(s, H, W)
    return s
