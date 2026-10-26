"""(c34) Cell speed from a labkit frames.npz of the crawler: periodic phi-weighted centroid (circular mean), speed over
1-time-unit windows, in world units (L=5, 256 px). usage: speed.py frames.npz [frames.npz ...]"""
import sys, numpy as np
L, N = 5.0, 256
for p in sys.argv[1:]:
    F = np.load(p); phi = F["matter"].astype(np.float32); T = len(phi)
    th = 2 * np.pi * np.arange(N) / N; c = []
    for f in phi:
        w = np.clip(f, 0, 1); a = np.angle((w.sum(0) * np.exp(1j * th)).sum()); b = np.angle((w.sum(1) * np.exp(1j * th)).sum())
        c.append([a, b])
    c = np.unwrap(np.array(c), axis=0) * L / (2 * np.pi)
    t = np.linspace(0, 20, T); k = int(round((T - 1) / 20))
    v = np.hypot(*(c[k:] - c[:-k]).T)
    out = " ".join(f"t{int(t[i])}-{int(t[i]) + 1}:{v[i]:.2f}" for i in range(0, len(v), k))
    print(p.split("contrib/")[-1], "speed per unit time:", out)
