"""c13: births with exactly one earlier peak within 12 px (fed arm): crops of phi around the birth before and after,
to see whether a lone peak buds/splits or whether the birth is templated by peaks just outside 12 px."""
import sys, os, json, importlib.util, numpy as np
from scipy import ndimage
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
N = 128; os.environ["WORLD_P"] = sys.argv[1]; T = int(sys.argv[2]); seed = int(sys.argv[3]); out = sys.argv[4]
spec = importlib.util.spec_from_file_location("w", os.path.join(os.path.dirname(os.path.abspath(__file__)), "world.py"))
w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
s = w.init(seed, (N, N)); prev = None; snaps = {}; ev = []
def peaks(p): return np.argwhere((p == ndimage.maximum_filter(p, size=7, mode="wrap")) & (p > 0.0))
def dists(a, B):
    d = np.abs(B - a); d = np.minimum(d, N - d); return np.hypot(d[:, 0], d[:, 1])
for n in range(1, T + 1):
    w.step(s)
    if n % 20 == 0:
        snaps[n] = s["phi"].copy()
        if n * w.P["dt"] >= 60:
            pk = peaks(s["phi"])
            if prev is not None:
                for a in pk:
                    d = dists(a, prev)
                    if d.min() > 3:
                        ev.append((n, a, int((d <= 12).sum()), int((d <= 20).sum())))
            prev = pk
sel = [e for e in ev if e[2] == 1]
offs = [-60, -20, 0, 100, 300]
fig, ax = plt.subplots(len(sel), len(offs), figsize=(2 * len(offs), 2 * len(sel)), squeeze=False)
for i, (n, a, k12, k20) in enumerate(sel):
    for j, o in enumerate(offs):
        m = min(max(n + o, 20), T - T % 20); m -= m % 20
        f = np.roll(np.roll(snaps[m], N // 2 - a[0], 0), N // 2 - a[1], 1)[N//2-24:N//2+24, N//2-24:N//2+24]
        ax[i, j].imshow(f, vmin=-1.2, vmax=1.2, cmap="magma"); ax[i, j].set_xticks([]); ax[i, j].set_yticks([])
        ax[i, j].set_title(f"t={m*w.P['dt']:.0f}" + (f" k20={k20}" if j == 0 else ""), fontsize=7)
plt.tight_layout(); plt.savefig(out, dpi=80)
print(json.dumps({"singles": [(int(n * w.P['dt']), int(k20)) for n, a, k12, k20 in sel]}))
