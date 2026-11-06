"""Certificate figures (labenv python). usage: python plot_certs.py WORLD [WORLD ...] -> results/certificates.png"""
import json
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

names = sys.argv[1:]
R = {n: json.load(open(f"results/{n}_certificates.json")) for n in names}
COL = {"persistence": "#888888", "ar1": "#000000", "ridge_p1": "#9ecae1", "ridge_p4": "#3182bd", "ridge_p8": "#08519c",
       "knn": "#e6550d", "mlp": "#31a354", "kinematic": "#756bb1", "kin+ridge_p4": "#c51b8a"}
fig, axs = plt.subplots(len(names), 5, figsize=(22, 4.3 * len(names)), squeeze=False)
for r, n in enumerate(names):
    res = R[n]
    for c, phi in enumerate(("coarse", "objects")):
        cl = res[f"closure_{phi}"]
        H = cl["horizons_ticks"]
        ax = axs[r, c]
        ax.plot(H, cl["V0_mean_predictor"], "k--", lw=1, label="unconditional mean (V0)")
        for nm, col in COL.items():
            if nm in cl["V"]:
                ax.plot(H, cl["V"][nm], color=col, lw=1.4, marker="o", ms=3, label=nm)
        ax.plot(H, cl["V_oracle"], "r-", lw=2.2, marker="s", ms=4, label="oracle: true simulator from h0")
        ax.set_xscale("log", base=2)
        ax.set_xticks(H)
        ax.set_xticklabels([str(h) for h in H])
        ax.set_xlabel("horizon (ticks of 20 steps)")
        ax.set_ylabel("standardised MSE per coordinate")
        ax.set_title(f"{n} / Phi_{phi} (n1={cl['n1']}, {cl['n_test_states']} states x {cl['replicates']} reps)",
                     fontsize=9)
        ax.set_ylim(0, max(1.6, max(cl["V"]["persistence"]) * 1.05))
        if r == 0 and c == 1:
            ax.legend(fontsize=7, frameon=False, ncol=2)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    ax = axs[r, 2]
    for phi, col in (("coarse", "#3182bd"), ("objects", "#c51b8a")):
        cl = res[f"closure_{phi}"]
        H = cl["horizons_ticks"]
        ax.errorbar(H, cl["ceiling"], yerr=cl["ceiling_se"], color=col, marker="o", ms=4, capsize=2,
                    label=f"ceiling c, Phi_{phi}")
        ax.errorbar(H, cl["depth_gain"], yerr=cl["depth_gain_se"], color=col, marker="^", ms=4, capsize=2,
                    ls="--", label=f"depth gain g, Phi_{phi}")
    ax.set_xscale("log", base=2)
    ax.set_xticks(H)
    ax.set_xticklabels([str(h) for h in H])
    ax.axhline(0.5, color="0.7", lw=0.8, ls=":")
    ax.set_ylim(-0.05, 1.05)
    ax.set_xlabel("horizon (ticks)")
    ax.set_title(f"{n}: closure ceiling c = (V0-Vbest)/(V0-Vu) and depth gain g = (Vbest-Vu)/V0", fontsize=8.5)
    ax.legend(fontsize=7, frameon=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for c, phi in ((3, "objects"), (4, "coarse")):
        ax = axs[r, c]
        rep = (res.get("inputs_replicated") or {}).get(phi, {})
        cols = plt.get_cmap("tab10")
        for k, (cn, v) in enumerate(rep.items()):
            H = [int(t) for t in v["twin_snr_median"]]
            ax.plot(H, list(v["twin_snr_median"].values()), color=cols(k), ls=":", lw=1.2)
            ms = np.maximum(np.array(list(v["mean_shift_snr_vs_oracle_spread_median"].values())), 1e-4)
            ax.plot(H, ms, color=cols(k), lw=1.8, marker="o", ms=3, label=cn)
        ax.set_xscale("log", base=2)
        ax.set_yscale("log")
        ax.set_ylim(1e-4, 5)
        ax.axhline(1, color="r", lw=0.8)
        ax.set_xlabel("ticks after the input starts")
        ax.set_ylabel("|response|^2 / oracle spread")
        ax.set_title(f"{n} / Phi_{phi}: input visibility (solid: mean shift over 6 noise\n"
                     "realisations; dotted: identical-noise twin difference)", fontsize=8.5)
        ax.legend(fontsize=7, frameon=False)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
plt.tight_layout()
fig.savefig("results/certificates.png", dpi=90)
print("ok")
