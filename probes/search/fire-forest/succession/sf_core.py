
"""succession core: W7 grass-fire backbone + slow tree layer (Staver-Levin).

Fields (LxL torus, dt = 1 tick):
  B grass fuel in [0.01, 1]:
      dB = g_i*(rho + B)*(1 - B - T) - eta*F*B
      grass regrows fast but only into space not held by trees (1-B-T).
  F fire in [0, 1]:  dF = beta*<F>_nn*sig(B)*(1-F) - delta*F, quench F<Fq->0
      sig(flam) = logistic((flam - theta)/w), flam = B + veg_flam*T.
      Default veg_flam=0: flammability carried by GRASS fine fuel only
      (surface fires). Mature forest (T high => B <= 1-T < theta) is a fuel
      break: canopy fire suppression, the Staver-Levin mechanism. Canopy
      megafires excluded BY CHOICE (mesic savanna-forest systems; also keeps
      the L3 clock intact inside grass regions).
  T tree cover in [0, 0.99]:
      dT = gT_i*(rhoT + T + <T>_nn)*(1 - T)  recruitment (seed rain + local
                                              dispersal), slow: gT = R*g
           - mu*T                             senescence (absolute price)
           - kapT*F*trap(T)*T                 FIRE TRAP: saplings killed
      trap(T) = logistic(-(T - Tm)/wm): mortality ~1 below maturity cover Tm,
      ~0 above (big trees fire-resistant). Trees overtop grass (space
      asymmetry in the B equation); grass fights back only via fire.
  lightning: Poisson sparks rate f/site/tick, F = max(F, 0.9*sig).

THEORY COORDINATES (round 2):
  R    = gT/g     succession slowness ratio
  W    = mu/gT    senescence/growth balance -> forest-branch T*
  Tm   = fire-trap maturity threshold (vs emergent fireproof cover ~1-theta)
  kapT = trap severity (fire kill rate on immature trees)
  rhoT = tree seed rain
  gT   = R*g is the G3 "tree growth price" (mu held ABSOLUTE in G3 sweeps)
Inherited W7 (certified round 1): theta=.78 Lam=9 M=2 D=8 gsig=.35 rho=.03
  g=2e-3, delta=.2, w=.05, Fq=.02.

Layers: L1 fire front (tau1 = hot residence) -> L2 fire events (tau2) ->
L3 fire-return clock in savanna (tau3 = grass-region FRI / phi_grass clock)
-> L4 biome field (tau4 from relaxation/switch fit on meanT).
"""
import numpy as np, time, sys
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
from hier_metrics import *


def nominal_Tg(g, theta, Bfloor=0.01):
    return np.log((theta / (1 - theta)) * ((1 - Bfloor) / Bfloor)) / g


def make_init(L, rng, init, patch_frac, Tinit_patch):
    B = rng.uniform(0.05, 0.35, (L, L))
    if init == "savanna":
        T = np.full((L, L), 0.02)
    elif isinstance(init, float) or (isinstance(init, str) and init.startswith("uni")):
        val = init if isinstance(init, float) else float(init[3:])
        T = np.full((L, L), val)
    elif init == "half":
        T = np.full((L, L), 0.02)
        T[:, :L // 2] = 0.85
        B[:, :L // 2] = 0.08
    elif init == "forest":
        T = np.full((L, L), 0.85); B[:] = 0.08
    elif init == "mixed":
        T = np.full((L, L), 0.02)
        area_target = patch_frac * L * L
        placed = 0.0
        yy, xx = np.mgrid[0:L, 0:L]
        while placed < area_target:
            cx, cy = rng.integers(0, L, 2)
            r = rng.uniform(3.0, 6.0)
            dx = np.minimum(np.abs(xx - cx), L - np.abs(xx - cx))
            dy = np.minimum(np.abs(yy - cy), L - np.abs(yy - cy))
            m = dx * dx + dy * dy <= r * r
            placed += float((m & (T < Tinit_patch)).sum())
            T[m] = Tinit_patch
    else:
        raise ValueError(init)
    return B, T


def run(L=64, T_ticks=60000, g=2e-3, Lam=9.0, theta=0.78, M=2.0, D=8.0,
        gsig=0.35, rho=0.03, gT=6e-5, mu=3e-5, Tm=0.45, wm=0.08, kapT=1.5,
        rhoT=0.03, delta=0.2, w=0.05, Bfloor=0.01, Fq=0.02, seed=0, rec=5,
        init="mixed", patch_frac=0.30, Tinit_patch=0.62,
        snap_times=(), f_abs=None, veg_flam=0.0, cT=0.5, record_maps=True):
    rng = np.random.default_rng(seed)
    beta = 4.0 * delta * M
    eta = delta * D
    Tg = nominal_Tg(g, theta, Bfloor)
    f = f_abs if f_abs is not None else Lam / (L * L * Tg)
    umap = rng.uniform(-gsig, gsig, (L, L)) if gsig > 0 else np.zeros((L, L))
    gmap = g * np.exp(umap); gTmap = gT * np.exp(umap)
    B, T = make_init(L, rng, init, patch_frac, Tinit_patch)
    F = np.zeros((L, L))
    hot_prev = np.zeros((L, L), bool)
    nrec = T_ticks // rec
    meanB = np.zeros(nrec); phi = np.zeros(nrec)
    meanT = np.zeros(nrec); fracForest = np.zeros(nrec)
    phi_grass = np.zeros(nrec)
    area = np.zeros(nrec, np.int32); ign = np.zeros(nrec, np.int32)
    # per-cell fire-return bookkeeping, split by biome at ignition time
    last_burn = np.full((L, L), -1.0)
    fri_grass = []; fri_forest = []
    burn_count = np.zeros((L, L), np.int32)
    hot_ticks = 0; ign_total = 0
    snaps = {}; prof_list = []
    t0 = time.time()
    inv_LL = 1.0 / (L * L)
    for t in range(T_ticks):
        Fn = 0.25 * (np.roll(F, 1, 0) + np.roll(F, -1, 0)
                     + np.roll(F, 1, 1) + np.roll(F, -1, 1))
        flam = B + veg_flam * T
        sig = 1.0 / (1.0 + np.exp(-(flam - theta) / w))
        F += beta * Fn * sig * (1.0 - F) - delta * F
        nsp = rng.poisson(f * L * L)
        if nsp:
            xs = rng.integers(0, L, nsp); ys = rng.integers(0, L, nsp)
            F[xs, ys] = np.maximum(F[xs, ys], 0.9 * sig[xs, ys])
        F[F < Fq] = 0.0
        np.clip(F, None, 1.0, out=F)
        # tree layer (slow)
        Tn = 0.25 * (np.roll(T, 1, 0) + np.roll(T, -1, 0)
                     + np.roll(T, 1, 1) + np.roll(T, -1, 1))
        trap = 1.0 / (1.0 + np.exp((T - Tm) / wm))
        T += gTmap * (rhoT + 0.5 * (T + Tn)) * (1.0 - T) - mu * T \
             - kapT * F * trap * T
        np.clip(T, 0.0, 0.99, out=T)
        # grass layer (canopy asymmetry: grass persists under open canopy)
        space = 1.0 - B - cT * T
        B += gmap * (rho + B) * space - eta * F * B
        np.clip(B, Bfloor, 1.0, out=B)
        hot = F > 0.1
        new = hot & ~hot_prev
        if new.any():
            idx = np.where(new)
            prev = last_burn[idx]
            fresh = prev >= 0
            if fresh.any():
                iv = t - prev[fresh]
                tf = T[idx][fresh]
                for v, tv in zip(iv, tf):
                    (fri_forest if tv > 0.5 else fri_grass).append(float(v))
            last_burn[idx] = t
            burn_count[idx] += 1
        r = t // rec
        meanB[r] += B.mean(); phi[r] += (B > theta).sum() * inv_LL
        meanT[r] += T.mean(); fracForest[r] += (T > 0.5).sum() * inv_LL
        gm = T < 0.3
        ng = int(gm.sum())
        phi_grass[r] += ((B > theta) & gm).sum() / max(ng, 1)
        a = int(hot.sum())
        if a > area[r]: area[r] = a
        ni = int(new.sum())
        ign[r] += ni
        hot_ticks += a; ign_total += ni
        hot_prev = hot
        if t in snap_times:
            snaps[t] = (B.copy(), F.copy(), T.copy())
        if t % 500 == 0:
            prof_list.append(T.mean(0).copy())
    meanB /= rec; phi /= rec; meanT /= rec; fracForest /= rec
    phi_grass /= rec
    return dict(meanB=meanB, phi=phi, phi_grass=phi_grass, meanT=meanT,
                fracForest=fracForest, prof=np.array(prof_list),
                area=area, ign=ign, rec=rec, hot_ticks=hot_ticks,
                ign_total=ign_total, snaps=snaps, fri_grass=fri_grass,
                fri_forest=fri_forest, burn_count=burn_count,
                T_final=T.copy(), B_final=B.copy(),
                runtime=time.time() - t0, f=float(f), Tg=float(Tg), L=L,
                T_ticks=T_ticks,
                params=dict(L=L, T_ticks=T_ticks, g=g, Lam=Lam, theta=theta,
                            M=M, D=D, gsig=gsig, rho=rho, gT=gT, mu=mu,
                            Tm=Tm, wm=wm, kapT=kapT, rhoT=rhoT, cT=cT,
                            delta=delta, w=w, seed=seed, init=init,
                            patch_frac=patch_frac, Tinit_patch=Tinit_patch,
                            veg_flam=veg_flam))
