"""usage: WORLD_P=... snapt.py SEED OUT.png : predator matter coloured by log trait at t=1000, 2000, 3000 (prey grey)."""
import sys, os, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import world as w
seed, out = int(sys.argv[1]), sys.argv[2]; s = w.init(seed, (160, 160)); dt = w.CFG['dt']; marks = [1000, 2000, 3000]; fr = []
for i in range(int(3000 / dt) + 1):
    if any(abs(i * dt - m) < dt / 2 for m in marks): fr.append((i * dt, s['A'].sum(0).copy(), s['B'].sum(0).copy(), np.log(w.trait(s)).copy()))
    s = w.step(s)
fig, ax = plt.subplots(1, 3, figsize=(12, 4.2))
for a, (t, A, B, lt) in zip(ax, fr):
    a.imshow(np.clip(A, 0, 1.5), cmap='gray_r', vmin=0, vmax=3, interpolation='nearest')
    m = np.ma.masked_where(B < 0.3, lt); im = a.imshow(m, cmap='coolwarm', vmin=-0.8, vmax=0.8, interpolation='nearest')
    a.set_title(f't={t:.0f}: predators coloured by log trait (prey grey)', fontsize=8); a.set_xticks([]); a.set_yticks([])
fig.colorbar(im, ax=ax, shrink=0.7); plt.savefig(out, dpi=80); print('ok')
