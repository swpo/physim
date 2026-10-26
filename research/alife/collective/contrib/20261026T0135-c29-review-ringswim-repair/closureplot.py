"""(c29) Plot ring closure and area of cut vs twin over the first 1000 steps, for every front/ring arm in the given result.json files."""
import sys, json
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
files = sys.argv[2:]; out = sys.argv[1]
rows = [(f, c) for f in files for c in json.load(open(f))["cells"]]
fig, axs = plt.subplots(2, len(rows), figsize=(2.6 * len(rows), 4.6), squeeze=False)
for j, (f, c) in enumerate(rows):
    for a, col in (("twin", "k"), ("cut", "r")):
        tr = [r for r in c["tracks"][a] if r[0] <= 1000]
        axs[0, j].plot([r[0] for r in tr], [r[6] if r[6] is not None else float("nan") for r in tr], col, label=a)
        axs[1, j].plot([r[0] for r in tr], [r[1] for r in tr], col)
    tag = f.split("/")[-2] + (" keepS" if c["damage"].get("keep_S") else "")
    axs[0, j].set_title(f"{tag} cell {c['cell']} {c['mode']}", fontsize=7); axs[0, j].set_ylim(0, 1.05)
    axs[1, j].set_xlabel("steps after damage", fontsize=7)
axs[0, 0].set_ylabel("ring closure (share of wall with L>0.15)", fontsize=7); axs[1, 0].set_ylabel("area (px)", fontsize=7)
axs[0, 0].legend(fontsize=7); fig.tight_layout(); fig.savefig(out, dpi=70)
