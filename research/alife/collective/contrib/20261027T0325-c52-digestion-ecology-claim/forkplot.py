import json, sys, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt, numpy as np
fig, ax = plt.subplots(2, 2, figsize=(9, 5.5))
for s in (0, 1):
    for k, ls in (('fed', '-'), ('dfork', '--'), ('ffork', ':')):
        R = np.array(json.load(open(f'fork/{k}_s{s}.json'))['rows'])
        ax[0, s].plot(R[:, 0], R[:, 1], 'g' + ls, label=f'prey, {k}'); ax[0, s].plot(R[:, 0], R[:, 2], 'r' + ls, label=f'predators, {k}')
        ax[1, s].plot(R[:, 0], R[:, 8], 'r' + ls, label=f'max c_b, {k}'); ax[1, s].plot(R[:, 0], R[:, 3], 'g' + ls, label=f'mean c_a, {k}')
    for a in ax[:, s]: a.axvline(6000, color='k', lw=0.5); a.set_xlim(4000, 9000); a.set_xlabel('t')
    ax[0, s].set_title(f'seed {s}, 128^2: fed vs prey removed (dfork) vs fuel cut (ffork) at t=6000', fontsize=8)
ax[0, 0].legend(fontsize=6); ax[1, 0].legend(fontsize=6); ax[0, 0].set_ylabel('bodies'); ax[1, 0].set_ylabel('field')
plt.tight_layout(); plt.savefig('fork/forks.png', dpi=80)
