"""Figure for preyarms.py: rows = arm x target, columns = +0,+250,+500,+1000,+2000; crop 40 px around the target's start.
R prey c_a, G predator c_b, B fuel F. usage: armsfig.py ARMSDIR SEED OUT.png"""
import sys, json, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
D, seed, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
d = json.load(open(f'{D}/preyarms_{seed}.json')); arms = ['fed', 'fcut', 'kc0']; cols = [0, 1, 2, 4, 8]; C = 20; N = 128
fig, ax = plt.subplots(9, len(cols), figsize=(1.5 * len(cols), 1.5 * 9))
for a, arm in enumerate(arms):
    fr = np.load(f'{D}/frames_{arm}_{seed}.npz')['f']
    for k, t in enumerate(d['targets']):
        cy, cx = int(round(t['c'][0])), int(round(t['c'][1]))
        for j, c in enumerate(cols):
            f = fr[c]; img = np.stack([np.clip(f[0], 0, 1), np.clip(f[1], 0, 1), np.clip(f[2], 0, 1) * 0.6], -1)
            img = np.roll(np.roll(img, N // 2 - cy, 0), N // 2 - cx, 1)[N // 2 - C:N // 2 + C, N // 2 - C:N // 2 + C]
            x = ax[a * 3 + k, j]; x.imshow(img, interpolation='nearest'); x.set_xticks([]); x.set_yticks([])
            if j == 0: x.set_ylabel(f'{arm} T{k}', fontsize=7)
            if a == 0 and k == 0: x.set_title(f'+{c * 250}', fontsize=8)
plt.suptitle(f'seed {seed}: target prey at centre (R prey, G predator, B fuel)', fontsize=8); plt.tight_layout(); plt.savefig(out, dpi=80)
