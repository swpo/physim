
"""slime.py v2 — Dictyostelium-inspired lifecycle world (standalone numpy/scipy).

Fields (LxL, periodic):
  R : resource in [0,1], regen rho*(1-R), grazed by active cells
  V : cell density; eats R, starves->hungry (hysteretic on smoothed R),
      hungry cells chemotax up grad(A) (+ small grad(S)), fed cells diffuse fast
  S : fast attractant pulses (excitable relay: hungry cells re-fire, refractory)
  A : slow aggregation pheromone emitted by hungry cells (Keller-Segel layer)
  aggregated (dense) hungry cells: protected from death (pd) and quiescent (pe)

Layers: L1 S relay waves (~tens of ticks) -> L2 aggregation/coarsening
(~hundreds) -> L3 lifecycle oscillator disperse<->aggregate (~thousands).
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
    # resource
    rho=1.0 / 1200, g=0.02, Y=0.6,
    # mortality / protection (starving death slower than aggregation)
    d0=1.5e-3, d_base=1e-4, pd=0.92, pe=0.97, V_c=1.5,
    # hunger hysteresis (sensed on smoothed R)
    R_star=0.15, R_wake=0.55, n_sense=3,
    # fast relay S
    Ds=0.25, ks=0.06, a_s=0.8, S_thr=0.08, T_e=2, T_r=14, p_spont=1.5e-3,
    V_min=0.03,
    # slow pheromone A
    Da=0.15, ka=0.005, a_a=0.01, V_h=1.0,
    # movement
    chi_a=8.0, chi_s=0.5, u_max=0.18, Dv0=0.02, Dv_fed=0.12, V_pack=6.0,
    V0=0.35,
)


def run(params=None, T=30000, seed=0, rec=10, snap_times=(), s_probe=True,
        keep_fields=False):
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
    E = np.zeros((L, L), dtype=np.int32)
    Q = np.zeros((L, L), dtype=np.int32)
    H = np.zeros((L, L), dtype=bool)

    n_rec = T // rec + 1
    ser = dict(t=np.zeros(n_rec), cv=np.zeros(n_rec), lf=np.zeros(n_rec),
               ncl=np.zeros(n_rec), rmean=np.zeros(n_rec), vmean=np.zeros(n_rec),
               hf=np.zeros(n_rec), smean=np.zeros(n_rec), amean=np.zeros(n_rec),
               vmax=np.zeros(n_rec))
    fires = np.zeros(T, dtype=np.int32)
    pr_pts = [(L // 4, L // 4), (L // 4, 3 * L // 4), (3 * L // 4, L // 4), (L // 2, L // 2)]
    s_tr = np.zeros((T, len(pr_pts))) if s_probe else None
    snaps = {}
    clsizes_pool = []
    ri = 0
    Te, Tr = int(p["T_e"]), int(p["T_r"])

    for t in range(T):
        Rs = smooth9(R, int(p["n_sense"]))
        H = np.where(Rs < p["R_star"], True, np.where(Rs > p["R_wake"], False, H))
        Hf = H.astype(float)
        # --- fast relay
        can = H & (Q == 0) & (V > p["V_min"])
        fire = can & ((S > p["S_thr"]) | (rng.random((L, L)) < p["p_spont"] * V))
        E[fire] = Te
        Q[fire] = Te + Tr
        fires[t] = int(fire.sum())
        sat = V / (V + p["V_h"])
        S = S + p["Ds"] * lap(S) - p["ks"] * S + p["a_s"] * sat * (E > 0)
        np.maximum(S, 0.0, out=S)
        E = np.maximum(E - 1, 0)
        Q = np.maximum(Q - 1, 0)
        # --- slow pheromone (emitted by hungry biomass)
        A = A + p["Da"] * lap(A) - p["ka"] * A + p["a_a"] * sat * Hf
        # --- movement
        gax, gay = gradc(A)
        gsx, gsy = gradc(S)
        Vs = smooth9(V, 1)
        pack = np.clip(1.0 - Vs / p["V_pack"], 0.0, 1.0)
        ux = np.clip(p["chi_a"] * gax + p["chi_s"] * gsx, -p["u_max"], p["u_max"]) * Hf * pack
        uy = np.clip(p["chi_a"] * gay + p["chi_s"] * gsy, -p["u_max"], p["u_max"]) * Hf * pack
        Dv = p["Dv0"] + p["Dv_fed"] * (1.0 - Hf)
        V = V + advect(V, ux, uy) + diffuse_var(V, Dv)
        np.maximum(V, 0.0, out=V)
        # --- crowd factor (aggregated = dense smoothed V)
        Vs = smooth9(V, 1)
        C = Vs * Vs / (Vs * Vs + p["V_c"] ** 2)
        # --- eat / grow / die
        eatf = p["g"] * (1.0 - p["pe"] * C * Hf)
        Rold = R.copy()
        R = R * np.exp(-eatf * V)
        eaten = Rold - R
        V = V + p["Y"] * eaten * (1.0 - 0.5 * C * Hf)
        death = p["d_base"] + p["d0"] * Hf * (1.0 - p["pd"] * C)
        V = V * np.exp(-death)
        R = R + p["rho"] * (1.0 - R)
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
        if not np.isfinite(V.sum()) or V.mean() > 50:
            return dict(ok=False, why="blowup", t=t, ser={k: v[:ri] for k, v in ser.items()},
                        fires=fires[:t], s_tr=None if s_tr is None else s_tr[:t],
                        snaps=snaps, clsizes=clsizes_pool, p=p)
        if V.mean() < 1e-3:
            return dict(ok=False, why="extinct", t=t, ser={k: v[:ri] for k, v in ser.items()},
                        fires=fires[:t], s_tr=None if s_tr is None else s_tr[:t],
                        snaps=snaps, clsizes=clsizes_pool, p=p)
    out = dict(ok=True, why="", t=T, ser={k: v[:ri] for k, v in ser.items()},
               fires=fires, s_tr=s_tr, snaps=snaps, clsizes=clsizes_pool, p=p)
    if keep_fields:
        out["fields"] = dict(V=V, R=R, S=S, A=A)
    return out
