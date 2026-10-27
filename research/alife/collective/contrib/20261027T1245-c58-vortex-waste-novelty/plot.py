"""c58: plot vortex trait over time, favoured vs identical-draw twin. python plot.py out.png sel1.json neu1.json [sel2 neu2 ...]"""
import sys, json, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
out = sys.argv[1]; fs = sys.argv[2:]; n = len(fs) // 2
fig, ax = plt.subplots(n, 1, figsize=(9, 3.2 * n), squeeze=False)
for i in range(n):
    for f, col, lab in ((fs[2 * i], 'C3', 'favoured'), (fs[2 * i + 1], 'C0', 'neutral twin')):
        r = json.load(open(f)); dm = 0.4
        if 'traits_by_frame' in r:
            for t, th in r['traits_by_frame'][::2]:
                ax[i, 0].scatter([t] * len(th), th, s=2, c=col, alpha=0.25, lw=0)
        p = np.array(r['pop_t_n_mean_std_domclass_domshare_min_max'], float)
        ax[i, 0].plot(p[:, 0], p[:, 2], col, lw=2, label=f"{lab} ({r['WORLD_P']}) mean trait")
        ax[i, 0].plot(p[:, 0], p[:, 4] * dm, col, lw=1, ls='--', label=f"{lab} dominant class x dm")
    ax[i, 0].set_ylabel('vortex trait theta'); ax[i, 0].set_title(f"seed {r['seed']}"); ax[i, 0].legend(fontsize=7, loc='upper left')
ax[-1, 0].set_xlabel('t'); fig.tight_layout(); fig.savefig(out, dpi=90)
