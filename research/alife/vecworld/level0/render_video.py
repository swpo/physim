"""Render a packaged world (labenv python: matplotlib + ffmpeg).
Usage: python render_video.py NAME
Reads scratch/frames_NAME.npz, scratch/snaps_NAME.json, worlds/NAME/metrics.json; writes
worlds/NAME/video.mp4 (H.264 yuv420p, 512 px, <= 3 MB), sheet.png, tracks.png, timeseries.png."""
import json
import os
import subprocess
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render import to_rgb

HERE = os.path.dirname(os.path.abspath(__file__))


def upscale(img, f):
    return np.repeat(np.repeat(img, f, 0), f, 1)


def video(name, frames, every, out, fps=30, crf=24):
    H, W = frames.shape[2:]
    f = max(1, 512 // W)
    S = W * f
    pad = 28
    cmd = ["/usr/bin/ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{S}x{S + pad}", "-r", str(fps), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p",
           "-crf", str(crf), "-preset", "slow", "-movflags", "+faststart", out]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    fig = plt.figure(figsize=(S / 100, (S + pad) / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, S / (S + pad)])
    ax.set_axis_off()
    im = ax.imshow(upscale(to_rgb(frames[0]), f), interpolation="nearest")
    tx = fig.text(0.02, 1 - 0.5 * pad / (S + pad), "", color="white", fontsize=11, va="center", family="monospace")
    fig.text(0.98, 1 - 0.5 * pad / (S + pad), f"{name}  Flow-Lenia level 0, {H}x{W} torus", color="0.7",
             fontsize=9, va="center", ha="right")
    fig.patch.set_facecolor("black")
    for n in range(len(frames)):
        im.set_data(upscale(to_rgb(frames[n]), f))
        tx.set_text(f"step {n * every:5d}")
        fig.canvas.draw()
        buf = np.asarray(fig.canvas.buffer_rgba())[..., :3]
        proc.stdin.write(np.ascontiguousarray(buf).tobytes())
    proc.stdin.close()
    proc.wait()
    plt.close(fig)
    return os.path.getsize(out)


def sheet(name, frames, every, out, n=8):
    idx = np.linspace(0, len(frames) - 1, n).astype(int)
    fig, axs = plt.subplots(2, n // 2, figsize=(2.4 * n // 2, 5.0))
    for ax, i in zip(axs.ravel(), idx):
        ax.imshow(to_rgb(frames[i]), interpolation="nearest")
        ax.set_title(f"step {i * every}", color="white", fontsize=9)
        ax.set_xticks([]); ax.set_yticks([])
    fig.suptitle(f"{name}: level-0 matter (colour = channel)", color="white", fontsize=10)
    fig.patch.set_facecolor("black")
    plt.tight_layout()
    fig.savefig(out, dpi=100, facecolor="black")
    plt.close(fig)


def tracks_png(name, frames, snaps, metrics, out):
    H, W = frames.shape[2:]
    long_ids = {t["id"] for t in metrics["tracks"] if t["life"] >= 0.25 * metrics["steps"]}
    paths = {}
    for s in snaps:
        for b in s["bodies"]:
            paths.setdefault(b["id"], []).append((s["t"], b["cy"], b["cx"], b["mass"]))
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(to_rgb(frames[-1]) * 0.5, interpolation="nearest")
    cmap = plt.get_cmap("tab20")
    for k, (i, P) in enumerate(sorted(paths.items())):
        P = np.array(P)
        if len(P) < 3:
            continue
        lw, al = (1.4, 0.95) if i in long_ids else (0.6, 0.45)
        # break the line where it wraps around the torus
        seg = [0]
        for j in range(1, len(P)):
            jump = max(P[j, 3], P[j - 1, 3]) / max(min(P[j, 3], P[j - 1, 3]), 1e-9) > 1.3
            if abs(P[j, 1] - P[j - 1, 1]) > H / 2 or abs(P[j, 2] - P[j - 1, 2]) > W / 2 or jump:
                seg.append(j)
        seg.append(len(P))
        for a, b in zip(seg[:-1], seg[1:]):
            ax.plot(P[a:b, 2], P[a:b, 1], color=cmap(i % 20), lw=lw, alpha=al)
    ax.set_xlim(-0.5, W - 0.5); ax.set_ylim(H - 0.5, -0.5)
    ax.set_title(f"{name}: body centroid tracks over {metrics['steps']} steps (thick: life >= 25% of run;\n"
                 "lines break at wrap-around and at fusion/fission mass jumps > 30%)", fontsize=8)
    ax.set_xticks([]); ax.set_yticks([])
    plt.tight_layout()
    fig.savefig(out, dpi=110)
    plt.close(fig)


def timeseries_png(name, metrics, out):
    ser = metrics["series"]
    t = np.array([s["t"] for s in ser])
    n = np.array([s["n"] for s in ser])
    cm = np.cumsum([s["merge"] for s in ser])
    cs = np.cumsum([s["split"] for s in ser])
    co = np.array([s["contacts"] for s in ser])
    occ = np.array([s["occ"] for s in ser])
    fig, axs = plt.subplots(3, 1, figsize=(7, 6), sharex=True)
    axs[0].plot(t, n, color="#2a6fdb", lw=1.2, label="bodies")
    axs[0].plot(t, co, color="#d9822b", lw=0.8, label="bodies in contact (pairs)")
    axs[0].legend(fontsize=8, frameon=False); axs[0].set_ylabel("count")
    axs[1].plot(t, cm, color="#2a6fdb", lw=1.2, label="fusions (cumulative)")
    axs[1].plot(t, cs, color="#c23b5a", lw=1.2, label="fissions (cumulative)")
    axs[1].legend(fontsize=8, frameon=False); axs[1].set_ylabel("events")
    axs[2].plot(t, occ, color="#555555", lw=1.0)
    axs[2].set_ylabel("occupancy"); axs[2].set_xlabel("step")
    for ax in axs:
        ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    axs[0].set_title(f"{name}: screens (snapshot every 10 steps)", fontsize=9)
    plt.tight_layout()
    fig.savefig(out, dpi=110)
    plt.close(fig)


def main():
    name = sys.argv[1]
    crf = int(sys.argv[2]) if len(sys.argv) > 2 else 24
    wdir = os.path.join(HERE, "worlds", name)
    d = np.load(os.path.join(HERE, "scratch", f"frames_{name}.npz"))
    frames, every = d["frames"], int(d["every"])
    snaps = json.load(open(os.path.join(HERE, "scratch", f"snaps_{name}.json")))
    metrics = json.load(open(os.path.join(wdir, "metrics.json")))
    sheet(name, frames, every, os.path.join(wdir, "sheet.png"))
    tracks_png(name, frames, snaps, metrics, os.path.join(wdir, "tracks.png"))
    timeseries_png(name, metrics, os.path.join(wdir, "timeseries.png"))
    out = os.path.join(wdir, "video.mp4")
    size = video(name, frames, every, out, crf=crf)
    while size > 3e6 and crf < 40:
        crf += 3
        size = video(name, frames, every, out, crf=crf)
    print(name, "video bytes", size, "crf", crf, "frames", len(frames))


if __name__ == "__main__":
    main()
