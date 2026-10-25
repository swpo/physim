"""Run the world to t0, keep only the window around one body (u and a), reset the rest to rest state, and follow it alone.
usage: isolate.py world.py seed t0 T out.png [which: bump|bar]"""
import sys, json, os, importlib.util, numpy as np
from scipy import ndimage
def plabel(z):
    lab, n = ndimage.label(z)
    par = np.arange(n + 1)
    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]; a = par[a]
        return a
    for a, b in [(lab[0], lab[-1]), (lab[:, 0], lab[:, -1])]:
        m = (a > 0) & (b > 0)
        for x, y in set(zip(a[m].tolist(), b[m].tolist())):
            rx, ry = find(x), find(y)
            if rx != ry: par[ry] = rx
    roots = np.array([find(i) for i in range(n + 1)])
    lab = roots[lab]; u = np.unique(lab[lab > 0]); return lab, u
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
over = json.loads(os.environ.get("ISO_P", "{}"))
spec = importlib.util.spec_from_file_location("w", sys.argv[1]); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
w.P.update(over)
seed, t0, T, out = int(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), sys.argv[5]; which = sys.argv[6] if len(sys.argv) > 6 else "bump"
s = w.init(seed, w.META["size"])
for i in range(int(t0 / w.P["dt"])): s = w.step(s)
fu = w.f(s["u"]); lab, k = ndimage.label(fu > 0.5); sz = ndimage.sum(fu > 0.5, lab, range(1, k + 1))
order = np.argsort(sz)
j = (order[len(order) // 2] if which == "bump" else order[-1]) + 1
m = ndimage.binary_dilation(lab == j, iterations=10)
s["u"] = np.where(m, s["u"], 0.0); s["a"] = np.where(m, s["a"], 0.0)
n = int(T / w.P["dt"]); snaps = np.linspace(0, n, 12).astype(int); imgs = []; log = []
for i in range(n + 1):
    if i in snaps:
        fu = w.f(s["u"]); lab, ids = plabel(fu > 0.5); sz = ndimage.sum(fu > 0.5, lab, ids) if len(ids) else []
        imgs.append((round(i * w.P["dt"]), fu.copy())); log.append((round(i * w.P["dt"]), [int(z) for z in sz if z >= 6]))
    if i < n: s = w.step(s)
np.save(out.replace(".png", ".npy"), np.array([im for t, im in imgs], dtype=np.float16))
fig, ax = plt.subplots(1, len(imgs), figsize=(1.6 * len(imgs), 1.9))
for a, (t, im) in zip(ax, imgs): a.imshow(im, vmin=0, vmax=1, cmap="magma"); a.set_title(f"+{t}", fontsize=7); a.axis("off")
fig.suptitle(f"seed {seed}: one {which} isolated at t={t0}, then {over}", fontsize=7); plt.tight_layout(); plt.savefig(out, dpi=70)
print(over, seed, which, log, flush=True)
