"""snets -- slot encoders, readouts, heads and objectives of the round-5 study `slots` (JAX, float32; see s5.py).

One transducer for every encoder (no-learning and learned): "geometric slot attention with memory".
  tokens   P x P px patches of the raw field (2 x 128 x 128) on a (128/P)^2 torus grid. Fixed token statistics
           (matter, channel-1 matter, circular and second moments) make every slot moment exact at pixel level for
           token-level masks. Learned token features: patch MLP + one 3 x 3 token-neighbourhood layer + absolute
           position code (Fourier features of the token centre).
  slots    K = 12; state = content s_k (D numbers) + position p_k on the torus + the previous centroid. Tick 0:
           fixed start (learned content vectors, positions on a fixed 4 x 3 lattice), N_INIT + N_IT iterations;
           later ticks: N_IT iterations from the state carried over from the previous tick (the memory).
  tick     learned encoders only: before a carried tick the slots exchange pairwise messages (content, mass,
           relative position; zero-initialised output), so a slot can know that another slot sits on the same blob.
  step     logits[n, k] = key_n . query_k / sqrt(D) - softplus(beta_k) d^2(x_n, p_k) / (2 sigma^2) + c_k;
           attention = softmax over slots; p_k <- matter-weighted circular mean of its tokens; s_k <- GRU of the
           attention- and matter-weighted mean of the token values (+ the slot's mass and size) + residual MLP.
           With the content term, beta's and c's slot dependence switched off this is soft k-means with bandwidth
           sigma: the no-learning baseline `km` IS this transducer with no parameters, and the learned geometric
           encoders start exactly there (zero-initialised query, beta and c weights).
  readout  'mom': the moments of the matter under each final mask in the tracker's 12-number layout (soft presence
           g = sigmoid((m - m_min) / tau), mass, channel-1 fraction, g * centroid on the torus (4), g * rg, g * q1,
           g * q2, g * velocity (2); velocity = centroid displacement over the last tick). Only the masks are learned.
           'code': DC = 6 learned numbers per slot, a linear map of the normalised slot content.
Objectives (s5.py): 'rec' decodes the token patches from the readout (mixture over slots); 'set' / 'self' predict
the slots' own future at h = 1, 4, 16 from 2 lags with a permutation-equivariant head ('set': pairwise slot-slot
messages; 'self': one shared rule on the slot's own past), the error measured in the metric of the joint covariance
of the 72 slot numbers (running estimate mixed with the batch estimate, relative ridge): redundant, constant or
collapsed slots make that covariance singular and their noise is amplified, so they cannot lower the loss.
"""
from __future__ import annotations

import math

import jax
import jax.numpy as jnp
import numpy as np

import s5

F32 = jnp.float32
K, NF, DC = s5.K, s5.NF, s5.DC
NPIX = s5.NPIX
D, C, HID = 32, 32, 64                       # slot content width, token feature width, head width
N_IT, N_INIT = 2, 4                          # iterations per tick, extra iterations at a fresh start
E = NPIX / (2 * math.pi)
TAU_M = 2.0                                  # softness of the presence gate (matter units)
SCALE12 = np.array([1, 200, 1, E, E, E, E, 10, 1, 1, 2, 2], np.float32)     # network units of the 12 numbers
XSCALE = 0.2                                 # raw field scale (about one channel sd)
COV_MIX, COV_EPS = 0.9, 1e-3                 # weight of the running joint covariance, relative ridge
NFREQ = (1, 2, 4, 8)


def gelu(x):
    return jax.nn.gelu(x)


def normal(key, shape, fan_in, gain=1.0):
    return (jax.random.normal(key, shape, F32) * (gain / math.sqrt(fan_in))).astype(F32)


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


def lnorm(x):
    m = x.mean(-1, keepdims=True)
    v = ((x - m) ** 2).mean(-1, keepdims=True)
    return (x - m) / jnp.sqrt(v + 1e-5)


def mi(d):
    """Minimum-image difference on the torus of size NPIX."""
    return (d + NPIX / 2) % NPIX - NPIX / 2


# ----------------------------------------------------------------------------- fixed geometry
def geometry(P):
    """Token grid for patch size P: centres (N, 2) [y, x], position code (N, 16), lattice start (K, 2)."""
    G = NPIX // P
    c = (np.arange(G) + 0.5) * P - 0.5
    yy, xx = np.meshgrid(c, c, indexing="ij")
    cen = np.stack([yy.ravel(), xx.ravel()], 1).astype(np.float32)
    code = []
    for f in NFREQ:
        for a in (cen[:, 0], cen[:, 1]):
            code += [np.cos(2 * np.pi * f * a / NPIX), np.sin(2 * np.pi * f * a / NPIX)]
    code = np.stack(code, 1).astype(np.float32)
    lat = np.array([[(j + 0.5) * NPIX / 3, ((i + 0.5) * NPIX / 4 + (j % 2) * NPIX / 8) % NPIX]
                    for j in range(3) for i in range(4)], np.float32)
    return {"G": G, "N": G * G, "cen": cen, "code": code, "lat": lat}


def token_stats(x, P):
    """x (F, 2, 128, 128) raw -> (F, N, 11): matter m, channel-1 matter, sum S sin/cos(theta_y), sum S sin/cos
    (theta_x), first moments about the token centre (my, mx), second moments about it (syy, sxx, sxy)."""
    Fr = x.shape[0]
    G = NPIX // P
    S = x[:, 0] + x[:, 1]
    pix = jnp.arange(NPIX, dtype=F32)
    th = 2 * jnp.pi * pix / NPIX
    off = pix - ((jnp.floor(pix / P) + 0.5) * P - 0.5)                    # offset from the token centre

    def tok(a):                                                            # (F, 128, 128) -> (F, N)
        return a.reshape(Fr, G, P, G, P).sum((2, 4)).reshape(Fr, G * G)
    oy, ox = off[:, None], off[None, :]
    cols = [tok(S), tok(x[:, 1]), tok(S * jnp.sin(th)[:, None]), tok(S * jnp.cos(th)[:, None]),
            tok(S * jnp.sin(th)[None, :]), tok(S * jnp.cos(th)[None, :]), tok(S * oy), tok(S * ox),
            tok(S * oy * oy), tok(S * ox * ox), tok(S * oy * ox)]
    return jnp.stack(cols, -1)


def patches(x, P):
    """(F, 2, 128, 128) -> (F, N, 2 P P): each token's raw content in network units."""
    Fr = x.shape[0]
    G = NPIX // P
    return (x.reshape(Fr, 2, G, P, G, P).transpose(0, 2, 4, 1, 3, 5).reshape(Fr, G * G, 2 * P * P) / XSCALE).astype(F32)


# ----------------------------------------------------------------------------- parameters
def default_cfg(**kw):
    cfg = dict(P=4, readout="mom", learned=True, geo=True, sigma=6.0, prior=False, freeze_p=False, mem=True,
               stopcarry=False, n_it=N_IT, n_init=N_INIT)
    cfg.update(kw)
    return cfg


def init_enc(cfg, key):
    """Encoder parameters ({} for the no-learning encoders)."""
    if not cfg["learned"]:
        return {}
    P = cfg["P"]
    k = jax.random.split(key, 13)
    geo = cfg["geo"]
    Pm = {"W1": normal(k[0], (2 * P * P, C), 2 * P * P, math.sqrt(2.0)), "b1": jnp.zeros((C,), F32),
          "W2": normal(k[1], (9 * C, C), 9 * C, math.sqrt(2.0)), "b2": jnp.zeros((C,), F32),
          "Wp": normal(k[2], (4 * len(NFREQ), C), 4 * len(NFREQ)),
          "Wk": normal(k[3], (C, D), C), "Wv": normal(k[4], (C, D), C),
          "Wq": jnp.zeros((D, D), F32) if geo else normal(k[5], (D, D), D),
          "wb": jnp.zeros((D,), F32), "wc": jnp.zeros((D,), F32),
          "Wi": normal(k[6], (D + 2, 3 * D), D + 2), "Wh": normal(k[7], (D, 3 * D), D),
          "bi": jnp.zeros((3 * D,), F32), "bh": jnp.zeros((3 * D,), F32),
          "mlp": mlp_init(k[8], [D, 2 * D, D], zero_last=True),
          "ia": mlp_init(k[11], [2 * (D + 1) + 3, HID // 2, HID // 2]),
          "ia_out": mlp_init(jax.random.fold_in(k[11], 1), [HID // 2, D], zero_last=True),
          "s0": jax.random.normal(k[9], (K, D), F32)}
    if cfg["readout"] == "code":
        Pm["Wr"] = normal(k[10], (D, DC), D)
        Pm["br"] = jnp.zeros((DC,), F32)
    return Pm


# ----------------------------------------------------------------------------- the transducer
def make_encoder(cfg):
    """Returns the pure functions of one encoder configuration:
    tokens(Pm, x (F, 2, 128, 128)) -> dict of per-frame token arrays
    start(Pm, tk0) -> state at a fresh start (after the extra iterations on the first frame)
    tick(Pm, st, tk) -> st', out; out = feat (K, 12), z (K, DC) (zeros for 'mom'), attn (N, K), cen (K, 2) = the
                           ungated mask centroid (cy, cx)
    state = (s (K, D), p (K, 2), pc (K, 2) previous centroid, mk (K,) previous mass)."""
    P = cfg["P"]
    geom = geometry(P)
    G, N = geom["G"], geom["N"]
    cen, code, lat = jnp.asarray(geom["cen"]), jnp.asarray(geom["code"]), jnp.asarray(geom["lat"])
    learned, geo, readout = cfg["learned"], cfg["geo"], cfg["readout"]
    sig2 = 2.0 * cfg["sigma"] ** 2
    beta0 = math.log(math.e - 1.0)                                         # softplus(beta0) = 1

    def tokens(Pm, x):
        ts = token_stats(x, P)
        out = {"ts": ts}
        if learned:
            f = gelu(patches(x, P) @ Pm["W1"] + Pm["b1"])                  # (F, N, C)
            fg = f.reshape(-1, G, G, C)
            nb = jnp.concatenate([jnp.roll(fg, (-dy, -dx), (1, 2)) for dy in (-1, 0, 1) for dx in (-1, 0, 1)], -1)
            f = f + gelu(nb.reshape(-1, N, 9 * C) @ Pm["W2"] + Pm["b2"])
            f = lnorm(f + code @ Pm["Wp"])
            out["k"], out["v"] = f @ Pm["Wk"], f @ Pm["Wv"]
        return out

    def logits(Pm, s, p, mk, tk):
        d2 = mi(cen[:, None, 0] - p[None, :, 0]) ** 2 + mi(cen[:, None, 1] - p[None, :, 1]) ** 2     # (N, K)
        if not learned:
            lg = -d2 / sig2
        else:
            sn = lnorm(s)
            lg = (tk["k"] @ (sn @ Pm["Wq"]).T) / math.sqrt(D) + (sn @ Pm["wc"])[None, :]
            if geo:
                lg = lg - jax.nn.softplus(beta0 + sn @ Pm["wb"])[None, :] * d2 / sig2
        if cfg["prior"]:
            lg = lg + jnp.log(mk + 1.0)[None, :]
        return lg

    def slot_moments(a, ts, p_prev):
        """a (N, K) masks, ts (N, 11) -> R (K, 11) raw sums, centroid (K, 2) (p_prev where a slot holds no matter)."""
        R = a.T @ ts
        ok = R[:, 0] > 1e-3
        cy = jnp.where(ok, (jnp.arctan2(jnp.where(ok, R[:, 2], 0.0), jnp.where(ok, R[:, 3], 1.0)) * E) % NPIX, p_prev[:, 0])
        cx = jnp.where(ok, (jnp.arctan2(jnp.where(ok, R[:, 4], 0.0), jnp.where(ok, R[:, 5], 1.0)) * E) % NPIX, p_prev[:, 1])
        return R, jnp.stack([cy, cx], 1), ok

    def shape_moments(a, ts, R, c):
        """Second moments about the centroid c (K, 2): rg, q1, q2 (K,) as the tracker defines them."""
        dy, dx = mi(cen[:, None, 0] - c[None, :, 0]), mi(cen[:, None, 1] - c[None, :, 1])            # (N, K)
        m, my, mx = ts[:, 0:1], ts[:, 6:7], ts[:, 7:8]
        ms = jnp.maximum(R[:, 0], 1e-3)
        syy = (a * (ts[:, 8:9] + 2 * dy * my + dy * dy * m)).sum(0) / ms
        sxx = (a * (ts[:, 9:10] + 2 * dx * mx + dx * dx * m)).sum(0) / ms
        sxy = (a * (ts[:, 10:11] + dx * my + dy * mx + dx * dy * m)).sum(0) / ms
        tr = jnp.maximum(sxx + syy, 1e-6)
        return jnp.sqrt(tr), (sxx - syy) / tr, 2 * sxy / tr

    def iterate(Pm, s, p, mk, tk):
        ts = tk["ts"]
        a = jax.nn.softmax(logits(Pm, s, p, mk, tk), axis=1)                                       # (N, K)
        R, c, ok = slot_moments(a, ts, p)
        p_new = p if cfg["freeze_p"] else c
        if learned:
            w = a * (ts[:, 0:1] + 0.02 * ts[:, 0].mean() + 1e-6)
            w = w / w.sum(0, keepdims=True)
            rg, _, _ = shape_moments(a, ts, R, c)
            upd = jnp.concatenate([w.T @ tk["v"], jnp.log1p(R[:, 0:1] / 50.0), jnp.where(ok, rg, 0.0)[:, None] / 10.0], 1)
            gi, gh = upd @ Pm["Wi"] + Pm["bi"], s @ Pm["Wh"] + Pm["bh"]
            r = jax.nn.sigmoid(gi[:, :D] + gh[:, :D])
            z = jax.nn.sigmoid(gi[:, D:2 * D] + gh[:, D:2 * D])
            n = jnp.tanh(gi[:, 2 * D:] + r * gh[:, 2 * D:])
            s = (1 - z) * n + z * s
            s = s + mlp_apply(Pm["mlp"], lnorm(s))
        return s, p_new, R[:, 0]

    def interact(Pm, s, p, mk):
        """Slots see each other once per tick, before they look at the new frame: pairwise messages from the other
        slots' content, mass and relative position (zero-initialised output: no effect at the start of training)."""
        e = jnp.concatenate([lnorm(s), jnp.log1p(mk / 50.0)[:, None]], 1)                             # (K, D + 1)
        dy, dx = mi(p[None, :, 0] - p[:, None, 0]) / 16.0, mi(p[None, :, 1] - p[:, None, 1]) / 16.0    # [k, j]
        pair = jnp.concatenate([jnp.broadcast_to(e[:, None, :], (K, K, D + 1)), jnp.broadcast_to(e[None, :, :], (K, K, D + 1)),
                                jnp.stack([dy, dx, jnp.sqrt(dy * dy + dx * dx + 1e-6)], -1)], -1)
        msg = gelu(mlp_apply(Pm["ia"], pair)) * (1.0 - jnp.eye(K, dtype=F32))[..., None]
        return s + mlp_apply(Pm["ia_out"], msg.sum(1) / (K - 1))

    def readout_fn(Pm, s, p, pc, mk, tk, fresh):
        ts = tk["ts"]
        a = jax.nn.softmax(logits(Pm, s, p, mk, tk), axis=1)
        R, c, ok = slot_moments(a, ts, p)
        rg, q1, q2 = shape_moments(a, ts, R, c)
        m = R[:, 0]
        g = jax.nn.sigmoid((m - s5.M_MIN) / TAU_M)
        vy = jnp.where(fresh, 0.0, mi(c[:, 0] - pc[:, 0]))
        vx = jnp.where(fresh, 0.0, mi(c[:, 1] - pc[:, 1]))
        thy, thx = c[:, 0] / E, c[:, 1] / E
        feat = jnp.stack([g, m, R[:, 1] / jnp.maximum(m, 1e-3), g * E * jnp.cos(thx), g * E * jnp.sin(thx),
                          g * E * jnp.cos(thy), g * E * jnp.sin(thy), g * rg, g * q1, g * q2, g * vx, g * vy], 1)
        if learned and readout == "code":
            z = lnorm(s) @ Pm["Wr"] + Pm["br"]
        else:
            z = jnp.zeros((K, DC), F32)
        return feat, z, a, c, m

    def init_state(Pm):
        s0 = Pm["s0"] if learned else jnp.zeros((K, D), F32)
        return (s0, lat, lat, jnp.zeros((K,), F32))

    def run_tick(Pm, st, tk, n_iter, fresh):
        s, p, pc, mk = st
        if learned and not fresh:
            s = interact(Pm, s, p, mk)
        for _ in range(n_iter):
            s, p, mk = iterate(Pm, s, p, mk, tk)
        feat, z, a, c, m = readout_fn(Pm, s, p, pc, mk, tk, fresh)
        return (s, p if cfg["freeze_p"] else c, c, m), {"feat": feat, "z": z, "attn": a, "cen": c}

    def tick(Pm, st, tk, fresh):
        """fresh (scalar bool): this frame starts the transducer (state ignored, extra iterations)."""
        if not cfg["mem"]:
            return run_tick(Pm, init_state(Pm), tk, cfg["n_init"] + cfg["n_it"], True)
        st_f, out_f = run_tick(Pm, init_state(Pm), tk, cfg["n_init"] + cfg["n_it"], True)
        if cfg["stopcarry"]:
            st = jax.tree_util.tree_map(jax.lax.stop_gradient, st)
        st_c, out_c = run_tick(Pm, st, tk, cfg["n_it"], False)
        sel = lambda a, b: jnp.where(fresh, a, b)
        return jax.tree_util.tree_map(sel, st_f, st_c), jax.tree_util.tree_map(sel, out_f, out_c)

    def tick_carry(Pm, st, tk):
        """A later tick of a running transducer (no fresh-start branch; used when encoding)."""
        if not cfg["mem"]:
            return run_tick(Pm, init_state(Pm), tk, cfg["n_init"] + cfg["n_it"], True)
        return run_tick(Pm, st, tk, cfg["n_it"], False)

    def tick_fresh(Pm, tk):
        return run_tick(Pm, init_state(Pm), tk, cfg["n_init"] + cfg["n_it"], True)

    return {"tokens": tokens, "tick": tick, "tick_carry": tick_carry, "tick_fresh": tick_fresh,
            "init_state": init_state, "geom": geom}


def encode_window(enc, Pm, x, st, fresh):
    """One trajectory window. x (L, 2, 128, 128), st = carried state, fresh (scalar bool): the first frame starts
    the transducer. Returns outs (feat (L, K, 12), z (L, K, DC), attn (L, N, K)) and the states after every tick."""
    tk = enc["tokens"](Pm, x)
    first = jax.tree_util.tree_map(lambda a: a[0], tk)
    st1, o1 = enc["tick"](Pm, st, first, fresh)

    def body(s, t):
        s, o = enc["tick_carry"](Pm, s, t)
        return s, (o, s)
    rest = jax.tree_util.tree_map(lambda a: a[1:], tk)
    _, (outs, sts) = jax.lax.scan(body, st1, rest)
    cat = lambda a, b: jnp.concatenate([a[None], b], 0)
    return jax.tree_util.tree_map(cat, o1, outs), jax.tree_util.tree_map(cat, st1, sts)


def loss_vector(cfg, outs):
    """The numbers the objectives act on, in network units: (..., K, DC)."""
    if cfg["readout"] == "code":
        return outs["z"]
    f = outs["feat"] / jnp.asarray(SCALE12)
    return f[..., jnp.asarray(s5.MP6)]


def certified(cfg, outs):
    """The certified readout of Phi: (..., K * 12) for 'mom' (tracker layout), (..., K * DC) for 'code'."""
    y = outs["z"] if cfg["readout"] == "code" else outs["feat"]
    return y.reshape(y.shape[:-2] + (-1,))


# ----------------------------------------------------------------------------- heads
def init_head(cfg, obj, key):
    k = jax.random.split(key, 6)
    nh = len(s5.HTR)
    if obj == "rec":
        P = cfg["P"]
        d_in = 12 + 5 if cfg["readout"] == "mom" else DC + 4 * len(NFREQ)
        return {"dec": mlp_init(k[0], [d_in, HID, HID, 2 * P * P + 1], zero_last=True)}
    if obj == "self":
        return {"A": jnp.zeros((2 * DC, nh * DC), F32), "f": mlp_init(k[0], [2 * DC, HID, HID, nh * DC], zero_last=True)}
    if obj == "set":
        return {"A": jnp.zeros((2 * DC, nh * DC), F32), "e": mlp_init(k[0], [2 * DC, HID]),
                "psi": mlp_init(k[1], [2 * HID, HID, HID]),
                "f": mlp_init(k[2], [2 * HID, HID, nh * DC], zero_last=True)}
    raise ValueError(obj)


def predict(obj, H, z0, zm):
    """z0, zm (..., K, DC): the slots now and one tick earlier -> predictions (..., K, nh, DC)."""
    nh = len(s5.HTR)
    x = jnp.concatenate([z0, zm], -1)
    if obj == "self":
        d = x @ H["A"] + mlp_apply(H["f"], x)
    else:
        e = gelu(mlp_apply(H["e"], x))                                                  # (..., K, HID)
        pair = jnp.concatenate([jnp.broadcast_to(e[..., :, None, :], e.shape[:-1] + (K, HID)),
                                jnp.broadcast_to(e[..., None, :, :], e.shape[:-1] + (K, HID))], -1)
        msg = gelu(mlp_apply(H["psi"], pair))                                           # (..., K, K, HID)
        off = 1.0 - jnp.eye(K, dtype=F32)
        m = (msg * off[..., None]).sum(-2) / (K - 1)
        d = x @ H["A"] + mlp_apply(H["f"], jnp.concatenate([e, m], -1))
    return z0[..., None, :] + d.reshape(d.shape[:-1] + (nh, DC))


def decode(cfg, geom, H, outs_t):
    """Mixture decoder on the token grid. outs_t: feat (F, K, 12), z (F, K, DC) -> patches (F, N, 2 P P).
    'mom': each slot's 12 numbers plus the token's offset from the slot's centroid (read off those numbers:
    offsets / 16 px and three Gaussian bumps of widths 4, 8, 16 px); 'code': the slot's code plus the token's
    absolute position code. Output layer zero-initialised (the loss starts at 1)."""
    cen, code = jnp.asarray(geom["cen"]), jnp.asarray(geom["code"])
    N = geom["N"]
    if cfg["readout"] == "mom":
        f = outs_t["feat"]
        n12 = f / jnp.asarray(SCALE12)
        cx = (jnp.arctan2(f[..., 4], f[..., 3] + 1e-6) * E) % NPIX
        cy = (jnp.arctan2(f[..., 6], f[..., 5] + 1e-6) * E) % NPIX
        dy = mi(cen[None, None, :, 0] - cy[..., None])                                   # (F, K, N), px
        dx = mi(cen[None, None, :, 1] - cx[..., None])
        d2 = dy * dy + dx * dx
        inp = jnp.concatenate([jnp.broadcast_to(n12[:, :, None, :], n12.shape[:2] + (N, 12)),
                               jnp.stack([dy / 16.0, dx / 16.0, jnp.exp(-d2 / 32.0), jnp.exp(-d2 / 128.0),
                                          jnp.exp(-d2 / 512.0)], -1)], -1)
    else:
        z = outs_t["z"]
        inp = jnp.concatenate([jnp.broadcast_to(z[:, :, None, :], z.shape[:2] + (N, DC)),
                               jnp.broadcast_to(code[None, None], z.shape[:2] + code.shape)], -1)
    o = mlp_apply(H["dec"], inp)                                                         # (F, K, N, 2PP + 1)
    w = jax.nn.softmax(o[..., -1], axis=1)
    return (w[..., None] * o[..., :-1]).sum(1)


# ----------------------------------------------------------------------------- objectives
def joint_whitener(Zf, cov_state, mix_w=COV_MIX):
    """Zf (M, K * DC) -> (mean, Cholesky factor of the mixed joint covariance, batch moments).
    cov_state = (sum of batch means, sum of batch second moments, weight): the running estimate (no gradient),
    mixed mix_w : 1 - mix_w with the current batch (which carries the gradient; mix_w = 1: running estimate only)."""
    q = Zf.shape[1]
    m1_b = Zf.mean(0)
    m2_b = Zf.T @ Zf / Zf.shape[0]
    s1, s2, wt = cov_state
    has = wt > 0
    wsafe = jnp.where(has, wt, 1.0)
    mix = jnp.where(has, mix_w, 0.0)
    mu = mix * s1 / wsafe + (1 - mix) * m1_b
    Cm = mix * s2 / wsafe + (1 - mix) * m2_b - jnp.outer(mu, mu)
    Cm = Cm + (COV_EPS * jnp.trace(Cm) / q + 1e-6) * jnp.eye(q, dtype=F32)
    return mu, jnp.linalg.cholesky(Cm), (jax.lax.stop_gradient(m1_b), jax.lax.stop_gradient(m2_b))


def closure_loss(obj, H, z, cov_state, anchors, mix_w=COV_MIX):
    """z (B, Lw, K, DC) slots along each window; anchors: tick indices i with i - 1 >= 0 and i + 16 < Lw.
    Returns the loss (mean squared whitened error over horizons, anchors and the 72 numbers; 1 = the mean
    predictor), the per-horizon losses and the batch statistics for the running covariance."""
    B, Lw = z.shape[:2]
    mu, Lc, stats = joint_whitener(z.reshape(B * Lw, K * DC), cov_state, mix_w)
    ia = jnp.asarray(anchors)
    pred = predict(obj, H, z[:, ia], z[:, ia - 1])                                        # (B, A, K, nh, DC)
    per_h = []
    for hi, h in enumerate(s5.HTR):
        e = (pred[:, :, :, hi, :] - z[:, ia + h]).reshape(-1, K * DC)
        ew = jax.scipy.linalg.solve_triangular(Lc, e.T, lower=True)
        per_h.append(jnp.mean(ew ** 2))
    per_h = jnp.stack(per_h)
    return per_h.mean(), per_h, stats


def recon_loss(cfg, geom, H, outs, x, ticks):
    """outs along a batch of windows (B, Lw, ...), x (B, Lw, 2, 128, 128); decode the ticks in `ticks`."""
    it = jnp.asarray(ticks)
    B = x.shape[0]
    sub = {k: outs[k][:, it].reshape((B * len(ticks),) + outs[k].shape[2:]) for k in ("feat", "z")}
    tgt = patches(x[:, it].reshape((B * len(ticks),) + x.shape[2:]), cfg["P"])
    rec = decode(cfg, geom, H, sub)
    return jnp.mean((rec - tgt) ** 2) / jnp.mean(tgt ** 2)
