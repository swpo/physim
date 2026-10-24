"""Per-kind analysis of a heredity pack: kind = cell-mean of marker h > 0.5 (on) or not (off).
Uses frames.npz 'render' (channels u, m, h as positive deviations). Tracks cells by overlap
between consecutive rendered frames, counts cells per kind, kind switches, and splits by
parent kind -> daughter kinds.   python kinds.py packs/xcell-her/seed0"""
import sys, json
import numpy as np
from scipy import ndimage
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

d = sys.argv[1]
z = np.load(f"{d}/frames.npz")
R = z["render"].astype(np.float32); fr = z["render_f"]
meta = json.load(open(f"{d}/metrics.json"))
dtf = meta["summary"]["time"] / (meta["summary"]["frames"] - 1)
H = R.shape[-1]

def label_periodic(mask):
    lab, n = ndimage.label(mask)
    par = list(range(n + 1))
    def f(a):
        while par[a] != a: par[a] = par[par[a]]; a = par[a]
        return a
    for a, b in list(zip(lab[0], lab[-1])) + list(zip(lab[:, 0], lab[:, -1])):
        if a and b: par[f(a)] = f(b)
    roots = sorted({f(i) for i in range(1, n + 1)})
    lut = np.zeros(n + 1, int)
    for i in range(1, n + 1): lut[i] = roots.index(f(i)) + 1
    return lut[lab], len(roots)

thr = 0.45 * R[:, 0].max()
cells = []
for k in range(len(R)):
    lab, n = label_periodic(ndimage.gaussian_filter(R[k, 0], 1, mode="wrap") > thr)
    sizes = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
    hmax = ndimage.mean(R[k, 2], lab, range(1, n + 1)) if n else []   # cell-mean h (robust to noise spikes)
    keep = [i for i in range(n) if sizes[i] >= 10]
    cells.append(dict(lab=lab, ids=[i + 1 for i in keep], on=[bool(hmax[i] > 0.5) for i in keep]))
n_on = [sum(c["on"]) for c in cells]; n_off = [len(c["on"]) - sum(c["on"]) for c in cells]
switch_on_off = switch_off_on = 0
splits = {"on->on+on": 0, "on->on+off": 0, "on->off+off": 0, "off->off+off": 0, "off->on+x": 0}
births = 0
sw_events = []
deaths = {"on": 0, "off": 0}
for k in range(1, len(cells)):
    A, B = cells[k - 1], cells[k]
    ch = {}
    for j, bid in enumerate(B["ids"]):
        m = B["lab"] == bid
        ov = A["lab"][m]; ov = ov[ov > 0]
        if len(ov) == 0: births += 1; continue
        pid = np.bincount(ov).argmax()
        if pid in A["ids"]:
            ch.setdefault(pid, []).append(B["on"][j])
    for q, pid in enumerate(A["ids"]):
        if pid not in ch:
            deaths["on" if A["on"][q] else "off"] += 1
    for pid, kids in ch.items():
        pk = A["on"][A["ids"].index(pid)]
        if len(kids) == 1:
            if pk != kids[0]:
                if pk: switch_on_off += 1
                else: switch_off_on += 1
                m = A["lab"] == pid
                ys, xs = np.nonzero(m)
                sw_events.append(dict(frame=int(fr[k]), t=float(fr[k] * dtf), to_on=bool(kids[0]), cy=int(np.median(ys)), cx=int(np.median(xs))))
        else:
            non = sum(kids)
            if pk:
                splits["on->on+on" if non == len(kids) else ("on->off+off" if non == 0 else "on->on+off")] += 1
            else:
                splits["off->off+off" if non == 0 else "off->on+x"] += 1
t = fr * dtf
out = dict(pack=d, n_on_start=n_on[0], n_off_start=n_off[0], n_on_end=n_on[-1], n_off_end=n_off[-1],
           switches_on_to_off=switch_on_off, switches_off_to_on=switch_off_on, splits=splits, births=births, switch_events=sw_events, deaths=deaths,
           on_fraction_mean_last_quarter=float(np.mean([a / max(a + b, 1) for a, b in zip(n_on, n_off)][3 * len(n_on) // 4:])))
print(json.dumps(out))
json.dump(out | {"t": t.tolist(), "n_on": n_on, "n_off": n_off}, open(f"{d}/kinds.json", "w"))
plt.figure(figsize=(5, 3)); plt.plot(t, n_on, label="h-on cells"); plt.plot(t, n_off, label="h-off cells")
plt.xlabel("time"); plt.ylabel("cells"); plt.legend(); plt.title(d.split("packs/")[-1], fontsize=9)
plt.tight_layout(); plt.savefig(f"{d}/kinds.png", dpi=80)
