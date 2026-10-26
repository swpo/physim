"""Positive control: spatial Rosenzweig-MacArthur with a per-site extinction floor (demographic cutoff).
u_t = D lap u + u(1-u) - u v/(u+h);  v_t = D lap v + k u v/(u+h) - m v;  any site with u<eps (v<eps) is set to 0.
Well-mixed twin: the same ODE on one site with the same floor. usage: rmpc.py out L seed [eps] [m] [mode]"""
import sys, json, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
out, L, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
eps = float(sys.argv[4]) if len(sys.argv) > 4 else 0.01
m = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
mode = sys.argv[6] if len(sys.argv) > 6 else 'patchy'   # patchy | uniform
h, k, D, dt, T = 0.4, 2.0, 1.0, 0.05, 3000.0
rng = np.random.default_rng(seed)
ustar = m * h / (k - m); vstar = (1 - ustar) * (ustar + h) / k
u = np.full((L, L), ustar) * (1 + (0.2 * rng.standard_normal((L, L)) if mode == 'patchy' else 0)); v = np.full((L, L), vstar)
if mode == 'patchy':
    from scipy import ndimage
    n = ndimage.gaussian_filter(rng.standard_normal((L, L)), 8, mode='wrap'); u = np.clip(ustar * (1 + 3 * n / n.std()), 0, 1)
else:
    u = u + 0.01
def lap(x): return np.roll(x, 1, 0) + np.roll(x, -1, 0) + np.roll(x, 1, 1) + np.roll(x, -1, 1) - 4 * x
rec = []; snaps = []; nst = int(T / dt)
for i in range(nst + 1):
    if i % int(5 / dt) == 0:
        rec.append([i * dt, u.mean(), v.mean(), (v > eps).mean(), u[:16, :16].mean(), v[:16, :16].mean()])
    if i % int(T / 8 / dt) == 0: snaps.append((i * dt, v.copy()))
    f = u * v / (u + h)
    u = u + dt * (D * lap(u) + u * (1 - u) - f); v = v + dt * (D * lap(v) + k * f - m * v)
    u[u < eps] = 0; v[v < eps] = 0
R = np.array(rec)
json.dump(dict(cols=['t', 'u', 'v', 'occ_v', 'u_patch', 'v_patch'], rows=R.tolist(), L=L, seed=seed, eps=eps, m=m, mode=mode), open(out + '.json', 'w'))
fig = plt.figure(figsize=(14, 4.5))
for j, (t, V) in enumerate(snaps[:9]):
    ax = fig.add_subplot(2, 9, j + 1); ax.imshow(V, vmin=0, vmax=0.6, cmap='magma'); ax.set_title('t=%.0f' % t, fontsize=7); ax.axis('off')
ax = fig.add_subplot(2, 1, 2); ax.plot(R[:, 0], R[:, 2], label='mean predator'); ax.plot(R[:, 0], R[:, 1], label='mean prey')
ax.plot(R[:, 0], R[:, 5], lw=0.6, label='predator, 16x16 patch'); ax.legend(fontsize=7); ax.set_xlabel('t')
ax.set_title(f'RM spatial L={L} seed={seed} eps={eps} m={m} {mode}', fontsize=8)
plt.tight_layout(); plt.savefig(out + '.png', dpi=70)
print(out, 'final u %.3f v %.3f, last v>0 t=%s' % (u.mean(), v.mean(), R[R[:, 2] > 0, 0].max() if (R[:, 2] > 0).any() else -1))
