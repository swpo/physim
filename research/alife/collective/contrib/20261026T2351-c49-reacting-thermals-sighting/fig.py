"""python fig.py out.png seed T : heat T (top: flow on, bottom: g=0 twin) at 8 times, plus body counts (T>0.25, >=4 px)."""
import sys, os, json, importlib, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy import ndimage
sys.path.insert(0, '/home/user/physim/research/alife'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
out, seed, T = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
rows = []
for g in (None, 0.0):
    os.environ['WORLD_P'] = json.dumps({} if g is None else {"g": g})
    import world; importlib.reload(world)
    s = world.init(seed, (128, 128)); dt = world.P['dt']; n = int(T / dt); snaps = set(np.linspace(0, n, 8).astype(int)); fr = []; cnt = []
    for i in range(n + 1):
        if i in snaps: fr.append((i * dt, s['T'].copy(), s['Y'].copy()))
        if i % int(5 / dt) == 0:
            l, k = ndimage.label(s['T'] > 0.25); a = ndimage.sum(np.ones_like(s['T']), l, range(1, k + 1)) if k else []
            cnt.append((i * dt, int((np.asarray(a) >= 4).sum())))
        if i < n: s = world.step(s)
    rows.append((fr, np.array(cnt)))
fig = plt.figure(figsize=(16, 6.4))
for r, (fr, c) in enumerate(rows):
    for j, (t, Tf, Yf) in enumerate(fr):
        ax = fig.add_subplot(3, 8, r * 8 + j + 1)
        rgb = np.stack([np.clip(Tf / 0.7, 0, 1), 0.45 * np.clip(Yf, 0, 1), 0.25 * np.clip(Yf, 0, 1)], -1)
        ax.imshow(rgb, origin='lower'); ax.axis('off'); ax.set_title(f"{'flow' if r == 0 else 'g=0 twin'} t={t:.0f}", fontsize=8)
ax = fig.add_subplot(3, 1, 3)
ax.plot(rows[0][1][:, 0], rows[0][1][:, 1], 'r', label='burning bodies, flow on'); ax.plot(rows[1][1][:, 0], rows[1][1][:, 1], 'k', label='g=0 twin (no flow)')
ax.set_xlabel('t'); ax.legend(fontsize=8); ax.set_ylabel('bodies (T>0.25)')
plt.tight_layout(); plt.savefig(out, dpi=70)
print(out, 'final', rows[0][1][-1], rows[1][1][-1])
