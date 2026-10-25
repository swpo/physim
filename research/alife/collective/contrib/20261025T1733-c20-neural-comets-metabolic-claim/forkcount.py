"""Comet counts in the left (cut) and right halves over time for fed / cut runs (labkit frames.npz, channel 2 = firing).
usage: forkcount.py out.png label=dir ..."""
import sys, numpy as np
from scipy import ndimage
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
out, runs = sys.argv[1], [a.split("=", 1) for a in sys.argv[2:]]
fig, ax = plt.subplots(1, 2, figsize=(11, 3.6))
for k, (lab, d) in enumerate(runs):
    F = np.load(d + "/frames.npz"); R, fr = F["render"], F["render_f"]; spf = 50; dt = 0.1
    t = fr * spf * dt; L, Rt = [], []
    for i in range(len(R)):
        m = R[i, 2] > 0.5; lb, n = ndimage.label(m)
        if n == 0: L.append(0); Rt.append(0); continue
        cx = np.array(ndimage.center_of_mass(m, lb, range(1, n + 1)))[:, 1]; sz = ndimage.sum(m, lb, range(1, n + 1))
        ok = sz >= 6; L.append(int(((cx < m.shape[1] / 2) & ok).sum())); Rt.append(int(((cx >= m.shape[1] / 2) & ok).sum()))
    ax[0].plot(t, L, color=f"C{k}", label=lab); ax[1].plot(t, Rt, color=f"C{k}", label=lab)
    print(lab, "left half at t~500/750/1000:", L[len(L) // 2], L[3 * len(L) // 4], L[-1], " right half:", Rt[len(Rt) // 2], Rt[3 * len(Rt) // 4], Rt[-1])
for a, ttl in zip(ax, ["left half (recovery cut in 'cut half')", "right half (never cut)"]):
    a.axvline(500, color="k", lw=0.6, ls=":"); a.set_title(ttl, fontsize=9); a.set_xlabel("t"); a.set_ylabel("comets (>= 6 px)")
ax[0].legend(fontsize=7); plt.tight_layout(); plt.savefig(out, dpi=80)
