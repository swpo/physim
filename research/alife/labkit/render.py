"""Rendering: fixed-scale channel compositing, contact sheets, track biographies, movies.

Colour scales are fixed for the whole run (global percentiles), never per frame, so
brightness changes on a sheet are real changes in the fields.
"""
from __future__ import annotations

import numpy as np
from PIL import Image, ImageDraw, ImageFont

PALETTE = np.array([
    [0.10, 0.85, 0.95],  # cyan
    [1.00, 0.55, 0.10],  # orange
    [0.95, 0.20, 0.55],  # magenta
    [0.45, 0.95, 0.30],  # green
    [0.95, 0.90, 0.25],  # yellow
    [0.40, 0.45, 1.00],  # blue
    [1.00, 1.00, 1.00],  # white
    [0.60, 0.30, 0.90],  # violet
])

TYPE_COLORS = (np.array([
    [255, 255, 255], [0, 220, 255], [255, 140, 30], [255, 60, 140],
    [120, 240, 80], [250, 230, 60], [110, 120, 255], [180, 90, 230],
]))


def channel_scales(frames, lo_pct=1.0, hi_pct=99.5):
    """Per-channel (lo, hi) over all frames, from a pixel sample. frames: (T, C, H, W)."""
    T, C = frames.shape[:2]
    rng = np.random.default_rng(0)
    scales = []
    for c in range(C):
        x = frames[:, c].reshape(-1)
        if x.size > 2_000_000:
            x = x[rng.integers(0, x.size, 2_000_000)]
        x = x.astype(np.float32)
        lo, hi = np.percentile(x, [lo_pct, hi_pct])
        if hi - lo < 1e-9:
            hi = lo + 1e-9
        scales.append((float(lo), float(hi)))
    return scales


def normalize(fr, scales):
    out = np.empty(fr.shape, np.float32)
    for c, (lo, hi) in enumerate(scales):
        out[c] = np.clip((fr[c] - lo) / (hi - lo), 0, 1)
    return out


def composite(fr_norm):
    """(C, H, W) in [0,1] -> (H, W, 3) uint8. One channel uses a dark-to-bright ramp."""
    C = fr_norm.shape[0]
    if C == 1:
        x = fr_norm[0]
        rgb = np.stack([x ** 0.8, x ** 1.5 * 0.9 + 0.1 * x, 0.35 * x + 0.65 * x ** 3], -1)
    else:
        rgb = np.tensordot(fr_norm.transpose(1, 2, 0), PALETTE[np.arange(C) % len(PALETTE)], axes=1)
        rgb = 1 - np.exp(-1.6 * rgb)  # soft saturation so overlapping channels stay readable
    return (np.clip(rgb, 0, 1) * 255).astype(np.uint8)


def particle_canvas(pos, types, view, size=256, radius=1.5, background=None):
    """Draw particles. view = (x0, y0, x1, y1) in world units."""
    img = Image.new("RGB", (size, size), (8, 8, 12)) if background is None else Image.fromarray(background).resize((size, size))
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = view
    sx = size / (x1 - x0)
    sy = size / (y1 - y0)
    r = max(1.0, radius)
    for i, (x, y) in enumerate(pos):
        px, py = (x - x0) * sx, (y - y0) * sy
        if -r <= px <= size + r and -r <= py <= size + r:
            col = tuple(int(v) for v in TYPE_COLORS[int(types[i]) % len(TYPE_COLORS)]) if types is not None else (230, 230, 230)
            d.ellipse([px - r, py - r, px + r, py + r], fill=col)
    return np.asarray(img)


def _font(size=14):
    for name in ("DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default()


def contact_sheet(images, labels, ncols=6, title=None, tile=None):
    """Grid of RGB images with a label under each."""
    n = len(images)
    ncols = min(ncols, n)
    nrows = int(np.ceil(n / ncols))
    h, w = images[0].shape[:2]
    if tile is not None:
        scale = tile / max(h, w)
        h, w = int(h * scale), int(w * scale)
    pad, lab_h = 4, 18
    top = 26 if title else 0
    sheet = Image.new("RGB", (ncols * (w + pad) + pad, top + nrows * (h + lab_h + pad) + pad), (24, 24, 28))
    d = ImageDraw.Draw(sheet)
    f = _font(13)
    if title:
        d.text((pad, 5), title, fill=(235, 235, 235), font=_font(15))
    for k, (im, lab) in enumerate(zip(images, labels)):
        r, c = divmod(k, ncols)
        x, y = pad + c * (w + pad), top + pad + r * (h + lab_h + pad)
        pim = Image.fromarray(im)
        if pim.size != (w, h):
            pim = pim.resize((w, h), Image.NEAREST)
        sheet.paste(pim, (x, y))
        d.text((x + 2, y + h + 2), lab, fill=(200, 200, 200), font=f)
    return sheet


def crop_periodic(img, cy, cx, half):
    """Periodic crop of an (H, W, 3) image centred at (cy, cx)."""
    H, W = img.shape[:2]
    ys = (np.arange(int(cy) - half, int(cy) + half) % H)
    xs = (np.arange(int(cx) - half, int(cx) + half) % W)
    return img[np.ix_(ys, xs)]


def save_movie(rgb_frames, path, fps=12):
    """MP4 (H.264) via imageio-ffmpeg; returns the path written."""
    import imageio.v2 as imageio

    H, W = rgb_frames[0].shape[:2]
    Hp, Wp = H + (H % 2), W + (W % 2)
    frames = []
    for fr in rgb_frames:
        if (Hp, Wp) != (H, W):
            fr = np.pad(fr, ((0, Hp - H), (0, Wp - W), (0, 0)))
        frames.append(fr)
    imageio.mimwrite(path, frames, fps=fps, codec="libx264", quality=7, macro_block_size=1,
                     ffmpeg_log_level="error")
    return path
