"""c13: is a closed 2D bilayer ring (a planted vesicle) stable in c12's lipid-2d at default kT, or does it open?
usage: planted.py Rm T_end seed out_prefix [WORLD_P json]
Plants one bilayer ring with tail midplane radius Rm (outer and inner leaflets, beads 1 sigma apart, lipids
1.1 sigma apart along the arc) alone in the default box, runs to T_end and scores enclosure (holes.py rule) and
the ring's integrity every 300 t. Writes <out>_snap.png (beads at 4 times) and prints a JSON line."""
import sys, os, json, importlib.util, numpy as np
from scipy import ndimage
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
Rm, Tend, seed, out = float(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
if len(sys.argv) > 5: os.environ["WORLD_P"] = sys.argv[5]
spec = importlib.util.spec_from_file_location("w", os.path.join(os.path.dirname(os.path.abspath(__file__)), "world.py"))
w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
L = w.P["L"]; c0 = np.array([L / 2, L / 2]); lip = []
for sgn in (+1, -1):  # outer leaflet: heads outward; inner leaflet: heads inward
    rT2 = Rm + 0.5 * sgn; n = int(2 * np.pi * (Rm + 1.5 * sgn) / 1.1)
    for th in np.linspace(0, 2 * np.pi, n, endpoint=False):
        d = np.array([np.cos(th), np.sin(th)])
        lip.append([c0 + (rT2 + 2 * sgn) * d, c0 + (rT2 + sgn) * d, c0 + rT2 * d])  # H, T1, T2
x = np.array(lip).reshape(-1, 2) % L; N = len(lip)
w.P["N"] = N
typ = np.zeros(3 * N, np.int64); typ[1::3] = 1; typ[2::3] = 1
s = {"x": x, "typ": typ, "rng": np.random.default_rng(seed), "size": (128, 128)}
def enclosed(x):
    n = int(round(L / 0.5)); g = np.zeros((n, n)); ix = (x / L * n).astype(int) % n
    np.add.at(g, (ix[:, 1], ix[:, 0]), 1); g = ndimage.gaussian_filter(g, 1.0, mode="wrap"); lipm = g > 0.15
    bg = np.tile(~lipm, (3, 3)); lab, k = ndimage.label(bg); c = lab[n:2 * n, n:2 * n]
    ids, cnt = np.unique(c[c > 0], return_counts=True); sizes = ndimage.sum(bg, lab, ids)
    return [round(a * 0.25) for i, a, sz in zip(ids, cnt, sizes) if sz == a and a * 0.25 >= 8]
fdt = w.P["dt"] * w.P["sub"]; nf = int(Tend / fdt); log = []; snaps = []
want = [0, nf // 6, nf // 2, nf]
for f in range(nf + 1):
    if f in want: snaps.append((f * fdt, s["x"].copy()))
    if f % int(300 / fdt) == 0: log.append((round(f * fdt), enclosed(s["x"])))
    if f < nf: w.step(s)
fig, ax = plt.subplots(1, len(snaps), figsize=(3 * len(snaps), 3))
for a, (t, xx) in zip(ax, snaps):
    a.scatter(xx[0::3, 0], xx[0::3, 1], s=2, c="tab:blue"); a.scatter(xx[1::3, 0], xx[1::3, 1], s=2, c="tab:orange"); a.scatter(xx[2::3, 0], xx[2::3, 1], s=2, c="tab:orange")
    a.set_xlim(0, L); a.set_ylim(0, L); a.set_aspect(1); a.set_xticks([]); a.set_yticks([]); a.set_title(f"Rm={Rm} N={N} t={t:.0f}", fontsize=8)
plt.tight_layout(); plt.savefig(out + "_snap.png", dpi=70)
print(json.dumps({"Rm": Rm, "N": N, "seed": seed, "WORLD_P": os.environ.get("WORLD_P", "{}"), "enclosed_area_every_300t": log}))
