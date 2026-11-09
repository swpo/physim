"""chand -- hand designs of the study `bias2` (see c5.py): pixel features of each world, block / tent windows,
and closed-form block-feature designs (slow-feature analysis, PCA).

Pixel features (raw units, x = (N, 4, 128, 128) in c5.FIELDS order):
  vortex    om, absom = |om|, ens = om^2, Y, a, b, lab = a + b, dab = b - a, kb = |om| b / (a + b + 1e-3),
            ka = |om| - kb  (ka, kb: the 2-channel field the vortex tracker runs on)
  membrane  phi, S, K, L, wall = 4 phi (1 - phi), phiK = phi clip(K, 0, 1), phi1k = phi - phiK (the 2-channel
            field the cell tracker runs on), area = 1[phi > 0.5]
  gliders   c0, c1, mass = c0 + c1, dc = c0 - c1, msq = (c0 + c1)^2
Windows: weighted means over a block plus an h-px periodic halo; weight 1 on the block, 1/2 on the halo
(h = 0: the block mean; h = 8: round 4's tent). Closed forms, fitted on one half's block means (per-feature
standardisation) and applied to the other half:
  sfa   generalised eigenvectors of the symmetrised lagged covariance (mean over lags 1, 4, 16 ticks) against the
        covariance of the per-block feature vector, pooled over blocks: the slowest linear combinations of block
        means (solved in the PCA-whitened basis; directions below 1e-6 of the largest variance are dropped).
        `sfa` uses the raw fields (what a linear block-mean encoder can reach), `sfax` the nonlinear feature set
        c5.SFAX.
  pca   first principal component of the standardised block means of the raw fields.
"""
from __future__ import annotations

import numpy as np

import c5

BS, G = c5.BS, c5.G


def pixel_features(world):
    """-> f(x (N, 4, 128, 128) jnp float32) -> {name: (N, 128, 128)}."""
    import jax.numpy as jnp
    if world == "vortex":
        def f(x):
            om, Y, a, b = x[:, 0], x[:, 1], x[:, 2], x[:, 3]
            w = jnp.abs(om)
            kb = w * b / (a + b + 1e-3)
            return {"om": om, "absom": w, "ens": om * om, "Y": Y, "a": a, "b": b, "lab": a + b, "dab": b - a,
                    "kb": kb, "ka": w - kb}
    elif world == "gliders":
        def f(x):
            c0, c1 = x[:, 0], x[:, 1]
            return {"c0": c0, "c1": c1, "mass": c0 + c1, "dc": c0 - c1, "msq": (c0 + c1) ** 2}
    else:
        def f(x):
            phi, S, K, L = x[:, 0], x[:, 1], x[:, 2], x[:, 3]
            pk = phi * jnp.clip(K, 0.0, 1.0)
            return {"phi": phi, "S": S, "K": K, "L": L, "wall": 4 * phi * (1 - phi), "phiK": pk, "phi1k": phi - pk,
                    "area": (phi > 0.5).astype(x.dtype)}
    return f


def window(h):
    """(16 + 2h)^2 weights, sum 1: 1 on the block, 1/2 on the h-px halo (outer product of the 1D profile)."""
    p = np.concatenate([np.full(h, 0.5), np.ones(BS), np.full(h, 0.5)])
    w = np.outer(p, p)
    return w / w.sum()


def pool(F, h):
    """F (N, k, 128, 128) -> (N, k, 8, 8): the window mean of every channel (stride 16, periodic)."""
    import jax
    import jax.numpy as jnp
    N, k = F.shape[:2]
    if h == 0:
        return F.reshape(N, k, G, BS, G, BS).mean((3, 5))
    w = jnp.asarray(window(h), F.dtype)[None, None]
    x = jnp.pad(F, ((0, 0), (0, 0), (h, h), (h, h)), mode="wrap").reshape(N * k, 1, c5.NPIX + 2 * h, c5.NPIX + 2 * h)
    y = jax.lax.conv_general_dilated(x, w, (BS, BS), "VALID", dimension_numbers=("NCHW", "OIHW", "NCHW"))
    return y.reshape(N, k, G, G)


def feature_list(world):
    """Pixel features in the order the pooled tensor stores them (h = 0 block): BASE1 then the extra ones."""
    extra = [n for v in c5.MULTI.values() for n in v if n not in c5.BASE1]
    return list(c5.BASE1) + sorted(set(extra))


# ----------------------------------------------------------------------------- closed forms (numpy)
def _vecs(F, idx, mu, sd):
    """F (J, T, nf, 64) -> standardised per-block vectors (J, T, 64, k) of the features idx."""
    return np.moveaxis((F[:, :, idx] - mu[idx][None, None, :, None]) / sd[idx][None, None, :, None], 2, 3)


def fit_closed(F, names):
    """F (J, T, nf, 64) block means (h = 0) of feature_list on the FIT half. -> dict of projection specs."""
    nf = F.shape[2]
    mu = F.mean((0, 1, 3))
    sd = np.maximum(F.std((0, 1, 3)), 1e-12)
    out = {"mu": mu, "sd": sd, "features": list(names)}
    for tag, feats in (("sfa", list(c5.FIELDS)), ("sfax", list(c5.SFAX))):
        idx = np.array([names.index(f) for f in feats])
        V = _vecs(F, idx, mu, sd)                                   # (J, T, 64, k)
        k = len(idx)
        C0 = np.cov(V.reshape(-1, k).T)
        Ct = np.zeros((k, k))
        lam_lag = {}
        for lag in c5.HTR:
            a, b = V[:, :-lag].reshape(-1, k), V[:, lag:].reshape(-1, k)
            m = V.reshape(-1, k).mean(0)
            Cl = (a - m).T @ (b - m) / len(a)
            Cl = 0.5 * (Cl + Cl.T)
            Ct += Cl / len(c5.HTR)
            lam_lag[lag] = Cl
        e0, E0 = np.linalg.eigh(C0)
        keep = e0 > 1e-6 * e0.max()
        Wh = E0[:, keep] / np.sqrt(e0[keep])                        # whitening of the kept directions
        w, Q = np.linalg.eigh(Wh.T @ Ct @ Wh)
        o = np.argsort(w)[::-1]
        w, U = w[o], (Wh @ Q)[:, o]
        U = U * np.sign(U[np.argmax(np.abs(U), 0), np.arange(U.shape[1])])   # sign: largest weight positive
        k = U.shape[1]
        out[tag] = {"features": feats, "idx": idx, "U": U, "eig_mean_autocorr": w,
                    "autocorr_by_lag": {lag: [float(U[:, i] @ lam_lag[lag] @ U[:, i] / (U[:, i] @ C0 @ U[:, i]))
                                              for i in range(k)] for lag in c5.HTR},
                    "feature_autocorr_by_lag": {lag: (np.diag(lam_lag[lag]) / np.diag(C0)).tolist() for lag in c5.HTR},
                    "corr": (C0 / np.sqrt(np.outer(np.diag(C0), np.diag(C0)))).tolist()}
    idx = np.array([names.index(f) for f in c5.FIELDS])
    V = _vecs(F, idx, mu, sd).reshape(-1, len(idx))
    w, U = np.linalg.eigh(np.cov(V.T))
    o = np.argsort(w)[::-1]
    w, U = w[o], U[:, o]
    U = U * np.sign(U[np.argmax(np.abs(U), 0), np.arange(len(idx))])
    out["pca"] = {"features": list(c5.FIELDS), "idx": idx, "U": U, "eig": w}
    return out


def apply_closed(spec, name, F):
    """F (..., nf, 64) block means of the CERT half -> latent (..., c * 64) channel-major, for a c5.CLOSED name."""
    tag, c = name.rsplit("_c", 1)
    c = int(c)
    s = spec[tag]
    idx = s["idx"]
    lead = F.shape[:-2]
    V = (F[..., idx, :] - spec["mu"][idx][:, None]) / spec["sd"][idx][:, None]     # (..., k, 64)
    Z = np.einsum("...kb,kc->...cb", V, s["U"][:, :c])                             # (..., c, 64)
    return Z.reshape(lead + (c * 64,))
