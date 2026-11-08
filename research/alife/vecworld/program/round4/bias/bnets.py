"""bnets -- encoders, heads and objectives of the round-4 study `bias` (JAX, float32; see b4.py).

Inputs are standardised level-0 fields xs (N, 2, 128, 128) (per-channel mean / sd of the fitting half).
Encoders return z (N, 8, 8, c). Whitening as learned_phi2/lphi.whiten (relative ridge eps, so shrinking the latent
cannot drive a whitened loss to zero): per block-channel (c x c, equivariant) for the local encoders, over all
64 c numbers for U.
"""
from __future__ import annotations

import math

import jax
import jax.numpy as jnp
import numpy as np

import b4

F32 = jnp.float32
G, BS = b4.G, b4.BS
HID_PIX, FEAT_PIX, HID_WIN, HID_MLP = 8, 4, 16, 16       # N encoder widths
U_HID = 64                                                # U residual width
PIB_NOISE = 0.5


def gelu(x):
    return jax.nn.gelu(x)


def normal(key, shape, fan_in, gain=1.0):
    return (jax.random.normal(key, shape, F32) * (gain / math.sqrt(fan_in))).astype(F32)


def win(h):
    return BS + 2 * h


def conv_win(x, w, h):
    """x (N, Cin, 128, 128), w (Cout, Cin, 16 + 2h, 16 + 2h) -> (N, Cout, 8, 8): each block's window = the block
    plus an h-px periodic halo (stride 16)."""
    if h:
        x = jnp.pad(x, ((0, 0), (0, 0), (h, h), (h, h)), mode="wrap")
    return jax.lax.conv_general_dilated(x, w, (BS, BS), "VALID", dimension_numbers=("NCHW", "OIHW", "NCHW"))


def blocks(xs):
    """(N, 2, 128, 128) -> (N, 8, 8, 512): each block's content, inner order [channel, dy, dx]."""
    N = xs.shape[0]
    return xs.reshape(N, 2, G, BS, G, BS).transpose(0, 2, 4, 1, 3, 5).reshape(N, G, G, 2 * BS * BS)


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
def init_enc(enc, h, c, key):
    k = jax.random.split(key, 6)
    if enc == "L":
        w = win(h)
        return {"W": normal(k[0], (c, 2, w, w), 2 * w * w), "b": jnp.zeros((c,), F32)}
    if enc == "N":
        w = win(h)
        return {"W": normal(k[0], (c, 2, w, w), 2 * w * w), "b": jnp.zeros((c,), F32),
                "pix": mlp_init(k[1], [2, HID_PIX, FEAT_PIX]),
                "Wh": normal(k[2], (HID_WIN, FEAT_PIX, w, w), FEAT_PIX * w * w, math.sqrt(2.0)),
                "bh": jnp.zeros((HID_WIN,), F32),
                "head": mlp_init(k[3], [HID_WIN, HID_MLP, c], zero_last=True)}
    if enc == "U":
        n = 2 * b4.NPIX * b4.NPIX
        return {"W": normal(k[0], (n, G * G * c), n), "b": jnp.zeros((G * G * c,), F32),
                "Wa": normal(k[1], (n, U_HID), n, math.sqrt(2.0)), "ba": jnp.zeros((U_HID,), F32),
                "head": mlp_init(k[2], [U_HID, G * G * c], zero_last=True)}
    raise ValueError(enc)


def enc_apply(enc, h, P, xs):
    """xs (N, 2, 128, 128) standardised -> z (N, 8, 8, c)."""
    N = xs.shape[0]
    if enc in ("L", "N"):
        z = conv_win(xs, P["W"], h) + P["b"][None, :, None, None]                    # (N, c, 8, 8)
        z = z.transpose(0, 2, 3, 1)
        if enc == "N":
            f = jnp.moveaxis(mlp_apply(P["pix"], jnp.moveaxis(xs, 1, -1)), -1, 1)       # (N, 4, 128, 128)
            a = gelu(conv_win(f, P["Wh"], h) + P["bh"][None, :, None, None]).transpose(0, 2, 3, 1)
            z = z + mlp_apply(P["head"], a)
        return z
    x = xs.reshape(N, -1)
    z = x @ P["W"] + P["b"] + mlp_apply(P["head"], gelu(x @ P["Wa"] + P["ba"]))
    c = z.shape[-1] // (G * G)
    return z.reshape(N, c, G, G).transpose(0, 2, 3, 1)                                 # channel-major grid


def l2_matrices(enc, P):
    """Encoder matrices for decoupled weight decay (U only)."""
    return {"W", "Wa"} if enc == "U" else set()


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
    """Frame offsets the loss reads (relative to t): encoded frames and raw target frames."""
    if obj == "recon":
        return (0,), ()
    if obj == "pib":
        return (-1, 0), b4.HTR
    hz = {"clos1": (1,), "clos16": (16,)}.get(obj, b4.HTR)
    return (-1, 0) + tuple(hz), ()


def horizons(obj):
    return {"clos1": (1,), "clos16": (16,)}.get(obj, b4.HTR)


def init_model(enc, h, obj, c, key):
    k = jax.random.split(key, 4)
    P = {"enc": init_enc(enc, h, c, k[0])}
    nb = 2 * BS * BS
    if obj == "recon":
        P["dec"] = mlp_init(k[1], [c, nb]) if enc == "L" else {"lin": mlp_init(k[1], [c, nb]),
                                                                 "mlp": mlp_init(k[2], [c, 128, nb], zero_last=True)}
    elif obj in ("clos", "clos1", "clos16"):
        nh = len(horizons(obj))
        P["A"] = jnp.zeros((nh, 2 * G * G * c, G * G * c), F32)
    elif obj == "local":
        nh = len(b4.HTR)
        P["A"] = jnp.zeros((18 * c, nh * c), F32)
        P["head"] = mlp_init(k[1], [18 * c, 64, 64, nh * c], zero_last=True)
    elif obj == "pib":
        nh = len(b4.HTR)
        P["A"] = jnp.zeros((18 * c, nh * nb), F32)
        P["head"] = mlp_init(k[1], [18 * c, 128, 128, nh * nb], zero_last=True)
    else:
        raise ValueError(obj)
    return P


def make_loss(enc, h, obj, c):
    """loss(P, enc_frames (F, N, 2, 128, 128), tgt_frames (K, N, 2, 128, 128), key) -> scalar."""
    glob = enc == "U"

    def loss(P, xe, xt, key):
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
        if obj in ("clos", "clos1", "clos16"):
            x = jnp.concatenate([z0.reshape(N, -1), zm.reshape(N, -1)], 1)
            errs = [jnp.mean((z0.reshape(N, -1) + x @ P["A"][i] - zw[2 + i].reshape(N, -1)) ** 2)
                    for i in range(len(horizons(obj)))]
            return sum(errs) / len(errs)
        if obj == "local":
            x = jnp.concatenate([nbhd(z0), nbhd(zm)], -1)
            d = (x @ P["A"] + mlp_apply(P["head"], x)).reshape(N, G, G, len(b4.HTR), c)
            errs = [jnp.mean((z0 + d[..., i, :] - zw[2 + i]) ** 2) for i in range(len(b4.HTR))]
            return sum(errs) / len(errs)
        if obj == "pib":
            zn = zw + PIB_NOISE * jax.random.normal(key, zw.shape, F32)
            x = jnp.concatenate([nbhd(zn[1]), nbhd(zn[0])], -1)
            pred = (x @ P["A"] + mlp_apply(P["head"], x)).reshape(N, G, G, len(b4.HTR), 2 * BS * BS)
            errs = [jnp.mean((pred[..., i, :] - blocks(xt[i])) ** 2) for i in range(len(b4.HTR))]
            return sum(errs) / len(errs)
        raise ValueError(obj)
    return loss


# ----------------------------------------------------------------------------- designed windows (numpy, bwin)
from bwin import block_window, tent_window  # noqa: E402,F401
