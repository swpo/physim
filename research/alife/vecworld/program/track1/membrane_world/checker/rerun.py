"""Checker: rerun the pilot's main arm (16 seeds, first 60 ticks) and the dt1 arm (16 seeds, 40 ticks)
exactly as pilot.py builds them, compare with the saved pilot_{arm}.npz; then time it."""
import sys, json, time
sys.path.insert(0, "/home/user/evalwork/vecworld/program/track1/membrane_world")
import _paths
import numpy as np
import pilot  # module-level constants only; main() not called
OUT = {}
for arm, T in (("main", 60), ("dt1", 40)):
    w, parts = pilot.make(arm)
    d = w.designer
    ens = d.ensemble(16, seed=0)
    t0 = time.process_time()
    ens, r = d.rollout(ens, T=T, rec=("L1", "L2", "ev"))
    sec = time.process_time() - t0
    S = np.load(f"{_paths.RESULTS}/pilot_{arm}.npz")
    L1, L2, ev = np.asarray(r["L1"], np.float32), np.asarray(r["L2"], np.float32), np.asarray(r["ev"], np.int32)
    o = {"T": T, "cpu_s_incl_compile": sec,
         "L1_maxabs": float(np.abs(L1 - S["L1"][:, :T + 1]).max()),
         "ev_mismatch": int((ev != S["ev"][:, :T + 1]).sum()),
         "N_equal_all": bool((L2[..., 0] == S["L2"][:, :T + 1, 0]).all())}
    if arm == "main":
        o["L2_maxabs"] = float(np.abs(L2 - S["L2"][:, :T + 1]).max())
        # second call, compiled: timing
        e2 = d.ensemble(16, seed=0)
        t1 = time.process_time(); d.rollout(e2, T=T, rec=("L1", "L2", "ev")); o["cpu_s_per_member_tick_compiled"] = (time.process_time() - t1) / (16 * T)
    OUT[arm] = o
    print(arm, o, flush=True)
json.dump(OUT, open("/home/user/evalwork/vecworld/program/track1/membrane_world/checker/rerun.json", "w"), indent=1)
