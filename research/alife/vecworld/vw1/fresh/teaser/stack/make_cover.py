"""PhySim v2 teaser cover, concept A: "the stack".

Four translucent planes float in perspective over a dark ground, built from one real VW-1 episode
(hero_objects_s0.npz / hero_coarse_s0.npz, tick T):
  plane 0  the level-0 matter field (Flow-Lenia, 2 channels x 128 x 128), coloured with to_rgb
  plane 1  its 8x8 block means (the first 128 numbers of Phi_coarse), as glass tiles
  plane 2  the tracked bodies of Phi_objects (12 slots), as soft discs with short trails
  plane 3  a thin ribbon: the agent's last observations, 144 numbers in its hidden permuted order
Threads of light rise from matter cells to the block they average into (64 -> 1), from blocks to the
body they belong to, and from each body to the scattered columns its features occupy in the ribbon
(out_map). One dotted thread falls from the ribbon back to the matter: the agent acting blind.
Poetic licence, stated: Phi_coarse and Phi_objects are two alternative upper levels, each computed
from level 0 directly; the stack shows them as one chain. The episode file stores no actions, so the
falling thread's landing point (on a glider at cell 70,100) is illustrative, not a recorded input.

usage: python -B make_cover.py [landscape|portrait|both] [--tick T] [--draft]
Writes cover.png (1920x1080) and cover_portrait.png (1080x1350) next to this script.
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
MPL_TTF = os.path.join(matplotlib.get_data_path(), "fonts", "ttf")
FONT_TITLE = "/usr/share/fonts/opentype/inter/InterDisplay-ExtraLight.otf"
FONT_TITLE_V = "/usr/share/fonts/opentype/inter/InterDisplay-Thin.otf"
FONT_SUB = os.path.join(MPL_TTF, "cmti10.ttf")      # Computer Modern text italic

CYAN = np.array([0.15, 0.85, 1.0])
ORANGE = np.array([1.0, 0.45, 0.1])
PALE = np.array([0.78, 0.9, 1.0])
WARM = np.array([1.0, 0.82, 0.55])
K, NF, G = 12, 12, 8
RNG = np.random.default_rng(7)


# ----------------------------------------------------------------------------------------------- data
def load(t):
    o = np.load(f"{RES}/hero_objects_s0.npz")
    c = np.load(f"{RES}/hero_coarse_s0.npz")
    X = o["x"]                                    # (T, 2, 128, 128) level-0 matter
    Lo, tab, out_map, obs = o["L1"], o["tab"], o["out_map"], o["obs64"]
    Lc = c["L1"]
    assert np.array_equal(X[t], c["x"][t])
    blocks = Lc[t, :2 * G * G].reshape(2, G, G)   # Phi_coarse block means (same matter, same tick)
    sd = obs.std(0)
    Z = (obs - obs.mean(0)) / np.where(sd > 0, sd, 1.0)
    past = [X[max(t - d, 0)] for d in range(1, 11)]
    return dict(x=X[t], past=past, blocks=blocks, L=Lo, tab=tab, t=t, out_map=out_map, Z=Z)


def decode(y):
    S = y.reshape(K, NF)
    out = []
    for s in range(K):
        if S[s, 0] < 0.5:
            continue
        cx = np.arctan2(S[s, 4], S[s, 3]) * 128 / (2 * np.pi) % 128
        cy = np.arctan2(S[s, 6], S[s, 5]) * 128 / (2 * np.pi) % 128
        out.append(dict(slot=s, mass=S[s, 1], f1=S[s, 2], cx=cx, cy=cy, vx=S[s, 10], vy=S[s, 11]))
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
    def __init__(self, el, az, dist, target, f=1.0, c=(0.0, 0.0)):
        el, az = np.radians(el), np.radians(az)
        d = np.array([np.cos(el) * np.cos(az), np.cos(el) * np.sin(az), np.sin(el)])
        eye = np.asarray(target, float) + dist * d
        fwd = -d
        right = np.cross(fwd, [0, 0, 1.0])
        right /= np.linalg.norm(right)
        up = np.cross(right, fwd)
        self.R = np.stack([right, -up, fwd])
        self.t = -self.R @ eye
        self.f, self.c = f, np.asarray(c, float)
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
def tex_matter(x, past=(), up=4):
    """Level 0 at tick t (to_rgb), with faint ghosts of earlier ticks so the gliders carry their wake."""
    rgb = to_rgb(x)
    for k, xp in enumerate(past):
        rgb = np.maximum(rgb, 0.13 * np.exp(-k / 3.0) * to_rgb(xp))
    rgb = np.repeat(np.repeat(rgb, up, 0), up, 1)
    a = np.clip(rgb.max(-1) * 1.4, 0, 0.92)       # matter is fairly opaque: it occludes threads below
    return rgb, a


def tex_blocks(blocks, n=512, gain=2.0, gap=0.10, level=0.7):
    """8x8 glass tiles: each tile glows with to_rgb of its block mean (dimmer than the matter below),
    with a brighter rim so empty tiles still read as a lattice."""
    f = n // G
    up = np.repeat(np.repeat(blocks, f, 1), f, 2)
    lum = to_rgb(up * gain).max(-1)[..., None]               # brightness of the block mean, hue dropped
    yy, xx = np.mgrid[0:n, 0:n] % f / f
    inside = (xx > gap / 2) & (xx < 1 - gap / 2) & (yy > gap / 2) & (yy < 1 - gap / 2)
    e = 0.022
    edge = inside & ((xx < gap / 2 + e) | (xx > 1 - gap / 2 - e) | (yy < gap / 2 + e) | (yy > 1 - gap / 2 - e))
    rc = np.hypot(xx - 0.5, yy - 0.5)
    pool = np.exp(-0.5 * (rc / 0.16) ** 2)[..., None]        # light pooling where the threads land
    glass = PALE * (0.25 + 0.75 * pool)
    rgb = lum * glass * inside[..., None] * level
    rgb = rgb + 0.016 * inside[..., None] * PALE + (0.045 + 0.45 * lum) * edge[..., None] * PALE
    a = 0.05 * inside + 0.3 * rgb.max(-1)
    return rgb, np.clip(a, 0, 0.6)


def tex_bodies(bodies, tr, n=640, scale=0.55):
    """Each tracked body as an abstracted glider: warm core, cyan halo ring (radius = scale sqrt(mass),
    as in render_l1.draw_objects), plus a fading trail of its recent centres."""
    s = n / 128.0
    rgb = np.zeros((n, n, 3))
    a = np.zeros((n, n))
    for b in bodies:
        r = scale * np.sqrt(max(b["mass"], 0.0))
        R = r + 3.0
        for oy in (-128, 0, 128):
            for ox in (-128, 0, 128):
                cx, cy = b["cx"] + ox, b["cy"] + oy
                c0, c1 = int(max((cx - R) * s, 0)), int(min((cx + R) * s + 1, n))
                r0, r1 = int(max((cy - R) * s, 0)), int(min((cy + R) * s + 1, n))
                if c1 <= c0 or r1 <= r0:
                    continue
                yy, xx = (np.mgrid[r0:r1, c0:c1] + 0.5) / s
                d = np.hypot(xx - cx, yy - cy)
                core = np.exp(-0.5 * (d / (0.42 * r)) ** 2)
                halo = np.exp(-0.5 * (d / (0.9 * r)) ** 2)
                ring = np.exp(-0.5 * ((d - r) / 0.3) ** 2)
                rgb[r0:r1, c0:c1] += (0.55 * core[..., None] * WARM + 0.10 * halo[..., None] * CYAN
                                      + 0.75 * ring[..., None] * CYAN)
                a[r0:r1, c0:c1] += 0.45 * core
    pts, cws = [], []
    for sl, P in tr.items():
        P = np.array(P)
        for i in range(1, len(P)):
            if np.abs(P[i] - P[i - 1]).max() > 64:
                continue
            u = np.linspace(0, 1, 40, endpoint=False)[:, None]
            q = (P[i - 1] + u * (P[i] - P[i - 1])) * s
            w = 0.10 * (i / len(P)) ** 1.5 * np.hypot(*(P[i] - P[i - 1])) * s / 40
            pts.append(q)
            cws.append(np.tile(CYAN * w, (len(q), 1)))
    if pts:
        q = np.concatenate(pts)
        rgb += ndi.gaussian_filter(splat(q[:, 0], q[:, 1], np.concatenate(cws), n, n), (1.0, 1.0, 0))
    return np.clip(rgb, 0, 1.6), np.clip(a, 0, 0.6)


def ribbon_colour(Zrows):
    v = np.tanh(Zrows / 1.6)
    rgb = 0.05 + np.clip(v, 0, None)[..., None] * ORANGE + np.clip(-v, 0, None)[..., None] * CYAN
    return rgb * 1.25


def tex_ribbon(Z, t, rows=12, cw=8, rh=8):
    """The agent's view: its last `rows` observation vectors, one per tick (newest at the front edge),
    each coordinate a small cell in the hidden permuted order, standardised for display."""
    lo = max(0, t - rows + 1)
    Zr = Z[lo:t + 1]
    if len(Zr) < rows:
        Zr = np.vstack([np.zeros((rows - len(Zr), Z.shape[1])), Zr])
    rgb = ribbon_colour(Zr)                                  # (rows, n_obs, 3), oldest first
    age = np.linspace(0.3, 1.0, rows)[:, None, None] ** 1.2   # older rows fade toward the back
    rgb = rgb * age
    rgb[-1] *= 1.35                                           # the current observation
    rgb = np.repeat(np.repeat(rgb, rh, 0), cw, 1)
    col = np.arange(rgb.shape[1]) % cw
    row = np.arange(rgb.shape[0]) % rh
    rgb[:, col < 2] *= 0.08                                   # gaps: discrete anonymous numbers
    rgb[row < 2] *= 0.08
    a = np.full(rgb.shape[:2], 0.4)
    return rgb, a


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


class Lines:
    """Additive thread layer: dense projected samples of 3D segments, splatted bilinearly in one pass."""

    def __init__(self, Hs, Ws, SS=1):
        self.Hs, self.Ws, self.SS = Hs, Ws, SS   # weights scale with SS so lines keep their output brightness
        self.pend = []

    def add(self, cam, A, B, cA, cB, iA, iB, gamma=1.5, fade=0.12, dots=0, cgamma=0.8):
        A, B = np.asarray(A, float), np.asarray(B, float)
        pa, _ = cam.proj(A)
        pb, _ = cam.proj(B)
        n = int(np.ceil(np.hypot(*(pb - pa)) / 0.35)) + 2
        u = np.linspace(0, 1, n)
        p, zd = cam.proj(A[None] + u[:, None] * (B - A)[None])
        w = (iA + (iB - iA) * u ** gamma) * cam.fog(zd)
        if fade > 0:
            w = w * np.clip(u / fade, 0, 1) ** 2
        if dots:
            w = w * (np.sin(u * dots * 2 * np.pi) > 0.3)
        w = w * self.SS * (np.hypot(*(pb - pa)) / max(n - 1, 1))   # per-sample weight = step length (px)
        col = cA[None] + u[:, None] ** cgamma * (cB - cA)[None]
        self.pend.append((p, col * w[:, None]))

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


# -------------------------------------------------------------------------------------------- scene
def scene(D, cfg, SS):
    W, H = cfg["W"] * SS, cfg["H"] * SS
    h = cfg["gap"]
    side = 2.0
    O = lambda z, y0=-1.0: np.array([-1.0, y0, z])  # noqa: E731
    U = np.array([side, 0, 0])
    Vfull = np.array([0, side, 0])
    rib_depth = cfg["ribbon_depth"]
    Vrib = np.array([0, rib_depth, 0])
    z = [0.0, h, 2 * h, 3 * h + cfg.get("top_extra", 0.0)]
    rib_y0 = -rib_depth / 2 + cfg.get("ribbon_y", 0.0)

    cam = Cam(cfg["el"], cfg["az"], cfg["dist"], target=(0, 0, cfg["target_z"] * h))
    pts = np.array([[sx, sy, zz] for sx in (-1, 1) for sy in (-1, 1) for zz in z[:3]] +
                   [[sx, rib_y0 + sy * rib_depth, z[3]] for sx in (-1, 1) for sy in (0, 1)])
    box = cfg["box"]
    cam.fit(pts, tuple(v * SS for v in box))
    cam.fog_k = cfg.get("fog", 0.35)

    def world(cx, cy, zz):            # level-0 pixel coords (col, row) -> world point on a 128-plane
        return np.array([-1 + side * cx / 128.0, -1 + side * cy / 128.0, zz])

    canvas = np.zeros((H, W, 3))
    # ground: faint radial lift behind the stack
    yy, xx = np.mgrid[0:H, 0:W].astype(float)
    pc, _ = cam.proj(np.array([0, 0, 1.2 * h]))
    r = np.hypot((xx - pc[0]) / W, (yy - pc[1]) / W)
    canvas += (np.exp(-0.5 * (r / 0.32) ** 2) * 0.05)[..., None] * np.array([0.35, 0.6, 0.75])
    canvas += np.array([0.012, 0.016, 0.022])

    x, blocks = D["x"], D["blocks"]
    bodies = decode(D["L"][D["t"]])
    lines = Lines(H, W, SS)

    # plane 0: matter
    rgb0, a0 = tex_matter(x, D["past"])
    warp_plane(canvas, cam, O(z[0]), U, Vfull, rgb0, a0, fill=0.018, fill_a=0.0)
    edge_lines(lines, cam, O(z[0]), U, Vfull, 0.32)
    lines.flush(canvas)

    # threads 0 -> 1: sampled matter cells to the centre of the block they average into
    msum = x.sum(0)
    bm = blocks.sum(0)
    for bi in range(G):
        for bj in range(G):
            if bm[bi, bj] < 0.012:
                continue
            cell = msum[bi * 16:(bi + 1) * 16, bj * 16:(bj + 1) * 16]
            wts = np.clip(cell - 0.05, 0, None).ravel()
            if wts.sum() <= 0:
                continue
            nthr = int(np.clip(bm[bi, bj] * cfg["thr_per_mass"], 6, 28))
            pick = RNG.choice(256, size=min(nthr, int((wts > 0).sum())), replace=False, p=wts / wts.sum())
            k_int = 1.0 / np.sqrt(len(pick))                      # keep the funnel tops from burning white
            for k in pick:
                r_, c_ = divmod(k, 16)
                cy_, cx_ = bi * 16 + r_, bj * 16 + c_
                ccol = to_rgb(x[:, cy_:cy_ + 1, cx_:cx_ + 1])[0, 0]
                ccol = ccol / max(ccol.max(), 1e-6)
                jx, jy = RNG.normal(0, 1.2, 2)                      # land softly near the block centre
                Bc = world(bj * 16 + 8 + jx, bi * 16 + 8 + jy, z[1])
                lines.add(cam, world(cx_ + 0.5, cy_ + 0.5, z[0]), Bc, ccol, PALE, 0.3 * k_int, 0.75 * k_int,
                          gamma=1.6, cgamma=3.0, fade=0.08)
    lines.flush(canvas, glow=0.2, sigma=1.5 * SS)

    # plane 1: block means
    rgb1, a1 = tex_blocks(blocks)
    warp_plane(canvas, cam, O(z[1]), U, Vfull, rgb1, a1, fill=0.016, fill_a=0.07)
    edge_lines(lines, cam, O(z[1]), U, Vfull, 0.28)
    lines.flush(canvas)

    # threads 1 -> 2: blocks with matter near each body to the body
    for b in bodies:
        rb = 0.55 * np.sqrt(b["mass"])
        for bi in range(G):
            for bj in range(G):
                if bm[bi, bj] < 0.012:
                    continue
                bx, by = bj * 16 + 8, bi * 16 + 8
                dx, dy = bx - b["cx"], by - b["cy"]
                if abs(dx) > 64 or abs(dy) > 64:      # do not draw across the torus seam
                    continue
                if np.hypot(dx, dy) > rb + 14:
                    continue
                col = CYAN
                lines.add(cam, world(bx, by, z[1]), world(b["cx"], b["cy"], z[2]), PALE * 0.9, col,
                          0.15, 0.45, gamma=1.6, fade=0.2)
    lines.flush(canvas, glow=0.35, sigma=2.0 * SS)

    # plane 2: tracked bodies
    rgb2, a2 = tex_bodies(bodies, trails(D))
    warp_plane(canvas, cam, O(z[2]), U, Vfull, rgb2, a2, fill=0.014, fill_a=0.06)
    edge_lines(lines, cam, O(z[2]), U, Vfull, 0.26)
    lines.flush(canvas)

    # threads 2 -> 3: each body's 12 features scatter to their permuted columns in the ribbon
    out_map = D["out_map"]
    pos = {int(j): i for i, j in enumerate(out_map)}          # L1 index -> observation column
    nobs = len(out_map)
    for b in bodies:
        col = CYAN
        for f in range(NF):
            i = pos[b["slot"] * NF + f]
            P1 = np.array([-1 + side * (i + 0.5) / nobs, rib_y0 + rib_depth, z[3]])
            lines.add(cam, world(b["cx"], b["cy"], z[2]), P1, col, PALE, 0.08, 0.22, gamma=1.0, fade=0.1)
    lines.flush(canvas)

    # plane 3: the agent's ribbon
    rgb3, a3 = tex_ribbon(D["Z"], D["t"])
    warp_plane(canvas, cam, O(z[3], rib_y0), U, Vrib, rgb3, a3, fill=0.0, fill_a=0.0)
    edge_lines(lines, cam, O(z[3], rib_y0), U, Vrib, 0.4)

    # the agent acts blind: one dotted thread falling from the ribbon onto the matter
    act = cfg["act"]
    Bp = world(act["cx"], act["cy"], z[0])
    pB, _ = cam.proj(Bp)
    avoid, _ = cam.proj(np.array([world(o["cx"], o["cy"], z[2]) for o in bodies]))
    radii = np.array([0.55 * np.sqrt(o["mass"]) for o in bodies]) * cam.f * side / 128 / cam.t[2] + 8 * SS

    def clearance(i):            # screen distance from the falling line to the nearest body glyph
        pA, _ = cam.proj(np.array([-1 + side * (i + 0.5) / nobs, rib_y0 + rib_depth * 0.5, z[3]]))
        d = pB - pA
        u = np.clip(((avoid - pA) @ d) / (d @ d), 0, 1)
        return (np.hypot(*(avoid - pA - u[:, None] * d).T) - radii).min()
    iA = act["col"] if act["col"] != "auto" else max(range(nobs // 3, nobs - 8), key=clearance)
    A = np.array([-1 + side * (iA + 0.5) / nobs, rib_y0 + rib_depth * 0.5, z[3]])
    lines.add(cam, A, Bp, WARM, WARM, 1.25, 1.25, gamma=1.0, fade=0.0, dots=60)
    for rr, ii in ((2.5, 0.6), (5.0, 0.35), (8.0, 0.18)):
        ring(lines, cam, world, act["cx"], act["cy"], z[0], rr, WARM, ii)
    lines.flush(canvas, glow=0.8, sigma=2.0 * SS)
    return canvas, cam


def edge_lines(lines, cam, O, U, V, inten):
    C = [O, O + U, O + U + V, O + V, O]
    for a, b in zip(C[:-1], C[1:]):
        lines.add(cam, a, b, PALE, PALE, inten, inten, gamma=1.0, fade=0.0)


def ring(lines, cam, world, cx, cy, zz, r, col, inten):
    th = np.linspace(0, 2 * np.pi, 97)
    P = [world(cx + r * np.cos(a), cy + r * np.sin(a), zz) for a in th]
    for a, b in zip(P[:-1], P[1:]):
        lines.add(cam, a, b, col, col, inten, inten, gamma=1.0, fade=0.0)


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
    img += RNG.normal(0, 0.008, img.shape)
    return np.clip(img, 0, 1)


def compose(img, cfg, out):
    W, H = cfg["W"], cfg["H"]
    fig = plt.figure(figsize=(W / 100, H / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.imshow(img, interpolation="nearest")
    ax.set_axis_off()
    T = cfg["title"]
    fpx = lambda px: px * 72 / 100  # noqa: E731   pixel height -> points at dpi 100
    fig.text(T["x"] / W, 1 - T["y"] / H, "PhySim", fontproperties=FontProperties(fname=FONT_TITLE),
             fontsize=fpx(T["size"]), color="#f2f6f8", ha="left", va="baseline")
    # measure "PhySim" to place "v2" after it
    fig.canvas.draw()
    t0 = fig.texts[-1].get_window_extent()
    fig.text((t0.x1 + T["size"] * 0.22) / W, 1 - T["y"] / H, "v2", fontproperties=FontProperties(fname=FONT_TITLE_V),
             fontsize=fpx(T["size"]), color="#7fdcf2", ha="left", va="baseline")
    fig.text(T["x"] / W + T.get("sub_dx", 0) / W, 1 - (T["y"] + T["sub_dy"]) / H, "supervenience",
             fontproperties=FontProperties(fname=FONT_SUB), fontsize=fpx(T["sub_size"]), color="#d6e3e8",
             ha="left", va="baseline")
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())[..., :3]
    plt.close(fig)
    assert buf.shape == (H, W, 3), buf.shape
    Image.fromarray(np.ascontiguousarray(buf)).save(out, optimize=True)


LAND = dict(W=1920, H=1080, gap=0.8, ribbon_depth=0.62, el=24, az=-58, dist=7.5, target_z=1.4,
            box=(870, 60, 1850, 1020), thr_per_mass=80,
            act=dict(col="auto", cx=70, cy=100),
            title=dict(x=120, y=520, size=156, sub_dy=104, sub_size=74))
PORT = dict(W=1080, H=1350, gap=0.8, ribbon_depth=0.62, el=24, az=-58, dist=7.5, target_z=1.4,
            box=(50, 400, 1030, 1305), thr_per_mass=80,
            act=dict(col="auto", cx=70, cy=100),
            title=dict(x=88, y=218, size=150, sub_dy=100, sub_size=70))


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "both"
    tick = int(sys.argv[sys.argv.index("--tick") + 1]) if "--tick" in sys.argv else 278
    SS = 1 if "--draft" in sys.argv else 2
    D = load(tick)
    jobs = {"landscape": [(LAND, "cover.png")], "portrait": [(PORT, "cover_portrait.png")]}
    jobs["both"] = jobs["landscape"] + jobs["portrait"]
    for cfg, name in jobs[which]:
        canvas, cam = scene(D, cfg, SS)
        img = finish(canvas, SS, cfg)
        compose(img, cfg, os.path.join(HERE, name))
        print("wrote", os.path.join(HERE, name), flush=True)
