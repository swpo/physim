"""Steer video from results/steer_video_frames.npz (VW-1 twin pair), drawn with the VW-0 helpers
(integrate/render_l1.py glyphs, make_videos.Pipe, level0 render.to_rgb), read only.

usage: python -B render_steer.py   -> media/steer.mp4, media/steer.jpg
Panels (each rolled on the torus so that the target starts at the centre): level 0 of the no-input
twin | level 0 with the steering input (sources red, sinks green on the ticks they act) | level 1:
the steered glider (colour) and its track against the twin's glider and track (grey)."""
import json
import os
import subprocess

import common as CM
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

import render_l1 as R      # noqa: E402  (VW-0 drawing helpers, read only)
import make_videos as MV   # noqa: E402

os.makedirs(f"{CM.RES}/check", exist_ok=True)
d = np.load(f"{CM.RES}/steer_video_frames.npz")
Ft, Fs = d["twin"], d["steered"]
tt, ts = d["tab_twin"], d["tab_steered"]
Yt, Ys = d["L1_twin"][:, CM.NC:], d["L1_steered"][:, CM.NC:]
cells = d["cells"]
s = int(d["slot"])
strat = str(d["strategy"])
summ = json.load(open(f"{CM.RES}/steer.json"))["summary"]
vr = summ["video_run"]
K, UID = CM.K, CM.NF + 4
uid0 = tt[0, s, UID]
cy0, cx0 = tt[0, s, CM.NF], tt[0, s, CM.NF + 1]
sy, sx = int(round(64 - cy0)), int(round(64 - cx0))


def alive(tab, k):
    return tab[k, s, 0] > 0.5 and tab[k, s, UID] == uid0


def path(tab):
    P, cur, last = [], None, None
    for k in range(len(tab)):
        if not alive(tab, k):
            break
        p = np.array([tab[k, s, CM.NF + 1], tab[k, s, CM.NF]])        # (x, y)
        if cur is None:
            cur = np.array([64.0, 64.0]) + CM.mi(p - [cx0, cy0], 128.0)
        else:
            cur = cur + CM.mi(p - last, 128.0)
        last = p
        P.append(cur.copy())
    return np.array(P)


def shifted(objs):
    out = []
    for o in objs:
        o = dict(o)
        o["cx"], o["cy"] = (o["cx"] + sx) % 128, (o["cy"] + sy) % 128
        out.append(o)
    return out


Pt, Ps = path(tt), path(ts)
ORANGE = "#ff8c1a"
NTf = min(len(Fs), int(vr["survived_ticks"]) + 2)      # stop once the target's track identity is gone
Wpx, Hpx = 900, 300 + 64
fig = plt.figure(figsize=(Wpx / 100, Hpx / 100), dpi=100)
fig.patch.set_facecolor("black")
axs = [fig.add_axes([i / 3, 0, 1 / 3, 300 / Hpx]) for i in range(3)]
hdr = fig.text(0.01, 1 - 14 / Hpx, "", color="white", fontsize=9.5, va="center", family="monospace")
for i, txt in enumerate(["level 0, no input (twin)", "level 0, with input (k=8, +-0.5, zero sum)",
                         "level 1: steered glider and track vs twin"]):
    fig.text((i + 0.5) / 3, 1 - 44 / Hpx, txt, color="0.8", fontsize=8.5, ha="center", va="center")


def draw(k):
    for ax in axs:
        ax.cla()
        R.setup_ax(ax)
    axs[0].imshow(np.roll(R.to_rgb(Ft[k]), (sy, sx), (0, 1)), interpolation="nearest")
    axs[1].imshow(np.roll(R.to_rgb(Fs[k]), (sy, sx), (0, 1)), interpolation="nearest")
    if k < len(cells) and cells[k][0] >= 0:
        c = cells[k]
        ys, xs = (c // 128 + sy) % 128, (c % 128 + sx) % 128
        axs[1].scatter(xs[:4], ys[:4], s=18, facecolors="none", edgecolors="red", lw=1.1)
        axs[1].scatter(xs[4:], ys[4:], s=18, facecolors="none", edgecolors="lime", lw=1.1)
    ot = [o for o in shifted(R.decode_slots(Yt[k], K)) if o["slot"] == s and alive(tt, k)]
    os_ = shifted(R.decode_slots(Ys[k], K))
    others = [o for o in os_ if o["slot"] != s]
    tgt = [o for o in os_ if o["slot"] == s and alive(ts, k)]
    R.draw_objects(axs[2], others, None, alpha=0.3, label=False)
    R.draw_objects(axs[2], ot, None, color="0.6", fill=False, label=False)
    R.draw_objects(axs[2], tgt, None, color=ORANGE, label=False)
    kk = min(k + 1, len(Pt))
    if kk >= 2:
        axs[2].plot(Pt[:kk, 0], Pt[:kk, 1], color="0.6", lw=1.3)
    kk = min(k + 1, len(Ps))
    if kk >= 2:
        axs[2].plot(Ps[:kk, 0], Ps[:kk, 1], color=ORANGE, lw=1.8)
    axs[2].text(4, 122, "orange: with input   grey: twin", color="0.85", fontsize=7.5, va="bottom",
                bbox=dict(facecolor="black", alpha=0.6, lw=0))
    on = k < len(cells) and cells[k][0] >= 0
    hdr.set_text(f"VW-1 A_gliders  steering program '{strat}'  tick {k:2d}   "
                 + ("input ON: red = sources, green = sinks" if on else "input off"))


out = f"{CM.MEDIA}/steer.mp4"
for crf in (26, 30, 34):
    pipe = MV.Pipe(out, Wpx, Hpx, crf, fps=4)
    for k in range(NTf):
        draw(k)
        pipe.write(fig)
    size = pipe.close()
    if size < 2.4e6:
        break
kp = int(min(vr["survived_ticks"], NTf - 1))
draw(kp)
fig.savefig(f"{CM.MEDIA}/steer.jpg", dpi=100, facecolor="black", pil_kwargs={"quality": 88})
for k in (0, NTf // 2, kp):
    draw(k)
    fig.savefig(f"{CM.RES}/check/steer_frame_{k:02d}.png", dpi=100, facecolor="black")
plt.close(fig)
probe = subprocess.run(["/usr/bin/ffprobe", "-v", "error", "-show_entries", "stream=codec_name,pix_fmt,width,height,nb_frames",
                        "-of", "json", out], capture_output=True, text=True).stdout
print("steer video bytes", size, "crf", crf, probe, "poster tick", kp)
