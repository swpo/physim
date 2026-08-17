
"""slime.py v4 — Dictyostelium-inspired lifecycle world (standalone numpy/scipy).

Fields (LxL, periodic):
  R : resource in [0,1], regen rho*(1-R), grazed by FED cells only
  V : cell density. Hungry cells (hysteretic threshold on smoothed R, with
      per-cell commitment timers against flicker) stop feeding (development),
      chemotax up grad(A), and relay S pulses. Fed cells diffuse (foraging)
      and eat. Dense hungry aggregates are protected (low death: slug/spore).
  S : fast attractant (excitable relay with refractory T_r) -> L1 waves.
  A : slow pheromone = leaky integral of relay firing -> marks wave sources;
      chemotaxis target -> L2 aggregation onto pacemaker centers.

Commitment timers (micro-physiology, both << lifecycle period):
  T_dev  : once starving, committed to development for >= T_dev ticks
  T_wake : once fed/germinated, committed to foraging for >= T_wake ticks

Hierarchy target: L1 relay waves (~20-40 ticks) -> L2 aggregation/coarsening
(~200-500) -> L3 lifecycle feast<->famine oscillator (~2000-6000, set by
resource regen 1/rho). Top variable: aggregated-dormant fraction / cv(V).
"""
import numpy as np
from scipy import ndimage


def lap(f):
    return (np.roll(f, 1, 0) + np.roll(f, -1, 0) + np.roll(f, 1, 1) + np.roll(f, -1, 1) - 4.0 * f)


def smooth9(f, n=1):
    for _ in range(n):
        f = (f + np.roll(f, 1, 0) + np.roll(f, -1, 0) + np.roll(f, 1, 1) + np.roll(f, -1, 1)
             + np.roll(np.roll(f, 1, 0), 1, 1) + np.roll(np.roll(f, 1, 0), -1, 1)
             + np.roll(np.roll(f, -1, 0), 1, 1) + np.roll(np.roll(f, -1, 0), -1, 1)) / 9.0
    return f


def gradc(f):
    return (0.5 * (np.roll(f, -1, 0) - np.roll(f, 1, 0)),
            0.5 * (np.roll(f, -1, 1) - np.roll(f, 1, 1)))


def advect(V, ux, uy):
    """Conservative donor-cell upwind advection with per-donor outflow limiter."""
    uxf = 0.5 * (ux + np.roll(ux, -1, 0))
    uyf = 0.5 * (uy + np.roll(uy, -1, 1))
    Fx = np.where(uxf > 0, uxf * V, uxf * np.roll(V, -1, 0))
    Fy = np.where(uyf > 0, uyf * V, uyf * np.roll(V, -1, 1))
    out = (np.maximum(Fx, 0) - np.minimum(np.roll(Fx, 1, 0), 0)
           + np.maximum(Fy, 0) - np.minimum(np.roll(Fy, 1, 1), 0))
    lam = np.minimum(1.0, 0.9 * V / (out + 1e-12))
    Fx = Fx * np.where(uxf > 0, lam, np.roll(lam, -1, 0))
    Fy = Fy * np.where(uyf > 0, lam, np.roll(lam, -1, 1))
    return -(Fx - np.roll(Fx, 1, 0)) - (Fy - np.roll(Fy, 1, 1))


def diffuse_var(V, D):
    Dxf = 0.5 * (D + np.roll(D, -1, 0))
    Dyf = 0.5 * (D + np.roll(D, -1, 1))
    Fx = Dxf * (np.roll(V, -1, 0) - V)
    Fy = Dyf * (np.roll(V, -1, 1) - V)
    return (Fx - np.roll(Fx, 1, 0)) + (Fy - np.roll(Fy, 1, 1))


DEFAULTS = dict(
    L=64,
    # resource: grazing crash (g*V >> rho) vs slow regen; Dr mixes R globally
    rho=1.0 / 4000, g=0.03, Y=0.6, Dr=0.2,
    # mortality: famine kills loners fast; dense aggregates nearly immortal
    d0=2e-3, d_base=1e-4, pd=0.95, V_c=1.5,
    # hunger switch: famine len ~ (1/rho) ln((1-R_star)/(1-R_wake))
    R_star=0.12, R_wake=0.55, n_sense=1, T_dev=400, T_wake=400,
    # fast relay S (2 diffusion substeps)
    Ds=0.3, ks=0.10, a_s=1.2, S_thr=0.06, T_e=2, T_r=14, p_spont=1.0e-3,
    V_min=0.03, S_sub=2, C_spore=2.0,
    # slow pheromone A = leaky integral of firing (aggregation memory ~1/ka)
    Da=0.12, ka=0.004, a_a=0.05, V_h=1.0,
    # movement: hungry chemotax up A; germinating disperse down A; fed graze
    chi_a=12.0, chi_d=12.0, u_max=0.18, Dv0=0.02, Dv_fed=0.05, Dv_germ=0.22,
    V_pack=8.0, V0=0.35,
    # famine-onset wave recruitment of marginal fed cells (synchronizer)
    S_dev=0.25, R_join=0.35,
)

def run(params=None, T=30000, seed=0, rec=10, snap_times=(), s_probe=False,
        keep_fields=False, snap_every=None):
    p = dict(DEFAULTS)
    if params:
        p.update(params)
    L = int(p["L"])
    rng = np.random.default_rng(seed)
    R = np.ones((L, L))
    V = p["V0"] * (1.0 + 0.1 * rng.standard_normal((L, L)))
    V = np.maximum(V, 0.01)
    S = np.zeros((L, L))
    A = np.zeros((L, L))
    E = np.zeros((L, L), dtype=np.int32)   # emission timer
    Q = np.zeros((L, L), dtype=np.int32)   # relay refractory
    H = np.zeros((L, L), dtype=bool)       # hungry/developing
    Wd = np.zeros((L, L), dtype=np.int32)  # dev commitment countdown
    Ww = np.zeros((L, L), dtype=np.int32)  # wake commitment countdown

    n_rec = T // rec + 1
    keys = ("t", "cv", "lf", "ncl", "rmean", "vmean", "hf", "smean", "amean",
            "vmax", "aggm", "fire")
    ser = {k: np.zeros(n_rec) for k in keys}
    fires = np.zeros(T, dtype=np.int32)
    pr_pts = [(L // 4, L // 4), (L // 2, L // 2), (3 * L // 4, L // 4)]
    s_tr = np.zeros((T, len(pr_pts)), dtype=np.float32) if s_probe else None
    snaps = {}
    movie = []
    clsizes_pool = []
    fire_hist = np.zeros(1001, dtype=np.int64)   # per-cell refire intervals (L1)
    lastF = np.full((L, L), -1, dtype=np.int64)
    ri = 0
    Te, Tr = int(p["T_e"]), int(p["T_r"])
    nsub = int(p["S_sub"])

    for t in range(T):
        # --- hunger switch with hysteresis + commitment
        # NEW: relay-wave recruitment — strong S recruits marginally-fed cells
        # into development (the wave synchronizes the lifecycle globally).
        Rs = smooth9(R, int(p["n_sense"]))
        starving = (Rs < p["R_star"]) | ((S > p["S_dev"]) & (Rs < p["R_join"]))
        want_h = np.where(starving, True,
                          np.where(Rs > p["R_wake"], False, H))
        newly_h = want_h & ~H & (Ww == 0)
        newly_f = ~want_h & H & (Wd == 0)
        H = H.copy()
        H[newly_h] = True
        H[newly_f] = False
        Wd[newly_h] = int(p["T_dev"])
        Ww[newly_f] = int(p["T_wake"])
        Wd = np.maximum(Wd - 1, 0)
        Ww = np.maximum(Ww - 1, 0)
        Hf = H.astype(float)
        # --- crowding (used for spore quiescence, protection, eating)
        Vs = smooth9(V, 1)
        C = Vs * Vs / (Vs * Vs + p["V_c"] ** 2)
        # --- fast relay (spore quiescence: dense aggregates go silent)
        can = H & (Q == 0) & (V > p["V_min"]) & (C < p["C_spore"])
        fire = can & ((S > p["S_thr"]) | (rng.random((L, L)) < p["p_spont"] * V))
        E[fire] = Te
        Q[fire] = Te + Tr
        fires[t] = int(fire.sum())
        seen = fire & (lastF >= 0)
        if seen.any():
            iv = np.clip(t - lastF[seen], 0, 1000)
            fire_hist += np.bincount(iv, minlength=1001)
        lastF[fire] = t
        sat = V / (V + p["V_h"])
        firing = (E > 0)
        for _ in range(nsub):
            S = S + (p["Ds"] / nsub) * lap(S)
        S = S - p["ks"] * S + p["a_s"] * sat * firing
        np.maximum(S, 0.0, out=S)
        E = np.maximum(E - 1, 0)
        Q = np.maximum(Q - 1, 0)
        # --- slow pheromone: leaky integral of firing
        A = A + p["Da"] * lap(A) - p["ka"] * A + p["a_a"] * sat * firing
        # --- movement in three modes:
        # hungry: chemotax up grad(A) (aggregate);
        # germinating (fed, Ww>0): disperse — fast diffusion + drift DOWN
        #   grad(A) (away from the fruiting center), no feeding yet;
        # fed grazer (Ww==0): slow foraging diffusion.
        gax, gay = gradc(A)
        pack = np.clip(1.0 - Vs / p["V_pack"], 0.0, 1.0)
        Ff = 1.0 - Hf
        Gf = Ff * (Ww > 0)   # germinating dispersers
        ux = (np.clip(p["chi_a"] * gax, -p["u_max"], p["u_max"]) * Hf * pack
              - np.clip(p["chi_d"] * gax, -p["u_max"], p["u_max"]) * Gf)
        uy = (np.clip(p["chi_a"] * gay, -p["u_max"], p["u_max"]) * Hf * pack
              - np.clip(p["chi_d"] * gay, -p["u_max"], p["u_max"]) * Gf)
        Dv = p["Dv0"] + p["Dv_fed"] * (Ff - Gf) + p["Dv_germ"] * Gf
        np.minimum(Dv, 0.24, out=Dv)
        # sequential updates keep V >= 0 without clipping (mass-conserving):
        # advect outflow <= 0.9 V; diffusion outflow <= 4*0.24 V < V.
        V = V + advect(V, ux, uy)
        V = V + diffuse_var(V, Dv)
        np.maximum(V, 0.0, out=V)  # numerical dust only
        # --- crowd factor (protection when dense; post-move density)
        Vs = smooth9(V, 1)
        C = Vs * Vs / (Vs * Vs + p["V_c"] ** 2)
        # --- eat / grow / die (developing cells and germinating dispersers
        # do not feed; only settled grazers eat)
        eatf = p["g"] * (1.0 - Hf) * (Ww == 0)
        Rold = R.copy()
        R = R * np.exp(-eatf * V)
        eaten = Rold - R
        V = V + p["Y"] * eaten
        death = p["d_base"] + p["d0"] * Hf * (1.0 - p["pd"] * C)
        V = V * np.exp(-death)
        R = R + p["rho"] * (1.0 - R) + p["Dr"] * lap(R)
        # --- record
        if s_probe:
            for j, (i0, j0) in enumerate(pr_pts):
                s_tr[t, j] = S[i0, j0]
        if t % rec == 0:
            vm = V.mean()
            ser["t"][ri] = t
            ser["vmean"][ri] = vm
            ser["vmax"][ri] = V.max()
            ser["rmean"][ri] = R.mean()
            ser["hf"][ri] = H.mean()
            ser["smean"][ri] = S.mean()
            ser["amean"][ri] = A.mean()
            ser["cv"][ri] = V.std() / max(vm, 1e-9)
            ser["aggm"][ri] = float((V * C * Hf).sum() / max(V.sum(), 1e-9))
            ser["fire"][ri] = fires[t]
            thr = max(0.3, 3.0 * vm)
            labm, ncl = ndimage.label(V > thr)
            ser["ncl"][ri] = ncl
            if ncl > 0:
                masses = ndimage.sum(V, labm, index=range(1, ncl + 1))
                ser["lf"][ri] = float(np.max(masses)) / max(V.sum(), 1e-9)
                if t % (rec * 5) == 0:
                    clsizes_pool.extend([float(m) for m in np.atleast_1d(masses)])
            else:
                ser["lf"][ri] = 0.0
            ri += 1
        if t in snap_times:
            snaps[t] = dict(V=V.copy(), R=R.copy(), S=S.copy(), A=A.copy())
        if snap_every and t % snap_every == 0:
            movie.append((t, V.astype(np.float32).copy(), S.astype(np.float32).copy()))
        if not np.isfinite(V.sum()) or V.mean() > 50:
            return dict(ok=False, why="blowup", t=t, ser={k: v[:ri] for k, v in ser.items()},
                        fires=fires[:t], s_tr=None if s_tr is None else s_tr[:t],
                        snaps=snaps, movie=movie, clsizes=clsizes_pool,
                        fire_hist=fire_hist, p=p)
        if V.mean() < 1e-3:
            return dict(ok=False, why="extinct", t=t, ser={k: v[:ri] for k, v in ser.items()},
                        fires=fires[:t], s_tr=None if s_tr is None else s_tr[:t],
                        snaps=snaps, movie=movie, clsizes=clsizes_pool,
                        fire_hist=fire_hist, p=p)
    out = dict(ok=True, why="", t=T, ser={k: v[:ri] for k, v in ser.items()},
               fires=fires, s_tr=s_tr, snaps=snaps, movie=movie, clsizes=clsizes_pool,
               fire_hist=fire_hist, p=p)
    if keep_fields:
        out["fields"] = dict(V=V, R=R, S=S, A=A)
    return out
