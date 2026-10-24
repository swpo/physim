"""Per-allele droplet counts over time from evidence-pack frames (ad5-style worlds).
python allele_plot.py out.png packA[:label] packB[:label] ...   (each pack dir holds seed*/frames.npz)
Droplet = periodic component of phi > 0; allele = argmax of mean catalyst channel (channels 2..)."""
import sys, json
from pathlib import Path
import numpy as np
from scipy import ndimage
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from labkit.metrics import periodic_label
COL = ["#4f8fff", "#3ccf5a", "#e8b923", "#e8403f"]
out, packs = sys.argv[1], sys.argv[2:]
seeds = sorted({p.name for pk in packs for p in Path(pk.split(":")[0]).glob("seed*")})
fig, axs = plt.subplots(len(packs), len(seeds), figsize=(4 * len(seeds), 3 * len(packs)), squeeze=False, sharey=True)
summary = {}
for i, pk in enumerate(packs):
    d, lab_ = (pk.split(":") + [Path(pk).name])[:2]
    for j, sd in enumerate(seeds):
        f = Path(d) / sd / "frames.npz"
        if not f.exists():
            continue
        z = np.load(f); R = z["render"].astype(np.float32); fr = z["render_f"]
        spf_dt = json.load(open(Path(d) / sd / "metrics.json")).get("dt_frame", 100.0) if (Path(d) / sd / "metrics.json").exists() else 100.0
        N = R.shape[1] - 2
        C = np.zeros((len(R), N), int)
        for t, F in enumerate(R):
            lab, n = periodic_label(F[0] > 0)
            if n == 0:
                continue
            m = np.stack([ndimage.mean(F[2 + k], lab, range(1, n + 1)) for k in range(N)])
            ok = m.max(0) > 0.05
            C[t] = np.bincount(m.argmax(0)[ok], minlength=N)
        ax = axs[i, j]
        for k in range(N):
            ax.plot(fr * spf_dt, C[:, k], color=COL[k % 4], lw=2, label=f"allele {k}")
        ax.set_title(f"{lab_} {sd}"); ax.set_xlabel("time")
        summary[f"{lab_}/{sd}"] = {"start": C[0].tolist(), "end": C[-1].tolist()}
axs[0, 0].set_ylabel("droplets"); axs[0, 0].legend(fontsize=7)
fig.tight_layout(); fig.savefig(out, dpi=80)
print(json.dumps(summary))
