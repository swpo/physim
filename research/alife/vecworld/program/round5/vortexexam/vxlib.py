"""vxlib -- the fed-vortex exam pilot (round 5, study vortexexam, track 2): world runner and level-1/2 pipeline.

World: track1/vortex_world (vortex_jax: c53's fed vortices with heredity as a JAX Level; stirring channel with
exact nats at sigma_a = 0.005; level 1 = vortex list from vw.objects.BlobTracker on (|om| (1 - f_b), |om| f_b);
level 2 = (N, s_b)). Nothing there or in vw is changed; this module wraps it.

What is new here
  * per-member hidden parameters: every entry of vortex_jax.THETA can differ per member, and the mutation
    interval is a parameter too, declared PER UNIT AREA: `mut128` = time between mutation events per 128 x 128
    px of box (default 50), so a box of H x W px mutates every mut128 * 128^2 / (H W) time units (64^2: 200).
    The native step is vortex_jax.make_native_step with its own labelling and mutation switched off; the
    labelling and the mutation are applied before it by `pre` below with the same rules (labelling first, then
    the mutation; same uniform, same raster-order pick, same disk). At the default parameters one tick equals
    vortex_jax.make_level(cfg).step (checked in check_lib.py).
  * batching for the GPU: members are a leading axis; the 250 native steps of a tick run in one fori_loop over
    the whole batch (vmap of the native step), and the mutation branch is behind one batch-level lax.cond, so
    its cumulative sum is only paid at steps where some member mutates. Large constants (the stirring basis)
    are passed to the jitted functions as arguments (JAX 0.12 would otherwise compile them in).
  * level-1 summaries (numpy): permutation-invariant statistics of the vortex list per tick, a block raster of
    the list (mass and kind-b mass per 16-px block) as the scored level-1 view, and level 2 = (N, s_b).

Units: one tick = 250 native steps = 5 time units. Labelling at t = 300 (tick 60).
"""
from __future__ import annotations

import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
PROG = os.path.dirname(os.path.dirname(HERE))
VEC = os.path.dirname(PROG)
VW1 = os.path.join(VEC, "vw1")
VWORLD = os.path.join(PROG, "track1", "vortex_world")
if VW1 not in sys.path:
    sys.path.insert(0, VW1)
import vw  # noqa: E402  (first, so that vortex_world/_paths cannot shadow this copy)

if VWORLD not in sys.path:
    sys.path.insert(1, VWORLD)
import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402
from jax import lax  # noqa: E402

import vortex_jax as VJ  # noqa: E402
import vortex_world as VW  # noqa: E402
from vw.core import Noise  # noqa: E402
from vw.objects import NF  # noqa: E402

assert os.path.realpath(os.path.dirname(vw.__file__)) == os.path.realpath(os.path.join(VW1, "vw")), vw.__file__

LAB_T = 300.0
LAB_TICK = 60
MUT_R = 6.0
SIGMA_A = 0.005
N_SUB = 250
DT = 0.02
TICK_TIME = N_SUB * DT
THETA0 = dict(VJ.THETA, mut128=50.0)
PNAMES = tuple(THETA0)
_ST_PROC, _ST_DYN = 3, 6            # vw.world._ST_PROC, _ST_DYN


def area_factor(H, W):
    return (128.0 * 128.0) / (H * W)


def theta_batch(B, **over):
    """Dict of (B,) float64 arrays: THETA0 with per-member overrides (scalars or (B,) arrays)."""
    out = {}
    for k, v in THETA0.items():
        a = np.asarray(over.get(k, v), float)
        out[k] = np.broadcast_to(a, (B,)).copy()
    bad = set(over) - set(THETA0)
    if bad:
        raise KeyError(f"unknown parameters {bad}")
    return out


class Runner:
    """Batched fed-vortex world at H x H with the vortex tracker.

    init(Q, k_init)                        -> X, M           (state at t = 0 and tracker memory)
    run(Q, X, M, kp, tick0, U)             -> X, M, Y1       U (T, B, m); Y1 (T, B, K*12) float32, the vortex
                                                            list AFTER each tick; kp = process keys (B,)
    Q: dict name -> (B,) (theta_batch). Keys: typed jax keys (B,). tick0 (B,) int64: the tick index of the
    first tick (the noise clock). proc_key(member_key) = fold_in(member_key, 3), as vw.World does.
    """

    def __init__(self, H: int = 64, n_sub: int = N_SUB, track: bool = True, cpu_map: bool | None = None):
        self.H = H
        self.cfg = VJ.Config(H=H, W=H, G=H // 16, n_sub=n_sub, mut_dt=0.0, lab_t=-1.0, sigma_a=SIGMA_A)
        self.cfg_ref = VJ.Config(H=H, W=H, G=H // 16, n_sub=n_sub, mut_dt=50.0 * area_factor(H, H), lab_t=LAB_T,
                                 mut_r=MUT_R, sigma_a=SIGMA_A)
        self.m = self.cfg.m
        self.Bm = jnp.asarray(VJ.stir_basis(self.cfg))                   # (m, H*W), passed as an argument
        self.centres = VJ.bump_centres(self.cfg)
        _, self.bt = VW.phi_vortices(self.cfg_ref)
        self.K = self.bt.K
        self.track = track
        self.af = area_factor(H, H)
        on_cpu = jax.default_backend() == "cpu"
        self.cpu_map = on_cpu if cpu_map is None else cpu_map
        ns = VJ.make_native_step(self.cfg)
        init0 = VJ.make_init(self.cfg)
        bt, cfg, n, dt = self.bt, self.cfg, n_sub, DT
        yy = jnp.arange(H, dtype=jnp.float64)[:, None]
        xx = jnp.arange(H, dtype=jnp.float64)[None, :]

        def per_of(q):
            return jnp.maximum(jnp.round(q["mut128"] * self.af / dt), 1.0).astype(jnp.int64)

        def flags(q, t):
            lab = jnp.abs(t - LAB_T) < dt / 2
            when = (t > LAB_T) & (jnp.round(t / dt).astype(jnp.int64) % per_of(q) == 0)
            return lab, when

        def pre(q, x, kp, tk, i):
            """Labelling and mutation of one member before native step i of tick tk (vortex_jax's rules)."""
            om, Y, a, b, t = x["om"], x["Y"], x["a"], x["b"], x["t"]
            lab, when = flags(q, t)
            w2 = om ** 2
            sat = w2 / (w2 + q["wi"] ** 2)
            eat = jnp.minimum(q["e"] * Y * sat * w2, Y / dt)
            a = jnp.where(lab, jnp.where(eat > 1e-3, 1.0, 0.0), a)
            b = jnp.where(lab, 0.0, b)
            mut_u = Noise(kp, tk).stream(1).substep(n, i).uniform()
            mask = (eat > 1e-3).ravel()
            cnt = mask.sum()
            r = jnp.floor(mut_u * cnt).astype(jnp.int64)
            kk = jnp.argmax(mask & (jnp.cumsum(mask) == r + 1))
            cy, cx = (kk // H).astype(jnp.float64), (kk % H).astype(jnp.float64)
            d2 = ((yy - cy + H / 2) % H - H / 2) ** 2 + ((xx - cx + H / 2) % H - H / 2) ** 2
            mm = (d2 <= MUT_R ** 2) & (cnt > 0) & when
            return {"om": om, "Y": Y, "a": jnp.where(mm, b, a), "b": jnp.where(mm, a, b), "t": t}

        def kinds_field(x):
            w = jnp.abs(x["om"])
            fb = x["b"] / (x["a"] + x["b"] + 1e-3)
            return jnp.stack([w * (1 - fb), w * fb])

        def tick_one(q, x, kp, tk, u, Bm):
            """One member, one tick (lax.map path on CPU)."""
            ut = u + cfg.sigma_a * Noise(kp, tk).stream(0).normal((cfg.m,))
            f = (ut @ Bm).reshape(H, H) / cfg.tick_time

            def body(i, xx_):
                lab, when = flags(q, xx_["t"])
                xx_ = lax.cond(lab | when, lambda z: pre(q, z, kp, tk, i), lambda z: z, xx_)
                return ns(q, xx_, 0.0, f)
            return lax.fori_loop(0, n, body, x)

        def tick_batch(Q, X, kp, tk, U, Bm):
            """All members, one tick: one fori_loop over the batch, mutation behind a batch-level cond."""
            eta = jax.vmap(lambda k, t: Noise(k, t).stream(0).normal((cfg.m,)))(kp, tk)
            f = ((U + cfg.sigma_a * eta) @ Bm).reshape(-1, H, H) / cfg.tick_time
            vns = jax.vmap(lambda q, x, ff: ns(q, x, 0.0, ff))

            def body(i, XX):
                lab, when = jax.vmap(flags)(Q, XX["t"])
                XX = lax.cond(jnp.any(lab | when),
                              lambda Z: jax.vmap(lambda q, z, k, t: pre(q, z, k, t, i))(Q, Z, kp, tk),
                              lambda Z: Z, XX)
                return vns(Q, XX, f)
            return lax.fori_loop(0, n, body, X)

        def upd(M, X):
            return jax.vmap(lambda m, x: bt.update_memory(m, kinds_field(x)))(M, X)

        def y1_of(M):
            return jax.vmap(lambda m: bt.phi(None, m))(M).astype(jnp.float32)

        def run(Q, X, M, kp, tick0, U, Bm):
            def body(c, a):
                X, M, tk = c
                u, = a
                if self.cpu_map:
                    X = lax.map(lambda args: tick_one(args[0], args[1], args[2], args[3], args[4], Bm),
                                (Q, X, kp, tk, u))
                else:
                    X = tick_batch(Q, X, kp, tk, u, Bm)
                if self.track:
                    M = upd(M, X)
                    y = y1_of(M)
                else:
                    y = jnp.zeros((kp.shape[0], 1), jnp.float32)
                return (X, M, tk + 1), y
            (X, M, _), Y = lax.scan(body, (X, M, tick0), (U,))
            return X, M, Y

        def init(Q, k_init):
            X = jax.vmap(lambda q, k: init0(q, jax.random.fold_in(k, 1)))(Q, k_init)     # vw.world._ST_INIT = 1
            M = jax.vmap(lambda x: bt.init_memory(kinds_field(x)))(X)
            return X, M

        self._run = jax.jit(run)
        self._init = jax.jit(init)
        self._tick_one = tick_one
        self.kinds_field = kinds_field
        self.overflow = lambda M: np.asarray(bt.split(M)["overflow"])

    # ------------------------------------------------------------------ host API
    @staticmethod
    def jq(Q):
        return {k: jnp.asarray(v, jnp.float64) for k, v in Q.items()}

    @staticmethod
    def proc_keys(member_keys, fresh=False):
        """Process-noise keys. Member keys k_i as vw's Designer.ensemble: dyn = fold_in(k_i, 6), process =
        fold_in(dyn, 3). fresh=True: the given keys are dyn keys already (branches with fresh noise)."""
        if fresh:
            return jax.vmap(lambda k: jax.random.fold_in(k, _ST_PROC))(member_keys)
        return jax.vmap(lambda k: jax.random.fold_in(jax.random.fold_in(k, _ST_DYN), _ST_PROC))(member_keys)

    def init(self, Q, k_init):
        return self._init(self.jq(Q), k_init)

    def run(self, Q, X, M, kp, tick0, U):
        """U (T, B, m) numpy or None-like zeros. Returns X, M, Y1 numpy (T, B, K*12) float32."""
        B = kp.shape[0]
        t0 = jnp.broadcast_to(jnp.asarray(tick0, jnp.int64), (B,))
        X, M, Y = self._run(self.jq(Q), X, M, kp, t0, jnp.asarray(U, jnp.float64), self.Bm)
        return X, M, np.asarray(Y)

    def rollout(self, Q, keys, T, U=None, chunk=40, log=None, X=None, M=None, tick0=0, kp=None):
        """From init (or from a given state): T ticks in chunks. keys: member keys (B,) (init from fold 1,
        process noise from fold 3). U (T, B, m) or None. Returns X, M, Y1 (B, T, K*12) float32."""
        B = keys.shape[0]
        if X is None:
            X, M = self.init(Q, keys)
        kp = self.proc_keys(keys) if kp is None else kp
        out = []
        for s in range(0, T, chunk):
            n = min(chunk, T - s)
            Uc = np.zeros((n, B, self.m)) if U is None else np.asarray(U[s:s + n], float)
            Xn, Mn, Y = self.run(Q, X, M, kp, tick0 + s, Uc)
            X, M = Xn, Mn
            out.append(Y)
            if log:
                log(f"    rollout {s + n}/{T} ticks x {B}")
        return X, M, np.concatenate(out, 0).transpose(1, 0, 2)


def take(tree, idx):
    """Index the leading (member) axis of a pytree of device arrays."""
    idx = jnp.asarray(idx)
    return jax.tree_util.tree_map(lambda a: a[idx], tree)


def take_keys(keys, idx):
    return keys[jnp.asarray(idx)]


# ----------------------------------------------------------------------------- level 1 / level 2 (numpy)
S1_NAMES = ("N", "s_b", "fb_mass", "fb_mean", "fb_sd", "mixed", "log_mass_tot", "log_mass_mean", "mass_cv",
            "speed_mean", "rg_mean", "turnover")


def tables(Y1, K):
    """(..., K*12) -> (..., K, 12) float64."""
    Y1 = np.asarray(Y1, np.float64)
    return Y1.reshape(Y1.shape[:-1] + (K, NF))


def level2(Y1, K):
    """(N, s_b) from vortex lists (..., K*12) -> (..., 2): vortex_world.kinds in numpy."""
    T = tables(Y1, K)
    pres = T[..., 0] > 0.5
    n = pres.sum(-1).astype(float)
    nb = (pres & (T[..., 2] > 0.5)).sum(-1).astype(float)
    return np.stack([n, nb / np.maximum(n, 1.0)], -1)


def summaries(Y1, K):
    """Permutation-invariant level-1 statistics per tick: Y1 (B, T, K*12) -> (B, T, len(S1_NAMES)).
    turnover = slots whose presence changed since the previous tick (0 at the first tick)."""
    T = tables(Y1, K)
    pres = T[..., 0] > 0.5
    n = pres.sum(-1).astype(float)
    n1 = np.maximum(n, 1.0)
    mass = np.where(pres, T[..., 1], 0.0)
    frac = np.where(pres, T[..., 2], 0.0)
    mt = mass.sum(-1)
    mt1 = np.maximum(mt, 1e-9)
    fbm = (mass * frac).sum(-1) / mt1
    fbu = frac.sum(-1) / n1
    fbsd = np.sqrt(np.maximum((np.where(pres, frac, 0.0) ** 2).sum(-1) / n1 - fbu ** 2, 0.0))
    mixed = (pres & (T[..., 2] > 0.2) & (T[..., 2] < 0.8)).sum(-1) / n1
    mm = mt / n1
    mcv = np.sqrt(np.maximum((mass ** 2).sum(-1) / n1 - mm ** 2, 0.0)) / np.maximum(mm, 1e-9)
    spd = np.where(pres, np.hypot(T[..., 10], T[..., 11]), 0.0).sum(-1) / n1
    rg = np.where(pres, T[..., 7], 0.0).sum(-1) / n1
    turn = np.zeros_like(n)
    turn[:, 1:] = (pres[:, 1:] != pres[:, :-1]).sum(-1)
    sb = (pres & (T[..., 2] > 0.5)).sum(-1) / n1
    return np.stack([n, sb, fbm, fbu, fbsd, mixed, np.log(mt1), np.log(np.maximum(mm, 1e-9)), mcv, spd, rg, turn],
                    -1).astype(np.float32)


def raster(Y1, K, H, block=16):
    """The scored level-1 view: per block of `block` px, the summed vortex mass and kind-b mass (mass * frac_b)
    of the vortices whose centroid lies in the block. Y1 (..., K*12) -> (..., 2 * G * G), G = H / block."""
    T = tables(Y1, K)
    G = H // block
    pres = T[..., 0] > 0.5
    cx = (np.arctan2(T[..., 4], T[..., 3]) * H / (2 * np.pi)) % H
    cy = (np.arctan2(T[..., 6], T[..., 5]) * H / (2 * np.pi)) % H
    bi = np.floor(cy / block).astype(int) % G
    bj = np.floor(cx / block).astype(int) % G
    flat = (bi * G + bj).reshape(-1, K)
    mass = np.where(pres, T[..., 1], 0.0).reshape(-1, K)
    mb = (np.where(pres, T[..., 1] * T[..., 2], 0.0)).reshape(-1, K)
    n = flat.shape[0]
    out = np.zeros((n, 2, G * G))
    rows = np.repeat(np.arange(n), K)
    np.add.at(out[:, 0], (rows, flat.ravel()), mass.ravel())
    np.add.at(out[:, 1], (rows, flat.ravel()), mb.ravel())
    return out.reshape(T.shape[:-2] + (2 * G * G,))


# ----------------------------------------------------------------------------- stirring programs
def nats_of(U):
    """Information cost of a dense program (..., T, m): sum |u_t|^2 / (2 sigma_a^2) nats (exact for the channel)."""
    return 0.5 * (np.asarray(U, float) ** 2).sum((-1, -2)) / SIGMA_A ** 2


PROGRAM_CLASSES = ("a", "b", "c", "d")
U_MAX = 0.2


def make_program(cls, rng, y1_last, K, H, T, nats, centres):
    """A dense (T, m) open-loop stirring program of the public mix, total cost `nats` (within u_max):
      a  none
      b  blind: 4 random coefficients, random signs, constant over the first 4 ticks
      c  aimed from the history: the coefficient nearest to the heaviest kind-b vortex (heaviest vortex if no
         kind b) of the last revealed vortex list, constant over the first 2 ticks, random sign
      d  regional: one sign on a random 2 x 2 group of neighbouring coefficients (periodic) for 4 ticks
    """
    m = len(centres)
    G = int(round(np.sqrt(m)))
    U = np.zeros((T, m))
    if cls == "a" or nats <= 0:
        return U
    if cls == "b":
        idx = rng.choice(m, size=min(4, m), replace=False)
        nt = min(4, T)
        amp = np.sqrt(2 * nats * SIGMA_A ** 2 / (len(idx) * nt))
        U[:nt, idx] = amp * rng.choice([-1.0, 1.0], size=len(idx))
    elif cls == "c":
        Tb = tables(y1_last, K)
        pres = Tb[:, 0] > 0.5
        cand = pres & (Tb[:, 2] > 0.5)
        if not cand.any():
            cand = pres
        if cand.any():
            s = int(np.argmax(np.where(cand, Tb[:, 1], -1.0)))
            cx = (np.arctan2(Tb[s, 4], Tb[s, 3]) * H / (2 * np.pi)) % H
            cy = (np.arctan2(Tb[s, 6], Tb[s, 5]) * H / (2 * np.pi)) % H
            d = np.hypot((centres[:, 0] - cy + H / 2) % H - H / 2, (centres[:, 1] - cx + H / 2) % H - H / 2)
            j = int(np.argmin(d))
        else:
            j = int(rng.integers(m))
        nt = min(2, T)
        U[:nt, j] = np.sqrt(2 * nats * SIGMA_A ** 2 / nt) * rng.choice([-1.0, 1.0])
    elif cls == "d":
        i0, j0 = rng.integers(G), rng.integers(G)
        idx = [((i0 + di) % G) * G + (j0 + dj) % G for di in (0, 1) for dj in (0, 1)]
        idx = sorted(set(idx))
        nt = min(4, T)
        U[:nt, idx] = np.sqrt(2 * nats * SIGMA_A ** 2 / (len(idx) * nt)) * rng.choice([-1.0, 1.0])
    else:
        raise ValueError(cls)
    if np.abs(U).max() > U_MAX + 1e-12:
        U *= U_MAX / np.abs(U).max()
    return U
