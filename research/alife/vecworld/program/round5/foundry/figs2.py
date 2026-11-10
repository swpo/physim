"""figs2 -- charts of job 2 (CPU, seconds): results/fig/enrichment.png, late_types.png.

    python -B figs2.py [--out results]

enrichment.png  yield of every target in the control arm, the enriched arm and as predicted from job 1
                (a dumbbell per target on a log axis; values printed)
late_types.png  where the worlds of each early type are at ticks 2000-2240 (stacked shares per early type)
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import numpy as np  # noqa: E402

import figs as F  # noqa: E402


def enrichment(a2, out):
    plt = F._mpl()
    e = a2["enrich"]
    names = ["structured", "active", "movers", "closure_gate", "candidate"]
    labels = ["structured", "active", "movers", "closure gate", "candidate (all gates)"]
    en, co, pr = e["arms"]["enriched"]["yields"], e["arms"]["control"]["yields"], e["prediction_from_job1"]["predicted_yield"]
    fig, ax = plt.subplots(figsize=(7.6, 4.3))
    y = np.arange(len(names))[::-1]
    for yi, n in zip(y, names):
        c, o, p = max(co[n]["frac"], 1e-4), en[n]["frac"], pr[n]
        ax.plot([c, o], [yi, yi], color="#b9b8b2", lw=2, zorder=1)
        ax.scatter([c], [yi], s=70, color=F.ORANGE, edgecolor=F.SURF, lw=1.2, zorder=3)
        ax.scatter([o], [yi], s=70, color=F.BLUE, edgecolor=F.SURF, lw=1.2, zorder=3)
        ax.scatter([p], [yi], s=70, marker="D", facecolor="none", edgecolor=F.AQUA, lw=1.8, zorder=4)
        ax.text(c, yi + 0.26, f"{100 * co[n]['frac']:.1f}%", ha="center", color=F.INK, fontsize=8.5)
        ax.text(o, yi + 0.26, f"{100 * o:.1f}%", ha="center", color=F.INK, fontsize=8.5)
    ax.scatter([], [], s=70, color=F.ORANGE, label=f"control arm ({e['arms']['control']['n']} random draws from the unselected 90.6%)")
    ax.scatter([], [], s=70, color=F.BLUE, label=f"enriched arm ({e['arms']['enriched']['n']} draws, the best 9.4% by weights)")
    ax.scatter([], [], s=70, marker="D", facecolor="none", edgecolor=F.AQUA, lw=1.8, label="predicted from job 1 before the run")
    ax.set_xscale("log")
    ax.set_xlim(0.004, 1.6)
    ax.set_xticks([0.01, 0.03, 0.1, 0.3, 1.0], ["1%", "3%", "10%", "30%", "100%"])
    ax.set_yticks(y, labels)
    ax.set_ylim(-0.6, len(names) - 0.3)
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("share of draws (log scale)")
    ax.set_title("Draws chosen by their weights alone against the rest", loc="left")
    ax.legend(frameon=False, fontsize=8.5, loc="upper center", bbox_to_anchor=(0.45, -0.2), ncol=1)
    fig.tight_layout()
    p = os.path.join(out, "enrichment.png")
    fig.savefig(p, dpi=140, bbox_inches="tight")
    plt.close(fig)
    return p


def late_types(a2, out):
    plt = F._mpl()
    tr = a2["late"]["transitions"]
    rows = [r for r in ("uniform", "frozen", "active:field", "active:bodies", "active:movers") if r in tr]
    groups = [("uniform", ["uniform"], F.AQUA), ("frozen", ["frozen"], F.ORANGE),
              ("active", ["active:field", "active:bodies", "active:movers"], F.BLUE)]
    fig, ax = plt.subplots(figsize=(7.2, 0.5 * len(rows) + 1.5))
    y = np.arange(len(rows))[::-1]
    for yi, r in zip(y, rows):
        tot = sum(tr[r].values())
        left = 0.0
        for gname, members, col in groups:
            v = sum(tr[r].get(m, 0) for m in members) / tot
            if v > 0:
                ax.barh(yi, v, left=left, height=0.56, color=col, edgecolor=F.SURF, lw=2)
                if v > 0.06:
                    ax.text(left + v / 2, yi, f"{100 * v:.0f}%", ha="center", va="center", color=F.INK, fontsize=9)
            left += v
        ax.text(1.01, yi, f"n = {tot}", va="center", color=F.INK2, fontsize=8.5)
    from matplotlib.patches import Patch
    handles = [Patch(facecolor=col, edgecolor=F.SURF, label=f"{gname} at ticks 2000-2240") for gname, members, col in groups]
    ax.set_yticks(y, [f"{r} early" for r in rows])
    ax.set_xlim(0, 1.12)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0], ["0", "25%", "50%", "75%", "100%"])
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("share of the worlds of that early type (ticks 50-290)")
    ax.set_title("Is the type a transient? The same worlds 2000 ticks later", loc="left")
    ax.legend(handles=handles, frameon=False, fontsize=8.5, loc="upper center", bbox_to_anchor=(0.45, -0.32), ncol=3)
    fig.tight_layout()
    p = os.path.join(out, "late_types.png")
    fig.savefig(p, dpi=140, bbox_inches="tight")
    plt.close(fig)
    return p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(HERE, "results"))
    a = ap.parse_args()
    a2 = json.load(open(os.path.join(a.out, "analysis_r2.json")))
    fd = os.path.join(a.out, "fig")
    made = {}
    if "enrich" in a2:
        made["enrichment"] = os.path.relpath(enrichment(a2, fd), a.out)
    if "late" in a2:
        made["late_types"] = os.path.relpath(late_types(a2, fd), a.out)
    fj = os.path.join(a.out, "figs.json")
    allf = json.load(open(fj)) if os.path.exists(fj) else {}
    allf.update(made)
    json.dump(allf, open(fj, "w"), indent=1)
    print(made)


if __name__ == "__main__":
    main()
