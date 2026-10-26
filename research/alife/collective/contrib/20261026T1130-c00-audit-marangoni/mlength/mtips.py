"""For the top dividing tracks: displacement of the rear and front tips along the net direction (growth-free bound:
the rear tip advances only if the body translates), the steps with their area changes around the largest step, and
whether a sub-min_area fragment touches the body at that step. usage: mtips.py frames.npz world.py [K=20] [ntop=8]"""
import sys, importlib.util, numpy as np
sys.path.insert(0, "/home/user/physim/research/alife")
from labkit import run as LR, metrics as M
F = np.load(sys.argv[1]); mat = F["matter"].astype(np.float32)
spec = importlib.util.spec_from_file_location("w", sys.argv[2]); W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
K = int(sys.argv[3]) if len(sys.argv) > 3 else 20; ntop = int(sys.argv[4]) if len(sys.argv) > 4 else 8
mn, thr, lo, hi = LR._normalize_matter(mat, W.META, True, W.META.get("threshold")); H, Wd = mn.shape[1:]
comps, links = LR._segment_frames(mn, thr, LR._default_min_area(H, Wd), True)
tracks, ev = M.track(comps, links, (H, Wd), True); byid = {t["id"]: t for t in tracks}
out = []
for t in tracks:
    kids = [c for c in t["children"] if byid[c]["birth"] == "split" and byid[c]["end"] - byid[c]["start"] + 1 >= K]
    n = len(t["cy"])
    if len(kids) < 2 or n < 5: continue
    sy = M._wrap(np.diff(t["cy"]), H); sx = M._wrap(np.diff(t["cx"]), Wd)
    cy = np.concatenate([[0], np.cumsum(sy)]); cx = np.concatenate([[0], np.cumsum(sx)])  # unwrapped centroid path
    net = np.hypot(cy[-1], cx[-1]); u = np.array([cy[-1], cx[-1]]) / max(net, 1e-9)
    size = np.sqrt(np.mean(t["area"]))
    rear, front, fer = [], [], []
    for k in range(n):
        m = comps[t["start"] + k]["lab"] == t["comp"][k] + 1
        ys, xs = np.nonzero(m)
        dy = M._wrap(ys - t["cy"][k], H); dx = M._wrap(xs - t["cx"][k], Wd)
        p = (cy[k] + dy) * u[0] + (cx[k] + dx) * u[1]
        rear.append(p.min()); front.append(p.max())
        C = np.cov(np.vstack([dy, dx])); lam, vec = np.linalg.eigh(C); v = vec[:, -1]; q = dy * v[0] + dx * v[1]
        fer.append(q.max() - q.min() + 1)
    st = np.hypot(sy, sx); ar = np.array(t["area"], float)
    j = int(np.argmax(st))
    out.append((net / size, t["id"], n, net, np.median(fer), rear[-1] - rear[0], front[-1] - front[0], j, st[j], np.median(st), ar[j], ar[j + 1]))
out.sort(key=lambda r: -r[0])
print(sys.argv[1])
print(" id life net Fmed | rear_adv front_adv | rear_adv/Fmed | maxstep@k (median) area before->after")
for r in out[:ntop]:
    bl, tid, n, net, fm, ra, fa, j, smax, smed, a0, a1 = r
    print(f" {tid} {n} {net:.1f} {fm:.1f} | {ra:.1f} {fa:.1f} | {ra / fm:.2f} | {smax:.2f}@{j} ({smed:.2f}) {a0:.0f}->{a1:.0f}")
