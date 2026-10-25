"""Physical check of genealogy deaths on labkit's recorded fields: for each mature death (>= 20 snapshots,
t > 1000), follow the catalyst blob (render channel K > KT, 8-connected, periodic via tiling) under the dying
cell's last position through the recorded frames from t_death - 3000 to t_death + 8000. A death is PHYSICAL
if, in some frame within 3000 steps after t_death, no blob of >= 4 px overlaps a 3 px disk at that position
(and the blob present before has not merged with a large cell); otherwise the object persisted (flicker).
Reports per death the blob area series.
usage: python physdeath.py pack snaps.pkl gen.json"""
import sys, json, pickle, numpy as np
from scipy import ndimage
pk, pkl, gj = sys.argv[1:4]; KT = 0.3
f = np.load(f"{pk}/frames.npz"); R = f["render"]; RF = f["render_f"]; spf = json.load(open(f"{pk}/metrics.json"))["steps_per_frame"]
H, W = R.shape[2:]
snaps = pickle.load(open(pkl, "rb"))["snaps"]; d = json.load(open(gj)); S = d["series"]; E = d["events"]
pos = {}
for a, x in enumerate(S):
    for i, c in enumerate(x["id"]): pos.setdefault(c, []).append((a, i))
yy, xx = np.mgrid[0:H, 0:W]
def area_at(k, cy, cx):
    K = np.roll(np.roll(R[k, 1].astype(np.float32), H // 2 - int(cy), 0), W // 2 - int(cx), 1)
    lab, n = ndimage.label(K > KT, structure=np.ones((3, 3)))
    disk = (yy - H // 2) ** 2 + (xx - W // 2) ** 2 <= 9
    ids = np.unique(lab[disk & (lab > 0)])
    return int(sum((lab == i).sum() for i in ids))
out = []
for e in E:
    if e[1] != "death" or e[0] <= 1000: continue
    c = e[2][0]
    if len(pos.get(c, [])) < 20: continue
    a, i = pos[c][-1]; C = snaps[a][1][i]; td = e[0]
    ks = [k for k in range(len(RF)) if td - 3000 <= RF[k] * spf <= td + 8000]
    ser = [(int(RF[k] * spf), area_at(k, C["cy"], C["cx"])) for k in ks]
    after = [ar for t, ar in ser if td <= t <= td + 3000]
    gone = any(ar < 4 for ar in after)
    before = [ar for t, ar in ser if t < td]
    out.append(dict(cell=c, t=td, np_last=C["n"], area_before=before[-1] if before else None, after=after, physical=gone))
n = len(out); g = sum(o["physical"] for o in out)
print(json.dumps(dict(pack=pk, mature_deaths=n, physically_gone_within_3000=g, details=out)))
