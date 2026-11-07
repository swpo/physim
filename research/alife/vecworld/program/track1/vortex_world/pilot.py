"""pilot -- level-2 selection signal and a first rough closure number, through the vw types.

    python pilot.py H n_seeds T_ticks R H_branch every [arms]
        e.g. python pilot.py 64 4 500 4 32 25 sel,neu,sel0

World: vortex_world.build(Config(H, W=H, G=H/16)) with the 'kinds' spec (level 0 -> vortex list -> (N, s_b)).
Arms (identical keys, so each pair is an identical-draw twin until the first mutation acts):
    sel   eps = 0.2 (kind b gains 20% more per unit fuel), sigma_a = 0.005
    neu   eps = 0   (neutral twin)
    sel0  eps = 0.2 with the channel noise off (sigma_a = 0): the source law, for the noise effect
Main runs: n_seeds members per arm from the initial law (designer ensemble, seed 0), T_ticks ticks,
L1 and L2 recorded every tick. Branches (sel and neu only, R > 0): every `every` ticks from tick
`every * 3` on, R fresh-noise replicates of every member for H_branch ticks (L2 recorded), the oracle
spread for the closure numbers (analyse.py). Level-0 states at branch points saved in float32.
Writes results/pilot_H{H}.npz and results/pilot_H{H}.json (timing).
"""
import json
import os
import sys
import time

import _paths
import jax
import numpy as np

import vw
import vortex_jax as VJ
import vortex_world as VW

H, NSEED, T, R, HB, EVERY = (int(a) for a in sys.argv[1:7])
ARMS = sys.argv[7].split(",") if len(sys.argv) > 7 else ["sel", "neu", "sel0"]
SEEDS = {a.split(":")[0]: int(a.split(":")[1]) if ":" in a else NSEED for a in ARMS}   # 'sel0:2' = 2 seeds
ARMS = list(SEEDS)
CHUNK = EVERY


def make(arm):
    cfg = VJ.Config(H=H, W=H, G=H // 16, sigma_a=0.0 if arm == "sel0" else VJ.Config.sigma_a)
    specs, parts = VW.build(cfg)
    theta = dict(VJ.THETA, eps=0.0 if arm == "neu" else 0.2)
    w = VW.MapWorld(specs["kinds"], world_seed=0, params={k: jax.numpy.asarray(v, jax.numpy.float64) for k, v in theta.items()})
    return w, parts


def main():
    out, timing = {}, {}
    for arm in ARMS:
        NS = SEEDS[arm]
        w, parts = make(arm)
        d = w.designer
        t0 = time.process_time()
        ens = d.ensemble(NS, seed=0)
        L1, L2, BR, XS, TB = [], [], [], [], []
        n_br = 0
        br_sec = 0.0
        while ens.t < T:
            ens, r = d.rollout(ens, T=CHUNK, rec=("L1", "L2"))
            L1.append(r["L1"] if not L1 else r["L1"][:, 1:])
            L2.append(r["L2"] if not L2 else r["L2"][:, 1:])
            if R > 0 and arm != "sel0" and ens.t >= 3 * EVERY:
                tb = time.process_time()
                rep = ens.clone(rep=R, fresh=True)
                _, rb = d.rollout(rep, T=HB, rec=("L2",))
                BR.append(rb["L2"].reshape(NS, R, HB + 1, -1).astype(np.float32))
                XS.append({k: np.asarray(v, np.float32) for k, v in ens.x.items()})
                TB.append(ens.t)
                n_br += NS * R * HB
                br_sec += time.process_time() - tb
            print(arm, ens.t, np.round(L2[-1][:, -1], 2).tolist(), flush=True)
        sec = time.process_time() - t0
        out[f"{arm}_L1"] = np.concatenate(L1, 1).astype(np.float32)
        out[f"{arm}_L2"] = np.concatenate(L2, 1).astype(np.float32)
        if BR:
            out[f"{arm}_branch_L2"] = np.stack(BR, 0)                  # (n_points, seeds, R, HB+1, 2)
            out[f"{arm}_branch_t"] = np.asarray(TB)
            for k in XS[0]:
                out[f"{arm}_x_{k}"] = np.stack([x[k] for x in XS], 0)   # (n_points, seeds, ...)
        main_ticks = NS * T
        timing[arm] = {"cpu_s_total": sec, "cpu_s_branches": br_sec, "member_ticks_main": main_ticks,
                       "member_ticks_branches": n_br,
                       "cpu_s_per_member_tick_main": (sec - br_sec) / main_ticks,
                       "cpu_s_per_member_tick_branches": br_sec / n_br if n_br else None,
                       "overflow": np.asarray(ens.carry.mem[0][1][:, -4:]).tolist() if isinstance(ens.carry.mem[0], tuple) else None}
        print(arm, json.dumps(timing[arm]), flush=True)
        meta = {"H": H, "n_seeds": NSEED, "seeds_per_arm": SEEDS, "T_ticks": T, "R": R, "H_branch": HB, "every": EVERY,
                "arms": ARMS, "arms_done": list(timing), "tick_time": VJ.Config().tick_time,
                "tracker": dict(VW.TRACK, **VW.slots_for(VJ.Config(H=H, W=H))), "sigma_a": VJ.Config.sigma_a, "timing": timing}
        np.savez_compressed(os.path.join(_paths.RESULTS, f"pilot_H{H}.npz"), **out)      # after every arm
        json.dump(meta, open(os.path.join(_paths.RESULTS, f"pilot_H{H}.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
