"""PhySim v2 teaser cover, final: "the aperture", refined.

Built from one VW-1 episode (media/results/hero_objects_s0.npz, seed 0, tick 120 by default).
Reading upward:

  ground   level 0: the Flow-Lenia matter at that tick (2 channels x 128 x 128), coloured with
           level0/render.py to_rgb and laid out as a ground plane in perspective, nearest-neighbour so
           the 128-grid cells stay visible. The torus is tiled, which is what a torus looks like when
           you stand on it.
  threads  one fibre rises from every occupied cell and channel (cyan or orange, weighted by that
           channel's matter) to the 16x16-cell block it averages into (the 8x8 block geometry of
           Phi_coarse), then on to the tracked body that block is drawn with, then through one aperture.
           Above its block a fibre carries the block's mean colour; it turns warm white only on the
           last stretch before the aperture, so the point of light is made of cyan and orange matter.
  floor 1  the blocks: one tile per 16x16 block near the funnel (the 26 heaviest), tinted with the
           block's mean colour (hue = the orange channel's share of the block mean), in a faint glass
           stratum.
  floor 2  the bodies: the 12 slots of Phi_objects decoded with integrate/render_l1.decode_slots, each a
           soft disc (warm core, cyan ring, radius 0.40 sqrt(mass) cells, render_l1.draw_objects uses
           0.55), in a second, higher stratum.
  above    the aperture, and above it the agent's whole view: a one-cell-wide strip of the first 16
           coordinates of o(t) exactly as the agent receives it (obs[t], hidden permuted order,
           quantised to 0.001), each cell's colour = that coordinate's value standardised over the
           episode (display only, as in media/scripts/render_hero.py: orange above its mean, cyan
           below). No digits are drawn. At the top, a small mark is the agent; one thin line falls from
           it back to the field and lands blind.
  grace    one glider at the foot of the funnel is caught halfway: across its body its cells coarsen
           from 1x1 to 2x2 to 4x4 block means (the 4x4 part tinted like the tiles above), and the fibres
           of its coarse end are drawn brighter, so one creature is seen turning into blocks.

Liberties, stated (nothing here claims that every mark is recorded data):
  * The act line and its landing point are illustrative. The hero episodes record no actions, so
    where the agent touches the field (just short of a mid-ground glider, nudged sideways until the
    line clears the body discs) is a composition choice.
  * Level heights, the inward pull of the funnel and the two glass strata are artistic. In VW-1 the
    upper levels have no position in space; Phi_coarse and Phi_objects are two alternative upper
    levels, each computed from level 0 directly, and the picture shows them as one chain
    (cell -> block -> body).
  * Each block is assigned to its nearest tracked body (on the torus) for display only; nothing in
    Phi_objects routes through blocks. Tiles and discs are nudged apart on their floors so they do
    not pile up, and the fibres follow the nudged positions. Only the bodies with the largest
    bundles get a disc (8 at most).
  * Tile tint is saturated for display: the channel share goes through a steep sigmoid centred on
    the median share of the occupied blocks, so mixed blocks read as cyan or orange at thumbnail size.
  * The caught-halfway glider's 2x2 and 4x4 cells are a visual intermediate, not VW-1 levels, and its
    fibres are boosted (3x in number, up to 7x in brightness below the block floor).
  * Fibre density is importance-subsampled (unbiased reweighting). Fibres from the nearest ground and
    from far outside the funnel's basin are faded out, and below the block floor fibres are drawn as
    hairlines with no wide glow, so the ground stays a crisp field rather than fog.

Type: Instrument Serif Regular and Italic (SIL OFL 1.1), copied into ./fonts with the licence
(fonts/InstrumentSerif-OFL.txt). Fallback for the italic: Computer Modern text italic (cmti10, bundled
with matplotlib).

usage: OMP_NUM_THREADS=1 nice -n 10 python -B make_cover.py [land|portrait|both|ground-land|ground-portrait]
                                                             [TICK=120] [--draft] [--suffix=S]
writes cover.png (1920x1080) and/or cover_portrait.png (1080x1350) next to this script.
"""
import os
import sys
import time

sys.path.insert(0, "/home/user/evalwork/vecworld/level0")
sys.path.insert(0, "/home/user/evalwork/vecworld/integrate")
import numpy as np  # noqa: E402
from scipy.ndimage import gaussian_filter  # noqa: E402
from scipy.interpolate import BSpline  # noqa: E402
import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.font_manager import FontProperties  # noqa: E402

from render import to_rgb  # noqa: E402   (level-0 colouring, read only)
import render_l1 as R  # noqa: E402       (slot decoding, read only)

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = "/home/user/evalwork/vecworld/vw1/fresh/media/results/hero_objects_s0.npz"
F_SERIF = os.path.join(HERE, "fonts", "InstrumentSerif-Regular.ttf")
F_ITAL = os.path.join(HERE, "fonts", "InstrumentSerif-Italic.ttf")
F_ITAL_FB = os.path.join(matplotlib.get_data_path(), "fonts", "ttf", "cmti10.ttf")
CYAN = np.array([0.15, 0.85, 1.0])      # level0/render.PAL[2]
ORANGE = np.array([1.0, 0.45, 0.1])
WARM = np.array([1.0, 0.93, 0.84])
GLASS = np.array([0.62, 0.80, 0.90])
N, G = 128, 8
BS = N // G


def smoothstep(a, b, v):
    s = np.clip((np.asarray(v, float) - a) / (b - a), 0, 1)
    return s * s * (3 - 2 * s)


# ----------------------------------------------------------------------------------------------- data
def load(tick):
    h = np.load(SRC)
    x = h["x"][tick].astype(float)                         # (2, 128, 128) level-0 matter
    objs = R.decode_slots(h["L1"][tick], 12)               # level-1 tracked bodies (designer side)
    obs = h["obs"][tick].astype(float)                     # what the agent receives, permuted order
    O = h["obs64"]
    sd = O.std(0)
    z = (obs - O.mean(0)) / np.where(sd > 0, sd, 1.0)      # display-only standardisation (as render_hero)
    return x, objs, obs, z


def hierarchy(x, objs):
    """cell -> block -> body: block mass and centroid (cell units), nearest body of each block (torus)."""
    m = x.sum(0)
    mr = m.reshape(G, BS, G, BS)
    mb = mr.sum((1, 3))
    ii, jj = np.mgrid[0:N, 0:N] + 0.5
    cb_i = (ii.reshape(G, BS, G, BS) * mr).sum((1, 3)) / np.maximum(mb, 1e-9)
    cb_j = (jj.reshape(G, BS, G, BS) * mr).sum((1, 3)) / np.maximum(mb, 1e-9)
    gi, gj = np.mgrid[0:G, 0:G]
    cb_i = np.where(mb > 1e-6, cb_i, (gi + 0.5) * BS)
    cb_j = np.where(mb > 1e-6, cb_j, (gj + 0.5) * BS)
    oc = np.array([[o["cy"], o["cx"]] for o in objs])
    d_i = (oc[None, None, :, 0] - cb_i[..., None] + N / 2) % N - N / 2
    d_j = (oc[None, None, :, 1] - cb_j[..., None] + N / 2) % N - N / 2
    owner = np.argmin(d_i ** 2 + d_j ** 2, -1)
    # block hue: the two channels' share of the block mean, pushed apart a little so tints survive small
    bm = x.reshape(2, G, BS, G, BS).mean((2, 4))           # (2, G, G) = Phi_coarse block means
    share = bm[1] / np.maximum(bm.sum(0), 1e-9)
    med = np.median(share[mb > 4.0])
    s2 = 1 / (1 + np.exp(-(share - med) * 22))            # display saturation of the block tint
    hue = (1 - s2)[..., None] * CYAN + s2[..., None] * ORANGE
    hue = hue + (4 * s2 * (1 - s2))[..., None] * 0.35 * (1 - hue)
    hue = hue / hue.max(-1, keepdims=True)
    return m, mb, cb_i, cb_j, owner, d_i, d_j, hue, bm


# --------------------------------------------------------------------------------------------- camera
class Cam:
    """Level pinhole camera (shifted principal point) looking along +Y, Z up: verticals stay vertical."""

    def __init__(s, W, H, f, u0, v0, hc):
        s.W, s.H, s.f, s.u0, s.v0, s.hc = W, H, f, u0, v0, hc

    def proj(s, P):
        P = np.asarray(P, float)
        Y = np.maximum(P[..., 1], 1e-3)
        return np.stack([s.u0 + s.f * P[..., 0] / Y, s.v0 - s.f * (P[..., 2] - s.hc) / Y], -1)

    def unproj(s, u, v, depth):
        return np.array([(u - s.u0) * depth / s.f, depth, s.hc + (s.v0 - v) * depth / s.f])

    def on_plane(s, u, v, z):
        """screen point -> world (X, Y) on the horizontal plane at height z"""
        Y = s.f * (z - s.hc) / (s.v0 - v)
        return np.array([(u - s.u0) * Y / s.f, Y])


# ------------------------------------------------------------------------------------------- splatting
class Acc:
    """Additive bilinear splat of (uv, rgb weight) samples, accumulated chunk by chunk."""

    def __init__(s, H, W):
        s.H, s.W = H, W
        s.buf = np.zeros((3, H * W))

    def add(s, uv, w):
        uv, w = np.asarray(uv, float).reshape(-1, 2), np.asarray(w, float).reshape(-1, 3)
        u, v = uv[:, 0] - 0.5, uv[:, 1] - 0.5
        j0, i0 = np.floor(u).astype(np.int64), np.floor(v).astype(np.int64)
        fu, fv = u - j0, v - i0
        for di, dj, ww in ((0, 0, (1 - fu) * (1 - fv)), (0, 1, fu * (1 - fv)), (1, 0, (1 - fu) * fv), (1, 1, fu * fv)):
            ii, jj = i0 + di, j0 + dj
            ok = (ii >= 0) & (ii < s.H) & (jj >= 0) & (jj < s.W)
            idx = ii[ok] * s.W + jj[ok]
            for c in range(3):
                s.buf[c] += np.bincount(idx, weights=w[ok, c] * ww[ok], minlength=s.H * s.W)

    def curve(s, uv, rgb, ramp=None):
        """uv (R,S,2) or (S,2) in buffer px; rgb (3,), (R,3) or (R,S,3) intensity per unit screen length."""
        uv = np.asarray(uv, float)
        if uv.ndim == 2:
            uv = uv[None]
        Rn, S = uv.shape[:2]
        rgb = np.asarray(rgb, float)
        rgb = rgb[:, None, :] if rgb.ndim == 2 else rgb
        rgb = np.broadcast_to(rgb, (Rn, S, 3))
        seg = np.linalg.norm(np.diff(uv, axis=1), axis=-1)
        step = np.concatenate([seg[:, :1], 0.5 * (seg[:, 1:] + seg[:, :-1]), seg[:, -1:]], 1)
        if ramp is not None:
            step = step * ramp
        s.add(uv, step[..., None] * rgb)

    def point(s, uv, rgb):
        uv = np.asarray(uv, float).reshape(-1, 2)
        s.add(uv, np.broadcast_to(np.asarray(rgb, float), (len(uv), 3)))

    def render(s):
        return s.buf.T.reshape(s.H, s.W, 3)


class Glyphs:
    """Final-resolution layer of soft glyphs, composited far-to-near with 'over' (premultiplied)."""

    def __init__(s, H, W):
        s.H, s.W, s.items = H, W, []

    def add(s, depth, box, fn):
        s.items.append((depth, box, fn))

    def render(s):
        rgb = np.zeros((s.H, s.W, 3))
        for depth, (x0, y0, x1, y1), fn in sorted(s.items, key=lambda q: -q[0]):
            x0, y0 = max(int(x0), 0), max(int(y0), 0)
            x1, y1 = min(int(np.ceil(x1)), s.W), min(int(np.ceil(y1)), s.H)
            if x1 <= x0 or y1 <= y0:
                continue
            yy, xx = np.mgrid[y0:y1, x0:x1] + 0.5
            c, a = fn(xx, yy)                              # premultiplied colour, coverage
            rgb[y0:y1, x0:x1] = rgb[y0:y1, x0:x1] * (1 - a[..., None]) + c
        return rgb


def tile_fn(u, v, hs, col, a_fill, a_edge):
    def fn(xx, yy):
        dx, dy = np.abs(xx - u), np.abs(yy - v)
        inside = np.clip(hs - dx + 0.5, 0, 1) * np.clip(hs - dy + 0.5, 0, 1)
        inner = np.clip(hs - 1.2 - dx + 0.5, 0, 1) * np.clip(hs - 1.2 - dy + 0.5, 0, 1)
        edge = inside - inner
        a = np.clip(inside * a_fill + edge * a_edge, 0, 1)
        c = (inside * a_fill)[..., None] * col + (edge * a_edge)[..., None] * (0.5 * col + 0.5 * WARM)
        return c, a
    return fn


def disc_fn(u, v, r, gain, ring_w):
    def fn(xx, yy):
        d = np.hypot(xx - u, yy - v)
        core = np.exp(-0.5 * (d / (0.42 * r)) ** 2)
        halo = np.exp(-0.5 * (d / (0.95 * r)) ** 2)
        ring = np.exp(-0.5 * ((d - r) / ring_w) ** 2)
        c = gain * (0.80 * core[..., None] * WARM + 0.14 * halo[..., None] * CYAN + 0.80 * ring[..., None] * CYAN)
        a = np.clip(gain * (0.55 * core + 0.6 * ring + 0.15 * halo), 0, 1)
        return c, a
    return fn


# ------------------------------------------------------------------------------------------------ scene
def setup(L, tick):
    x, objs, obs, z = load(tick)
    H_ = hierarchy(x, objs)
    W, H, SS = L["W"], L["H"], 2
    cam = Cam(W * SS, H * SS, L["f"] * SS, L["u0"] * SS, L["v0"] * SS, 1.0)
    return x, objs, obs, z, H_, cam, SS


def coarse_tex(x, b, gain=1.0):
    """to_rgb of the b x b block means, upsampled back to 128 x 128 (nearest)"""
    mb_ = x.reshape(2, N // b, b, N // b, b).mean((2, 4)) * gain
    return to_rgb(np.repeat(np.repeat(mb_, b, 1), b, 2))


def ground(L, cam, tex, SS, x=None):
    """level 0 as a ground plane: nearest-neighbour texture on the tiled torus, fog with depth, and a
    soft fade on the nearest ground so nothing is cut by the bottom edge. With L["ghost"], one glider
    (one copy of it) is drawn caught halfway: its cells coarsen from 1x1 through 2x2 and 4x4 to 8x8
    block means across its body, toward the funnel's axis."""
    cs, X0, Y0, fogL = L["cs"], L["X0"], L["Y0"], L["fogL"]
    y_near = cam.f * cam.hc / (cam.H - cam.v0)
    img = np.zeros((cam.H, cam.W, 3))
    vv, uu = np.mgrid[0:cam.H, 0:cam.W] + 0.5
    g = vv > cam.v0 + 1
    Yg = cam.f * cam.hc / (vv[g] - cam.v0)
    Xg = (uu[g] - cam.u0) * Yg / cam.f
    jj = np.floor((Xg - X0) / cs).astype(np.int64) % N
    ii = np.floor((Yg - Y0) / cs).astype(np.int64) % N
    gain = L["ground_gain"] * np.exp(-(Yg - y_near) / fogL) * smoothstep(L["near_fade"][0], L["near_fade"][1], Yg)
    col = tex[ii, jj]
    if L.get("ghost") and x is not None:
        gi0, gi1, gj0, gj1, tx, ty = L["ghost"]
        fi = (Yg - Y0) / cs - N * ty
        fj = (Xg - X0) / cs - N * tx
        inreg = (fi >= gi0) & (fi < gi1) & (fj >= gj0) & (fj < gj1)
        t = (fj - gj0) / (gj1 - gj0)
        t = t if L["ghost_dir"] > 0 else 1 - t
        for b, t_on in L["ghost_levels"]:
            ct = coarse_tex(x, b, L["ghost_gain"])
            if b >= 4:                                     # the same display tint as the block tiles above
                bm_ = x.reshape(2, N // b, b, N // b, b).mean((2, 4))
                sh = bm_[1] / np.maximum(bm_.sum(0), 1e-9)
                s2_ = 1 / (1 + np.exp(-(sh - 0.5) * 22))
                hb = (1 - s2_)[..., None] * CYAN + s2_[..., None] * ORANGE
                hb = hb + (4 * s2_ * (1 - s2_))[..., None] * 0.35 * (1 - hb)
                hb = hb / hb.max(-1, keepdims=True)
                ct = np.repeat(np.repeat(hb, b, 0), b, 1) * ct.max(-1, keepdims=True) * L["ghost_tint"]
            sel = inreg & (t >= t_on)
            fb_i, fb_j = (fi[sel] % b) / b, (fj[sel] % b) / b
            seam = smoothstep(0.0, 0.06 if b >= 4 else 0.0001, np.minimum(np.minimum(fb_i, 1 - fb_i), np.minimum(fb_j, 1 - fb_j)))
            mval = x.reshape(2, N // b, b, N // b, b).mean((2, 4)).sum(0)
            keepb = mval[ii[sel] // b, jj[sel] // b] > L["ghost_thr"] * (b / 4)
            col[sel] = ct[ii[sel], jj[sel]] * (seam[:, None] if b >= 4 else 1.0) * keepb[:, None]
    img[g] = col * gain[:, None]
    return img.reshape(cam.H // SS, SS, cam.W // SS, SS, 3).mean((1, 3)), y_near


def render(L, tick, out, draft=False):
    t0 = time.time()
    rng = np.random.default_rng(7)
    x, objs, obs, z, Hh, cam, SS = setup(L, tick)
    m, mb, cb_i, cb_j, owner, d_i, d_j, hue, bm = Hh
    W, H = L["W"], L["H"]
    tex = to_rgb(x)
    cs, X0, Y0 = L["cs"], L["X0"], L["Y0"]
    A = cam.unproj(L["A_uv"][0] * SS, L["A_uv"][1] * SS, L["A_depth"])
    fogL = L["fogL"]
    img, y_near = ground(L, cam, tex, SS, x)
    h1, h2 = L["h1"] * A[2], L["h2"] * A[2]
    Gx, Gy = A[0], A[1]                                    # the ground point under the aperture
    Bx, By = Gx + L["basin_c"][0], Gy + L["basin_c"][1]    # centre of the basin that feeds the funnel
    cxs = np.array([o["cx"] for o in objs])
    cys = np.array([o["cy"] for o in objs])

    def basin(X, Y):
        """how strongly a ground point feeds the funnel (soft disc around the axis)"""
        d2 = ((np.asarray(X) - Bx) ** 2 + ((np.asarray(Y) - By) * L["basin_y"]) ** 2) / L["Rs"] ** 2
        near = np.clip((np.asarray(Y) - L["near_cut"][0]) / (L["near_cut"][1] - L["near_cut"][0]), 0, 1)
        return (L["floor"] + (1 - L["floor"]) * np.exp(-d2 ** L["basin_p"])) * near ** 2

    def fogw(Y):
        return np.exp(-(np.asarray(Y) - y_near) / (fogL * L["ray_fog_mult"]))

    # ---- B-spline spine: ground cell, a short lift, block knot (x2), body knot (x2), aperture (x2)
    deg, nC = 3, 8
    knots = np.concatenate([np.zeros(deg), np.linspace(0, 1, nC - deg + 1), np.ones(deg)])

    def basis(t):
        return np.stack([BSpline(knots, np.eye(nC)[c], deg)(t) for c in range(nC)], -1)

    tB, tO = knots[deg + 2], knots[deg + 4]                # 0.4 (block), 0.8 (body)
    wB, wO = basis(np.array([tB]))[0], basis(np.array([tO]))[0]
    zT = (wB[2] + wB[3]) * h1 + wB[4] * h2                 # rendered height of the tile floor
    zD = (wO[4] + wO[5]) * h2 + wO[6] * A[2]               # rendered height of the body floor

    # ---- fibres: every occupied cell and channel, on every visible copy of the torus
    tiles = [(tx, ty) for tx in range(L["tiles_x"][0], L["tiles_x"][1] + 1)
             for ty in range(L["tiles_y"][0], L["tiles_y"][1] + 1)]
    occ_c, occ_i, occ_j = np.nonzero(x > L["thr"])
    jit = rng.uniform(-0.35, 0.35, (2, len(occ_i)))        # sub-cell offsets so the two channels' threads part
    P, Bk, Ob, wsc, w0, ccol, bcol, key, bkey, gst = [], [], [], [], [], [], [], [], [], []
    for tx, ty in tiles:
        Xc = X0 + (occ_j + 0.5 + jit[0] + N * tx) * cs
        Yc = Y0 + (occ_i + 0.5 + jit[1] + N * ty) * cs
        uv = cam.proj(np.stack([Xc, Yc, np.zeros_like(Xc)], -1))
        keep = (Yc > L["src_y"][0]) & (Yc < L["src_y"][1]) & (uv[:, 0] > -0.1 * cam.W) & (uv[:, 0] < 1.1 * cam.W)
        if not keep.any():
            continue
        cc, ci, cj = occ_c[keep], occ_i[keep], occ_j[keep]
        bi, bj = ci // BS, cj // BS
        BX = X0 + (cb_j[bi, bj] + N * tx) * cs
        BY = Y0 + (cb_i[bi, bj] + N * ty) * cs
        k = owner[bi, bj]
        OX, OY = BX + d_j[bi, bj, k] * cs, BY + d_i[bi, bj, k] * cs
        tbx = np.round(((OX - X0) / cs - cxs[k]) / N).astype(int)
        tby = np.round(((OY - Y0) / cs - cys[k]) / N).astype(int)
        P.append(np.stack([Xc[keep], Yc[keep], 0 * Xc[keep]], -1))
        Bk.append(np.stack([BX, BY], -1))
        Ob.append(np.stack([OX, OY], -1))
        wv = x[cc, ci, cj] * fogw(Yc[keep]) * basin(Xc[keep], Yc[keep])
        w0.append(wv)
        isg = np.zeros(len(wv))
        if L.get("ghost") and (tx, ty) == tuple(L["ghost"][4:]):    # the creature caught halfway lifts off,
            gi0, gi1, gj0, gj1 = L["ghost"][:4]                     # most strongly from its coarsest end
            inr = (ci >= gi0) & (ci < gi1) & (cj >= gj0) & (cj < gj1)
            tc = (cj - gj0) / (gj1 - gj0)
            tc = tc if L["ghost_dir"] > 0 else 1 - tc
            isg = np.where(inr, smoothstep(0.2, 0.7, tc), 0.0)
            wv = wv * np.where(inr, L["ghost_boost"], 1.0)
        wsc.append(wv)
        gst.append(isg)
        ccol.append(np.where(cc[:, None] == 0, CYAN, ORANGE))
        bcol.append(hue[bi, bj])
        key.append(np.stack([k, tbx, tby], -1))
        bkey.append(((bi * G + bj) * 64 + (tx + 32)) * 64 + (ty + 32))
    P, Bk, Ob, wsc, w0, ccol, bcol, key, bkey, gst = map(np.concatenate, (P, Bk, Ob, wsc, w0, ccol, bcol, key, bkey, gst))
    nR = len(P)

    # ---- bodies: one disc per body image that receives a visible bundle; nudged apart on their floor
    ukeys, inv = np.unique(key, axis=0, return_inverse=True)
    inv = inv.ravel()
    tot = np.bincount(inv, weights=w0, minlength=len(ukeys))      # (without the grace-note boost)
    bodies = []
    for q, (k, tbx, tby) in enumerate(ukeys):
        OX, OY = X0 + (cxs[k] + N * tbx) * cs, Y0 + (cys[k] + N * tby) * cs
        Dxy = np.array([OX, OY]) + (A[:2] - np.array([OX, OY])) * L["s2"]
        Dxy = (wO[4] + wO[5]) * Dxy + wO[6] * A[:2]        # where the default spline puts the body
        D = np.array([Dxy[0], Dxy[1], zD])
        uv = cam.proj(D) / SS
        r = L["ring_scale"] * cs * np.sqrt(max(objs[k]["mass"], 0)) * (1 - L["s2"]) * L["f"] / D[1]
        vis = tot[q] >= L["body_min"] * tot.max() and -r < uv[0] < W + r
        bodies.append(dict(q=q, k=k, uv=uv, r=r, D=D, vis=vis, w=tot[q], OY=OY, OX=OX))
    for rank, b in enumerate(sorted(bodies, key=lambda b: -b["w"])):
        b["vis"] = b["vis"] and rank < L["body_max"]
    vis = [b for b in bodies if b["vis"]]
    if vis:
        p = np.array([b["uv"] for b in vis], float)
        rr = np.array([b["r"] for b in vis])
        mass = np.array([objs[b["k"]]["mass"] for b in vis])
        for _ in range(300):
            moved = False
            for i in range(len(p)):
                for j in range(i + 1, len(p)):
                    dv = p[j] - p[i]
                    dist = np.hypot(*dv)
                    need = (rr[i] + rr[j]) * L["body_sep"] + 4
                    if dist < need:
                        dirn = dv / max(dist, 1e-6) if dist > 1e-6 else np.array([1.0, 0.0])
                        push = (need - dist) * 0.5
                        fi, fj = mass[j] / (mass[i] + mass[j]), mass[i] / (mass[i] + mass[j])
                        sc = np.array([1.0, L["body_sep_vy"]])
                        p[i] -= dirn * push * fi * sc
                        p[j] += dirn * push * fj * sc
                        moved = True
            if not moved:
                break
        for b, pp in zip(vis, p):
            XY = cam.on_plane(pp[0] * SS, pp[1] * SS, zD)
            b["D"] = np.array([XY[0], XY[1], zD])
            b["uv"] = pp
            b["r"] = L["ring_scale"] * cs * np.sqrt(max(objs[b["k"]]["mass"], 0)) * (1 - L["s2"]) * L["f"] / XY[1]
    # control point B2 for every body image: the one that puts the curve through the (nudged) disc
    B2xy = np.zeros((len(ukeys), 2))
    for b in bodies:
        B2xy[b["q"]] = (b["D"][:2] - wO[6] * A[:2]) / (wO[4] + wO[5])

    # ---- tiles: one per 16x16 block image near the funnel, nudged apart on their floor
    def body_B2(k, OX, OY):
        tbx = int(np.round(((OX - X0) / cs - cxs[k]) / N))
        tby = int(np.round(((OY - Y0) / cs - cys[k]) / N))
        q = np.nonzero((ukeys == [k, tbx, tby]).all(1))[0]
        return B2xy[q[0]] if len(q) else np.array([OX, OY]) + (A[:2] - np.array([OX, OY])) * L["s2"]

    tl = []
    for tx, ty in tiles:
        for bi in range(G):
            for bj in range(G):
                if mb[bi, bj] < L["thr_block"]:
                    continue
                BX = X0 + (cb_j[bi, bj] + N * tx) * cs
                BY = Y0 + (cb_i[bi, bj] + N * ty) * cs
                bsn = basin(BX, BY)
                if not (L["src_y"][0] < BY < L["mark_ymax"]) or bsn < L["mark_basin"]:
                    continue
                k = owner[bi, bj]
                B2 = body_B2(k, BX + d_j[bi, bj, k] * cs, BY + d_i[bi, bj, k] * cs)
                B1 = np.array([BX, BY]) + (A[:2] - np.array([BX, BY])) * L["s1"]
                T = (wB[2] + wB[3]) * B1 + wB[4] * B2           # where the default spline puts the tile
                uvq = cam.proj(np.array([T[0], T[1], zT])) / SS
                hs = L["sq"] * BS * cs * (1 - L["s1"]) * L["f"] / T[1] / 2
                if not (-hs < uvq[0] < W + hs):
                    continue
                wb = fogw(BY) * bsn * min(1.0, mb[bi, bj] / L["mb_ref"])
                tl.append(dict(key=((bi * G + bj) * 64 + (tx + 32)) * 64 + (ty + 32), bi=bi, bj=bj, uv=uvq, hs=hs,
                               B2=B2, wb=wb))
    tl = sorted(tl, key=lambda t: -t["wb"])[:L["tile_max"]]
    if tl:
        p = np.array([t["uv"] for t in tl], float)
        rr = np.array([t["hs"] for t in tl]) * 1.25
        for _ in range(300):
            moved = False
            for i in range(len(p)):
                d = p - p[i]
                dist = np.hypot(d[:, 0], d[:, 1])
                need = (rr + rr[i]) * L["tile_sep"]
                for j in np.nonzero((dist < need) & (np.arange(len(p)) > i))[0]:
                    dirn = d[j] / dist[j] if dist[j] > 1e-6 else np.array([1.0, 0.0])
                    push = (need[j] - dist[j]) * 0.5 * np.array([1.0, L["tile_sep_vy"]])
                    p[i] -= dirn * push
                    p[j] += dirn * push
                    moved = True
            if not moved:
                break
        for t, pp in zip(tl, p):
            XY = cam.on_plane(pp[0] * SS, pp[1] * SS, zT)
            t["uv"] = pp
            t["hs"] = L["sq"] * BS * cs * (1 - L["s1"]) * L["f"] / XY[1] / 2
            t["T"] = np.array([XY[0], XY[1], zT])
            t["B1"] = (XY - wB[4] * t["B2"]) / (wB[2] + wB[3])
    B1map = {t["key"]: t["B1"] for t in tl}

    # ---- importance subsample of fibres (unbiased reweighting)
    cap = L["max_rays"] // (3 if draft else 1)
    if nR > cap:
        pr = wsc / wsc.sum()
        pick = rng.choice(nR, cap, replace=False, p=pr)
        rw = 1.0 / (pr[pick] * nR)
        P, Bk, Ob, ccol, bcol, inv, bkey, gst = P[pick], Bk[pick], Ob[pick], ccol[pick], bcol[pick], inv[pick], bkey[pick], gst[pick]
        wsc = wsc[pick] * (rw / rw.mean() * nR / cap)
    nP = len(P)

    def spine(Pg, Bxy, B2, B1xy=None):
        n = len(Pg)
        B1xy = Bxy + (A[:2] - Bxy) * L["s1"] if B1xy is None else B1xy
        B1 = np.concatenate([B1xy, np.full((n, 1), h1)], 1)
        B2 = np.concatenate([B2, np.full((n, 1), h2)], 1)
        lift = Pg + np.array([0, 0, L["lift"] * h1])
        Ab = np.broadcast_to(A, Pg.shape)
        return np.stack([Pg, lift, B1, B1, B2, B2, Ab, Ab], 1)

    B1xy = Bk + (A[:2] - Bk) * L["s1"]
    for i_, kk in enumerate(bkey):
        if kk in B1map:
            B1xy[i_] = B1map[kk]
    ctrl = spine(P, Bk, B2xy[inv], B1xy)
    S = L["samples"] // (2 if draft else 1)
    ts = np.linspace(0, 1, S) ** 0.8
    Bm = basis(ts)
    # intensity along the fibre: fade in off the ground, thinner below the block floor (no mist)
    ramp = smoothstep(0, L["ramp_in"], ts) * (L["low_gain"] + (1 - L["low_gain"]) * smoothstep(tB - 0.16, tB - 0.02, ts))
    # colour along the fibre: own channel -> block mean colour -> warm white just before the aperture
    a1 = smoothstep(tB - 0.14, tB, ts)[None, :, None]
    a2 = smoothstep(1 - L["warm_tail"], 1.0, ts)[None, :, None]
    hi = smoothstep(tB - 0.12, tB - 0.02, ts)            # below the block floor: crisp, no wide glow (no mist)
    acc, acc_lo = Acc(cam.H, cam.W), Acc(cam.H, cam.W)
    for a in range(0, nP, 1500):
        sl = slice(a, a + 1500)
        cur = cam.proj(np.einsum("sk,rkd->rsd", Bm, ctrl[sl]))
        col = ((1 - a1) * ccol[sl][:, None] + a1 * bcol[sl][:, None]) * (1 - a2) + a2 * WARM
        col = col * (wsc[sl] * L["ray_gain"])[:, None, None]
        acc.curve(cur, col, (ramp * hi)[None])
        lowf = (1 + (L["ghost_low"] - 1) * gst[sl])[:, None, None]
        acc_lo.curve(cur, col * lowf, (ramp * (1 - hi))[None])
    light, light_lo = acc.render(), acc_lo.render()
    t1 = time.time()

    # ---- glyph layer (final px): block tiles on floor 1, body discs on floor 2
    gl = Glyphs(H, W)
    for t in tl:
        u, v = t["uv"]
        hs, wb = t["hs"], t["wb"]
        col = hue[t["bi"], t["bj"]] * L["tile_gain"] * (0.45 + 0.55 * wb)
        gl.add(t["T"][1], (u - hs - 2, v - hs - 2, u + hs + 3, v + hs + 3),
               tile_fn(u, v, hs, col, L["tile_fill"] * (0.5 + 0.5 * wb), L["tile_edge"] * (0.5 + 0.5 * wb)))
    nq = len(tl)
    nb = 0
    for b in bodies:
        if not b["vis"]:
            continue
        u, v = b["uv"]
        r = b["r"]
        gain = L["disc_gain"] * (0.45 + 0.55 * min(1.0, fogw(b["OY"]) * basin(b["OX"], b["OY"]) / 0.6))
        gl.add(b["D"][1], (u - 2.2 * r - 4, v - 2.2 * r - 4, u + 2.2 * r + 4, v + 2.2 * r + 4),
               disc_fn(u, v, r, gain, L["ring_w"]))
        nb += 1

    # ---- aperture: small horizontal ring + bright point, flare, beam up to the strip
    mk = Acc(cam.H, cam.W)
    th = np.linspace(0, 2 * np.pi, 240)
    ap = A + L["ap_r"] * np.stack([np.cos(th), np.sin(th), 0 * th], -1)
    mk.curve(cam.proj(ap), WARM * L["ap_gain"])
    auv = cam.proj(A)
    mk.point(auv, np.array([1, 1, 1.0]) * L["ap_point"])
    fl = np.linspace(-1, 1, 3000)
    flare = np.stack([auv[0] + fl * L["flare_w"] * SS, np.full(3000, auv[1])], -1)
    mk.curve(flare, np.array([0.75, 0.9, 1.0]) * L["flare_gain"], ramp=np.exp(-(fl / 0.35) ** 2)[None])
    bl = np.linspace(0, 1, 3000)
    beam_top = (L["agent_uv"][1] + L["agent_r"] + 3) * SS
    beam = np.stack([np.full(3000, auv[0]), auv[1] + bl * (beam_top - auv[1])], -1)
    mk.curve(beam, WARM * L["beam_gain"], ramp=(L["beam_floor"] + (1 - L["beam_floor"]) * (1 - bl) ** 2)[None])

    # ---- the agent's act: one thin line from above, down to the field, landing blind (illustrative)
    ag_uv = np.array(L["agent_uv"], float) * SS + np.array([0, L["agent_r"] * SS])
    discs = [(b["uv"], b["r"]) for b in bodies if b["vis"]]

    def clearance(land):                                   # final px between the act line and the nearest disc
        a_, b_ = ag_uv / SS, np.asarray(land, float)
        out = 1e9
        for c_, r_ in discs:
            t_ = np.clip(np.dot(c_ - a_, b_ - a_) / np.dot(b_ - a_, b_ - a_), 0, 1)
            out = min(out, np.hypot(*(a_ + t_ * (b_ - a_) - c_)) - r_)
        return out
    land = np.array(L["act_uv"], float)
    for dx in sorted(np.arange(-120, 121, 4), key=abs):    # nearest landing (same row) the line reaches cleanly
        if clearance(land + [dx, 0]) >= L["act_clear"]:
            land = land + [dx, 0]
            break
    Yt = cam.f * cam.hc / (land[1] * SS - cam.v0)
    tgt3 = np.array([(land[0] * SS - cam.u0) * Yt / cam.f, Yt, 0.0])
    tuv = cam.proj(tgt3)
    nl = 4000
    lr = np.linspace(0, 1, nl)
    mk.curve(np.linspace(ag_uv, tuv, nl), WARM * L["act_gain"], ramp=(0.55 + 0.45 * lr)[None])
    for rr_, gg_ in L["ripples"]:
        rip = tgt3 + rr_ * np.stack([np.cos(th), np.sin(th), 0 * th], -1)
        mk.curve(cam.proj(rip), WARM * L["act_gain"] * gg_)
    marks = mk.render()

    # ---- compose: tone map, glow, screen blend over the ground
    li = (light + marks).reshape(H, SS, W, SS, 3).mean((1, 3)) * SS     # line integral per final px
    li_lo = light_lo.reshape(H, SS, W, SS, 3).mean((1, 3)) * SS
    glyph = gl.render()
    glow = (gaussian_filter(li, (L["g1"], L["g1"], 0)) * L["g1w"] + gaussian_filter(li, (L["g2"], L["g2"], 0)) * L["g2w"]
            + gaussian_filter(li_lo, (L["g1"], L["g1"], 0)) * L["g1w"] * L["low_glow"]
            + gaussian_filter(glyph, (L["g2"], L["g2"], 0)) * L["glyph_glow"])
    li = li + li_lo

    def tone(b, k):                                       # hue-preserving: compress the max channel, keep chroma
        mx = b.max(-1, keepdims=True)
        o = b * (1 - np.exp(-k * mx)) / np.maximum(mx, 1e-9)
        hot = 1 - np.exp(-L["white_k"] * np.maximum(mx - L["white_thr"], 0))   # very dense bundles burn white
        return o + (1 - o) * hot
    core = tone(li, L["k_core"])
    halo = tone(glow, L["k_glow"])
    comp = 1 - (1 - img) * (1 - core) * (1 - halo)
    comp = 1 - (1 - comp) * (1 - np.clip(glyph, 0, 1))
    yy, xx = np.mgrid[0:H, 0:W] + 0.5
    au, av = auv / SS
    r2 = (xx - au) ** 2 + (yy - av) ** 2
    for sig, amp in L["halo"]:                             # light through a pinhole
        comp = comp + (amp * np.exp(-r2 / (2 * sig ** 2)))[..., None] * WARM
    # ---- the two glass strata (floors of the blocks and of the bodies)
    for zf, Rf, (a_fill, a_rim) in ((zT, L["R1"], L["glass1"]), (zD, L["R2"], L["glass2"])):
        v_ok = yy < L["v0"] - 0.5
        Yp = np.where(v_ok, L["f"] * (zf - 1.0) / np.maximum(L["v0"] - yy, 0.5), 1e9)
        Xp = (xx - L["u0"]) * Yp / L["f"]
        d = np.hypot(Xp - Gx, (Yp - Gy) * L["glass_y"]) / Rf
        front = 0.55 + 0.45 * smoothstep(Gy + 0.6 * Rf, Gy - Rf, Yp)       # the near rim catches more light
        a = (a_fill * (1 - smoothstep(0.55, 1.0, d)) * (0.6 + 0.4 * d)
             + a_rim * np.exp(-0.5 * ((d - 1) / L["rim_w"]) ** 2) * front)
        a = np.where(v_ok, a, 0)
        comp = comp * (1 - a[..., None]) + a[..., None] * GLASS
    vy = (np.arange(H) + 0.5)[:, None]
    haze = np.exp(-((vy - L["v0"]) / (L["haze_w"] * H)) ** 2) * L["haze"]
    comp = comp + haze[..., None] * np.array([0.07, 0.16, 0.22])
    # ---- the agent's view: a one-cell strip of o(t), permuted order, colour = standardised value
    strip = np.zeros((H, W, 3))
    n = L["strip_n"]
    cw, ch, gap = L["cell"]
    top = L["agent_uv"][1] + L["agent_r"] + L["strip_gap_top"]
    bot = av - L["strip_gap_bot"]
    pitch = (bot - top) / n
    for r_ in range(n):
        q = (L["strip_start"] + r_) % len(obs)
        vz = np.tanh(z[q] / 1.6)
        col = 0.10 + np.clip(vz, 0, None) * ORANGE * 1.1 + np.clip(-vz, 0, None) * CYAN * 1.1
        col = col * (0.55 + 0.45 * (1 - r_ / n) ** 0.7) * L["strip_gain"]
        yc = bot - (r_ + 0.5) * pitch
        y0_, y1_ = yc - (pitch - gap) / 2, yc + (pitch - gap) / 2
        x0_, x1_ = au - cw / 2, au + cw / 2
        iy0, iy1, ix0, ix1 = int(y0_) - 1, int(y1_) + 2, int(x0_) - 1, int(x1_) + 2
        sy, sx = np.mgrid[iy0:iy1, ix0:ix1] + 0.5
        cov = (np.clip(np.minimum(sx - x0_, x1_ - sx) + 0.5, 0, 1) * np.clip(np.minimum(sy - y0_, y1_ - sy) + 0.5, 0, 1))
        strip[iy0:iy1, ix0:ix1] = np.maximum(strip[iy0:iy1, ix0:ix1], cov[..., None] * col)
    strip_glow = gaussian_filter(strip, (3, 3, 0)) * L["strip_glow"]
    comp = 1 - (1 - comp) * (1 - np.clip(strip + strip_glow, 0, 1))
    vig = 1 - L["vig"] * (((xx - W / 2) / (W / 2)) ** 2 * 0.6 + ((yy - H / 2) / (H / 2)) ** 2 * 0.4)
    comp = np.clip(comp * vig[..., None] + rng.normal(0, 0.007, comp.shape), 0, 1)
    t2 = time.time()

    # ---- typography and the agent mark
    fig = plt.figure(figsize=(W / 100, H / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.imshow(comp, interpolation="nearest", extent=(0, W, H, 0))
    ax.set_xlim(0, W)
    ax.set_ylim(H, 0)
    ax.axis("off")
    ax.add_patch(plt.Circle(L["agent_uv"], L["agent_r"], fill=False, ec=WARM, lw=1.1, alpha=0.85))
    ax.add_patch(plt.Circle(L["agent_uv"], L["agent_r"] * 0.32, fc=WARM, ec="none", alpha=0.9))
    title(ax, L)
    fig.savefig(out, dpi=100, facecolor="black")
    plt.close(fig)
    from PIL import Image                                  # opaque RGB, not RGBA, for slides and video
    Image.open(out).convert("RGB").save(out, optimize=True)
    print(f"{out}: fibres {nP} of {nR}, tiles {nq}, bodies {nb}, aperture {auv / SS}, landing {tuv / SS}, "
          f"strip pitch {pitch:.1f}px; fibres {t1 - t0:.1f}s, compose {t2 - t1:.1f}s, total {time.time() - t0:.1f}s")


def title(ax, L):
    fi = F_ITAL if os.path.exists(F_ITAL) else F_ITAL_FB
    fpt = FontProperties(fname=F_SERIF, size=L["title_size"])
    tx, ty = L["title_xy"]
    t1 = ax.text(tx, ty, "PhySim", fontproperties=fpt, color=(0.95, 0.95, 0.93), ha="left", va="baseline")
    w = t1.get_window_extent(renderer=ax.figure.canvas.get_renderer()).width
    ax.text(tx + w + L["title_size"] * L["v2_space"], ty, "v2", fontproperties=fpt, color=tuple(CYAN * 0.9 + 0.08),
            ha="left", va="baseline")
    fps = FontProperties(fname=fi, size=L["sub_size"])
    ax.text(tx + L["sub_dx"], ty + L["sub_dy"], "supervenience", fontproperties=fps, color=L["sub_col"],
            ha="left", va="baseline")


def ground_debug(L, tick, out):
    """ground layer only, with a 100 px grid, to place the camera, the act landing and the ghost."""
    x, objs, obs, z, Hh, cam, SS = setup(L, tick)
    img, _ = ground(L, cam, to_rgb(x), SS, x)
    W, H = L["W"], L["H"]
    fig = plt.figure(figsize=(W / 100, H / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.imshow(np.clip(img * 1.6, 0, 1), extent=(0, W, H, 0))
    for gx in range(0, W, 100):
        ax.axvline(gx, color="w", lw=0.3, alpha=0.4)
        ax.text(gx + 2, 14, str(gx), color="w", fontsize=7)
    for gy in range(0, H, 100):
        ax.axhline(gy, color="w", lw=0.3, alpha=0.4)
        ax.text(2, gy - 2, str(gy), color="w", fontsize=7)
    # where each torus cell lands: label glider centres (connected components of matter) with cell coords
    from scipy.ndimage import label, center_of_mass
    lab, nlab = label(x.sum(0) > 0.05)
    for tx in range(L["tiles_x"][0], L["tiles_x"][1] + 1):
        for ty in range(L["tiles_y"][0], L["tiles_y"][1] + 1):
            for c in range(1, nlab + 1):
                ci, cj = center_of_mass(lab == c)
                Pw = np.array([L["X0"] + (cj + 0.5 + N * tx) * L["cs"], L["Y0"] + (ci + 0.5 + N * ty) * L["cs"], 0])
                if Pw[1] < 1.5 or Pw[1] > 9:
                    continue
                u, v = cam.proj(Pw) / SS
                if 0 < u < W and 0 < v < H:
                    ax.text(u, v, f"{c}:{int(ci)},{int(cj)}\n{tx},{ty} Y{Pw[1]:.1f}", color="yellow", fontsize=6,
                            ha="center")
    ax.set_xlim(0, W)
    ax.set_ylim(H, 0)
    ax.axis("off")
    fig.savefig(out, dpi=100, facecolor="black")
    plt.close(fig)
    print(out)


LAND = dict(
    W=1920, H=1080, f=950, u0=960, v0=610, cs=4.0 / 128, X0=-0.85, Y0=-1.2,
    A_uv=(1330, 275), A_depth=7.0, fogL=5.0, ground_gain=1.0, near_fade=(2.05, 2.45), basin_c=(0.0, -1.2),
    tiles_x=(-4, 4), tiles_y=(0, 6), src_y=(1.4, 22), thr=0.04, max_rays=14000, ray_fog_mult=1.3,
    Rs=3.2, basin_y=1.0, basin_p=2.0, floor=0.006, near_cut=(2.6, 4.0),
    s1=0.22, s2=0.42, h1=0.42, h2=0.60, lift=0.25, samples=1100, ramp_in=0.035, low_gain=1.8, low_glow=0.6, warm_tail=0.17,
    ray_gain=0.070, ring_scale=0.40, ring_w=1.1, disc_gain=0.9, body_min=0.10, body_max=8, body_sep=1.35, body_sep_vy=0.5,
    sq=0.54, tile_sep=0.9, tile_sep_vy=0.35, tile_max=26, thr_block=6.0, mb_ref=40.0, tile_gain=1.0, tile_fill=0.42, tile_edge=0.20,
    mark_basin=0.35, mark_ymax=16,
    R1=3.3, R2=2.6, glass1=(0.04, 0.06), glass2=(0.04, 0.06), glass_y=1.0, rim_w=0.012,
    ap_r=0.10, ap_gain=0.35, ap_point=14.0, beam_gain=0.18, beam_floor=0.25, halo=((22, 0.10), (90, 0.06), (320, 0.035)),
    flare_w=260, flare_gain=0.05,
    agent_uv=(1330, 76), agent_r=6.0, act_uv=(1610, 806), act_clear=16, act_gain=0.40,
    ripples=((0.03, 1.0), (0.065, 0.6), (0.11, 0.3)),
    g1=2.0, g1w=1.0, g2=16, g2w=1.3, glyph_glow=0.5, k_core=1.0, k_glow=0.9, white_k=0.8, white_thr=1.0,
    haze=0.20, haze_w=0.06, vig=0.35,
    strip_n=16, strip_start=0, cell=(8, 0, 3.0), strip_gap_top=10, strip_gap_bot=28, strip_gain=1.2, strip_glow=0.35,
    ghost=(28, 60, 60, 96, 0, 1), ghost_dir=1, ghost_gain=1.5, ghost_boost=3.0, ghost_low=7.0, ghost_thr=0.1, ghost_tint=0.9, ghost_levels=((2, 0.3), (4, 0.58)),
    title_size=150, title_xy=(120, 300), v2_space=0.22, sub_size=62, sub_dx=6, sub_dy=92, sub_col=(0.80, 0.86, 0.89),
)

PORT = dict(LAND)
PORT.update(
    W=1080, H=1350, f=760, u0=540, v0=860, X0=-1.9, Y0=-1.67, A_uv=(610, 640), A_depth=6.5,
    agent_uv=(610, 400), act_uv=(900, 1030), Rs=3.0, tiles_x=(-3, 3), near_fade=(1.58, 1.98),
    title_xy=(84, 230), title_size=132, sub_size=56, sub_dy=82,
    flare_w=200, halo=((22, 0.10), (80, 0.06), (260, 0.035)), ray_gain=0.095,
)

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    draft = "--draft" in sys.argv
    suffix = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--suffix=")), "")
    which = args[0] if args else "both"
    tick = int(args[1]) if len(args) > 1 else 120
    for a in sys.argv:                                     # --set=key=value (python literal), for trials
        if a.startswith("--set="):
            k_, v_ = a[6:].split("=", 1)
            tgt = PORT if which.endswith("portrait") else LAND
            tgt[k_] = eval(v_)
    if which == "ground-land":
        ground_debug(LAND, tick, os.path.join(HERE, "wip", "ground_land.png"))
    if which == "ground-portrait":
        ground_debug(PORT, tick, os.path.join(HERE, "wip", "ground_port.png"))
    if which in ("land", "both"):
        render(LAND, tick, os.path.join(HERE, f"cover{suffix}.png"), draft)
    if which in ("portrait", "both"):
        render(PORT, tick, os.path.join(HERE, f"cover_portrait{suffix}.png"), draft)
