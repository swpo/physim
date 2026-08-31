"""render_film.py — house-style MP4 render from a *_film.npz capture.

Layout: one row = na activator field panels (magma/viridis/inferno/cividis)
+ one population panel (total blob count vs t, moving cursor).
Timestamp overlay. ~2.5 fps, ffmpeg -crf 23, yuv420p.

Usage: python render_film.py <film.npz> <out.mp4> [--title "..."] [--fps 2.5]
"""
import argparse, json, os, subprocess, tempfile
import numpy as np
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt

CMAPS = ["magma", "viridis", "inferno", "cividis"]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("npz"); ap.add_argument("out")
    ap.add_argument("--title", default=None)
    ap.add_argument("--fps", type=float, default=2.5)
    ap.add_argument("--crf", type=int, default=23)
    ap.add_argument("--zoom-pop", action="store_true",
                    help="zoom population panel to the snapshot window (slomo)")
    a = ap.parse_args()

    d = np.load(a.npz, allow_pickle=True)
    frames = np.asarray(d["frames"], np.float32)      # (nf, na, N, N)
    ts = np.asarray(d["ts"], float)
    rec_ts, rec_ct = np.asarray(d["rec_ts"], float), np.asarray(d["rec_ct"], float)
    na = int(d["na"]); name = str(d["name"])
    g = json.loads(str(d["genome"]))
    title = a.title or name

    nf = frames.shape[0]
    # per-channel fixed color scale (robust percentiles across the whole film)
    vlims = []
    for i in range(na):
        ch = frames[:, i]
        vlims.append((np.percentile(ch, 0.5), np.percentile(ch, 99.8)))

    ncol = na + 1
    panel = 3.4
    fig_w, fig_h = panel * ncol, panel + 0.55
    tmp = tempfile.mkdtemp(prefix="film_")
    if a.zoom_pop and len(rec_ts):          # slomo: window-local pop panel
        m = (rec_ts >= ts.min() - 1e-9) & (rec_ts <= ts.max() + 1e-9)
        rec_ts, rec_ct = rec_ts[m], rec_ct[m]
    ct_max = max(rec_ct.max(), 1.0) if len(rec_ct) else 1.0
    ct_min = min(rec_ct.min(), ct_max) if len(rec_ct) else 0.0

    for k in range(nf):
        fig, axes = plt.subplots(1, ncol, figsize=(fig_w, fig_h))
        if ncol == 1: axes = [axes]
        for i in range(na):
            ax = axes[i]
            ax.imshow(frames[k, i], cmap=CMAPS[i % len(CMAPS)],
                      vmin=vlims[i][0], vmax=vlims[i][1],
                      origin="lower", interpolation="nearest")
            ax.set_xticks([]); ax.set_yticks([])
            ax.set_title(f"species {i+1} (u{i+1})", fontsize=10)
        # timestamp overlay on first panel
        axes[0].text(0.03, 0.965, f"t = {ts[k]:,.0f} tu", transform=axes[0].transAxes,
                     fontsize=11, color="w", va="top", fontweight="bold",
                     bbox=dict(facecolor="k", alpha=0.55, pad=3, edgecolor="none"))
        # population panel
        axp = axes[-1]
        if len(rec_ts):
            axp.plot(rec_ts, rec_ct, color="#0969da", lw=1.2)
            axp.axvline(ts[k], color="#d43a2f", lw=1.0)
            axp.set_xlim((ts.min() if a.zoom_pop else 0),
                         max(rec_ts.max(), ts.max()))
            axp.set_ylim((max(0.0, ct_min * 0.92) if a.zoom_pop else 0),
                         ct_max * 1.08)
        axp.set_title("blob count", fontsize=10)
        axp.tick_params(labelsize=8)
        axp.set_xlabel("t (tu)", fontsize=8)
        fig.suptitle(title, fontsize=12, y=0.995)
        fig.tight_layout(rect=(0, 0, 1, 0.96))
        fig.savefig(os.path.join(tmp, f"f_{k:04d}.png"), dpi=100)
        plt.close(fig)

    subprocess.run([
        "ffmpeg", "-y", "-framerate", str(a.fps),
        "-i", os.path.join(tmp, "f_%04d.png"),
        "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2,format=yuv420p",
        "-c:v", "libx264", "-crf", str(a.crf), "-movflags", "+faststart",
        a.out], check=True, capture_output=True)
    sz = os.path.getsize(a.out) / 1e6
    print(f"[{name}] {nf} frames -> {a.out} ({sz:.2f} MB)")
    for f in os.listdir(tmp): os.remove(os.path.join(tmp, f))
    os.rmdir(tmp)

if __name__ == "__main__":
    main()
