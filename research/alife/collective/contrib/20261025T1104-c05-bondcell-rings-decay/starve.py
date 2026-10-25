"""bondcell starvation fork: run to t_fork, branch (fed vs k_cat=0, i.e. food can no longer become core), run to T.
usage: starve.py module seed t_fork T out_prefix  (WORLD_P honoured)"""
import sys, copy, time, numpy as np
sys.path.insert(0, "."); import importlib
w = importlib.import_module(sys.argv[1]); seed, tf, T, out = int(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
dt = w.META["dt"]; s = w.init(seed, w.META["size"]); t0 = time.time()
for k in range(int(tf / dt)): s = w.step(s)
arms = {"fed": s, "starve": copy.deepcopy(s)}
arms["starve"]["p"]["k_cat"] = 0.0; arms["starve"]["p"]["k_cat1"] = 0.0
rows = []
for name, st in arms.items():
    for k in range(int((T - tf) / dt) + 1):
        if k % int(10 / dt) == 0:
            d = w.stats(st); d.update(arm=name, t=round(tf + k * dt)); rows.append(d); print(d, round(time.time() - t0), flush=True)
            np.savez("%s_%s_t%d.npz" % (out, name, round(tf + k * dt)), x=st["x"], t=st["t"], bA=st["bA"], bB=st["bB"])
        st = w.step(st)
