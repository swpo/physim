"""PhySim v2 teaser, concept B "the dissolve".

One continuous flat image, built from one real VW-1 episode (media/results/hero_coarse_s0.npz, seed 0,
the agent run of media/scripts/hero_run.py). Reading upward:

  bottom   level 0: the Flow-Lenia matter at one tick, bicubic between cells. The frame is cut into
           tiles of the same torus at the same instant, each rolled to a different stretch of rows
           (landscape: two full 128-column periods, 7.5 px/cell; portrait: two 64-column halves of one
           period, 8.44 px/cell). Each join sits in a column corridor that is empty in both tiles, so
           no glider is cut by it.
  rising   the same field as the literal 1-cell lattice, then 2x2, 4x4, 8x8 and finally the 16x16
           blocks of Phi_coarse: block means on the true torus grid, coloured with level0/render.py's
           to_rgb, with integrate/render_l1.py coarse_rgb's 1.6 gain and dark block seams at the top
           level, each level slightly dimmer and greyer. Every block switches on along a ragged
           seeded frontier with a slow horizontal swell, so no level has a hard edge.
  top      what the agent receives: 192 columns, one per coordinate of o(t) in its own hidden permuted
           order (obs = round(L1[out_map], 3)), each a thread of light whose tone is that coordinate's
           value now (standardised over the episode, as in media/scripts/render_hero.py's strip, with
           a quarter of its own past mixed in going up). The threads fray out of the blocks and fade
           into the dark where the title sits.

Type: Instrument Serif (Regular / Italic, OFL), copied into ./fonts from the canvas-design font folder.

usage: nice -n 10 env OMP_NUM_THREADS=1 python -B make_cover.py [landscape|portrait|both] [suffix]
  writes cover{suffix}.png (1920x1080) and cover_portrait{suffix}.png (1080x1350) next to this script.
"""
import os
import sys

import numpy as np
from scipy import ndimage
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.font_manager import FontProperties  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RES = "/home/user/evalwork/vecworld/vw1/fresh/media/results"
FONT_DIRS = [os.path.join(HERE, "fonts"), "/mnt/skills/examples/canvas-design/canvas-fonts"]
N = 128                                                     # torus side (cells)
PAL = np.array([[0.15, 0.85, 1.0], [1.0, 0.45, 0.1]])      # level0/render.py PAL[2]: cyan, orange


def to_rgb(A, scale=0.6):
    """level0/render.py to_rgb (channel-last): saturating additive colour mix on black."""
    return 1.0 - np.exp(-np.tensordot(A, PAL, axes=(-1, 0)) / scale)


def block_means(x, b):
    """(2,N,N) -> (N/b, N/b, 2) block means on the true torus grid (origin 0), as Phi_coarse."""
    return np.moveaxis(x.reshape(2, N // b, b, N // b, b).mean((2, 4)), 0, -1)


def smoothstep(a, b, v):
    s = np.clip((v - a) / (b - a), 0, 1)
    return s * s * (3 - 2 * s)


def glow(img, passes):
    for sig, w in passes:
        img = img + w * np.stack([ndimage.gaussian_filter(img[..., c], sig, mode="nearest") for c in range(3)], -1)
    return img


def render(W, Hpx, cfg, data):
    """(Hpx, W, 3) float image, no text."""
    X, O = data["x"], data["obs"]
    t = cfg["tick"]
    x = np.clip(X[t].astype(np.float64), 0, None)
    cell = cfg["cell"]
    tiles = np.array(cfg["tiles"])                     # per tile: torus (row, col) at its top-left cell
    nt, tw = len(tiles), cfg["tile_w"]
    rng = np.random.default_rng(cfg["seed"])

    # ---- screen cells -> torus coordinates ----
    ncr, ncc = int(np.ceil(Hpx / cell)) + 1, int(np.ceil(W / cell)) + 1
    cc = np.arange(ncc)
    tile_c = np.minimum(cc // tw, nt - 1)
    tcol_c = (cc - tile_c * tw + tiles[tile_c, 1]) % N                     # (ncc,)
    trow_c = (np.arange(ncr)[:, None] + tiles[tile_c, 0][None, :]) % N     # (ncr, ncc)
    ys, xs = np.arange(Hpx) + 0.5, np.arange(W) + 0.5
    pr, pc = np.floor(ys / cell).astype(int), np.floor(xs / cell).astype(int)
    TR = trow_c[pr[:, None], pc[None, :]]                                  # (Hpx, W) torus row
    TC = np.broadcast_to(tcol_c[pc][None, :], (Hpx, W))                    # torus col
    TT = np.broadcast_to(tile_c[pc][None, :], (Hpx, W))                    # tile
    d = Hpx - ys                                                           # px above the bottom edge
    lam = lambda dd: np.interp(dd, cfg["lam_d"], cfg["lam_v"])  # noqa: E731   level parameter vs height
    # one slow horizontal swell shared by every frontier, so blocks and threads rise and fall together
    wave = ndimage.gaussian_filter1d(rng.normal(size=W), cfg["wave_sigma"], mode="wrap")
    wave = cfg["wave_amp"] * wave / wave.std()

    # ---- the field itself, bicubic between cells ----
    scr = x[:, trow_c, tcol_c[None, :]]                                    # (2, ncr, ncc)
    up = np.stack([ndimage.zoom(scr[c], cell, order=3, mode="nearest", grid_mode=True)
                   for c in range(2)], -1)[:Hpx, :W]
    img = to_rgb(np.clip(up, 0, None))

    # ---- levels 0..4: blocks of 1, 2, 4, 8, 16 cells ----
    new_r = np.r_[True, pr[1:] != pr[:-1]]                                 # first pixel row of a cell
    new_c = np.r_[True, pc[1:] != pc[:-1]]
    for k in range(5):
        b = 2 ** k
        brgb = to_rgb(block_means(x, b) * (1.0 + (cfg["gain_top"] - 1.0) * k / 4))   # gain 1.0 -> 1.6
        brgb = (1 - cfg["desat"] * k) * brgb + cfg["desat"] * k * brgb.mean(-1, keepdims=True)
        brgb = brgb * (1 - cfg["dim"] * k)                                 # detail drains away
        BR, BC = TR // b, TC // b
        cen_d = Hpx - (pr[:, None] - TR % b + b / 2.0) * cell              # height of the block centre
        cen_x = np.clip(((pc - TC % b + b / 2.0) * cell).astype(int), 0, W - 1)
        jit = rng.uniform(-1, 1, size=(nt, N // b, N // b)) * cfg["jitter"]
        active = lam(cen_d) + wave[cen_x] + jit[TT, BR, BC] > k
        pix = brgb[BR, BC]
        if k >= 1:   # dark seams on block edges (coarse_rgb), plus a faint lattice that shows on black
            edge = (new_r[:, None] & (TR % b == 0)) | (new_c[None, :] & (TC % b == 0))
            pix = np.where(edge[..., None], pix * cfg["seam"] + cfg["grid_add"] * (k - 1) / 3, pix)
        img = np.where(active[..., None], pix, img)
    img = glow(img, cfg["bloom"])                       # the matter glows; the threads stay crisp

    # ---- level 5: o(t), 192 threads in the agent's hidden order ----
    nb = O.shape[1]
    bw = W / nb
    col = np.minimum((xs / bw).astype(int), nb - 1)
    Z = O[: t + 1]
    sd = Z.std(0)
    Zs = (Z - Z.mean(0)) / np.where(sd > 0, sd, 1.0)
    jb = rng.uniform(-1, 1, size=nb) * cfg["bar_jitter"]
    bar_cx = np.clip(((col + 0.5) * bw).astype(int), 0, W - 1)
    on = lam(d)[:, None] + (wave[bar_cx] + jb[col])[None, :] > 5.0        # monotone in y per column
    age_px = np.clip(on.sum(0)[None, :] - ys[:, None], 0, None)           # px above the column's frontier
    past = np.clip(t - (age_px / cfg["tick_px"]).astype(int), 0, t)       # older ticks higher up
    sig = lambda v: 1.0 / (1.0 + np.exp(-cfg["bar_k"] * (v - cfg["bar_mid"])))  # noqa: E731
    tone = (1 - cfg["hist_mix"]) * sig(Zs[t][col])[None, :] + cfg["hist_mix"] * sig(Zs[past, col[None, :]])
    src = data["out_map"][col]                                            # designer coordinate in this column
    kind = np.where(src < 64, 0, np.where(src < 128, 1, 2))               # means c0 / means c1 / moments
    tint = np.array([PAL[0], PAL[1], [0.9, 0.9, 0.9]])[kind]
    tint = (1 - cfg["bar_tint"]) * np.array(cfg["bar_base"]) + cfg["bar_tint"] * tint
    fpx = cfg["bar_fade_px"] * (1 + cfg["fade_tilt"] * smoothstep(cfg["tilt_x0"] * W, W, xs))  # climb higher
    fade = np.exp(-np.clip(age_px - cfg["bar_hold_px"], 0, None) / fpx[None, :])               # away from title
    gut = np.where((xs % bw) < cfg["gutter"], cfg["gutter_dim"], 1.0)
    bar = (tone * fade)[..., None] * tint[None, :, :] * cfg["bar_gain"] * gut[None, :, None]
    alpha = (on * smoothstep(0.0, cfg["bar_rise_px"], age_px))[..., None]  # fray out of the blocks
    img = glow((1 - alpha) * img + alpha * bar, cfg["bloom_late"])

    # dark above, over the title side (the far side keeps its climbing threads), then a little grain
    side = 1 - (1 - cfg["vig_side"]) * smoothstep(cfg["tilt_x0"] * W, W, xs)
    img = img * (1 - smoothstep(cfg["vig0"], cfg["vig1"], d)[:, None] * side[None, :])[..., None]
    img = img + cfg["grain"] * rng.normal(size=img.shape[:2])[..., None]
    return np.clip(img, 0, 1)


def load():
    h = np.load(f"{RES}/hero_coarse_s0.npz")
    return {"x": h["x"], "obs": h["obs64"], "out_map": h["out_map"]}


def font(name):
    for dd in FONT_DIRS:
        if os.path.exists(os.path.join(dd, name)):
            return FontProperties(fname=os.path.join(dd, name))
    raise FileNotFoundError(name)


def compose(W, Hpx, cfg, data, out):
    img = render(W, Hpx, cfg, data)
    fig = plt.figure(figsize=(W / 100, Hpx / 100), dpi=100)
    fig.patch.set_facecolor("black")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.imshow(img, interpolation="none", extent=(0, W, Hpx, 0))
    ax.set_xlim(0, W)
    ax.set_ylim(Hpx, 0)
    ax.axis("off")
    for key, text in (("title", "PhySim v2"), ("sub", "supervenience")):
        T = cfg[key]
        ax.text(T["x"], T["y"], text, fontproperties=font(T["font"]), fontsize=T["size"], color=T["color"],
                ha="left", va="baseline")
    fig.savefig(out, dpi=100, facecolor="black")
    plt.close(fig)


COMMON = dict(
    seed=11, tile_w=N, wave_sigma=140.0, wave_amp=0.55, jitter=0.5,
    gain_top=1.6, desat=0.07, dim=0.06, seam=0.55, grid_add=0.04,
    bloom=[(4.0, 0.16), (26.0, 0.08)], bloom_late=[(8.0, 0.10)], grain=0.012,
    bar_jitter=0.4, tick_px=5.0, bar_k=2.2, bar_mid=0.5, hist_mix=0.25,
    bar_tint=0.25, bar_base=[0.80, 0.88, 0.92], bar_gain=1.25,
    bar_rise_px=40.0, bar_hold_px=60.0, bar_fade_px=80.0, gutter=2.5, gutter_dim=0.12,
)
LAND = dict(COMMON,
    tick=278, cell=7.5, tiles=[(58, 23), (98, 23)],
    lam_d=[0, 100, 160, 220, 300, 390, 480, 560, 1080],
    lam_v=[-1.8, -0.7, 0.5, 1.5, 2.5, 3.5, 4.5, 5.3, 9.0],
    vig0=600, vig1=1000, fade_tilt=1.25, tilt_x0=0.42, vig_side=0.6,
    title=dict(x=112, y=228, font="InstrumentSerif-Regular.ttf", size=140, color="#f2f2ee"),
    sub=dict(x=120, y=322, font="InstrumentSerif-Italic.ttf", size=66, color="#a9c2cc"),
)
PORT = dict(COMMON,
    tick=270, cell=1080 / 128, tile_w=64, tiles=[(44, 112), (78, 48)],
    lam_d=[0, 120, 190, 260, 355, 460, 570, 660, 1350],
    lam_v=[-1.8, -0.7, 0.5, 1.5, 2.5, 3.5, 4.5, 5.3, 10.0],
    wave_amp=0.4, vig0=720, vig1=940, fade_tilt=0.9, tilt_x0=0.6, vig_side=0.4,
    title=dict(x=80, y=250, font="InstrumentSerif-Regular.ttf", size=140, color="#f2f2ee"),
    sub=dict(x=88, y=344, font="InstrumentSerif-Italic.ttf", size=66, color="#a9c2cc"),
)

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "both"
    tag = sys.argv[2] if len(sys.argv) > 2 else ""
    data = load()
    if which in ("landscape", "both"):
        compose(1920, 1080, LAND, data, os.path.join(HERE, f"cover{tag}.png"))
    if which in ("portrait", "both"):
        compose(1080, 1350, PORT, data, os.path.join(HERE, f"cover_portrait{tag}.png"))
