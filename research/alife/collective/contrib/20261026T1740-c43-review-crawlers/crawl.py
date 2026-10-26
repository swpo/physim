"""c43: follow one crawler in a labkit frames.npz (matter channel > 0.5) from frame F0, linking to the component
whose periodic centroid is nearest the previous one; stop at any area jump > 25% (merge or split).
The field is rolled to put the previous centroid at the box centre before labelling.
Reports net displacement in sqrt(area) and in the long-axis length (the body moves broadside, protocol unit sqrt(area)).
usage: python crawl.py frames.npz T_total F0 Y0 X0 OUT.json"""
import sys, json, numpy as np
from scipy import ndimage
M = np.load(sys.argv[1])["matter"]; T = float(sys.argv[2]); f0 = int(sys.argv[3]); y0, x0 = float(sys.argv[4]), float(sys.argv[5])
n, H, W = M.shape; dtf = T / (n - 1)
def wrap(d, P): return (d + P / 2) % P - P / 2
def comps(f):
    lab, k = ndimage.label(f > 0.5); out = []
    for i in range(1, k + 1):
        yy, xx = np.nonzero(lab == i)
        cy = (np.angle(np.exp(2j*np.pi*yy/H).mean())*H/(2*np.pi)) % H; cx = (np.angle(np.exp(2j*np.pi*xx/W).mean())*W/(2*np.pi)) % W
        dy, dx = wrap(yy-cy, H), wrap(xx-cx, W); ev = np.linalg.eigvalsh(np.cov(np.stack([dy, dx])))
        out.append((cy, cx, len(yy), 4*np.sqrt(ev[-1])))
    return out
py, px = y0, x0; path = [(0.0, 0.0)]; rows = []; prev_a = None
for t in range(f0, n):
    sy, sx = int(round(H/2 - py)), int(round(W/2 - px))
    c = comps(np.roll(M[t], (sy, sx), (0, 1)))   # crawler re-centred so it never straddles the periodic edge
    c = [((b[0]-sy) % H, (b[1]-sx) % W, b[2], b[3]) for b in c]
    d, j = min((np.hypot(wrap(b[0]-py, H), wrap(b[1]-px, W)), j) for j, b in enumerate(c))
    b = c[j]
    if prev_a is not None and abs(b[2]/prev_a - 1) > 0.25: rows.append({"stop": round(t*dtf, 2), "reason": "area jump", "area": b[2], "prev": prev_a}); break
    if t > f0: path.append((path[-1][0]+wrap(b[0]-py, H), path[-1][1]+wrap(b[1]-px, W)))
    py, px, prev_a = b[0], b[1], b[2]; rows.append({"t": round(t*dtf, 2), "area": b[2], "long_axis": round(b[3], 1)})
p = np.array(path); net = float(np.hypot(*(p[-1]-p[0]))); sa = float(np.sqrt(np.median([r["area"] for r in rows if "area" in r and "t" in r])))
la = float(np.median([r["long_axis"] for r in rows if "long_axis" in r]))
res = {"start_t": round(f0*dtf, 2), "end_t": rows[-1].get("t", rows[-1].get("stop")), "net_px": net, "sqrt_area_px": sa, "long_axis_px": la,
       "net_sqrt_area": net/sa, "net_long_axis": net/la, "rows": rows}
json.dump(res, open(sys.argv[6], "w"), indent=0); print({k: v for k, v in res.items() if k != "rows"})
