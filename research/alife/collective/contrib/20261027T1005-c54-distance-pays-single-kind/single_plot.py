"""(c54) Figure for the single-kind assay: per arm and seed, median path speed, median cycle and median D (own rod lengths per
cycle) of dividing rods, from spread_stats.py's json. usage: single_plot.py anadir out.png seed [seed ...]"""
import sys, json, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
A, png = sys.argv[1], sys.argv[2]; seeds = [int(x) for x in sys.argv[3:]]
arms = ["m40dep", "m60dep", "m40E", "m60E"]; col = ["C0", "C3", "C0", "C3"]; hat = ["", "", "//", "//"]
fig, ax = plt.subplots(1, 3, figsize=(12, 3.4))
for qi, (key, lab) in enumerate([("vpath", "path speed of dividing rods (px/t)"), ("cycle", "cycle (t)"), ("D", "D: own rod lengths per cycle")]):
    for si, s in enumerate(seeds):
        for ai, a in enumerate(arms):
            try: J = json.load(open(f"{A}/{a}_s{s}.json"))
            except FileNotFoundError: continue
            v = [d[key] for d in J["div"]]
            if not v: continue
            x = si * 5 + ai
            ax[qi].bar(x, np.median(v), color=col[ai], hatch=hat[ai], alpha=0.8, label=a if si == 0 else None)
            ax[qi].plot([x] * len(v), v, "k.", ms=3)
    ax[qi].set_xticks([si * 5 + 1.5 for si in range(len(seeds))]); ax[qi].set_xticklabels([f"seed {s}" for s in seeds]); ax[qi].set_title(lab, fontsize=9)
ax[2].axhline(3, ls=":", c="k"); ax[0].legend(fontsize=7)
fig.suptitle("c54: single-kind Marangoni populations (mar 40 blue, mar 60 red) with birth-site depletion (solid) and sink discs only (hatched)", fontsize=9)
fig.tight_layout(); fig.savefig(png, dpi=90)
