"""c52: run world_local.py and follow predator material inside the cut disk vs the rest; snapshots of the neighbourhood.
usage: localcut.py out seed y x r tcut T"""
import sys, json, os, importlib.util, numpy as np
sys.path.insert(0, '/home/user/physim/research/alife')
from scipy import ndimage
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
out, seed, y, x, r, tc, T = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6]), float(sys.argv[7])
cut = os.environ.get('CUT', '1') == '1'
os.environ['WORLD_P'] = json.dumps({"pcut_t": tc if cut else -1.0, "pcut_y": y, "pcut_x": x, "pcut_r": r})
spec = importlib.util.spec_from_file_location('w', 'world_local.py'); w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
s = w.init(seed, (128, 128)); dt = w.P['dt']; H = W = 128
yy, xx = np.mgrid[0:H, 0:W]; d2 = ((yy - y + H/2) % H - H/2) ** 2 + ((xx - x + W/2) % W - W/2) ** 2
inner = d2 < (r + 6) ** 2  # disk plus a 6 px margin: a predator that has not left the area
rows, snaps = [], []
snapt = [tc - 200, tc, tc + 100, tc + 200, tc + 400, tc + 700, tc + 1000, tc + 1500]
for i in range(int(T / dt) + 1):
    t = i * dt
    if i % int(50 / dt) == 0 or any(abs(t - st) < dt / 2 for st in snapt):
        F = w.fields(s); cb, ca = F[1], F[0]
        L, n = ndimage.label(cb > 0.5); a = np.bincount(L.ravel())
        ids = [k for k in range(1, n + 1) if a[k] >= 4]
        inside = [k for k in ids if inner[L == k].mean() > 0.5]
        rows.append([t, float(cb[inner].max()), len(inside), len(ids) - len(inside), float(ca[inner].max())])
        if any(abs(t - st) < dt / 2 for st in snapt):
            sl = np.roll(np.roll(F, int(H/2 - y), -2), int(W/2 - x), -1)[:, 34:94, 34:94]
            snaps.append((t, sl))
    if i * dt < T: s = w.step(s)
R = np.array(rows)
json.dump({"cols": ["t", "max_cb_area", "pred_bodies_in_area", "pred_bodies_elsewhere", "max_ca_area"], "rows": R.tolist(), "cut": cut, "y": y, "x": x, "r": r, "tc": tc}, open(out + '.json', 'w'))
fig = plt.figure(figsize=(1.7 * len(snaps), 4.4))
for k, (t, F) in enumerate(snaps):
    ax = fig.add_subplot(2, len(snaps), k + 1)
    ax.imshow(np.stack([F[1], F[0], 0.35 * F[2]], -1).clip(0, 1)); ax.add_patch(plt.Circle((30, 30), r, fill=False, ec='w', lw=0.6, ls='--'))
    ax.set_title(f't={t:.0f}', fontsize=7); ax.axis('off')
ax = fig.add_subplot(2, 1, 2); ax.plot(R[:, 0], R[:, 1], 'r', label='max c_b in cut area (disk + 6 px)'); ax.plot(R[:, 0], R[:, 4], 'g', label='max c_a in cut area')
ax2 = ax.twinx(); ax2.plot(R[:, 0], R[:, 3], 'k:', label='predator bodies elsewhere'); ax2.set_ylabel('bodies elsewhere', fontsize=7)
ax.axvline(tc, color='k', lw=0.5); ax.legend(fontsize=7, loc='lower left'); ax.set_xlabel('t'); ax.set_title(f'{"local prey cut" if cut else "no cut (twin)"} r={r} at t={tc}', fontsize=8)
plt.tight_layout(); plt.savefig(out + '.png', dpi=75)
print(out, R[R[:, 0] >= tc][::4, :4].round(2).tolist())
