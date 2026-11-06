"""Do the three views (objects, coarse, both; world_seed 0, reset seed SEED) share hidden structure?
Compares the hidden input maps and the level-0 trajectories (float32 copies) of the three hero episodes.

usage: python -B compare_l0.py SEED   -> results/compare_l0.json
"""
import json
import sys

import numpy as np

BASE = "/home/user/evalwork/vecworld/vw1/fresh/media/results"
seed = int(sys.argv[1])
H = {v: np.load(f"{BASE}/hero_{v}_s{seed}.npz") for v in ("objects", "coarse", "both")}
res = {"seed": seed, "world_seed": 0}
for a, b in (("objects", "coarse"), ("objects", "both"), ("coarse", "both")):
    xa, xb = H[a]["x"], H[b]["x"]
    d = np.abs(xa - xb).reshape(len(xa), -1).max(1)
    nz = np.flatnonzero(d > 0)
    res[f"{a}_vs_{b}"] = {"in_map_identical": bool(np.array_equal(H[a]["in_map"], H[b]["in_map"])),
                          "level0_max_abs_diff_float32_at_ticks_0_1_10_50_100_300": [float(d[t]) for t in (0, 1, 10, 50, 100, 300) if t < len(d)],
                          "first_tick_level0_differs": int(nz[0]) if nz.size else None,
                          "level0_identical_all_ticks": bool(nz.size == 0)}
json.dump(res, open(f"{BASE}/compare_l0.json", "w"), indent=1)
print(json.dumps(res, indent=1))
