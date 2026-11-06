"""A fusion followed by a fission in the hero objects episode (fresh VW-1 agent episode; designer side).

usage: python -B events_fig.py SEED [T_FUSION]   -> media/A_gliders_fusion_fission.png, results/events_fig.json
Finds fusions (tracker event 3 on the survivor, -1 on the absorbed slot) whose survivor then runs
event-free for >= 4 ticks and ends in a fission (event 2), and draws level 0 (top) and the Phi_objects
glyphs (bottom) in a 64 x 64 window centred on the merged body.
"""
import json
import sys

sys.path.insert(0, "/home/user/evalwork/vecworld/integrate")
import numpy as np  # noqa: E402
import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

import render_l1 as R  # noqa: E402
import make_videos as MV  # noqa: E402

BASE = "/home/user/evalwork/vecworld/vw1/fresh/media"
seed = int(sys.argv[1])
h = np.load(f"{BASE}/results/hero_objects_s{seed}.npz")
X, L1, tab = h["x"], h["L1"], h["tab"]
K, NF = 12, 12
S = L1.reshape(len(L1), K, NF)
pres, ev, uid = S[:, :, 0] > 0.5, tab[:, :, 3], tab[:, :, 4]
cands = []
for t in range(1, len(L1)):
    for s in np.flatnonzero(pres[t] & (ev[t] == 3)):
        u, t2 = uid[t, s], t + 1
        while t2 < len(L1) and pres[t2, s] and uid[t2, s] == u and ev[t2, s] == 0:
            t2 += 1
        if t2 < len(L1) and pres[t2, s] and uid[t2, s] == u and ev[t2, s] == 2 and t2 - t >= 4 and t >= 6 and t2 + 6 < len(L1):
            cands.append({"t_fusion": t, "t_fission": t2, "slot": int(s), "absorbed": [int(a) for a in np.flatnonzero(ev[t] == -1)],
                          "worm_mass": float(S[t, s, 1]), "worm_elongation": float(np.hypot(S[t, s, 8], S[t, s, 9]))})
if len(sys.argv) > 2:
    c = [c for c in cands if c["t_fusion"] == int(sys.argv[2])][0]
else:
    good = [c for c in cands if 6 <= c["t_fission"] - c["t_fusion"] <= 30] or cands
    c = max(good, key=lambda c: c["worm_mass"])
t1, t2, s = c["t_fusion"], c["t_fission"], c["slot"]
ticks = [t1 - 6, t1 - 2, t1, (t1 + t2) // 2, t2, t2 + 5]
o = [q for q in R.decode_slots(L1[t1], K) if q["slot"] == s][0]
sy, sx = int(round(64 - o["cy"])), int(round(64 - o["cx"]))
fig, axs = plt.subplots(2, len(ticks), figsize=(9.6, 3.62), dpi=100)
fig.subplots_adjust(left=0.025, right=0.998, top=0.86, bottom=0.005, wspace=0.02, hspace=0.02)
fig.patch.set_facecolor("black")
for i, t in enumerate(ticks):
    a, b = axs[0, i], axs[1, i]
    R.setup_ax(a)
    a.imshow(np.roll(R.to_rgb(X[t]), (sy, sx), (0, 1)), interpolation="nearest")
    R.setup_ax(b)
    objs = []
    for q in R.decode_slots(L1[t], K):
        q = dict(q)
        q["cx"], q["cy"] = (q["cx"] + sx) % 128, (q["cy"] + sy) % 128
        objs.append(q)
    tr = {k: [((x + sx) % 128, (y + sy) % 128) for x, y in v] for k, v in MV.trails_for(L1, tab, t, K, 8).items()}
    R.draw_objects(b, objs, tr)
    for ax in (a, b):
        ax.set_xlim(31.5, 95.5)
        ax.set_ylim(95.5, 31.5)
        for art in list(ax.texts) + list(ax.patches) + list(ax.lines):
            art.set_clip_on(True)
            art.set_clip_box(ax.bbox)
    tag = {t1: "fusion", t2: "fission"}.get(t, "")
    a.set_title(f"tick {t}" + (f"  {tag}" if tag else ""), color="white", fontsize=8.5)
axs[0, 0].set_ylabel("level 0", color="white", fontsize=8.5)
axs[1, 0].set_ylabel("Phi_objects", color="white", fontsize=8.5)
fig.suptitle(y=0.985, t=f"VW-1 agent episode (seed {seed}): slots {c['absorbed']} and {s} fuse at tick {t1} into one body (slot {s}), "
             f"which splits again at tick {t2}  (64 x 64 px window)", color="0.85", fontsize=8.5)
out = f"{BASE}/media/A_gliders_fusion_fission.png"
fig.savefig(out, dpi=100, facecolor="black")
json.dump({"chosen": c, "ticks_drawn": ticks, "n_candidates": len(cands), "candidates": cands, "file": out},
          open(f"{BASE}/results/events_fig.json", "w"), indent=1)
print(json.dumps(c), len(cands))
