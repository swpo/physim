import numpy as np, os, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 3, figsize=(16, 4))
runs = [("j3", "160, s1"), ("j3_s2", "160, s2"), ("big_s1", "256, s1"), ("big_s2", "256, s2"), ("huge_s1", "320, s1"), ("huge_s2", "320, s2")]
cols = {"160": "C0", "256": "C1", "320": "C3"}
ext = {}
for f, lab in runs:
    if not os.path.exists(f + ".txt"):
        continue
    r = np.loadtxt(f + ".txt")
    L = lab.split(",")[0]
    ls = "-" if lab.endswith("s1") else "--"
    ax[0].plot(r[:, 0], r[:, 2], ls, color=cols[L], lw=1, label=f"{L}^2 {lab.split(',')[1]}")
    area = int(L) ** 2 / 160 ** 2
    ax[1].plot(r[:, 0], r[:, 1] / area, ls, color=cols[L], lw=1)
    alive = r[(r[:, 0] > 200) & (r[:, 2] > 0), 0]
    ext[f] = float(alive.max()) if len(alive) else None
ax[0].set_title("specialist predator B cells (introduced at t=200)"); ax[0].legend(fontsize=7)
ax[1].set_title("prey A cells per 160^2 area")
for f, c, lab in [("comp_s2", "k", "competition only s2"), ("om1_s2", "C2", "omnivore PRATE 0.2 s2"), ("om2_s2", "C4", "omnivore PRATE 1.0 s2"),
                  ("comp_s1", "k", "competition only s1"), ("om1", "C2", "PRATE 0.2 s1"), ("om2", "C4", "PRATE 1.0 s1")]:
    r = np.loadtxt(f + ".txt"); r = r[r[:, 0] <= 600]
    ax[2].plot(r[:, 0], r[:, 1], "-" if "s2" in lab else "--", color=c, lw=1, label=lab)
ax[2].set_title("prey A cells, 160^2: intraguild predation by B"); ax[2].legend(fontsize=6)
for a in ax: a.set_xlabel("t")
plt.tight_layout(); plt.savefig("predation.png", dpi=75)
print(ext)
