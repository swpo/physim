"""viability -- does background wind noise keep the gliders world alive?

usage: python -B viability.py sim     -> results/viability.npz (float32 level-1 records)
       python -B viability.py stats   -> results/viability.json

Ensemble: J = 3 members per sigma_w in SIGMAS (sigma_w = 0 is the port's world, bitwise), each from the
declared initial law (init_patches) + the 50-tick burn-in, both under the member's wind noise, then
T = 250 free ticks (300 ticks in all), no input. All sigma_w share the member keys (same initial
patches, same flow-noise draws; eta is the same draw scaled by sigma_w): a paired comparison.
Statistics per trajectory (definitions of integrate/analyze.objects_stats): objects present per tick,
speed of continuing slots (present, no event), mass and rg of present slots, fusions / fissions /
births / deaths per 100 ticks (tracker globals), track life (ticks from first to last presence of a
uid; tracks cut by the window counted as they are), coarse-level SD relative to the closure study's.
Native band: the same statistics on the 36 noise-free closure trajectories (sim_A/sim_B, ticks 0..250);
for each statistic the 2.5-97.5% range of means of 3 trajectories drawn from them (10^4 resamples).
"""
import json
import sys
import time

import jax.numpy as jnp
import numpy as np

import wind as WD
from vw.world import make_key, member_keys

SIGMAS = [0.0, 0.05, 0.1, 0.2, 0.4, 0.8]
J, T = 3, 250
NPZ = f"{WD.RES}/viability.npz"


def simulate():
    t0 = time.time()
    WW = WD.WindWorld()
    init_burn, run = WW.make_init(), WW.make_run()
    kb = member_keys(make_key(9001, 0), J)
    B = J * len(SIGMAS)
    keys = kb[jnp.asarray(np.tile(np.arange(J), len(SIGMAS)))]
    sig = jnp.asarray(np.repeat(SIGMAS, J))
    A, m = init_burn(WW.params, keys, sig)
    A.block_until_ready()
    t1 = time.time()
    print("init + burn-in", round(t1 - t0, 1), "s", flush=True)
    import jax
    kd = jax.vmap(lambda k: jax.random.fold_in(k, WD._ST_DYN))(keys)
    mass0 = np.asarray(A).sum((2, 3))
    y, tab, glob, A1, m1 = run(WW.params, A, m, kd, jnp.zeros((B,), jnp.int64), jnp.zeros((B, T, WD.KMAX), int),
                               jnp.zeros((B, T, WD.KMAX)), jnp.zeros((B, T, WD.NW)), sig)
    A1 = np.asarray(A1)
    print("run", round(time.time() - t1, 1), "s", flush=True)
    np.savez_compressed(NPZ, y=np.asarray(y, np.float32), tab=np.asarray(tab, np.float32),
                        glob=np.asarray(glob, np.float32), sigmas=np.repeat(SIGMAS, J), member=np.tile(np.arange(J), len(SIGMAS)),
                        mass0=mass0, mass1=A1.sum((2, 3)), Amax=A1.sum(1).max((1, 2)), Amin=A1.min((1, 2, 3)),
                        seconds=np.array([t1 - t0, time.time() - t1]))


def traj_stats(Yo, tab, gl):
    """Yo (T+1, 144) objects readout; tab (T+1, K, 5) slot extras (cy, cx, age, event, uid); gl (T+1, 5)."""
    K = WD.K_SLOTS
    S = Yo.reshape(len(Yo), K, WD.NF)
    pres = S[:, :, 0] > 0.5
    ev, uid = tab[:, :, 3], tab[:, :, 4]
    cont = pres & (ev == 0)
    sp = np.hypot(S[:, :, 10], S[:, :, 11])[cont]
    nT = len(Yo) - 1
    d = (gl[-1, 1:] - gl[0, 1:]) * 100.0 / nT
    life = {}
    for t in range(len(Yo)):
        for s in np.flatnonzero(pres[t]):
            u = int(uid[t, s])
            f, l = life.get(u, (t, t))
            life[u] = (min(f, t), t)
    L = np.array([l - f + 1 for f, l in life.values()])
    return {"objects_mean": float(pres.sum(1).mean()), "speed_median": float(np.median(sp)),
            "speed_p90": float(np.percentile(sp, 90)), "mass_median": float(np.median(S[:, :, 1][pres])),
            "rg_median": float(np.median(S[:, :, 7][pres])), "births_per100": float(d[0]), "deaths_per100": float(d[1]),
            "fusions_per100": float(d[2]), "fissions_per100": float(d[3]), "track_life_median": float(np.median(L)),
            "tracks_ge50_frac": float((L >= 50).mean()), "n_tracks": int(len(L))}


def stats():
    z = np.load(NPZ)
    sd = WD.closure_sd()
    out = {"sigmas": SIGMAS, "members": J, "ticks_after_burn_in": T, "burn_in_ticks": WD.BURN_TICKS,
           "member_ticks": int(len(z["sigmas"]) * (T + WD.BURN_TICKS)), "sim_seconds": z["seconds"].tolist(),
           "per_sigma": {}}
    # native band from the closure trajectories (noise-free world), same window length
    nat = []
    for tg in "AB":
        c = np.load(f"/home/user/evalwork/vecworld/vw1/fresh/closure/results/sim_{tg}.npz")
        Y, TAB = c["Y"].astype(float), c["TAB"].astype(float)
        for j in range(len(Y)):
            tb = TAB[j, :T + 1, :WD.K_SLOTS * 5].reshape(T + 1, WD.K_SLOTS, 5)
            nat.append(traj_stats(Y[j, :T + 1, WD.NC:], tb, TAB[j, :T + 1, WD.K_SLOTS * 5:]))
    keys = list(nat[0].keys())
    rng = np.random.default_rng(1)
    band = {}
    for k in keys:
        v = np.array([s[k] for s in nat])
        means = v[rng.integers(0, len(v), (10000, J))].mean(1)
        band[k] = {"closure_mean_36": float(v.mean()), "band_3traj_2.5": float(np.percentile(means, 2.5)),
                   "band_3traj_97.5": float(np.percentile(means, 97.5))}
    out["native_band_from_closure_runs"] = band
    for sw in SIGMAS:
        idx = np.flatnonzero(z["sigmas"] == sw)
        rows = []
        for b in idx:
            tb = z["tab"][b][:, :, WD.NF:].astype(float)
            rows.append(traj_stats(z["y"][b][:, WD.NC:].astype(float), tb, z["glob"][b].astype(float)))
        r = {k: float(np.mean([x[k] for x in rows])) for k in keys}
        r["in_native_band"] = {k: bool(band[k]["band_3traj_2.5"] <= r[k] <= band[k]["band_3traj_97.5"]) for k in keys
                               if k != "n_tracks"}
        r["per_member"] = rows
        yc = z["y"][idx][:, 1:, :WD.NC].reshape(-1, WD.NC).astype(float)
        s_c, eff = sd["coarse"]
        r["coarse_sd_ratio_mean"] = float((yc.std(0)[eff] / s_c[eff]).mean())
        yo = z["y"][idx][:, 1:, WD.NC:].reshape(-1, WD.NO).astype(float)
        s_o, eff_o = sd["objects"]
        r["objects_sd_ratio_mean"] = float((yo.std(0)[eff_o] / s_o[eff_o]).mean())
        r["mass_drift_max_abs"] = float(np.abs(z["mass1"][idx] - z["mass0"][idx]).max())
        r["A_sum_max_end"] = float(z["Amax"][idx].max())
        r["A_min_end"] = float(z["Amin"][idx].min())
        r["wind_random_walk_px_per_tick"] = float(sw * 1.9451893575223667)
        out["per_sigma"][str(sw)] = r
        print(sw, {k: round(r[k], 3) for k in keys}, "coarse sd ratio", round(r["coarse_sd_ratio_mean"], 3),
              "drift", r["mass_drift_max_abs"], flush=True)
    json.dump(out, open(f"{WD.RES}/viability.json", "w"), indent=1)


if __name__ == "__main__":
    if sys.argv[1] == "sim":
        simulate()
    stats()
