"""Nucleation test for the claimed world from different initial fields (construction lens, S).
usage: WORLD_P='{...}' python nuc.py SEED T OUTPREFIX
Runs the claim's world.py unchanged (parameters via WORLD_P, read by the world itself), logs the number of
bodies (e>0.5, >=10 px, periodic-merged), body area and max e every 100 t, and saves 6 snapshots."""
import sys, os, json, importlib.util
import numpy as np
from scipy import ndimage

CLAIM = "/home/user/physim/research/alife/collective/contrib/20261026T1100-c40-cips-layered-divide-claim/world.py"
spec = importlib.util.spec_from_file_location("w", CLAIM)
w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
seed, T, out = int(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
s = w.init(seed, w.META["size"])
e0 = s["e"].copy()
log, snaps = [], []
k = 0
dt = s["par"]["dt"]
while s["t"] <= T + 1e-9:
    if k % int(round(100 / dt)) == 0:
        lab, n = ndimage.label(s["e"] > 0.5)
        sizes = ndimage.sum(np.ones_like(s["e"]), lab, range(1, n + 1)) if n else []
        log.append({"t": round(s["t"]), "n": int(sum(1 for a in sizes if a >= 10)), "area": int((s["e"] > 0.5).sum()),
                    "max_e": float(s["e"].max()), "std_e": float(s["e"].std())})
    if k % int(round(T / 5 / dt)) == 0:
        snaps.append((round(s["t"]), s["e"].copy()))
    w.step(s); k += 1
json.dump({"seed": seed, "WORLD_P": os.environ.get("WORLD_P", ""), "init_std": float(e0.std()), "init_max": float(e0.max()),
           "log": log}, open(out + ".json", "w"), indent=0)
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, len(snaps), figsize=(2.0 * len(snaps), 2.3))
for j, (t, e) in enumerate(snaps):
    ax[j].imshow(e, cmap="magma", vmin=0, vmax=1 if j else None); ax[j].axis("off"); ax[j].set_title(f"t={t} max={e.max():.2f}", fontsize=7)
fig.suptitle(f"seed {seed} WORLD_P={os.environ.get('WORLD_P', '')}", fontsize=7)
fig.tight_layout(); fig.savefig(out + ".png", dpi=70)
print(log[0], log[len(log) // 2], log[-1])
