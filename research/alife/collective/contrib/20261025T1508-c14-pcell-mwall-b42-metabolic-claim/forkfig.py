"""Fed vs starved twin (feed cut at t=Foff): wall channel (4phi(1-phi), render ch 3) and M (ch 5) around the cut.
usage: python forkfig.py fed_pack starved_pack seed out.png"""
import sys, json, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
fed, st, seed, out = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
A = np.load(f"{fed}/frames.npz"); B = np.load(f"{st}/frames.npz"); spf = json.load(open(f"{fed}/metrics.json"))["steps_per_frame"]
times = [59000, 60500, 61000, 61500, 62500, 65000, 80000]
fig, ax = plt.subplots(2, len(times), figsize=(2.1 * len(times), 4.6))
for r, (F, lab) in enumerate(((A, "fed"), (B, "starved"))):
    RF = F["render_f"] * spf
    for j, t in enumerate(times):
        i = int(np.argmin(np.abs(RF - t)))
        img = np.stack([F["render"][i, 5], F["render"][i, 3] * 0.8, F["render"][i, 1]], -1).clip(0, 1)
        ax[r, j].imshow(img); ax[r, j].set_title(f"{lab} t={RF[i]}", fontsize=7); ax[r, j].set_xticks([]); ax[r, j].set_yticks([])
fig.suptitle(f"seed {seed}: substrate feed cut at t=60000 (bottom) vs fed twin (top); red = M wall material, green = wall, blue = catalyst", fontsize=8)
fig.tight_layout(); fig.savefig(out, dpi=90)
