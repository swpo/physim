"""cnets -- encoders, heads and objectives of the study `bias2` (JAX, float32; see c5.py). round4/bias/bnets.py
generalised from 2 to c5.NCH level-0 fields; the pib objective is dropped (reduced grid).

Inputs are standardised level-0 fields xs (N, 4, 128, 128) (per-field mean / sd of the fitting half).
Encoders return z (N, 8, 8, c). Whitening as learned_phi2/lphi.whiten (relative ridge eps): per block-channel
(c x c, equivariant) for the local encoders and for Uc, over all 64 c numbers for U.
"""
from __future__ import annotations

import math

import jax
import jax.numpy as jnp

import c5

F32 = jnp.float32
G, BS, NCH = c5.G, c5.BS, c5.NCH
HID_PIX, FEAT_PIX, HID_WIN, HID_MLP = 8, 4, 16, 16       # N encoder widths (as round 4)
U_HID = 64                                                # U residual width (as round 4)


def gelu(x):
    return jax.nn.gelu(x)


def normal(key, shape, fan_in, gain=1.0):
    return (jax.random.normal(key, shape, F32) * (gain / math.sqrt(fan_in))).astype(F32)


def win(h):
    return BS + 2 * h


def win_apply(x, w, h):
    """x (N, C, 128, 128), w (O, C, 16 + 2h, 16 + 2h) -> (N, O, 8, 8): each block's window = the block plus an
    h-px periodic halo (stride 16), written as matrix products over the 3 x 3 block neighbourhood (no convolution
    kernels, so jax.vmap over replicas gives batched GEMMs instead of grouped convolutions). The window is embedded
    in a 48 x 48 frame (zeros outside), split into 3 x 3 sub-blocks of 16 x 16; sub-block (a, b) reads block
    (i + a - 1, j + b - 1), periodic."""
    N, C = x.shape[:2]
    O = w.shape[0]
    xb = x.reshape(N, C, G, BS, G, BS).transpose(0, 2, 4, 1, 3, 5)                   # (N, 8, 8, C, 16, 16)
    if h == 0:
        return jnp.einsum("nijcyx,ocyx->noij", xb, w)
    w48 = jnp.pad(w, ((0, 0), (0, 0), (BS - h, BS - h), (BS - h, BS - h))).reshape(O, C, 3, BS, 3, BS)
    out = 0.0
    for a in range(3):
        for b in range(3):
            xs = jnp.roll(xb, (1 - a, 1 - b), (1, 2))                                  # xs[i, j] = xb[i + a - 1, j + b - 1]
            out = out + jnp.einsum("nijcyx,ocyx->noij", xs, w48[:, :, a, :, b, :])
    return out


def blocks(xs):
    """(N, C, 128, 128) -> (N, 8, 8, C * 256): each block's content, inner order [channel, dy, dx]."""
    N, C = xs.shape[:2]
    return xs.reshape(N, C, G, BS, G, BS).transpose(0, 2, 4, 1, 3, 5).reshape(N, G, G, C * BS * BS)


def nbhd(z):
    """(N, 8, 8, k) -> (N, 8, 8, 9k): the 3 x 3 periodic neighbourhood."""
    return jnp.concatenate([jnp.roll(z, (-dy, -dx), (1, 2)) for dy in (-1, 0, 1) for dx in (-1, 0, 1)], -1)


def mlp_init(key, dims, zero_last=False):
    P = []
    ks = jax.random.split(key, len(dims) - 1)
    for i, (a, b) in enumerate(zip(dims[:-1], dims[1:])):
        last = i == len(dims) - 2
        W = jnp.zeros((a, b), F32) if (last and zero_last) else normal(ks[i], (a, b), a, 1.0 if last else math.sqrt(2.0))
        P.append({"W": W, "b": jnp.zeros((b,), F32)})
    return P


def mlp_apply(P, x):
    for i, L in enumerate(P):
        x = x @ L["W"] + L["b"]
        if i < len(P) - 1:
            x = gelu(x)
    return x


# ----------------------------------------------------------------------------- encoders
def base_enc(enc):
    """'Uc' is the U encoder (it differs in the whitening only)."""
    return "U" if enc == "Uc" else enc


def glob_white(enc):
    return enc == "U"


def init_enc(enc, h, c, key):
    enc = base_enc(enc)
    k = jax.random.split(key, 6)
    if enc == "L":
        w = win(h)
        return {"W": normal(k[0], (c, NCH, w, w), NCH * w * w), "b": jnp.zeros((c,), F32)}
    if enc == "N":
        w = win(h)
        return {"W": normal(k[0], (c, NCH, w, w), NCH * w * w), "b": jnp.zeros((c,), F32),
                "pix": mlp_init(k[1], [NCH, HID_PIX, FEAT_PIX]),
                "Wh": normal(k[2], (HID_WIN, FEAT_PIX, w, w), FEAT_PIX * w * w, math.sqrt(2.0)),
                "bh": jnp.zeros((HID_WIN,), F32),
                "head": mlp_init(k[3], [HID_WIN, HID_MLP, c], zero_last=True)}
    if enc == "U":
        n = NCH * c5.NPIX * c5.NPIX
        return {"W": normal(k[0], (n, G * G * c), n), "b": jnp.zeros((G * G * c,), F32),
                "Wa": normal(k[1], (n, U_HID), n, math.sqrt(2.0)), "ba": jnp.zeros((U_HID,), F32),
                "head": mlp_init(k[2], [U_HID, G * G * c], zero_last=True)}
    raise ValueError(enc)


def enc_parts(enc, h, P, xs):
    """xs (N, 4, 128, 128) standardised -> (linear part (N, 8, 8, c) incl. bias, nonlinear part or None)."""
    enc = base_enc(enc)
    N = xs.shape[0]
    if enc in ("L", "N"):
        z = win_apply(xs, P["W"], h) + P["b"][None, :, None, None]                   # (N, c, 8, 8)
        z = z.transpose(0, 2, 3, 1)
        if enc == "L":
            return z, None
        f = jnp.moveaxis(mlp_apply(P["pix"], jnp.moveaxis(xs, 1, -1)), -1, 1)           # (N, 4, 128, 128)
        a = gelu(win_apply(f, P["Wh"], h) + P["bh"][None, :, None, None]).transpose(0, 2, 3, 1)
        return z, mlp_apply(P["head"], a)
    x = xs.reshape(N, -1)
    c = P["b"].shape[0] // (G * G)
    lin = (x @ P["W"] + P["b"]).reshape(N, c, G, G).transpose(0, 2, 3, 1)             # channel-major grid
    nl = mlp_apply(P["head"], gelu(x @ P["Wa"] + P["ba"])).reshape(N, c, G, G).transpose(0, 2, 3, 1)
    return lin, nl


def enc_apply(enc, h, P, xs):
    """xs (N, 4, 128, 128) standardised -> z (N, 8, 8, c)."""
    lin, nl = enc_parts(enc, h, P, xs)
    return lin if nl is None else lin + nl


def field_parts(enc, h, P, xs):
    """Local encoders only: the linear window's contribution of each level-0 field, (N, 8, 8, c, 4) (no bias)."""
    out = [win_apply(xs[:, f:f + 1], P["W"][:, f:f + 1], h).transpose(0, 2, 3, 1) for f in range(NCH)]
    return jnp.stack(out, -1)


def whiten(z, glob, eps=1e-5):
    """lphi.whiten: batch whitening per block-channel (c x c) or over all 64 c numbers (glob)."""
    M = z.shape[0]
    Zf = z.reshape(M, -1) if glob else z.reshape(-1, z.shape[-1])
    mu = Zf.mean(0)
    D = Zf - mu
    Cv = D.T @ D / D.shape[0]
    Cv = Cv + eps * (jnp.trace(Cv) / D.shape[1] + 1e-30) * jnp.eye(D.shape[1], dtype=F32)
    L = jnp.linalg.cholesky(Cv)
    Zw = jax.scipy.linalg.solve_triangular(L, D.T, lower=True).T
    return Zw.reshape(z.shape)


# ----------------------------------------------------------------------------- objectives
def frames_needed(obj):
    """Frame offsets the loss reads (relative to t)."""
    if obj == "recon":
        return (0,)
    return (-1, 0) + tuple(c5.HTR)


def init_model(enc, h, obj, c, key):
    k = jax.random.split(key, 4)
    P = {"enc": init_enc(enc, h, c, k[0])}
    nb = NCH * BS * BS
    nh = len(c5.HTR)
    if obj == "recon":
        P["dec"] = mlp_init(k[1], [c, nb]) if enc == "L" else {"lin": mlp_init(k[1], [c, nb]),
                                                                 "mlp": mlp_init(k[2], [c, 128, nb], zero_last=True)}
    elif obj == "clos":
        P["A"] = jnp.zeros((nh, 2 * G * G * c, G * G * c), F32)
    elif obj == "local":
        P["A"] = jnp.zeros((18 * c, nh * c), F32)
        P["head"] = mlp_init(k[1], [18 * c, 64, 64, nh * c], zero_last=True)
    else:
        raise ValueError(obj)
    return P


def make_loss(enc, h, obj, c):
    """loss(P, enc_frames (F, N, 4, 128, 128)) -> scalar."""
    glob = glob_white(enc)
    nh = len(c5.HTR)

    def loss(P, xe):
        F, N = xe.shape[:2]
        z = enc_apply(enc, h, P["enc"], xe.reshape((F * N,) + xe.shape[2:]))           # (F N, 8, 8, c)
        if obj == "recon":
            Xb = blocks(xe[0])
            if enc == "L":
                rec = mlp_apply(P["dec"], z)
            else:
                rec = mlp_apply(P["dec"]["lin"], z) + mlp_apply(P["dec"]["mlp"], z)
            return jnp.mean((rec - Xb) ** 2)
        zw = whiten(z, glob).reshape((F, N) + z.shape[1:])
        zm, z0 = zw[0], zw[1]
        if obj == "clos":
            x = jnp.concatenate([z0.reshape(N, -1), zm.reshape(N, -1)], 1)
            errs = [jnp.mean((z0.reshape(N, -1) + x @ P["A"][i] - zw[2 + i].reshape(N, -1)) ** 2) for i in range(nh)]
            return sum(errs) / len(errs)
        if obj == "local":
            x = jnp.concatenate([nbhd(z0), nbhd(zm)], -1)
            d = (x @ P["A"] + mlp_apply(P["head"], x)).reshape(N, G, G, nh, c)
            errs = [jnp.mean((z0 + d[..., i, :] - zw[2 + i]) ** 2) for i in range(nh)]
            return sum(errs) / len(errs)
        raise ValueError(obj)
    return loss
