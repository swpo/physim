"""Strip of seed-7 predator track 515 (gen 5) from t=10000: fed twin vs its own digestion product cut (kd=0 in a disk following it)."""
import json, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
ts = [0, 100, 200, 300, 400, 600, 1000, 1200, 1500]; C = 22
fig, ax = plt.subplots(2, len(ts), figsize=(1.5 * len(ts), 3.4))
for r, arm in enumerate(['ctrl', 'kdlocal']):
    R = np.load(f'{arm}_frames.npz')['render']; d = json.load(open(f'{arm}.json')); c = d['targets'][0]
    cy, cx = int(round(c['cy'])), int(round(c['cx'])); H = R.shape[-1]
    for j, t in enumerate(ts):
        f = R[t // 100]; img = np.stack([np.clip(f[1], 0, 1), np.clip(f[0], 0, 1), 0.5 * np.clip(f[2], 0, 1)], -1)
        img = np.roll(np.roll(img, H // 2 - cy, 0), H // 2 - cx, 1)[H // 2 - C:H // 2 + C, H // 2 - C:H // 2 + C]
        a = ax[r, j]; a.imshow(img, interpolation='nearest'); a.set_xticks([]); a.set_yticks([])
        a.set_title(f't={10000 + t}', fontsize=7)
        if j == 0: a.set_ylabel('fed twin' if arm == 'ctrl' else 'own q cut\n(kd=0, eats)', fontsize=7)
plt.suptitle('seed 7 (256^2) predator track 515, gen 5: red predator, green prey, blue q', fontsize=8); plt.tight_layout()
plt.savefig('track515_strip.png', dpi=90)
