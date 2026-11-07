"""pilot -- cells, growth and division at level 1, a rough level-2 closure, the dt check and the noise level.

    python pilot.py arm[,arm...] [n_seeds] [T_ticks]          (defaults: all arms, 16 seeds, 600 ticks)

World: membrane_world.build(cfg) with the 'population' spec (level 0 -> cell list -> (N, size, rate)) through
MapWorld; 128^2; one tick = 10 time units. Every arm uses designer ensemble seed 0 of world_seed 0, so member j
has the same key in every arm: the same initial state (the init law does not depend on dt or sigma_a) and the
same standard normals behind the channel noise (eta = sigma_a * z). The dt arms are therefore exact paired
twins that differ only in the native step.
Arms:
    main    dt 0.5,  sigma_a 0.01   (+ branches for the closure numbers)
    dt025   dt 0.25, sigma_a 0.01   (the dt check: 40 native steps per tick)
    dt1     dt 1.0,  sigma_a 0.01   (the source's own step: 10 per tick)
    det     dt 0.5,  sigma_a 0      (the source law, no noise)
    sa003   dt 0.5,  sigma_a 0.003
    sa03    dt 0.5,  sigma_a 0.03
Records every tick: L1 (K x 12 + 5), L2 (3), ev (K x 2 tracker event and uid per slot). Branches (main only):
at ticks 100, 150, ..., 550, R = 8 fresh-noise replicates of every member for 32 ticks (L2, and the level-1
(present, mass) columns plus the 5 counters as branch_L1pm, recorded): the
oracle spread for the closure numbers (analyse.py). phi snapshots of member 0 at ticks 0, 25, 50, 100, 300,
600 (float32). Writes results/pilot_{arm}.npz and results/pilot_{arm}.json after every arm.
"""
import json
import os
import sys
import time

import _paths
import jax
import jax.numpy as jnp
import numpy as np

import membrane_jax as MJ
import membrane_world as MW

ARMS = {"main": (0.5, 0.01, True), "dt025": (0.25, 0.01, False), "dt1": (1.0, 0.01, False),
        "det": (0.5, 0.0, False), "sa003": (0.5, 0.003, False), "sa03": (0.5, 0.03, False)}
RUN = sys.argv[1].split(",") if len(sys.argv) > 1 and sys.argv[1] != "all" else list(ARMS)
NSEED = int(sys.argv[2]) if len(sys.argv) > 2 else 16
T = int(sys.argv[3]) if len(sys.argv) > 3 else 600
R, HB, EVERY, FIRST = 8, 32, 50, 100
SNAP = (0, 25, 50, 100, 300, 600)
CHUNK = 25


def make(arm):
    dt, sa, _ = ARMS[arm]
    cfg = MJ.with_dt(MJ.Config(sigma_a=sa), dt)
    specs, parts = MW.build(cfg)
    return MW.MapWorld(specs["population"], world_seed=0), parts


def main():
    for arm in RUN:
        w, parts = make(arm)
        d = w.designer
        branches = ARMS[arm][2]
        t0 = time.process_time()
        ens = d.ensemble(NSEED, seed=0)
        L1, L2, EV, BR, BR1, TB, SN = [], [], [], [], [], [], {}
        br_sec, n_br = 0.0, 0
        while True:
            if ens.t in SNAP:
                SN[ens.t] = np.asarray(ens.x["phi"][0], np.float32)
            if branches and ens.t >= FIRST and (ens.t - FIRST) % EVERY == 0 and ens.t + HB <= T:
                tb = time.process_time()
                rep = ens.clone(rep=R, fresh=True)
                _, rb = d.rollout(rep, T=HB, rec=("L1", "L2"))
                BR.append(rb["L2"].reshape(NSEED, R, HB + 1, -1).astype(np.float32))
                Kt = parts["tracker"].K
                l1 = rb["L1"].reshape(NSEED, R, HB + 1, -1)
                tab = l1[..., :Kt * 12].reshape(NSEED, R, HB + 1, Kt, 12)[..., :2].reshape(NSEED, R, HB + 1, 2 * Kt)
                BR1.append(np.concatenate([tab, l1[..., Kt * 12:]], -1).astype(np.float32))
                TB.append(ens.t)
                n_br += NSEED * R * HB
                br_sec += time.process_time() - tb
            if ens.t >= T:
                break
            step = min(CHUNK, T - ens.t, min([s - ens.t for s in SNAP if s > ens.t] + [CHUNK]))
            if branches:
                nxt = [p for p in range(FIRST, T, EVERY) if p > ens.t]
                if nxt:
                    step = min(step, nxt[0] - ens.t)
            ens, r = d.rollout(ens, T=step, rec=("L1", "L2", "ev"))
            first = not L1
            L1.append(r["L1"] if first else r["L1"][:, 1:])
            L2.append(r["L2"] if first else r["L2"][:, 1:])
            EV.append(r["ev"] if first else r["ev"][:, 1:])
            if ens.t % 100 == 0:
                print(arm, ens.t, np.round(L2[-1][:, -1, 0], 0).astype(int).tolist(), flush=True)
        sec = time.process_time() - t0
        out = {"L1": np.concatenate(L1, 1).astype(np.float32), "L2": np.concatenate(L2, 1).astype(np.float32),
               "ev": np.concatenate(EV, 1).astype(np.int32)}
        if BR:
            out["branch_L2"] = np.stack(BR, 0)               # (points, seeds, R, HB + 1, 3)
            out["branch_L1pm"] = np.stack(BR1, 0)            # (points, seeds, R, HB + 1, K*2 + 5): (present, mass) per slot + globals
            out["branch_t"] = np.asarray(TB)
        for t, v in SN.items():
            out[f"phi_t{t}"] = v
        cfg = parts["cfg"]
        mem = ens.carry.mem[0][1]
        meta = {"arm": arm, "dt": cfg.dt, "n_sub": cfg.n_sub, "sigma_a": cfg.sigma_a, "tick_time": cfg.tick_time,
                "H": cfg.H, "n_seeds": NSEED, "T_ticks": T, "R": R, "H_branch": HB, "every": EVERY, "first": FIRST,
                "K": parts["tracker"].K, "tracker": dict(MW.TRACK, **MW.slots_for(cfg)), "W_rate": MW.W_RATE,
                "cpu_s_total": sec, "cpu_s_branches": br_sec, "member_ticks_main": NSEED * T, "member_ticks_branches": n_br,
                "cpu_s_per_member_tick_main": (sec - br_sec) / (NSEED * T),
                "cpu_s_per_member_tick_branches": br_sec / n_br if n_br else None,
                "tracker_overflow_per_member": np.asarray(mem[:, -4:]).tolist()}
        np.savez_compressed(os.path.join(_paths.RESULTS, f"pilot_{arm}.npz"), **out)
        json.dump(meta, open(os.path.join(_paths.RESULTS, f"pilot_{arm}.json"), "w"), indent=1)
        print(arm, json.dumps({k: v for k, v in meta.items() if k != "tracker_overflow_per_member"}), flush=True)


if __name__ == "__main__":
    main()
