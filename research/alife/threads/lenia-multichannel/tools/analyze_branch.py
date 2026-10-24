"""Summarize branch_test.py outputs: paired S vs N per branch point, whole vs old operator, plus a plot.

python analyze_branch.py BT_DIR OUT_PNG OUT_JSON
"""
import glob
import json
import re
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

d = sys.argv[1]
runs = {}
for f in glob.glob(d + "/*.json"):
    m = re.match(r".*/(whole|old)_e([0-9.]+)_s(\d)_t(\d+)\.json", f)
    if not m:
        continue
    op, e, sd, t = m.group(1), float(m.group(2)), int(m.group(3)), int(m.group(4))
    runs[(op, e > 0, sd, t)] = json.load(open(f))
rows = []
for (op, sel, sd, t), r in sorted(runs.items()):
    se = r["series"]
    mixed = sum(x["mixed"] for x in se)
    bearing = sum(x["mixed"] + x["carriers"] for x in se)
    rows.append(dict(op=op, arm="S" if sel else "N", point=f"s{sd}_t{t}", flipped=r["flipped_mass_fraction"],
                     frac1_0=se[0]["frac1"], frac1_end=se[-1]["frac1"], pure1_end=se[-1]["pure1"],
                     pure1_max=max(x["pure1"] for x in se), lost=se[-1]["frac1"] < 1e-3,
                     leak=mixed / max(bearing, 1), n_end=se[-1]["n"]))
json.dump(rows, open(sys.argv[3], "w"), indent=1)
print(f"{'op':5} {'pt':10} {'flip':>5} {'f0':>6} {'S_end':>6} {'N_end':>6} {'S_pure1':>7} {'N_pure1':>7} {'leakS':>5} {'leakN':>5}")
for op in ("whole", "old"):
    pts = sorted({r["point"] for r in rows if r["op"] == op})
    wins = 0; npair = 0
    for p in pts:
        S = [r for r in rows if r["op"] == op and r["point"] == p and r["arm"] == "S"]
        N = [r for r in rows if r["op"] == op and r["point"] == p and r["arm"] == "N"]
        if not (S and N):
            continue
        S, N = S[0], N[0]
        npair += 1; wins += S["frac1_end"] > N["frac1_end"]
        print(f"{op:5} {p:10} {S['flipped']:5.2f} {S['frac1_0']:6.3f} {S['frac1_end']:6.3f} {N['frac1_end']:6.3f} "
              f"{S['pure1_end']:7d} {N['pure1_end']:7d} {S['leak']:5.2f} {N['leak']:5.2f}")
    print(f"  {op}: S > N in {wins}/{npair} paired branch points")
fig, ax = plt.subplots(1, 2, figsize=(12, 3.8), sharey=True)
for i, op in enumerate(("whole", "old")):
    for (o, sel, sd, t), r in runs.items():
        if o != op:
            continue
        se = r["series"]
        ax[i].plot([x["t"] for x in se], [x["frac1"] for x in se], color="#d95f02" if sel else "#7570b3", alpha=0.7, lw=1.2)
    ax[i].set_title(f"{op}-body flip: allele-1 mass fraction (orange S, purple N)" if op == "whole" else
                    "old operator (A0 component + 4 px): allele-1 mass fraction", fontsize=10)
    ax[i].set_xlabel("steps after the flip"); ax[i].grid(alpha=0.3)
fig.tight_layout(); fig.savefig(sys.argv[2], dpi=90)
