"""refs_closure -- public scales and default-world OES denominators from existing data (no simulation).

Data: vw1/fresh/closure/results/sim_{A,B}.npz (the port world at default theta, wind-free, flow noise
0.5): 36 trajectories x 301 ticks of level 1 (coarse 192 + objects 144), and at 144 test states
(4 ticks x 36) 6 replicate futures (the base trajectory + 5 fresh-noise branches) for h = 1..32.

Scales (public, from this default-theta ensemble; for a real suite they must come from the prior
predictive): level 1 = per-coordinate SD of the coarse view (coordinates with SD ~ 0 get scale 1),
level 2 = SD of (count, tracked mass, mean speed).
Denominators per horizon h: D_h = mean over states of [ES_fair(clim pool, reps) - ES_loo(reps)], with
the climatology pool = 256 snapshots drawn from all trajectories and ticks (seed 0), the fair energy
score of vw.scoring (RMS norm on scaled coordinates).
Output: results/refs_closure.json, results/scales.npz.
"""
import json

import numpy as np

import gworld as GW
from vw.scoring import energy_fair, energy_loo

CL = "/home/user/evalwork/vecworld/vw1/fresh/closure/results"
TEST = [40, 100, 160, 220]
HS = [1, 2, 4, 8, 16, 32]


def load():
    Ys, Bs = [], []
    for t in "AB":
        z = np.load(f"{CL}/sim_{t}.npz")
        Ys.append(z["Y"].astype(float))
        Bs.append(z["B"].astype(float))
    return np.concatenate(Ys), np.concatenate(Bs)


def main():
    Y, B = load()                                   # (36, 301, 336), (36, 4, 5, 32, 336)
    J = Y.shape[0]
    yc = Y[..., :GW.NC].reshape(-1, GW.NC)
    sd1 = yc.std(0)
    eff = sd1 > 1e-6 * sd1.max()
    sc1 = np.where(eff, sd1, 1.0)
    pop = GW.population(Y)                          # (36, 301, 3)
    sc2 = pop.reshape(-1, 3).std(0)
    np.savez("results/scales.npz", level1=sc1, level2=sc2, eff1=eff)
    rng = np.random.default_rng(0)
    pick = rng.integers(0, Y.shape[0] * Y.shape[1], 256)
    pool = Y.reshape(-1, Y.shape[-1])[pick]
    out = {"source": [f"{CL}/sim_A.npz", f"{CL}/sim_B.npz"], "n_states": J * len(TEST), "R": 6, "clim_pool": 256,
           "scales": {"level2_names": ["count", "tracked_mass", "mean_speed"], "level2_sd": sc2.tolist(),
                      "level1_eff_coords": int(eff.sum())},
           "level2_means": pop.reshape(-1, 3).mean(0).tolist(), "horizons": HS, "level1": {}, "level2": {}}
    for h in HS:
        reps = np.stack([np.concatenate([Y[:, t + h][:, None], B[:, i, :, h - 1]], 1) for i, t in enumerate(TEST)], 1)
        reps = reps.reshape(-1, 6, Y.shape[-1])                                  # (144, 6, 336)
        for lev, f, sc, pl in ((1, GW.coarse, sc1, GW.coarse(pool)), (2, GW.population, sc2, GW.population(pool))):
            Yr = f(reps)
            o = energy_loo(Yr, sc)
            c = energy_fair(np.broadcast_to(pl[None], (Yr.shape[0],) + pl.shape), Yr, sc)
            d = c - o
            out[f"level{lev}"][str(h)] = {"S_oracle": float(o.mean()), "S_clim": float(c.mean()), "D": float(d.mean()),
                                          "D_se": float(d.std(ddof=1) / np.sqrt(len(d)))}
        print(h, out["level1"][str(h)], out["level2"][str(h)], flush=True)
    json.dump(out, open("results/refs_closure.json", "w"), indent=1)


if __name__ == "__main__":
    main()
