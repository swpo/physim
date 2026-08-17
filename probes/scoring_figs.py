
import numpy as np, json, base64, io
import matplotlib.pyplot as plt

def b64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=110, bbox_inches="tight")
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode()

out = {}

# ---- fig 1: proper scoring on bimodal truth ----
import sys
sys.path.insert(0, "environments/physim")
from physim.session import crps_accuracy, QLEVELS
rng = np.random.default_rng(3)
truth = np.concatenate([rng.normal(-0.62, 0.05, 24), rng.normal(0.55, 0.06, 16)])
scale = 0.3
ans = {
    "point at the mean": {"mean": float(truth.mean())},
    "point at a mode": {"mean": -0.62},
    "honest quantiles": {"mean": float(truth.mean()),
        "quantiles": {str(p): float(np.quantile(truth, p)) for p in QLEVELS}},
}
fig, axes = plt.subplots(1, 2, figsize=(9.4, 3.0), gridspec_kw={"width_ratios": [1.15, 1]})
ax = axes[0]
ax.hist(truth, bins=24, color="#9ecae1", edgecolor="white", label="truth ensemble (40 clones)")
colors = {"point at the mean": "#cf222e", "point at a mode": "#e69f00", "honest quantiles": "#1a7f37"}
for k, a in ans.items():
    sc = crps_accuracy(list(truth), scale, a)["accuracy_crps"]
    if "quantiles" in a:
        for i, (p, q) in enumerate(a["quantiles"].items()):
            ax.axvline(float(q), color=colors[k], lw=1.4, alpha=0.85,
                       label=f"{k} → score {sc:.2f}" if i == 0 else None)
    else:
        ax.axvline(a["mean"], color=colors[k], lw=2.2, ls="--", label=f"{k} → score {sc:.2f}")
ax.legend(fontsize=7, loc="upper center")
ax.set_title("a bimodal contract: e.g. 'which species wins' differs across clones", fontsize=8.5)
ax.set_xlabel("contract statistic"); ax.set_yticks([])
ax = axes[1]
xs = np.linspace(-1.1, 1.1, 300)
emp = np.searchsorted(np.sort(truth), xs) / len(truth)
ax.plot(xs, emp, color="#9ecae1", lw=2.5, label="truth CDF")
qs = ans["honest quantiles"]["quantiles"]
ax.step([-1.1] + [float(v) for v in qs.values()] + [1.1],
        [0] + list(np.array([float(p) for p in qs.keys()])) + [1],
        where="post", color="#1a7f37", lw=1.6, label="quantile answer CDF")
ax.axvline(truth.mean(), color="#cf222e", ls="--", lw=1.6, label="point answer (step CDF at mean)")
ax.set_title("CRPS = area between answer CDF and truth CDF²", fontsize=8.5)
ax.legend(fontsize=7); ax.set_xlabel("value"); ax.set_ylabel("P(Y ≤ v)")
fig.suptitle("Why distributional answers: a proper score makes honest structure the best strategy",
             fontsize=10, y=1.05)
out["crps_bimodal"] = b64(fig)

# ---- fig 2: the reference ladder on B2 (numbers from the CRPS battery + frontier re-runs) ----
rows = [
    ("null", 0.317, "#bbb"), ("tail", 0.416, "#bbb"),
    ("frontier: gpt-5.2 (points)", 0.373, "#e69f00"),
    ("frontier: fable (quantiles)", 0.53, "#e69f00"),
    ("compact oracle, point answers", 0.917, "#4c78a8"),
    ("compact oracle + honest spread", 0.975, "#1a7f37"),
]
fig, ax = plt.subplots(figsize=(7.6, 2.7))
y = np.arange(len(rows))
ax.barh(y, [r[1] for r in rows], color=[r[2] for r in rows], height=0.62)
ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rows], fontsize=8)
for yi, r in zip(y, rows):
    ax.text(r[1] + 0.012, yi, f"{r[1]:.2f}", va="center", fontsize=8)
ax.set_xlim(0, 1.05); ax.invert_yaxis()
ax.axvline(1.0, color="#ddd", lw=1)
ax.set_xlabel("prediction accuracy (CRPS-based)", fontsize=8)
ax.set_title("the reference ladder on one world (B2, seed 0): the frontier gap is the benchmark's "
             "headroom", fontsize=9)
out["ladder_b2"] = b64(fig)

# ---- fig 3: adequacy decomposition from the real report ----
rep = json.load(open("/tmp/adequacy_report.json"))
fig, axes = plt.subplots(1, 3, figsize=(9.6, 2.7))
for ax, world in zip(axes, ("B2", "C4", "D2")):
    tbl = rep[world]
    A = [max(r["A"], 1e-2) for r in tbl]
    gap = [r["gap"] for r in tbl]
    ax.scatter(A, gap, s=26, color="#4c78a8")
    ax.set_xscale("log")
    ax.set_xlabel("adequacy ratio A (log)", fontsize=8)
    ax.set_title(world, fontsize=9)
    ax.set_ylim(-0.05, 1.0)
axes[0].set_ylabel("CRPS gap: instance-aware − climatology", fontsize=8)
fig.suptitle("the audit: contracts whose truth depends on the instance (A≫1) are exactly those "
             "where knowing YOUR instance pays (Spearman ρ = 1.00 / sat. / 0.90)", fontsize=9, y=1.06)
out["adequacy"] = b64(fig)

import pathlib, base64 as B
for k, v in out.items():
    pathlib.Path("docs/assets/scoring_%s.png" % k).write_bytes(B.b64decode(v))
print("figs:", {k: len(v)//1024 for k, v in out.items()}, "KB")
