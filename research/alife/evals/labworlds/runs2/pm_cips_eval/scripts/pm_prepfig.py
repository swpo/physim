import json, sys
sys.path.insert(0, "/home/user/evalwork/pm_cips_eval/scripts")
EVALPILOT = "/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot"; OUT = "/home/user/evalwork/pm_cips_eval"
import numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from scipy import ndimage
FIELDS=("S","K","L","phi")
z=np.load(f"{EVALPILOT}/out/prep_s0.npz"); st={f: z[f] for f in FIELDS}
nodes=json.load(open(f"{OUT}/figs/pm_nodes.json"))
info = json.load(open(f"{EVALPILOT}/out/prep_s0.json"))
fig, ax = plt.subplots(1, 4, figsize=(20, 5.4))
for a, f in zip(ax, FIELDS):
    im = a.imshow(st[f], origin="lower", cmap="viridis"); plt.colorbar(im, ax=a, fraction=0.046)
    for d, c in zip(("device0", "device1"), ("r", "w")):
        n = np.array(nodes[d])
        a.plot(n[:, 1], n[:, 0], ".", color=c, ms=4)
    a.set_title(f"{f} t=4000")
lab, n = ndimage.label(st["phi"] > 0.5)
for j in range(1, n + 1):
    yy, xx = np.nonzero(lab == j)
    ax[3].text(xx.mean(), yy.mean(), str(j), color="k", fontsize=7)
fig.tight_layout(); fig.savefig(f"{OUT}/figs/pm_prep.png", dpi=70)
print(n, [int((lab == j).sum()) for j in range(1, n + 1)])
print({f: (float(st[f].min()), float(st[f].max())) for f in FIELDS})
print(info["sites"])
