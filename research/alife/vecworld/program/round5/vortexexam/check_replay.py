"""check_replay -- CPU check of the exam's branching (seconds; small box, 5-step ticks).

run_episodes saves the device state at each program tick a. Replaying from that snapshot with the main run's own
process keys, the clock a and the main run's program U[a : a + HB] must reproduce the main run's vortex lists at
states a + 1 .. a + HB exactly; with fresh keys it must differ. This fixes the index convention used by job2.py
for the exam's replicate truths (state index = ticks done; U[t] acts during tick t; noise clock = tick index).
usage: python -B check_replay.py   -> results/check_replay.json
"""
import json
import os
import sys

import vxlib as VX

import numpy as np

from vw.world import make_key, member_keys

VX.LAB_T, VX.LAB_TICK = 0.3, 3
VX.THETA0["mut128"] = 0.0125
RN = VX.Runner(32, n_sub=5)
B, T, PROG, HB = 5, 24, (8, 14), 6
Q = VX.theta_batch(B, eps=np.linspace(0, 0.4, B))
keys = member_keys(make_key(1, 2), B)
out = VX.run_episodes(RN, Q, keys, 7, T=T, prog_ticks=PROG, nats=200.0, snaps=PROG, keep_lists=True)
kp = RN.proc_keys(keys)
res = {"nats": out["nats"].tolist(), "classes": out["cls"].tolist(), "anchors": {}}
ok = True
for a in PROG:
    X, M = out["snaps"][a]
    U = out["U"][:, a:a + HB].transpose(1, 0, 2)
    _, _, Y = RN.run(Q, X, M, kp, a, U)
    d = float(np.abs(Y.transpose(1, 0, 2) - out["lists"][:, a + 1:a + HB + 1]).max())
    kf = RN.proc_keys(member_keys(make_key(9, a), B), fresh=True)
    _, _, Y2 = RN.run(Q, X, M, kf, a, U)
    fresh = float(np.abs(Y2 - Y).max())
    res["anchors"][str(a)] = {"max_abs_diff_replay_vs_main": d, "max_abs_diff_fresh_vs_replay": fresh}
    ok &= (d == 0.0) and fresh > 0
res["summaries_match_level2"] = bool(np.allclose(out["S"][..., :2], VX.level2(out["lists"], RN.K)))
res["pass"] = bool(ok and res["summaries_match_level2"])
os.makedirs(os.path.join(VX.HERE, "results"), exist_ok=True)
json.dump(res, open(os.path.join(VX.HERE, "results", "check_replay.json"), "w"), indent=1)
print(res)
sys.exit(0 if res["pass"] else 1)
