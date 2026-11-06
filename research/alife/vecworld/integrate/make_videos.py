"""Videos and posters (labenv python + ffmpeg).

usage: python make_videos.py WORLD [steer]
  videos/WORLD_objects.mp4   level 0 | level 1 (Phi_objects glyphs) | strip: the agent's view
  videos/WORLD_coarse.mp4    level 0 | level 1 (Phi_coarse blocks)   | strip: the agent's view
  videos/WORLD_poster.png    4 times x (level 0, Phi_objects, Phi_coarse)
  steer: videos/WORLD_steer.mp4  twin without input | with input (sites marked) | level 1 of both
"""
import json
import os
import subprocess
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import render_l1 as R

FPS = 15


class Pipe:
    def __init__(self, out, w, h, crf, fps=FPS):
        self.out = out
        self.p = subprocess.Popen(["/usr/bin/ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt",
                                   "rgb24", "-s", f"{w}x{h}", "-r", str(fps), "-i", "-", "-c:v", "libx264",
                                   "-pix_fmt", "yuv420p", "-crf", str(crf), "-preset", "slow", "-movflags",
                                   "+faststart", out], stdin=subprocess.PIPE)

    def write(self, fig):
        fig.canvas.draw()
        buf = np.asarray(fig.canvas.buffer_rgba())[..., :3]
        self.p.stdin.write(np.ascontiguousarray(buf).tobytes())

    def close(self):
        self.p.stdin.close()
        self.p.wait()
        return os.path.getsize(self.out)


def trails_for(Yo, tab, t, K, n=12):
    tr = {}
    uid_now = {s: tab[t, s, 4] for s in range(K)}
    for tt in range(max(0, t - n), t + 1):
        for o in R.decode_slots(Yo[tt], K):
            if tab[tt, o["slot"], 4] == uid_now[o["slot"]]:
                tr.setdefault(o["slot"], []).append((o["cx"], o["cy"]))
    return tr


def agent_view(Y, perm, t, n=48):
    """The last n observations o(t) = permuted h1, standardised per coordinate (time runs down)."""
    lo = max(0, t - n + 1)
    Z = Y[lo:t + 1][:, perm]
    img = np.zeros((n, Z.shape[1]))
    img[n - len(Z):] = Z
    return img


def world_video(name, phi, frames, Yo, Yc, tab, K, perm, sd, out, crf=26):
    Wpx, Hpx = 896, 34 + 448 + 20 + 88
    fig = plt.figure(figsize=(Wpx / 100, Hpx / 100), dpi=100)
    fig.patch.set_facecolor("black")
    pb = (20 + 88) / Hpx
    a0 = fig.add_axes([0, pb, 0.5, 448 / Hpx])
    a1 = fig.add_axes([0.5, pb, 0.5, 448 / Hpx])
    a2 = fig.add_axes([0.0, 0.0, 1.0, 88 / Hpx])
    t_hdr = fig.text(0.01, 1 - 17 / Hpx, "", color="white", fontsize=10, va="center", family="monospace")
    lab = (f"level 1: Phi_objects, {K} tracked slots (glyph: disc ~ mass, white tick = orientation, "
           "arrow = velocity, trail)" if phi == "objects" else "level 1: Phi_coarse, 8x8 block means of the "
           "two channels (second moments not drawn)")
    fig.text(0.99, 1 - 17 / Hpx, lab, color="0.75", fontsize=8, ha="right", va="center")
    Y = Yo if phi == "objects" else Yc
    fig.text(0.01, 10 / Hpx + 88 / Hpx, f"what the agent sees: the last 48 observations o(t), {Y.shape[1]} "
             "coordinates in a hidden permuted order (standardised for display; newest at the bottom)",
             color="0.85", fontsize=8, va="center")
    Z = (Y - Y.mean(0)) / sd
    pipe = Pipe(out, Wpx, Hpx, crf)
    for t in range(len(frames)):
        for ax in (a0, a1, a2):
            ax.cla()
        R.setup_ax(a0)
        a0.imshow(R.to_rgb(frames[t]), interpolation="nearest")
        a0.text(2, 4, "level 0 (hidden): Flow-Lenia matter", color="white", fontsize=8, va="top",
                bbox=dict(facecolor="black", alpha=0.6, lw=0))
        R.setup_ax(a1)
        if phi == "objects":
            R.draw_objects(a1, R.decode_slots(Yo[t], K), trails_for(Yo, tab, t, K))
        else:
            a1.imshow(R.coarse_rgb(Yc[t]), interpolation="nearest")
        a1.text(2, 4, "level 1 (designer render)", color="white", fontsize=8, va="top",
                bbox=dict(facecolor="black", alpha=0.6, lw=0))
        a2.imshow(agent_view(Z, perm, t), aspect="auto", cmap="RdBu_r", vmin=-2.5, vmax=2.5,
                  interpolation="nearest")
        a2.set_xticks([])
        a2.set_yticks([])
        t_hdr.set_text(f"{name}  tick {t:3d}  (step {20 * t:4d})")
        pipe.write(fig)
    plt.close(fig)
    return pipe.close()


def poster(name, frames, Yo, Yc, tab, K, out):
    ts = np.linspace(10, len(frames) - 1, 4).astype(int)
    fig, axs = plt.subplots(3, 4, figsize=(12, 9.4))
    fig.patch.set_facecolor("black")
    for c, t in enumerate(ts):
        R.setup_ax(axs[0, c])
        axs[0, c].imshow(R.to_rgb(frames[t]), interpolation="nearest")
        axs[0, c].set_title(f"tick {t} (step {20 * t})", color="white", fontsize=9)
        R.setup_ax(axs[1, c])
        R.draw_objects(axs[1, c], R.decode_slots(Yo[t], K), trails_for(Yo, tab, t, K, 20))
        R.setup_ax(axs[2, c])
        axs[2, c].imshow(R.coarse_rgb(Yc[t]), interpolation="nearest")
    for r, txt in enumerate(["level 0 (hidden)", "level 1: Phi_objects", "level 1: Phi_coarse"]):
        axs[r, 0].set_ylabel(txt, color="white", fontsize=10)
    fig.suptitle(f"{name}: one Flow-Lenia world, two coarse-grainings (designer renders; the agent sees "
                 "only permuted vectors)", color="white", fontsize=11)
    plt.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(out, dpi=90, facecolor="black")
    plt.close(fig)


def steer_video(name, d, K, out, key="lead+", crf=26):
    """Twin without input | same state and noise with the steering input | level 1 of both.
    Every panel is rolled on the torus so that the target starts at the centre."""
    Ft, Fs = d["none__frames"], d[f"{key}__frames"]
    s = int(d["target"])
    Ys_, Yt_ = d[f"{key}__Yo"], d["none__Yo"]
    cells = d[f"{key}__cells"]
    tab_s, tab_t = d[f"{key}__tab"], d["none__tab"]
    o0 = [o for o in R.decode_slots(Yt_[0], K) if o["slot"] == s][0]
    sy, sx = int(round(64 - o0["cy"])), int(round(64 - o0["cx"]))
    uid0 = tab_t[0, s, R.NF + 4]

    def shifted(objs):
        out_ = []
        for o in objs:
            o = dict(o)
            o["cx"], o["cy"] = (o["cx"] + sx) % 128, (o["cy"] + sy) % 128
            out_.append(o)
        return out_

    def target_path(Y, tab):
        P, last = [], None
        for k in range(len(Y)):
            if tab[k, s, 0] < 0.5 or tab[k, s, R.NF + 4] != uid0:
                break
            o = [q for q in R.decode_slots(Y[k], K) if q["slot"] == s][0]
            p = np.array([o["cx"], o["cy"]])
            if last is None:
                cur = np.array([64.0, 64.0]) + ((p + [sx, sy]) % 128 - 64)
            else:
                cur = cur + ((p - last + 64) % 128 - 64)
            last = p
            P.append(cur.copy())
        return np.array(P)
    Pt, Ps = target_path(Yt_, tab_t), target_path(Ys_, tab_s)
    Wpx, Hpx = 900, 300 + 64
    fig = plt.figure(figsize=(Wpx / 100, Hpx / 100), dpi=100)
    fig.patch.set_facecolor("black")
    axs = [fig.add_axes([i / 3, 0, 1 / 3, 300 / Hpx]) for i in range(3)]
    hdr = fig.text(0.01, 1 - 14 / Hpx, "", color="white", fontsize=9.5, va="center", family="monospace")
    for i, txt in enumerate(["level 0, no input (twin)", "level 0, with input (k=8, +-0.5, zero sum)",
                             "level 1: target, twin (grey) vs with input"]):
        fig.text((i + 0.5) / 3, 1 - 44 / Hpx, txt, color="0.8", fontsize=8.5, ha="center", va="center")
    pipe = Pipe(out, Wpx, Hpx, crf, fps=5)
    for k in range(len(Fs)):
        for ax in axs:
            ax.cla()
            R.setup_ax(ax)
        axs[0].imshow(np.roll(R.to_rgb(Ft[k]), (sy, sx), (0, 1)), interpolation="nearest")
        axs[1].imshow(np.roll(R.to_rgb(Fs[k]), (sy, sx), (0, 1)), interpolation="nearest")
        if k < len(cells) and cells[k][0] >= 0:
            c = cells[k]
            ys, xs = (c // 128 + sy) % 128, (c % 128 + sx) % 128
            axs[1].scatter(xs[:4], ys[:4], s=16, facecolors="none", edgecolors="red", lw=1.0)
            axs[1].scatter(xs[4:], ys[4:], s=16, facecolors="none", edgecolors="lime", lw=1.0)
        if k > 0:
            ot = [o for o in shifted(R.decode_slots(Yt_[k - 1], K)) if o["slot"] == s and tab_t[k - 1, s, R.NF + 4] == uid0]
            os_ = shifted(R.decode_slots(Ys_[k - 1], K))
            others = [o for o in os_ if o["slot"] != s]
            tgt = [o for o in os_ if o["slot"] == s and tab_s[k - 1, s, R.NF + 4] == uid0]
            R.draw_objects(axs[2], others, None, alpha=0.3, label=False)
            R.draw_objects(axs[2], ot, None, color="0.6", fill=False, label=False)
            R.draw_objects(axs[2], tgt, None)
            kk = min(k, len(Pt))
            if kk >= 2:
                axs[2].plot(Pt[:kk, 0], Pt[:kk, 1], color="0.6", lw=1.3)
            kk = min(k, len(Ps))
            if kk >= 2:
                axs[2].plot(Ps[:kk, 0], Ps[:kk, 1], color=R.slot_color(s), lw=1.6)
        hdr.set_text(f"{name}  steering slot {s} (program '{key}')  tick {k:2d}   "
                     f"red = sources, green = sinks")
        pipe.write(fig)
    plt.close(fig)
    return pipe.close()


def main():
    name = sys.argv[1]
    os.makedirs("videos", exist_ok=True)
    meta = np.load(f"data/{name}/render_meta.npz")
    K = int(meta["K"])
    if len(sys.argv) > 2 and sys.argv[2] == "steer":
        j = int(meta['steer_video_j'])
        f = f"data/{name}/steer_{j:03d}_s2_video.npz"
        d = np.load(f if os.path.exists(f) else f"data/{name}/steer_{j:03d}_s2.npz")
        key = str(meta["steer_video_key"])
        for crf in (26, 30, 34):
            size = steer_video(name, d, K, f"videos/{name}_steer.mp4", key=key, crf=crf)
            if size < 3e6:
                break
        print("steer video", size)
        return
    b = np.load(f"data/{name}/base_000.npz")
    frames = np.load(f"data/{name}/frames_000.npz")["A"]
    Yo, Yc, tab = b["Yo"], b["Yc"], b["tab"]
    poster(name, frames, Yo, Yc, tab, K, f"videos/{name}_poster.png")
    for phi, perm, sd in (("objects", meta["perm_objects"], meta["sd_objects"]),
                          ("coarse", meta["perm_coarse"], meta["sd_coarse"])):
        for crf in (26, 30, 34, 38):
            size = world_video(name, phi, frames, Yo, Yc, tab, K, perm, sd, f"videos/{name}_{phi}.mp4", crf=crf)
            if size < 3e6:
                break
        print(phi, "video bytes", size, "crf", crf)


if __name__ == "__main__":
    main()
