"""explore -- field ranges, cell sizes and threshold sensitivity, to fix the channel field and the tracker.

    python explore.py [n_seeds] [T_end]         (defaults 2 seeds, 6000 time units; dt 0.5, 128^2)

Free runs of membrane_jax (channel noise off and on at the default sigma_a) from the JAX initial law.
Every 100 time units: ranges of S, K, L, phi (fractions near their clips); phi > thr components of the
sigma-1 blurred phi (the tracker's segmentation) for thr in 0.3, 0.4, 0.5, 0.6, 0.7: count and mean mass,
and the component mass distribution at 0.5 (to pick m_min). Uses t >= 1000 (after formation) for the pooled
statistics. Writes results/explore.json and results/threshold.json.
"""
import json
import os
import sys

import _paths
import jax
import jax.numpy as jnp
import numpy as np
from scipy import ndimage

import vw
import membrane_jax as MJ

NS = int(sys.argv[1]) if len(sys.argv) > 1 else 2
T_END = float(sys.argv[2]) if len(sys.argv) > 2 else 6000.0
THR = (0.3, 0.4, 0.5, 0.6, 0.7)
H = 128


def comps(phi, thr):
    """Masses (sum phi) of the 8-connected components of blur(phi, 1) > thr on the torus."""
    B = ndimage.gaussian_filter(phi, 1.0, mode="wrap") > thr
    lab, n = ndimage.label(np.tile(B, (3, 3)), structure=np.ones((3, 3)))
    c = lab[H:2 * H, H:2 * H]
    ids = np.unique(c[c > 0])
    return np.array([phi[c == i].sum() for i in ids]) if ids.size else np.zeros(0)


def main():
    out = {"ranges": {}, "thresholds": {}, "mass_hist": {}}
    rows = {s: {thr: [] for thr in THR} for s in ("off", "on")}
    rng_stats = {s: [] for s in ("off", "on")}
    for arm, sa in (("off", 0.0), ("on", MJ.Config.sigma_a)):
        cfg = MJ.Config(sigma_a=sa)
        lev = MJ.make_level(cfg)
        q = lev.params
        nt = int(round(100 / cfg.tick_time))
        run = jax.jit(lambda x, t0, key: jax.lax.fori_loop(
            0, nt, lambda i, xx: lev.step(q, xx, vw.Noise(key, t0 + i), jnp.zeros(cfg.m)), x))
        for seed in range(NS):
            key = vw.make_key(5, seed)
            x = lev.init(q, jax.random.fold_in(key, 1))
            t, tick = 0.0, 0
            while t <= T_END + 1e-9:
                xn = {f: np.asarray(v) for f, v in x.items()}
                if t >= 1000:
                    rng_stats[arm].append([xn["S"].min(), xn["S"].max(), (xn["phi"] < 1e-3).mean(), (xn["phi"] > 1 - 1e-3).mean(),
                                           (xn["K"] < 1e-6).mean(), (xn["L"] < 1e-6).mean(), xn["K"].max(), xn["L"].max()])
                    for thr in THR:
                        m = comps(xn["phi"], thr)
                        rows[arm][thr].append(m)
                x = run(x, tick, key)
                tick += nt
                t += 100.0
            print(arm, seed, "done", flush=True)
        R = np.array(rng_stats[arm])
        out["ranges"][arm] = {"S_min": float(R[:, 0].min()), "S_max": float(R[:, 1].max()),
                              "phi_below_1e-3_frac_mean": float(R[:, 2].mean()), "phi_above_1-1e-3_frac_mean": float(R[:, 3].mean()),
                              "K_below_1e-6_frac_mean": float(R[:, 4].mean()), "L_below_1e-6_frac_mean": float(R[:, 5].mean()),
                              "K_max": float(R[:, 6].max()), "L_max": float(R[:, 7].max()), "n_snapshots": int(len(R))}
        th = {}
        for thr in THR:
            ms = rows[arm][thr]
            allm = np.concatenate(ms)
            th[str(thr)] = {"count_mean_all": float(np.mean([len(m) for m in ms])),
                            "count_mean_mass_ge12": float(np.mean([(m >= 12).sum() for m in ms])),
                            "mean_mass_ge12": float(allm[allm >= 12].mean()),
                            "frac_components_below_12": float((allm < 12).mean())}
        out["thresholds"][arm] = th
        m5 = np.concatenate(rows[arm][0.5])
        edges = [0, 2, 4, 8, 12, 16, 24, 32, 48, 64, 96, 128, 192, 256, 384, 512, 768, 1024, 2048, 4096]
        out["mass_hist"][arm] = {"edges": edges, "counts": np.histogram(m5, edges)[0].tolist(),
                                 "quantiles": {str(p): float(np.quantile(m5, p)) for p in (0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.99)}}
    out["config"] = {"dt": MJ.Config.dt, "tick_time": MJ.Config().tick_time, "sigma_a_on": MJ.Config.sigma_a,
                     "n_seeds": NS, "T_end": T_END, "window": "t >= 1000, every 100 t", "blur_sigma": 1.0}
    json.dump(out, open(os.path.join(_paths.RESULTS, "explore.json"), "w"), indent=1)
    json.dump(out["thresholds"], open(os.path.join(_paths.RESULTS, "threshold.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
