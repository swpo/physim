"""btrain -- fit every encoder of the round-4 `bias` grid on the GPU and encode the certification data (see b4.py).

usage: python -B btrain.py          (B4_TINY=1: code-path test)
For each config (b4.configs(), priority order) four replicas are trained at once (jax.vmap): fit half A or B x
seed 0 or 1 (independent inits and batch streams). Adam, early stopping on held-out trajectories of the fit half
(the last N_VAL_TRAJ), best-validation parameters frozen. Frozen Phi = encoder (+ for whitened objectives the
whitening computed on all frames of the fit half). Each frozen Phi is applied to the OTHER half's certification
trajectories (base + branches) -> $B4_WORK/lat/<phi>__cert<h>.npz plus a .ready marker that the CPU certification
workers (bcert.py) pick up. Hand designs (block mass, block channel means, block view, tent window, object mass and
object mass + position at block resolution) and untrained random linear windows go first.
"""
import json
import os
import time

import numpy as np

import b4

import jax  # noqa: E402

jax.config.update("jax_enable_x64", False)
import jax.numpy as jnp  # noqa: E402

import bnets as BN  # noqa: E402

T0 = time.time()
DATA = b4.work_dir("data")
LAT = b4.work_dir("lat")
OUT = b4.out_dir()
TRN = b4.out_dir("train")
WIN = b4.out_dir("windows")
HI = {h: i for i, h in enumerate(b4.HALVES)}
OTHER = {"A": "B", "B": "A"}
TMAXH = max(b4.HTR)
REPS = [("A", 0), ("A", 1), ("B", 0), ("B", 1)]
if b4.TINY:
    STEPS, CHUNK, BATCH, BATCH_U, NV = {"L": 4, "N": 4, "U": 4}, 2, 2, 4, 4
else:
    STEPS, CHUNK, BATCH, BATCH_U, NV = {"L": 3000, "N": 3000, "U": 2000}, 250, 128, 256, 256
LR = {"L": 1e-3, "N": 1e-3, "U": 1e-3}                  # peak; cosine decay to 10% over the run
WD_U = 0.3
ENC_CHUNK = 4 if b4.TINY else 1024
WSTRIDE = 1 if b4.TINY else 2                          # whitening statistics from every 2nd tick of the fit half


def log(*a):
    b4.progress(f"[btrain {time.time() - T0:7.1f}s] " + " ".join(str(x) for x in a))


def mem():
    try:
        st = jax.devices()[0].memory_stats() or {}
        return f"{st.get('peak_bytes_in_use', 0) / 2**30:.1f} GB peak"
    except Exception:
        return "n/a"


# ----------------------------------------------------------------------------- data
Xh = {h: np.load(f"{DATA}/X_{h}.npy", mmap_mode="r") for h in b4.HALVES}
XBh = {h: np.load(f"{DATA}/XB_{h}.npy", mmap_mode="r") for h in b4.HALVES}
L1h = {h: np.load(f"{DATA}/L1_{h}.npy") for h in b4.HALVES}
L1Bh = {h: np.load(f"{DATA}/L1B_{h}.npy") for h in b4.HALVES}
J, T1 = Xh["A"].shape[:2]
JC = b4.J_CERT
STAT = {}
for h in b4.HALVES:
    s1 = np.zeros(2)
    s2 = np.zeros(2)
    n = 0
    for j in range(J):
        a = np.asarray(Xh[h][j], np.float64)
        s1 += a.sum((0, 2, 3))
        s2 += (a ** 2).sum((0, 2, 3))
        n += a.shape[0] * a.shape[2] * a.shape[3]
    mu = s1 / n
    STAT[h] = (mu, np.sqrt(s2 / n - mu ** 2))
MU = jnp.asarray(np.stack([STAT[h][0] for h in b4.HALVES]), jnp.float32)          # (2, 2)
SD = jnp.asarray(np.stack([STAT[h][1] for h in b4.HALVES]), jnp.float32)
Xd = jnp.stack([jax.device_put(np.asarray(Xh[h])) for h in b4.HALVES])          # (2, J, T+1, 2, 128, 128)
XBd = jnp.stack([jax.device_put(np.asarray(XBh[h]).reshape((-1, 2, b4.NPIX, b4.NPIX))) for h in b4.HALVES])
NBR = XBd.shape[1]
jax.block_until_ready((Xd, XBd))
log("data on device", Xd.shape, XBd.shape, "channel mean/sd", {h: (STAT[h][0].round(4).tolist(), STAT[h][1].round(4).tolist())
                                                     for h in b4.HALVES}, mem())
N_TR = J - b4.N_VAL_TRAJ
T_LO, T_HI = 1, T1 - 1 - TMAXH                                                    # t in [1, T - 16]
_rng = np.random.default_rng(4242)
VAL_J = np.stack([_rng.integers(N_TR, J, 512) for _ in b4.HALVES])
VAL_T = np.stack([_rng.integers(T_LO, T_HI + 1, 512) for _ in b4.HALVES])


def gather(hidx, j, t, offs):
    """Standardised frames (F, n, 2, 128, 128) of half hidx at trajectories j, ticks t + offs."""
    x = Xd[hidx, j[None, :], t[None, :] + jnp.asarray(offs)[:, None]]
    return (x - MU[hidx][:, None, None]) / SD[hidx][:, None, None]


# ----------------------------------------------------------------------------- encoding (frozen Phi)
_ENCD = {}


def _enc_jit(enc, h, which):
    """Jitted encoder reading frames straight from the device copies: 'base' (Xd[half, j, t]) or 'branch'
    (XBd[half, k]); standardised with the fit half's statistics (hi)."""
    k = (enc, h, which)
    if k not in _ENCD:
        if which == "base":
            def g(P, dh, j, t, hi):
                x = Xd[dh, j, t]
                return BN.enc_apply(enc, h, P, (x - MU[hi][:, None, None]) / SD[hi][:, None, None])
        else:
            def g(P, dh, kk, hi):
                x = XBd[dh, kk]
                return BN.enc_apply(enc, h, P, (x - MU[hi][:, None, None]) / SD[hi][:, None, None])
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
    out = [f(P, HI[data_h], jnp.asarray(jp[i:i + ENC_CHUNK]), jnp.asarray(tp[i:i + ENC_CHUNK]), hidx)
           for i in range(0, len(jp), ENC_CHUNK)]
    return np.asarray(jnp.concatenate(out), np.float64)[:n]


def encode_branch(enc, h, P, data_h, hidx):
    f = _enc_jit(enc, h, "branch")
    kp, n = _pad(np.arange(NBR))
    out = [f(P, HI[data_h], jnp.asarray(kp[i:i + ENC_CHUNK]), hidx) for i in range(0, len(kp), ENC_CHUNK)]
    return np.asarray(jnp.concatenate(out), np.float64)[:n]


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


def save_latent(stem, ch, Zt, ZB, gshape, meta):
    path = f"{LAT}/{stem}__cert{ch}.npz"
    np.savez(path + ".tmp.npz", Zt=Zt.astype(np.float32), ZB=ZB.astype(np.float32), gshape=np.asarray(gshape),
             meta=json.dumps(b4.jsonable(meta)))
    os.replace(path + ".tmp.npz", path)
    open(path + ".ready", "w").close()


def encode_cert(enc, h, P, W, glob, fit_h):
    """The frozen Phi (fitted on fit_h) on the other half's certification data: Zt (JC, T+1, q), ZB."""
    ch = OTHER[fit_h]
    hidx = HI[fit_h]                       # standardise with the FIT half's statistics (part of the frozen Phi)
    jj, tt = np.meshgrid(np.arange(JC), np.arange(T1), indexing="ij")
    zt = encode_base(enc, h, P, ch, jj.ravel(), tt.ravel(), hidx)
    zb = encode_branch(enc, h, P, ch, hidx)
    zt, zb = apply_white(zt, W, glob), apply_white(zb, W, glob)
    q = zt.shape[1] * zt.shape[2] * zt.shape[3]
    return ch, flat_cm(zt).reshape(JC, T1, q), flat_cm(zb).reshape(XBh[ch].shape[:4] + (q,))


# ----------------------------------------------------------------------------- hand designs
def objfields(Lobj):
    """Object view at block resolution: bilinear splat of each present object's mass to the 4 nearest block
    centres (periodic), and the mass-weighted offsets (x, y) from those centres in block units.
    Lobj (..., 144) -> (..., 3, 8, 8): [mass, dipole_x, dipole_y]."""
    S = Lobj.reshape(Lobj.shape[:-1] + (12, 12)).astype(np.float64)
    pres = S[..., 0] > 0.5
    m = np.where(pres, S[..., 1], 0.0)
    cx = (np.arctan2(S[..., 4], S[..., 3]) * b4.NPIX / (2 * np.pi)) % b4.NPIX
    cy = (np.arctan2(S[..., 6], S[..., 5]) * b4.NPIX / (2 * np.pi)) % b4.NPIX
    ux, uy = (cx - 7.5) / b4.BS, (cy - 7.5) / b4.BS
    ix0, iy0 = np.floor(ux).astype(int), np.floor(uy).astype(int)
    fx, fy = ux - ix0, uy - iy0
    out = np.zeros(Lobj.shape[:-1] + (3, b4.G, b4.G))
    flat = out.reshape(-1, 3, b4.G * b4.G)
    lead = int(np.prod(Lobj.shape[:-1]))
    rows = np.repeat(np.arange(lead), 12)
    for ddy in (0, 1):
        for ddx in (0, 1):
            w = (fx if ddx else 1 - fx) * (fy if ddy else 1 - fy)
            bx, by = (ix0 + ddx) % b4.G, (iy0 + ddy) % b4.G
            dxo, dyo = ux - (ix0 + ddx), uy - (iy0 + ddy)
            cell = (by * b4.G + bx).reshape(-1)
            wm = (w * m).reshape(-1)
            np.add.at(flat, (rows, 0, cell), wm)
            np.add.at(flat, (rows, 1, cell), wm * dxo.reshape(-1))
            np.add.at(flat, (rows, 2, cell), wm * dyo.reshape(-1))
    return flat.reshape(out.shape)


def tent_latent(frames):
    w = BN.tent_window()
    Wt = jnp.asarray(np.stack([w, w])[None], jnp.float32)              # (1, 2, 32, 32), raw units
    f = jax.jit(lambda x: BN.conv_win(x, Wt, 8))
    out = []
    for i in range(0, len(frames), ENC_CHUNK):
        out.append(np.asarray(f(jnp.asarray(np.asarray(frames[i:i + ENC_CHUNK]))), np.float64))
    return np.concatenate(out).reshape(len(frames), -1)              # (N, 64)


def hand_designs():
    for ch in b4.HALVES:
        Yt, YB = L1h[ch][:JC].astype(np.float64), L1Bh[ch].astype(np.float64)
        for k in b4.HAND:
            t1 = time.time()
            if k in ("mass", "chan", "view"):
                f = {"view": lambda Y: Y[..., :192], "chan": lambda Y: Y[..., :128],
                     "mass": lambda Y: Y[..., :64] + Y[..., 64:128]}[k]
                Zt, ZB = f(Yt), f(YB)
            elif k == "tent":
                Zt = tent_latent(Xh[ch][:JC].reshape((-1,) + Xh[ch].shape[2:])).reshape(JC, T1, 64)
                ZB = tent_latent(XBh[ch].reshape((-1,) + XBh[ch].shape[4:])).reshape(XBh[ch].shape[:4] + (64,))
            else:
                Ft, FB = objfields(Yt[..., 192:]), objfields(YB[..., 192:])
                sl = slice(0, 1) if k == "objmass" else slice(0, 3)
                Zt = Ft[..., sl, :, :].reshape(Ft.shape[:-3] + (-1,))
                ZB = FB[..., sl, :, :].reshape(FB.shape[:-3] + (-1,))
            c = Zt.shape[-1] // 64
            save_latent(f"hand_{k}", ch, Zt, ZB, (c, b4.G, b4.G), {"phi": f"hand_{k}", "kind": "hand", "cert": ch,
                                                                   "c": c, "seconds": time.time() - t1})
    log("hand designs queued", b4.HAND)


# ----------------------------------------------------------------------------- training
_TRAINERS = {}


def trainer(enc, h, obj, c):
    key_ = (enc, h, obj, c)
    if key_ in _TRAINERS:
        return _TRAINERS[key_]
    loss = BN.make_loss(enc, h, obj, c)
    fe, ft = BN.frames_needed(obj)
    B = (BATCH_U * (2 if c == 4 else 1)) if enc == "U" else BATCH
    lr, wd = LR[enc], (WD_U if enc == "U" else 0.0)
    n_steps = float(STEPS[enc])
    l2 = BN.l2_matrices(enc, None)

    def one_step(carry, _):
        P, M, V, it, key, hidx = carry
        key, kj, kt, kn = jax.random.split(key, 4)
        j = jax.random.randint(kj, (B,), 0, N_TR)
        t = jax.random.randint(kt, (B,), T_LO, T_HI + 1)
        xe = gather(hidx, j, t, fe)
        xt = gather(hidx, j, t, ft) if ft else xe[:0]
        g = jax.grad(loss)(P, xe, xt, kn)
        it = it + 1.0
        M = jax.tree_util.tree_map(lambda m, gg: 0.9 * m + 0.1 * gg, M, g)
        V = jax.tree_util.tree_map(lambda v, gg: 0.999 * v + 0.001 * gg * gg, V, g)
        c1, c2 = 1 - 0.9 ** it, 1 - 0.999 ** it
        lr_t = lr * (0.1 + 0.45 * (1 + jnp.cos(jnp.pi * jnp.minimum(it / n_steps, 1.0))))
        P = jax.tree_util.tree_map(lambda p, m, v: p - lr_t * (m / c1) / (jnp.sqrt(v / c2) + 1e-8), P, M, V)
        if wd > 0:
            P["enc"] = {k: (v * (1 - lr_t * wd) if k in l2 else v) for k, v in P["enc"].items()}
        return (P, M, V, it, key, hidx), None

    def chunk(P, M, V, it, key, hidx):
        (P, M, V, it, key, _), _ = jax.lax.scan(one_step, (P, M, V, it, key, hidx), None, length=CHUNK)
        return P, M, V, it, key

    nv = NV * (2 if (enc == "U" and c == 4) else 1)

    def val(P, hidx):
        j, t = jnp.asarray(VAL_J)[hidx, :nv], jnp.asarray(VAL_T)[hidx, :nv]
        xe = gather(hidx, j, t, fe)
        xt = gather(hidx, j, t, ft) if ft else xe[:0]
        return loss(P, xe, xt, jax.random.PRNGKey(999))

    out = (jax.jit(jax.vmap(chunk)), jax.jit(jax.vmap(val)), B, nv)
    _TRAINERS[key_] = out
    return out


def pick(tree, i):
    return jax.tree_util.tree_map(lambda a: a[i], tree)


def train_config(cid, name, enc, h, obj, c):
    t1 = time.time()
    steps = 0 if obj == "rand" else STEPS[enc]
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
    glob = enc == "U"
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
                "steps": steps, "batch": B, "lr": LR[enc], "wd": WD_U if enc == "U" else 0.0, "val_n": nv,
                "val_init": float(v_init[r]), "val_best": float(best[r]), "best_step": best_it[r],
                "val_hist": [(a, b[r]) for a, b in hist], "min_rel_eig_latent_cov": mre,
                "train_seconds_config": t_train, "chunk_seconds": t_chunks, "n_params_enc": int(sum(np.size(x) for x in jax.tree_util.tree_leaves(Pe)))}
        save_latent(phi, ch, Zt, ZB, (c, b4.G, b4.G), info)
        infos.append(info)
        if enc in ("L", "N") and c <= 2:
            np.savez_compressed(f"{WIN}/{phi}__fit{fh}.npz", W=np.asarray(Pe["W"], np.float32), sd=STAT[fh][1],
                                mu=STAT[fh][0], h=h, c=c, enc=enc, obj=obj)
    b4.jdump(infos, f"{TRN}/{name}.json")
    log(f"{name}: steps {steps}, val {np.round(v_init, 4).tolist()} -> {np.round(best, 4).tolist()} "
        f"(best at {best_it}), train {t_train:.1f}s (chunks {t_chunks}), total {time.time() - t1:.1f}s, {mem()}")


def main():
    hand_designs()
    todo = [(f"{nm}", "L", hh, "rand", cc) for nm, hh, cc in b4.RANDOM] + list(b4.configs())
    todo = [(nm, e, hh, o, cc) for nm, e, hh, o, cc in todo]
    dl = b4.deadline("train")
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
    b4.jdump({"skipped_by_deadline": skipped, "n_configs": len(todo), "seconds": time.time() - T0,
              "platform": {"backend": jax.default_backend(), "devices": [str(d) for d in jax.devices()]}},
             os.path.join(OUT, "train_done.json"))
    open(os.path.join(LAT, "DONE"), "w").close()
    log("done; skipped", skipped)


if __name__ == "__main__":
    try:
        main()
    finally:
        open(os.path.join(LAT, "DONE"), "w").close()
