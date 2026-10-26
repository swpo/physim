"""Type-coloured particle snapshots (as in Sayama's Fig. 2) and the share of the three commonest types.
usage: python snapshots.py"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
import world
HERE = os.path.dirname(os.path.abspath(__file__))
times = [30, 100, 300, 1000, 2000, 5000, 10000, 20000]
rows = [("hash", dict(mode=0)), ("random U[0.2,1]", dict(mode=1, lo=0.2))]
fig = plt.figure(figsize=(2.4 * len(times), 7.6))
for ri, (lab, p) in enumerate(rows):
    S = world.init(0, p=dict(p, maxev=9_000_000)); tt, shares = [], []
    for t in range(1, times[-1] + 1):
        world.step(S)
        if t % 100 == 0 and S["n"]:
            c = np.bincount(S["ty"][:S["n"]], minlength=1001); tt.append(t); shares.append(np.sort(c)[::-1][:3] / S["n"])
        if t in times:
            a = fig.add_subplot(3, len(times), ri * len(times) + times.index(t) + 1); P = world.particles(S)
            a.scatter(P[:, 0], P[:, 1], c=P[:, 2], cmap="hsv", vmin=1, vmax=1000, s=1.2, lw=0)
            top = np.bincount(P[:, 2].astype(int)).argmax() if len(P) else 0
            a.set_title(f"{lab} t={t}\nn={len(P)}, top type {top}", fontsize=8); a.set_xticks([]); a.set_yticks([]); a.set_xlim(0, 1); a.set_ylim(0, 1)
    b = fig.add_subplot(3, 2, 5 + ri); sh = np.array(shares)
    for q in range(3): b.plot(tt, sh[:, q], label=f"rank {q+1} type")
    b.set_ylim(0, 1); b.set_title(f"{lab}, seed 0: population share of the 3 commonest particle types"); b.set_xlabel("step"); b.legend(fontsize=7)
plt.tight_layout(); plt.savefig(f"{HERE}/snapshots.png", dpi=70)
