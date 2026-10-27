"""python share2.py : share of kind-b caps (label share <= 0.5) over time, seeds 0-5, b favoured (eps -0.1) vs the neutral
twin (eps 0, same mutation draws), both starting with every cap of kind a (m_s*_e*.json from heredity2.py)."""
import json, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 2, figsize=(11, 3.4), gridspec_kw={'width_ratios': [3, 1]})
diff = []
for s in (21, 22, 23):
    m = {}
    for e, c in (('-0.1', 'r'), ('0', 'k')):
        K = np.array(json.load(open(f'm_s{s}_e{e}.json'))['kind_counts_all'], float); sh = K[:, 2] / np.maximum(K[:, 1] + K[:, 2], 1)
        k = np.ones(9) / 9; ax[0].plot(K[4:-4, 0], np.convolve(sh, k, 'valid'), c, alpha=0.6, label=(f'b favoured (eps -0.1)' if e == '-0.1' else 'neutral twin (eps 0)') if s == 21 else None)
        m[e] = sh[(K[:, 0] >= 400) & (K[:, 0] <= 1200)].mean()
    diff.append((m['-0.1'], m['0']))
ax[0].set_xlabel('t'); ax[0].set_ylabel('share of kind-b caps (9-point mean)'); ax[0].legend(fontsize=8); ax[0].set_ylim(0, 1)
D = np.array(diff); ax[1].plot([0, 1], D.T, 'o-', color='grey'); ax[1].set_xticks([0, 1]); ax[1].set_xticklabels(['b favoured', 'neutral']); ax[1].set_title('mean b share, t=400-1200, per seed', fontsize=8); ax[1].set_ylim(0, 1)
plt.tight_layout(); plt.savefig('share_b.png', dpi=80); print(D.round(2))
