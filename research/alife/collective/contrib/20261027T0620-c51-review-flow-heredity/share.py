"""python share.py : share of label-a caps over time (every 50 t from t=205) for eps 0, +0.1, -0.1, seeds 0-5 (h_s*_e*.json)."""
import json, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 3, figsize=(12, 3.2), sharey=True)
for k, (e, c) in enumerate((('0', 'k'), ('0.1', 'r'), ('-0.1', 'b'))):
    for s in range(6):
        r = json.load(open(f'h_s{s}_e{e}.json')); K = np.array(r['kind_counts_a_b'], float)
        ax[k].plot(K[:, 0], K[:, 1] / np.maximum(K[:, 1] + K[:, 2], 1), c, alpha=0.7)
    ax[k].set_title(f'eps = {e} (heat yield Q(1+eps(a-b)))', fontsize=9); ax[k].set_xlabel('t'); ax[k].set_ylim(-0.02, 1.02)
ax[0].set_ylabel('share of caps with label a'); plt.tight_layout(); plt.savefig('share.png', dpi=80)
