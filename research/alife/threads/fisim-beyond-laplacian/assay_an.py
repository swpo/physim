"""Analyse assay/<tag>.npz: every division whose parent is h-on, classified from the daughters'
raw max h deviation (on if > 1.5; the on-state deviation is ~2.2; noise-free runs), plus conversions of intact
cells. Divisions within 6 t / 8 px of a kill are excluded (cuts, not fissions).
python assay_an.py assay/<tag>  -> prints a JSON summary, writes <tag>_an.json"""
import sys, json
import numpy as np
from scipy import ndimage
tag = sys.argv[1]
z = np.load(tag + ".npz"); meta = json.load(open(tag + ".json"))
U, Hh, T = z["u"].astype(np.float32), z["h"].astype(np.float32), z["t"]
N = U.shape[-1]; dx = float(z["dx"]); thr = 0.45 * (np.sqrt(2) + 0.7035)
kills = np.array(meta["kills"]).reshape(-1, 3)
def near_kill(t, cy, cx):
    if not len(kills): return False
    dtk = np.abs(kills[:, 0] - t) < 6
    d = np.hypot((kills[:, 1] - cy + N / 2) % N - N / 2, (kills[:, 2] - cx + N / 2) % N - N / 2)
    return bool(np.any(dtk & (d < 8 / dx + 5 / dx)))
def lab_of(k):
    lab, n = ndimage.label(U[k] > thr)
    lab2 = lab.copy()
    # periodic merge
    for a_, b_ in list(zip(lab[0], lab[-1])) + list(zip(lab[:, 0], lab[:, -1])):
        if a_ and b_ and a_ != b_: lab2[lab2 == b_] = a_
    ids = [i for i in np.unique(lab2) if i and (lab2 == i).sum() >= 10 / (dx / 0.5) ** 2]
    return lab2, ids
divs, conv = [], []
prev = lab_of(0)
for k in range(1, len(T)):
    cur = lab_of(k)
    A, aids = prev; B, bids = cur
    children = {}
    for b in bids:
        m = B == b; ov = A[m]; ov = ov[ov > 0]
        if len(ov) == 0: continue
        children.setdefault(int(np.bincount(ov).argmax()), []).append(b)
    for p, kids in children.items():
        if p not in aids: continue
        pm = A == p; hp = float(Hh[k - 1][pm].max()) - 0.5   # cell max of h dev; on-state ~2.2, so on <=> max > 1.5
        cy, cx = ndimage.center_of_mass(pm)
        if len(kids) >= 2:
            if near_kill(T[k], cy, cx): continue
            hk = [float(Hh[k][B == b].max()) - 0.5 for b in kids]
            divs.append(dict(t=float(T[k]), parent_h=hp, daughters_h=hk, cy=float(cy), cx=float(cx)))
        else:
            hc = float(Hh[k][B == kids[0]].max()) - 0.5
            kt = meta["args"].get("kick_t", 100.0)
            if (hp > 1.0) != (hc > 1.0) and abs(T[k] - kt) > 20:
                conv.append(dict(t=float(T[k]), h_before=hp, h_after=hc, cy=float(cy), cx=float(cx)))
    prev = cur
on_divs = [d for d in divs if d["parent_h"] > 1.0]
cls = lambda d: "on+on" if all(x > 1.0 for x in d["daughters_h"]) else ("off+off" if all(x <= 1.0 for x in d["daughters_h"]) else "on+off")
counts = {c: sum(cls(d) == c for d in on_divs) for c in ("on+on", "on+off", "off+off")}
off_divs = [d for d in divs if d["parent_h"] <= 1.0]
off_counts = {c: sum(cls(d) == c for d in off_divs) for c in ("on+on", "on+off", "off+off")}
# conversions that are not the immediate aftermath of a division (genuine intact-cell switching)
div_t = [(d["t"], d["cy"], d["cx"]) for d in divs]
def near_div(c):
    return any(abs(c["t"] - t) < 10 and np.hypot((c["cy"] - y + N / 2) % N - N / 2, (c["cx"] - x + N / 2) % N - N / 2) < 20 / dx * 0.5 for t, y, x in div_t)
conv_intact = [c for c in conv if not near_div(c) and not near_kill(c["t"], c["cy"], c["cx"])]
out = dict(tag=tag.split("/")[-1], n_div=len(divs), on_divisions=counts, off_divisions=off_counts,
           on_on_frac=(counts["on+on"] / max(1, len(on_divs))),
           conversions_intact=dict(off_to_on=sum(c["h_after"] > 1 for c in conv_intact), on_to_off=sum(c["h_after"] <= 1 for c in conv_intact)),
           kicks=len(meta["kicks"]), kick_offset_px_mean=float(np.mean([k_["offset_px"] / max(k_["radius_px"], 1) for k_ in meta["kicks"]])) if meta["kicks"] else None,
           on_cells_end=int(sum(1 for b in lab_of(len(T) - 1)[1] if Hh[-1][lab_of(len(T) - 1)[0] == b].max() > 1.5)),
           cells_end=len(lab_of(len(T) - 1)[1]))
json.dump(dict(out, divisions=divs, conversions=conv_intact), open(tag + "_an.json", "w"))
print(json.dumps(out))
