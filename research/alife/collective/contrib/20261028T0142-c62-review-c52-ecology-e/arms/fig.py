"""Figure: for each seed, rows = arms, columns = times; crop around target k (centred on its start position).
Prey material red, predator material green, digestion product q blue (clipped at 1). usage: fig.py SEED"""
import json, sys, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
seed = int(sys.argv[1]); arms = ['ctrl', 'kdlocal', 'kdlocal_chiF0']
times = [0, 300, 600, 1000, 2000, 3000]; C = 24
d0 = json.load(open(f'/tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/rv3/arms/ctrl_s{seed}.json')); nt = len(d0['targets'])
fig, ax = plt.subplots(len(arms) * nt, len(times), figsize=(1.6 * len(times), 1.6 * len(arms) * nt))
for a, arm in enumerate(arms):
    try: R = np.load(f'/tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/rv3/arms/{arm}_s{seed}_frames.npz')['render']; d = json.load(open(f'/tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/rv3/arms/{arm}_s{seed}.json'))
    except Exception: continue
    for k, c in enumerate(d['targets']):
        cy, cx = int(round(c['cy'])), int(round(c['cx']))
        for j, t in enumerate(times):
            fr = R[min(t // 100, len(R) - 1)]
            img = np.stack([np.clip(fr[0], 0, 1), np.clip(fr[1], 0, 1), np.clip(fr[2], 0, 1)], -1)
            img = np.roll(np.roll(img, 64 - cy, 0), 64 - cx, 1)[64 - C:64 + C, 64 - C:64 + C]
            x = ax[a * nt + k, j]; x.imshow(img, interpolation='nearest'); x.set_xticks([]); x.set_yticks([])
            if j == 0: x.set_ylabel(f'{arm}\nT{k}', fontsize=7)
            if a == 0 and k == 0: x.set_title(f'+{t}', fontsize=8)
plt.suptitle(f'seed {seed}: target crops (R prey, G predator, B q)', fontsize=9); plt.tight_layout()
plt.savefig(f'/home/user/physim/research/alife/collective/contrib/20261028T0142-c62-review-c52-ecology-e/arms/targets_s{seed}.png', dpi=80)
