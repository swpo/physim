"""dtcheck_tick -- the time-step error of a tick against the tick's noise spread (level 0 and level-1 masses).

    python dtcheck_tick.py [n_states]       (default 6)

States: members 0..n-1 of the pilot's designer ensemble (world_seed 0, seed 0; dt 0.5, sigma_a 0.01) at tick 150
(t 1500, after formation). From each state, h = 1 and 10 ticks with the SAME channel noise at dt 0.5, 0.25 and
0.125 (the reference), and at dt 0.5 with an independent noise key (the spread). Reports per field the rms
difference to the reference, the observed order log2(err(0.5) / err(0.25)), and err / spread with spread =
rms(x(key a) - x(key b)) / sqrt(2); at level 1 the same for the cell masses (components of the tracker's
segmentation, compared only when both segmentations have the same number of cells). Writes results/dtcheck_tick.json.
"""
import json
import os
import sys

import _paths
import jax
import jax.numpy as jnp
import numpy as np

import vw
import membrane_jax as MJ
import membrane_world as MW

N_STATES = int(sys.argv[1]) if len(sys.argv) > 1 else 6
T0 = 150


def main():
    base = MJ.Config()
    specs, parts = MW.build(base)
    w = MW.MapWorld(specs["population"], world_seed=0)
    d = w.designer
    ens = d.ensemble(N_STATES, seed=0)
    ens, _ = d.rollout(ens, T=T0, rec=())
    X = {k: np.asarray(v) for k, v in ens.x.items()}
    keys = np.asarray(jax.random.key_data(ens.carry.key))
    tr = parts["tracker"]
    comp = jax.jit(lambda x: tr.components(MW.cells_field(x)))

    def masses(x):
        c = comp(x)
        n = int(min(int(c["n_kept"]), tr.max_kept))
        return np.sort(np.asarray(c["mass"])[:n])

    runners = {}
    for dt in (0.5, 0.25, 0.125):
        cfg = MJ.with_dt(base, dt)
        lev = MJ.make_level(cfg)
        q = lev.params
        runners[dt] = jax.jit(lambda x, key, t0, h, lev=lev, q=q: jax.lax.fori_loop(
            0, h, lambda i, xx: lev.step(q, xx, vw.Noise(key, t0 + i), jnp.zeros(base.m)), x), static_argnums=3)
    out = {"states": N_STATES, "tick": T0, "fields": MJ.FIELDS}
    for h in (1, 10):
        rows = {f: {"err05": [], "err025": [], "spread": []} for f in MJ.FIELDS + ("cell_mass",)}
        n_cells_eq = 0
        for i in range(N_STATES):
            x = {k: jnp.asarray(v[i]) for k, v in X.items()}
            ka = jax.random.wrap_key_data(jnp.asarray(keys[i]))
            kb = jax.random.fold_in(ka, 999)
            ref = runners[0.125](x, ka, T0, h)
            a5 = runners[0.5](x, ka, T0, h)
            a25 = runners[0.25](x, ka, T0, h)
            b5 = runners[0.5](x, kb, T0, h)
            for f in MJ.FIELDS:
                rows[f]["err05"].append(float(jnp.sqrt(jnp.mean((a5[f] - ref[f]) ** 2))))
                rows[f]["err025"].append(float(jnp.sqrt(jnp.mean((a25[f] - ref[f]) ** 2))))
                rows[f]["spread"].append(float(jnp.sqrt(jnp.mean((a5[f] - b5[f]) ** 2)) / np.sqrt(2)))
            mr, m5, m25, mb = masses(ref), masses(a5), masses(a25), masses(b5)
            if len(mr) == len(m5) == len(m25) == len(mb):
                n_cells_eq += 1
                rows["cell_mass"]["err05"].append(float(np.sqrt(np.mean((m5 - mr) ** 2))))
                rows["cell_mass"]["err025"].append(float(np.sqrt(np.mean((m25 - mr) ** 2))))
                rows["cell_mass"]["spread"].append(float(np.sqrt(np.mean((m5 - mb) ** 2)) / np.sqrt(2)))
        res = {}
        for f, r in rows.items():
            if not r["err05"]:
                continue
            e5, e25, sp = (float(np.mean(r[k])) for k in ("err05", "err025", "spread"))
            res[f] = {"rms_err_dt0.5": e5, "rms_err_dt0.25": e25, "order": float(np.log2(e5 / e25)) if e25 > 0 else None,
                      "noise_spread": sp, "err_over_spread_dt0.5": e5 / sp if sp > 0 else None,
                      "err_over_spread_dt0.25": e25 / sp if sp > 0 else None}
        res["n_states_same_cell_count"] = n_cells_eq
        out[f"h{h}"] = res
        print(h, json.dumps(res, indent=1), flush=True)
    json.dump(out, open(os.path.join(_paths.RESULTS, "dtcheck_tick.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
