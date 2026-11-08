"""sbi_lib -- simulate-to-train on the gliders wind world with 4 hidden parameters (round 4, study sbi).

Builds on program/track2/gliders_exam (gworld: per-member hidden theta = lR, dm_00, ls_00, lh; prior =
uniform box conditioned on the public viability rule; pilot: program mix, ridge predictor, exam) and
vw.harness / vw.scoring. Nothing in vw1/vw, vw1/port or track2 is changed; this module imports them.

Pieces
  params_batch   per-member parameter pytrees for a batch of theta (vectorised gworld.theta_to_params)
  VRunner        gworld.Runner with members batched by jax.vmap (the GPU batching; lax.map on CPU)
  sim_episodes   the agent's own simulator: episodes = init + burn-in + P ticks without input + an
                 open-loop test program of H ticks from the public mix, built from o(P) (as exam items)
  BatchLab       vw.harness.Lab running a batch of such episodes at once, every episode validated and
                 charged (ticks, nats) as the sequential Lab would
  features       per-episode level-1 summary statistics (phase-insensitive) and their linear projection
  Emulator       synthetic likelihood: s_bar(n episodes) ~ N(mu(theta), Sigma(theta)/n + emulator error)
  posterior      self-normalised importance sampling on the box with the viability prior p_v(theta)
  ridge          gliders_exam/pilot.fit_ridge, vectorised (same model, same numbers)
  net            a periodic conv net on the 8 x 8 block grid that outputs samples (noise inputs), trained
                 with the fair energy score (the exam's scoring rule); several nets trained at once (vmap)
"""
from __future__ import annotations

import json
import math
import os
import sys
import time

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
PROG = os.path.dirname(os.path.dirname(HERE))
VEC = os.path.dirname(PROG)
PORT = os.path.join(VEC, "vw1", "port")
ACT = os.path.join(PROG, "track2", "actuation")
GE = os.path.join(PROG, "track2", "gliders_exam")
for _p in (GE, ACT, PORT):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import _paths  # noqa: E402,F401

import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402

import vw  # noqa: E402
from vw.core import Noise  # noqa: E402
from vw.harness import Lab, program_dense  # noqa: E402
from vw.nats import NatsAccountant  # noqa: E402
import flowlenia_jax as FJ  # noqa: E402
import phi as PH  # noqa: E402
import gworld as GW  # noqa: E402
import pilot as PL  # noqa: E402

SIG = GW.SIGMA_W
NW, NC, NO, G = GW.NW, GW.NC, GW.NO, GW.G
N_OBS = NC + NO
PRIOR = json.load(open(os.path.join(GE, "results", "prior.json")))
NAMES = list(PRIOR["names"])
LO, HI = np.array(PRIOR["lo"], float), np.array(PRIOR["hi"], float)
CEN, HW_ = (LO + HI) / 2, (HI - LO) / 2
SC1 = PL.SC["level1"].astype(float)          # (192,) public level-1 scales
SC2 = PL.SC2.astype(float)                   # (3,)  public level-2 scales
POP_MEAN = np.array([7.482004429678848, 1441.8460833363622, 1.3635964380261172])   # refs_closure level2_means
QUANTUM = 1e-3
EP_CAP = PL.EP_CAP


def to_u(theta):
    return (np.asarray(theta, float) - CEN) / HW_


def from_u(u):
    return CEN + np.asarray(u, float) * HW_


# ----------------------------------------------------------------------------- parameters
_P_DEF = None


def params_batch(thetas) -> dict:
    """Stacked parameter pytree (leading axis B) for theta rows (B, 4) in NAMES order; equals
    gworld.stack_params([gworld.theta_to_params(dict(zip(NAMES, t))) for t in thetas])."""
    global _P_DEF
    th = np.atleast_2d(np.asarray(thetas, float))
    B = th.shape[0]
    if _P_DEF is None:
        _P_DEF = {k: np.asarray(v) for k, v in GW.theta_to_params({}).items()}
    d = dict(zip(NAMES, th.T))
    assert set(NAMES) == {"lR", "dm_00", "ls_00", "lh"}
    idx = GW.GROUPS["00"]
    m0, s0, h0 = (np.asarray(GW.P0[q], float) for q in "msh")
    dm = np.zeros((B, 20))
    dm[:, idx] = d["dm_00"][:, None]
    ls = np.ones((B, 20))
    ls[:, idx] = d["ls_00"][:, None]
    out = {k: np.broadcast_to(v, (B,) + v.shape).copy() for k, v in _P_DEF.items()}
    out["R"] = (float(GW.P0["R"]) + 15.0) * d["lR"] - 15.0
    out["m"] = m0[None] + dm * s0[None]
    out["s"] = s0[None] * ls
    out["h"] = h0[None] * d["lh"][:, None]
    return {k: jnp.asarray(v) for k, v in out.items()}


def quantize(y):
    return QUANTUM * np.round(np.asarray(y, float) / QUANTUM)


# ----------------------------------------------------------------------------- simulator (vmap)
class VRunner:
    """gworld.Runner with members batched by jax.vmap (per-member params): init_burn(P, k, sig) and
    run(P, A, m, key, t0, uw, sig) with the same keys, streams and outputs as gworld.Runner.
    burn: burn-in ticks (gworld.BURN = 50; smaller only in the CPU smoke test)."""

    def __init__(self, burn: int = GW.BURN):
        po, trv, _ = PH.phi_objects_jax("A_gliders")
        self.bt = trv.bt
        self.pc = PH.phi_coarse(GW.CFG, G)
        lev0, _, _ = FJ.make_level("A_gliders", GW.NOISE_STD)
        self.init0 = lev0.init
        self.burn = int(burn)
        self.init_burn = jax.jit(self._init_burn)
        self.run = jax.jit(self._run)

    def obs(self, A, m):
        return jnp.concatenate([self.pc.phi(A, ()), self.bt.phi(A, m)])

    def _init_burn(self, P, k, sig):
        bt, fold = self.bt, jax.random.fold_in

        def one(p, kk, sg):
            A = self.init0(p, fold(kk, GW._ST_INIT))
            m = bt.init_memory(A)
            kp = fold(fold(kk, GW._ST_BURN), GW._ST_PROC)
            zw = jnp.zeros((NW,))

            def body(c, t):
                A, m = c
                A = GW.tick(p, A, Noise(kp, t), zw, sg)
                return (A, bt.update_memory(m, A)), None
            (A, m), _ = jax.lax.scan(body, (A, m), jnp.arange(self.burn))
            return A, m
        return jax.vmap(one)(P, k, sig)

    def _run(self, P, A, m, key, t0, uw, sig):
        bt, fold = self.bt, jax.random.fold_in

        def one(p, A, m, kk, t0, uw, sg):
            kp = fold(kk, GW._ST_PROC)

            def rec(A, m):
                d = bt.split(m)
                return self.obs(A, m), d["table"][:, GW.NF:], d["globals"]

            def body(c, w):
                A, m, t = c
                A = GW.tick(p, A, Noise(kp, t), w, sg)
                m = bt.update_memory(m, A)
                return (A, m, t + 1), rec(A, m)
            r0 = rec(A, m)
            (A, m, _), outs = jax.lax.scan(body, (A, m, t0), uw)
            cat = lambda a, b: jnp.concatenate([a[None], b], 0)
            return tuple(cat(a, b) for a, b in zip(r0, outs)) + (A, m)
        return jax.vmap(one)(P, A, m, key, t0, uw, sig)


def _pad(a, n):
    a = np.asarray(a)
    if len(a) == n:
        return a
    return np.concatenate([a, np.repeat(a[-1:], n - len(a), 0)], 0)


def _pad_keys(k, n):
    data = np.asarray(jax.random.key_data(k))
    return jax.random.wrap_key_data(jnp.asarray(_pad(data, n)))


def make_program(cls, rng, hist, H):
    """Dense (H, NW) test program of class cls ('a'..'d') from the revealed history (P+1, n_obs)."""
    prog = PL.MIX.classes[cls](rng, hist, H, EP_CAP)
    return program_dense(prog, H, NW), prog


def sim_episodes(RN, thetas, keys, seed, P=16, H=16, chunk=256, classes=None, log=None):
    """The agent's own simulator, exam-shaped episodes: per member theta (B, 4), keys (B,) typed;
    init + burn-in, P ticks without input, then a test program of class classes[b] (default: uniform
    over the public mix) built from the quantised o(P). Returns dict: obs (B, P+H+1, 336) float32
    (quantised as the observe port), U (B, P+H, NW) float32, cls (B,), nats (B,)."""
    th = np.atleast_2d(np.asarray(thetas, float))
    B = len(th)
    rng0 = np.random.default_rng([int(seed), 0])
    if classes is None:
        classes = rng0.choice(list(PL.MIX.classes), size=B)
    classes = np.asarray(classes)
    OBS = np.zeros((B, P + H + 1, N_OBS), np.float32)
    UU = np.zeros((B, P + H, NW), np.float32)
    nats = np.zeros(B)
    for s in range(0, B, chunk):
        e = min(s + chunk, B)
        nb = e - s
        Pp = params_batch(_pad(th[s:e], chunk))
        k = _pad_keys(keys[s:e], chunk)
        sig = jnp.full((chunk,), SIG)
        A, m = RN.init_burn(Pp, k, sig)
        kd = GW.dyn_keys(k)
        y1, _, _, A, m = RN.run(Pp, A, m, kd, jnp.zeros((chunk,), jnp.int64), jnp.zeros((chunk, P, NW)), sig)
        y1 = quantize(np.asarray(y1)[:nb])
        U = np.zeros((chunk, H, NW))
        for b in range(nb):
            U[b], _ = make_program(classes[s + b], np.random.default_rng([int(seed), 1, s + b]), y1[b], H)
            nats[s + b] = GW.nats_of(U[b])
        y2, _, _, A, m = RN.run(Pp, A, m, kd, jnp.full((chunk,), P, jnp.int64), jnp.asarray(U), sig)
        y2 = quantize(np.asarray(y2)[:nb])
        OBS[s:e] = np.concatenate([y1, y2[:, 1:]], 1)
        UU[s:e, P:] = U[:nb]
        if log:
            log(f"  sim_episodes {e}/{B}")
    return {"obs": OBS, "U": UU, "cls": classes, "nats": nats}


# ----------------------------------------------------------------------------- the real world
def build_world(params, burn: int = GW.BURN):
    """gliders_exam/pilot.build_world with vw.World (vmap batching) instead of aworld.MapWorld."""
    lev = GW.level(SIG, params)
    pc = PH.phi_coarse(GW.CFG, G)
    po, _, _ = PH.phi_objects_jax("A_gliders")
    spec = vw.WorldSpec(base=lev, chain=(PH.pair(pc, po),),
                        inport=vw.InputPort(admissible=vw.Admissible(k=None, lo=-1.0, hi=1.0), in_map=tuple(range(NW))),
                        outport=vw.ObservePort(noise=0.0, quantum=QUANTUM, out_map=tuple(range(N_OBS)),
                                               out_sign=tuple([1.0] * N_OBS)),
                        burn_in=int(burn), replay="initial", name="gliders_wind_hidden4_sbi",
                        public_notes="wind input: 128 coefficients (2 x 8 x 8), cost |u|^2 / (2 sigma_w^2) nats")
    return vw.World(spec, world_seed=0, params=params)


class BatchLab(Lab):
    """vw.harness.Lab that runs a batch of exam-shaped episodes at once: for each label, reset(label)
    (reset_cost ticks), P ticks without input, then the agent's open-loop program built from o(0..P)
    by make_program(i, history) (agent side, history only). Episode keys, validation (bounds, nats
    tick / episode / total caps) and charging are those of the sequential Lab; the tick budget of the
    whole batch is checked before anything runs, each program before the test part runs."""

    def run_batch(self, labels, P: int, H: int, make_prog):
        w, C = self.world, self.world.inport.admissible
        B = len(labels)
        self._check_ticks(B * (self.reset_cost + P + H))
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
        c, rec = w._rollout(w.params, ens.carry, jnp.zeros((P, B, w.n_in)), rec=("obs",))
        self.ticks_used += B * P
        hist = np.asarray(rec["obs"]).transpose(1, 0, 2)                    # (B, P+1, n_obs)
        A = np.zeros((H, B, w.n_in))
        progs, nats = [], np.zeros(B)
        for i in range(B):
            prog = make_prog(i, hist[i])
            prog = [(int(t), {int(j): float(v) for j, v in a.items()}) for t, a in prog]
            vp = w._validate_program(prog, P, None, 0.0, H)
            canon = [(t, C.canonical(a)) for t, a in vp]
            if self.acct is not None:
                self.acct.new_episode()
                self.acct.check_program(canon, episode_used=0.0)
                for _, ca in canon:
                    nats[i] += self.acct.charge(ca)
            for t, ca in canon:
                for j, v in ca.items():
                    A[t, i, j] = v
            progs.append(prog)
        c, rec = w._rollout(w.params, c, jnp.asarray(A), rec=("obs",))
        self.ticks_used += B * H
        obs2 = np.asarray(rec["obs"]).transpose(1, 0, 2)
        self._ep = None
        U = np.zeros((B, P + H, w.n_in))
        U[:, P:] = A.transpose(1, 0, 2)
        return {"obs": np.concatenate([hist, obs2[:, 1:]], 1).astype(np.float32), "U": U.astype(np.float32),
                "programs": progs, "nats": nats}


# ----------------------------------------------------------------------------- summary statistics
FEATURES = ["count_mean", "count_sd", "count_absdiff", "log_mass_body", "mass_cv", "frac_c1", "log_rg", "aniso",
            "speed_mean", "speed_sd", "log_tracked_mass", "mass_c0", "mass_c1", "log_m2_mean", "log_sd_c0",
            "log_sd_c1", "corr_c0c1", "log_sd_m2", "log_dC1", "log_dC4", "log_max_m2", "log_density"]


def _lg(x):
    return np.log(np.maximum(x, 1e-6))


def episode_features(obs) -> np.ndarray:
    """Phase-insensitive level-1 statistics of each episode: obs (B, T+1, 336) -> (B, len(FEATURES))."""
    y = np.asarray(obs, float)
    B, T1, _ = y.shape
    C = y[..., :NC].reshape(B, T1, 3, G, G)
    O = y[..., NC:N_OBS].reshape(B, T1, GW.K, GW.NF)
    pres = O[..., 0] > 0.5
    npres = np.maximum(pres.sum((1, 2)), 1)
    n = pres.sum(-1).astype(float)

    def pm(v):
        return np.where(pres, v, 0.0).sum((1, 2)) / npres
    mass, frac, rg, q1, q2, vx, vy = (O[..., i] for i in (1, 2, 7, 8, 9, 10, 11))
    spd = np.hypot(vx, vy)
    mb = pm(mass)
    sp = pm(spd)
    sc = SC1.reshape(3, G, G)
    dC = lambda k: np.sqrt((((C[:, k:] - C[:, :-k]) / sc) ** 2).mean((2, 3, 4))).mean(1)
    c0 = C[:, :, 0].reshape(B, T1, -1)
    c1 = C[:, :, 1].reshape(B, T1, -1)
    c0c = c0 - c0.mean(-1, keepdims=True)
    c1c = c1 - c1.mean(-1, keepdims=True)
    corr = (c0c * c1c).sum(-1) / np.maximum(np.sqrt((c0c ** 2).sum(-1) * (c1c ** 2).sum(-1)), 1e-12)
    f = {"count_mean": n.mean(1), "count_sd": n.std(1), "count_absdiff": np.abs(np.diff(n, axis=1)).mean(1),
         "log_mass_body": _lg(mb), "mass_cv": np.sqrt(np.maximum(pm(mass ** 2) - mb ** 2, 0)) / np.maximum(mb, 1e-6),
         "frac_c1": pm(frac), "log_rg": _lg(pm(rg)), "aniso": pm(np.hypot(q1, q2)), "speed_mean": sp,
         "speed_sd": np.sqrt(np.maximum(pm(spd ** 2) - sp ** 2, 0)),
         "log_tracked_mass": _lg(np.where(pres, mass, 0.0).sum(-1).mean(1)),
         "mass_c0": C[:, 0, 0].mean((1, 2)), "mass_c1": C[:, 0, 1].mean((1, 2)),
         "log_m2_mean": _lg(C[:, :, 2].mean((2, 3))).mean(1), "log_sd_c0": _lg(c0.std(-1)).mean(1),
         "log_sd_c1": _lg(c1.std(-1)).mean(1), "corr_c0c1": corr.mean(1), "log_sd_m2": _lg(C[:, :, 2].std((2, 3))).mean(1),
         "log_dC1": _lg(dC(1)), "log_dC4": _lg(dC(min(4, T1 - 1))), "log_max_m2": _lg(C[:, :, 2].max((2, 3))).mean(1),
         "log_density": pm(_lg(mass) - 2 * _lg(rg))}
    return np.stack([f[k] for k in FEATURES], 1)


class Projection:
    """Linear regression summaries (Fearnhead & Prangle 2012): s = W^T z(f) + b, z = standardised
    features, fitted by ridge regression of u = (theta - centre) / half-width on z over the design."""

    def fit(self, F, U, lam=1e-3):
        F = np.asarray(F, float)
        self.mu, self.sd = F.mean(0), np.maximum(F.std(0), 1e-9)
        Z = np.concatenate([(F - self.mu) / self.sd, np.ones((len(F), 1))], 1)
        A = Z.T @ Z + lam * len(F) * np.diag(np.r_[np.ones(Z.shape[1] - 1), 0.0])
        self.W = np.linalg.solve(A, Z.T @ np.asarray(U, float))
        R = np.asarray(U) - Z @ self.W
        self.r2 = (1 - R.var(0) / np.asarray(U).var(0)).tolist()
        return self

    def __call__(self, F):
        F = np.asarray(F, float)
        Z = np.concatenate([(F - self.mu) / self.sd, np.ones(F.shape[:-1] + (1,))], -1)
        return Z @ self.W

    def state(self):
        return {"mu": self.mu.tolist(), "sd": self.sd.tolist(), "W": self.W.tolist(), "r2_per_param": self.r2,
                "features": FEATURES}


# ----------------------------------------------------------------------------- synthetic likelihood
def poly_feats(u, deg):
    """Monomials of u (..., 4) up to total degree deg (1, u_i, u_i u_j, ...)."""
    u = np.asarray(u, float)
    d = u.shape[-1]
    cols = [np.ones(u.shape[:-1])]
    import itertools
    for k in range(1, deg + 1):
        for c in itertools.combinations_with_replacement(range(d), k):
            cols.append(np.prod([u[..., i] for i in c], 0))
    return np.stack(cols, -1)


class Emulator:
    """Gaussian synthetic likelihood with a regression emulator over the design.

    Design: theta_j (N), K episodes each, summaries S (N, K, q). mean mu(theta) = cubic polynomial in u
    (OLS on per-theta means); per-episode covariance Sigma(theta) = D(u) Corr D(u), with variances a
    quadratic regression on the unbiased within-theta variances (floored) and Corr the pooled within-theta
    correlation; emulator error v(u) Sigma_mean (v = x^T (X^T X)^-1 x, Sigma_mean the covariance of
    the per-theta-mean residuals) plus a misfit covariance Bm from 5-fold cross-validation.
    Likelihood of the mean of n episodes: N(s_bar; mu(u), Sigma(u) / n + v(u) Sigma_mean + Bm)."""

    def __init__(self, deg_mean=3, deg_var=2):
        self.dm, self.dv = deg_mean, deg_var

    def _fit_mean(self, U, Sb):
        X = poly_feats(U, self.dm)
        XtX_inv = np.linalg.pinv(X.T @ X)
        beta = XtX_inv @ X.T @ Sb
        return beta, XtX_inv

    def fit(self, U, S, rng=None):
        U, S = np.asarray(U, float), np.asarray(S, float)
        N, K, q = S.shape
        while self.dm > 1 and N < 4 * poly_feats(np.zeros(4), self.dm).shape[0]:
            self.dm -= 1                                    # small designs (smoke test)
        while self.dv > 0 and N < 4 * poly_feats(np.zeros(4), self.dv).shape[0]:
            self.dv -= 1
        Sb = S.mean(1)
        self.beta, self.XtX_inv = self._fit_mean(U, Sb)
        Rm = Sb - poly_feats(U, self.dm) @ self.beta
        self.Sig_mean = np.cov(Rm.T, ddof=self.beta.shape[0]) if N > self.beta.shape[0] + 2 else np.cov(Rm.T)
        D = S - Sb[:, None]
        var_j = (D ** 2).sum(1) / (K - 1)                                    # (N, q) unbiased
        Xv = poly_feats(U, self.dv)
        self.gamma = np.linalg.lstsq(Xv, var_j, rcond=None)[0]
        self.var_floor = 0.1 * var_j.mean(0)
        Zw = D / np.sqrt(np.maximum(self.var(U), 1e-12))[:, None]
        Cw = np.einsum("nki,nkj->ij", Zw, Zw) / (N * (K - 1))
        dd = np.sqrt(np.diag(Cw))
        self.corr = Cw / np.outer(dd, dd)
        # misfit by 5-fold CV over theta points
        rng = rng or np.random.default_rng(0)
        fold = rng.permutation(N) % 5
        R = np.zeros_like(Sb)
        V = np.zeros(N)
        for f in range(5):
            tr, te = fold != f, fold == f
            b, XI = self._fit_mean(U[tr], Sb[tr])
            Xt = poly_feats(U[te], self.dm)
            R[te] = Sb[te] - Xt @ b
            V[te] = np.einsum("ni,ij,nj->n", Xt, XI, Xt)
        Sig_j = self.cov(U)                                                  # (N, q, q)
        E = np.einsum("ni,nj->nij", R, R) - Sig_j / K - V[:, None, None] * self.Sig_mean[None]
        Bm = E.mean(0)
        w, Q = np.linalg.eigh((Bm + Bm.T) / 2)
        self.Bm = (Q * np.maximum(w, 0)) @ Q.T
        tot = Sig_j / K + V[:, None, None] * self.Sig_mean[None] + self.Bm[None]
        chi = np.einsum("ni,nij,nj->n", R, np.linalg.inv(tot), R)
        chi0 = np.einsum("ni,nij,nj->n", R, np.linalg.inv(Sig_j / K + V[:, None, None] * self.Sig_mean[None]), R)
        self.diag = {"N_theta": int(N), "K": int(K), "q": int(q), "cv_chi2_mean_with_misfit": float(chi.mean()),
                     "cv_chi2_mean_without_misfit": float(chi0.mean()), "chi2_expected": float(q),
                     "misfit_sd_over_episode_sd": (np.sqrt(np.diag(self.Bm)) / np.sqrt(var_j.mean(0))).tolist(),
                     "cv_r2_of_mean": (1 - R.var(0) / Sb.var(0)).tolist()}
        return self

    def mean(self, u):
        return poly_feats(u, self.dm) @ self.beta

    def var(self, u):
        return np.maximum(poly_feats(u, self.dv) @ self.gamma, self.var_floor)

    def cov(self, u):
        sd = np.sqrt(self.var(u))
        return sd[..., :, None] * self.corr * sd[..., None, :]

    def emu_var(self, u):
        X = poly_feats(u, self.dm)
        return np.einsum("ni,ij,nj->n", X, self.XtX_inv, X)

    def loglik(self, u, sbar, n):
        u = np.atleast_2d(u)
        mu = self.mean(u)
        S = self.cov(u) / n + self.emu_var(u)[:, None, None] * self.Sig_mean[None] + self.Bm[None]
        r = np.asarray(sbar, float)[None] - mu
        L = np.linalg.cholesky(S)
        z = np.linalg.solve(L, r[..., None])[..., 0]
        return -0.5 * (z ** 2).sum(-1) - np.log(np.diagonal(L, axis1=-2, axis2=-1)).sum(-1) \
            - 0.5 * len(sbar) * math.log(2 * math.pi)


class ViabilityPrior:
    """p_v(u) = P(viable | theta): logistic regression on quadratic monomials of u (L2 penalty),
    fitted by Newton's method on (u, viable) from the viability design."""

    def fit(self, U, y, lam=1e-2, iters=50):
        X = poly_feats(U, 2)
        y = np.asarray(y, float)
        w = np.zeros(X.shape[1])
        P = lam * np.eye(X.shape[1])
        P[0, 0] = 0
        for _ in range(iters):
            p = 1 / (1 + np.exp(-(X @ w)))
            g = X.T @ (p - y) + P @ w
            Hm = (X * (p * (1 - p))[:, None]).T @ X + P + 1e-9 * np.eye(len(w))
            step = np.linalg.solve(Hm, g)
            w -= step
            if np.abs(step).max() < 1e-8:
                break
        self.w = w
        p = 1 / (1 + np.exp(-(X @ w)))
        self.diag = {"n": int(len(y)), "frac_viable": float(y.mean()),
                     "mean_loglik": float(np.mean(y * np.log(p + 1e-12) + (1 - y) * np.log(1 - p + 1e-12)))}
        return self

    def logp(self, u):
        z = poly_feats(u, 2) @ self.w
        return -np.logaddexp(0.0, -z)


def _ess(logw):
    w = np.exp(logw - logw.max())
    return float(w.sum() ** 2 / (w ** 2).sum()), w / w.sum()


def posterior(em, pv, sbar, n, rng, M=100_000, stages=5, target=3000, n_out=4000):
    """Self-normalised importance sampling of p(u | s_bar) on the box [-1, 1]^4 with prior p_v(u):
    stage 0 from the uniform prior box, then multivariate-t (df 5) proposals fitted to the previous
    stage's weighted draws (truncated to the box; the truncation constant cancels). Returns dict with
    n_out resampled draws (u), ESS, mean, sd and the log-density helper."""
    d = len(CEN)
    u = rng.uniform(-1, 1, (M, d))
    logq = np.zeros(M)
    hist = []
    for s in range(stages + 1):
        logw = pv.logp(u) + em.loglik(u, sbar, n) - logq
        ess, w = _ess(logw)
        hist.append(ess)
        if ess >= target or s == stages:
            break
        if ess < 20:                                      # degenerate: moments of the 50 best draws
            top = np.argsort(-logw)[:50]
            mu = u[top].mean(0)
            cov = np.cov(u[top].T) + 1e-4 * np.eye(d)
        else:
            mu = w @ u
            cov = (u - mu).T @ ((u - mu) * w[:, None]) + 1e-6 * np.eye(d)
        cov = cov * (1.5 ** 2)
        L = np.linalg.cholesky(cov)
        df = 5.0
        out = []
        while sum(len(o) for o in out) < M:
            z = rng.standard_normal((M, d)) @ L.T
            g = rng.chisquare(df, M) / df
            x = mu + z / np.sqrt(g)[:, None]
            out.append(x[(np.abs(x) <= 1).all(1)])
        u = np.concatenate(out)[:M]
        Li = np.linalg.inv(L)
        mz = ((u - mu) @ Li.T)
        logq = -0.5 * (df + d) * np.log1p((mz ** 2).sum(1) / df)
    # systematic resampling
    cw = np.cumsum(w)
    pos = (rng.random() + np.arange(n_out)) / n_out
    idx = np.minimum(np.searchsorted(cw, pos), M - 1)
    mean = w @ u
    sd = np.sqrt(np.maximum(w @ (u - mean) ** 2, 0))
    return {"u": u[idx], "ess": ess, "ess_stages": hist, "mean_u": mean, "sd_u": sd, "u_all": u, "w_all": w}


def posterior_checks(post, em, pv, sbar, n, u_true):
    """Marginal PIT of the truth, central-interval coverage flags and the HPD level of the truth
    (fraction of posterior mass with higher unnormalised posterior density than the truth)."""
    u, w = post["u_all"], post["w_all"]
    pit = [(w * (u[:, i] <= u_true[i])).sum() for i in range(len(u_true))]
    lp = lambda x: pv.logp(x) + em.loglik(x, sbar, n)
    lt = lp(np.asarray(u_true)[None])[0]
    hpd = float((w * (lp(u) > lt)).sum())
    return {"pit": [float(p) for p in pit], "hpd_level": hpd,
            "in50": [bool(0.25 <= p <= 0.75) for p in pit], "in90": [bool(0.05 <= p <= 0.95) for p in pit]}


# ----------------------------------------------------------------------------- ridge (pilot.fit_ridge, vectorised)
OFFS = PL.OFFS


def _nbhd_v(F):
    """(..., c, G, G) -> (..., 9 c, G, G): pilot.nbhd over leading axes."""
    return np.concatenate([np.roll(np.roll(F, -dy, -2), -dx, -1) for dy, dx in OFFS], -3)


def _feats_v(y3, us, act=True):
    """y3 (N, 3, 336) lags [t, t-1, t-2]; us (N, NW) -> (N, 64, n_f) as pilot.feats per row."""
    N = len(y3)
    sc = SC1.reshape(3, G, G)
    fs = [_nbhd_v(y3[:, l, :NC].reshape(N, 3, G, G) / sc) for l in range(3)]
    if act:
        fs.append(_nbhd_v(us.reshape(N, 2, G, G) / SIG))
    X = np.concatenate(fs, 1).reshape(N, -1, G * G).transpose(0, 2, 1)
    return np.concatenate([X, np.ones((N, G * G, 1))], 2)


def _feats2_v(y3, us):
    p = GW.population(y3) / SC2                                   # (N, 3, 3)
    nats = 0.5 * (us ** 2).sum(-1) / SIG ** 2
    return np.concatenate([p.reshape(len(y3), -1), (nats / 100.0)[:, None], np.ones((len(y3), 1))], 1)


def fit_ridge(Y, U, hs, lam=1.0, act=True, chunk=4096, max_res=20000, seed=0):
    """pilot.fit_ridge (same windows, features, targets and normal equations), vectorised and chunked;
    the residual tables are subsampled to max_res rows (they are only resampled from)."""
    Y = np.asarray(Y, float)
    U = np.asarray(U, float)
    J, T1, _ = Y.shape
    rng = np.random.default_rng(seed)
    model = {}
    for h in hs:
        jj, tt = np.meshgrid(np.arange(J), np.arange(2, T1 - h), indexing="ij")
        jj, tt = jj.ravel(), tt.ravel()
        CU = np.concatenate([np.zeros((J, 1, U.shape[-1])), np.cumsum(U, 1)], 1)
        AtA = AtB = X2tX2 = X2tT2 = None
        rows = []
        for s in range(0, len(jj), chunk):
            j, t = jj[s:s + chunk], tt[s:s + chunk]
            y3 = np.stack([Y[j, t], Y[j, t - 1], Y[j, t - 2]], 1)
            us = CU[j, t + h] - CU[j, t]
            X1 = _feats_v(y3, us, act)
            T1_ = ((Y[j, t + h, :NC] - Y[j, t, :NC]).reshape(-1, 3, G, G) / SC1.reshape(3, G, G)).reshape(-1, 3, G * G)
            T1_ = T1_.transpose(0, 2, 1)
            A = X1.reshape(-1, X1.shape[-1])
            Bt = T1_.reshape(-1, 3)
            X2 = _feats2_v(y3, us)
            T2 = (GW.population(Y[j, t + h]) - GW.population(Y[j, t])) / SC2
            AtA = A.T @ A if AtA is None else AtA + A.T @ A
            AtB = A.T @ Bt if AtB is None else AtB + A.T @ Bt
            X2tX2 = X2.T @ X2 if X2tX2 is None else X2tX2 + X2.T @ X2
            X2tT2 = X2.T @ T2 if X2tT2 is None else X2tT2 + X2.T @ T2
            rows.append((j, t))
        W1 = np.linalg.solve(AtA + lam * np.eye(AtA.shape[0]), AtB)
        W2 = np.linalg.solve(X2tX2 + lam * np.eye(X2tX2.shape[0]), X2tT2)
        keep = np.sort(rng.choice(len(jj), size=min(max_res, len(jj)), replace=False))
        j, t = jj[keep], tt[keep]
        res1, res2 = [], []
        for s in range(0, len(j), chunk):
            jb, tb = j[s:s + chunk], t[s:s + chunk]
            y3 = np.stack([Y[jb, tb], Y[jb, tb - 1], Y[jb, tb - 2]], 1)
            us = CU[jb, tb + h] - CU[jb, tb]
            X1 = _feats_v(y3, us, act)
            T1_ = ((Y[jb, tb + h, :NC] - Y[jb, tb, :NC]).reshape(-1, 3, G, G) / SC1.reshape(3, G, G)).reshape(-1, 3, G * G)
            T1_ = T1_.transpose(0, 2, 1)
            r1 = T1_ - X1 @ W1                                         # (n, 64, 3)
            res1.append(r1.transpose(0, 2, 1).reshape(len(jb), -1))
            X2 = _feats2_v(y3, us)
            res2.append((GW.population(Y[jb, tb + h]) - GW.population(Y[jb, tb])) / SC2 - X2 @ W2)
        model[h] = (W1, np.concatenate(res1), W2, np.concatenate(res2))
    return model


def ridge_samples(model, items, m, seed, hs1, hs2):
    """Samples for every item with pilot.ridge_predictor: list of {1: (m, len(hs1), 192), 2: (m, len(hs2), 3)}."""
    pred = PL.ridge_predictor(model)
    out = []
    for it in items:
        q = {1: hs1, 2: hs2}
        out.append(pred({**it, "queries": q}, m, seed))
    return out
