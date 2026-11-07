"""lphi -- learned level-2 coarse-grainings Phi2 of the gliders block view (track 1, E1 on real data).

Data (read only): vw1/fresh/closure/results/sim_{A,B}.npz. Block view = first 192 level-1 numbers,
channel-major (3, 8, 8): block means of channel 0 and channel 1 and the block mean of A_sum^2 on an
8 x 8 grid of 16-px blocks. Y (18, 301, 192) base trajectories per file; B (18, 4, 5, 32, 192)
branch replicates from test ticks (40, 100, 160, 220): B[j, i, r, s] is tick TEST[i] + s + 1 of
replicate r; Y continues as replicate 0 (R = 6).

Cross-fitting by designer seed: every Phi2 that is fitted (learned encoders, PCA, TICA) is fitted
on the level-1 base trajectories of ONE file (half) and certified on the OTHER file's 72 test states;
the two certified halves are pooled (144 test states). Branch replicates are never used in fitting.

Phi2 maps one level-1 frame to a 4 x 4 x c latent (local, equivariant encoders: one 2 x 2 cell of
level-1 blocks = a 32 x 32 px region) or to 16c numbers (unconstrained MLP control, global PCA).
Latents are flattened channel-major (c, 4, 4) so that a grid predictor can reshape them.

Certification (same fixed predictor family for every Phi2, and for level 1 itself):
  closure_lib.closure_ext (the VW-0 estimator: mean, persistence, AR(1), ridge on 1/2/4/8 lags, kNN;
  per-coordinate standardisation; 4 folds by trajectory) with horizons 1, 2, 4, 8, 16, plus hooks:
  'lridge'  local equivariant ridge on the latent grid: each cell's future from its 3 x 3 periodic
            neighbourhood at 2 lags (shared weights) -- the fixed LOCAL predictor;
  'yridge'  ridge of the latent's future on the level-1 past (2 lags) plus the latent past (2 lags):
            the level-1-informed predictor for the Gamma_Y(Z) proxy (Prop. 6 of CATEGORY.md);
  'rmlp'    optional: the fresh residual MLP on 4 lags (1 seed), a global nonlinear member.
Gaussian (log-det) proxies per horizon h, nats, Wishart-corrected (vw.certificates.logdet):
  I_capt = 1/2 [ld S_mean - ld S_best]     predictive information the level-2 past captures
  I_avail = 1/2 [ld S_mean - ld S_orac]    predictive information the level-0 state holds
  gapX   = 1/2 [ld S_best - ld S_orac]     closure gap proxy, Gamma_X(Z) at horizon h
  gammaY = 1/2 [ld S_best - ld S_yridge]   level-1 past beyond level-2 past, Gamma_Y(Z) at h
  inherit = 1/2 [ld S_yridge - ld S_orac]  I(x; z_{t+h} | y_<=t), the part inherited from level 1
"""
import json
import math
import os
import sys
import time

sys.path.insert(0, "/home/user/evalwork/vecworld/vw1/fresh/closure/scripts")
import closure_lib as CL  # noqa: E402  (puts the port and integrate/ on the path, read only)

sys.path.insert(0, "/home/user/evalwork/vecworld/vw1")
import numpy as np  # noqa: E402
import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
from vw.certificates import logdet  # noqa: E402

AN = CL.AN
OUT = "/home/user/evalwork/vecworld/program/track1/learned_phi2"
RES = f"{OUT}/results"
HZ = [1, 2, 4, 8, 16]
TEST = [40, 100, 160, 220]
NJ = 18
FAM_G = ["mean", "persistence", "ar1", "ridge_p1", "ridge_p2", "ridge_p4", "ridge_p8", "knn"]
jax.config.update("jax_enable_x64", False)


def log(*a):
    print(f"[{time.strftime('%H:%M:%S')}]", *a, flush=True)


# ----------------------------------------------------------------------------- data
def load_halves():
    out = {}
    for tag in ("A", "B"):
        d = np.load(f"{CL.RES}/sim_{tag}.npz")
        out[tag] = {"Y": d["Y"][..., :192].astype(np.float64), "B": d["B"][..., :192].astype(np.float64)}
    return out


def other(h):
    return "B" if h == "A" else "A"


def grid(Y):
    return Y.reshape(Y.shape[:-1] + (3, 8, 8))


def patches(G):
    """(..., 3, 8, 8) -> (..., 4, 4, 12): the 2 x 2 cells, inner order [channel, dy, dx]."""
    s = G.shape[:-3]
    nd = len(s)
    X = G.reshape(s + (3, 4, 2, 4, 2))
    X = X.transpose(tuple(range(nd)) + (nd + 1, nd + 3, nd, nd + 2, nd + 4))
    return X.reshape(s + (4, 4, 12))


def halo_patches(G):
    """(..., 3, 8, 8) -> (..., 4, 4, 48): for each 2 x 2 cell, the 4 x 4 window of level-1 blocks centred
    on it (one block of halo on every side, periodic), inner order [channel, dy, dx] with dy, dx in -1..2."""
    xp = jnp if isinstance(G, jnp.ndarray) else np
    F = [xp.roll(G, (-dy, -dx), (-2, -1))[..., 0::2, 0::2] for dy in (-1, 0, 1, 2) for dx in (-1, 0, 1, 2)]
    X = xp.stack(F, -1)                                                         # (..., 3, 4, 4, 16)
    X = xp.moveaxis(X, -4, -2)                                                  # (..., 4, 4, 3, 16)
    return X.reshape(X.shape[:-2] + (48,))


def flat_latent(z):
    """(..., 4, 4, c) -> (..., 16 c) channel-major."""
    s = z.shape[:-3]
    c = z.shape[-1]
    return np.moveaxis(np.asarray(z), -1, -3).reshape(s + (16 * c,))


def chan_norm(Y):
    """Per-channel mean and sd of a set of level-1 frames (..., 192)."""
    G = grid(Y).reshape(-1, 3, 64)
    return G.mean((0, 2)), G.std((0, 2))


def std_grid(Y, mu, sd):
    return (grid(Y) - mu[:, None, None]) / sd[:, None, None]


# ----------------------------------------------------------------------------- hand / closed-form Phi2
def pool(Y, c):
    """2 x 2 block averages of the block view in raw units: c=1 total mass density (c0 + c1),
    c=2 (c0, c1), c=3 (c0, c1, m2). Returns (..., 16 c) channel-major."""
    P = grid(Y).reshape(Y.shape[:-1] + (3, 4, 2, 4, 2)).mean((-3, -1))      # (..., 3, 4, 4)
    if c == 1:
        P = P[..., :1, :, :] + P[..., 1:2, :, :]
    else:
        P = P[..., :c, :, :]
    return P.reshape(Y.shape[:-1] + (16 * c,))


def train_patches(Ytr, mu, sd):
    return patches(std_grid(Ytr, mu, sd)).reshape(-1, 12)


def local_pca(Ytr, mu, sd, c):
    X = train_patches(Ytr, mu, sd)
    w, U = np.linalg.eigh(np.cov(X.T))
    return U[:, np.argsort(w)[::-1][:c]], np.sort(w)[::-1]


def local_tica(Ytr_traj, mu, sd, c, lag):
    """Symmetrised lag-`lag` TICA on the 12-dim cell patches (pooled over cells and trajectories)."""
    P = patches(std_grid(Ytr_traj, mu, sd))                                    # (J, T, 4, 4, 12)
    X0 = P[:, :-lag].reshape(-1, 12)
    X1 = P[:, lag:].reshape(-1, 12)
    m = P.reshape(-1, 12).mean(0)
    C0 = np.cov(P.reshape(-1, 12).T)
    Ct = (X0 - m).T @ (X1 - m) / len(X0)
    Ct = 0.5 * (Ct + Ct.T)
    import scipy.linalg as sl
    w, U = sl.eigh(Ct, C0)
    o = np.argsort(w)[::-1][:c]
    return U[:, o], w[o]


def global_pca(Ytr, q):
    m, s = Ytr.reshape(-1, 192).mean(0), Ytr.reshape(-1, 192).std(0)
    X = (Ytr.reshape(-1, 192) - m) / s
    w, U = np.linalg.eigh(np.cov(X.T))
    o = np.argsort(w)[::-1][:q]
    return m, s, U[:, o]


SPATIAL = {"u": np.array([1, 1, 1, 1]) / 2.0,          # cell positions (dy, dx) = (0,0), (0,1), (1,0), (1,1)
           "dx": np.array([-1, 1, -1, 1]) / 2.0, "dy": np.array([-1, -1, 1, 1]) / 2.0,
           "quad": np.array([1, -1, -1, 1]) / 2.0}


def pool_subspaces(sd):
    """Reference subspaces in standardised-patch coordinates (12 = [ch, dy, dx]):
    P3 pooling of each channel; P2 pooling of the two mass channels; P1 pooled total mass c0 + c1;
    Pmom9 zeroth + first spatial moments of every channel; Pmm3 zeroth + first moments of total mass."""
    S = SPATIAL
    e = lambda ch, m: np.kron(np.eye(3)[ch], S[m])
    P3 = np.stack([e(0, "u"), e(1, "u"), e(2, "u")], 1)
    P2 = P3[:, :2]
    mass = lambda m: sd[0] * e(0, m) + sd[1] * e(1, m)                         # raw c0 + c1 in std units
    P1 = (mass("u") / np.linalg.norm(mass("u")))[:, None]
    Pmom9 = np.stack([e(ch, m) for ch in range(3) for m in ("u", "dx", "dy")], 1)
    Pmm3 = np.stack([mass(m) for m in ("u", "dx", "dy")], 1)
    return {"P3": P3, "P2": P2, "P1": P1, "Pmom9": Pmom9, "Pmm3": Pmm3}


def pool_mom(Y):
    """Designed Phi2 'pmom3': per 2 x 2 cell, the mean total mass density (c0 + c1) and its first spatial
    moments (right minus left, bottom minus top, /4), raw units. (..., 48) channel-major."""
    G = grid(Y)
    m = (G[..., 0, :, :] + G[..., 1, :, :]).reshape(Y.shape[:-1] + (4, 2, 4, 2))   # (..., I, dy, J, dx)
    u = m.mean((-3, -1))
    dx = (m[..., :, :, :, 1] - m[..., :, :, :, 0]).mean(-2) / 2.0               # (..., I, dy, J) -> (..., I, J)
    dy = (m[..., :, 1, :, :] - m[..., :, 0, :, :]).mean(-1) / 2.0               # (..., I, J, dx) -> (..., I, J)
    return np.stack([u, dx, dy], -3).reshape(Y.shape[:-1] + (48,))


def span_alignment(W, P):
    """tr(Pi_W Pi_P) / dim(W): mean squared cosine of the principal angles of span(W) to span(P)
    (1 when span(W) lies inside span(P))."""
    Qw, _ = np.linalg.qr(W)
    Qp, _ = np.linalg.qr(P)
    return float(np.sum((Qp.T @ Qw) ** 2) / W.shape[1])


# ----------------------------------------------------------------------------- JAX encoders / heads
def mlp_init(key, dims, zero_last=False):
    P = []
    ks = jax.random.split(key, len(dims) - 1)
    for i, (a, b) in enumerate(zip(dims[:-1], dims[1:])):
        last = i == len(dims) - 2
        W = jnp.zeros((a, b)) if (last and zero_last) else jax.random.normal(ks[i], (a, b)) * math.sqrt((1.0 if last else 2.0) / a)
        P.append({"W": W, "b": jnp.zeros(b)})
    return P


def mlp_apply(P, x):
    for i, L in enumerate(P):
        x = x @ L["W"] + L["b"]
        if i < len(P) - 1:
            x = jax.nn.gelu(x)
    return x


def enc_dims(kind, c):
    return {"LL": [12, c], "LM": [12, 64, 64, c], "GM": [192, GM_HIDDEN, GM_HIDDEN, 16 * c], "GL": [192, 16 * c], "LH": [48, c]}[kind]


GM_HIDDEN = 128


def init_enc(kind, c, key):
    if kind == "GM":                           # unconstrained control: linear map + zero-initialised MLP residual
        k1, k2 = jax.random.split(key)
        return {"lin": mlp_init(k1, [192, 16 * c]), "mlp": mlp_init(k2, enc_dims("GM", c), zero_last=True)}
    return mlp_init(key, enc_dims(kind, c))


def enc_apply(kind, P, Gs):
    """Gs standardised grids (N, 3, 8, 8) -> z (N, 4, 4, c)."""
    N = Gs.shape[0]
    if kind in ("LL", "LM"):
        return mlp_apply(P, patches(Gs))
    if kind == "LH":                           # local linear with a one-block halo (overlapping 4 x 4 windows, stride 2)
        return mlp_apply(P, halo_patches(Gs))
    x = Gs.reshape(N, 192)
    z = mlp_apply(P["lin"], x) + mlp_apply(P["mlp"], x) if kind == "GM" else mlp_apply(P, x)   # unconstrained
    return z.reshape(N, -1, 4, 4).transpose(0, 2, 3, 1)


def whiten(z, glob, eps=1e-6):
    """Batch whitening: per cell-channel (equivariant, c x c) or over all 16c numbers (global). The
    ridge eps is RELATIVE to the mean variance, so shrinking the latent cannot drive the loss to zero
    (an absolute floor let a weight-decayed MLP encoder collapse to val loss 0.0 in a pilot). eps is only
    numerical: with exact whitening the loss is invariant to rescaling any latent direction, so it gives
    no gradient toward shrinking one (train() records the smallest relative eigenvalue as a check)."""
    M = z.shape[0]
    Zf = z.reshape(M, -1) if glob else z.reshape(-1, z.shape[-1])
    mu = Zf.mean(0)
    D = Zf - mu
    Cv = D.T @ D / D.shape[0]
    Cv = Cv + eps * (jnp.trace(Cv) / D.shape[1] + 1e-30) * jnp.eye(D.shape[1])
    L = jnp.linalg.cholesky(Cv)
    Zw = jax.scipy.linalg.solve_triangular(L, D.T, lower=True).T
    return Zw.reshape(z.shape), mu, L


def nbhd(z):
    """(N, 4, 4, k) -> (N, 4, 4, 9k): the 3 x 3 periodic neighbourhood (value at i+dy, j+dx)."""
    return jnp.concatenate([jnp.roll(z, (-dy, -dx), (1, 2)) for dy in (-1, 0, 1) for dx in (-1, 0, 1)], -1)


def init_model(kind, obj, c, key):
    k = jax.random.split(key, 4)
    P = {"enc": init_enc(kind, c, k[0])}
    loc = kind in ("LL", "LM", "LH")
    if obj == "recon":
        if kind in ("LL", "LH"):
            P["dec"] = mlp_init(k[1], [c, 12])
        elif kind == "LM":
            P["dec"] = mlp_init(k[1], [c, 64, 64, 12])
        elif kind == "GL":
            P["dec"] = mlp_init(k[1], [16 * c, 192])
        else:
            P["dec"] = mlp_init(k[1], [16 * c, 256, 256, 192])
    elif obj == "closG":                       # global LINEAR head on 2 lags (the P0 / Kalman analogue)
        P["A"] = jnp.zeros((32 * c, 16 * c))
    elif obj in ("closL", "closLlin"):         # local head: 3 x 3 neighbourhood, 2 lags, shared weights
        assert loc
        d = 18 * c
        P["A"] = jnp.zeros((d, c))
        if obj == "closL":                     # linear + MLP
            P["head"] = mlp_init(k[1], [d, 64, 64, c], zero_last=True)
    elif obj == "pib":
        if loc:
            d = 18 * c
            P["A"] = jnp.zeros((d, 12))
            P["head"] = mlp_init(k[1], [d, 64, 64, 12], zero_last=True)
        else:
            d = 32 * c
            P["A"] = jnp.zeros((d, 192))
            P["head"] = mlp_init(k[1], [d, 256, 256, 192], zero_last=True)
    return P


PIB_NOISE = 0.5      # per-dimension channel noise on the whitened latent: <= 1/2 ln(1 + 1/0.25) = 0.80 nats/dim/tick


def make_loss(kind, obj, c):
    loc = kind in ("LL", "LM", "LH")
    glob_white = not loc
    assert obj not in ("closL", "closLlin") or loc

    def loss(P, Gm, G0, Gp, key):
        N = G0.shape[0]
        if obj == "recon":
            z = enc_apply(kind, P["enc"], G0)
            if loc:
                return jnp.mean((mlp_apply(P["dec"], z) - patches(G0)) ** 2)
            return jnp.mean((mlp_apply(P["dec"], z.reshape(N, -1)) - G0.reshape(N, 192)) ** 2)
        if obj in ("closG", "closL", "closLlin"):
            z3 = enc_apply(kind, P["enc"], jnp.concatenate([Gm, G0, Gp], 0))
            zw, _, _ = whiten(z3, glob_white)
            zm, z0, zp = zw[:N], zw[N:2 * N], zw[2 * N:]
            if obj == "closG":
                x = jnp.concatenate([z0.reshape(N, -1), zm.reshape(N, -1)], 1)
                pred = z0.reshape(N, -1) + x @ P["A"]
                return jnp.mean((pred - zp.reshape(N, -1)) ** 2)
            x = jnp.concatenate([nbhd(z0), nbhd(zm)], -1)
            pred = z0 + x @ P["A"] + (mlp_apply(P["head"], x) if obj == "closL" else 0.0)
            return jnp.mean((pred - zp) ** 2)
        if obj == "pib":
            z2 = enc_apply(kind, P["enc"], jnp.concatenate([Gm, G0], 0))
            zw, _, _ = whiten(z2, glob_white)
            zw = zw + PIB_NOISE * jax.random.normal(key, zw.shape)
            zm, z0 = zw[:N], zw[N:]
            if loc:
                x = jnp.concatenate([nbhd(z0), nbhd(zm)], -1)
                return jnp.mean((x @ P["A"] + mlp_apply(P["head"], x) - patches(Gp)) ** 2)
            x = jnp.concatenate([z0.reshape(N, -1), zm.reshape(N, -1)], 1)
            return jnp.mean((x @ P["A"] + mlp_apply(P["head"], x) - Gp.reshape(N, 192)) ** 2)
        raise ValueError(obj)
    return loss


def train(kind, obj, c, tau, Ytr, seed=0, steps=2000, batch=256, n_val_traj=3, eval_every=100, lr=None, wd=None):
    """Fit one encoder on the base trajectories Ytr (J, T, 192) of one half. Returns the frozen
    Phi2 (encoder params, channel normaliser, final whitening) and training info."""
    t0 = time.time()
    lr = lr or {"LL": 3e-3, "LM": 2e-3, "GM": 1e-3, "GL": 1e-3, "LH": 3e-3}[kind]
    wd = {"GM": 1.0}.get(kind, 0.0) if wd is None else wd    # decoupled, encoder matrices (GM only)
    mu, sd = chan_norm(Ytr)
    Gs = std_grid(Ytr, mu, sd).astype(np.float32)                              # (J, T, 3, 8, 8)
    J, T = Gs.shape[:2]
    tr_j, va_j = np.arange(J - n_val_traj), np.arange(J - n_val_traj, J)
    tau_eff = tau if obj != "recon" else 0
    ts = np.arange(1, T - tau_eff)

    def pairs(js):
        jj, tt = np.meshgrid(js, ts, indexing="ij")
        return jj.ravel(), tt.ravel()
    jtr, ttr = pairs(tr_j)
    jva, tva = pairs(va_j)
    Gd = jnp.asarray(Gs)
    loss = make_loss(kind, obj, c)
    key = jax.random.PRNGKey(seed)
    P = init_model(kind, obj, c, key)
    M = jax.tree_util.tree_map(jnp.zeros_like, P)
    V = jax.tree_util.tree_map(jnp.zeros_like, P)

    def batch_of(j, t):
        return Gd[j, t - 1], Gd[j, t], Gd[j, t + tau_eff]

    @jax.jit
    def step(P, M, V, it, j, t, k):
        g = jax.grad(lambda P_: loss(P_, *batch_of(j, t), k))(P)
        M = jax.tree_util.tree_map(lambda m, gg: 0.9 * m + 0.1 * gg, M, g)
        V = jax.tree_util.tree_map(lambda v, gg: 0.999 * v + 0.001 * gg * gg, V, g)
        c1, c2 = 1 - 0.9 ** it, 1 - 0.999 ** it
        P = jax.tree_util.tree_map(lambda p, m, v: p - lr * (m / c1) / (jnp.sqrt(v / c2) + 1e-8), P, M, V)
        if wd > 0:
            P["enc"] = jax.tree_util.tree_map(lambda w: w * (1 - lr * wd) if w.ndim == 2 else w, P["enc"])
        return P, M, V

    jva_j, tva_j = jnp.asarray(jva), jnp.asarray(tva)
    val_fn = jax.jit(lambda P_: loss(P_, *batch_of(jva_j, tva_j), jax.random.PRNGKey(999)))
    rng = np.random.default_rng(seed + 17)
    best, bestP, hist = float(val_fn(P)), P, []
    v_init = best
    for it in range(1, steps + 1):
        ib = rng.integers(0, len(jtr), batch)
        P, M, V = step(P, M, V, float(it), jnp.asarray(jtr[ib]), jnp.asarray(ttr[ib]), jax.random.PRNGKey(seed * 100003 + it))
        if it % eval_every == 0 or it == steps:
            v = float(val_fn(P))
            hist.append((it, v))
            if v < best:
                best, bestP = v, P
    # frozen map: encoder + (for whitened objectives) the whitening computed on the whole half
    enc = jax.tree_util.tree_map(np.asarray, bestP["enc"])
    wmu, wL = None, None
    z = np.asarray(enc_apply(kind, bestP["enc"], jnp.asarray(Gs.reshape(-1, 3, 8, 8))))
    Zf = z.reshape(len(z), -1) if kind in ("GM", "GL") else z.reshape(-1, c)
    ev = np.linalg.eigvalsh(np.cov(Zf.T.astype(np.float64)).reshape(Zf.shape[1], Zf.shape[1]))
    min_rel_eig = float(ev.min() / ev.mean())
    if obj != "recon":
        _, m_, L_ = whiten(jnp.asarray(z), kind in ("GM", "GL"))
        wmu, wL = np.asarray(m_), np.asarray(L_)
    info = {"kind": kind, "obj": obj, "c": c, "tau": tau, "seed": seed, "steps": steps, "batch": batch, "lr": lr, "wd": wd,
            "val_init": v_init, "val_best": best, "val_hist": hist, "seconds": time.time() - t0,
            "n_train_pairs": int(len(jtr)), "n_val_pairs": int(len(jva)), "min_rel_eig_latent_cov": min_rel_eig}
    return {"kind": kind, "c": c, "enc": enc, "mu": mu, "sd": sd, "wmu": wmu, "wL": wL}, info


_ENC_JIT = {}


def apply_phi(phi, Y):
    """Frozen Phi2: level-1 frames (..., 192) -> latent (..., 16 c), deterministic."""
    s = Y.shape[:-1]
    kind = phi["kind"]
    Gs = std_grid(Y.reshape(-1, 192), phi["mu"], phi["sd"]).astype(np.float32)
    f = _ENC_JIT.get(kind)
    if f is None:
        f = _ENC_JIT[kind] = jax.jit(lambda P, G: enc_apply(kind, P, G))
    z = np.concatenate([np.asarray(f(phi["enc"], jnp.asarray(Gs[i:i + 4096]))) for i in range(0, len(Gs), 4096)])
    z = z.astype(np.float64)
    if phi["wL"] is not None:
        if kind in ("GM", "GL"):
            Zf = z.reshape(len(z), -1)
            Zf = np.linalg.solve(phi["wL"], (Zf - phi["wmu"]).T).T
            z = Zf.reshape(z.shape)
        else:
            Zf = z.reshape(-1, z.shape[-1])
            Zf = np.linalg.solve(phi["wL"], (Zf - phi["wmu"]).T).T
            z = Zf.reshape(z.shape)
    return flat_latent(z).reshape(s + (-1,))


def linear_phi(W, mu, sd):
    """A local linear encoder with weights W (12, c) in standardised-patch coordinates."""
    return {"kind": "LL", "c": W.shape[1], "enc": [{"W": np.asarray(W, np.float32), "b": np.zeros(W.shape[1], np.float32)}],
            "mu": mu, "sd": sd, "wmu": None, "wL": None}


def save_phi(phi, path):
    leaves = jax.tree_util.tree_leaves(phi["enc"])
    arrs = {f"leaf{i}": np.asarray(v, np.float32) for i, v in enumerate(leaves)}
    arrs.update(mu=phi["mu"], sd=phi["sd"])
    if phi["wL"] is not None:
        arrs["wmu"], arrs["wL"] = phi["wmu"], phi["wL"]
    np.savez_compressed(path, kind=phi["kind"], c=phi["c"], n_leaves=len(leaves), **arrs)


def load_phi(path):
    d = np.load(path)
    kind, c = str(d["kind"]), int(d["c"])
    tdef = jax.tree_util.tree_structure(init_enc(kind, c, jax.random.PRNGKey(0)))
    enc = jax.tree_util.tree_unflatten(tdef, [d[f"leaf{i}"] for i in range(int(d["n_leaves"]))])
    return {"kind": kind, "c": c, "enc": enc, "mu": d["mu"], "sd": d["sd"],
            "wmu": d["wmu"] if "wmu" in d else None, "wL": d["wL"] if "wL" in d else None}


# ----------------------------------------------------------------------------- certification
def make_lridge(gshape, p=2):
    c, gh, gw = gshape
    ncell = gh * gw
    nH = len(HZ)
    tmax = max(HZ)

    def feats(Y, ts):
        Zg = Y.reshape(len(Y), c, gh, gw)
        F = [np.roll(Zg[ts - l], (-dy, -dx), (2, 3)) for l in range(p) for dy in (-1, 0, 1) for dx in (-1, 0, 1)]
        return np.stack(F, 1).reshape(len(ts), -1, ncell).transpose(0, 2, 1)       # (n, cells, 9 c p)

    def extra(f, Ys, tr_j, fit_j, va_j, te_items):
        def mk(js):
            X, T = [], []
            for jj in js:
                Y = Ys[jj]
                ts = np.arange(p - 1, len(Y) - tmax)
                X.append(feats(Y, ts).reshape(-1, 9 * c * p))
                Zg = Y.reshape(len(Y), c, ncell)
                T.append(np.stack([(Zg[ts + h] - Zg[ts]).transpose(0, 2, 1).reshape(-1, c) for h in HZ], 0))
            return np.concatenate(X), np.concatenate(T, 1)
        Xf, Tf = mk(fit_j)
        Xv, Tv = mk(va_j)
        rg = AN.Ridge().fit(Xf, list(Tf), Xv, list(Tv))
        del Xf, Tf, Xv, Tv
        X, T = mk(tr_j)
        rg = AN.Ridge().fit(X, list(T), lams=rg.lams)
        del X, T
        out = []
        for jj, i, t in te_items:
            x = feats(Ys[jj], np.array([t]))[0]                                     # (cells, d)
            z0 = Ys[jj][t].reshape(c, ncell)
            out.append(np.stack([(z0 + rg.predict(x, hi).T).reshape(-1) for hi in range(nH)]))
        return {"lridge": np.stack(out)}
    return extra


class _RidgeWide(AN.Ridge):
    LAMS = AN.Ridge.LAMS + [1e6, 1e7, 1e8, 1e9]      # lets the level-1 correction shrink to zero


def make_yridge(Y1s, p=2):
    """Two-stage: 'ridge_p2' on the latent past (refitted exactly as closure_ext does), then a ridge of
    its residual on the level-1 past (2 lags of the standardised 192 numbers), penalty chosen on the
    validation trajectories from a grid that reaches 1e9 (so the correction can vanish).
    Y1s: list of standardised level-1 trajectories (T, 192) of the certification half."""
    nH = len(HZ)
    tmax = max(HZ)

    def extra(f, Ys, tr_j, fit_j, va_j, te_items):
        AN.HORIZONS = list(HZ)

        def mk(js):
            X, F, Y0 = AN.multi_pairs([Ys[jj] for jj in js], p, tmax)
            Yl = np.concatenate([AN.lag_matrix(Y1s[jj], np.arange(p - 1, len(Ys[jj]) - tmax), p) for jj in js])
            return X, [F[hi] - Y0 for hi in range(nH)], Yl
        Xf, Tf, Ylf = mk(fit_j)
        Xv, Tv, Ylv = mk(va_j)
        r1 = AN.Ridge().fit(Xf, Tf, Xv, Tv)
        Rf = [Tf[hi] - r1.predict(Xf, hi) for hi in range(nH)]
        Rv = [Tv[hi] - r1.predict(Xv, hi) for hi in range(nH)]
        r2 = _RidgeWide().fit(Ylf, Rf, Ylv, Rv)
        X, T, Yl = mk(tr_j)
        r1 = AN.Ridge().fit(X, T, lams=r1.lams)
        R = [T[hi] - r1.predict(X, hi) for hi in range(nH)]
        r2 = _RidgeWide().fit(Yl, R, lams=r2.lams)
        out = []
        for jj, i, t in te_items:
            x = AN.lag_matrix(Ys[jj], np.array([t]), p)
            yl = AN.lag_matrix(Y1s[jj], np.array([t]), p)
            out.append(np.stack([Ys[jj][t] + r1.predict(x, hi)[0] + r2.predict(yl, hi)[0] for hi in range(nH)]))
        return {"yridge": np.stack(out), }
    return extra


def certify(Zt, ZB, gshape=None, Y1s=None, rmlp=False):
    """Zt (J, 301, q), ZB (J, 4, 5, 32, q): one certification half. Returns per-item errors for every
    predictor, the oracle, item trajectory index, and the per-half Gaussian log-det measures."""
    AN.HORIZONS = list(HZ)
    J = Zt.shape[0]
    D = {"Yc": [Zt[j] for j in range(J)], "Bc": [ZB[j] for j in range(J)],
         "st_tick": [np.array(TEST) for _ in range(J)], "j": list(range(J))}
    sd = np.concatenate(D["Yc"]).std(0)
    eff_all = bool((sd > 1e-6 * max(sd.max(), 1e-12)).all())
    hooks = []
    if gshape is not None and eff_all:
        hooks.append(make_lridge(gshape))
    if Y1s is not None and eff_all:
        hooks.append(make_yridge(Y1s))
    if rmlp:
        hooks.append(CL.make_rmlp_extra(seeds=(0,), epochs=300))
    out, det = CL.closure_ext(D, "coarse", K=None, mlp=False, extra=CL.combine(*hooks) if hooks else None)
    err, orac, FUT, preds = det["err"], det["orac"], det["FUT"], det["preds"]
    n, R, nH, q = FUT.shape
    # Gaussian log-det measures (this half's own coordinates)
    ld = {}
    Do = FUT - FUT.mean(1, keepdims=True)

    def S_of(P):
        E = FUT - P[:, None]
        return np.einsum("nrhi,nrhj->hij", E, E) / (n * R)
    So = np.einsum("nrhi,nrhj->hij", Do, Do) / (n * (R - 1))
    S = {nm: S_of(preds[nm]) for nm in preds}
    Vg = {nm: err[nm].mean(0) for nm in FAM_G}
    bestG = [min(FAM_G, key=lambda nm: Vg[nm][hi]) for hi in range(nH)]
    lds = lambda M, dof: np.array([logdet(M[hi], dof) for hi in range(nH)])
    l_or = lds(So, n * (R - 1))
    l_mean = lds(S["mean"], n * R)
    l_best = np.array([logdet(S[bestG[hi]][hi], n * R) for hi in range(nH)])
    ld["I_avail"] = 0.5 * (l_mean - l_or)
    ld["I_capt"] = 0.5 * (l_mean - l_best)
    ld["gapX"] = 0.5 * (l_best - l_or)
    ld["bestG"] = bestG
    if "lridge" in S:
        ld["I_capt_local"] = 0.5 * (l_mean - lds(S["lridge"], n * R))
    if "yridge" in S:                          # Prop. 6 split on the ridge_p2 base: gapX_r2 = gammaY + inherit
        l_y = lds(S["yridge"], n * R)
        l_r2 = lds(S["ridge_p2"], n * R)
        ld["gapX_r2"] = 0.5 * (l_r2 - l_or)
        ld["gammaY"] = 0.5 * (l_r2 - l_y)
        ld["inherit"] = 0.5 * (l_y - l_or)
    ld["q"] = q
    return {"err": {k: v.astype(np.float64) for k, v in err.items()}, "orac": orac, "item_j": det["item_j"],
            "ld": ld, "n_eff": out["n_eff_coords"], "q": q}


def nontriviality(Zt, Y1t, P3t=None):
    """On one certification half's base trajectories: within-trajectory variance fraction, participation
    ratio of the correlation matrix, linear R^2 of level 1 from z (content), and R^2 between z and pool3."""
    J, T, q = Zt.shape
    Z = Zt.reshape(-1, q)
    s = Z.std(0)
    keep = s > 1e-9 * max(s.max(), 1e-30)
    r_dyn = float(np.mean(Zt[..., keep].var(1).mean(0) / Z[:, keep].var(0)))
    C = np.corrcoef(Z[:, keep].T) if keep.sum() > 1 else np.ones((1, 1))
    ev = np.clip(np.linalg.eigvalsh(C), 0, None)
    pr = float(ev.sum() ** 2 / (ev ** 2).sum())

    def r2(X, Yt):
        X1 = np.column_stack([np.ones(len(X)), X])
        coef, *_ = np.linalg.lstsq(X1, Yt, rcond=None)
        res = Yt - X1 @ coef
        return float(1 - (res ** 2).sum() / ((Yt - Yt.mean(0)) ** 2).sum())
    Y1 = Y1t.reshape(-1, 192)
    Y1 = (Y1 - Y1.mean(0)) / Y1.std(0)
    Zs = (Z[:, keep] - Z[:, keep].mean(0)) / Z[:, keep].std(0)
    out = {"r_dyn": r_dyn, "participation_ratio": pr, "R2_level1_from_z": r2(Zs, Y1)}
    if P3t is not None:
        P3 = P3t.reshape(-1, P3t.shape[-1])
        P3 = (P3 - P3.mean(0)) / P3.std(0)
        out["R2_pool3_from_z"] = r2(Zs, P3)
        out["R2_z_from_pool3"] = r2(P3, Zs)
    return out


def combine(cA, cB, n_boot=400, seed=0):
    """Pool two certified halves (cert half A uses the Phi2 fitted on B and vice versa)."""
    names = sorted(set(cA["err"]) & set(cB["err"]))
    err = {nm: np.concatenate([cA["err"][nm], cB["err"][nm]]) for nm in names}
    orac = np.concatenate([cA["orac"], cB["orac"]])
    ij = np.concatenate([cA["item_j"], cB["item_j"] + NJ])

    def fam(idx, names_):
        V0 = err["mean"][idx].mean(0)
        Vu = orac[idx].mean(0)
        Vs = np.stack([err[nm][idx].mean(0) for nm in names_])
        return (V0 - Vs.min(0)) / (V0 - Vu), Vs.argmin(0), V0, Vu, Vs.min(0)
    fams = {"G": [nm for nm in FAM_G if nm in err]}
    if "lridge" in err:
        fams["L"] = ["lridge"]
        fams["GL"] = fams["G"] + ["lridge"]
    if "rmlp" in err:
        fams["G+rmlp"] = fams["G"] + ["rmlp"]
    all_idx = np.arange(len(ij))
    rng = np.random.default_rng(seed)
    uj = np.unique(ij)
    boots = [np.concatenate([np.flatnonzero(ij == u) for u in rng.choice(uj, uj.size, replace=True)]) for _ in range(n_boot)]
    res = {}
    for fn, nms in fams.items():
        c, arg, V0, Vu, Vb = fam(all_idx, nms)
        se = np.std([fam(b, nms)[0] for b in boots], 0)
        res[fn] = {"ceiling": c, "se": se, "best": [nms[a] for a in arg], "V0": V0, "V_oracle": Vu, "V_best": Vb}
    # half-difference of the G ceiling (Phi2 fitted on different data)
    cGA = fam(np.flatnonzero(ij < NJ), fams["G"])[0]
    cGB = fam(np.flatnonzero(ij >= NJ), fams["G"])[0]
    res["G_half_A_cert"], res["G_half_B_cert"] = cGA, cGB
    ld = {}
    for k in cA["ld"]:
        if k in ("bestG", "q"):
            continue
        if k in cB["ld"]:
            ld[k] = 0.5 * (np.asarray(cA["ld"][k]) + np.asarray(cB["ld"][k]))
            ld[k + "_halfdiff"] = np.asarray(cA["ld"][k]) - np.asarray(cB["ld"][k])
    if "I_capt" in ld:
        ld["c_info"] = ld["I_capt"] / ld["I_avail"]
    res["logdet"] = ld
    res["q"] = cA["q"]
    return res


def tau_half(c, hz=HZ):
    """First horizon with c < 0.5, log-linear interpolation; None if never below 0.5 by 16."""
    c = np.asarray(c)
    for i in range(1, len(hz)):
        if c[i] < 0.5 <= c[i - 1]:
            a, b = math.log(hz[i - 1]), math.log(hz[i])
            return float(math.exp(a + (b - a) * (c[i - 1] - 0.5) / (c[i - 1] - c[i])))
    return None if c[-1] >= 0.5 else float(hz[0])


def jsonable(o):
    return CL.jsonable(o)
