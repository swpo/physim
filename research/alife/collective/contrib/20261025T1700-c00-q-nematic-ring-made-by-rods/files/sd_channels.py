import sys, numpy as np
from scipy import ndimage
F = np.load(sys.argv[1]); R = F["render"].astype(np.float32); rf = list(F["render_f"])
H, W = R.shape[2:]; nch = R.shape[1]
acc = {k: np.zeros(nch) for k in ("rim", "core", "out")}; cnt = {k: 0 for k in acc}
for k, f in enumerate(rf):
    if f < 20: continue
    phi = R[k, 0]; ins = phi > 0
    t = np.tile(ins, (3, 3)); sl = (slice(H, 2*H), slice(W, 2*W))
    d = np.where(t, -(ndimage.distance_transform_edt(t) - 0.5), ndimage.distance_transform_edt(~t) - 0.5)[sl]
    for name, m in (("rim", np.abs(d) <= 0.5), ("core", d <= -1.5), ("out", (d >= 2) & (d <= 4))):
        acc[name] += [R[k, c][m].sum() for c in range(nch)]; cnt[name] += m.sum()
print("render frames used:", sum(1 for f in rf if f >= 20), "channels", nch)
for c in range(2, nch):
    r, co, o = acc["rim"][c]/cnt["rim"], acc["core"][c]/cnt["core"], acc["out"][c]/cnt["out"]
    print(f"ch{c}: rim {r:.4f} core {co:.4f} out {o:.4f}  rim/core {r/co:.2f} rim/out {r/o:.2f}")
