"""Two-seed summary for world 1 (c40 layered CIPS cells): death kF vs ramp time, against the constant-supply bracket."""
import json, os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from loadlog import load, tracks

O = "/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/paperexp/supply-ramp"
SEEDS = [90, 91]
MK = {90: "o", 91: "D"}
CO = {90: "#1f77b4", 91: "#d62728"}


def get(sd, name):
    p = f"{O}/arms/s{sd}/{name}/log.jsonl"
    return load(p) if os.path.exists(p) else None


fig, ax = plt.subplots(1, 3, figsize=(15.5, 4.8))
res = {}
# (a) kF at each cell's death vs ramp duration
for sd in SEEDS:
    for T in (100, 1000, 4000, 8000):
        L = get(sd, f"R{T}")
        if L is None:
            continue
        _, recs, evs = L
        dk = np.array([e["kF"] for e in evs if e["ev"] == "death"])
        res[f"s{sd}_R{T}"] = {"n_deaths": int(dk.size), "kF_min": float(dk.min()), "kF_median": float(np.median(dk)), "kF_max": float(dk.max()),
                              "survivors_at_end": recs[-1]["n"]}
        jit = np.exp(np.random.default_rng(sd + T).uniform(-0.08, 0.08, dk.size)) * (1.06 if sd == 91 else 0.94)
        ax[0].plot(T * jit, dk, MK[sd], color=CO[sd], mfc="none", ms=5, alpha=0.8, label=f"seed {sd}" if T == 1000 else None)
ax[0].axhspan(0.025, 0.03, color="0.85", zorder=0, label="constant-supply bracket:\ndie at 0.025, survive at 0.03\n(abrupt step and slow approach)")
T = np.logspace(1.8, 4.0, 50)
ax[0].set_xscale("log"); ax[0].set_xlabel("ramp duration T (kF 0.2 -> 0 linearly)"); ax[0].set_ylabel("kF at which each cell dissolves")
ax[0].set_title("(a) death kF per cell vs ramp time", fontsize=9); ax[0].legend(fontsize=7, loc="lower right"); ax[0].set_ylim(-0.002, 0.04)

# (b) per-cell area vs current kF: slowest ramp lines, constant and hold medians
for sd in SEEDS:
    name = "R8000" if get(sd, "R8000") else "R4000"
    _, recs, _ = get(sd, name)
    for i, h in tracks(recs).items():
        ax[1].plot(h[:, 1], h[:, 2], color=CO[sd], lw=0.5, alpha=0.45)
    for f, k in (("C1", 0.2), ("C0.75", 0.15), ("C0.5", 0.1), ("C0.25", 0.05), ("C0.15", 0.03)):
        L = get(sd, f)
        late = [r for r in L[1] if r["t_rel"] >= L[1][-1]["t_rel"] - 500]
        a = np.concatenate([r["areas"] for r in late])
        ax[1].errorbar(k, np.median(a), yerr=[[np.median(a) - np.percentile(a, 25)], [np.percentile(a, 75) - np.median(a)]],
                       fmt="s", color="k", mfc=CO[sd], ms=6, capsize=3, label=f"step to constant kF, seed {sd}" if f == "C1" else None)
    L = get(sd, "H0.03")
    late = [r for r in L[1] if r["t_rel"] >= L[1][-1]["t_rel"] - 500]
    a = np.concatenate([r["areas"] for r in late])
    ax[1].plot(0.03, np.median(a), "^", color="k", mfc=CO[sd], ms=8, label=f"slow ramp then hold 0.03, seed {sd}")
    res[f"s{sd}_lines_from"] = name
ax[1].invert_xaxis(); ax[1].set_xlabel("current kF"); ax[1].set_ylabel("area of each cell (px, e>0.5)")
ax[1].set_title("(b) cell size tracks supply: slowest ramp (lines) vs steady states (markers)", fontsize=9); ax[1].legend(fontsize=6.5)

# (c) cell number: ramps vs steps vs holds, and the up-ramp
rows = []
for sd in SEEDS:
    for f, k in (("C0.15", 0.03), ("H0.03", 0.03), ("C0.125", 0.025), ("H0.025", 0.025), ("C0.1", 0.02)):
        L = get(sd, f)
        if L is None:
            continue
        _, recs, evs = L
        rows.append((sd, f, k, recs[0]["n"], max(r["n"] for r in recs), recs[-1]["n"], recs[-1]["t_rel"]))
labels = {"C0.15": "step 0.2->0.03", "H0.03": "slow ramp, hold 0.03", "C0.125": "step 0.2->0.025", "H0.025": "slow ramp, hold 0.025", "C0.1": "step 0.2->0.02"}
x = 0
for sd in SEEDS:
    for r in [r for r in rows if r[0] == sd]:
        ax[2].bar(x, r[4], color="0.85", edgecolor="k", width=0.8)
        ax[2].bar(x, r[5], color=CO[sd], width=0.5)
        ax[2].text(x, r[4] + 0.3, f"{r[4]}->{r[5]}", ha="center", fontsize=7)
        ax[2].text(x, -0.6, labels[r[1]], rotation=60, ha="right", va="top", fontsize=7)
        x += 1
    x += 0.6
ax[2].set_xticks([]); ax[2].set_ylabel("cells: most during arm (grey) and at end (colour)"); ax[2].set_ylim(-0.5, 19)
ax[2].set_title("(c) the threshold lies between 0.025 and 0.03 for both approaches", fontsize=9)
fig.tight_layout(rect=(0, 0.06, 1, 0.95))
fig.suptitle("c40 layered CIPS cells (seeds 90, 91; branched at t=6000): B-tipping in the fuel regrowth kF (default 0.2)", fontsize=10)
fig.savefig(f"{O}/fig_summary.png", dpi=85)
json.dump({"ramps": res, "threshold_arms": rows}, open(f"{O}/summary_threshold.json", "w"), indent=1)
print(json.dumps(res, indent=1)); print(rows)
