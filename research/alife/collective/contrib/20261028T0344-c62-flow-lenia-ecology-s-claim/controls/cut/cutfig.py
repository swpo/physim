"""Figure for flcut.py runs saved with FRAMES: rows fed / qcut, columns t = 0, 40, 80, 160, 400 after the cut; red prey,
green predator (both clipped at 1.5); white circles mark the targets' positions at the cut. usage: cutfig.py PREFIX CUT.json OUT.png"""
import sys, json, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
pre, cj, out = sys.argv[1], sys.argv[2], sys.argv[3]; d = json.load(open(cj)); cols = [0, 2, 4, 8, 20]
fig, ax = plt.subplots(2, len(cols), figsize=(2.6 * len(cols), 5.4))
for r, arm in enumerate(['fed', 'qcut']):
    F = np.load(f'{pre}_{arm}.npz')['f'].astype(float)
    for j, c in enumerate(cols):
        f = F[min(c, len(F) - 1)]; img = np.stack([np.clip(f[0] / 1.5, 0, 1), np.clip(f[1] / 1.5, 0, 1), np.zeros_like(f[0])], -1)
        a = ax[r, j]; a.imshow(img, interpolation='nearest'); a.set_xticks([]); a.set_yticks([])
        for t in d['targets']: a.add_patch(plt.Circle((t['c'][1], t['c'][0]), 12, fill=False, ec='w', lw=0.8))
        a.set_title(f"{arm} +{c * 20} t", fontsize=8)
plt.suptitle(f"seed {d['seed']}: digestion product cut around 4 predators at t={d['T0']:.0f} (qcut) vs fed twin", fontsize=9)
plt.tight_layout(); plt.savefig(out, dpi=75)
