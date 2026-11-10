"""strain -- fit the slot encoders of the round-5 study `slots` on the GPU and encode the certification data.

usage: python -B strain.py          (S5_SIZE=tiny|dev: CPU code path / CPU pilot)
Reference and no-learning Phi first: the tracker's object view (trk), block views (hand_mass, hand_chan), soft
k-means and the frozen grid (s5.fixed_configs). Then every learned config (s5.learned_configs), four replicas at
once (jax.vmap): fit half A or B x seed 0 or 1. Training is truncated backpropagation through time with persistent
slot memory: every training trajectory keeps a pointer and its slot state; a step takes B trajectories, encodes the
window [p, p + Lw) from the stored state (a fresh start when p = 0), takes the loss on it, stores the state after
L ticks (no gradient) and advances the pointer by L. Adam, gradient clipping, cosine decay; the best parameters on
the held-out trajectories of the fit half (encoded from tick 0, as at certification; checkpoints after the first
quarter of the steps) are frozen. Objective 'sup' (capacity control) imitates the tracker's segmentation: the loss
is 2 - recall - purity of the soft masks against the tracker's label map (best slot per object, best object per
slot, matter-weighted). '_ws' configs start from the 'sup' encoder (frozen for the first eighth of the steps while
the new head warms up) and continue with their own objective. At every validation the training history also
records the recall and purity of the soft masks against the tracker's label map on the held-out trajectories
('val_trk_recall_purity'; a diagnostic for every objective, the loss itself for 'sup'). Time limits: no new config
starts with less than S5_CFG_MIN_S seconds left before the training deadline, and one config's training loop stops
after S5_CFG_MAX_S seconds ('cut_by_deadline' is then true for its Phi, as for a cut at the training deadline).
Each frozen Phi is run as a transducer over the OTHER half's certification trajectories (301 ticks from a fresh
start; the branches continue from the state at their test tick) -> $S5_WORK/lat/<phi>__cert<h>.npz with
  Zt (JC, T+1, q), ZB (JC, nT, R, TB, q)   the certified readout (q = 144 moment layout / 72 code)
  MM (JC, T+1, K, 14)                      moments of the matter under each mask (tracker layout) + the ungated
                                           mask centroid (cy, cx); for every encoder
  OS, OH (JC, T+1, K, 13)                  matter shared by slot k and tracker label s (0 = untracked), soft / hard masks
plus a .ready marker for the CPU certification workers (scert.py). Moment-layout Phi also get the 6-number
sub-view <phi>@mp6. Pairs of hard segmentations on the same frames (seed 0 vs seed 1 of one fit half; each learned
Phi vs km_s6) go to $S5_WORK/pair/.
Objective values under one protocol ($S5_OUT/objval/<name>.json): for every slot Phi (tracker included) the three
heads are trained from scratch on the FROZEN readout of the fit half (set, self: the 6 loss numbers per slot, same
joint-covariance metric; rec: the mixture decoder on the readout) and evaluated on its held-out trajectories. This
says which view each objective prefers, separately from what gradient descent on the encoder finds.
Device data are passed to every jitted function as ARGUMENTS and compiled functions are released between configs
(round-4 lesson: JAX 0.12 embeds closed-over device arrays as constants). No device array may exceed 2^31 - 1
elements: level 0, branches and label maps are one array per half, validation encodes one trajectory at a time,
and fits() checks the large planned shapes (the largest go to train_done.json).
A replica whose training is cut by the deadline before the first checkpoint is certified with the weights at the
cut ('checkpoint': 'last'), never with its initial weights.
"""
import gc
import json
import os
import time
import traceback

import numpy as np

import s5

import jax  # noqa: E402

jax.config.update("jax_enable_x64", False)
import jax.numpy as jnp  # noqa: E402

import snets as SN  # noqa: E402

T0 = time.time()
DATA = s5.work_dir("data")
LAT = s5.work_dir("lat")
PAIR = s5.work_dir("pair")
OUT = s5.out_dir()
TRN = s5.out_dir("train")
PRM = s5.out_dir("params")
MSK = s5.out_dir("masks")
OBV = s5.out_dir("objval")
HI = {h: i for i, h in enumerate(s5.HALVES)}
OTHER = {"A": "B", "B": "A"}
REPS = [("A", 0), ("A", 1), ("B", 0), ("B", 1)]
if os.environ.get("S5_REPS"):                # dev only: a subset of the replicas, e.g. "A0,B0"
    REPS = [(r[0], int(r[1])) for r in os.environ["S5_REPS"].split(",")]
K, NPIX = s5.K, s5.NPIX
LWIN = 16
if s5.SIZE == "tiny":
    STEPS, CHUNK, BATCH, ENC_J, OV_STEPS = 4, 2, 2, 2, 4
elif s5.SIZE == "dev":
    STEPS, CHUNK, BATCH, ENC_J, OV_STEPS = int(os.environ.get("S5_STEPS", 60)), 10, 4, 2, int(os.environ.get("S5_OV_STEPS", 20))
elif s5.SIZE == "pilot":
    STEPS, CHUNK, BATCH, ENC_J, OV_STEPS = int(os.environ.get("S5_STEPS", 800)), 100, 32, 8, int(os.environ.get("S5_OV_STEPS", 500))
else:
    STEPS, CHUNK, BATCH, ENC_J, OV_STEPS = int(os.environ.get("S5_STEPS", 4000)), 100, 32, 4, int(os.environ.get("S5_OV_STEPS", 1500))
LR, CLIP, COV_DECAY = 1e-3, 1.0, 0.95
CFG_MIN_S = float(os.environ.get("S5_CFG_MIN_S", 0))          # no new config with less than this left before the training deadline
CFG_MAX_S = float(os.environ.get("S5_CFG_MAX_S", "inf"))      # one config's training loop stops after this many seconds
SNAP_T = (20, 24, 28) if s5.T < 120 else (100, 104, 108)


def log(*a):
    s5.progress(f"[strain {time.time() - T0:7.1f}s] " + " ".join(str(x) for x in a))


def mem():
    try:
        st = jax.devices()[0].memory_stats() or {}
        return (f"{st.get('peak_bytes_in_use', 0) / 2**30:.1f} GB peak, "
                f"{st.get('bytes_in_use', 0) / 2**30:.1f} GB in use")
    except Exception:
        return "n/a"


_JIT = {}


def release():
    """Drop every compiled function and JAX's caches, then collect (between configs)."""
    _JIT.clear()
    gc.collect()
    jax.clear_caches()


# ----------------------------------------------------------------------------- data
Xh = {h: np.load(f"{DATA}/X_{h}.npy", mmap_mode="r") for h in s5.HALVES}
XBh = {h: np.load(f"{DATA}/XB_{h}.npy", mmap_mode="r") for h in s5.HALVES}
MAPh = {h: np.load(f"{DATA}/MAP_{h}.npy", mmap_mode="r") for h in s5.HALVES}
TABh = {h: np.load(f"{DATA}/TAB_{h}.npy") for h in s5.HALVES}
TABBh = {h: np.load(f"{DATA}/TABB_{h}.npy") for h in s5.HALVES}
BLKh = {h: np.load(f"{DATA}/BLK_{h}.npy") for h in s5.HALVES}
BLKBh = {h: np.load(f"{DATA}/BLKB_{h}.npy") for h in s5.HALVES}
J, T1 = Xh["A"].shape[:2]
JC, nT, R_BR, TB = XBh["A"].shape[:4]
MAX_ELEMS = 2 ** 31 - 1                     # no device array may hold more elements (XLA GPU kernels index with int32)
PLANNED = {}


def fits(name, shape):
    """Record a (planned or real) device array shape and refuse one above MAX_ELEMS."""
    n = int(np.prod([int(x) for x in shape], dtype=np.float64))
    PLANNED[name] = (tuple(int(x) for x in shape), n)
    if n > MAX_ELEMS:
        raise RuntimeError(f"{name}: shape {tuple(shape)} has {n:.3e} elements, above 2^31")
    return n


def to_device(name, a):
    fits(name, a.shape)
    return jax.device_put(a)


# One device array per half (tuples indexed by HI[half]); a replica picks its half with hsel.
Xd = tuple(to_device(f"X_{h}", np.asarray(Xh[h])) for h in s5.HALVES)                   # (J, T+1, 2, 128, 128) each
XBd = tuple(to_device(f"XB_{h}", np.asarray(XBh[h]).reshape((JC * nT * R_BR, TB, 2, NPIX, NPIX))) for h in s5.HALVES)
MAPd = tuple(to_device(f"MAP_{h}", np.asarray(MAPh[h])) for h in s5.HALVES)             # (J, T+1, 128, 128) int8 each
jax.block_until_ready((Xd, XBd, MAPd))
N_TR = J - s5.N_VAL
TEST = np.asarray(s5.TEST)
log("data on device", Xd[0].shape, XBd[0].shape, MAPd[0].shape, "per half; train trajectories per half", N_TR, mem())


def hsel(A, hidx, f):
    """A = (half A's array, half B's array), hidx = the replica's half (0 / 1, traced), f indexes one half's array."""
    return jnp.where(hidx == 0, f(A[0]), f(A[1]))


def tracker_tokens(x, lab, P):
    """x (..., 2, 128, 128), lab (..., 128, 128) tracker labels (slot + 1, 0 = none) -> (..., N, 13): the matter
    of every tracker label in every token."""
    G = NPIX // P
    S = x[..., 0, :, :] + x[..., 1, :, :]
    lead = S.shape[:-2]
    return jnp.stack([(S * (lab == s)).reshape(lead + (G, P, G, P)).sum((-3, -1)).reshape(lead + (G * G,))
                      for s in range(K + 1)], -1)


# ----------------------------------------------------------------------------- encoding (frozen Phi)
def _encoders(cfg):
    """Jitted transducer passes for one encoder configuration (data passed as arguments)."""
    key_ = ("enc", json.dumps(cfg, sort_keys=True))
    if key_ in _JIT:
        return _JIT[key_]
    enc = SN.make_encoder(cfg)
    P = cfg["P"]

    def fresh(Pm, x):
        return jax.vmap(lambda xx: SN.encode_window(enc, Pm, xx, enc["init_state"](Pm), True))(x)

    def base(Pm, X, MAP, js):                                                            # X, MAP: one half's arrays
        x = X[js]                                                                        # (n, T+1, 2, 128, 128)
        outs, sts = fresh(Pm, x)
        Mtok = tracker_tokens(x, MAP[js], P)                                             # (n, T+1, N, 13)
        attn = outs["attn"]                                                              # (n, T+1, N, K)
        lab = jnp.argmax(attn, -1)
        hard = jax.nn.one_hot(lab, K, dtype=jnp.float32)
        OS = jnp.einsum("jtnk,jtns->jtks", attn, Mtok)
        OH = jnp.einsum("jtnk,jtns->jtks", hard, Mtok)
        st_test = jax.tree_util.tree_map(lambda a: a[:, jnp.asarray(TEST)], sts)        # states at the test ticks
        mm = jnp.concatenate([outs["feat"], outs["cen"]], -1)                            # (n, T+1, K, 14)
        return SN.certified(cfg, outs), mm, OS, OH, lab.astype(jnp.int8), st_test

    def branch(Pm, XB, idx, st):
        x = XB[idx]                                                                      # (n, TB, 2, 128, 128)

        def one(xx, s):
            tk = enc["tokens"](Pm, xx)

            def body(c, t):
                c, o = enc["tick_carry"](Pm, c, t)
                return c, SN.certified(cfg, o)
            return jax.lax.scan(body, s, tk)[1]
        return jax.vmap(one)(x, st)

    def feats(Pm, X, js):
        outs, _ = fresh(Pm, X[js])
        return SN.loss_vector(cfg, outs), outs["feat"]

    _JIT[key_] = (jax.jit(base), jax.jit(branch), jax.jit(feats))
    return _JIT[key_]


def encode_cert(cfg, Pm, ch):
    """Phi on half ch's certification data. Returns Zt, ZB, MM, OS, OH (numpy) and the hard labels (JC, T+1, N)."""
    fb, fbr, _ = _encoders(cfg)
    dh = HI[ch]
    nj = min(ENC_J, JC) if cfg["P"] > 1 else 1
    Ntok = (NPIX // cfg["P"]) ** 2
    fits(f"encode tokens P={cfg['P']}", (nj, T1, Ntok, max(SN.C, 13)))
    fits(f"encode branch tokens P={cfg['P']}", (nj * nT * R_BR, TB, Ntok, max(SN.C, 13)))
    Zt, MM, OS, OH, LAB, ZB = [], [], [], [], [], []
    for j0 in range(0, JC, nj):
        js = np.arange(j0, min(j0 + nj, JC))
        y, mm, os_, oh, lab, st = fb(Pm, Xd[dh], MAPd[dh], jnp.asarray(js))
        Zt.append(np.asarray(y)), MM.append(np.asarray(mm)), OS.append(np.asarray(os_)), OH.append(np.asarray(oh))
        LAB.append(np.asarray(lab))
        # branches of these trajectories: (j, i, r) flat index = (j * nT + i) * R + r; state of (j, i) repeated R times
        idx = (js[:, None, None] * nT + np.arange(nT)[None, :, None]) * R_BR + np.arange(R_BR)[None, None, :]
        stb = jax.tree_util.tree_map(lambda a: jnp.repeat(a.reshape((len(js) * nT,) + a.shape[2:]), R_BR, 0), st)
        zb = fbr(Pm, XBd[dh], jnp.asarray(idx.ravel()), stb)
        ZB.append(np.asarray(zb).reshape(len(js), nT, R_BR, TB, -1))
    cat = lambda a: np.concatenate(a, 0)
    return cat(Zt), cat(ZB), cat(MM), cat(OS), cat(OH), cat(LAB)


def encode_fit(cfg, Pm, h):
    """The loss numbers (J, T+1, K, 6) and the 12-number mask moments (J, T+1, K, 12) of Phi on ALL trajectories of
    half h (fresh start at tick 0), for the objective values."""
    ff = _encoders(cfg)[2]
    nj = min(ENC_J, J) if cfg["P"] > 1 else 1
    Z, F = [], []
    for j0 in range(0, J, nj):
        z, f = ff(Pm, Xd[HI[h]], jnp.asarray(np.arange(j0, min(j0 + nj, J))))
        Z.append(np.asarray(z)), F.append(np.asarray(f))
    return np.concatenate(Z), np.concatenate(F)


def save_latent(stem, ch, Zt, ZB, meta, **extra):
    path = f"{LAT}/{stem}__cert{ch}.npz"
    np.savez(path + ".tmp.npz", Zt=Zt.astype(np.float32), ZB=ZB.astype(np.float32),
             meta=json.dumps(s5.jsonable(meta)), **{k: v.astype(np.float32) for k, v in extra.items()})
    os.replace(path + ".tmp.npz", path)
    open(path + ".ready", "w").close()


def sub6(Z):
    return Z.reshape(Z.shape[:-1] + (K, 12))[..., list(s5.MP6)].reshape(Z.shape[:-1] + (K * 6,))


def save_slot_phi(stem, ch, cfg, meta, Zt, ZB, MM, OS, OH):
    lay = "trk" if cfg["readout"] == "mom" else "code"
    save_latent(stem, ch, Zt, ZB, dict(meta, layout=lay, d=Zt.shape[-1] // K), MM=MM, OS=OS, OH=OH)
    if lay == "trk":
        save_latent(stem + "@mp6", ch, sub6(Zt), sub6(ZB), dict(meta, layout="sub", d=6, of=stem))


def pair_tables(labA, labB, ch, P):
    """Matter-weighted contingency (JC, T+1, K, K) of two hard token segmentations of half ch's base frames."""
    G = NPIX // P
    out = np.zeros((JC, T1, K, K), np.float32)
    for j in range(JC):
        x = np.asarray(Xh[ch][j], np.float32)
        m = (x[:, 0] + x[:, 1]).reshape(T1, G, P, G, P).sum((2, 4)).reshape(T1, G * G)
        flat = labA[j].astype(np.int64) * K + labB[j].astype(np.int64)
        for t in range(T1):
            out[j, t] = np.bincount(flat[t], weights=m[t], minlength=K * K).reshape(K, K)
    return out


def snapshot(stem, ch, lab, P):
    """Hard token labels of trajectory 0 at a few ticks (for the segmentation figure)."""
    np.savez_compressed(f"{MSK}/{stem}__cert{ch}.npz", lab=lab[0][list(SNAP_T)].astype(np.int8), ticks=np.asarray(SNAP_T), P=P)


# ----------------------------------------------------------------------------- objective values (frozen readout)
def objval_trainer(obj, readout):
    key_ = ("ov", obj, readout)
    if key_ in _JIT:
        return _JIT[key_]
    cfg = SN.default_cfg(readout=readout)
    geom = SN.geometry(cfg["P"])
    L = LWIN
    Lw = L + 1 + max(s5.HTR)
    anchors = np.arange(1, L + 1)
    rt = jnp.asarray(tuple(range(3, L, 4)))
    n_steps = float(OV_STEPS)
    q = K * s5.DC

    def rec_loss(H, z, f, x):
        n = x.shape[0] * x.shape[1]
        r = SN.decode(cfg, geom, H, {"feat": f.reshape((n,) + f.shape[2:]), "z": z.reshape((n,) + z.shape[2:])})
        tgt = SN.patches(x.reshape((n,) + x.shape[2:]), cfg["P"])
        return jnp.mean((r - tgt) ** 2) / jnp.mean(tgt ** 2)

    def loss(H, z, f, x, cov):
        if obj == "rec":
            return rec_loss(H, z, f, x), ((jnp.zeros((q,)), jnp.zeros((q, q))), jnp.zeros((len(s5.HTR),)))
        l, per_h, stats, _ = SN.closure_loss(obj, H, z, cov, anchors)
        return l, (stats, per_h)

    def one_step(carry, Z, F, X):
        H, M, V, it, key, hidx, cov = carry
        key, kj, kt = jax.random.split(key, 3)
        j = jax.random.randint(kj, (BATCH,), 0, N_TR)
        t = jax.random.randint(kt, (BATCH,), 0, T1 - Lw + 1)
        ar = t[:, None] + (rt[None, :] if obj == "rec" else jnp.arange(Lw)[None, :])
        z, f = Z[j[:, None], ar], F[j[:, None], ar]
        x = hsel(X, hidx, lambda a: a[j[:, None], ar]) if obj == "rec" else jnp.zeros((1, 1, 2, NPIX, NPIX))
        (l, (stats, per_h)), g = jax.value_and_grad(loss, has_aux=True)(H, z, f, x, cov)
        gn = jnp.sqrt(sum(jnp.sum(a * a) for a in jax.tree_util.tree_leaves(g)))
        ok = jnp.isfinite(l) & jnp.isfinite(gn)
        sc = jnp.where(ok, jnp.minimum(1.0, CLIP / (gn + 1e-12)), 0.0)
        g = jax.tree_util.tree_map(lambda a: jnp.where(ok, a, 0.0) * sc, g)
        it = it + 1.0
        M = jax.tree_util.tree_map(lambda m, gg: 0.9 * m + 0.1 * gg, M, g)
        V = jax.tree_util.tree_map(lambda v, gg: 0.999 * v + 0.001 * gg * gg, V, g)
        c1, c2 = 1 - 0.9 ** it, 1 - 0.999 ** it
        lr_t = LR * (0.1 + 0.45 * (1 + jnp.cos(jnp.pi * jnp.minimum(it / n_steps, 1.0))))
        H = jax.tree_util.tree_map(lambda p, m, v: p - lr_t * (m / c1) / (jnp.sqrt(v / c2) + 1e-8), H, M, V)
        s1, s2, wt = cov
        cov = (jnp.where(ok, COV_DECAY * s1 + stats[0], s1), jnp.where(ok, COV_DECAY * s2 + stats[1], s2),
               jnp.where(ok, COV_DECAY * wt + 1.0, wt))
        return (H, M, V, it, key, hidx, cov), l

    def chunk(carry, Z, F, X):
        return jax.lax.scan(lambda c, _: one_step(c, Z, F, X), carry, None, length=CHUNK)

    v_anch = np.arange(1, T1 - max(s5.HTR))
    v_rec = jnp.asarray(tuple(range(4, T1, 8))[:24])

    def val(H, hidx, cov, Z, F, X):
        if obj == "rec":
            return (rec_loss(H, Z[N_TR:J][:, v_rec], F[N_TR:J][:, v_rec], hsel(X, hidx, lambda a: a[N_TR:J][:, v_rec])),
                    jnp.zeros((len(s5.HTR),)), jnp.zeros(()))
        l, per_h, _, pen = SN.closure_loss(obj, H, Z[N_TR:J], cov, v_anch, 1.0)
        return l, per_h, pen

    def init(key):
        return SN.init_head(cfg, obj, key)

    _JIT[key_] = (jax.jit(jax.vmap(chunk, in_axes=(0, 0, 0, None))), jax.jit(jax.vmap(val, in_axes=(0, 0, 0, 0, 0, None))),
                  jax.vmap(init))
    return _JIT[key_]


def objective_values(name, readout, Z, F, reps, objs=("set", "self", "rec")):
    """Z (nr, J, T+1, K, 6), F (nr, J, T+1, K, 12): frozen readouts of nr replicas on their fit halves reps[i][0]."""
    t1 = time.time()
    nr = len(reps)
    Zd, Fd = jnp.asarray(Z, jnp.float32), jnp.asarray(F, jnp.float32)
    hidx = jnp.asarray([HI[fh] for fh, _ in reps])
    res = {"name": name, "reps": [f"{fh}{s}" for fh, s in reps], "steps": OV_STEPS, "batch": BATCH}
    q = K * s5.DC
    for oi, obj in enumerate(objs):
        if time.time() > s5.deadline("train"):
            res[obj] = None
            continue
        chunk_v, val_v, init_v = objval_trainer(obj, readout)
        keys = jnp.stack([jax.random.PRNGKey(900001 + 131 * oi + 17 * HI[fh] + 1009 * s) for fh, s in reps])
        H = init_v(keys)
        z0 = jax.tree_util.tree_map(jnp.zeros_like, H)
        carry = (H, z0, z0, jnp.zeros((nr,)), keys, hidx, (jnp.zeros((nr, q)), jnp.zeros((nr, q, q)), jnp.zeros((nr,))))
        done, tr = 0, None
        while done < OV_STEPS:
            carry, l = chunk_v(carry, Zd, Fd, Xd)
            done += CHUNK
            tr = np.asarray(l).mean(1)
        v, vh, vp = val_v(carry[0], hidx, carry[6], Zd, Fd, Xd)
        res[obj] = {"val": np.asarray(v).tolist(), "val_h": np.asarray(vh).tolist(), "train_last_chunk": tr.tolist()}
        if obj != "rec":           # the dead-direction term of this readout (snets.closure_loss); val + dead_pen = the
            res[obj]["dead_pen"] = np.asarray(vp).tolist()        # value under the guarded objective ('_dg' configs)
    res["seconds"] = time.time() - t1
    s5.jdump(res, f"{OBV}/{name}.json")
    return res


def ov_text(res):
    return ", ".join(f"{o} {np.round(res[o]['val'], 4).tolist()}" for o in ("set", "self", "rec") if res.get(o))


# ----------------------------------------------------------------------------- reference and no-learning Phi
LAB_KM = {}
FULL_REPS = [(h, s) for h in s5.HALVES for s in (0, 1)]


def references():
    for ch in s5.HALVES:
        tab, tabb = TABh[ch][:JC, :, :, :12], TABBh[ch][..., :12]
        Zt, ZB = tab.reshape(JC, T1, K * 12), tabb.reshape(JC, nT, R_BR, TB, K * 12)
        meta = {"phi": "trk", "kind": "tracker", "cert": ch}
        save_latent("trk", ch, Zt, ZB, dict(meta, layout="trk", d=12))
        save_latent("trk@mp6", ch, sub6(Zt), sub6(ZB), dict(meta, layout="sub", d=6, of="trk"))
        blk, blkb = BLKh[ch].astype(np.float64), BLKBh[ch].astype(np.float64)
        for k in s5.HAND:
            f = {"chan": lambda Y: Y[..., :128], "mass": lambda Y: Y[..., :64] + Y[..., 64:128]}[k]
            save_latent(f"hand_{k}", ch, f(blk), f(blkb), {"phi": f"hand_{k}", "kind": "hand", "cert": ch,
                                                           "layout": "grid", "gshape": [1 if k == "mass" else 2, 8, 8]})
        # the tracker's own map (for the figure) and the matter field
        x = np.asarray(Xh[ch][0][list(SNAP_T)], np.float32)
        np.savez_compressed(f"{MSK}/_frames__cert{ch}.npz", S=(x[:, 0] + x[:, 1]), map=np.asarray(MAPh[ch][0][list(SNAP_T)]),
                            ticks=np.asarray(SNAP_T), table=TABh[ch][0][list(SNAP_T)])
    log("references queued: trk, trk@mp6,", ", ".join(f"hand_{k}" for k in s5.HAND))
    fixed = {}
    for name, kind, kw in s5.fixed_configs():
        t1 = time.time()
        cfg = SN.default_cfg(learned=False, n_it=3, n_init=10, freeze_p=(kind == "grid"), **kw)
        for ch in s5.HALVES:
            Zt, ZB, MM, OS, OH, lab = encode_cert(cfg, {}, ch)
            save_slot_phi(name, ch, cfg, {"phi": name, "kind": kind, "cert": ch, "cfg": cfg}, Zt, ZB, MM, OS, OH)
            snapshot(name, ch, lab, cfg["P"])
            if name == "km_s6":
                LAB_KM[ch] = lab
        if cfg["P"] == 4:
            fixed[name] = {h: encode_fit(cfg, {}, h) for h in s5.HALVES}
        release()
        log(f"{name}: encoded both halves in {time.time() - t1:.1f}s, {mem()}")
    # objective values of the reference views (frozen readouts; the tracker's table in the same network units)
    F = {h: TABh[h][..., :12] for h in s5.HALVES}
    Zr = {h: (F[h] / SN.SCALE12)[..., list(s5.MP6)] for h in s5.HALVES}
    res = objective_values("trk", "mom", np.stack([Zr[h] for h, _ in FULL_REPS]), np.stack([F[h] for h, _ in FULL_REPS]), FULL_REPS)
    log(f"objective values trk: {ov_text(res)} ({res['seconds']:.1f}s)")
    for name, d in fixed.items():
        res = objective_values(name, "mom", np.stack([d[h][0] for h, _ in FULL_REPS]), np.stack([d[h][1] for h, _ in FULL_REPS]), FULL_REPS)
        log(f"objective values {name}: {ov_text(res)} ({res['seconds']:.1f}s)")
    release()


# ----------------------------------------------------------------------------- training
def sup_loss(attn, Mtok):
    """attn (B, L, N, K) soft masks, Mtok (B, L, N, 13) tracker matter per token: 2 - recall - purity, where recall
    is the matter of each tracked object held by its best slot and purity the matter of each slot that belongs to
    its best object (both matter-weighted over the frame; untracked matter ignored)."""
    rec, pur = sup_parts(attn, Mtok)
    return 2.0 - rec - pur


def sup_parts(attn, Mtok):
    """(recall, purity) of the soft masks against the tracker's label map, means over frames (see sup_loss)."""
    O = jnp.einsum("blnk,blns->blks", attn, Mtok[..., 1:])                               # (B, L, K, 12)
    tot = O.sum((-2, -1)) + 1e-6
    return jnp.mean(O.max(-2).sum(-1) / tot), jnp.mean(O.max(-1).sum(-1) / tot)


def trainer(cfg, obj, warm, dead=False):
    enc = SN.make_encoder(cfg)
    geom = enc["geom"]
    L = LWIN
    Lw = L if obj in ("rec", "sup") else L + 1 + max(s5.HTR)
    anchors = np.arange(1, L + 1)
    rec_ticks = tuple(range(3, L, 4))
    max_p = ((T1 - Lw) // L) * L
    n_steps = float(STEPS)
    q = K * s5.DC
    nostat = (jnp.zeros((q,)), jnp.zeros((q, q)))

    def loss(Pall, x, lab, st, fresh, cov):
        outs, sts = jax.vmap(lambda xx, s, f: SN.encode_window(enc, Pall["enc"], xx, s, f))(x, st, fresh)
        new_st = jax.tree_util.tree_map(lambda a: jax.lax.stop_gradient(a[:, L - 1]), sts)
        if obj == "rec":
            return SN.recon_loss(cfg, geom, Pall["head"], outs, x, rec_ticks), (new_st, nostat, jnp.zeros((len(s5.HTR),)))
        if obj == "sup":
            return sup_loss(outs["attn"], tracker_tokens(x, lab, cfg["P"])), (new_st, nostat, jnp.zeros((len(s5.HTR),)))
        l, per_h, stats, _ = SN.closure_loss(obj, Pall["head"], SN.loss_vector(cfg, outs), cov, anchors, dead=dead)
        return l, (new_st, stats, per_h)

    def one_step(carry, X, MAP):
        Pall, M, V, it, key, hidx, memst, ptr, fresh, cov = carry
        key, kp = jax.random.split(key)
        idx = jax.random.permutation(kp, N_TR)[:BATCH]
        p0 = ptr[idx]
        ar = p0[:, None] + jnp.arange(Lw)[None, :]
        x = hsel(X, hidx, lambda a: a[idx[:, None], ar])
        lab = hsel(MAP, hidx, lambda a: a[idx[:, None], ar]) if obj == "sup" else jnp.zeros((1,), jnp.int8)
        st = jax.tree_util.tree_map(lambda a: a[idx], memst)
        (l, (new_st, stats, per_h)), g = jax.value_and_grad(loss, has_aux=True)(Pall, x, lab, st, fresh[idx], cov)
        gn = jnp.sqrt(sum(jnp.sum(a * a) for a in jax.tree_util.tree_leaves(g)))
        ok = jnp.isfinite(l) & jnp.isfinite(gn)
        sc = jnp.where(ok, jnp.minimum(1.0, CLIP / (gn + 1e-12)), 0.0)
        g = jax.tree_util.tree_map(lambda a: jnp.where(ok, a, 0.0) * sc, g)
        it = it + 1.0
        M = jax.tree_util.tree_map(lambda m, gg: 0.9 * m + 0.1 * gg, M, g)
        V = jax.tree_util.tree_map(lambda v, gg: 0.999 * v + 0.001 * gg * gg, V, g)
        c1, c2 = 1 - 0.9 ** it, 1 - 0.999 ** it
        lr_t = LR * (0.1 + 0.45 * (1 + jnp.cos(jnp.pi * jnp.minimum(it / n_steps, 1.0))))
        new = jax.tree_util.tree_map(lambda p, m, v: p - lr_t * (m / c1) / (jnp.sqrt(v / c2) + 1e-8), Pall, M, V)
        enc_on = it > warm                                # warm start: the encoder waits while the new head warms up
        new["enc"] = jax.tree_util.tree_map(lambda a, b: jnp.where(enc_on, a, b), new["enc"], Pall["enc"])
        Pall = new
        memst = jax.tree_util.tree_map(lambda a, n: a.at[idx].set(jnp.where(ok, n, a[idx])), memst, new_st)
        nxt = p0 + L
        wrap = nxt > max_p
        ptr = ptr.at[idx].set(jnp.where(wrap, 0, nxt))
        fresh = fresh.at[idx].set(wrap | ~ok)
        s1, s2, wt = cov
        cov = (jnp.where(ok, COV_DECAY * s1 + stats[0], s1), jnp.where(ok, COV_DECAY * s2 + stats[1], s2),
               jnp.where(ok, COV_DECAY * wt + 1.0, wt))
        return (Pall, M, V, it, key, hidx, memst, ptr, fresh, cov), (l, per_h, gn, ok)

    def chunk(carry, X, MAP):
        return jax.lax.scan(lambda c, _: one_step(c, X, MAP), carry, None, length=CHUNK)

    v_anch = np.arange(1, T1 - max(s5.HTR))
    v_rec = tuple(range(4, T1, 8))[:24]
    v_sup = jnp.asarray(tuple(range(4, T1, 4)))

    def val(Pall, hidx, cov, X, MAP):
        x = hsel(X, hidx, lambda a: a[N_TR:J])
        # one validation trajectory at a time (lax.map): no token array of N_VAL x (T + 1) frames x replicas
        outs = jax.lax.map(lambda xx: SN.encode_window(enc, Pall["enc"], xx, enc["init_state"](Pall["enc"]), True)[0], x)
        zh, z0 = jnp.zeros((len(s5.HTR),)), jnp.zeros(())
        # diagnostic for every objective: recall and purity of the soft masks against the tracker's label map
        lab = hsel(MAP, hidx, lambda a: a[N_TR:J][:, v_sup])
        agr = jnp.stack(sup_parts(outs["attn"][:, v_sup], tracker_tokens(x[:, v_sup], lab, cfg["P"])))
        if obj == "rec":
            return SN.recon_loss(cfg, geom, Pall["head"], outs, x, v_rec), zh, z0, agr
        if obj == "sup":
            return 2.0 - agr[0] - agr[1], zh, z0, agr
        l, per_h, _, pen = SN.closure_loss(obj, Pall["head"], SN.loss_vector(cfg, outs), cov, v_anch, 1.0, dead=dead)
        return l, per_h, pen, agr

    nr, Ntok = len(REPS), geom["N"]
    fits(f"train tokens {obj}", (nr, BATCH, Lw, Ntok, max(SN.C, 2 * cfg["P"] ** 2)))
    fits(f"val tokens {obj}", (nr, T1, Ntok, max(SN.C, 2 * cfg["P"] ** 2)))
    fits(f"val attention {obj}", (nr, J - N_TR, T1, Ntok, K))
    if obj == "rec":
        fits("train decoder hidden", (nr, BATCH * len(rec_ticks), K, Ntok, SN.HID))
        fits("val decoder hidden", (nr, (J - N_TR) * len(v_rec), K, Ntok, SN.HID))
    if obj == "sup":
        fits("train tracker tokens", (nr, BATCH, Lw, Ntok, K + 1))
    fits("val tracker tokens", (nr, J - N_TR, int(v_sup.shape[0]), Ntok, K + 1))
    chunk_v = jax.jit(jax.vmap(chunk, in_axes=(0, None, None)))
    val_v = jax.jit(jax.vmap(val, in_axes=(0, 0, 0, None, None)))
    return chunk_v, val_v, enc, max_p, L, Lw


def pick(tree, i):
    return jax.tree_util.tree_map(lambda a: a[i], tree)


def init_carry(cfg, obj, cid, enc, max_p, L, enc_init=None):
    keys = jnp.stack([jax.random.PRNGKey(100003 * cid + 1009 * s + 17 * HI[fh] + 5) for fh, s in REPS])

    def one(k):
        k1, k2 = jax.random.split(k)
        return {"enc": SN.init_enc(cfg, k1), "head": {} if obj == "sup" else SN.init_head(cfg, obj, k2)}
    Pall = jax.vmap(one)(keys)
    if enc_init is not None:
        Pall["enc"] = enc_init
    nr = len(REPS)
    z = lambda t: jax.tree_util.tree_map(jnp.zeros_like, t)
    st0 = enc["init_state"](pick(Pall["enc"], 0))
    memst = jax.tree_util.tree_map(lambda a: jnp.zeros((nr, N_TR) + a.shape, a.dtype), st0)
    rng = np.random.default_rng(555 + cid)
    ptr = jnp.asarray(rng.integers(0, max_p // L + 1, (nr, N_TR)) * L, jnp.int32)
    q = K * s5.DC
    cov = (jnp.zeros((nr, q)), jnp.zeros((nr, q, q)), jnp.zeros((nr,)))
    skeys = jnp.stack([jax.random.PRNGKey(7 + 31 * cid + 1000 * s + 3 * HI[fh]) for fh, s in REPS])
    hidx = jnp.asarray([HI[fh] for fh, _ in REPS])
    return (Pall, z(Pall), z(Pall), jnp.zeros((nr,)), skeys, hidx, memst, ptr, jnp.ones((nr, N_TR), bool), cov)


def flat_params(Pm):
    leaves, _ = jax.tree_util.tree_flatten(Pm)
    return {f"leaf{i}": np.asarray(a, np.float32) for i, a in enumerate(leaves)}


BEST_ENC = {}


def train_config(cid, c):
    t1 = time.time()
    name, obj = c["name"], c["obj"]
    cfg = SN.default_cfg(P=c["P"], readout=c["readout"], geo=c["geo"], stopcarry=c["stopcarry"], mem=c["mem"])
    enc_init = None
    if c.get("init_from"):
        if c["init_from"] not in BEST_ENC:
            raise RuntimeError(f"{name}: warm start needs {c['init_from']}, which was not trained")
        enc_init = BEST_ENC[c["init_from"]]
    warm = float(STEPS // 8) if enc_init is not None else 0.0
    dead = bool(c.get("dead"))
    chunk_v, val_v, enc, max_p, L, Lw = trainer(cfg, obj, warm, dead)
    carry = init_carry(cfg, obj, cid, enc, max_p, L, enc_init)
    nr = len(REPS)
    v, vh, vp, va = val_v(carry[0], carry[5], carry[9], Xd, MAPd)
    v_init = np.asarray(v)                  # set / self: no running covariance yet, so this value is not comparable
    best = np.full(nr, np.inf)
    bestP, best_it = carry[0], [0] * nr
    hist = [{"step": 0, "val": v_init.tolist(), "val_h": np.asarray(vh).tolist(), "val_trk_recall_purity": np.asarray(va).tolist()}]
    done, tch, bad = 0, [], 0
    while done < STEPS:
        tc = time.time()
        carry, (l, per_h, gn, ok) = chunk_v(carry, Xd, MAPd)
        done += CHUNK
        v, vh, vp, va = val_v(carry[0], carry[5], carry[9], Xd, MAPd)
        v = np.asarray(v)
        tch.append(time.time() - tc)
        l, ok = np.asarray(l), np.asarray(ok)
        bad += int((~ok).sum())
        hist.append({"step": done, "train": np.nanmean(np.where(ok, l, np.nan), 1).tolist(),
                     "train_h": np.asarray(per_h).mean(1).tolist(), "gnorm": np.asarray(gn).mean(1).tolist(),
                     "val": v.tolist(), "val_h": np.asarray(vh).tolist(), "val_dead_pen": np.asarray(vp).tolist(),
                     "val_trk_recall_purity": np.asarray(va).tolist(), "skipped": int((~ok).sum())})
        if len(tch) <= 2 or done % (10 * CHUNK) == 0:
            log(f"{name}: step {done}, chunk {tch[-1]:.1f}s, train {np.round(hist[-1]['train'], 4).tolist()}, "
                f"val {np.round(v, 4).tolist()}, tracker recall+purity {np.round(np.asarray(va).sum(1), 3).tolist()}, "
                f"skipped {hist[-1]['skipped']}")
        better = np.isfinite(v) & (v < best) & (done >= STEPS // 4)
        for r in np.flatnonzero(better):
            best_it[r] = done
        bm = jnp.asarray(better)
        bestP = jax.tree_util.tree_map(lambda b, p: jnp.where(bm.reshape((-1,) + (1,) * (p.ndim - 1)), p, b), bestP, carry[0])
        best = np.where(better, v, best)
        if time.time() > s5.deadline("train"):
            log(f"{name}: training deadline reached at step {done}")
            break
        if done < STEPS and time.time() - t1 > CFG_MAX_S:
            log(f"{name}: the config's own time limit ({CFG_MAX_S:.0f}s) reached at step {done}")
            break
    t_train = time.time() - t1
    # A replica without a checkpoint (training cut before STEPS // 4, or no finite validation value after it) must
    # not be certified with its INITIAL weights: it takes the weights at the cut if their validation value is
    # finite ('last'), otherwise it is dropped ('none').
    cut = done < STEPS
    ckpt = ["best"] * nr
    for r in range(nr):
        if best_it[r] == 0:
            ckpt[r] = "last" if np.isfinite(v[r]) else "none"
            if ckpt[r] == "last":
                best[r], best_it[r] = float(v[r]), done
    lm = jnp.asarray([c == "last" for c in ckpt])
    bestP = jax.tree_util.tree_map(lambda b, p: jnp.where(lm.reshape((-1,) + (1,) * (p.ndim - 1)), p, b), bestP, carry[0])
    del carry
    if any(c != "best" for c in ckpt):
        log(f"{name}: checkpoints {ckpt} (cut by the deadline: {cut})")
    if "none" not in ckpt:
        BEST_ENC[name] = bestP["enc"]
    infos, labs, ZF, reps_ok = [], {}, [], []
    for r, (fh, s) in enumerate(REPS):
        if ckpt[r] == "none":
            log(f"{name}_s{s} (fit {fh}): no finite validation value, not certified")
            continue
        reps_ok.append((fh, s))
        Pe = pick(bestP["enc"], r)
        ch = OTHER[fh]
        Zt, ZB, MM, OS, OH, lab = encode_cert(cfg, Pe, ch)
        ZF.append(encode_fit(cfg, Pe, fh))
        phi = f"{name}_s{s}"
        dist = {}
        if cfg["geo"]:
            dist = {"Wq_rms": float(jnp.sqrt(jnp.mean(Pe["Wq"] ** 2))), "wb_rms": float(jnp.sqrt(jnp.mean(Pe["wb"] ** 2))),
                    "wc_rms": float(jnp.sqrt(jnp.mean(Pe["wc"] ** 2)))}
        info = {"phi": phi, "config": name, "kind": "learned", "readout": c["readout"], "obj": obj, "seed": s, "fit": fh,
                "cert": ch, "cfg": cfg, "init_from": c.get("init_from"), "warm_steps": warm, "dead_guard": dead, "steps": done, "batch": BATCH,
                "L": L, "Lw": Lw, "lr": LR, "clip": CLIP,
                "val_init": float(v_init[r]), "val_best": float(best[r]), "best_step": best_it[r],
                "checkpoint": ckpt[r], "cut_by_deadline": bool(cut), "steps_planned": STEPS,
                "skipped_steps_all_replicas": bad, "train_seconds_config": t_train,
                "chunk_seconds": {"first_incl_compile": tch[0], "rest_mean": float(np.mean(tch[1:])) if len(tch) > 1 else None},
                "moved_from_kmeans": dist,
                "n_params_enc": int(sum(np.size(x) for x in jax.tree_util.tree_leaves(Pe)))}
        save_slot_phi(phi, ch, cfg, info, Zt, ZB, MM, OS, OH)
        snapshot(phi, ch, lab, cfg["P"])
        np.savez_compressed(f"{PRM}/{phi}__fit{fh}.npz", **flat_params(Pe))
        labs[(fh, s)] = lab
        if ch in LAB_KM and cfg["P"] == 4:
            np.savez_compressed(f"{PAIR}/{phi}__vs_km_s6__cert{ch}.npz", C=pair_tables(lab, LAB_KM[ch], ch, 4))
        infos.append(info)
    for fh in s5.HALVES:                           # seed 0 vs seed 1, fitted on the same half, same certification frames
        if (fh, 0) not in labs or (fh, 1) not in labs:
            continue
        np.savez_compressed(f"{PAIR}/{name}_s0__vs_{name}_s1__cert{OTHER[fh]}.npz",
                            C=pair_tables(labs[(fh, 0)], labs[(fh, 1)], OTHER[fh], cfg["P"]))
    s5.jdump({"infos": infos, "hist": hist, "checkpoints": ckpt, "cut_by_deadline": bool(cut)}, f"{TRN}/{name}.json")
    log(f"{name}: steps {done}, val {np.round(v_init, 4).tolist()} -> {np.round(best, 4).tolist()} (best at {best_it}), "
        f"skipped {bad}, train {t_train:.1f}s (chunk {np.mean(tch[1:]) if len(tch) > 1 else tch[0]:.1f}s), "
        f"total {time.time() - t1:.1f}s, {mem()}")
    release()
    if "none" in ckpt:
        raise RuntimeError(f"{name}: replicas without a finite validation value: {ckpt}")
    res = objective_values(name, c["readout"], np.stack([z for z, _ in ZF]), np.stack([f for _, f in ZF]), reps_ok)
    log(f"objective values {name}: {ov_text(res)} ({res['seconds']:.1f}s)")


def main():
    references()
    todo = s5.learned_configs()
    dl = s5.deadline("train")
    skipped = []
    for cid, c in enumerate(todo):
        if time.time() + CFG_MIN_S > dl:
            skipped.append(c["name"])
            continue
        try:
            train_config(cid, c)
        except Exception as exc:  # one config failing must not stop the grid
            log(f"{c['name']} FAILED: {exc!r}")
            with open(os.path.join(OUT, "train_errors.txt"), "a") as f:
                f.write(f"{c['name']}\n{traceback.format_exc()}\n")
            del exc
        release()
    s5.jdump({"skipped_by_deadline": skipped, "n_configs": len(todo), "seconds": time.time() - T0, "steps": STEPS,
              "ov_steps": OV_STEPS, "batch": BATCH, "enc_j": ENC_J,
              "largest_device_arrays": {k: {"shape": list(v[0]), "elements": v[1]} for k, v in
                                        sorted(PLANNED.items(), key=lambda kv: -kv[1][1])[:8]},
              "max_elements_allowed": MAX_ELEMS,
              "platform": {"backend": jax.default_backend(), "devices": [str(d) for d in jax.devices()],
                           "jax": jax.__version__, "x64": bool(jax.config.jax_enable_x64)}},
             os.path.join(OUT, "train_done.json"))
    log("done; skipped", skipped)


if __name__ == "__main__":
    try:
        main()
    finally:
        open(os.path.join(LAT, "DONE"), "w").close()
