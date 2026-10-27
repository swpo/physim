"""share of kind-b caps over time, seeds 32-36, both arms (heredity2.py output in heredity/)."""
import json, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt, os
h = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'heredity')
fig, ax = plt.subplots(1, 2, figsize=(11, 3.4), gridspec_kw={'width_ratios': [3, 1]})
for arm, col in [('sel', 'tab:red'), ('neu', 'k')]:
    ms = []
    for s in range(32, 37):
        d = json.load(open(f'{h}/h_{arm}{s}.json')); c = np.array(d['kind_counts_all'], float)
        sh = c[:, 2] / np.maximum(c[:, 1] + c[:, 2], 1); sm = np.convolve(sh, np.ones(9) / 9, 'same')
        ax[0].plot(c[4:-4, 0], sm[4:-4], color=col, alpha=0.6, label=('b favoured (eps -0.1)' if arm == 'sel' else 'neutral twin (eps 0)') if s == 32 else None)
        ms.append(sh[c[:, 0] >= 400].mean())
        if s == 32: ax[0].text(c[-1, 0], sm[-5], ' s32', color=col, fontsize=7)
    ax[1].plot([0 if arm == 'sel' else 1] * 5, ms, 'o', color=col)
ax[0].set_xlabel('t'); ax[0].set_ylabel('share of kind-b caps (9-pt mean)'); ax[0].legend(fontsize=8); ax[0].set_ylim(0, 1)
ax[1].set_xticks([0, 1]); ax[1].set_xticklabels(['favoured', 'neutral']); ax[1].set_ylim(0, 1); ax[1].set_title('mean b share t>=400, seeds 32-36', fontsize=8)
plt.tight_layout(); plt.savefig(os.path.join(os.path.dirname(h), 'share_b_c55.png'), dpi=90)
