import sys, glob, os, numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
OUT = "/home/user/evalwork/pm_cips_eval"
world, variant = sys.argv[1], sys.argv[2]
names = sys.argv[3].split(",")
alias = {n: n.removesuffix("_d1x") for n in names}
fields = ("S", "K", "L", "phi") if world == "pm" else ("e", "p", "F", "s")
show = [int(x) for x in sys.argv[4].split(",")]   # field indices
times = [int(x) for x in sys.argv[5].split(",")]
crop = int(sys.argv[6]) if len(sys.argv) > 6 else 0
runs = [(n, np.load(f"{OUT}/pilot/{world}/{variant if ':' not in n else n.split(':')[0]}__{n.split(':')[-1]}.npz")) for n in names]
fig, ax = plt.subplots(len(runs), len(show) * len(times), figsize=(2.6 * len(show) * len(times), 2.6 * len(runs)), squeeze=False)
for r, (n, z) in enumerate(runs):
    for i, fi in enumerate(show):
        for j, t in enumerate(times):
            a = ax[r, i * len(times) + j]
            F = z[f"F_{t}"][fi].astype(float)
            c0, c1 = z[f"c0_{t}"], z[f"c1_{t}"]
            dev = (c1 if "_d1" in n else c0) if len(sys.argv) <= 8 else (c1 if sys.argv[8] == "1" else c0)
            vmax = {"S": 1, "K": 0.6, "L": 0.6, "phi": 1, "e": 1, "p": 0.6, "F": 1, "s": 45}[fields[fi]]
            a.imshow(F, origin="lower", vmin=0, vmax=vmax, cmap="viridis")
            for c, col in ((c0, "r"), (c1, "w")):
                a.plot(c[1] - 0.5, c[0] - 0.5, "+", color=col, ms=8)
            if crop:
                a.set_xlim(dev[1] - crop, dev[1] + crop); a.set_ylim(dev[0] - crop, dev[0] + crop)
            a.set_xticks([]); a.set_yticks([])
            a.set_title(f"{n} {fields[fi]} {t}tu", fontsize=7)
fig.tight_layout(); fig.savefig(f"{OUT}/figs/pilot_{world}_{sys.argv[7] if len(sys.argv) > 7 else variant}.png", dpi=60)
