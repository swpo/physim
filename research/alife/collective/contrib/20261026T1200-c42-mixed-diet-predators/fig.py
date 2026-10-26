import json, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
def L(f): d = json.load(open(f + '.json')); return np.array(d['rows'])
fig, ax = plt.subplots(2, 4, figsize=(16, 6), sharex=True)
runs = {0: ('in_s0', 'f1s0', 'f2s0'), 1: ('k2s1', 'f1s1', 'f2s1'), 2: ('k2s2', 'f1s2', 'f2s2'), 3: ('in_s3', None, None)}
for j, (sd, (a, b, c)) in enumerate(runs.items()):
    for f, lab, col in [(a, 'intact', 'k'), (b, 'dissolved prey only after t=3000', 'tab:blue'), (c, 'prey droplets only after t=3000', 'tab:red')]:
        if f is None: continue
        R = L(f); ax[0, j].plot(R[:, 0], R[:, 2], color=col, label=lab); ax[1, j].plot(R[:, 0], R[:, 4], color=col)
    ax[0, j].set_title(f'seed {sd}, 128^2'); ax[0, j].axvline(3000, color='gray', ls=':')
    ax[1, j].axvline(3000, color='gray', ls=':'); ax[1, j].set_xlabel('t')
ax[0, 0].set_ylabel('predator droplets'); ax[1, 0].set_ylabel('mean predator c'); ax[0, 0].legend(fontsize=7)
plt.suptitle('Condensate food chain (chi=0, k0=0.002): predators persist only on a mixed diet of prey droplets and dissolved prey')
plt.tight_layout(); plt.savefig('fork_ablation.png', dpi=70)
# cycles figure: prey and predator mass, intact seeds + 256
fig, ax = plt.subplots(5, 1, figsize=(11, 11), sharex=True)
for k, f in enumerate(['in_s0', 'k2s1', 'k2s2', 'in_s3', 'k2L256']):
    R = L(f); a2 = ax[k].twinx()
    ax[k].plot(R[:, 0], R[:, 3], 'c', label='prey mass'); a2.plot(R[:, 0], R[:, 4], 'r', label='predator mass')
    ax[k].set_ylabel('mean prey c', color='c'); a2.set_ylabel('mean pred c', color='r'); ax[k].set_title(f, fontsize=8)
ax[-1].set_xlabel('t'); plt.tight_layout(); plt.savefig('cycles.png', dpi=70)
# RM positive control
fig, ax = plt.subplots(1, 2, figsize=(13, 3.5))
for f in ['rm_wm', 'rm_L128_unif', 'rm_L16', 'rm_L32', 'rm_L64', 'rm_L128_s0', 'rm_L128_s1']:
    R = L(f); ax[0].plot(R[:, 0], R[:, 2], label=f, lw=0.8)
ax[0].set_xscale('symlog', linthresh=50); ax[0].set_xlabel('t'); ax[0].set_ylabel('mean predator v'); ax[0].legend(fontsize=7)
R = L('rm_L128_s0'); ax[1].plot(R[:, 0], R[:, 2], label='domain mean'); ax[1].plot(R[:, 0], R[:, 5], lw=0.6, label='16x16 patch'); ax[1].set_xlim(0, 600); ax[1].legend(fontsize=7)
ax[1].set_title('RM L=128 seed 0: local cycles, damped global mean', fontsize=8)
plt.tight_layout(); plt.savefig('rm_control.png', dpi=70)
