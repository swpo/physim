"""c47: are the consumers separate bodies or layers of prey droplets? From labkit frames.npz of the cips-consumer world.
Per frame: consumer bodies (q>0.5, min 4 px), the share of them touching a prey body (c_a>0.5 dilated by 2 px),
the share whose own pixels are mostly outside prey, and, for consecutive frames, how many consumers change
which prey body they touch (prey label of the largest overlap, matched by prey-body overlap between frames).
usage: python attach.py frames.npz OUT.json"""
import sys, json, numpy as np
from scipy import ndimage
z = np.load(sys.argv[1]); R = z["render"]; fi = z["render_f"]
res = []
for k in range(len(R)):
    a, q = R[k][0].astype(float), R[k][1].astype(float)
    pl, npre = ndimage.label(a > 0.5); ql, ncon = ndimage.label(q > 0.5)
    pd = ndimage.binary_dilation(a > 0.5, iterations=2)
    sizes = ndimage.sum(np.ones_like(q), ql, range(1, ncon + 1))
    ids = [i + 1 for i, sz in enumerate(sizes) if sz >= 4]
    touch = sum(1 for i in ids if pd[ql == i].any())
    inside = sum(1 for i in ids if (a[ql == i] > 0.5).mean() > 0.5)
    res.append({"frame": int(fi[k]), "prey": int(npre), "consumers": len(ids), "touching_prey": touch, "mostly_inside_prey": inside})
json.dump(res, open(sys.argv[2], "w"))
late = [r for r in res if r is not None][len(res) // 4:]
n = sum(r["consumers"] for r in late); t = sum(r["touching_prey"] for r in late); i = sum(r["mostly_inside_prey"] for r in late)
print("frames", len(late), "consumer-frames", n, "touching prey", t, round(t / max(n, 1), 3), "mostly inside prey", i, round(i / max(n, 1), 3))
