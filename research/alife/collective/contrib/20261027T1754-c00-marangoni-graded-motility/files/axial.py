"""Heading along the rod axis: signed axial velocity u = v . a (centroid velocity over a 25 t window, a = long axis
oriented continuously along each track), split-born rods. Two symmetric swimming directions would give a bimodal |u|
-> sign structure: |u| / speed near 1 with long runs of one sign. Reports: fraction of rod-frames with |u| >= 0.9 speed,
bimodality of u (symmetric by construction; two peaks at +-v mean persistent direction), reversals (sign changes of u
with a dead band +-THR) per rod per 100 t, median run length between reversals, and the fraction of dividing rods that
never reverse.  usage: axial.py OUT.json THR eps=path,path ..."""
import sys, json
import numpy as np
from scipy import stats
sys.path.insert(0, "/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/paperexp/marangoni-bistability")
import states as S
FT = 2.5; W = 5
thr = float(sys.argv[2])
arms = [(a.split("=")[0], a.split("=")[1].split(",")) for a in sys.argv[3:]]
res = {}
for eps, paths in arms:
    U = []; rev = 0; T = 0; runs = []; never_div = []; ncross_div = []
    for p in paths:
        d = json.load(open(p))
        for t in d["tracks"]:
            if t["birth"] != "split" or t["n"] < 2 * W + 9: continue
            ax = np.array(t["ax"], float)
            for k in range(1, len(ax)):
                if ax[k] @ ax[k - 1] < 0: ax[k] = -ax[k]
            y = np.array(t["y"]); x = np.array(t["x"]); n = t["n"]; L = np.median(t["L4"])
            ks = np.arange(W, n - W)
            vy = (y[ks + W] - y[ks - W]) / (2 * W * FT) / L; vx = (x[ks + W] - x[ks - W]) / (2 * W * FT) / L
            u = vy * ax[ks, 0] + vx * ax[ks, 1]
            if np.median(u) < 0: u = -u  # orient each track's axis by its dominant travel direction
            U.append(u)
            st = S.schmitt(u, -thr, thr)  # 1 = moving along +axis, 0 = along -axis
            ch = np.nonzero(np.diff(st))[0]; rev += len(ch); T += len(u) * FT
            b = np.concatenate([[-1], ch, [len(u) - 1]])
            runs += [(b[i + 1] - b[i]) * FT for i in range(1, len(b) - 2)]
            if t["dividing"]: never_div.append(len(ch) == 0); ncross_div.append(len(ch))
    Ua = np.concatenate(U)
    res[eps] = dict(rodframes=int(len(Ua)), frac_negative=float(np.mean(Ua < 0)), reversals_per_rod_100t=100 * rev / T,
                    complete_runs=len(runs), median_run=float(np.median(runs)) if runs else None,
                    mean_run=float(np.mean(runs)) if runs else None, cv_run=float(np.std(runs) / np.mean(runs)) if len(runs) > 3 else None,
                    dividing=len(never_div), dividing_never_reverse=int(np.sum(never_div)),
                    dividing_reversals_median=float(np.median(ncross_div)) if ncross_div else None)
    print(eps, res[eps])
json.dump(res, open(sys.argv[1], "w"), indent=1)
