"""figs -- study foundryexam: two figures from results/analysis.json (CPU, seconds).

    python -B figs.py [--analysis results/analysis.json] [--out results]

fig_budget.png   per arm: pooled oracle-normalised skill of every policy against the Lab budget (S, FT, D, Dr as
                 curves; C, P0, P0s, persistence as levels), seed-mean, with the 90% interval of C and P0.
fig_worlds.png   per arm: every hidden world's skill of C against P0, and the state-given loss against sigma.
"""
from __future__ import annotations

import argparse
import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
TITLE = {"P": "arm P: screened prior (all 250 numbers hidden)", "N30": "arm N30: neighbourhood, eps = 0.3",
         "N10": "arm N10: neighbourhood, eps = 0.1"}
COL = {"S": "#1f77b4", "FT": "#2ca02c", "D": "#d62728", "Dr": "#9467bd"}
LAB = {"S": "S(N): amortised inference", "FT": "FT(N): P0 fine-tuned", "D": "D(N): data only, net", "Dr": "Dr(N): data only, ridge"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--analysis", default=os.path.join(HERE, "results", "analysis.json"))
    ap.add_argument("--out", default=os.path.join(HERE, "results"))
    a = ap.parse_args()
    A = json.load(open(a.analysis))
    arms = [x for x in ("P", "N30", "N10") if x in A["arms"]]
    fig, axs = plt.subplots(1, len(arms), figsize=(5.2 * len(arms), 4.2), squeeze=False)
    for ax, arm in zip(axs[0], arms):
        R = A["arms"][arm]
        T = R["table"]
        for fam, c in COL.items():
            cv = R["budgets"]["curves"].get(fam)
            if cv:
                x = [max(n, 1) for n in cv["N"]]
                ax.plot(x, cv["oes_pooled"], "o-", color=c, label=LAB[fam], ms=4)
        for b, ls, col in (("C", "-", "k"), ("P0", "--", "k"), ("P0s", ":", "k"), ("Kp", "-.", "gray")):
            if b in T:
                q = T[b]["oes_pooled"]
                ax.axhline(q["value"], ls=ls, color=col, lw=1.2,
                           label={"C": "C: true weights", "P0": "P0: prior simulations, own history",
                                  "P0s": "P0s: prior simulations, 2 frames", "Kp": "persistence"}[b])
                if b in ("C", "P0"):
                    ax.axhspan(q["p05"], q["p95"], color=col, alpha=0.07)
        ax.set_xscale("log", base=2)
        ax.set_xlabel("Lab episodes N (S at N = 0 is drawn at 1)")
        ax.set_ylabel("pooled skill, climatology 0 to oracle 1")
        ax.set_title(f"{TITLE[arm]}\n{R['n_hidden']} hidden worlds", fontsize=9)
        lo = min([T[b]["oes_pooled"]["value"] for b in ("Kp", "P0s", "P0") if b in T] + [0.0])
        ax.set_ylim(max(lo - 0.15, -0.5), 1.0)
        ax.grid(alpha=0.3)
    axs[0][0].legend(fontsize=7, loc="lower right")
    fig.tight_layout()
    fig.savefig(os.path.join(a.out, "fig_budget.png"), dpi=110)
    plt.close(fig)

    fig, axs = plt.subplots(1, 2, figsize=(10, 4.2))
    mk = {"P": "o", "N30": "s", "N10": "^"}
    for arm in arms:
        pw = A["arms"][arm]["per_world"]
        if "oes_C" in pw and "oes_P0" in pw:
            axs[0].scatter(pw["oes_P0"], pw["oes_C"], marker=mk[arm], label=f"arm {arm}", alpha=0.8)
        if "oes_plugPrior" in pw:
            axs[1].scatter(1.0 - np.array(pw["oes_plugPrior"]), pw["sigma"], marker=mk[arm], label=f"arm {arm}", alpha=0.8)
    lim = axs[0].get_xlim()
    axs[0].plot(lim, lim, "k:", lw=1)
    axs[0].set_xlabel("P0: skill per hidden world")
    axs[0].set_ylabel("C: skill per hidden world")
    axs[0].set_title("no-experiment policy against the true-weight net", fontsize=9)
    axs[1].axhline(0.15, color="r", lw=1, ls="--")
    axs[1].set_xscale("symlog", linthresh=0.1)
    axs[1].set_xlabel("state-given loss: 1 - skill of the simulator with a prior draw of the weights")
    axs[1].set_ylabel("science share sigma per hidden world")
    axs[1].set_title("round 5's screen against sigma (bar 0.15 dashed)", fontsize=9)
    for ax in axs:
        ax.grid(alpha=0.3)
        ax.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(os.path.join(a.out, "fig_worlds.png"), dpi=110)
    print("wrote fig_budget.png, fig_worlds.png")


if __name__ == "__main__":
    main()
