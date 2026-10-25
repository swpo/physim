"""Kind (hole side) composition over time for several tracked runs: stacked fractions + population size."""
import json, sys, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
files = sys.argv[1:-1]; out = sys.argv[-1]
kinds = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
cols = plt.cm.tab20(np.linspace(0, 1, len(kinds) + 1))
fig, axes = plt.subplots(len(files), 1, figsize=(10, 2.6 * len(files)), squeeze=False)
for ax, f in zip(axes[:, 0], files):
    r = json.load(open(f)); C = r["census"]; t = np.array([c["t"] for c in C])
    M = np.zeros((len(kinds) + 1, len(C)))
    for j, c in enumerate(C):
        for a, n in zip(c["areas"], c["counts"]):
            M[kinds.index(a) if a in kinds else len(kinds), j] += n
    N = M.sum(0); F = M / np.maximum(N, 1)
    ax.stackplot(t, F, colors=cols, labels=[f"side {k}" for k in kinds] + ["other"])
    ax2 = ax.twinx(); ax2.plot(t, N, 'k-', lw=1); ax2.set_ylabel('loops (black)')
    ax.set_xlim(t[0], t[-1]); ax.set_ylim(0, 1); ax.set_ylabel('kind fraction')
    ax.set_title(f"{f}: rule {r['params'].get('rule', 'Evoloop.rule')}, founder m={r['params'].get('m', 15)}, seed {r['seed']}, {r['L']}^2", fontsize=9)
axes[0, 0].legend(ncol=7, fontsize=7, loc='upper center', bbox_to_anchor=(0.5, 1.45))
axes[-1, 0].set_xlabel('time step'); plt.tight_layout(); plt.savefig(out, dpi=75)
