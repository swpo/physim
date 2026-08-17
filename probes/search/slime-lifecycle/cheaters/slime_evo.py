
"""slime_evo.py — slime lifecycle (certified c30) + heritable cooperativeness.

Evolution layer (the Dictyostelium cheater problem):
  K strain bins with trait c_k = linspace(0,1,K). VK[k] = biomass of strain k.
  PARTICULATE inheritance: growth at a site is allocated to bins in proportion
  to the site's current composition (clonal copying); mutation moves a small
  fraction mu of NEW growth to adjacent bins. Traits never average.
  SIGNAL COST: while a site is emitting (E>0), each strain burns biomass
  exp(-lam_c * c_k): cooperators pay, cheaters ride for free.
  EMISSION ~ cooperator-weighted biomass sat_c = Vc/(Vc+V_h), Vc = sum c_k VK.
  A pure-cheater site fires but emits nothing -> relay/aggregation degrade
  where cooperation is scarce (public-good failure).
  SHARED BENEFIT: crowding protection, chemotaxis, dispersal are trait-blind.
  DEMOGRAPHIC noise sig_d: composition jitter on growth (regenerates
  between-site variance; set 0 to test the deterministic limit).
  NO fitness function anywhere: selection emerges from the lifecycle.
"""
import sys
import numpy as np
from scipy import ndimage

sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/slime-lifecycle")
import slime
from slime import lap, smooth9, gradc

C30 = {"rho": 0.0003614125334469841, "d0": 0.0010594617613073891,
       "pd": 0.9325258075035722, "chi_a": 13.053734982241894,
       "g": 0.047816969591130645, "T_r": 24, "p_spont": 0.0007398342764553882,
       "R_star": 0.12, "R_wake": 0.55}

DEFAULTS = dict(slime.DEFAULTS)
DEFAULTS.update(C30)
DEFAULTS.update(dict(
    K=11, lam_c=2e-3, mu=0.01, init_c="uniform",
    N_f=3.0,        # founder number of the wake bottleneck (Dirichlet conc.)
    V_found=0.5,    # only dense mound cores get bottlenecked
    a_s=2.4,        # recalibrated: <c>=0.5 world emits like certified c30
    a_a=0.10,       # same recalibration for the A integrator
))


def advectK(V, ux, uy):
    """Donor-cell upwind advection for stacked strains V (K,L,L); ux,uy (L,L)."""
    uxf = 0.5 * (ux + np.roll(ux, -1, 0))
    uyf = 0.5 * (uy + np.roll(uy, -1, 1))
    Fx = np.where(uxf > 0, uxf * V, uxf * np.roll(V, -1, -2))
    Fy = np.where(uyf > 0, uyf * V, uyf * np.roll(V, -1, -1))
    out = (np.maximum(Fx, 0) - np.minimum(np.roll(Fx, 1, -2), 0)
           + np.maximum(Fy, 0) - np.minimum(np.roll(Fy, 1, -1), 0))
    lam = np.minimum(1.0, 0.9 * V / (out + 1e-12))
    Fx = Fx * np.where(uxf > 0, lam, np.roll(lam, -1, -2))
    Fy = Fy * np.where(uyf > 0, lam, np.roll(lam, -1, -1))
    return -(Fx - np.roll(Fx, 1, -2)) - (Fy - np.roll(Fy, 1, -1))


def diffuseK(V, D):
    """Conservative diffusion for stacked strains; D (L,L) face-averaged."""
    Dxf = 0.5 * (D + np.roll(D, -1, 0))
    Dyf = 0.5 * (D + np.roll(D, -1, 1))
    Fx = Dxf * (np.roll(V, -1, -2) - V)
    Fy = Dyf * (np.roll(V, -1, -1) - V)
    return (Fx - np.roll(Fx, 1, -2)) + (Fy - np.roll(Fy, 1, -1))


def run(params=None, T=60000, seed=0, rec=50, snap_times=(), keep_fields=False):
    p = dict(DEFAULTS)
    if params:
        p.update(params)
    L = int(p["L"]); K = int(p["K"])
    cbins = np.asarray(p.get("cbins", np.linspace(0.0, 1.0, K)), float)
    K = len(cbins)
    costfac = np.exp(-p["lam_c"] * cbins)[:, None]
    rng = np.random.default_rng(seed)
    R = np.ones((L, L))
    Vtot0 = p["V0"] * (1.0 + 0.1 * rng.standard_normal((L, L)))
    Vtot0 = np.maximum(Vtot0, 0.01)
    VK = np.zeros((K, L, L))
    mode = p["init_c"]
    if mode == "top" or K == 1:
        VK[-1] = Vtot0
    elif mode == "uniform":
        VK[:] = Vtot0 / K
    else:  # mosaic: monoclonal patches; bin weights optionally skewed
        eta = {"mosaic": 0.0, "mosaic_lo": -6.0, "mosaic_hi": 6.0}[mode]
        w = np.exp(eta * cbins); w = w / w.sum()
        u = smooth9(rng.random((L, L)), int(p.get("mosaic_sm", 2)))
        qs = np.quantile(u, np.concatenate([[0.0], np.cumsum(w)]))
        qs[0] -= 1; qs[-1] += 1
        binmap = np.clip(np.digitize(u, qs) - 1, 0, K - 1)
        for k in range(K):
            VK[k][binmap == k] = Vtot0[binmap == k]
    S = np.zeros((L, L)); A = np.zeros((L, L))
    E = np.zeros((L, L), np.int32); Q = np.zeros((L, L), np.int32)
    H = np.zeros((L, L), bool)
    Wd = np.zeros((L, L), np.int32); Ww = np.zeros((L, L), np.int32)

    n_rec = T // rec + 1
    keys = ("t", "cv", "lf", "ncl", "rmean", "vmean", "hf", "aggm", "fire",
            "cmean", "csd", "rass", "vcoop")
    ser = {k: np.zeros(n_rec) for k in keys}
    fires = np.zeros(T, dtype=np.int32)
    fire_hist = np.zeros(1001, dtype=np.int64)
    lastF = np.full((L, L), -1, dtype=np.int64)
    snaps = {}
    ri = 0
    Te, Tr = int(p["T_e"]), int(p["T_r"])
    nsub = int(p["S_sub"])
    mu = p["mu"]; sig_d = p.get("sig_d", 0.0)
    cb3 = cbins[:, None, None]

    for t in range(T):
        V = VK.sum(0)
        Rs = smooth9(R, int(p["n_sense"]))
        starving = (Rs < p["R_star"]) | ((S > p["S_dev"]) & (Rs < p["R_join"]))
        want_h = np.where(starving, True, np.where(Rs > p["R_wake"], False, H))
        newly_h = want_h & ~H & (Ww == 0)
        newly_f = ~want_h & H & (Wd == 0)
        H = H.copy(); H[newly_h] = True; H[newly_f] = False
        Wd[newly_h] = int(p["T_dev"]); Ww[newly_f] = int(p["T_wake"])
        Wd = np.maximum(Wd - 1, 0); Ww = np.maximum(Ww - 1, 0)
        Hf = H.astype(float)
        Vs = smooth9(V, 1)
        C = Vs * Vs / (Vs * Vs + p["V_c"] ** 2)
        # --- relay (fire capability on total V; emission on cooperator mass)
        can = H & (Q == 0) & (V > p["V_min"]) & (C < p["C_spore"])
        fire = can & ((S > p["S_thr"]) | (rng.random((L, L)) < p["p_spont"] * V))
        E[fire] = Te; Q[fire] = Te + Tr
        fires[t] = int(fire.sum())
        seen = fire & (lastF >= 0)
        if seen.any():
            iv = np.clip(t - lastF[seen], 0, 1000)
            fire_hist += np.bincount(iv, minlength=1001)
        lastF[fire] = t
        Vc = (cb3 * VK).sum(0)
        sat_c = Vc / (Vc + p["V_h"])
        firing = (E > 0)
        for _ in range(nsub):
            S = S + (p["Ds"] / nsub) * lap(S)
        S = S - p["ks"] * S + p["a_s"] * sat_c * firing
        np.maximum(S, 0.0, out=S)
        # SIGNAL COST: emitting sites burn biomass prop. to own c_k
        if p["lam_c"] > 0 and firing.any():
            VK[:, firing] *= costfac
        E = np.maximum(E - 1, 0); Q = np.maximum(Q - 1, 0)
        A = A + p["Da"] * lap(A) - p["ka"] * A + p["a_a"] * sat_c * firing
        # --- movement (trait-blind: cheaters ride gradients for free)
        gax, gay = gradc(A)
        pack = np.clip(1.0 - Vs / p["V_pack"], 0.0, 1.0)
        Ff = 1.0 - Hf
        Gf = Ff * (Ww > 0)
        ux = (np.clip(p["chi_a"] * gax, -p["u_max"], p["u_max"]) * Hf * pack
              - np.clip(p["chi_d"] * gax, -p["u_max"], p["u_max"]) * Gf)
        uy = (np.clip(p["chi_a"] * gay, -p["u_max"], p["u_max"]) * Hf * pack
              - np.clip(p["chi_d"] * gay, -p["u_max"], p["u_max"]) * Gf)
        Dv = p["Dv0"] + p["Dv_fed"] * (Ff - Gf) + p["Dv_germ"] * Gf
        np.minimum(Dv, 0.24, out=Dv)
        VK = VK + advectK(VK, ux, uy)
        VK = VK + diffuseK(VK, Dv)
        np.maximum(VK, 0.0, out=VK)
        # FOUNDER BOTTLENECK at wake (Dicty spore-head sampling): when a mound
        # germinates, its outgoing lineage pool descends from ~N_f founder
        # cells. Per waking mound (connected component of newly-fed dense
        # sites) draw ONE Dirichlet(N_f * share) composition and assign it to
        # the whole mound (site masses unchanged). Strain-blind, mass-
        # conserving, no fitness function: pure demographic sampling.
        if p["N_f"] > 0 and newly_f.any():
            wakemask = newly_f & (Vs > p["V_found"])
            if wakemask.any():
                labw, nw = ndimage.label(wakemask)
                for ci in range(1, nw + 1):
                    msk = labw == ci
                    mound = VK[:, msk]
                    tot = mound.sum()
                    if tot < 1e-6:
                        continue
                    share = mound.sum(1) / tot
                    alpha = np.maximum(p["N_f"] * share, 1e-12)
                    draw = rng.gamma(alpha)
                    ssum = draw.sum()
                    if ssum <= 0:
                        continue
                    draw = draw / ssum
                    VK[:, msk] = draw[:, None] * mound.sum(0)[None, :]
        V = VK.sum(0)
        Vs = smooth9(V, 1)
        C = Vs * Vs / (Vs * Vs + p["V_c"] ** 2)
        # --- eat / grow (particulate: growth copies local composition)
        eatf = p["g"] * (1.0 - Hf) * (Ww == 0)
        Rold = R.copy()
        R = R * np.exp(-eatf * V)
        G = p["Y"] * (Rold - R)          # new biomass per site
        if G.max() > 1e-12:
            share = VK / (V + 1e-12)
            if sig_d > 0:
                w = share * np.maximum(1.0 + sig_d * rng.standard_normal(VK.shape), 0.0)
                w = w / (w.sum(0) + 1e-12)
            else:
                w = share
            GK = G * w
            if mu > 0 and K > 1:
                GM = GK * (1 - mu)
                GM[0] += GK[0] * mu * 0.5
                GM[-1] += GK[-1] * mu * 0.5
                GM[:-1] += GK[1:] * (mu * 0.5)
                GM[1:] += GK[:-1] * (mu * 0.5)
                GK = GM
            VK = VK + GK
        # --- death (protection trait-blind: SHARED benefit)
        death = p["d_base"] + p["d0"] * Hf * (1.0 - p["pd"] * C)
        VK = VK * np.exp(-death)
        R = R + p["rho"] * (1.0 - R) + p["Dr"] * lap(R)
        # --- record
        if t % rec == 0:
            V = VK.sum(0)
            vtot = V.sum()
            vm = V.mean()
            ser["t"][ri] = t
            ser["vmean"][ri] = vm
            ser["rmean"][ri] = R.mean()
            ser["hf"][ri] = H.mean()
            ser["cv"][ri] = V.std() / max(vm, 1e-9)
            ser["aggm"][ri] = float((V * C * Hf).sum() / max(vtot, 1e-9))
            ser["fire"][ri] = fires[t]
            binmass = VK.reshape(K, -1).sum(1)
            cmean = float((cbins * binmass).sum() / max(vtot, 1e-9))
            ser["cmean"][ri] = cmean
            ser["csd"][ri] = float(np.sqrt(max((binmass * (cbins - cmean) ** 2).sum()
                                               / max(vtot, 1e-9), 0.0)))
            cbar_s = (cb3 * VK).sum(0) / (V + 1e-12)
            betw = float((V * (cbar_s - cmean) ** 2).sum() / max(vtot, 1e-9))
            within = float((VK * (cb3 - cbar_s) ** 2).sum() / max(vtot, 1e-9))
            ser["rass"][ri] = betw / max(betw + within, 1e-12)
            ser["vcoop"][ri] = float((cb3 * VK).sum() / max(vtot, 1e-9))
            thr = max(0.3, 3.0 * vm)
            labm, ncl = ndimage.label(V > thr)
            ser["ncl"][ri] = ncl
            if ncl > 0:
                masses = ndimage.sum(V, labm, index=range(1, ncl + 1))
                ser["lf"][ri] = float(np.max(masses)) / max(vtot, 1e-9)
            ri += 1
            if not np.isfinite(vtot) or vm > 50:
                return dict(ok=False, why="blowup", t=t,
                            ser={k: v[:ri] for k, v in ser.items()},
                            fires=fires[:t], fire_hist=fire_hist, snaps=snaps, p=p)
            if vm < 5e-4:
                return dict(ok=False, why="extinct", t=t,
                            ser={k: v[:ri] for k, v in ser.items()},
                            fires=fires[:t], fire_hist=fire_hist, snaps=snaps, p=p)
        if t in snap_times:
            V = VK.sum(0)
            snaps[t] = dict(V=V.copy(), R=R.copy(), S=S.copy(),
                            cbar=((cb3 * VK).sum(0) / (V + 1e-12)))
    out = dict(ok=True, why="", t=T, ser={k: v[:ri] for k, v in ser.items()},
               fires=fires, fire_hist=fire_hist, snaps=snaps, p=p)
    if keep_fields:
        out["fields"] = dict(VK=VK, R=R, S=S, A=A)
    return out
