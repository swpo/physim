"""pathprobe.py's measurement (c31) applied to labkit frames.npz instead of a fresh simulation:
largest body (phi > 1/2, periodic labels via the world's plabel), periodic centroid, unwrapped; net displacement
over stretches with a constant body count from t >= 2, in the body's own mean diameter.
usage: pathframes.py world.py frames.npz dt_frame seed"""
import sys, importlib.util, numpy as np
spec = importlib.util.spec_from_file_location("w", sys.argv[1]); W = importlib.util.module_from_spec(spec); spec.loader.exec_module(W)
R = np.load(sys.argv[2])["render"]; dtf = float(sys.argv[3]); seed = sys.argv[4]
L = W.P["L"]; N = R.shape[-1]; dx = L / N
x = (np.arange(N) + 0.5) * dx; X, Y = np.meshgrid(x, x)   # x varies along axis 1
rows = []
for f, F in enumerate(R):
    lab, nb = W.plabel(F[0] > 0.5)
    if not nb: continue
    a = np.bincount(lab.ravel())[1:]; j = int(a.argmax()) + 1; m = lab == j
    c = [float((np.angle(np.exp(2j * np.pi * Z[m] / L).mean()) % (2 * np.pi)) * L / (2 * np.pi)) for Z in (X, Y)]
    rows.append((f * dtf, nb, a.max() * dx * dx, c[0], c[1]))
t, nb, A, cx, cy = map(np.array, zip(*rows)); c = np.c_[cx, cy]
d = (np.diff(c, axis=0) + L / 2) % L - L / 2; pos = np.r_[[c[0]], c[0] + np.cumsum(d, axis=0)]
diam = 2 * np.sqrt(A / np.pi)
i = int(np.searchsorted(t, 2.0)); best = 0
while i < len(t):
    k = i
    while k + 1 < len(t) and nb[k + 1] == nb[i]: k += 1
    net = float(np.hypot(*(pos[k] - pos[i]))); od = net / diam[i:k + 1].mean()
    best = max(best, od)
    print(f"seed {seed} t {t[i]:.2f}-{t[k]:.2f} bodies {nb[i]} net {net:.2f} = {od:.2f} own diameters, speed {net / max(t[k] - t[i], 1e-9):.3f}")
    i = k + 1
i2 = int(np.searchsorted(t, 2.0))
print(f"seed {seed} best merger-free {best:.2f} own diameters; whole run from t=2 net {np.hypot(*(pos[-1] - pos[i2])):.2f} = {np.hypot(*(pos[-1] - pos[i2])) / diam[-1]:.2f} final diameters (spans absorptions)")
