"""Snapshots of chosen pulse cases vs the uninjected twin (phi of the pulsed run, |dphi|, |ds|, |dc|) at t = 20, 50, 100.
usage: pulse_view.py field:site:amp [...]   -> pulse_view.png"""
import copy, json, sys
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import apparatus as A

m = A.load()
s0, info = A.load_prep(m, 0, 128)
S = info["sites"]
dt = m.P["dt"]
marks = [20, 50, 100]
tw, t, twin = {}, 0, copy.deepcopy(s0)
for mk in marks:
    n = int(round(mk / dt)); twin = A.advance(m, twin, n - t, t0=t); t = n; tw[mk] = copy.deepcopy(twin)
cases = [(c.split(":")[0], c.split(":")[1], float(c.split(":")[2])) for c in sys.argv[1:]]
fig, ax = plt.subplots(len(cases) * len(marks), 4, figsize=(13, 3.2 * len(cases) * len(marks)))
row = 0
for field, site, amp in cases:
    y, x = S[site]
    inj = dict(field=field, y=y, x=x, amp=amp, sig=2.0, start=0, dur=20)
    s, t = copy.deepcopy(s0), 0
    for mk in marks:
        n = int(round(mk / dt)); s = A.advance(m, s, n - t, inj=inj, t0=t); t = n
        ims = [("phi pulsed", s["phi"], "viridis", None), ("|dphi|", np.abs(s["phi"] - tw[mk]["phi"]), "magma", 1.0),
               ("|ds|", np.abs(s["s"] - tw[mk]["s"]), "magma", 0.2), ("|dc|", np.abs(s["c"] - tw[mk]["c"]), "magma", 1.0)]
        for j, (nm, im, cm, vm) in enumerate(ims):
            a = ax[row, j]
            a.imshow(im, cmap=cm, vmin=0 if vm else None, vmax=vm)
            a.plot(x, y, "c+", ms=12, mew=2)
            a.set_title(f"{field} {site} amp {amp:g}, t={mk}: {nm}", fontsize=8)
            a.set_xticks([]); a.set_yticks([])
        row += 1
plt.tight_layout()
out = A.D / ("pulse_view_" + "_".join(c.replace(":", "-") for c in sys.argv[1:]) + ".png")
plt.savefig(out, dpi=60)
print(out)
