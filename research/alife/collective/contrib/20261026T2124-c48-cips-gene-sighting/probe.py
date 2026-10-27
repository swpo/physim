import sys, os, json, importlib.util, numpy as np
from scipy import ndimage
spec = importlib.util.spec_from_file_location("w", os.path.join(os.path.dirname(os.path.abspath(__file__)), "world.py"))
w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
seed, T, out = int(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
s = w.init(seed, w.META["size"]); snaps = []; k = 0
def bodies(s):
    lab, n = ndimage.label(s["e"] > 0.5); res = []
    for j in range(1, n + 1):
        m = lab == j
        if m.sum() >= 10: res.append((int(m.sum()), round(float(s["g1"][m].mean()), 3), round(float(s["g2"][m].mean()), 3)))
    return res
while s["t"] < T - 1e-9:
    w.step(s); k += 1
    if k % 5000 == 0:
        b = bodies(s); print(round(s["t"]), len(b), b[:20], flush=True); snaps.append((round(s["t"]), s["e"].copy(), s["g1"].copy(), s["g2"].copy()))
print("wash", s.get("wash_log"))
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
n = len(snaps); fig, ax = plt.subplots(3, n, figsize=(1.6 * n, 5), squeeze=False)
for j, (t, e, g1, g2) in enumerate(snaps):
    for r, (f, c) in enumerate([(e, "magma"), (g1, "viridis"), (g2, "viridis")]):
        ax[r, j].imshow(f, cmap=c, vmin=0, vmax=1); ax[r, j].axis("off")
    ax[0, j].set_title(f"t={t}", fontsize=7)
fig.tight_layout(); fig.savefig(out + ".png", dpi=60)
