"""Summarise invade.py outputs: fraction of loops of the invader's kind (side m-4) vs time, planted vs unplanted twin."""
import json, glob, sys, os
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
d = sys.argv[1]
def frac(c, ks):
    n = sum(c.values()); return (sum(v for k, v in c.items() if int(k) in ks) / n) if n else float("nan")
fig, ax = plt.subplots(1, 2, figsize=(12, 4.2)); rows = []
for j, (m, ks, lab) in enumerate([(8, {2, 3, 4}, "side<=4 (invader side 4)"), (16, {12}, "side 12 (invader side 12)")]):
    for f in sorted(glob.glob(f"{d}/inv_m{m}_b*.json")):
        r = json.load(open(f))
        if "skipped" in r: rows.append(f"m={m} base {r['base']}: skipped ({r['skipped']})"); continue
        tw = r["twin"]; t = [x[0] for x in tw]
        ax[j].plot(t, [frac(x[1], ks) for x in tw], "k-", lw=2, alpha=0.6)
        ends = []
        for rep in r["reps"]:
            if not rep.get("planted"): continue
            ax[j].plot([x[0] for x in rep["census"]], [frac(x[1], ks) for x in rep["census"]], lw=1)
            ends.append(frac(rep["census"][-1][1], ks))
        n0 = sum(r["census_t0"].values())
        rows.append(f"m={m} base {r['base']}: loops at t0 {n0}; twin final {lab} {frac(tw[-1][1], ks):.2f} (loops {sum(tw[-1][1].values())}); planted finals " + ", ".join(f"{e:.2f}" for e in ends))
    ax[j].set_title(f"{lab}: planted (colour) vs unplanted twin (black)", fontsize=9); ax[j].set_xlabel("step"); ax[j].set_ylabel("fraction of loops"); ax[j].set_ylim(0, 1)
plt.tight_layout(); plt.savefig(f"{d}/invasion.png", dpi=80)
open(f"{d}/invasion_summary.txt", "w").write("\n".join(rows) + "\n"); print("\n".join(rows))
