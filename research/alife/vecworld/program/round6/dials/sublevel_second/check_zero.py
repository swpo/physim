"""check_zero -- the zero point of the dial: with lam = 0 every candidate's hidden world IS the public world.

    python -B check_zero.py [size] [members] [ticks]          (defaults 64, 3, 60)

For each candidate: the hidden world (lam = 0; the hidden field starts at its equilibrium, which is 0) and the public world
(membrane_world.build, unchanged) are run from the same designer ensemble (same keys) under the same random
input program; compared: the four public level-0 fields at the last tick, the level-1 cell list and level 2 at
every tick (largest absolute difference; 0.0 means bit for bit), and the hidden field (must stay 0).
Also prints substrate statistics inside cells of the public world at the last tick (used to place the dormancy
threshold s_c below the passive range). Writes results/check_zero.json.
"""
import json
import os
import sys
import time

import numpy as np

import sublevel as SL
from sublevel import MJ, MW

SIZE = int(sys.argv[1]) if len(sys.argv) > 1 else 64
NM = int(sys.argv[2]) if len(sys.argv) > 2 else 3
T = int(sys.argv[3]) if len(sys.argv) > 3 else 60


def main():
    cfg = SL.small_cfg(SIZE)
    rng = np.random.default_rng(0)
    P = np.zeros((T, cfg.m))
    for t in range(10, T, 7):                                    # a few random pushes of 0.03 (feed and withdraw)
        P[t, rng.integers(cfg.m, size=3)] = rng.choice([-0.03, 0.03], 3)
    spec, parts = SL.build(cfg)
    wp = MW.MapWorld(spec, world_seed=0)
    dp = wp.designer
    t0 = time.process_time()
    ep, rp = dp.rollout(dp.ensemble(NM, seed=0), P=P, T=T, rec=("L1", "L2"))
    cpu_pub = time.process_time() - t0
    xp = {k: np.asarray(v) for k, v in ep.x.items()}
    out = {"size": SIZE, "members": NM, "ticks": T, "cpu_s_public_incl_compile": cpu_pub, "candidates": {}}
    for cand in SL.CANDS:
        s, _ = SL.build(cfg, cand, hidden=dict(lam=0.0))
        wh = MW.MapWorld(s, world_seed=0)
        dh = wh.designer
        t0 = time.process_time()
        eh, rh = dh.rollout(dh.ensemble(NM, seed=0), P=P, T=T, rec=("L1", "L2"))
        cpu = time.process_time() - t0
        xh = {k: np.asarray(v) for k, v in eh.x.items()}
        res = {"max_abs_diff_fields": {k: float(np.abs(xh[k] - xp[k]).max()) for k in MJ.FIELDS},
               "max_abs_diff_L1": float(np.abs(rh["L1"] - rp["L1"]).max()),
               "max_abs_diff_L2": float(np.abs(rh["L2"] - rp["L2"]).max()),
               "hidden_field_max": float(np.abs(xh[SL.EXTRA[cand]]).max()),
               "cpu_s_incl_compile": cpu}
        res["bit_for_bit"] = bool(max(list(res["max_abs_diff_fields"].values()) + [res["max_abs_diff_L1"],
                                                                                 res["max_abs_diff_L2"]]) == 0.0)
        out["candidates"][cand] = res
        print(cand, res, flush=True)
    inside = xp["phi"] > 0.5
    qs = [0.01, 0.05, 0.25, 0.5, 0.75, 0.95]
    out["public_state_stats_last_tick"] = {
        "S_inside_cells_quantiles": dict(zip(map(str, qs), np.quantile(xp["S"][inside], qs).tolist())),
        "S_outside_quantiles": dict(zip(map(str, qs), np.quantile(xp["S"][~inside], qs).tolist())),
        "K_inside_mean": float(xp["K"][inside].mean()), "L_inside_mean": float(xp["L"][inside].mean()),
        "phi_area_per_member": inside.reshape(NM, -1).sum(1).tolist(),
        "N_cells_last_tick": rp["L2"][:, -1, 0].tolist()}
    print(out["public_state_stats_last_tick"])
    os.makedirs(os.path.join(SL.HERE, "results"), exist_ok=True)
    json.dump(out, open(os.path.join(SL.HERE, "results", "check_zero.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
