"""Kind (hole side) census over time from evo_track.py JSONs. usage: kindplot.py out.png trk1.json trk2.json ..."""
import sys, json, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
out, fs = sys.argv[1], sys.argv[2:]
fig, ax = plt.subplots(1, len(fs), figsize=(6 * len(fs), 3.8), squeeze=False)
groups = [("side 2-4", range(2, 5)), ("side 5-8", range(5, 9)), ("side 9-10", range(9, 11)), ("side 11 (founders)", [11]), ("side 12", [12]), ("side >=13", range(13, 40))]
for a, f in zip(ax[0], fs):
    r = json.load(open(f)); t = [c["t"] for c in r["census"]]
    for lab, ks in groups:
        y = [sum(n for k, n in zip(c["areas"], c["counts"]) if k in ks) for c in r["census"]]
        a.plot(np.array(t) / 1000, y, label=lab, lw=1.2 if "11" in lab else 0.8, color=dict(zip([g[0] for g in groups], ["tab:blue", "tab:orange", "tab:green", "black", "tab:purple", "tab:red"]))[lab])
    a.set_title(f"seed {r['seed']} (L={r['L']}): loops per kind"); a.set_xlabel("t (k steps)"); a.set_ylabel("loops")
ax[0][0].legend(fontsize=7)
plt.tight_layout(); plt.savefig(out, dpi=80)
