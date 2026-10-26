import os, sys, json, importlib.util, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from scipy import ndimage as ndi
runs = json.loads(sys.argv[1]); nsteps = int(sys.argv[2]); tag = sys.argv[3]
fig, ax = plt.subplots(len(runs), 4, figsize=(12, 3*len(runs)))
ax = np.atleast_2d(ax)
for i, wp in enumerate(runs):
    os.environ["WORLD_P"] = json.dumps(wp)
    spec = importlib.util.spec_from_file_location("w%d" % i, "world.py"); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
    s = w.init(0, w.META["size"])
    cents = []
    for j in range(4):
        for _ in range(nsteps // 4): s = w.step(s)
        u = s["u"]; lab, n = ndi.label(ndi.gaussian_filter(u, 1.5) > 0.4)
        ax[i, j].imshow(u, cmap="magma", vmin=-0.5, vmax=1.5); ax[i, j].set_title("%s t=%.0f n=%d max=%.2f" % (json.dumps(wp)[:40], s["t"], n, u.max()), fontsize=7); ax[i, j].axis("off")
        cents.append(ndi.center_of_mass(u > 0.4))
    print(wp, "n", n, "umax %.2f" % u.max(), "frac %.3f" % (u > 0.4).mean(), flush=True)
plt.tight_layout(); plt.savefig("probe_%s.png" % tag, dpi=70)
