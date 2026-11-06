"""Hero videos + posters from the fresh VW-1 agent episodes (hero_run.py output), in the style of
integrate/make_videos.py (its Pipe and trails_for, and the render_l1 glyphs, reused read-only).

usage: python -B render_hero.py SEED POSTER_TICK
  media/A_gliders_objects.mp4/.jpg   level 0 | Phi_objects glyphs (designer render) | agent strip
  media/A_gliders_coarse.mp4/.jpg    level 0 | Phi_coarse 8x8 blocks (designer render) | agent strip
The strip is the observation vectors World.reset/World.step returned, columns in the agent's own
(permuted) order, each coordinate standardised over the episode for display only.
"""
import json
import os
import sys

sys.path.insert(0, "/home/user/evalwork/vecworld/integrate")
import numpy as np  # noqa: E402
import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

import render_l1 as R  # noqa: E402   (VW-0 drawing helpers, read only)
import make_videos as MV  # noqa: E402   (Pipe, trails_for; read only)

BASE = "/home/user/evalwork/vecworld/vw1/fresh/media"
seed, t_poster = int(sys.argv[1]), int(sys.argv[2])
K = 12
CMAP = plt.get_cmap("RdBu_r").copy()
CMAP.set_bad("black")


def strip(Z, t, n=48):
    img = np.full((n, Z.shape[1]), np.nan)       # rows before o(0): no observation yet (drawn black)
    lo = max(0, t - n + 1)
    img[n - (t + 1 - lo):] = Z[lo:t + 1]
    return img


def video(view, out, crf, poster_out=None):
    h = np.load(f"{BASE}/results/hero_{view}_s{seed}.npz")
    X, L1, O = h["x"], h["L1"], h["obs64"]
    tab = h["tab"] if view == "objects" else None
    sd = O.std(0)
    Z = (O - O.mean(0)) / np.where(sd > 0, sd, 1.0)
    Wpx, Hpx = 896, 34 + 448 + 20 + 88
    fig = plt.figure(figsize=(Wpx / 100, Hpx / 100), dpi=100)
    fig.patch.set_facecolor("black")
    pb = (20 + 88) / Hpx
    a0 = fig.add_axes([0, pb, 0.5, 448 / Hpx])
    a1 = fig.add_axes([0.5, pb, 0.5, 448 / Hpx])
    a2 = fig.add_axes([0.0, 0.0, 1.0, 88 / Hpx])
    hdr = fig.text(0.01, 1 - 17 / Hpx, "", color="white", fontsize=10, va="center", family="monospace")
    lab = (f"level 1: Phi_objects, {K} tracked slots (glyph: disc ~ mass, white tick = orientation, "
           "arrow = velocity, trail)" if view == "objects" else "level 1: Phi_coarse, 8x8 block means of the "
           "two channels (second moments not drawn)")
    fig.text(0.99, 1 - 17 / Hpx, lab, color="0.75", fontsize=8, ha="right", va="center")
    fig.text(0.01, 10 / Hpx + 88 / Hpx, f"what the agent receives: the last 48 vectors o(t) returned by World.step, "
             f"{O.shape[1]} coordinates in its hidden permuted order (standardised for display; newest at the bottom)",
             color="0.85", fontsize=8, va="center")
    pipe = MV.Pipe(out, Wpx, Hpx, crf)
    for t in range(len(X)):
        for ax in (a0, a1, a2):
            ax.cla()
        R.setup_ax(a0)
        a0.imshow(R.to_rgb(X[t]), interpolation="nearest")
        a0.text(2, 4, f"level 0 (hidden): Flow-Lenia matter (agent episode, seed {seed})", color="white", fontsize=8, va="top",
                bbox=dict(facecolor="black", alpha=0.6, lw=0))
        R.setup_ax(a1)
        if view == "objects":
            R.draw_objects(a1, R.decode_slots(L1[t], K), MV.trails_for(L1, tab, t, K))
        else:
            a1.imshow(R.coarse_rgb(L1[t]), interpolation="nearest")
        a1.text(2, 4, "level 1 (designer render)", color="white", fontsize=8, va="top",
                bbox=dict(facecolor="black", alpha=0.6, lw=0))
        a2.imshow(strip(Z, t), aspect="auto", cmap=CMAP, vmin=-2.5, vmax=2.5, interpolation="nearest")
        a2.set_xticks([])
        a2.set_yticks([])
        hdr.set_text(f"VW-1 A_gliders  tick {t:3d}  (step {20 * t:4d})")
        pipe.write(fig)
        if poster_out and t == t_poster:
            fig.savefig(poster_out, dpi=100, facecolor="black", pil_kwargs={"quality": 88})
    plt.close(fig)
    return pipe.close(), len(X)


res = {}
for view in ("objects", "coarse"):
    out = f"{BASE}/media/A_gliders_{view}.mp4"
    for crf in (26, 30, 34, 38):
        size, nfr = video(view, out, crf, poster_out=f"{BASE}/media/A_gliders_{view}.jpg")
        if size <= 2.5e6:
            break
    res[view] = {"file": out, "bytes": size, "crf": crf, "frames": nfr, "poster": f"{BASE}/media/A_gliders_{view}.jpg",
                 "poster_tick": t_poster, "poster_bytes": os.path.getsize(f"{BASE}/media/A_gliders_{view}.jpg")}
    print(view, res[view], flush=True)
json.dump(res, open(f"{BASE}/results/render_hero.json", "w"), indent=1)
