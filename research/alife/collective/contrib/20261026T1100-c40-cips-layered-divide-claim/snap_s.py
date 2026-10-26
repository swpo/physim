"""e and s fields side by side over a run of world_s.py; also the share of s production inside bodies (e>0.5).
usage: python snap_s.py WORLD SEED T OUT"""
import sys, os, json, importlib.util, numpy as np
from scipy import ndimage
wf, seed, T, out = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
spec = importlib.util.spec_from_file_location("w", wf); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
s = w.init(seed, w.META["size"]); q = s["par"]
snaps, share = [], []
k = 0; every = int(round(T / 12 / q["dt"]))
while s["t"] < T - 1e-9:
    if k % every == 0:
        snaps.append((round(s["t"]), s["e"].copy(), s["s"].copy()))
    if k % 1000 == 0 and s["t"] > 1000:
        cat = q["kc"] * s["F"] * np.clip(s["e"], 0, None) ** q["n"] * (1 - s["p"])
        m = s["e"] > 0.5
        # bodies plus a 3 px halo (the rim where s sits)
        mh = ndimage.binary_dilation(m, iterations=3)
        share.append((round(s["t"]), float(cat[m].sum() / cat.sum()), float(cat[mh].sum() / cat.sum()), float(s["s"][mh].sum() / s["s"].sum())))
    w.step(s); k += 1
snaps.append((round(s["t"]), s["e"].copy(), s["s"].copy()))
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
n = len(snaps); fig, ax = plt.subplots(2, n, figsize=(1.5 * n, 3.3))
smax = max(x[2].max() for x in snaps[1:])
for j, (t, e, sv) in enumerate(snaps):
    ax[0, j].imshow(e, cmap="magma", vmin=0, vmax=1); ax[0, j].set_title(f"e t={t}", fontsize=6)
    ax[1, j].imshow(sv, cmap="viridis", vmin=0, vmax=smax); ax[1, j].set_title(f"s t={t}", fontsize=6)
    ax[0, j].axis("off"); ax[1, j].axis("off")
fig.suptitle(f"{os.path.basename(wf)} seed {seed} {os.environ.get('WORLD_P','')}: enzyme e (top), amphiphile s (bottom, 0..{smax:.2f})", fontsize=7)
fig.tight_layout(); fig.savefig(out + ".png", dpi=90)
np.save(out + "_final.npy", np.stack([s["e"], s["s"]]))
json.dump({"columns": ["t", "cat share in bodies e>0.5", "cat share in bodies+3px", "s share in bodies+3px"], "rows": share}, open(out + "_share.json", "w"))
print(share[::3], share[-1])
