"""fx_lib -- study foundryexam (round 6): the foundry's transport automaton as an exam world.

  Runner        the public simulator of the family, batched over members that each carry their own weights
                (one compiled program per chunk size; weights are arguments, never closed over)
  gate          the exam-time gate of DESIGN.md section 2 (active after the exam's burn-in)
  programs      the public program mix (a none, b blind, c aimed, d regional) in dense and harness form
  build_world   the family as a vw.World (block view observed, wind input with exact nats); the hidden
                weights are `world.params`, swapped per hidden world without recompiling
  FBatchLab     round 4's BatchLab (vw.harness.Lab running exam-shaped episodes in batches)
  build_exam    vw.harness.HistoryExam with per-world evaluator scales; plug-in simulators from the hidden state
  ridge         the cheap data-only predictor Dr (local ridge with Gaussian residuals)

PILOT ONLY: nothing produced with this module may be reused as an exam.
"""
from __future__ import annotations

import math
import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
PROG = os.path.abspath(os.path.join(HERE, "..", ".."))
FOUNDRY = os.path.join(PROG, "round5", "foundry")
for _p in (FOUNDRY,):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import tnca as TN  # noqa: E402  (sets the vw path and float64)
import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402
from jax import lax  # noqa: E402

import vw  # noqa: E402
from vw.core import Noise  # noqa: E402
from vw.harness import HistoryExam, Lab, ProgramMix  # noqa: E402
from vw.nats import NatsBudget  # noqa: E402
from vw.scoring import energy_fair, energy_loo  # noqa: E402

FAM = TN.FAM
G, NW, NCH = FAM.GW, FAM.NW, FAM.C + 1
NB = G * G
NOBS = NCH * NB                         # 192: block means of the two kinds and of S^2
SIGW = FAM.sigma_w
P, H = 16, 16                           # history ticks, test ticks
T1 = P + H + 1                          # frames of an episode
HS = (1, 2, 4, 8, 16)
TICK_CAP, EP_CAP = 100.0, 400.0         # nats
T_IN = 4                                # ticks of a command
C_BLIND, C_AIM, C_REG = 200.0, 200.0, 400.0
U_MAX = 4.0                             # admissible bound of a wind coefficient
CV_UNIFORM, VP_NOISY = 0.25, 1.0                       # round5/foundry/criteria.py
VP_ACTIVE16 = 0.2                                       # exam-time activity (criteria.py's frozen threshold is 0.02; see DESIGN.md)
TKEYS = ("W1", "b1", "W2", "beta", "gam", "alpha", "mu", "kappa", "gr", "dens", "wq")


# ----------------------------------------------------------------------------- weights
def stack_thetas(ths) -> dict:
    return {k: np.stack([np.asarray(t[k], np.float64) for t in ths]) for k in TKEYS}


def take(TH: dict, idx) -> dict:
    idx = np.asarray(idx)
    return {k: v[idx] for k, v in TH.items()}


def theta_of(TH: dict, i: int) -> dict:
    return {k: v[i] for k, v in TH.items()}


def neighbour(th_c: dict, draw: int, j: int, eps: float) -> dict:
    """The j-th eps-neighbour of centre `draw` (weights move, the 10 scalars stay the centre's)."""
    return TN.perturb_theta(th_c, 606000 + int(draw), int(j), float(eps), hyper=False)


# ----------------------------------------------------------------------------- the public simulator
class Runner:
    """Batched simulation with per-member weights. All calls are padded to `chunk` members."""

    def __init__(self, chunk: int, burn: int):
        self.chunk, self.burn = int(chunk), int(burn)
        # size guard: the largest array of a substep is (chunk, C, 4, H, W) logits or (chunk, HID, H, W) hidden units
        big = self.chunk * max(FAM.C * 4, FAM.HID) * FAM.H * FAM.W
        if big >= 2 ** 30:
            raise ValueError(f"Runner: chunk {chunk} would build an array of {big:.3g} elements (limit 2^30)")
        fam = FAM
        fold = jax.random.fold_in
        view = lambda x: TN.block_view(x).reshape(-1)

        def start(TH, keys, ticks):
            def one(th, k):
                x = TN.init(th, fold(k, 1), fam)
                kb = fold(k, 2)
                x, _ = lax.scan(lambda x, t: (TN.tick_free(th, x, Noise(kb, t), fam), None), x, ticks)
                S = x.sum(0)
                return x, view(x), S.std() / S.mean()
            return jax.vmap(one)(TH, keys)

        def run(TH, x, keys, U, t0):
            def one(th, x, k, u):
                kd = fold(k, 3)

                def body(x, tu):
                    t, ut = tu
                    xn = TN.tick(th, x, Noise(kd, t), ut, fam)
                    return xn, view(xn)
                x, Y = lax.scan(body, x, (t0 + jnp.arange(u.shape[0]), u))
                S = x.sum(0)
                return x, Y, S.std() / S.mean()
            return jax.vmap(one)(TH, x, keys, U)
        self._start, self._run = jax.jit(start), jax.jit(run)
        self.member_ticks = 0

    def _pad(self, a, n):
        a = np.asarray(a)
        if a.shape[0] == n:
            return a
        return np.concatenate([a, np.repeat(a[:1], n - a.shape[0], 0)], 0)

    def episodes(self, TH: dict, seed: int, classes=None, prog_seed: int = 0, log=None, tag=""):
        """Exam-shaped episodes, one per row of TH: init, burn-in, P free ticks, then H ticks under a program of
        the row's class (None: no input). Returns obs (n, T1, NOBS) f32, U (n, P + H, NW) f32, cv (n,)."""
        n = TH["W1"].shape[0]
        CH = self.chunk
        obs = np.zeros((n, T1, NOBS), np.float32)
        UU = np.zeros((n, P + H, NW), np.float32)
        cv = np.zeros(n)
        base = jax.random.key(int(seed))
        ticks = jnp.arange(self.burn)
        for s in range(0, n, CH):
            e = min(n, s + CH)
            b = e - s
            th = {k: jnp.asarray(self._pad(v[s:e], CH)) for k, v in TH.items()}
            keys = jax.vmap(lambda i: jax.random.fold_in(base, i))(jnp.asarray(self._pad(np.arange(s, e), CH)))
            x, y0, _ = self._start(th, keys, ticks)
            x, Y1, _ = self._run(th, x, keys, jnp.zeros((CH, P, NW)), 0)
            hist = np.concatenate([np.asarray(y0)[:, None], np.asarray(Y1)], 1)          # (CH, P + 1, NOBS)
            U = np.zeros((CH, H, NW))
            if classes is not None:
                for i in range(b):
                    rng = np.random.default_rng([int(prog_seed), int(seed) % (2 ** 31), s + i])
                    U[i] = prog_dense(classes[s + i], rng, hist[i, -1])
            x, Y2, c = self._run(th, x, keys, jnp.asarray(U), P)
            obs[s:e] = np.concatenate([hist, np.asarray(Y2)], 1)[:b]
            UU[s:e, P:] = U[:b]
            cv[s:e] = np.asarray(c)[:b]
            self.member_ticks += CH * (self.burn + P + H)
            if log and (s // CH) % 8 == 0:
                log(f"  sim{tag} {e}/{n}")
        return obs, UU, cv


def gate(obs, cv, M: int) -> dict:
    """Exam-time gate per world from M free episodes each (obs (W * M, T1, NOBS), cv (W * M,))."""
    W = obs.shape[0] // M
    y = obs.reshape(W, M, T1, NCH, NB).astype(np.float64)
    mu = y.mean((1, 2, 4), keepdims=True)
    sd = y.std((1, 2, 4), keepdims=True)
    z = (y - mu) / np.maximum(sd, 1e-12 * np.maximum(np.abs(mu), 1e-300))
    vp = lambda h: ((z[:, :, h:] - z[:, :, :-h]) ** 2).mean((1, 2, 3, 4))
    vp1, vp16 = vp(1), vp(16)
    cvw = cv.reshape(W, M).mean(1)
    fin = np.isfinite(y).all((1, 2, 3, 4))
    tick_r2 = z.mean((1, 4)).var(1).mean(1)                 # variance over ticks of the member-and-block mean
    ok = fin & (cvw >= CV_UNIFORM) & (vp16 >= VP_ACTIVE16) & (vp1 <= VP_NOISY)
    return dict(ok=ok, cv_cell=cvw, vp1=vp1, vp16=vp16, finite=fin, tick_r2=tick_r2,
                mean=mu.reshape(W, NCH), sd=sd.reshape(W, NCH))


# ----------------------------------------------------------------------------- programs (public mix)
def _densest(frame):
    f = np.asarray(frame, float)
    return int(np.argmax(f[:NB] + f[NB:2 * NB]))


def prog_dense(cls: str, rng, last_frame, left: float = EP_CAP) -> np.ndarray:
    """(H, NW) wind command of class a | b | c | d built from the last revealed frame."""
    U = np.zeros((H, NW))
    if cls == "a":
        return U
    if cls == "b":
        d = rng.standard_normal((T_IN, NW))
        amp = math.sqrt(2.0 * min(C_BLIND, left)) * SIGW * (1 - 1e-9)
        U[:T_IN] = amp * d / math.sqrt((d ** 2).sum())
        return np.clip(U, -U_MAX * 0.999, U_MAX * 0.999)
    b = _densest(last_frame)
    phi = rng.uniform(0.0, 2.0 * math.pi)
    if cls == "c":
        a = math.sqrt(2.0 * min(C_AIM, left) / T_IN) * SIGW * (1 - 1e-9)
        U[:T_IN, b], U[:T_IN, NB + b] = a * math.cos(phi), a * math.sin(phi)
        return U
    if cls == "d":
        r, c = divmod(b, G)
        blocks = [((r + dy) % G) * G + (c + dx) % G for dy in (-1, 0, 1) for dx in (-1, 0, 1)]
        a = math.sqrt(2.0 * min(C_REG, left, T_IN * TICK_CAP) / T_IN / len(blocks)) * SIGW * (1 - 1e-9)
        for bb in blocks:
            U[:T_IN, bb], U[:T_IN, NB + bb] = a * math.cos(phi), a * math.sin(phi)
        return U
    raise ValueError(cls)


def dense_to_prog(U):
    return [(int(t), {int(j): float(U[t, j]) for j in np.flatnonzero(U[t])}) for t in range(U.shape[0]) if np.any(U[t])]


def _cls(name):
    return lambda rng, hist, Hh, left: dense_to_prog(prog_dense(name, rng, np.asarray(hist)[-1], left))


MIX = ProgramMix({k: _cls(k) for k in "abcd"})
CLASSES = tuple("abcd")


def mix_classes(n: int, rng) -> list:
    lab = [CLASSES[i % 4] for i in range(n)]
    rng.shuffle(lab)
    return lab


def nats_of(U) -> np.ndarray:
    return 0.5 * (np.asarray(U, float) ** 2).sum((-2, -1)) / SIGW ** 2


def budget(total=None) -> NatsBudget:
    return NatsBudget.isotropic(NW, SIGW, tick=TICK_CAP, episode=EP_CAP, total=total,
                                note="wind coefficients enter as a shift before N(0, sigma_w^2 I) noise")


# ----------------------------------------------------------------------------- the hidden world (vw)
def build_world(theta: dict, burn: int) -> vw.World:
    th = {k: jnp.asarray(theta[k]) for k in TKEYS}
    lev = vw.Level(init=lambda p, key: TN.init(p, key, FAM), step=lambda p, x, nz, u: TN.tick(p, x, nz, u, FAM),
                   input_dim=NW, params=th, conserved={"mass_total": lambda x: x.sum()}, name="tnca-foundryexam")
    phi = vw.CoarseGrain.of(lambda x: TN.block_view(x).reshape(-1), name="Phi_coarse8")
    spec = vw.WorldSpec(base=lev, chain=(phi,),
                        inport=vw.InputPort(admissible=vw.Admissible(k=None, lo=-U_MAX, hi=U_MAX), in_map=tuple(range(NW))),
                        outport=vw.ObservePort(noise=0.0, quantum=None, out_map=tuple(range(NOBS)),
                                               out_sign=tuple([1.0] * NOBS)),
                        burn_in=int(burn), replay="initial", name="foundryexam",
                        public_notes="wind input: 128 coefficients (2 x 8 x 8), cost |u|^2 / (2 sigma_w^2) nats")
    return vw.World(spec, world_seed=0, params=th)


def set_params(world: vw.World, theta: dict):
    world.params = {k: jnp.asarray(theta[k]) for k in TKEYS}


class FBatchLab(Lab):
    """round4/sbi/sbi_lib.BatchLab (copied: that module imports the gliders world): vw.harness.Lab that runs a
    batch of exam-shaped episodes at once. For each label: reset(label), P ticks without input, then the
    open-loop program built from o(0..P) by make_prog(i, history). Keys, validation (bounds, nats caps) and
    charging are those of the sequential Lab."""

    def run_batch(self, labels, Pp: int, Hh: int, make_prog):
        w, C = self.world, self.world.inport.admissible
        B = len(labels)
        self._check_ticks(B * (self.reset_cost + Pp + Hh))
        ki, kd = [], []
        for lab in labels:
            lab = lab if isinstance(lab, str) else int(lab)
            self._count += 1
            self.n_resets += 1
            ki.append(np.asarray(jax.random.key_data(self._sec.key("init", lab))))
            kd.append(np.asarray(jax.random.key_data(self._sec.key("dyn", lab, self._count))))
        KI = jax.random.wrap_key_data(jnp.asarray(np.stack(ki)))
        KD = jax.random.wrap_key_data(jnp.asarray(np.stack(kd)))
        ens = w._new_ensemble(KI, KD)
        self.ticks_used += B * self.reset_cost
        c, rec = w._rollout(w.params, ens.carry, jnp.zeros((Pp, B, w.n_in)), rec=("obs",))
        self.ticks_used += B * Pp
        hist = np.asarray(rec["obs"]).transpose(1, 0, 2)                    # (B, P+1, n_obs)
        A = np.zeros((Hh, B, w.n_in))
        nats = np.zeros(B)
        for i in range(B):
            prog = make_prog(i, hist[i])
            prog = [(int(t), {int(j): float(v) for j, v in a.items()}) for t, a in prog]
            vp = w._validate_program(prog, Pp, None, 0.0, Hh)
            canon = [(t, C.canonical(a)) for t, a in vp]
            if self.acct is not None:
                self.acct.new_episode()
                self.acct.check_program(canon, episode_used=0.0)
                for _, ca in canon:
                    nats[i] += self.acct.charge(ca)
            for t, ca in canon:
                for j, v in ca.items():
                    A[t, i, j] = v
        c, rec = w._rollout(w.params, c, jnp.asarray(A), rec=("obs",))
        self.ticks_used += B * Hh
        obs2 = np.asarray(rec["obs"]).transpose(1, 0, 2)
        self._ep = None
        U = np.zeros((B, Pp + Hh, w.n_in))
        U[:, Pp:] = A.transpose(1, 0, 2)
        return {"obs": np.concatenate([hist, obs2[:, 1:]], 1).astype(np.float32), "U": U.astype(np.float32), "nats": nats}


def run_lab(world, secret, n: int, chunk: int, seed_rng) -> dict:
    """A Lab of n exam-mix episodes on the hidden world (labels 0..n-1; classes a-d in equal shares, shuffled)."""
    lab = FBatchLab(world, secret, nats=budget(), max_ticks=None, reset_cost=1)
    cls = mix_classes(n, seed_rng)
    prng = [np.random.default_rng([int(seed_rng.integers(2 ** 31)), i]) for i in range(n)]
    out = []
    for s in range(0, n, chunk):
        e = min(n, s + chunk)
        mk = lambda i, hist, s=s: MIX.classes[cls[s + i]](prng[s + i], hist, H, EP_CAP)
        out.append(lab.run_batch(list(range(s, e)), P, H, mk))
    res = {k: np.concatenate([o[k] for o in out]) for k in out[0]}
    res["cls"] = np.array(cls)
    res["usage"] = lab.usage()
    return res


def build_exam(world, secret, n_items: int, R: int, n_clim: int, name: str) -> HistoryExam:
    ex = HistoryExam(world, secret, MIX, n_items=n_items, prefix=P, queries={1: list(HS)}, R=R, nats=budget(),
                     n_clim=n_clim, name=name)
    pool = np.asarray(ex.clim[1], float)                               # (n_clim, nt, NOBS)
    sd = pool.reshape(pool.shape[0], pool.shape[1], NCH, NB).std((0, 1, 3))
    mu = pool.reshape(pool.shape[0], pool.shape[1], NCH, NB).mean((0, 1, 3))
    sd = np.maximum(sd, 1e-9 * np.maximum(np.abs(mu), 1e-300))
    ex.scales = {1: np.repeat(sd, NB)}
    ex.clim_mean, ex.clim_sd = mu, sd
    return ex


def score_es(ex: HistoryExam, S) -> np.ndarray:
    """Fair energy score per item and cell of samples S (n_items, m, nt, NOBS) through the exam's own scorer."""
    return ex._per_cell(lambda X, Y, s, l: energy_fair(X, Y, s), samples=[{1: S[i]} for i in range(ex.n)])


def references(ex: HistoryExam) -> dict:
    return {"O": ex._per_cell(None, lambda Y, s, l: energy_loo(Y, s, True)),
            "K": ex._per_cell(lambda X, Y, s, l: energy_fair(X, Y, s), pool=ex.clim)}


def plugin(ex: HistoryExam, world, theta: dict, m: int, keys, zero_program: bool = False) -> np.ndarray:
    """Samples (n_items, m, nt, NOBS) of the simulator run from each item's hidden state at t = P with the
    weights `theta` (and the item's test program, or none)."""
    old = world.params
    set_params(world, theta)
    try:
        rep = ex._snap.clone(rep=m, keys=keys)
        Pt = np.zeros_like(ex._Ptest) if zero_program else ex._Ptest
        Pfull = np.concatenate([np.zeros((ex.n, ex.P, world.n_in)), Pt], 1)
        _, rec = world.designer.rollout(rep, np.repeat(Pfull, m, axis=0), T=ex.H, rec=("obs",))
    finally:
        world.params = old
    obs = rec["obs"].reshape(ex.n, m, ex.H + 1, -1)
    return obs[:, :, ex.queries[1]]


def item_arrays(ex: HistoryExam):
    """Public side of the items as arrays: history (n, P + 1, NOBS), test program (n, H, NW), class labels."""
    hist = np.stack([np.asarray(it.history, float) for it in ex.items])
    return hist, np.asarray(ex._Ptest, float), np.array([it.klass for it in ex.items])


# ----------------------------------------------------------------------------- Dr: local ridge on Lab data
def _nb3(a):
    """(..., c, G, G) -> (..., 9 c, G, G)."""
    return np.concatenate([np.roll(a, (dy, dx), (-2, -1)) for dy in (-1, 0, 1) for dx in (-1, 0, 1)], -3)


def _ridge_feats(z1, z0, usum):
    """z1, z0 (n, NCH, G, G) standardised frames at t and t - 1; usum (n, 2, G, G) wind sum in sigma_w units."""
    f = np.concatenate([_nb3(z1), _nb3(z0), _nb3(usum)], 1)             # (n, 72, G, G)
    f = np.moveaxis(f, 1, -1).reshape(-1, f.shape[1])
    return np.concatenate([f, np.ones((f.shape[0], 1))], 1)


def ridge_fit(obs, U, lam: float = 1e-3, max_anchor: int = 12, seed: int = 0) -> dict:
    """Per horizon: change of the standardised block view at a block from its 3 x 3 neighbourhood at t and
    t - 1 and the summed command over [t, t + h); residual covariance over the 3 channels."""
    y = np.asarray(obs, np.float64).reshape(obs.shape[0], T1, NCH, G, G)
    mu = y.mean((0, 1, 3, 4))
    sd = np.maximum(y.std((0, 1, 3, 4)), 1e-9 * np.maximum(np.abs(mu), 1e-300))
    z = (y - mu[None, None, :, None, None]) / sd[None, None, :, None, None]
    Ug = np.asarray(U, np.float64).reshape(U.shape[0], P + H, 2, G, G) / SIGW
    cu = np.concatenate([np.zeros_like(Ug[:, :1]), np.cumsum(Ug, 1)], 1)             # (E, T1, 2, G, G)
    rng = np.random.default_rng(seed)
    W, L = [], []
    for h in HS:
        ts = np.arange(1, T1 - h)
        if len(ts) > max_anchor:
            ts = np.sort(rng.choice(ts, max_anchor, replace=False))
        X = np.concatenate([_ridge_feats(z[:, t], z[:, t - 1], cu[:, t + h] - cu[:, t]) for t in ts])
        Y = np.concatenate([np.moveaxis(z[:, t + h] - z[:, t], 1, -1).reshape(-1, NCH) for t in ts])
        A = X.T @ X + lam * X.shape[0] * np.eye(X.shape[1])
        w = np.linalg.solve(A, X.T @ Y)
        r = Y - X @ w
        cov = r.T @ r / max(r.shape[0] - 1, 1) + 1e-12 * np.eye(NCH)
        W.append(w)
        L.append(np.linalg.cholesky(cov))
    return dict(W=W, L=L, mu=mu, sd=sd)


def ridge_samples(model, hist, Ptest, m: int, seed: int) -> np.ndarray:
    """(n_items, m, len(HS), NOBS) samples in raw units."""
    n = hist.shape[0]
    mu, sd = model["mu"], model["sd"]
    y = np.asarray(hist, np.float64).reshape(n, P + 1, NCH, G, G)
    z = (y - mu[None, None, :, None, None]) / sd[None, None, :, None, None]
    Ug = np.asarray(Ptest, np.float64).reshape(n, H, 2, G, G) / SIGW
    cu = np.concatenate([np.zeros_like(Ug[:, :1]), np.cumsum(Ug, 1)], 1)
    rng = np.random.default_rng(seed)
    out = np.zeros((n, m, len(HS), NOBS))
    for j, h in enumerate(HS):
        X = _ridge_feats(z[:, P], z[:, P - 1], cu[:, h])
        d = (X @ model["W"][j]).reshape(n, G, G, NCH)
        eps = rng.standard_normal((n, m, G, G, NCH)) @ model["L"][j].T
        zs = np.moveaxis(z[:, P], 1, -1)[:, None] + d[:, None] + eps                 # (n, m, G, G, NCH)
        ys = zs * sd + mu
        out[:, :, j] = np.moveaxis(ys, -1, 2).reshape(n, m, NOBS)
    return out


def persistence_samples(hist, m: int = 2) -> np.ndarray:
    return np.repeat(np.repeat(hist[:, None, None, P], m, 1), len(HS), 2)


def load_acceptance():
    import importlib.util
    p = os.path.join(PROG, "round5", "agentenv", "evaluator", "acceptance.py")
    spec = importlib.util.spec_from_file_location("fx_acceptance", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
