"""c43 screen: run world.py to T for several WORLD_P settings (one seed); count prey (c_a>0.5) and consumer (q>0.5)
bodies every 100 t and draw prey (green) / consumer (red) snapshots.
usage: python scan.py OUT.png T SEED 'json list of overrides'"""
import sys, json, os, importlib.util, numpy as np
from scipy import ndimage
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
out, T, seed, sets = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]), json.loads(sys.argv[4])
here = os.path.dirname(os.path.abspath(__file__)); nsnap = 8; rows = []; logs = {}
for ov in sets:
    os.environ["WORLD_P"] = json.dumps(ov)
    spec = importlib.util.spec_from_file_location("w", os.path.join(here, "world.py")); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
    s = w.init(seed, w.META["size"]); dt = w.P["dt"]; n = int(T / dt); ev = int(100 / dt)
    tt = set(np.linspace(0, n, nsnap).astype(int)); snaps = []; log = []
    for i in range(n + 1):
        if i % ev == 0 or i in tt:
            F = w.fields(s)
            if i % ev == 0:
                log.append((round(i * dt), int(ndimage.label(F[0] > 0.5)[1]), int(ndimage.label(F[1] > 0.5)[1]), float(F[1].max()), float(F[0].mean())))
                if not np.isfinite(F).all(): print("NaN", ov); break
            if i in tt: snaps.append((i * dt, F[0].copy(), F[1].copy()))
        if i < n: w.step(s)
    rows.append((ov, snaps, log)); logs[json.dumps(ov)] = log; print(ov, log[-1], flush=True)
fig, ax = plt.subplots(len(rows), nsnap, figsize=(1.6 * nsnap, 1.8 * len(rows)), squeeze=False)
for r_, (ov, snaps, log) in enumerate(rows):
    for j in range(nsnap):
        ax[r_, j].axis("off")
        if j < len(snaps):
            t, a, q = snaps[j]; img = np.stack([np.clip(q, 0, 1), np.clip(a, 0, 1), np.zeros_like(a)], -1)
            ax[r_, j].imshow(img); ax[r_, j].set_title(f"t={t:.0f} prey {int(ndimage.label(a>0.5)[1])} cons {int(ndimage.label(q>0.5)[1])}", fontsize=5)
    ax[r_, 0].text(-5, 64, json.dumps(ov).replace(", ", "\n"), fontsize=5, ha="right", va="center")
fig.tight_layout(); fig.savefig(out, dpi=80); json.dump(logs, open(out.replace(".png", ".json"), "w"), indent=0)
