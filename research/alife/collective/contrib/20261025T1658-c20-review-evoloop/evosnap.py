"""Run c16's evoloop world.py to step T (seed s, L) and save the grid. usage: evosnap.py world.py seed L T out.npy"""
import sys, importlib.util, numpy as np, os
os.environ["WORLD_P"] = "{}"
spec = importlib.util.spec_from_file_location("w", sys.argv[1]); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
seed, L, T = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
s = w.init(seed, (L, L))
for t in range(T): w.step(s)
np.save(sys.argv[5], s["g"])
