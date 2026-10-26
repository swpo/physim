"""Local feed cut (RUBRIC L4c local ablation) on c40's world from one shared state:
run world_iso.py (DRIFT default = c40's muscl) to T0, choose the body farthest from its neighbours, then branch
fed (unchanged) and cut (kF=0 inside a disk of radius R around that body, cut_t=T0) for TA.
Logs the target body's area (component overlapping the disk centre region) and the other bodies' count/area.
usage: cut.py SEED T0 TA R TAG"""
import os, sys, json, copy, importlib.util, numpy as np
from scipy import ndimage as ndi
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
seed, T0, TA, R, tag = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("w", os.path.join(here, "world_iso.py")); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
s = w.init(seed, w.META["size"])
while s["t"] < T0 - 1e-9: w.step(s)
H, W = s["shape"]; yy, xx = s["yy"], s["xx"]
lab, n = ndi.label(s["e"] > 0.5, structure=np.ones((3, 3)))
cents = []
for i in range(1, n + 1):
    m = lab == i
    if m.sum() < 30: continue
    th = [np.angle(np.exp(2j * np.pi * g[m] / N).mean()) % (2 * np.pi) * N / (2 * np.pi) for g, N in ((yy, H), (xx, W))]
    cents.append((i, th[0], th[1], int(m.sum())))
def pdist(a, b):
    dy = (a[1] - b[1] + H / 2) % H - H / 2; dx = (a[2] - b[2] + W / 2) % W - W / 2; return np.hypot(dy, dx)
best = max(cents, key=lambda c: min(pdist(c, o) for o in cents if o is not c))
gap = min(pdist(best, o) for o in cents if o is not best)
print(tag, "T0", T0, "bodies", len(cents), "target", best, "nearest neighbour dist %.1f" % gap, flush=True)
def disk(cy, cx, r):
    dy = (yy - cy + H / 2) % H - H / 2; dx = (xx - cx + W / 2) % W - W / 2; return dy * dy + dx * dx <= r * r
inner = disk(best[1], best[2], 12)
arms = {"fed": {}, "cut": {"cut_t": T0, "cut_r": R, "cut_y": best[1], "cut_x": best[2]}}
res = {}; snaps = {}
for name, mod in arms.items():
    a = copy.deepcopy(s); a["par"] = dict(s["par"], **mod); log = []; sn = []; k = 0
    while a["t"] <= T0 + TA + 1e-9:
        if k % 1000 == 0:
            e = a["e"]; lab, n = ndi.label(e > 0.5, structure=np.ones((3, 3)))
            tgt = set(np.unique(lab[inner & (lab > 0)]))
            ta = int(sum((lab == i).sum() for i in tgt))
            others = [int((lab == i).sum()) for i in range(1, n + 1) if i not in tgt and (lab == i).sum() >= 30]
            log.append(dict(t=round(a["t"]), target_area=ta, target_pieces=len(tgt), others=len(others), others_area=sum(others),
                            F_in=round(float(a["F"][disk(best[1], best[2], 10)].mean()), 4), F_mean=round(float(a["F"].mean()), 4)))
            if k % 5000 == 0: sn.append((a["t"], e.copy()))
        w.step(a); k += 1
    res[name] = log; snaps[name] = sn
    print(tag, name, [(l["t"], l["target_area"], l["others"], l["others_area"], l["F_in"]) for l in log], flush=True)
json.dump(dict(seed=seed, T0=T0, R=R, target=best[:3], nn_dist=gap, arms=res), open("cut_%s.json" % tag, "w"))
nc = max(len(v) for v in snaps.values())
fig, ax = plt.subplots(2, nc, figsize=(2.1 * nc, 4.6))
for i, name in enumerate(arms):
    for j in range(nc):
        a_ = ax[i, j]; a_.axis("off")
        if j < len(snaps[name]):
            t, im = snaps[name][j]; a_.imshow(im, cmap="magma", vmin=0, vmax=1)
            if name == "cut": a_.add_patch(plt.Circle((best[2], best[1]), R, fill=False, color="cyan", lw=0.6))
            a_.set_title("%s t=%.0f" % (name, t), fontsize=7)
fig.suptitle("seed %d: kF=0 in the cyan disk (R=%g) from t=%g; top: fed twin" % (seed, R, T0), fontsize=8)
fig.tight_layout(); fig.savefig("cut_%s.png" % tag, dpi=70)
