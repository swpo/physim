"""Particle movie from a lineage snapshot file: python movie.py TAG [size] -> screens/TAG.mp4 (+ poster png).
Food grey, core kind 0 cyan, membrane orange, core kind 1 magenta."""
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from labkit import render as R  # noqa: E402

COL = {0: (70, 70, 80), 1: (0, 210, 255), 2: (255, 150, 30), 3: (255, 50, 150)}
RAD = {0: 1.0, 1: 1.8, 2: 1.8, 3: 1.8}


def frame(x, t, L, size, label):
    img = Image.new("RGB", (size, size), (6, 6, 10))
    d = ImageDraw.Draw(img)
    sc = size / L
    for k in (0, 2, 1, 3):
        for px, py in x[t == k] * sc:
            r = RAD[k] * size / 512
            d.ellipse([px - r, py - r, px + r, py + r], fill=COL[k])
    d.text((8, 6), label, fill=(220, 220, 220), font=R._font(max(12, size // 40)))
    return np.asarray(img)


def main():
    tag = sys.argv[1]
    size = int(sys.argv[2]) if len(sys.argv) > 2 else 512
    z = np.load(f"scratch/{tag}_snaps.npz")
    L, dt = float(z["L"]), float(z["dt"])
    X, T = z["x"].astype(np.float32), z["t"]
    frames = [frame(X[k], T[k], L, size, f"{tag}  t={k * dt:.0f}") for k in range(len(X))]
    R.save_movie(frames, f"scratch/{tag}_raw.mp4", fps=15)
    import subprocess
    import imageio_ffmpeg
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-loglevel", "error", "-y", "-i", f"scratch/{tag}_raw.mp4",
                    "-c:v", "libx264", "-crf", "32", "-preset", "slow", "-pix_fmt", "yuv420p", f"screens/{tag}.mp4"], check=True)
    pick = np.linspace(0, len(frames) - 1, 6).astype(int)
    R.contact_sheet([frames[k] for k in pick], [f"t={k * dt:.0f}" for k in pick], ncols=6,
                    title=f"{tag}: grey food, cyan core (kind 0), orange membrane, magenta core (kind 1)").save(f"screens/{tag}_poster.png")
    print("wrote", f"screens/{tag}.mp4", len(frames), "frames")


if __name__ == "__main__":
    main()
