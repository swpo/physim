"""Summary of the coevbits O test: late cohort novelty (a* = 99.9th pct of the twin's early activity) real vs twin, per seed."""
import json, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
N = json.load(open("data/b10_vs_b10N_twincal_lc10000.json")); S = json.load(open("data/b10_vs_b10S_twincal_lc10000.json"))
L = json.load(open("data/b10L_vs_b10LN_twincal_lc10000.json")) if __import__("os").path.exists("data/b10L_vs_b10LN_twincal_lc10000.json") else None
fig, ax = plt.subplots(1, 3, figsize=(16, 4.5)); rows = []
for j, (nm, col) in enumerate((("pred", "tab:red"), ("prey", "tab:blue"))):
    for k, (D, lab) in enumerate(((N, "neutral twin (constant capture)"), (S, "shuffled twin (random predator's genotype)"))):
        for s in range(6):
            r = D[f"s{s}_{nm}_q99.9"]; x = s + (k - 0.5) * 0.35
            ax[j].bar(x, r["late_real"], 0.17, color=col, alpha=1.0 if k == 0 else 0.6)
            ax[j].bar(x + 0.17, r["late_twin"], 0.17, color="0.5" if k == 0 else "0.75")
            rows.append((nm, lab, s, r["late_real"], r["late_twin"], round(r["astar"])))
    ax[j].set_xticks(range(6)); ax[j].set_xlabel("seed"); ax[j].set_title(f"{nm}: late (t>=20k) new genotypes with early activity >= twin's 99.9 pct\n"
                                                                        "pairs: real|neutral twin (left), real|shuffled twin (right)", fontsize=8)
if L:
    for nm, col in (("pred", "tab:red"), ("prey", "tab:blue")):
        r = L[f"s0_{nm}_q99.9"]; c = np.cumsum(r["sig"]); ct = np.cumsum(r["twin_sig"]); x = np.arange(len(c)) * 10000
        ax[2].plot(x, c, color=col, label=f"{nm} real"); ax[2].plot(x, ct, ":", color=col, label=f"{nm} neutral twin")
    ax[2].set_title("700k-step run, seed 0: cumulative significant new genotypes", fontsize=8); ax[2].legend(fontsize=7); ax[2].set_xlabel("t")
fig.tight_layout(); fig.savefig("data/b10_summary.png", dpi=85)
for r in rows: print(r)
