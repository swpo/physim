"""Mean yield vs inert marker (particle-weighted) over time, and death percentiles, for genealogy files."""
import sys, json, numpy as np, subprocess
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
fs = sys.argv[1:-1]; out = sys.argv[-1]
fig, ax = plt.subplots(1, 2, figsize=(11, 3.6))
for k, fn in enumerate(fs):
    d = json.load(open(fn)); S = [x for x in d["series"] if x["n"]]
    t = [x["t"] for x in S]
    ax[0].plot(t, [np.average(x["ym"], weights=x["np"]) for x in S], color=f"C{k}", lw=1, label=f"yield, seed {k}")
    ax[0].plot(t, [np.average(x["zm"], weights=x["np"]) for x in S], color=f"C{k}", lw=1, ls=":")
    for j, key in enumerate(("ym", "zm")):
        r = json.loads(subprocess.check_output([sys.executable, "deathsel.py", fn, key, "20"]))
        ax[1].bar(k * 3 + j, r["death_pct_mean"], color=f"C{k}", alpha=1 if j == 0 else 0.35)
ax[0].set_xlabel("t"); ax[0].set_ylabel("mean trait (solid yield, dotted marker)"); ax[0].legend(fontsize=7)
ax[1].set_xticks([k * 3 + 0.5 for k in range(len(fs))]); ax[1].set_xticklabels([f"seed {k}" for k in range(len(fs))])
ax[1].axhline(0.5, color="k", lw=0.5); ax[1].set_ylabel("mature-cell deaths: mean percentile\n(dark yield, light marker)")
fig.suptitle("pcell-mwall: heritable link efficiency vs identical-event inert marker (intrinsic deaths only)", fontsize=9)
fig.tight_layout(); fig.savefig(out, dpi=90)
