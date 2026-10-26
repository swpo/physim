"""Figure for the complex-world contest rules: python fig.py (reads runs/*.json and calibrated.json)."""
import os, json, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
HERE = os.path.dirname(os.path.abspath(__file__))
cal = json.load(open(f"{HERE}/calibrated.json"))
R = [("neu", "neutral twin (P = 1/2)", "k"), ("tr", "transitive f_A/(f_A+f_B)", "C0"), ("zs", "zero-sum hash h(A,B)", "C3"), ("feat", "correlated feature contest", "C2")]
fig, ax = plt.subplots(1, 3, figsize=(17, 4.6)); tb = np.arange(20) * 1000 + 500
for tag, lab, c in R:
    for s in range(3):
        m = cal[f"{tag}_s{s}"]; r = json.load(open(f"{HERE}/runs/{tag}_s{s}.json"))
        rate = 1000 * np.array(m["sig"][:19]) / np.maximum(1, np.array(m["births"][:19]))
        ax[0].plot(tb[:19], rate + 1e-3, c=c, lw=1, label=lab if s == 0 else None)
        ax[1].plot(np.arange(1, 21) * 1000, r["topshare"], c=c, lw=1, label=lab if s == 0 else None)
        ax[2].plot(np.arange(1, 21) * 1000, r["msize"], c=c, lw=1)
ax[0].axhline(1.0, c="k", ls=":", lw=1); ax[0].set_yscale("log")
ax[0].set_title("kinds born per 1000-step window whose replications within 1000 steps\nreach the neutral twin's 99.9th percentile, per 1000 births (neutral = 1 by construction)", fontsize=9)
ax[1].set_title("share of complexes held by the commonest kind"); ax[1].legend(fontsize=8)
ax[2].set_title("mean complex size (members; cap 16)")
for a in ax: a.set_xlabel("step")
plt.tight_layout(); plt.savefig(f"{HERE}/contests.png", dpi=72)
