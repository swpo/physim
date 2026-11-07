"""PhySim v2 teaser cover, concept C "the aperture".

The bottom of the frame is the level-0 matter of one real VW-1 episode (hero_objects_s0.npz, Flow-Lenia
gliders, coloured with level0/render.to_rgb) laid out as a ground plane in perspective; the torus is tiled,
which is what a torus looks like when you stand on it. Light fibres rise from every occupied cell and channel
(cyan or orange thread, weighted by that channel's matter), bundle at its 8x8 coarse block (Phi_coarse geometry), bundle again at the tracked body
that block belongs to (Phi_objects slots decoded with integrate/render_l1.decode_slots, drawn as the usual
ring + orientation tick), and all of it passes through one small aperture. Above the aperture: a slim column
of the agent's actual observation o(t) at that tick, in its hidden permuted order, quantised to 0.001. A faint
mark above the column is the agent; one thin line falls from it back to the field.

usage: OMP_NUM_THREADS=1 nice -n 10 python -B make_cover.py [land|portrait|both] [TICK=120]   (~25 s + ~15 s)
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
F_TITLE = "/usr/share/fonts/opentype/inter/InterDisplay-Light.otf"
F_TITLE2 = "/usr/share/fonts/opentype/inter/InterDisplay-Regular.otf"
F_MONO = "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Light.ttf"
F_MONO_SUB = "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Regular.ttf"
CYAN = np.array([0.15, 0.85, 1.0])      # level0/render.PAL[2]
ORANGE = np.array([1.0, 0.45, 0.1])
WARM = np.array([1.0, 0.93, 0.84])
N, G = 128, 8
BS = N // G


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
    return m, mb, cb_i, cb_j, owner, d_i, d_j


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


# ------------------------------------------------------------------------------------------- splatting
class Acc:
    """Collects (uv, rgb weight) samples; one bilinear additive splat at the end."""

    def __init__(s, H, W):
        s.H, s.W, s.uv, s.w = H, W, [], []

    def curve(s, uv, rgb, ramp=None):
        """uv (R,S,2) or (S,2) in buffer px; rgb (R,3)/(3,) intensity per unit screen length."""
        uv = np.asarray(uv, float)
        if uv.ndim == 2:
            uv = uv[None]
        rgb = np.broadcast_to(np.asarray(rgb, float), (uv.shape[0], 3))
        seg = np.linalg.norm(np.diff(uv, axis=1), axis=-1)
        step = np.concatenate([seg[:, :1], 0.5 * (seg[:, 1:] + seg[:, :-1]), seg[:, -1:]], 1)
        if ramp is not None:
            step = step * ramp
        s.uv.append(uv.reshape(-1, 2))
        s.w.append((step[..., None] * rgb[:, None, :]).reshape(-1, 3))

    def point(s, uv, rgb):
        s.uv.append(np.asarray(uv, float).reshape(-1, 2))
        s.w.append(np.asarray(rgb, float).reshape(-1, 3))

    def render(s):
        buf = np.zeros((s.H * s.W, 3))
        uv, w = np.concatenate(s.uv), np.concatenate(s.w)
        u, v = uv[:, 0] - 0.5, uv[:, 1] - 0.5
        j0, i0 = np.floor(u).astype(np.int64), np.floor(v).astype(np.int64)
        fu, fv = u - j0, v - i0
        for di, dj, ww in ((0, 0, (1 - fu) * (1 - fv)), (0, 1, fu * (1 - fv)), (1, 0, (1 - fu) * fv), (1, 1, fu * fv)):
            ii, jj = i0 + di, j0 + dj
            ok = (ii >= 0) & (ii < s.H) & (jj >= 0) & (jj < s.W)
            idx = ii[ok] * s.W + jj[ok]
            for c in range(3):
                buf[:, c] += np.bincount(idx, weights=w[ok, c] * ww[ok], minlength=s.H * s.W)
        return buf.reshape(s.H, s.W, 3)


# ------------------------------------------------------------------------------------------------ scene
def render(L, tick, out):
    t0 = time.time()
    rng = np.random.default_rng(7)
    x, objs, obs, z = load(tick)
    m, mb, cb_i, cb_j, owner, d_i, d_j = hierarchy(x, objs)
    tex = to_rgb(x)
    W, H, SS = L["W"], L["H"], 2
    cam = Cam(W * SS, H * SS, L["f"] * SS, L["u0"] * SS, L["v0"] * SS, 1.0)
    cs, X0, Y0 = L["cs"], L["X0"], L["Y0"]
    A = cam.unproj(L["A_uv"][0] * SS, L["A_uv"][1] * SS, L["A_depth"])
    fogL = L["fogL"]
    y_near = cam.f * cam.hc / (cam.H - cam.v0)
    h1, h2 = L["h1"] * A[2], L["h2"] * A[2]
    Gx, Gy = A[0], A[1]                                    # the ground point under the aperture

    def basin(X, Y):
        """how strongly a ground point feeds the funnel (soft disc around the axis)"""
        d2 = ((np.asarray(X) - Gx) ** 2 + ((np.asarray(Y) - Gy) * L["basin_y"]) ** 2) / L["Rs"] ** 2
        near = np.clip((np.asarray(Y) - L["near_cut"][0]) / (L["near_cut"][1] - L["near_cut"][0]), 0, 1)
        return (L["floor"] + (1 - L["floor"]) * np.exp(-d2 ** L["basin_p"])) * near ** 2

    def fogw(Y):
        return np.exp(-(np.asarray(Y) - y_near) / (fogL * L["ray_fog_mult"]))

    # ---- level 0: ground plane, nearest-neighbour texture on the tiled torus, fog with depth
    img = np.zeros((cam.H, cam.W, 3))
    vv, uu = np.mgrid[0:cam.H, 0:cam.W] + 0.5
    g = vv > cam.v0 + 1
    Yg = cam.f * cam.hc / (vv[g] - cam.v0)
    Xg = (uu[g] - cam.u0) * Yg / cam.f
    jj = np.floor((Xg - X0) / cs).astype(np.int64) % N
    ii = np.floor((Yg - Y0) / cs).astype(np.int64) % N
    img[g] = tex[ii, jj] * (L["ground_gain"] * np.exp(-(Yg - y_near) / fogL))[:, None]
    del vv, uu, g, Yg, Xg, jj, ii

    # ---- fibres: cell -> block -> body -> aperture
    tiles = [(tx, ty) for tx in range(L["tiles_x"][0], L["tiles_x"][1] + 1)
             for ty in range(L["tiles_y"][0], L["tiles_y"][1] + 1)]
    occ_c, occ_i, occ_j = np.nonzero(x > L["thr"])
    jit = rng.uniform(-0.35, 0.35, (2, len(occ_i)))        # sub-cell offsets so the two channels' threads part
    P, Bk, Ob, wcol = [], [], [], []
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
        P.append(np.stack([Xc[keep], Yc[keep], 0 * Xc[keep]], -1))
        Bk.append(np.stack([BX, BY], -1))
        Ob.append(np.stack([BX + d_j[bi, bj, k] * cs, BY + d_i[bi, bj, k] * cs], -1))
        # fibre colour: the cell's own two channels, linear mix (bundles add up to white)
        pal = np.where(cc[:, None] == 0, CYAN, ORANGE)
        wcol.append(pal * (x[cc, ci, cj] * fogw(Yc[keep]) * basin(Xc[keep], Yc[keep]))[:, None])
    P, Bk, Ob, wcol = map(np.concatenate, (P, Bk, Ob, wcol))
    nR = len(P)
    if nR > L["max_rays"]:                                 # importance subsample, unbiased reweighting
        pr = wcol.sum(1) / wcol.sum()
        pick = rng.choice(nR, L["max_rays"], replace=False, p=pr)
        rw = 1.0 / (pr[pick] * nR)
        P, Bk, Ob = P[pick], Bk[pick], Ob[pick]
        wcol = wcol[pick] * (rw / rw.mean() * nR / L["max_rays"])[:, None]
    nP = len(P)
    # spine of every fibre: ground cell, a short vertical lift, its block knot (x2), its body knot (x2), aperture (x2)
    # (uniform clamped cubic B-spline; a block's fibres share span 2 exactly, a body's share span 4)
    deg, nC = 3, 8
    knots = np.concatenate([np.zeros(deg), np.linspace(0, 1, nC - deg + 1), np.ones(deg)])

    def basis(t):
        return np.stack([BSpline(knots, np.eye(nC)[c], deg)(t) for c in range(nC)], -1)

    def spine(Pg, Bxy, Oxy):
        n = len(Pg)
        B1 = np.concatenate([Bxy + (A[:2] - Bxy) * L["s1"], np.full((n, 1), h1)], 1)
        B2 = np.concatenate([Oxy + (A[:2] - Oxy) * L["s2"], np.full((n, 1), h2)], 1)
        lift = Pg + np.array([0, 0, L["lift"] * h1])
        Ab = np.broadcast_to(A, Pg.shape)
        return np.stack([Pg, lift, B1, B1, B2, B2, Ab, Ab], 1)

    ctrl = spine(P, Bk, Ob)
    S = L["samples"]
    ts = np.linspace(0, 1, S) ** 0.8
    Bm = basis(ts)
    ramp = (np.clip(ts / L["ramp_in"], 0, 1) ** 1.2)[None, :]
    acc = Acc(cam.H, cam.W)
    for a in range(0, nP, 2000):
        cur = np.einsum("sk,rkd->rsd", Bm, ctrl[a:a + 2000])
        acc.curve(cam.proj(cur), wcol[a:a + 2000] * L["ray_gain"], ramp)
    light = acc.render()
    t1 = time.time()

    # ---- level-1 glyphs at the knots: coarse blocks as small squares, bodies as rings + orientation tick
    mk = Acc(cam.H, cam.W)
    th = np.linspace(0, 2 * np.pi, 240)
    bk_t, bd_t = basis(np.array([knots[deg + 2]]))[0], basis(np.array([knots[deg + 4]]))[0]
    nb = nq = 0
    for tx, ty in tiles:
        for bi in range(G):
            for bj in range(G):
                if mb[bi, bj] < L["thr_block"]:
                    continue
                BX = X0 + (cb_j[bi, bj] + N * tx) * cs
                BY = Y0 + (cb_i[bi, bj] + N * ty) * cs
                if not (L["src_y"][0] < BY < L["mark_ymax"]) or basin(BX, BY) < L["mark_basin"]:
                    continue
                k = owner[bi, bj]
                c = spine(np.array([[BX, BY, 0.0]]), np.array([[BX, BY]]),
                          np.array([[BX + d_j[bi, bj, k] * cs, BY + d_i[bi, bj, k] * cs]]))[0]
                q3 = bk_t @ c
                uvq = cam.proj(q3)
                hs = L["sq"] * BS * cs * (1 - L["s1"]) * cam.f / q3[1] / 2
                sq = uvq + hs * np.array([[-1, -1], [1, -1], [1, 1], [-1, 1], [-1, -1]])
                pts = np.concatenate([np.linspace(sq[i], sq[i + 1], 80) for i in range(4)])
                mean = x[:, bi * BS:(bi + 1) * BS, bj * BS:(bj + 1) * BS].mean((1, 2))
                col = (mean[0] * CYAN + mean[1] * ORANGE) / max(mean.sum(), 1e-9)
                wb = fogw(BY) * basin(BX, BY) * min(1.0, mb[bi, bj] / L["mb_ref"])
                mk.curve(pts, (0.5 * col + 0.5 * WARM) * L["block_gain"] * wb)
                if L["block_fill"] > 0:                    # a coarse pixel: filled with the block mean colour
                    gg = np.linspace(-hs, hs, max(2, int(2 * hs)))
                    fx, fy_ = np.meshgrid(gg, gg)
                    mk.point(np.stack([uvq[0] + fx.ravel(), uvq[1] + fy_.ravel()], -1),
                             np.broadcast_to(col * L["block_fill"] * wb, (fx.size, 3)))
                nq += 1
    for tx, ty in tiles:
        for o in objs:
            OX = X0 + (o["cx"] + N * tx) * cs
            OY = Y0 + (o["cy"] + N * ty) * cs
            if not (L["src_y"][0] < OY < L["mark_ymax"]) or basin(OX, OY) < L["mark_basin"]:
                continue
            c = spine(np.array([[OX, OY, 0.0]]), np.array([[OX, OY]]), np.array([[OX, OY]]))[0]
            q3 = bd_t @ c
            uvc = cam.proj(q3)
            if not (-50 < uvc[0] < cam.W + 50):
                continue
            r = L["ring_scale"] * cs * np.sqrt(o["mass"]) * (1 - L["s2"]) * cam.f / q3[1]
            col = WARM * L["ring_gain"] * fogw(OY) * basin(OX, OY)
            mk.curve(uvc + r * np.stack([np.cos(th), np.sin(th)], -1), col)
            Lt = r * (0.35 + 1.3 * o["e"])
            d = np.array([np.cos(o["theta"]), np.sin(o["theta"])]) * Lt
            mk.curve(uvc + np.linspace(-1, 1, 60)[:, None] * d, col * 0.8)
            nb += 1

    # ---- aperture: small horizontal ring + bright point
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

    # ---- the agent's act: one thin line from above, down to the field, landing blind
    ag_uv = np.array(L["agent_uv"], float) * SS + np.array([0, L["agent_r"] * SS])
    tgt3 = np.array([L["act_ground"][0], L["act_ground"][1], 0.0])
    tuv = cam.proj(tgt3)
    nl = 4000
    lr = np.linspace(0, 1, nl)
    mk.curve(np.linspace(ag_uv, tuv, nl), WARM * L["act_gain"], ramp=(0.55 + 0.45 * lr)[None])
    for rr, gg in L["ripples"]:
        rip = tgt3 + rr * np.stack([np.cos(th), np.sin(th), 0 * th], -1)
        mk.curve(cam.proj(rip), WARM * L["act_gain"] * gg)
    marks = mk.render()

    # ---- compose: tone map, glow (at final res), screen blend over the ground
    li = (light + marks).reshape(H, SS, W, SS, 3).mean((1, 3)) * SS     # line integral per final px
    img = img.reshape(H, SS, W, SS, 3).mean((1, 3))
    glow = gaussian_filter(li, (L["g1"], L["g1"], 0)) * L["g1w"] + gaussian_filter(li, (L["g2"], L["g2"], 0)) * L["g2w"]
    def tone(b, k):                                       # hue-preserving: compress the max channel, keep chroma
        mx = b.max(-1, keepdims=True)
        out = b * (1 - np.exp(-k * mx)) / np.maximum(mx, 1e-9)
        hot = 1 - np.exp(-L["white_k"] * np.maximum(mx - L["white_thr"], 0))   # very dense bundles burn white
        return out + (1 - out) * hot
    core = tone(li, L["k_core"])
    halo = tone(glow, L["k_glow"])
    comp = 1 - (1 - img) * (1 - core) * (1 - halo)
    yy, xx = np.mgrid[0:H, 0:W] + 0.5
    r2 = (xx - auv[0] / SS) ** 2 + (yy - auv[1] / SS) ** 2
    for sig, amp in L["halo"]:                             # light through a pinhole
        comp = comp + (amp * np.exp(-r2 / (2 * sig ** 2)))[..., None] * WARM
    vy = (np.arange(H) + 0.5)[:, None]
    haze = np.exp(-((vy - L["v0"]) / (L["haze_w"] * H)) ** 2) * L["haze"]
    comp = comp + haze[..., None] * np.array([0.07, 0.16, 0.22])
    vig = 1 - L["vig"] * (((xx - W / 2) / (W / 2)) ** 2 * 0.6 + ((yy - H / 2) / (H / 2)) ** 2 * 0.4)
    comp = np.clip(comp * vig[..., None] + rng.normal(0, 0.007, comp.shape), 0, 1)
    t2 = time.time()

    # ---- typography and the observation column
    fig = plt.figure(figsize=(W / 100, H / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.imshow(comp, interpolation="nearest", extent=(0, W, H, 0))
    ax.set_xlim(0, W)
    ax.set_ylim(H, 0)
    ax.axis("off")
    column(ax, L, obs, z, auv / SS)
    ax.add_patch(plt.Circle(L["agent_uv"], L["agent_r"], fill=False, ec=WARM, lw=1.0, alpha=0.8))
    ax.add_patch(plt.Circle(L["agent_uv"], L["agent_r"] * 0.3, fc=WARM, ec="none", alpha=0.85))
    title(ax, L)
    fig.savefig(out, dpi=100, facecolor="black")
    plt.close(fig)
    print(f"{out}: fibres {nP} of {nR}, blocks {nq}, bodies {nb}, aperture {auv / SS}, landing {tuv / SS}; "
          f"fibres {t1 - t0:.1f}s, compose {t2 - t1:.1f}s, total {time.time() - t0:.1f}s")


def column(ax, L, obs, z, auv):
    """The agent's whole view: o(t) as received (hidden permuted order, quantised to 0.001)."""
    fp = FontProperties(fname=F_MONO, size=L["num_size"])
    u, v = auv[0], auv[1] - L["col_gap"]
    n = L["col_n"]
    base = np.array([0.86, 0.88, 0.9])
    for r in range(n):
        q = (L["col_start"] + r) % len(obs)
        zz = np.clip(z[q] / 2.5, -1, 1)
        col = base + (CYAN - base) * max(-zz, 0) * 0.8 + (ORANGE + 0.2 - base) * max(zz, 0) * 0.8
        fade = (1 - r / n) ** L["col_fade"] * L["num_alpha"]
        ax.text(u + L["num_dx"], v - r * L["row_h"], f"{obs[q]:.3f}", fontproperties=fp,
                color=np.clip(col, 0, 1), alpha=fade, ha="right", va="center")


def spaced(ax, x, y, s, fp, color, track, **kw):
    r = ax.figure.canvas.get_renderer()
    for ch in s:
        t = ax.text(x, y, ch, fontproperties=fp, color=color, **kw)
        x += t.get_window_extent(renderer=r).width + track
    return x


def title(ax, L):
    fpt = FontProperties(fname=F_TITLE, size=L["title_size"])
    fpv = FontProperties(fname=F_TITLE2, size=L["title_size"])
    tx, ty = L["title_xy"]
    t1 = ax.text(tx, ty, "PhySim", fontproperties=fpt, color=(0.94, 0.95, 0.96), ha="left", va="baseline")
    w = t1.get_window_extent(renderer=ax.figure.canvas.get_renderer()).width
    ax.text(tx + w + L["title_size"] * 0.30, ty, "v2", fontproperties=fpv, color=tuple(CYAN * 0.92 + 0.06),
            ha="left", va="baseline")
    fps = FontProperties(fname=F_MONO_SUB, size=L["sub_size"])
    spaced(ax, tx + L["sub_dx"], ty + L["sub_dy"], "supervenience", fps, L["sub_col"], L["sub_track"],
           ha="left", va="baseline")


LAND = dict(
    W=1920, H=1080, f=950, u0=960, v0=610, cs=4.0 / 128, X0=-1.3, Y0=0.1,
    A_uv=(1250, 300), A_depth=8.0, fogL=5.0, ground_gain=1.0,
    tiles_x=(-4, 4), tiles_y=(0, 6), src_y=(1.4, 22), thr=0.04, max_rays=14000, ray_fog_mult=1.3,
    Rs=3.2, basin_y=1.0, basin_p=2.0, floor=0.010, near_cut=(2.6, 4.4),
    s1=0.10, s2=0.40, h1=0.42, h2=0.66, lift=0.25, samples=1100, ramp_in=0.02,
    ray_gain=0.070, ring_scale=0.55, ring_gain=0.6, block_gain=0.16, block_fill=0.09, mb_ref=40.0, sq=0.36, thr_block=4.0,
    mark_basin=0.30, mark_ymax=16,
    ap_r=0.10, ap_gain=0.35, ap_point=14.0, beam_gain=0.30, beam_floor=0.25, halo=((22, 0.10), (90, 0.06), (320, 0.035)), flare_w=260, flare_gain=0.05,
    agent_uv=(1250, 62), agent_r=6.0, act_ground=(1.75, 2.35), act_gain=0.40,
    ripples=((0.03, 1.0), (0.065, 0.6), (0.11, 0.3)),
    g1=2.0, g1w=1.0, g2=16, g2w=1.3, k_core=1.0, k_glow=0.9, white_k=0.8, white_thr=1.0, haze=0.20, haze_w=0.06, vig=0.35,
    num_size=9.5, col_gap=36, col_n=14, col_start=0, row_h=14, num_dx=-14, num_alpha=0.95, col_fade=0.8,
    title_size=112, title_xy=(126, 300), sub_size=33, sub_dx=6, sub_dy=78, sub_track=9, sub_col=(0.84, 0.88, 0.91),
)

PORT = dict(LAND)
PORT.update(
    W=1080, H=1350, f=760, u0=540, v0=860, X0=-1.0, Y0=0.3, A_uv=(610, 615), A_depth=8.0,
    agent_uv=(610, 350), act_ground=(0.95, 2.05), Rs=3.0, tiles_x=(-3, 3),
    title_xy=(84, 214), title_size=100, sub_size=30, sub_dy=70, sub_track=8,
    flare_w=200, halo=((22, 0.10), (80, 0.06), (260, 0.035)), col_n=14, ray_gain=0.095, ring_gain=0.6,
)

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "both"
    tick = int(sys.argv[2]) if len(sys.argv) > 2 else 120
    if which in ("land", "both"):
        render(LAND, tick, os.path.join(HERE, "cover.png"))
    if which in ("portrait", "both"):
        render(PORT, tick, os.path.join(HERE, "cover_portrait.png"))
