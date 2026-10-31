"""Native division check of c40's CIPS world on a smaller square box (no noise, no actions).

usage: divcheck.py SEED N T_END OUTPREFIX [SNAP_FROM SNAP_EVERY]
Every 10 t: label e > 0.5 (8-connected, periodic, area >= 6 px) and link components to the previous
sample by overlap; a split is one component overlapping >= 2 later ones, a merge the reverse.
Every SNAP_EVERY t from SNAP_FROM (default 100 t from 1000): the full field state (e, p, F, s, t) is saved for preparation.
"""
import json, os, sys, time
os.environ.setdefault("OMP_NUM_THREADS", "1")
sys.path.insert(0, "/home/user/physim/research/alife")
import importlib.util
import numpy as np
from scipy import ndimage
from labkit import ops
ops.WORKERS = 1
W = "/home/user/physim/research/alife/collective/contrib/20261026T1100-c40-cips-layered-divide-claim/world.py"
spec = importlib.util.spec_from_file_location("w", W); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
seed, N, T, out = int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
SNAP_FROM = float(sys.argv[5]) if len(sys.argv) > 5 else 1000.0
SNAP_EVERY = int(round(float(sys.argv[6]) / 0.1)) if len(sys.argv) > 6 else 1000
ST = np.ones((3, 3))

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from plabel import plabel


def comps(e):
    return plabel(e > 0.5)

s = m.init(seed, (N, N))
t0 = time.process_time()
prev, nprev = comps(s["e"])
log, events, snaps = [], [], {}
k = 0
nsteps = int(round(T / 0.1))
for k in range(1, nsteps + 1):
    s = m.step(s)
    if k % 100 == 0:
        lab, n = comps(s["e"])
        t = round(s["t"], 6)
        # links by overlap
        fwd = {i: set(np.unique(lab[prev == i])) - {0} for i in range(1, nprev + 1)}
        bwd = {j: set(np.unique(prev[lab == j])) - {0} for j in range(1, n + 1)}
        for i, ch in fwd.items():
            if len(ch) >= 2:
                cm = [list(np.round(ndimage.center_of_mass(lab == c), 1)) for c in ch]
                events.append(dict(t=t, kind="split", parent_area=int((prev == i).sum()),
                                   child_areas=[int((lab == c).sum()) for c in ch], child_centres=cm))
            if len(ch) == 0:
                events.append(dict(t=t, kind="death", area=int((prev == i).sum())))
        for j, pa in bwd.items():
            if len(pa) >= 2:
                events.append(dict(t=t, kind="merge", child_area=int((lab == j).sum())))
            if len(pa) == 0:
                events.append(dict(t=t, kind="birth", area=int((lab == j).sum()),
                                   centre=list(np.round(ndimage.center_of_mass(lab == j), 1))))
        log.append((t, n, int((lab > 0).sum()), float(s["F"].mean()), float(s["e"].max()), float(s["s"].max())))
        prev, nprev = lab, n
    if k % SNAP_EVERY == 0 and s["t"] >= SNAP_FROM - 1e-9:
        snaps[f"t{int(round(s['t']))}"] = np.stack([s["e"], s["p"], s["F"], s["s"]])
np.savez_compressed(out + "_snaps.npz", **snaps)
info = dict(seed=seed, N=N, T=T, cpu_s=round(time.process_time() - t0, 1),
            columns=["t", "bodies", "body_area_px", "mean_F", "max_e", "max_s"], log=log[::10],
            events=events, splits=[e["t"] for e in events if e["kind"] == "split"],
            merges=[e["t"] for e in events if e["kind"] == "merge"])
json.dump(info, open(out + ".json", "w"), indent=1)
print(json.dumps({k: v for k, v in info.items() if k not in ("log", "events")}))
