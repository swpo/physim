"""feats -- level-1 input features of the declared future wind commands (for input-aware predictors).

All features are computable from level 1 at time t and the public channel (wind.py's embedding E):
  ucum      sum_{k<h} u(t+k)                                       (128: 2 components x 8 x 8 blocks)
  dblk      4 * Ebar(ucum): block-averaged displacement (px)        (128)
  adv       coarse only: central-difference advection of the block means of both channels and of m2
            by dblk: -[d_x(q D_x) + d_y(q D_y)] / (2 * 16 px)         (192, aligned with Phi_coarse)
  slot      objects only: per slot, the wind displacement (dy, dx) = 4 * sum_k E(u(t+k)) at the slot's
            kinematically extrapolated centroid c + v k, times 'present', and the change of the 4
            embedded position coordinates it causes around the kinematic position c + h v   (6 x 12 = 72)
kin_wind(Y0, h, disp): integrate/analyze.kinematic with the wind displacement added to every present slot.
"""
from __future__ import annotations

import numpy as np

import wr

WD = wr.WD
G, H, W, NC, NO, NF, K = WD.G, WD.H, WD.W, WD.NC, WD.NO, WD.NF, WD.K_SLOTS
BPX = H // G
EAMP = H / (2 * np.pi)


def _profiles():
    gh = WD.gauss_hat()
    up = np.zeros((H, W))
    up[:BPX, :BPX] = 1.0
    g = np.fft.irfft2(np.fft.rfft2(up) * gh, s=(H, W))            # field of block (0, 0), unit coefficient
    Mb = np.zeros((G * G, G * G))                                  # block averages of each basis field
    for bi in range(G):
        for bj in range(G):
            gb = np.roll(np.roll(g, bi * BPX, 0), bj * BPX, 1)
            Mb[:, bi * G + bj] = gb.reshape(G, BPX, G, BPX).mean((1, 3)).reshape(-1)
    return g, Mb


GPROF, EBAR = _profiles()
_BI = np.repeat(np.arange(G), G) * BPX
_BJ = np.tile(np.arange(G), G) * BPX


def point_weights(py, px):
    """(...,) pixel coords -> (..., 64) weights: field component c at the point = w @ a_c."""
    iy = np.rint(py).astype(int)[..., None]
    ix = np.rint(px).astype(int)[..., None]
    return GPROF[(iy - _BI) % H, (ix - _BJ) % W]


def ucum_all(U, ts, hs):
    """U (T, 128) commands; -> (len(hs), len(ts), 128) cumulative command over [t, t+h)."""
    cs = np.concatenate([np.zeros((1, U.shape[1])), np.cumsum(U, 0)])
    return np.stack([cs[ts + h] - cs[ts] for h in hs])


def dblk_of(uc):
    """(..., 128) -> (..., 2, 64) block-averaged displacement in px (component y, x)."""
    a = uc.reshape(uc.shape[:-1] + (2, G * G))
    return 4.0 * a @ EBAR.T


def adv_coarse(Y0, D):
    """Y0 (n, 192) raw coarse rows; D (n, 2, 64) px -> (n, 192) advection change of each coordinate."""
    q = Y0[:, :NC].reshape(len(Y0), 3, G, G)
    Dy = D[:, 0].reshape(-1, 1, G, G)
    Dx = D[:, 1].reshape(-1, 1, G, G)
    fx, fy = q * Dx, q * Dy
    div = (np.roll(fx, -1, 3) - np.roll(fx, 1, 3) + np.roll(fy, -1, 2) - np.roll(fy, 1, 2)) / (2.0 * BPX)
    return -div.reshape(len(Y0), NC)


def slot_geom(Yo):
    """Yo (n, 144) raw objects rows -> present (n, K), cy, cx (px), vy, vx."""
    S = Yo.reshape(len(Yo), K, NF)
    pres = S[:, :, 0] > 0.5
    cx = (np.arctan2(S[:, :, 4], S[:, :, 3]) * W / (2 * np.pi)) % W
    cy = (np.arctan2(S[:, :, 6], S[:, :, 5]) * H / (2 * np.pi)) % H
    return pres, cy, cx, S[:, :, 11], S[:, :, 10]


def slot_disp(Yo_rows, U, ts, hs):
    """Wind displacement of every slot over [t, t+h): -> (len(hs), len(ts), K, 2) (dy, dx) px."""
    pres, cy, cx, vy, vx = slot_geom(Yo_rows)               # rows are Y[ts]
    kmax = max(hs)
    out = np.zeros((len(hs), len(ts), K, 2))
    acc = np.zeros((len(ts), K, 2))
    hset = {h: i for i, h in enumerate(hs)}
    for k in range(kmax):
        u = U[ts + k]                                       # (n, 128)
        if np.any(u):
            w = point_weights(cy + vy * k, cx + vx * k)       # (n, K, 64)
            a = u.reshape(len(ts), 2, G * G)
            acc = acc + 4.0 * np.einsum("nkb,ncb->nkc", w, a)
        if (k + 1) in hset:
            out[hset[k + 1]] = acc * pres[..., None]
    return out


def slot_feats(Yo_rows, disp, h):
    """-> (n, 72): per slot dy, dx and the change of (x_cos, x_sin, y_cos, y_sin) from the wind displacement
    around the kinematic position c + h v."""
    pres, cy, cx, vy, vx = slot_geom(Yo_rows)
    ky, kx = cy + h * vy, cx + h * vx
    dy, dx = disp[..., 0], disp[..., 1]
    th_x0, th_x1 = 2 * np.pi * kx / W, 2 * np.pi * (kx + dx) / W
    th_y0, th_y1 = 2 * np.pi * ky / H, 2 * np.pi * (ky + dy) / H
    f = np.stack([dy, dx, EAMP * (np.cos(th_x1) - np.cos(th_x0)), EAMP * (np.sin(th_x1) - np.sin(th_x0)),
                  EAMP * (np.cos(th_y1) - np.cos(th_y0)), EAMP * (np.sin(th_y1) - np.sin(th_y0))], -1)
    return (f * pres[..., None]).reshape(len(Yo_rows), -1)


def kin_wind(Yo_rows, h, disp):
    """analyze.kinematic(Y0, h, K) plus the wind displacement disp (n, K, 2) on present slots (raw rows)."""
    out = Yo_rows.copy()
    S = out.reshape(len(Yo_rows), K, NF)
    cx = np.arctan2(S[:, :, 4], S[:, :, 3]) * W / (2 * np.pi) + h * S[:, :, 10] + disp[..., 1]
    cy = np.arctan2(S[:, :, 6], S[:, :, 5]) * H / (2 * np.pi) + h * S[:, :, 11] + disp[..., 0]
    pres = S[:, :, 0] > 0.5
    S[:, :, 3] = np.where(pres, EAMP * np.cos(2 * np.pi * cx / W), 0)
    S[:, :, 4] = np.where(pres, EAMP * np.sin(2 * np.pi * cx / W), 0)
    S[:, :, 5] = np.where(pres, EAMP * np.cos(2 * np.pi * cy / H), 0)
    S[:, :, 6] = np.where(pres, EAMP * np.sin(2 * np.pi * cy / H), 0)
    return S.reshape(len(Yo_rows), -1)


def input_features(view, Yraw, U, ts, hs):
    """-> dict h -> (len(ts), d_u) raw input features of the window [t, t+h) for one trajectory.
    Yraw: the view's raw level-1 rows (T+1, n); U (T, 128)."""
    uc = ucum_all(U, ts, hs)                                  # (nh, n, 128)
    D = dblk_of(uc)                                          # (nh, n, 2, 64)
    out = {}
    if view == "objects":
        disp = slot_disp(Yraw[ts], U, ts, hs)
    for i, h in enumerate(hs):
        parts = [uc[i], D[i].reshape(len(ts), -1)]
        if view == "coarse":
            parts.append(adv_coarse(Yraw[ts], D[i]))
        else:
            parts.append(slot_feats(Yraw[ts], disp[i], h))
        out[h] = np.concatenate(parts, 1)
    return out, (disp if view == "objects" else None)


# ----------------------------------------------------------------------------- local (equivariant) input features
# Added after the declared dense features overfit (see closure_run.py, '+u2' predictors): a few local
# features per output coordinate, with coefficients shared across blocks (coarse) or slots (objects).
N_LOC = 9


def coarse_local(Y0, D):
    """Y0 (n, 192) raw; D (n, 2, 64) px -> (n, 192, 9): for coordinate (q, b): central advection of q,
    the fluxes q D_x at b-x, b+x, q D_y at b-y, b+y, q D_x and q D_y at b, q |D| at b, |D| at b."""
    n = len(Y0)
    q = Y0[:, :NC].reshape(n, 3, G, G)
    Dy, Dx = D[:, 0].reshape(n, 1, G, G), D[:, 1].reshape(n, 1, G, G)
    fx, fy = q * Dx, q * Dy
    adv = -(np.roll(fx, -1, 3) - np.roll(fx, 1, 3) + np.roll(fy, -1, 2) - np.roll(fy, 1, 2)) / (2.0 * BPX)
    nd = np.sqrt(Dx ** 2 + Dy ** 2)
    F = [adv, np.roll(fx, 1, 3), np.roll(fx, -1, 3), np.roll(fy, 1, 2), np.roll(fy, -1, 2), fx, fy, q * nd,
         np.broadcast_to(nd, q.shape), semi_lagrangian(q, Dy, Dx) - q]
    return np.stack(F, -1).reshape(n, NC, N_LOC + 1)


def semi_lagrangian(q, Dy, Dx):
    """q (n, 3, G, G) block field moved by the block displacement (px): bilinear (periodic) read of q at
    b - D(b) / 16 px per block (a coarse semi-Lagrangian step)."""
    n = q.shape[0]
    ii, jj = np.meshgrid(np.arange(G), np.arange(G), indexing="ij")
    y = ii[None] - Dy[:, 0] / BPX
    x = jj[None] - Dx[:, 0] / BPX
    y0, x0 = np.floor(y).astype(int), np.floor(x).astype(int)
    wy, wx = (y - y0)[:, None], (x - x0)[:, None]
    nn = np.arange(n)[:, None, None]

    def g(a, b):
        return q[nn, :, a % G, b % G].transpose(0, 3, 1, 2)          # (n, 3, G, G)
    return ((1 - wy) * (1 - wx) * g(y0, x0) + (1 - wy) * wx * g(y0, x0 + 1) + wy * (1 - wx) * g(y0 + 1, x0)
            + wy * wx * g(y0 + 1, x0 + 1))


def slot_disp_cum(Yo_rows, U, ts, kmax=16):
    """Cumulative wind displacement of every slot after k = 0..kmax ticks: (kmax + 1, n, K, 2)."""
    pres, cy, cx, vy, vx = slot_geom(Yo_rows)
    out = np.zeros((kmax + 1, len(ts), K, 2))
    for k in range(kmax):
        u = U[ts + k]
        step = 0.0
        if np.any(u):
            w = point_weights(cy + vy * k, cx + vx * k)
            step = 4.0 * np.einsum("nkb,ncb->nkc", w, u.reshape(len(ts), 2, G * G))
        out[k + 1] = out[k] + step
    return out * pres[None, ..., None]


def objects_local(Yo_rows, cum, h):
    """-> (n, 144, 9): for coordinate (s, f) the features of slot s: dy, dx, the change of the 4 position
    coordinates around c + h v, |d|, and the last tick's displacement (dy, dx)."""
    n = len(Yo_rows)
    disp, last = cum[h], cum[h] - cum[h - 1]
    sf = slot_feats(Yo_rows, disp, h).reshape(n, K, 6)
    nd = np.linalg.norm(disp, axis=-1)[..., None]
    F = np.concatenate([sf, nd, last], -1)                    # (n, K, 9)
    return np.repeat(F[:, :, None, :], NF, 2).reshape(n, K * NF, N_LOC)
