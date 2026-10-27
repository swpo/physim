import json, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
runs = [('A_sel', 'selective s0'), ('A_sel_s1', 'selective s1'), ('A_neu', 'neutral s0'), ('A_neu_s1', 'neutral s1'), ('A_nomut', 'selective, no mutation s0')]
fig, ax = plt.subplots(2, 3, figsize=(13, 6)); ax = ax.ravel()
for k, (n, lab) in enumerate(runs):
    R = np.array(json.load(open(f'gro/{n}.json'))['rows']); m = R[:, 0] >= 2000
    a = ax[k]; a.plot(R[m, 0], R[m, 3], 'g', label='prey bodies'); a.plot(R[m, 0], R[m, 4], 'r', label='kind b bodies'); a.plot(R[m, 0], R[m, 5], 'b', label='kind e bodies')
    a.set_title(lab, fontsize=8); a.set_xlabel('t')
    ax[5].plot(R[m, 0], R[m, 2] / np.maximum(R[m, 1], 1e-9), label=lab)
ax[0].legend(fontsize=6); ax[5].set_yscale('log'); ax[5].set_ylabel('total material e / b'); ax[5].legend(fontsize=6); ax[5].axhline(1, color='gray', lw=0.5)
plt.suptitle('world2g: predator material made from digested prey (yield 0.5) and decaying in solution (5e-4); e hunts (taxis 0.5), b has none in the selective arms', fontsize=8)
plt.tight_layout(); plt.savefig('gro/turnover.png', dpi=75)
