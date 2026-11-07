"""PhySim v2 teaser cover, "the stack", refined (program/cover).

Concept kept from vw1/fresh/teaser/stack: translucent planes seen from an elevated camera, built from
one real VW-1 episode (media/results/hero_objects_s0.npz and hero_coarse_s0.npz, seed 0, tick 278),
read bottom to top:

  plane 0  level 0: the Flow-Lenia matter field (2 channels x 128 x 128) coloured with level0/render.py
           to_rgb, with faint ghosts of the previous 10 ticks as wakes, drawn as a glass slab. A faint
           8 x 8 grid marks the 16 x 16-cell blocks that Phi_coarse averages.
  funnels  each occupied block is a funnel: its mouth is the block's outline on the matter plane, a
           veil of threads rises from that outline to the block's tile, and brighter threads rise
           from matter cells sampled in proportion to matter (256 cells -> 1 number per channel).
  plane 1  the 8 x 8 block means (the first 128 numbers of Phi_coarse) as glass tiles, brightness =
           to_rgb of the block mean.
  plane 2  the tracked bodies of Phi_objects (8 of 12 slots occupied at this tick) as discs: warm core,
           cyan ring of radius 0.55 sqrt(mass) cells (as in render_l1.draw_objects), recent trail.
           Narrow cyan funnels join each body to the tiles whose block centres lie within its disc
           radius + 12 cells.
  strip    the agent's view: the last 12 observation vectors o(t-11..t), 144 numbers each, in the
           agent's hidden permuted order (out_map), each cell coloured by that coordinate standardised
           over the episode (orange above its mean, cyan below; display only).
  gather   every body sends 12 fibres (one per feature) from its ring; all 96 converge on one point
           under the strip, the observation port, and from there 144 short fibres spread to the
           columns of the newest row, each to its true permuted column.
  act      one dotted warm thread falls from the strip to the matter: the agent acting blind.

Data transforms (exact, not artistic):
  * The torus is re-centred: every array is translated by (dx, dy) = (-92, -80) cells (np.roll on the
    matter; the tracked positions rotated by the same angle in their cos/sin features; o(t) recomputed
    as L1[out_map] of the rotated L1 and quantised to 0.001 as recorded). Flow-Lenia on the torus is
    translation-equivariant, so this is the same episode with its origin moved; it was chosen by
    search so that no body disc or matter cell is cut by a plane edge (8 bodies, minimum clearance
    4.9 cells, zero matter within 3 cells of an edge). This removes the half-discs of the first cover.
  * The block means are recomputed as Phi_coarse of the translated matter (8 x 8 block means on the
    fixed grid); on the untranslated tick they match the recorded hero_coarse L1 to 5e-8.

Artistic liberties, stated:
  * Heights and plane sizes are artistic. The planes taper upward (sides 2.7, 1.9, 1.5, strip 1.2 x
    0.38) so each step reads as many-to-one; in VW-1 the levels have no position or size in space.
  * Phi_coarse and Phi_objects are two alternative upper levels, each computed from level 0 directly;
    the picture stacks them as one chain (cell -> block -> body). The tile-to-body funnels are a
    display choice (tiles near the disc), not a computation of Phi_objects.
  * The observation port is drawn as a single point where all fibres meet. In VW-1, o(t) = a fixed
    hidden permutation of the 144 numbers of L1 (quantised); there is no physical meeting point. The
    fan above the point lands each feature on its true column, so the scramble in the strip is real,
    but which ring point a fibre leaves from (feature f at angle 2 pi f / 12) is decorative. The
    first cover drew each feature straight to its column, which is faithful but read as a tangle.
  * Thread shapes (a flare that sweeps in low and arrives along the chord), the funnel veils from the
    block outlines, and the tint of each funnel mouth (half the block mean's hue, half pale) are drawn
    for legibility; only the end points carry meaning.
  * The act thread is illustrative: the hero episode records no actions. It lands on the glider of
    slot 7, and its column on the strip is chosen to clear the body discs and the port.
  * Fog, bloom, glow, grain, the slab edge and the light pool under the matter plane are atmosphere.

Type: "PhySim v2" in Instrument Serif Regular (SIL OFL 1.1, fonts copied in
vw1/fresh/teaser/final/fonts with their licence), "supervenience" in Computer Modern text italic
(cmti10, bundled with matplotlib).

usage: python -B make_cover.py [landscape|portrait|both] [--draft] [--tag NAME]
Writes cover.png (1920x1080) and cover_portrait.png (1080x1350) next to this script, plus
thumb_*.png at 400 px wide for checking.
"""
import os
import sys

import numpy as np
import scipy.ndimage as ndi
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.font_manager import FontProperties  # noqa: E402
from PIL import Image  # noqa: E402

sys.path.insert(0, "/home/user/evalwork/vecworld/level0")
from render import to_rgb  # noqa: E402  (VW-0 matter colouring, read only)

HERE = os.path.dirname(os.path.abspath(__file__))
RES = "/home/user/evalwork/vecworld/vw1/fresh/media/results"
FONTS = "/home/user/evalwork/vecworld/vw1/fresh/teaser/final/fonts"
MPL_TTF = os.path.join(matplotlib.get_data_path(), "fonts", "ttf")
FONT_TITLE = os.path.join(FONTS, "InstrumentSerif-Regular.ttf")
FONT_SUB = os.path.join(MPL_TTF, "cmti10.ttf")      # Computer Modern text italic

CYAN = np.array([0.15, 0.85, 1.0])
ORANGE = np.array([1.0, 0.45, 0.1])
PALE = np.array([0.78, 0.9, 1.0])
WARM = np.array([1.0, 0.82, 0.55])
K, NF, G = 12, 12, 8
TICK, SHIFT = 278, (92, 80)                     # (dx, dy) cells subtracted from every position
RNG = np.random.default_rng(7)


# ----------------------------------------------------------------------------------------------- data
def rotate_L1(L, dx, dy):
    """Translate the tracked bodies by (-dx, -dy) cells: rotate the (cos, sin) position features."""
    S = L.reshape(L.shape[0], K, NF).copy()
    for (ic, is_), d in (((3, 4), dx), ((5, 6), dy)):
        a = -2 * np.pi * d / 128
        c, s = S[..., ic].copy(), S[..., is_].copy()
        S[..., ic] = c * np.cos(a) - s * np.sin(a)
        S[..., is_] = c * np.sin(a) + s * np.cos(a)
    return S.reshape(L.shape)


def load(t, shift=SHIFT):
    dx, dy = shift
    o = np.load(f"{RES}/hero_objects_s0.npz")
    c = np.load(f"{RES}/hero_coarse_s0.npz")
    X = o["x"]
    assert np.array_equal(X[t], c["x"][t])
    bm0 = X[t].reshape(2, G, 16, G, 16).mean((2, 4))
    assert np.abs(bm0 - c["L1"][t, :2 * G * G].reshape(2, G, G)).max() < 1e-6   # Phi_coarse = block means
    roll = lambda a: np.roll(a, (-dy, -dx), (-2, -1))  # noqa: E731
    x = roll(X[t])
    blocks = x.reshape(2, G, 16, G, 16).mean((2, 4))
    past = [roll(X[max(t - d, 0)]) for d in range(1, 11)]
    L = rotate_L1(o["L1"], dx, dy)
    out_map = o["out_map"]
    assert np.abs(o["obs64"][t] - o["L1"][t][out_map]).max() < 1e-3
    obs = np.round(L[:, out_map], 3)
    sd = obs.std(0)
    Z = (obs - obs.mean(0)) / np.where(sd > 0, sd, 1.0)
    return dict(x=x, past=past, blocks=blocks, L=L, tab=o["tab"], t=t, out_map=out_map, Z=Z)


def decode(y):
    S = y.reshape(K, NF)
    out = []
    for s in range(K):
        if S[s, 0] < 0.5:
            continue
        cx = np.arctan2(S[s, 4], S[s, 3]) * 128 / (2 * np.pi) % 128
        cy = np.arctan2(S[s, 6], S[s, 5]) * 128 / (2 * np.pi) % 128
        out.append(dict(slot=s, mass=S[s, 1], cx=cx, cy=cy, r=0.55 * np.sqrt(max(S[s, 1], 0.0))))
    return out


def trails(D, n=22):
    L, tab, t = D["L"], D["tab"], D["t"]
    tr = {}
    for tt in range(max(0, t - n), t + 1):
        for b in decode(L[tt]):
            if tab[tt, b["slot"], 4] == tab[t, b["slot"], 4]:
                tr.setdefault(b["slot"], []).append((b["cx"], b["cy"]))
    return tr


# --------------------------------------------------------------------------------------------- camera
class Cam:
    def __init__(self, el, az, dist, target):
        el, az = np.radians(el), np.radians(az)
        d = np.array([np.cos(el) * np.cos(az), np.cos(el) * np.sin(az), np.sin(el)])
        eye = np.asarray(target, float) + dist * d
        fwd = -d
        right = np.cross(fwd, [0, 0, 1.0])
        right /= np.linalg.norm(right)
        up = np.cross(right, fwd)
        self.R = np.stack([right, -up, fwd])
        self.t = -self.R @ eye
        self.f, self.c = 1.0, np.zeros(2)
        self.zn, self.zf, self.fog_k = 0.0, 1.0, 0.0

    def proj(self, P):
        Q = np.asarray(P, float) @ self.R.T + self.t
        return np.stack([self.f * Q[..., 0] / Q[..., 2] + self.c[0],
                         self.f * Q[..., 1] / Q[..., 2] + self.c[1]], -1), Q[..., 2]

    def homography(self, O, U, V):
        Kc = np.array([[self.f, 0, self.c[0]], [0, self.f, self.c[1]], [0, 0, 1.0]])
        return Kc @ np.column_stack([self.R @ U, self.R @ V, self.R @ O + self.t])

    def fit(self, pts, box):
        """Choose focal length and principal point so the projected pts fill box=(x0,y0,x1,y1)."""
        self.f, self.c = 1.0, np.zeros(2)
        p, _ = self.proj(pts)
        lo, hi = p.min(0), p.max(0)
        x0, y0, x1, y1 = box
        self.f = min((x1 - x0) / (hi[0] - lo[0]), (y1 - y0) / (hi[1] - lo[1]))
        self.c = np.array([(x0 + x1) / 2, (y0 + y1) / 2]) - self.f * (lo + hi) / 2
        _, zd = self.proj(pts)
        self.zn, self.zf = zd.min(), zd.max()

    def fog(self, Z):
        """Atmospheric depth: the far side of the stack recedes into the dark."""
        return 1 - self.fog_k * np.clip((Z - self.zn) / (self.zf - self.zn), 0, 1)


# ------------------------------------------------------------------------------------------- textures
def tex_matter(x, past=(), up=6, grid=0.0):
    """Level 0 at tick t (to_rgb), with faint ghosts of earlier ticks so the gliders carry their wake,
    and an optional faint 16-cell block grid."""
    rgb = to_rgb(x)
    for k, xp in enumerate(past):
        rgb = np.maximum(rgb, 0.13 * np.exp(-k / 3.0) * to_rgb(xp))
    rgb = np.repeat(np.repeat(rgb, up, 0), up, 1)
    a = np.clip(rgb.max(-1) * 1.5, 0, 0.95)       # matter is fairly opaque: it occludes threads below
    if grid > 0:
        n = rgb.shape[0]
        i = np.arange(n)
        on = (i % (16 * up) < 1) | (i % (16 * up) >= 16 * up - 1)
        gm = (on[:, None] | on[None, :]).astype(float)
        rgb = rgb + grid * gm[..., None] * PALE * (1 - a[..., None])
        a = np.maximum(a, 0.5 * grid * gm)
    return rgb, a


def tex_blocks(blocks, n=512, gain=2.0, gap=0.12, level=0.8):
    """8x8 glass tiles: each tile glows with to_rgb of its block mean (hue dropped), with a brighter rim
    so empty tiles still read as a lattice."""
    f = n // G
    up = np.repeat(np.repeat(blocks, f, 1), f, 2)
    lum = to_rgb(up * gain).max(-1)[..., None]
    yy, xx = np.mgrid[0:n, 0:n] % f / f
    inside = (xx > gap / 2) & (xx < 1 - gap / 2) & (yy > gap / 2) & (yy < 1 - gap / 2)
    e = 0.03
    edge = inside & ((xx < gap / 2 + e) | (xx > 1 - gap / 2 - e) | (yy < gap / 2 + e) | (yy > 1 - gap / 2 - e))
    rc = np.hypot(xx - 0.5, yy - 0.5)
    pool = np.exp(-0.5 * (rc / 0.18) ** 2)[..., None]        # light pooling where the funnels land
    glass = PALE * (0.3 + 0.7 * pool)
    rgb = lum * glass * inside[..., None] * level
    rgb = rgb + 0.02 * inside[..., None] * PALE + (0.05 + 0.5 * lum) * edge[..., None] * PALE
    a = 0.06 * inside + 0.3 * rgb.max(-1)
    return rgb, np.clip(a, 0, 0.6)


def tex_bodies(bodies, tr, n=768):
    """Each tracked body as an abstracted glider: warm core, cyan ring (radius 0.55 sqrt(mass) cells),
    plus a fading trail of its recent centres."""
    s = n / 128.0
    rgb = np.zeros((n, n, 3))
    a = np.zeros((n, n))
    for b in bodies:
        r = b["r"]
        R = r + 3.0
        cx, cy = b["cx"], b["cy"]
        c0, c1 = int(max((cx - R) * s, 0)), int(min((cx + R) * s + 1, n))
        r0, r1 = int(max((cy - R) * s, 0)), int(min((cy + R) * s + 1, n))
        yy, xx = (np.mgrid[r0:r1, c0:c1] + 0.5) / s
        d = np.hypot(xx - cx, yy - cy)
        core = np.exp(-0.5 * (d / (0.42 * r)) ** 2)
        halo = np.exp(-0.5 * (d / (0.9 * r)) ** 2)
        ring = np.exp(-0.5 * ((d - r) / 0.32) ** 2)
        rgb[r0:r1, c0:c1] += (0.6 * core[..., None] * WARM + 0.12 * halo[..., None] * CYAN
                              + 0.85 * ring[..., None] * CYAN)
        a[r0:r1, c0:c1] += 0.5 * core + 0.3 * ring
    pts, cws = [], []
    for sl, P in tr.items():
        P = np.array(P)
        for i in range(1, len(P)):
            if np.abs(P[i] - P[i - 1]).max() > 64:
                continue
            u = np.linspace(0, 1, 40, endpoint=False)[:, None]
            q = (P[i - 1] + u * (P[i] - P[i - 1])) * s
            w = 0.12 * (i / len(P)) ** 1.5 * np.hypot(*(P[i] - P[i - 1])) * s / 40
            pts.append(q)
            cws.append(np.tile(CYAN * w, (len(q), 1)))
    if pts:
        q = np.concatenate(pts)
        rgb += ndi.gaussian_filter(splat(q[:, 0], q[:, 1], np.concatenate(cws), n, n), (1.0, 1.0, 0))
    return np.clip(rgb, 0, 1.6), np.clip(a, 0, 0.7)


def tex_ribbon(Z, t, rows=12, cw=8, rh=8):
    """The agent's view: its last `rows` observation vectors (newest at the +y edge), each coordinate a
    small cell in the hidden permuted order, standardised for display."""
    lo = max(0, t - rows + 1)
    Zr = Z[lo:t + 1]
    v = np.tanh(Zr / 1.6)
    rgb = 0.05 + np.clip(v, 0, None)[..., None] * ORANGE + np.clip(-v, 0, None)[..., None] * CYAN
    rgb = rgb * 1.3 * np.linspace(0.3, 1.0, rows)[:, None, None] ** 1.2   # older rows fade
    rgb[-1] *= 1.35
    rgb = np.repeat(np.repeat(rgb, rh, 0), cw, 1)
    col = np.arange(rgb.shape[1]) % cw
    row = np.arange(rgb.shape[0]) % rh
    rgb[:, col < 2] *= 0.08
    rgb[row < 2] *= 0.08
    return rgb, np.full(rgb.shape[:2], 0.45)


# ------------------------------------------------------------------------------------------- drawing
def warp_plane(canvas, cam, O, U, V, rgb, alpha, fill=0.0, fill_a=0.0):
    """Composite a textured planar quad (O + s U + t V, s,t in [0,1]) onto canvas: over, emissive."""
    Hs, Ws, _ = canvas.shape
    corners = np.array([O, O + U, O + U + V, O + V])
    p, _ = cam.proj(corners)
    x0, y0 = np.floor(p.min(0)).astype(int) - 1
    x1, y1 = np.ceil(p.max(0)).astype(int) + 2
    x0, y0, x1, y1 = max(x0, 0), max(y0, 0), min(x1, Ws), min(y1, Hs)
    if x1 <= x0 or y1 <= y0:
        return
    Hi = np.linalg.inv(cam.homography(O, U, V))
    yy, xx = np.mgrid[y0:y1, x0:x1].astype(float) + 0.5
    q = np.einsum("ij,jhw->ihw", Hi, np.stack([xx, yy, np.ones_like(xx)]))
    s, tt = q[0] / q[2], q[1] / q[2]
    m = (s >= 0) & (s <= 1) & (tt >= 0) & (tt <= 1) & (q[2] > 0)
    if not m.any():
        return
    Ht, Wt = alpha.shape
    rr, cc = tt[m] * Ht - 0.5, s[m] * Wt - 0.5
    ch = [ndi.map_coordinates(rgb[..., k], [rr, cc], order=1, mode="nearest") for k in range(3)]
    av = ndi.map_coordinates(alpha, [rr, cc], order=1, mode="nearest")
    av = np.clip(av + fill_a, 0, 1)
    sub = canvas[y0:y1, x0:x1]
    em = (np.stack(ch, -1) + fill) * cam.fog(q[2][m])[:, None]
    sub[m] = sub[m] * (1 - av[:, None]) + em


def bez(P0, P1, P2, P3, u):
    u = u[:, None]
    return (1 - u) ** 3 * P0 + 3 * (1 - u) ** 2 * u * P1 + 3 * (1 - u) * u ** 2 * P2 + u ** 3 * P3


class Lines:
    """Additive thread layer: dense projected samples of 3D curves, splatted bilinearly in one pass."""

    def __init__(self, Hs, Ws, SS=1):
        self.Hs, self.Ws, self.SS = Hs, Ws, SS
        self.pend = []

    def curve(self, cam, path, cA, cB, iA, iB, gamma=1.5, fade=0.12, dots=0, cgamma=0.8, fade_end=0.0):
        """path(u) -> (n, 3) for u in [0, 1]. Intensity iA -> iB (power gamma), colour cA -> cB."""
        p0, _ = cam.proj(path(np.linspace(0, 1, 33)))
        L = np.hypot(*np.diff(p0, axis=0).T).sum()
        n = int(np.ceil(L / 0.35)) + 2
        u = np.linspace(0, 1, n)
        p, zd = cam.proj(path(u))
        step = np.hypot(*np.gradient(p, axis=0).T)                # per-sample weight = local step (px)
        w = (iA + (iB - iA) * u ** gamma) * cam.fog(zd)
        if fade > 0:
            w = w * np.clip(u / fade, 0, 1) ** 2
        if fade_end > 0:
            w = w * np.clip((1 - u) / fade_end, 0, 1) ** 2
        if dots:
            w = w * (np.sin(u * dots * 2 * np.pi) > 0.3)
        w = w * self.SS * step
        col = cA[None] + u[:, None] ** cgamma * (cB - cA)[None]
        self.pend.append((p, col * w[:, None]))

    def seg(self, cam, A, B, cA, cB, iA, iB, **kw):
        A, B = np.asarray(A, float), np.asarray(B, float)
        self.curve(cam, lambda u: A[None] + u[:, None] * (B - A)[None], cA, cB, iA, iB, **kw)

    def flush(self, canvas, glow=0.0, sigma=3.0):
        if not self.pend:
            return
        p = np.concatenate([a for a, _ in self.pend])
        cw = np.concatenate([b for _, b in self.pend])
        self.pend = []
        img = splat(p[:, 0], p[:, 1], cw, self.Hs, self.Ws)
        if glow > 0:
            img = img + glow * ndi.gaussian_filter(img, (sigma, sigma, 0))
        canvas += img


def splat(x, y, cw, Hs, Ws):
    x, y = x - 0.5, y - 0.5
    ix, iy = np.floor(x).astype(int), np.floor(y).astype(int)
    fx, fy = x - ix, y - iy
    out = np.zeros((3, Hs * Ws))
    for dx, dy, ww in ((0, 0, (1 - fx) * (1 - fy)), (1, 0, fx * (1 - fy)), (0, 1, (1 - fx) * fy), (1, 1, fx * fy)):
        jx, jy = ix + dx, iy + dy
        ok = (jx >= 0) & (jx < Ws) & (jy >= 0) & (jy < Hs)
        idx = jy[ok] * Ws + jx[ok]
        for k in range(3):
            out[k] += np.bincount(idx, weights=(ww * cw[:, k])[ok], minlength=Hs * Ws)
    return out.reshape(3, Hs, Ws).transpose(1, 2, 0)


def flare(A, B, sweep=0.55, low=0.12, rise=0.5, tip=1.0):
    """A funnel thread from A (low, wide) to B (high, the neck): sweeps inward close to A's plane, then
    rises into B, so a bundle of them draws a flared funnel rather than a straight cone. tip sets the
    arrival direction: 1 = straight up (threads overlap in a spout), 0 = along the chord (they meet
    only at the point)."""
    A, B = np.asarray(A, float), np.asarray(B, float)
    h = B[2] - A[2]
    P1 = np.array([A[0] + sweep * (B[0] - A[0]), A[1] + sweep * (B[1] - A[1]), A[2] + low * h])
    P2 = B - rise * (tip * np.array([0, 0, h]) + (1 - tip) * (B - A))
    return lambda u: bez(A, P1, P2, B, u)


def edge_lines(lines, cam, O, U, V, inten, col=PALE):
    C = [O, O + U, O + U + V, O + V, O]
    for a, b in zip(C[:-1], C[1:]):
        lines.seg(cam, a, b, col, col, inten, inten, gamma=1.0, fade=0.0)


def ring(lines, cam, P, r, col, inten, n=97):
    th = np.linspace(0, 2 * np.pi, n)
    pts = [P + np.array([r * np.cos(a), r * np.sin(a), 0.0]) for a in th]
    for a, b in zip(pts[:-1], pts[1:]):
        lines.seg(cam, a, b, col, col, inten, inten, gamma=1.0, fade=0.0)


# -------------------------------------------------------------------------------------------- scene
def scene(D, cfg, SS):
    W, H = cfg["W"] * SS, cfg["H"] * SS
    S = cfg["sides"]                                  # plane sides, level 0..2
    z = cfg["z"]                                      # heights of plane 0, 1, 2, strip
    Wr, Dr = cfg["strip"]
    corner = lambda i: np.array([-S[i] / 2, -S[i] / 2, z[i]])  # noqa: E731
    UV = lambda i: (np.array([S[i], 0, 0.0]), np.array([0, S[i], 0.0]))  # noqa: E731
    Os = np.array([-Wr / 2, -Dr / 2, z[3]])
    Us, Vs = np.array([Wr, 0, 0.0]), np.array([0, Dr, 0.0])

    def world(i, cx, cy):            # level-0 cell coords (col, row) -> point on plane i
        return np.array([S[i] * (cx / 128.0 - 0.5), S[i] * (cy / 128.0 - 0.5), z[i]])

    cam = Cam(cfg["el"], cfg["az"], cfg["dist"], target=(0, 0, cfg["target_z"]))
    pts = np.array([[sx * S[i] / 2, sy * S[i] / 2, z[i]] for sx in (-1, 1) for sy in (-1, 1) for i in range(3)] +
                   [[sx * Wr / 2, sy * Dr / 2, z[3]] for sx in (-1, 1) for sy in (-1, 1)])
    cam.fit(pts, tuple(v * SS for v in cfg["box"]))
    cam.fog_k = cfg.get("fog", 0.35)
    px_per_world = cam.f / np.linalg.norm(cam.t)     # rough screen scale at the stack centre

    canvas = np.zeros((H, W, 3))
    yy, xx = np.mgrid[0:H, 0:W].astype(float)
    pc, _ = cam.proj(np.array([0, 0, 0.45 * z[3]]))
    r = np.hypot((xx - pc[0]) / W, (yy - pc[1]) / W)
    canvas += (np.exp(-0.5 * (r / 0.30) ** 2) * 0.05)[..., None] * np.array([0.35, 0.6, 0.75])
    # a soft pool of light under the matter plane: it rests on something
    pf, _ = cam.proj(np.array([0, 0, z[0]]))
    rf = np.hypot((xx - pf[0]) / (S[0] * px_per_world * 0.75), (yy - pf[1]) / (S[0] * px_per_world * 0.32))
    canvas += (np.exp(-0.5 * (rf / 0.75) ** 2) * cfg.get("pool", 0.05))[..., None] * np.array([0.3, 0.55, 0.7])
    canvas += np.array([0.012, 0.016, 0.022])

    x, blocks = D["x"], D["blocks"]
    bodies = decode(D["L"][D["t"]])
    lines = Lines(H, W, SS)

    # plane 0: matter, as a glass slab with a little thickness
    rgb0, a0 = tex_matter(x, D["past"], grid=cfg.get("grid", 0.05))
    th = cfg.get("slab", 0.035)
    O0, (U0, V0) = corner(0), UV(0)
    for c in (O0, O0 + U0, O0 + U0 + V0, O0 + V0):
        lines.seg(cam, c - [0, 0, th], c, PALE, PALE, 0.3, 0.3, gamma=1.0, fade=0.0)
    edge_lines(lines, cam, O0 - [0, 0, th], U0, V0, 0.22)
    lines.flush(canvas)
    warp_plane(canvas, cam, O0, U0, V0, rgb0, a0, fill=0.024, fill_a=0.04)
    edge_lines(lines, cam, O0, U0, V0, 0.5)
    lines.flush(canvas, glow=0.3, sigma=2.0 * SS)

    # funnels 0 -> 1: matter cells to the tile of the block they average into
    msum = x.sum(0)
    bm = blocks.sum(0)
    for bi in range(G):
        for bj in range(G):
            if bm[bi, bj] < 0.01:
                continue
            cell = msum[bi * 16:(bi + 1) * 16, bj * 16:(bj + 1) * 16]
            wts = np.clip(cell - 0.03, 0, None).ravel()
            if wts.sum() <= 0:
                continue
            nthr = int(np.clip(bm[bi, bj] * cfg["thr_per_mass"], 10, 48))
            pick = RNG.choice(256, size=min(nthr, int((wts > 0).sum())), replace=False, p=wts / wts.sum())
            k_int = 1.0 / np.sqrt(len(pick))
            Bc = world(1, bj * 16 + 8, bi * 16 + 8)
            # the funnel's envelope: faint threads from the block's outline, so its mouth is the whole block
            occ = np.sqrt(min(bm[bi, bj] / 0.08, 1.0))
            bcol = to_rgb(blocks[:, bi:bi + 1, bj:bj + 1] * 6)[0, 0]
            mouth = 0.5 * PALE + 0.5 * bcol / max(bcol.max(), 1e-6)   # the block's mean hue at the mouth
            ne = cfg.get("env_n", 5)
            if cfg.get("mouth_i", 0) > 0:     # the funnel's mouth: the block's outline on the matter plane
                mo = world(0, bj * 16, bi * 16)
                edge_lines(lines, cam, mo, np.array([S[0] / G, 0, 0]), np.array([0, S[0] / G, 0]),
                           cfg["mouth_i"] * occ, col=mouth)
            for k in range(4 * ne):
                side_, q_ = divmod(k, ne)
                q_ = (q_ + 0.5) / ne if cfg.get("env_mid", True) else q_ / ne
                ex, ey = [(q_, 0), (1, q_), (1 - q_, 1), (0, 1 - q_)][side_]
                A = world(0, bj * 16 + 16 * ex, bi * 16 + 16 * ey)
                lines.curve(cam, flare(A, Bc, **cfg["flare01"]), mouth, PALE,
                            cfg["env_i"][0] * occ, cfg["env_i"][1] * occ, gamma=1.0, fade=0.0)
            for k in pick:
                r_, c_ = divmod(k, 16)
                cy_, cx_ = bi * 16 + r_, bj * 16 + c_
                ccol = to_rgb(x[:, cy_:cy_ + 1, cx_:cx_ + 1])[0, 0]
                ccol = ccol / max(ccol.max(), 1e-6)
                A = world(0, cx_ + 0.5 + RNG.uniform(-.4, .4), cy_ + 0.5 + RNG.uniform(-.4, .4))
                lines.curve(cam, flare(A, Bc, **cfg["flare01"]), ccol, PALE,
                            cfg["fun_i"][0] * k_int, cfg["fun_i"][1] * k_int, gamma=1.0, cgamma=2.2, fade=0.03)
    lines.flush(canvas, glow=0.25, sigma=1.5 * SS)

    # plane 1: block means
    rgb1, a1 = tex_blocks(blocks)
    warp_plane(canvas, cam, corner(1), *UV(1), rgb1, a1, fill=0.016, fill_a=0.07)
    edge_lines(lines, cam, corner(1), *UV(1), 0.3)
    lines.flush(canvas)

    # funnels 1 -> 2: tiles whose block centre lies under a body's disc (with a margin) to the body
    for b in bodies:
        near = []
        for bi in range(G):
            for bj in range(G):
                if bm[bi, bj] < 0.01:
                    continue
                d = np.hypot(bj * 16 + 8 - b["cx"], bi * 16 + 8 - b["cy"])
                if d < b["r"] + 12:
                    near.append((bi, bj))
        P = world(2, b["cx"], b["cy"])
        h12 = cfg.get("tile_half", 6.5)               # half-width of a drawn tile, in cells
        ne = cfg.get("env12_n", 3)
        for bi, bj in near:                 # a narrow funnel from each tile's outline to the body
            for k in range(4 * ne):
                side_, q_ = divmod(k, ne)
                q_ = (q_ + 0.5) / ne
                ex, ey = [(q_, 0), (1, q_), (1 - q_, 1), (0, 1 - q_)][side_]
                A = world(1, bj * 16 + 8 + h12 * (2 * ex - 1), bi * 16 + 8 + h12 * (2 * ey - 1))
                lines.curve(cam, flare(A, P, **cfg["flare12"]), PALE * 0.9, CYAN, *cfg["env12_i"],
                            gamma=1.2, fade=0.0)
    lines.flush(canvas, glow=0.35, sigma=2.0 * SS)

    # plane 2: tracked bodies
    rgb2, a2 = tex_bodies(bodies, trails(D))
    warp_plane(canvas, cam, corner(2), *UV(2), rgb2, a2, fill=0.014, fill_a=0.06)
    edge_lines(lines, cam, corner(2), *UV(2), 0.28)
    lines.flush(canvas)

    # gather: 12 fibres per body from its ring to the observation port, then a fan to the strip columns
    port = np.array([0.0, cfg.get("port_y", 0.0), z[3] - cfg["port_drop"]])
    out_map = D["out_map"]
    pos = {int(j): i for i, j in enumerate(out_map)}
    nobs = len(out_map)
    for b in bodies:
        rr = b["r"] * S[2] / 128
        C = world(2, b["cx"], b["cy"])
        for f in range(NF):
            a_ = 2 * np.pi * f / NF
            A = C + np.array([rr * np.cos(a_), rr * np.sin(a_), 0.0])
            lines.curve(cam, flare(A, port, **cfg["flare23"]), CYAN, PALE, cfg["gather_i"][0],
                        cfg["gather_i"][1], gamma=1.2, fade=0.06, cgamma=1.5)
    lines.flush(canvas, glow=0.35, sigma=2.0 * SS)
    yrow = -Dr / 2 + Dr * (11.5 / 12)                # centre line of the newest row
    for b in bodies:
        for f in range(NF):
            i = pos[b["slot"] * NF + f]
            P1 = np.array([-Wr / 2 + Wr * (i + 0.5) / nobs, yrow, z[3]])
            lines.seg(cam, port, P1, PALE, PALE, cfg["fan_i"][0], cfg["fan_i"][1], gamma=1.0, fade=0.0)
    ring(lines, cam, port, 0.012, WARM, 0.5, n=49)
    lines.flush(canvas, glow=0.5, sigma=2.0 * SS)

    # the strip: the agent's view
    rgb3, a3 = tex_ribbon(D["Z"], D["t"])
    warp_plane(canvas, cam, Os, Us, Vs, rgb3, a3)
    edge_lines(lines, cam, Os, Us, Vs, 0.45)

    # the agent acts blind: one dotted thread falling from the strip onto the matter
    act = cfg["act"]
    tgt = [b for b in bodies if b["slot"] == act["slot"]][0]
    Bp = world(0, tgt["cx"] + act.get("dx", 0), tgt["cy"] + act.get("dy", 0))
    avoid, _ = cam.proj(np.array([world(2, o["cx"], o["cy"]) for o in bodies] + [port]))
    rad = np.array([o["r"] * S[2] / 128 * px_per_world + 10 * SS for o in bodies] + [24 * SS])

    def clearance(u_):               # screen distance from the falling thread to the nearest disc or the port
        pA, _ = cam.proj(np.array([-Wr / 2 + Wr * u_, 0.0, z[3]]))
        pB, _ = cam.proj(Bp)
        d = pB - pA
        w_ = np.clip(((avoid - pA) @ d) / (d @ d), 0, 1)
        return (np.hypot(*(avoid - pA - w_[:, None] * d).T) - rad).min()
    u_act = act["u"] if act["u"] != "auto" else max(np.linspace(0.04, 0.46, 43), key=clearance)
    A = np.array([-Wr / 2 + Wr * u_act, -Dr / 2 + Dr * 0.5, z[3]])
    lines.seg(cam, A, Bp, WARM, WARM, 1.5, 1.5, gamma=1.0, fade=0.0, dots=70)
    for rr, ii in ((2.5, 0.6), (5.0, 0.35), (8.0, 0.18)):
        ring(lines, cam, Bp, rr * S[0] / 128, WARM, ii)
    lines.flush(canvas, glow=0.8, sigma=2.0 * SS)
    return canvas, cam


# ----------------------------------------------------------------------------------------- finishing
def finish(canvas, SS, cfg):
    H, W = cfg["H"], cfg["W"]
    img = canvas.reshape(H, SS, W, SS, 3).mean((1, 3))
    bright = np.clip(img - 0.25, 0, None)
    img = img + 0.45 * ndi.gaussian_filter(bright, (5, 5, 0)) + 0.35 * ndi.gaussian_filter(bright, (22, 22, 0))
    yy, xx = np.mgrid[0:H, 0:W].astype(float)
    r = np.hypot((xx - W / 2) / (W / 2), (yy - H / 2) / (H / 2))
    img *= (1 - 0.35 * np.clip(r - 0.55, 0, None) ** 1.5)[..., None]
    img = 1 - np.exp(-1.15 * img)                     # soft shoulder tone map
    img += np.random.default_rng(3).normal(0, 0.008, img.shape)
    return np.clip(img, 0, 1)


def compose(img, cfg, out):
    W, H = cfg["W"], cfg["H"]
    fig = plt.figure(figsize=(W / 100, H / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.imshow(img, interpolation="nearest")
    ax.set_axis_off()
    T = cfg["title"]
    fpx = lambda px: px * 72 / 100  # noqa: E731   pixel height -> points at dpi 100
    ft = FontProperties(fname=FONT_TITLE)
    fig.text(T["x"] / W, 1 - T["y"] / H, "PhySim", fontproperties=ft,
             fontsize=fpx(T["size"]), color="#f3f1ea", ha="left", va="baseline")
    fig.canvas.draw()
    t0 = fig.texts[-1].get_window_extent()
    fig.text((t0.x1 + T["size"] * T.get("v_gap", 0.2)) / W, 1 - T["y"] / H, "v2", fontproperties=ft,
             fontsize=fpx(T["size"]), color=T.get("v_col", "#4fd3f5"), ha="left", va="baseline")
    fig.text((T["x"] + T.get("sub_dx", 0)) / W, 1 - (T["y"] + T["sub_dy"]) / H, "supervenience",
             fontproperties=FontProperties(fname=FONT_SUB), fontsize=fpx(T["sub_size"]), color="#e2ecef",
             ha="left", va="baseline")
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())[..., :3]
    plt.close(fig)
    assert buf.shape == (H, W, 3), buf.shape
    im = Image.fromarray(np.ascontiguousarray(buf))
    im.save(out, optimize=True)
    th = im.resize((400, round(400 * H / W)), Image.LANCZOS)
    th.save(os.path.join(os.path.dirname(out), "thumb_" + os.path.basename(out)))


COMMON = dict(sides=(2.7, 1.9, 1.5), z=(0.0, 0.55, 1.35, 2.22), strip=(1.2, 0.38),
              el=30, env_n=10, env_i=(0.10, 0.05), mouth_i=0.22, env12_n=3, env12_i=(0.05, 0.13), az=-58, dist=8.0, target_z=0.9, thr_per_mass=110, grid=0.05, slab=0.035,
              flare01=dict(sweep=0.5, low=0.22, rise=0.3, tip=0.25), flare12=dict(sweep=0.5, low=0.22, rise=0.3, tip=0.25),
              flare23=dict(sweep=0.4, low=0.2, rise=0.55), fun_i=(0.38, 0.18), gather_i=(0.12, 0.22),
              fan_i=(0.08, 0.13), port_drop=0.22, act=dict(slot=7, u="auto"))
LAND = dict(COMMON, W=1920, H=1080, box=(820, 50, 1870, 1035),
            title=dict(x=118, y=505, size=190, sub_dy=122, sub_size=84))
PORT = dict(COMMON, W=1080, H=1350, box=(40, 380, 1040, 1320),
            title=dict(x=86, y=222, size=180, sub_dy=110, sub_size=76))


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "both"
    SS = 1 if "--draft" in sys.argv else 2
    tag = sys.argv[sys.argv.index("--tag") + 1] if "--tag" in sys.argv else ""
    D = load(TICK)
    jobs = {"landscape": [(LAND, "cover.png")], "portrait": [(PORT, "cover_portrait.png")]}
    jobs["both"] = jobs["landscape"] + jobs["portrait"]
    outdir = os.path.join(HERE, "wip") if tag else HERE
    os.makedirs(outdir, exist_ok=True)
    for cfg, name in jobs[which]:
        canvas, cam = scene(D, cfg, SS)
        img = finish(canvas, SS, cfg)
        out = os.path.join(outdir, (tag + "_" if tag else "") + name)
        compose(img, cfg, out)
        print("wrote", out, flush=True)
