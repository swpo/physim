"""Branch test for repair on the LARGEST rod (c11's untested case): run world to t0, pick the largest
body (phi > 0), copy the state, erase an end cap of FRAC of its area (along its principal axis, plus
a 1 px rim) in one copy with the world's damage(), and run both copies for T more time. The tracked
body = all components overlapping the previous tracked mask (dilated 2 px), so daughters count as
pieces. Prints area(t)/area(t0) and piece counts for both arms and saves crops centred on the tracked body (periodic mean).
usage: bigcut.py world.py seed t0 frac T out.png [rank]"""
import sys, copy, importlib.util, numpy as np
from scipy import ndimage
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
spec = importlib.util.spec_from_file_location("w", sys.argv[1]); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
seed, t0, frac, T, out = int(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]), sys.argv[6]
rank = int(sys.argv[7]) if len(sys.argv) > 7 else 0
dt = w.P["dt"]; s = w.init(seed, w.META["size"])
for _ in range(int(round(t0 / dt))): s = w.step(s)
lab, n = ndimage.label(s["phi"] > 0); sizes = ndimage.sum(np.ones_like(s["phi"]), lab, range(1, n + 1))
med = float(np.median(sizes)); j = int(np.argsort(sizes)[::-1][rank]) + 1; body = lab == j
ys, xs = np.nonzero(body); cy, cx = ys.mean(), xs.mean()
cov = np.cov(np.vstack([ys - cy, xs - cx])); ev, evec = np.linalg.eigh(cov); ax_ = evec[:, -1]
proj = (ys - cy) * ax_[0] + (xs - cx) * ax_[1]; cut = proj >= np.quantile(proj, 1 - frac)
mask = np.zeros_like(body); mask[ys[cut], xs[cut]] = True; mask = ndimage.binary_dilation(mask, iterations=1)
print(f"seed {seed} t0 {t0}: target area {body.sum()} px = {body.sum() / med:.2f}x median ({n} bodies), aspect {np.sqrt(ev[-1] / max(ev[0], 1e-9)):.2f}; erased {(mask & body).sum()} px of it ({(mask & body).sum() / body.sum():.0%})")
a = copy.deepcopy(s); b = copy.deepcopy(s); b = w.damage(b, mask)
arms = {"undamaged": [a, body.copy(), []], "cut": [b, body.copy(), []]}
H, W = body.shape; rec = int(round(10 / dt)); snaps = {k: [] for k in arms}
for i in range(int(round(T / dt)) + 1):
    if i % rec == 0:
        for k, (st, m, hist) in arms.items():
            lb, nn = ndimage.label(st["phi"] > 0); ids = np.unique(lb[ndimage.binary_dilation(m, iterations=2) & (lb > 0)])
            m2 = np.isin(lb, ids) if len(ids) else np.zeros_like(m); arms[k][1] = m2
            hist.append((round(i * dt, 1), int(m2.sum()), len(ids)))
            if i % (rec * 4) == 0:
                yy, xx = np.nonzero(m2) if m2.any() else (np.array([cy]), np.array([cx]))
                ty = np.angle(np.exp(2j * np.pi * yy / H).mean()) * H / (2 * np.pi) % H; tx = np.angle(np.exp(2j * np.pi * xx / W).mean()) * W / (2 * np.pi) % W
                snaps[k].append((round(i * dt), np.roll(np.roll(st["phi"], H // 2 - int(ty), 0), W // 2 - int(tx), 1)[H // 2 - 24:H // 2 + 24, W // 2 - 24:W // 2 + 24]))
    if i < int(round(T / dt)):
        for k in arms: arms[k][0] = w.step(arms[k][0])
a0 = body.sum()
for k, (st, m, hist) in arms.items():
    print(k, "t, area/area0, pieces:", [(t, round(ar / a0, 2), p) for t, ar, p in hist])
fig, axs = plt.subplots(2, len(snaps["cut"]), figsize=(1.6 * len(snaps["cut"]), 3.6), squeeze=False)
for r, k in enumerate(["undamaged", "cut"]):
    for c, (t, img) in enumerate(snaps[k]):
        axs[r, c].imshow(img, cmap="gray", vmin=-1.1, vmax=1.1); axs[r, c].axis("off"); axs[r, c].set_title(f"{k} +{t}", fontsize=7)
plt.suptitle(f"seed {seed}: largest rod at t={t0}, end cap {frac:.0%} erased (phi=-1, Q=0, s=0) vs undamaged twin", fontsize=8)
plt.tight_layout(); plt.savefig(out, dpi=80)
