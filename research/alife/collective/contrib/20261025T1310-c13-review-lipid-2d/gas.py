"""c13: c12's lipid-2d from its random gas at a WORLD_P point; final enclosure count (holes.py rule) every 300 t and a
bead snapshot at 4 times. usage: gas.py T_end seed out_prefix WORLD_P"""
import sys, os, json, importlib.util, numpy as np
from scipy import ndimage
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
Tend, seed, out = float(sys.argv[1]), int(sys.argv[2]), sys.argv[3]; os.environ["WORLD_P"] = sys.argv[4]
spec = importlib.util.spec_from_file_location("w", os.path.join(os.path.dirname(os.path.abspath(__file__)), "world.py"))
w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w); L = w.P["L"]
s = w.init(seed, (128, 128))
def enclosed(x):
    n = int(round(L / 0.5)); g = np.zeros((n, n)); ix = (x / L * n).astype(int) % n
    np.add.at(g, (ix[:, 1], ix[:, 0]), 1); g = ndimage.gaussian_filter(g, 1.0, mode="wrap"); lipm = g > 0.15
    bg = np.tile(~lipm, (3, 3)); lab, k = ndimage.label(bg); c = lab[n:2 * n, n:2 * n]
    ids, cnt = np.unique(c[c > 0], return_counts=True); sizes = ndimage.sum(bg, lab, ids)
    return [round(a * 0.25) for i, a, sz in zip(ids, cnt, sizes) if sz == a and a * 0.25 >= 8]
fdt = w.P["dt"] * w.P["sub"]; nf = int(Tend / fdt); log = []; snaps = []; want = [0, nf // 6, nf // 2, nf]
for f in range(nf + 1):
    if f in want: snaps.append((f * fdt, s["x"].copy()))
    if f % int(300 / fdt) == 0: log.append((round(f * fdt), enclosed(s["x"])))
    if f < nf: w.step(s)
fig, ax = plt.subplots(1, len(snaps), figsize=(3.2 * len(snaps), 3.2))
for a, (t, xx) in zip(ax, snaps):
    a.scatter(xx[0::3, 0], xx[0::3, 1], s=0.6, c="tab:blue"); a.scatter(xx[1::3, 0], xx[1::3, 1], s=0.6, c="tab:orange"); a.scatter(xx[2::3, 0], xx[2::3, 1], s=0.6, c="tab:orange")
    a.set_xlim(0, L); a.set_ylim(0, L); a.set_aspect(1); a.set_xticks([]); a.set_yticks([]); a.set_title(f"{sys.argv[4]} s{seed} t={t:.0f}", fontsize=7)
plt.tight_layout(); plt.savefig(out + "_snap.png", dpi=80)
print(json.dumps({"seed": seed, "WORLD_P": sys.argv[4], "enclosed_area_every_300t": log}))
