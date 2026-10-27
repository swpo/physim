"""quick look: python quick.py '<WORLD_P json>' seed T out.png  -> |omega| (signed colour) and Y at 8 times"""
import sys, os, json, importlib.util, numpy as np
os.environ['WORLD_P'] = sys.argv[1]
sys.path.insert(0, '/home/user/physim/research/alife')
spec = importlib.util.spec_from_file_location('w', 'world.py'); W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
seed, T = int(sys.argv[2]), float(sys.argv[3]); s = W.init(seed, W.META['size']); dt = s['par']['dt']
NS = int(os.environ.get("NS", 8)); times = np.linspace(0, T, NS); snaps = []; k = 0
nsteps = int(T / dt)
for i in range(nsteps + 1):
    if k < NS and s['t'] >= times[k] - 1e-9:
        snaps.append((s['t'], s['om'].copy(), s['Y'].copy())); k += 1
    s = W.step(s)
    if i % 500 == 0:
        uy, ux = W._vel(s); print(round(s["t"],1), "umax", round(float(np.hypot(uy,ux).max()),2), "wmax", round(float(np.abs(s["om"]).max()),2), "Y", round(float(s["Y"].mean()),3))
    if not np.isfinite(s['om']).all(): print('blowup at', s['t']); break
fig, ax = plt.subplots(2, len(snaps), figsize=(2.2 * len(snaps), 4.6))
for j, (t, om, Y) in enumerate(snaps):
    m = max(np.abs(om).max(), 1e-3)
    ax[0, j].imshow(om, origin='lower', cmap='RdBu_r', vmin=-m, vmax=m); ax[0, j].set_title(f't={t:.0f} |w|max {m:.2f}', fontsize=7)
    ax[1, j].imshow(Y, origin='lower', cmap='viridis', vmin=0, vmax=1)
    for a in ax[:, j]: a.set_xticks([]); a.set_yticks([])
fig.suptitle(sys.argv[1], fontsize=8); plt.tight_layout(); plt.savefig(sys.argv[4], dpi=60)
print('done', [round(float(np.abs(o).max()), 2) for _, o, _ in snaps], [round(float(y.mean()), 2) for *_, y in snaps])
