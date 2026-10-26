import sys, json, numpy as np
sys.path.insert(0, "/home/user/physim/research/alife")
from labkit import run as LR, metrics as M
p = sys.argv[1]
F = np.load(p + "/frames.npz"); print(F.files)
mat = F["matter"].astype(np.float32)
meta = json.load(open(p + "/metrics.json")).get("meta", {}) if False else {}
mn, thr, lo, hi = LR._normalize_matter(mat, meta, True, None); H, Wd = mn.shape[1:]
comps, links = LR._segment_frames(mn, thr, LR._default_min_area(H, Wd), True)
fs = []
for f in range(len(comps) // 5, len(comps), 3):
    for j in range(len(comps[f]["area"])):
        m = comps[f]["lab"] == j + 1; ys, xs = np.nonzero(m)
        dy = M._wrap(ys - comps[f]["cy"][j], H); dx = M._wrap(xs - comps[f]["cx"][j], Wd)
        lam, vec = np.linalg.eigh(np.cov(np.vstack([dy, dx]))); v = vec[:, -1]; q = dy * v[0] + dx * v[1]; w = vec[:, 0]; r = dy * w[0] + dx * w[1]
        fs.append(((q.max() - q.min() + 1), (r.max() - r.min() + 1), np.sqrt(len(ys))))
fs = np.array(fs); print("median long axis, short axis, sqrt(area):", np.median(fs, 0).round(1), " long/sqrt(area):", round(float(np.median(fs[:, 0] / fs[:, 2])), 2))
