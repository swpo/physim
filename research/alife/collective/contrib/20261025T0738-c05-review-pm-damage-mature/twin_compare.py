"""Same-seed undamaged twin of each labkit damage target: follow the twin's component at the
target's pre-cut position (largest-overlap continuation, periodic labels) and compare area/pre
with labkit's own follow-up of the damaged target (metrics.json damage.followup.target_area_rel).
usage: python twin_compare.py <rerun/seedS> <twin/seedS>"""
import sys, json, numpy as np
from scipy import ndimage
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

def plabel(m):
    lab, n = ndimage.label(m)
    for a, b in ((lab[0], lab[-1]), (lab[:, 0], lab[:, -1])):
        for u, v in set(zip(a.tolist(), b.tolist())):
            if u and v and u != v: lab[lab == v] = u
    return lab

out = []
for rr, tw in zip(sys.argv[1::2], sys.argv[2::2]):
    dm = json.load(open(rr + "/metrics.json"))["damage"]; f0 = dm["frame"]
    rng = dm["followup"]["segmentation"]["range"]; thr = rng[0] + 0.35 * (rng[1] - rng[0])
    M = np.load(tw + "/frames.npz")["matter"]
    lab = plabel(M[f0] > thr)
    H, W = lab.shape; cy, cx = int(round(dm["cy"])) % H, int(round(dm["cx"])) % W
    i = lab[cy, cx]
    if i == 0:
        yy, xx = np.nonzero(lab); j = np.argmin((yy - cy) ** 2 + (xx - cx) ** 2); i = lab[yy[j], xx[j]]
    cur = lab == i; a0 = cur.sum(); rel = [1.0]
    for f in range(f0 + 1, M.shape[0]):
        lab = plabel(M[f] > thr)
        ov = np.bincount(lab[cur], minlength=lab.max() + 1); ov[0] = 0
        if ov.max() == 0: rel.append(None); break
        cur = lab == ov.argmax(); rel.append(round(float(cur.sum() / a0), 3))
    dmg = dm["followup"]["target_area_rel"]
    out.append(dict(run=rr, frame=f0, erased=dm["erased_frac"], twin_area_pre=int(a0), damaged_pre=dm["followup"]["target_area_pre"], twin=rel, damaged=dmg))
    print(rr, "erased %.2f" % dm["erased_frac"], "twin pre", a0, "damaged pre", dm["followup"]["target_area_pre"])
    for k in range(0, len(dmg), 5):
        print("  +%d frames: damaged %s twin %s" % (k, dmg[k], rel[k] if k < len(rel) else None))
json.dump(out, open("twin_compare.json", "w"))
fig, ax = plt.subplots(1, len(out), figsize=(5 * len(out), 3.5))
for a, o in zip(np.atleast_1d(ax), out):
    a.plot([x if x is not None else np.nan for x in o["damaged"]], "C3", label="damaged target (labkit follow-up)")
    a.plot([x if x is not None else np.nan for x in o["twin"]], "C0", label="same cell, undamaged twin")
    a.set_title(f"{o['run']} cut at frame {o['frame']}, erased {o['erased']:.2f}", fontsize=8); a.set_xlabel("frames after cut (x50 t)"); a.set_ylabel("area / pre-cut")
np.atleast_1d(ax)[0].legend(fontsize=7); plt.tight_layout(); plt.savefig("twin_compare.png", dpi=70)
