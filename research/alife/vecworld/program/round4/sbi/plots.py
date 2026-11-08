"""plots -- two figures from results/summary.json (study sbi, round 4).

fig_identification.png  posterior sd / prior sd per parameter vs Lab budget (episodes, ticks), and the
                        fraction of truths inside the marginal 50 / 90 % intervals.
fig_prediction.png      oracle-normalised fair energy skill vs budget: real@n and post@n per predictor
                        class, with true, prior predictive and box-centre references.
usage: python -B plots.py [summary.json] [outdir]
"""
import json
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SUMF = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "results", "summary.json")
OUTD = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "results")
S = json.load(open(SUMF))
names = S["truths"]["names"]
idt = S["identification"]["per_budget"]
bud = sorted(int(n) for n in idt)
x = np.array(bud)

fig, ax = plt.subplots(1, 2, figsize=(10, 3.8))
C = np.array([idt[str(n)]["contraction_sd_ratio_mean"] for n in bud])
for j, nm in enumerate(names):
    ax[0].plot(x, C[:, j], "o-", label=nm)
ax[0].set_xscale("log", base=2)
ax[0].set_xlabel("Lab budget (episodes of 33 ticks)")
ax[0].set_ylabel("posterior sd / prior sd (mean over truths)")
ax[0].set_ylim(0, 1.1)
ax[0].axhline(1, color="0.7", lw=0.8)
ax[0].legend(fontsize=8)
ax[0].set_title("contraction")
for key, lab, ref in (("in50_frac", "in 50% interval", 0.5), ("in90_frac", "in 90% interval", 0.9)):
    ax[1].plot(x, [idt[str(n)][key] for n in bud], "o-", label=lab)
    ax[1].axhline(ref, color="0.7", lw=0.8, ls="--")
ax[1].plot(x, [idt[str(n)]["hpd_le_90_frac"] for n in bud], "s:", label="joint 90% HPD")
ax[1].set_xscale("log", base=2)
ax[1].set_ylim(0, 1.05)
ax[1].set_xlabel("Lab budget (episodes)")
ax[1].set_ylabel("fraction of truths x params")
ax[1].legend(fontsize=8)
ax[1].set_title(f"coverage ({len(S['truths']['theta'])} truths)")
fig.tight_layout()
fig.savefig(os.path.join(OUTD, "fig_identification.png"), dpi=110)

tab = S["prediction"]["table"]
oes = S["prediction"]["oes"]
fig, ax = plt.subplots(1, len(tab), figsize=(5 * len(tab), 3.8), squeeze=False)
for k, (cl, t) in enumerate(tab.items()):
    a = ax[0, k]
    for kind, sty in (("real", "o-"), ("post", "s-")):
        xs = [n for n in bud if f"n{n}" in t and kind in t[f"n{n}"]]
        if xs:
            ys = [t[f"n{n}"][kind] for n in xs]
            es = [oes[f"{cl}|{kind}@{n}"]["se"] for n in xs]
            a.errorbar(xs, ys, yerr=es, fmt=sty, capsize=2, label=f"{kind}@n")
    for ref, col in (("true", "k"), ("prior_pred", "tab:green"), ("prior_mean", "tab:red")):
        if ref in t:
            a.axhline(t[ref], color=col, ls="--", lw=1, label=ref)
    a.set_xscale("log", base=2)
    a.set_xlabel("Lab budget (episodes)")
    a.set_ylabel("OES (oracle 1, climatology 0)")
    a.set_title(f"{cl}")
    vals = [v for row in t.values() if isinstance(row, dict) for kk, v in row.items() if kk in ("real", "post")]
    vals += [v for v in t.values() if isinstance(v, (int, float))]
    a.set_ylim(max(min(0.0, min(vals)) - 0.05, -1.2), max(vals) + 0.08)
    a.legend(fontsize=8, loc="lower right")
fig.tight_layout()
fig.savefig(os.path.join(OUTD, "fig_prediction.png"), dpi=110)
print("ok")
