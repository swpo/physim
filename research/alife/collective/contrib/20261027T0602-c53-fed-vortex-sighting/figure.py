"""python figure.py seed T out.png : signed vorticity and fuel at 6 times, with the body centroids from dipole_seed<k>.json"""
import sys, os, json, importlib.util, numpy as np
sys.path.insert(0, '/home/user/physim/research/alife')
spec = importlib.util.spec_from_file_location('w', 'world.py'); W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
seed, T = int(sys.argv[1]), float(sys.argv[2]); s = W.init(seed, W.META['size']); dt = s['par']['dt']
times = [0, 150, 500, 800, 1100, 1500]; snaps = []
rec = json.load(open(f'dipole_seed{seed}.json'))
for i in range(int(T / dt) + 1):
    if any(abs(s['t'] - t) < dt / 2 for t in times): snaps.append((s['t'], s['om'].copy(), s['Y'].copy()))
    s = W.step(s)
fig, ax = plt.subplots(2, len(snaps), figsize=(2.6 * len(snaps), 5.6))
for j, (t, om, Y) in enumerate(snaps):
    ax[0, j].imshow(om, origin='lower', cmap='RdBu_r', vmin=-0.2, vmax=0.2); ax[0, j].set_title(f't={t:.0f}', fontsize=9)
    ax[1, j].imshow(Y, origin='lower', cmap='viridis', vmin=0, vmax=1)
    for r in rec:
        if 100 <= r['t'] <= t:
            for b in r['bodies']:
                if b['area'] > 40: ax[0, j].plot(b['cx'], b['cy'], '.', ms=2, color='k' if b['sign'] > 0 else 'g')
    for a in ax[:, j]: a.set_xticks([]); a.set_yticks([])
ax[0, 0].set_ylabel('vorticity (red +, blue -)'); ax[1, 0].set_ylabel('fuel Y')
fig.suptitle(f'fed vortices, seed {seed}: a +/- pair travels as a dipole (dots: centroid paths, black +, green -), swaps partner at t~850 and the new dipole runs into fresh fuel; the abandoned vortex starves', fontsize=8)
plt.tight_layout(); plt.savefig(sys.argv[3], dpi=70)
