import sys, numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
z = np.load(sys.argv[1]); x, t, bA, bB = z["x"], z["t"], z["bA"], z["bB"]; L = 16.0
fig, ax = plt.subplots(figsize=(9, 9))
col = {0: (0.8, 0.8, 0.8), 1: "C0", 2: "C1", 3: "C3"}
for k in (0, 1, 3, 2):
    m = t == k; ax.scatter(x[m, 0], x[m, 1], s=1.5 if k == 0 else 4, c=[col[k]], lw=0)
for i in np.flatnonzero(bA >= 0):
    for j in (bA[i], bB[i]):
        if j > i:
            d = x[j] - x[i]
            if np.abs(d).max() < 2: ax.plot([x[i, 0], x[j, 0]], [x[i, 1], x[j, 1]], "k-", lw=0.6)
ax.set_xlim(0, L); ax.set_ylim(0, L); ax.set_aspect(1); ax.set_title(sys.argv[1] + "  grey F, blue/red C, orange M, black bonds")
plt.savefig(sys.argv[2], dpi=80)
