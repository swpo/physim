"""ctrain -- fit every encoder of the `bias2` grid on the GPU and encode the certification data (see c5.py).

usage: python -B ctrain.py          (B5_WORLD; B5_TINY=1: code-path test)
round4/bias/btrain.py for 4-field worlds. For each config (c5.configs(), priority order) four replicas are
trained at once (jax.vmap): fit half A or B x seed 0 or 1 (independent inits and batch streams). Adam, cosine
learning-rate decay, early stopping on held-out trajectories of the fit half (the last N_VAL), best-validation
parameters frozen. EVERY encoder (N, L, U, Uc) has the same settings: 3,000 steps, batch 128, peak learning rate
1e-3, no weight decay (round 4's unconstrained control had 2,000 steps, batch 256 and weight decay 0.3).
Frozen Phi = encoder (+ for whitened objectives the whitening computed on the fit half). Each frozen Phi is
applied to the OTHER half's certification trajectories (base + branches) -> $B5_WORK/<world>/lat/<phi>__cert<h>.npz
plus a .ready marker that the CPU certification workers (ccert.py) pick up.
Hand designs first (chand.py: window means of pixel features; closed-form slow features and PCA fitted on the
other half); their .ready markers are written only after every hand file exists, because the workers read hand
designs as agreement targets.
Memory (round-4 lesson): every jitted function takes the device data as ARGUMENTS; compiled trainers and encoders
are dropped and the JAX caches cleared after every config.
"""
import gc
import json
import os
import time

import numpy as np

import c5

c5.setup_paths()
import jax  # noqa: E402

jax.config.update("jax_enable_x64", False)
import jax.numpy as jnp  # noqa: E402

import chand as CHD  # noqa: E402
import cnets as BN  # noqa: E402

T0 = time.time()
DATA = c5.work_dir("data")
LAT = c5.work_dir("lat")
OUT = c5.out_dir()
TRN = c5.out_dir("train")
WIN = c5.out_dir("windows")
SUB = c5.out_dir("latsub")
HI = {h: i for i, h in enumerate(c5.HALVES)}
OTHER = {"A": "B", "B": "A"}
TMAXH = max(c5.HTR)
REPS = [("A", 0), ("A", 1), ("B", 0), ("B", 1)]
if c5.TINY:
    STEPS, CHUNK, BATCH, NV = 4, 2, 2, 4
else:
    STEPS, CHUNK, BATCH, NV = 3000, 250, 128, 256
LR, WD = 1e-3, 0.0                                     # peak; cosine decay to 10% over the run; no weight decay
ENC_CHUNK = 4 if c5.TINY else 1024
WSTRIDE = 1 if c5.TINY else 2                          # whitening statistics from every 2nd tick of the fit half
SUBSTRIDE = 6 if c5.TINY else 20                       # subsampled latents returned for checking (every 20th tick)
NC = c5.NCH


def log(*a):
    c5.progress(f"[ctrain {time.time() - T0:7.1f}s] " + " ".join(str(x) for x in a))


def mem():
    try:
        st = jax.devices()[0].memory_stats() or {}
        return (f"{st.get('peak_bytes_in_use', 0) / 2**30:.1f} GB peak, "
                f"{st.get('bytes_in_use', 0) / 2**30:.1f} GB in use")
    except Exception:
        return "n/a"


def release():
    """Drop every compiled trainer / encoder and JAX's caches, then collect (between configs)."""
    _TRAINERS.clear()
    _ENCD.clear()
    gc.collect()
    jax.clear_caches()


# ----------------------------------------------------------------------------- data
Xh = {h: np.load(f"{DATA}/X_{h}.npy", mmap_mode="r") for h in c5.HALVES}
XBh = {h: np.load(f"{DATA}/XB_{h}.npy", mmap_mode="r") for h in c5.HALVES}
J, T1 = Xh["A"].shape[:2]
assert Xh["B"].shape == Xh["A"].shape and Xh["A"].shape[2:] == (NC, c5.NPIX, c5.NPIX)
JC = c5.J_CERT
N_VAL = 1 if (c5.TINY or c5.PILOT) else (8 if J >= 48 else 4)
STAT = {}
for h in c5.HALVES:
    s1 = np.zeros(NC)
    s2 = np.zeros(NC)
    n = 0
    for j in range(J):
        a = np.asarray(Xh[h][j], np.float64)
        s1 += a.sum((0, 2, 3))
        s2 += (a ** 2).sum((0, 2, 3))
        n += a.shape[0] * a.shape[2] * a.shape[3]
    mu = s1 / n
    sd = np.sqrt(np.maximum(s2 / n - mu ** 2, 0.0))
    assert np.all(sd > 1e-8), (h, sd)                  # a constant level-0 field would make the study meaningless
    STAT[h] = (mu, sd)
MU = jnp.asarray(np.stack([STAT[h][0] for h in c5.HALVES]), jnp.float32)          # (2, 4)
SD = jnp.asarray(np.stack([STAT[h][1] for h in c5.HALVES]), jnp.float32)
Xd = jnp.stack([jax.device_put(np.asarray(Xh[h])) for h in c5.HALVES])          # (2, J, T+1, 4, 128, 128)
XBd = jnp.stack([jax.device_put(np.asarray(XBh[h]).reshape((-1, NC, c5.NPIX, c5.NPIX))) for h in c5.HALVES])
NBR = XBd.shape[1]
BSHAPE = XBh["A"].shape[:4]
jax.block_until_ready((Xd, XBd))
log("data on device", Xd.shape, XBd.shape, "field mean/sd", {h: (STAT[h][0].round(4).tolist(), STAT[h][1].round(4).tolist())
                                                   for h in c5.HALVES}, mem())
N_TR = J - N_VAL
T_LO, T_HI = 1, T1 - 1 - TMAXH                                                    # t in [1, T - 16]
_rng = np.random.default_rng(4242)
VAL_J = np.stack([_rng.integers(N_TR, J, 512) for _ in c5.HALVES])
VAL_T = np.stack([_rng.integers(T_LO, T_HI + 1, 512) for _ in c5.HALVES])


def gather(X, mu, sd, hidx, j, t, offs):
    """Standardised frames (F, n, 4, 128, 128) of half hidx at trajectories j, ticks t + offs (X passed as an
    argument, never closed over)."""
    x = X[hidx, j[None, :], t[None, :] + jnp.asarray(offs)[:, None]]
    return (x - mu[hidx][:, None, None]) / sd[hidx][:, None, None]


# ----------------------------------------------------------------------------- encoding (frozen Phi)
_ENCD = {}


def _enc_jit(enc, h, which, parts=False):
    """Jitted encoder reading frames straight from the device copies: 'base' (Xd[half, j, t]) or 'branch'
    (XBd[half, k]); standardised with the fit half's statistics (hi)."""
    k = (enc, h, which, parts)
    if k not in _ENCD:
        def app(P, xs):
            if not parts:
                return BN.enc_apply(enc, h, P, xs)
            lin, nl = BN.enc_parts(enc, h, P, xs)
            return BN.field_parts(enc, h, P, xs), (jnp.zeros_like(lin) if nl is None else nl), lin
        if which == "base":
            def g(P, X, mu, sd, dh, j, t, hi):
                x = X[dh, j, t]
                return app(P, (x - mu[hi][:, None, None]) / sd[hi][:, None, None])
        else:
            def g(P, X, mu, sd, dh, kk, hi):
                x = X[dh, kk]
                return app(P, (x - mu[hi][:, None, None]) / sd[hi][:, None, None])
        _ENCD[k] = jax.jit(g)
    return _ENCD[k]


def _pad(a):
    n = len(a)
    m = -(-n // ENC_CHUNK) * ENC_CHUNK
    return np.concatenate([a, np.zeros(m - n, a.dtype)]), n


def encode_base(enc, h, P, data_h, jj, tt, hidx):
    """Base frames (jj, tt) of half data_h -> z (n, 8, 8, c) float64 numpy. One transfer at the end."""
    f = _enc_jit(enc, h, "base")
    (jp, n), (tp, _) = _pad(np.asarray(jj)), _pad(np.asarray(tt))
    out = [f(P, Xd, MU, SD, HI[data_h], jnp.asarray(jp[i:i + ENC_CHUNK]), jnp.asarray(tp[i:i + ENC_CHUNK]), hidx)
           for i in range(0, len(jp), ENC_CHUNK)]
    return np.asarray(jnp.concatenate(out), np.float64)[:n]


def encode_branch(enc, h, P, data_h, hidx):
    f = _enc_jit(enc, h, "branch")
    kp, n = _pad(np.arange(NBR))
    out = [f(P, XBd, MU, SD, HI[data_h], jnp.asarray(kp[i:i + ENC_CHUNK]), hidx) for i in range(0, len(kp), ENC_CHUNK)]
    return np.asarray(jnp.concatenate(out), np.float64)[:n]


def field_shares(enc, h, P, data_h, hidx):
    """Local encoders: how much of each latent channel's variance each level-0 field's linear window and the
    nonlinear branch carry, share_k = cov(part_k, z) / var(z) (sums to 1 over the parts; pooled over blocks and
    over every 4th base tick of the certification trajectories of half data_h), plus the correlation of each part
    with z."""
    f = _enc_jit(enc, h, "base", parts=True)
    jj, tt = np.meshgrid(np.arange(JC), np.arange(0, T1, 1 if c5.TINY else 4), indexing="ij")
    (jp, n), (tp, _) = _pad(jj.ravel()), _pad(tt.ravel())
    fp, nl = [], []
    for i in range(0, len(jp), ENC_CHUNK):
        a, b, _ = f(P, Xd, MU, SD, HI[data_h], jnp.asarray(jp[i:i + ENC_CHUNK]), jnp.asarray(tp[i:i + ENC_CHUNK]), hidx)
        fp.append(np.asarray(a, np.float64))
        nl.append(np.asarray(b, np.float64))
    fp, nl = np.concatenate(fp)[:n], np.concatenate(nl)[:n]              # (n, 8, 8, c, 4), (n, 8, 8, c)
    c = fp.shape[3]
    out = []
    for k in range(c):
        parts = np.concatenate([fp[..., k, :].reshape(-1, NC), nl[..., k].reshape(-1, 1)], 1)     # (m, 5)
        parts = parts - parts.mean(0)
        z = parts.sum(1)
        vz = float(z.var())
        sh = (parts * z[:, None]).mean(0) / max(vz, 1e-300)
        sdp = parts.std(0)
        cr = (parts * z[:, None]).mean(0) / np.maximum(sdp * np.sqrt(vz), 1e-300)
        out.append({"share": dict(zip(list(c5.FIELDS) + ["nonlinear"], sh.tolist())),
                    "corr_with_z": dict(zip(list(c5.FIELDS) + ["nonlinear"], cr.tolist())),
                    "sd_part_over_sd_z": dict(zip(list(c5.FIELDS) + ["nonlinear"], (sdp / max(np.sqrt(vz), 1e-300)).tolist()))})
    return out


def whitening(z, glob):
    Zf = z.reshape(len(z), -1) if glob else z.reshape(-1, z.shape[-1])
    mu = Zf.mean(0)
    C = np.cov(Zf.T).reshape(Zf.shape[1], Zf.shape[1])
    ev = np.linalg.eigvalsh(C)
    C = C + 1e-9 * np.trace(C) / len(C) * np.eye(len(C))
    return mu, np.linalg.cholesky(C), float(ev.min() / max(ev.mean(), 1e-300))


def apply_white(z, W, glob):
    if W is None:
        return z
    mu, L = W
    Zf = z.reshape(len(z), -1) if glob else z.reshape(-1, z.shape[-1])
    Zf = np.linalg.solve(L, (Zf - mu).T).T
    return Zf.reshape(z.shape)


def flat_cm(z):
    """(N, 8, 8, c) -> (N, 64 c) channel-major (c, 8, 8)."""
    return np.moveaxis(z, -1, 1).reshape(len(z), -1)


def save_latent(stem, ch, Zt, ZB, gshape, meta, ready=True, sub=False):
    path = f"{LAT}/{stem}__cert{ch}.npz"
    np.savez(path + ".tmp.npz", Zt=Zt.astype(np.float32), ZB=ZB.astype(np.float32), gshape=np.asarray(gshape),
             meta=json.dumps(c5.jsonable(meta)))
    os.replace(path + ".tmp.npz", path)
    if sub:
        np.savez_compressed(f"{SUB}/{stem}__cert{ch}.npz", Zt=Zt[:, ::SUBSTRIDE].astype(np.float16),
                            ticks=np.arange(0, Zt.shape[1], SUBSTRIDE), gshape=np.asarray(gshape))
    if ready:
        open(path + ".ready", "w").close()
    return path


def encode_cert(enc, h, P, W, glob, fit_h):
    """The frozen Phi (fitted on fit_h) on the other half's certification data: Zt (JC, T+1, q), ZB."""
    ch = OTHER[fit_h]
    hidx = HI[fit_h]                       # standardise with the FIT half's statistics (part of the frozen Phi)
    jj, tt = np.meshgrid(np.arange(JC), np.arange(T1), indexing="ij")
    zt = encode_base(enc, h, P, ch, jj.ravel(), tt.ravel(), hidx)
    zb = encode_branch(enc, h, P, ch, hidx)
    zt, zb = apply_white(zt, W, glob), apply_white(zb, W, glob)
    q = zt.shape[1] * zt.shape[2] * zt.shape[3]
    return ch, flat_cm(zt).reshape(JC, T1, q), flat_cm(zb).reshape(BSHAPE + (q,))


# ----------------------------------------------------------------------------- hand designs
def pooled_features():
    """Per half: {h: (base (JC, T1, nf_h, 64), branch (JC, nT, R, TB, nf_h, 64))} float64 window means of the pixel
    features (h = 0: chand.feature_list; h > 0: c5.BASE1), raw units."""
    names = CHD.feature_list(c5.WORLD)
    nb = len(c5.BASE1)
    pf = CHD.pixel_features(c5.WORLD)

    def one(x):
        F = pf(x)
        full = jnp.stack([F[n] for n in names], 1)                                   # (N, nf, 128, 128)
        outs = [CHD.pool(full, 0).reshape(x.shape[0], len(names), 64)]
        for hh in c5.HSMOOTH[1:]:
            outs.append(CHD.pool(full[:, :nb], hh).reshape(x.shape[0], nb, 64))
        return outs

    fb = jax.jit(lambda X, dh, j, t: one(X[dh, j, t]))
    fr = jax.jit(lambda X, dh, kk: one(X[dh, kk]))
    res = {}
    for ch in c5.HALVES:
        jj, tt = np.meshgrid(np.arange(JC), np.arange(T1), indexing="ij")
        (jp, n), (tp, _) = _pad(jj.ravel()), _pad(tt.ravel())
        ob = [fb(Xd, HI[ch], jnp.asarray(jp[i:i + ENC_CHUNK]), jnp.asarray(tp[i:i + ENC_CHUNK])) for i in range(0, len(jp), ENC_CHUNK)]
        kp, m = _pad(np.arange(NBR))
        orr = [fr(XBd, HI[ch], jnp.asarray(kp[i:i + ENC_CHUNK])) for i in range(0, len(kp), ENC_CHUNK)]
        res[ch] = {}
        for a, hh in enumerate(c5.HSMOOTH):
            B = np.concatenate([np.asarray(o[a], np.float64) for o in ob])[:n]
            R = np.concatenate([np.asarray(o[a], np.float64) for o in orr])[:m]
            res[ch][hh] = (B.reshape(JC, T1, B.shape[1], 64), R.reshape(BSHAPE + (R.shape[1], 64)))
    del fb, fr
    return names, res


def hand_designs():
    t1 = time.time()
    names, PF = pooled_features()
    paths = []
    closed = {}
    for fit_h in c5.HALVES:
        closed[fit_h] = CHD.fit_closed(PF[fit_h][0][0], names)
    c5.jdump({h: {k: v for k, v in closed[h].items()} for h in closed}, os.path.join(OUT, "closed_forms.json"))
    for ch in c5.HALVES:
        fit_h = OTHER[ch]
        for f in c5.BASE1:
            for hh in c5.HSMOOTH:
                i = names.index(f) if hh == 0 else c5.BASE1.index(f)
                Zt, ZB = PF[ch][hh][0][:, :, i], PF[ch][hh][1][..., i, :]
                nm = f"hand_{f}_h{hh}"
                paths.append(save_latent(nm, ch, Zt, ZB, (1, c5.G, c5.G), {"phi": nm, "kind": "hand", "cert": ch, "c": 1,
                                                                             "feature": f, "halo": hh}, ready=False,
                                         sub=hh in (0, 8)))
        for k, fs in c5.MULTI.items():
            idx = [names.index(f) for f in fs]
            Bt, Br = PF[ch][0]
            Zt = Bt[:, :, idx].reshape(JC, T1, len(idx) * 64)
            ZB = Br[..., idx, :].reshape(BSHAPE + (len(idx) * 64,))
            nm = f"hand_{k}"
            paths.append(save_latent(nm, ch, Zt, ZB, (len(idx), c5.G, c5.G), {"phi": nm, "kind": "hand", "cert": ch,
                                                                              "c": len(idx), "features": list(fs)}, ready=False))
        for k in c5.CLOSED:
            Zt = CHD.apply_closed(closed[fit_h], k, PF[ch][0][0])
            ZB = CHD.apply_closed(closed[fit_h], k, PF[ch][0][1])
            c = int(k[-1])
            nm = f"hand_{k}"
            paths.append(save_latent(nm, ch, Zt, ZB, (c, c5.G, c5.G), {"phi": nm, "kind": "closed", "cert": ch, "c": c,
                                                                       "fit": fit_h}, ready=False, sub=c == 1))
    for p in paths:                                    # every hand file exists before any worker starts on one
        open(p + ".ready", "w").close()
    log(f"hand designs queued: {len(paths)} files ({len(c5.hand_names())} designs x 2 halves) in {time.time() - t1:.1f}s")


# ----------------------------------------------------------------------------- training
_TRAINERS = {}


def trainer(enc, h, obj, c):
    key_ = (enc, h, obj, c)
    if key_ in _TRAINERS:
        return _TRAINERS[key_]
    loss = BN.make_loss(enc, h, obj, c)
    fe = BN.frames_needed(obj)
    B = BATCH
    n_steps = float(STEPS)

    def one_step(carry, X, mu, sd):
        P, M, V, it, key, hidx = carry
        key, kj, kt = jax.random.split(key, 3)
        j = jax.random.randint(kj, (B,), 0, N_TR)
        t = jax.random.randint(kt, (B,), T_LO, T_HI + 1)
        xe = gather(X, mu, sd, hidx, j, t, fe)
        g = jax.grad(loss)(P, xe)
        it = it + 1.0
        M = jax.tree_util.tree_map(lambda m, gg: 0.9 * m + 0.1 * gg, M, g)
        V = jax.tree_util.tree_map(lambda v, gg: 0.999 * v + 0.001 * gg * gg, V, g)
        c1, c2 = 1 - 0.9 ** it, 1 - 0.999 ** it
        lr_t = LR * (0.1 + 0.45 * (1 + jnp.cos(jnp.pi * jnp.minimum(it / n_steps, 1.0))))
        P = jax.tree_util.tree_map(lambda p, m, v: p - lr_t * (m / c1) / (jnp.sqrt(v / c2) + 1e-8), P, M, V)
        return (P, M, V, it, key, hidx)

    def chunk(P, M, V, it, key, hidx, X, mu, sd):
        (P, M, V, it, key, _), _ = jax.lax.scan(lambda cr, _: (one_step(cr, X, mu, sd), None),
                                                (P, M, V, it, key, hidx), None, length=CHUNK)
        return P, M, V, it, key

    def val(P, hidx, vj, vt, X, mu, sd):
        j, t = vj[hidx, :NV], vt[hidx, :NV]
        return loss(P, gather(X, mu, sd, hidx, j, t, fe))

    chunk_v = jax.jit(jax.vmap(chunk, in_axes=(0, 0, 0, 0, 0, 0, None, None, None)))
    val_v = jax.jit(jax.vmap(val, in_axes=(0, 0, None, None, None, None, None)))
    vj, vt = jnp.asarray(VAL_J), jnp.asarray(VAL_T)
    out = (lambda P, M, V, it, key, hidx: chunk_v(P, M, V, it, key, hidx, Xd, MU, SD),
           lambda P, hidx: val_v(P, hidx, vj, vt, Xd, MU, SD), B, NV)
    _TRAINERS[key_] = out
    return out


def pick(tree, i):
    return jax.tree_util.tree_map(lambda a: a[i], tree)


def train_config(cid, name, enc, h, obj, c):
    t1 = time.time()
    steps = 0 if obj == "rand" else STEPS
    keys = [jax.random.PRNGKey(100003 * cid + 1009 * s + 17 * HI[fh] + 5) for fh, s in REPS]
    P = jax.vmap(lambda k: BN.init_model(enc, h, "clos" if obj == "rand" else obj, c, k))(jnp.stack(keys))
    hidx = jnp.asarray([HI[fh] for fh, _ in REPS])
    hist, best_it = [], [0] * len(REPS)
    if steps:
        chunk_f, val_f, B, nv = trainer(enc, h, obj, c)
        M = jax.tree_util.tree_map(jnp.zeros_like, P)
        V = jax.tree_util.tree_map(jnp.zeros_like, P)
        it = jnp.zeros((len(REPS),), jnp.float32)
        skeys = jnp.stack([jax.random.PRNGKey(7 + 31 * cid + 1000 * s + 3 * HI[fh]) for fh, s in REPS])
        best = np.asarray(val_f(P, hidx))
        v_init = best.copy()
        bestP = P
        hist.append((0, best.tolist()))
        done = 0
        tch = []
        while done < steps:
            tc = time.time()
            P, M, V, it, skeys = chunk_f(P, M, V, it, skeys, hidx)
            done += CHUNK
            v = np.asarray(val_f(P, hidx))
            tch.append(time.time() - tc)
            if cid <= 5 and len(tch) <= 2:
                log(f"{name}: chunk {len(tch)} of {CHUNK} steps (+ val) in {tch[-1]:.1f}s")
            hist.append((done, v.tolist()))
            better = v < best
            for r in np.flatnonzero(better):
                best_it[r] = done
            bm = jnp.asarray(better)
            bestP = jax.tree_util.tree_map(lambda b, p: jnp.where(bm.reshape((-1,) + (1,) * (p.ndim - 1)), p, b), bestP, P)
            best = np.where(better, v, best)
        P = bestP
        t_train = time.time() - t1
        t_chunks = {"first_incl_compile": tch[0], "rest_mean": float(np.mean(tch[1:])) if len(tch) > 1 else None}
    else:
        v_init = best = np.full(len(REPS), np.nan)
        B = nv = 0
        t_train = 0.0
        t_chunks = None
    glob = BN.glob_white(enc)
    infos = []
    for r, (fh, s) in enumerate(REPS):
        Pe = pick(P["enc"], r)
        W, mre = None, None
        if obj != "recon":
            jj, tt = np.meshgrid(np.arange(J), np.arange(0, T1, WSTRIDE), indexing="ij")
            zfit = encode_base(enc, h, Pe, fh, jj.ravel(), tt.ravel(), HI[fh])
            mu, L, mre = whitening(zfit, glob)
            W = (mu, L)
            del zfit
        ch, Zt, ZB = encode_cert(enc, h, Pe, W, glob, fh)
        phi = f"{name}_s{s}"
        info = {"phi": phi, "config": name, "enc": enc, "h": h, "obj": obj, "c": c, "seed": s, "fit": fh, "cert": ch,
                "steps": steps, "batch": B, "lr": LR, "wd": WD, "val_n": nv, "whitening": "global" if glob else "per-channel",
                "val_init": float(v_init[r]), "val_best": float(best[r]), "best_step": best_it[r],
                "val_hist": [(a, b[r]) for a, b in hist], "min_rel_eig_latent_cov": mre,
                "train_seconds_config": t_train, "chunk_seconds": t_chunks, "n_val_traj": N_VAL, "n_train_traj": N_TR,
                "n_params_enc": int(sum(np.size(x) for x in jax.tree_util.tree_leaves(Pe)))}
        if enc in ("L", "N"):
            info["field_shares"] = field_shares(enc, h, Pe, ch, HI[fh])
            if c <= 2:
                np.savez_compressed(f"{WIN}/{phi}__fit{fh}.npz", W=np.asarray(Pe["W"], np.float32), sd=STAT[fh][1],
                                    mu=STAT[fh][0], h=h, c=c, enc=enc, obj=obj)
        save_latent(phi, ch, Zt, ZB, (c, c5.G, c5.G), info, sub=c == 1)
        infos.append(info)
    c5.jdump(infos, f"{TRN}/{name}.json")
    vtxt = (f"val {np.round(v_init, 4).tolist()} -> {np.round(best, 4).tolist()} (best at {best_it})" if steps
            else "untrained (no validation loss)")
    log(f"{name}: steps {steps}, {vtxt}, train {t_train:.1f}s (chunks {t_chunks}), total {time.time() - t1:.1f}s, "
        f"{mem()}")


def main():
    hand_designs()
    todo = [(nm, "L", hh, "rand", cc) for nm, hh, cc in c5.RANDOM] + list(c5.configs())
    if c5.PILOT:
        todo = todo[:2]                                 # hand designs and the untrained windows only
    dl = c5.deadline("train")
    skipped = []
    for cid, (name, enc, h, obj, c) in enumerate(todo):
        if time.time() > dl:
            skipped.append(name)
            continue
        try:
            train_config(cid, name, enc, h, obj, c)
        except Exception as exc:  # one config failing must not stop the grid
            import traceback
            log(f"{name} FAILED: {exc!r}")
            with open(os.path.join(OUT, "train_errors.txt"), "a") as f:
                f.write(f"{name}\n{traceback.format_exc()}\n")
            del exc
        release()
    c5.jdump({"skipped_by_deadline": skipped, "n_configs": len(todo), "seconds": time.time() - T0, "J": J,
              "n_val_traj": N_VAL, "settings": {"steps": STEPS, "batch": BATCH, "lr_peak": LR, "wd": WD, "val_n": NV},
              "platform": {"backend": jax.default_backend(), "devices": [str(d) for d in jax.devices()]}},
             os.path.join(OUT, "train_done.json"))
    open(os.path.join(LAT, "DONE"), "w").close()
    log("done; skipped", skipped)


if __name__ == "__main__":
    try:
        main()
    finally:
        open(os.path.join(LAT, "DONE"), "w").close()
