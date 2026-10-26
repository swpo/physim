"""c43 scan: run world.py for T at several WORLD_P settings (one seed) and draw |A| snapshots plus pulse counts.
usage: python scan.py OUT.png T SEED 'json list of overrides'"""
import sys, json, os, importlib.util, numpy as np
from scipy import ndimage
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
out, T, seed, sets = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]), json.loads(sys.argv[4])
here = os.path.dirname(os.path.abspath(__file__))
nsnap = 8; rows = []; logs = {}
for ov in sets:
    os.environ["WORLD_P"] = json.dumps(ov)
    spec = importlib.util.spec_from_file_location("w", os.path.join(here, "world.py")); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
    s = w.init(seed, w.META["size"]); n = int(T / w.P["dt"]); tt = set(np.linspace(0, n, nsnap).astype(int)); snaps = []; log = []
    for i in range(n + 1):
        if i in tt or i % 1000 == 0:
            a = np.abs(s["A"]); c = ndimage.label(a > 0.5)[1]
            if i % 1000 == 0: log.append((round(i * w.P["dt"]), int(c), float(a.max()), float(s["g"].mean())))
            if i in tt: snaps.append((i * w.P["dt"], a.copy(), c))
            if not np.isfinite(a).all(): break
        if i < n: w.step(s)
    rows.append((ov, snaps)); logs[json.dumps(ov)] = log; print(ov, log[-1], flush=True)
fig, ax = plt.subplots(len(rows), nsnap, figsize=(1.6 * nsnap, 1.75 * len(rows)), squeeze=False)
for r, (ov, snaps) in enumerate(rows):
    for j in range(nsnap):
        ax[r, j].axis("off")
        if j < len(snaps):
            t, a, c = snaps[j]; ax[r, j].imshow(a, cmap="inferno", vmin=0, vmax=2); ax[r, j].set_title(f"t={t:.0f} n={c}", fontsize=6)
    ax[r, 0].text(-5, 48, json.dumps(ov).replace(", ", "\n"), fontsize=5, ha="right", va="center")
fig.tight_layout(); fig.savefig(out, dpi=80)
json.dump(logs, open(out.replace(".png", ".json"), "w"), indent=0)
