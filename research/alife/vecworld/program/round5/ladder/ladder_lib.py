"""ladder_lib -- round 5, study ladder (track 2): difficulty of the gliders wind world as a function of the
observed level and of the number of hidden parameters.

Builds on program/round4/sbi (sbi_lib: VRunner, BatchLab, build_world, Projection, ViabilityPrior, the patch
ridge; the synthetic-likelihood emulator and importance sampler are ported here for any number of
parameters) and on program/track2/gliders_exam (gworld, pilot, viab_joint, the headroom scan). Nothing in
vw1/vw, vw1/port, track2 or round4 is changed; this module imports them.

Cells
  observed view   'block'  the 192 block numbers (Phi_coarse: 3 channels x 8 x 8)
                  'object' the 144 object numbers (Phi_objects: 12 slots x 12 features)
                  'pop'    a level-2 population summary of the object view, 5 numbers per tick:
                           count, tracked mass, mean speed (= gworld.population), sd of body mass, largest body
  hidden set      1: lR;  4: lR, dm_00, ls_00, lh (the round-3 prior);  8: + dm_10, ls_01, dm_01, lA
                  (next in the headroom scan of gliders_exam/results/select.json, group members instead of the
                  pooled dm / ls, each viable at both edges; boxes = the scanned boxes x 0.6, as the 4-box).
The agent of a cell sees only its view (Lab data, item histories), infers from summaries of that view and
predicts that view. The Lab programs and the exam's test programs are built from the full level-1
observation in every cell (classes c and d need the object and the block view).

Scoring is not reimplemented here: per-item fair energy scores come from vw.harness.HistoryExam._per_cell
with vw.scoring.energy_fair (ViewCells restricts the exam to one view's cells), skill from
vw.scoring.skill_report, and the acceptance shares from round5/agentenv/evaluator/acceptance.py (the
functions a Verifiers reward would call).
"""
from __future__ import annotations

import importlib.util
import math
import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
PROG = os.path.dirname(os.path.dirname(HERE))
SBI = os.path.join(PROG, "round4", "sbi")
if SBI not in sys.path:
    sys.path.insert(0, SBI)
import sbi_lib as SL  # noqa: E402

import jax  # noqa: E402
import jax.numpy as jnp  # noqa: E402
import numpy as np  # noqa: E402

from vw.harness import HistoryExam, program_dense  # noqa: E402
from vw.scoring import energy_fair  # noqa: E402

GW, PL = SL.GW, SL.PL
SIG, NW, NC, NO, G = SL.SIG, SL.NW, SL.NC, SL.NO, SL.G
K, NF = GW.K, GW.NF
N_OBS = NC + NO
SC1 = SL.SC1                                   # (192,) public block-view scales
SC2, POP_MEAN = SL.SC2, SL.POP_MEAN            # (3,) public level-2 scales and means

VIEWS = ("block", "object", "pop")
LEVEL = {"block": 1, "object": 2, "pop": 3}    # level keys of the ladder exam (2 and 3 are derived views)
DIM = {"block": NC, "object": NO, "pop": 5}
POP_NAMES = ["count", "tracked_mass", "mean_speed", "mass_sd", "mass_max"]

# ----------------------------------------------------------------------------- hidden-parameter sets
SCAN_BOX = {"lR": (0.85, 1.15), "dm_00": (-0.25, 0.25), "ls_00": (0.85, 1.15), "lh": (0.85, 1.15),
            "dm_10": (-0.25, 0.25), "ls_01": (0.85, 1.15), "dm_01": (-0.25, 0.25), "lA": (0.75, 1.25)}
SHRINK = 0.6                                    # gliders_exam/results/prior.json ("shrink")
SETS = {1: ["lR"], 4: ["lR", "dm_00", "ls_00", "lh"],
        8: ["lR", "dm_00", "ls_00", "lh", "dm_10", "ls_01", "dm_01", "lA"]}
DMAX = 8


def box(n: int, extra_shrink: float = 1.0):
    """(names, lo, hi) of the prior box with n hidden parameters. The first 4 boxes are the round-3 prior
    (prior.json); parameters 5-8 use the scanned box x 0.6 x extra_shrink around the default."""
    names = SETS[int(n)]
    lo, hi = [], []
    for j, k in enumerate(names):
        a, b = SCAN_BOX[k]
        c, hw = (a + b) / 2, (b - a) / 2 * SHRINK * (extra_shrink if j >= 4 else 1.0)
        lo.append(c - hw)
        hi.append(c + hw)
    lo, hi = np.array(lo), np.array(hi)
    if n >= 4:
        assert np.allclose(lo[:4], SL.LO) and np.allclose(hi[:4], SL.HI), "first 4 boxes must equal prior.json"
    return names, lo, hi


def pad_u(u):
    """(..., d) box units -> (..., DMAX) zero-padded (parameters not hidden sit at their default, u = 0)."""
    u = np.asarray(u, np.float32)
    out = np.zeros(u.shape[:-1] + (DMAX,), np.float32)
    out[..., :u.shape[-1]] = u
    return out


_P_DEF = None


def params_batch(names, thetas) -> dict:
    """Stacked parameter pytree (leading axis B) for theta rows (B, d) in `names` order; equals
    gworld.stack_params([gworld.theta_to_params(dict(zip(names, t))) for t in thetas]) for any names."""
    global _P_DEF
    th = np.atleast_2d(np.asarray(thetas, float))
    B = th.shape[0]
    unknown = set(names) - set(GW.DEFAULT)
    if unknown:
        raise KeyError(f"unknown hidden parameters {sorted(unknown)}")
    if _P_DEF is None:
        _P_DEF = {k: np.asarray(v) for k, v in GW.theta_to_params({}).items()}
    t = {k: np.full(B, float(v)) for k, v in GW.DEFAULT.items()}
    for k, col in zip(names, th.T):
        t[k] = col
    m0, s0, h0 = (np.asarray(GW.P0[q], float) for q in "msh")
    dm = np.repeat(t["dm"][:, None], 20, 1)
    lh = np.repeat(t["lh"][:, None], 20, 1)
    ls = np.repeat(t["ls"][:, None], 20, 1)
    for g, idx in GW.GROUPS.items():
        dm[:, idx] += t[f"dm_{g}"][:, None]
        lh[:, idx] *= t[f"lh_{g}"][:, None]
        ls[:, idx] *= t[f"ls_{g}"][:, None]
    out = {k: np.broadcast_to(v, (B,) + v.shape).copy() for k, v in _P_DEF.items()}
    out["R"] = (float(GW.P0["R"]) + 15.0) * t["lR"] - 15.0
    out["m"] = m0[None] + dm * s0[None]
    out["s"] = s0[None] * ls
    out["h"] = h0[None] * lh
    out["theta_A"] = 2.0 * t["lA"]
    out["n"] = t["n"]
    out["gw"] = t["gw"]
    return {k: jnp.asarray(v) for k, v in out.items()}


# ----------------------------------------------------------------------------- views
def objects(obs):
    return np.asarray(obs)[..., NC:NC + NO]


def pop5(obs):
    """Level-2 population summary of the object view: obs (..., 336) -> (..., 5) = (count, tracked mass,
    mean speed, sd of body mass, largest body mass). The first three are gworld.population."""
    S = np.asarray(obs, float)[..., NC:NC + NO]
    S = S.reshape(S.shape[:-1] + (K, NF))
    pr = S[..., 0] > 0.5
    n = pr.sum(-1).astype(float)
    nn = np.maximum(n, 1.0)
    mass = np.where(pr, S[..., 1], 0.0)
    msum = mass.sum(-1)
    sp = np.where(pr, np.hypot(S[..., 10], S[..., 11]), 0.0).sum(-1) / nn
    mean = msum / nn
    msd = np.sqrt(np.maximum(np.where(pr, (S[..., 1] - mean[..., None]) ** 2, 0.0).sum(-1) / nn, 0.0))
    return np.stack([n, msum, sp, msd, mass.max(-1)], -1)


DERIVED = {1: GW.coarse, 2: objects, 3: pop5}


def view_of(view, obs):
    return np.asarray(DERIVED[LEVEL[view]](obs))


def public_scales(obs) -> dict:
    """Public scales of the two views that had none, from public no-input simulations at the prior mean:
    obs (E, T1, 336). object: per-feature SD pooled over slots, ticks and episodes (absent slots are zeros;
    slots are exchangeable), tiled over the 12 slots; pop: gliders_exam's level-2 scales and means for the
    first 3 numbers, SD and mean over ticks and episodes for the other 2."""
    O = objects(obs).reshape(-1, K, NF).astype(float)
    scf = np.maximum(O.reshape(-1, NF).std(0), 1e-6)
    p = pop5(obs).reshape(-1, 5)
    scp = np.concatenate([SC2, np.maximum(p[:, 3:].std(0), 1e-6)])
    popm = np.concatenate([POP_MEAN, p[:, 3:].mean(0)])
    return {"SCF": scf, "SCO": np.tile(scf, K), "SCP": scp, "POPM": popm, "SC1": SC1,
            "check_pop3_sd_here": p[:, :3].std(0), "check_pop3_mean_here": p[:, :3].mean(0)}


def scales_of(view, SC):
    return {"block": SC["SC1"], "object": SC["SCO"], "pop": SC["SCP"]}[view]


def slot_blocks(O):
    """Flat block index (row * G + col) of every slot: O (..., K, NF) -> (..., K) int (0 where absent)."""
    Hpx = GW.H
    cx = (np.arctan2(O[..., 4], O[..., 3]) * Hpx / (2 * np.pi)) % Hpx
    cy = (np.arctan2(O[..., 6], O[..., 5]) * Hpx / (2 * np.pi)) % Hpx
    b = Hpx // G
    return ((np.floor(cy / b).astype(int) % G) * G + np.floor(cx / b).astype(int) % G) * (O[..., 0] > 0.5)


# ----------------------------------------------------------------------------- programs
def cls_blind_eq(rng, hist, H, left, C=PL.C_AIM, T_in=GW.T_IN, k=8):
    """Class e, the blind twin of the aimed push (class c): the same nats (C in all, C / T_in per tick),
    the same ticks (0 .. T_in - 1) and the same number of coefficients per tick (8), but at random
    coefficients with random amplitudes instead of on the fastest body."""
    U = np.zeros((H, NW))
    c_t = min(C, left) / T_in
    for t in range(min(T_in, H)):
        idx = rng.choice(NW, size=k, replace=False)
        v = rng.standard_normal(k)
        v *= math.sqrt(2 * c_t * SIG ** 2 / float((v ** 2).sum())) * (1 - 1e-9)
        U[t, idx] = np.clip(v, -0.99, 0.99)
    return PL.dense_to_prog(U)


CLASSES = dict(PL.MIX.classes)
CLASSES["e"] = cls_blind_eq
MIXC = ("a", "b", "c", "d")                    # the public exam mix
ARMS = {"mix": MIXC, "passive": ("a",), "blind": ("e",), "aimed": ("c",), "regional": ("d",)}


def sim_episodes(RN, names, thetas, keys, seed, P=16, H=16, chunk=256, classes=None, log=None):
    """sbi_lib.sim_episodes for any hidden set and with class e: per member theta (B, d) in `names` order,
    keys (B,) typed; init + burn-in, P ticks without input, then a test program of class classes[b]
    built from the quantised o(0..P). Returns obs (B, P+H+1, 336) float32, U (B, P+H, NW) float32, cls, nats."""
    th = np.atleast_2d(np.asarray(thetas, float))
    B = len(th)
    rng0 = np.random.default_rng([int(seed), 0])
    if classes is None:
        classes = rng0.choice(list(MIXC), size=B)
    classes = np.asarray(classes)
    OBS = np.zeros((B, P + H + 1, N_OBS), np.float32)
    UU = np.zeros((B, P + H, NW), np.float32)
    nats = np.zeros(B)
    for s in range(0, B, chunk):
        e = min(s + chunk, B)
        nb = e - s
        Pp = params_batch(names, SL._pad(th[s:e], chunk))
        k = SL._pad_keys(keys[s:e], chunk)
        sig = jnp.full((chunk,), SIG)
        A, m = RN.init_burn(Pp, k, sig)
        kd = GW.dyn_keys(k)
        y1, _, _, A, m = RN.run(Pp, A, m, kd, jnp.zeros((chunk,), jnp.int64), jnp.zeros((chunk, P, NW)), sig)
        y1 = SL.quantize(np.asarray(y1)[:nb])
        U = np.zeros((chunk, H, NW))
        for b in range(nb):
            prog = CLASSES[classes[s + b]](np.random.default_rng([int(seed), 1, s + b]), y1[b], H, SL.EP_CAP)
            U[b] = program_dense(prog, H, NW)
            nats[s + b] = GW.nats_of(U[b])
        y2, _, _, A, m = RN.run(Pp, A, m, kd, jnp.full((chunk,), P, jnp.int64), jnp.asarray(U), sig)
        y2 = SL.quantize(np.asarray(y2)[:nb])
        OBS[s:e] = np.concatenate([y1, y2[:, 1:]], 1)
        UU[s:e, P:] = U[:nb]
        if log:
            log(f"  sim_episodes {e}/{B}")
    return {"obs": OBS, "U": UU, "cls": classes, "nats": nats}


# ----------------------------------------------------------------------------- summary statistics per view
_BASE = {"block": ["mass_c0", "mass_c1", "log_m2_mean", "log_sd_c0", "log_sd_c1", "corr_c0c1", "log_sd_m2",
                   "log_dC1", "log_dC4", "log_max_m2"],
         "object": ["count_mean", "count_sd", "count_absdiff", "log_mass_body", "mass_cv", "frac_c1", "log_rg",
                    "aniso", "speed_mean", "speed_sd", "log_tracked_mass", "log_density"]}
FEATS = {"block": _BASE["block"] + ["resp_flux", "d_log_sd_m2", "d_log_dC1"],
         "object": _BASE["object"] + ["resp_v", "d_speed", "d_count"],
         "pop": ["count_mean", "log_mass", "speed_mean", "log_mass_sd", "log_mass_max", "count_sd",
                 "count_absdiff", "speed_tsd", "log_dmass", "d_speed", "d_count", "d_log_mass_max"]}


def _lg(x):
    return np.log(np.maximum(x, 1e-6))


def view_features(view, obs, U, P) -> np.ndarray:
    """Per-episode summaries that use the observed view only: obs (B, T1, 336), U (B, T1 - 1, NW), program
    from tick P. The base statistics are sbi_lib.episode_features columns (block: those of the block
    numbers; object: those of the object numbers); the others are responses to the program (zero without
    input): block 'resp_flux' = regression of the block-mass change over the program on the convergence of
    (block mass at P) x (summed wind); object 'resp_v' = regression of the bodies' velocity change over the
    first 4 program ticks on the summed wind at their block; 'd_*' = program window minus prefix."""
    y = np.asarray(obs, float)
    U = np.asarray(U, float)
    B, T1, _ = y.shape
    W = U[:, P:].sum(1).reshape(B, 2, G, G) / SIG                       # summed wind, units of sigma_w
    pre, win = slice(0, P + 1), slice(P + 1, T1)
    if view in ("block", "object"):
        F = SL.episode_features(y)
        base = F[:, [SL.FEATURES.index(k) for k in _BASE[view]]]
    if view == "block":
        C = y[..., :NC].reshape(B, T1, 3, G, G) / SC1.reshape(3, G, G)
        M = C[:, :, 0] + C[:, :, 1]
        fy, fx = M[:, P] * W[:, 0], M[:, P] * W[:, 1]
        conv = -((np.roll(fy, -1, 1) - np.roll(fy, 1, 1)) / 2 + (np.roll(fx, -1, 2) - np.roll(fx, 1, 2)) / 2)
        resp = ((M[:, -1] - M[:, P]) * conv).sum((1, 2)) / ((conv ** 2).sum((1, 2)) + 1.0)
        sd2 = _lg(C[:, :, 2].std((2, 3)))
        dC = _lg(np.sqrt(((C[:, 1:] - C[:, :-1]) ** 2).mean((2, 3, 4))))
        extra = [resp, sd2[:, win].mean(1) - sd2[:, pre].mean(1), dC[:, P:].mean(1) - dC[:, :P].mean(1)]
        return np.concatenate([base, np.stack(extra, 1)], 1)
    O = y[..., NC:N_OBS].reshape(B, T1, K, NF)
    if view == "object":
        t1 = min(P + GW.T_IN, T1 - 1)
        both = (O[:, P, :, 0] > 0.5) & (O[:, t1, :, 0] > 0.5)
        blk = slot_blocks(O[:, P])                                       # (B, K)
        Wt = U[:, P:t1].sum(1).reshape(B, 2, G * G) / SIG
        wy = np.take_along_axis(Wt[:, 0], blk, 1)
        wx = np.take_along_axis(Wt[:, 1], blk, 1)
        dvx, dvy = O[:, t1, :, 10] - O[:, P, :, 10], O[:, t1, :, 11] - O[:, P, :, 11]
        resp = (both * (dvx * wx + dvy * wy)).sum(1) / ((both * (wx ** 2 + wy ** 2)).sum(1) + 1.0)
        pres = O[..., 0] > 0.5
        n = pres.sum(-1).astype(float)
        spd = np.where(pres, np.hypot(O[..., 10], O[..., 11]), 0.0).sum(-1) / np.maximum(n, 1.0)
        extra = [resp, spd[:, win].mean(1) - spd[:, pre].mean(1), n[:, win].mean(1) - n[:, pre].mean(1)]
        return np.concatenate([base, np.stack(extra, 1)], 1)
    p = pop5(y)                                                           # (B, T1, 5)
    f = [p[..., 0].mean(1), _lg(p[..., 1]).mean(1), p[..., 2].mean(1), np.log1p(p[..., 3]).mean(1),
         _lg(p[..., 4]).mean(1), p[..., 0].std(1), np.abs(np.diff(p[..., 0], axis=1)).mean(1), p[..., 2].std(1),
         np.log(np.abs(np.diff(p[..., 1], axis=1)).mean(1) + 1e-3),
         p[:, win, 2].mean(1) - p[:, pre, 2].mean(1), p[:, win, 0].mean(1) - p[:, pre, 0].mean(1),
         _lg(p[:, win, 4]).mean(1) - _lg(p[:, pre, 4]).mean(1)]
    return np.stack(f, 1)


# ----------------------------------------------------------------------------- synthetic likelihood, d parameters
poly_feats = SL.poly_feats


def n_terms(d, deg):
    return math.comb(d + deg, deg)


class Emulator:
    """sbi_lib.Emulator for any number of parameters d (same model: polynomial mean, quadratic variance
    regression, pooled within-theta correlation, emulator-error and cross-validated misfit covariance).
    The mean's degree (1-3) is the one with the smallest 5-fold cross-validated error among those with at
    least 3 design points per coefficient."""

    def __init__(self, deg_mean=3, deg_var=2):
        self.dm_max, self.dv = deg_mean, deg_var

    @staticmethod
    def _fit_mean(U, Sb, deg):
        X = poly_feats(U, deg)
        XtX_inv = np.linalg.pinv(X.T @ X)
        return XtX_inv @ X.T @ Sb, XtX_inv

    def _cv(self, U, Sb, deg, fold):
        R = np.zeros_like(Sb)
        V = np.zeros(len(U))
        for f in range(5):
            tr, te = fold != f, fold == f
            if not te.any() or tr.sum() < 2:
                continue
            b, XI = self._fit_mean(U[tr], Sb[tr], deg)
            Xt = poly_feats(U[te], deg)
            R[te] = Sb[te] - Xt @ b
            V[te] = np.einsum("ni,ij,nj->n", Xt, XI, Xt)
        return R, V

    def fit(self, U, S, rng=None):
        U, S = np.asarray(U, float), np.asarray(S, float)
        N, Kk, q = S.shape
        self.d = d = U.shape[1]
        rng = rng or np.random.default_rng(0)
        fold = rng.permutation(N) % 5
        Sb = S.mean(1)
        degs = [g for g in range(1, self.dm_max + 1) if g == 1 or N >= 3 * n_terms(d, g)]
        cv = {}
        for g in degs:
            R, V = self._cv(U, Sb, g, fold)
            cv[g] = (float(((R ** 2).mean(0) / np.maximum(Sb.var(0), 1e-30)).mean()), R, V)
        self.dm = min(cv, key=lambda g: cv[g][0])
        while self.dv > 0 and N < 4 * n_terms(d, self.dv):
            self.dv -= 1
        self.beta, self.XtX_inv = self._fit_mean(U, Sb, self.dm)
        Rm = Sb - poly_feats(U, self.dm) @ self.beta
        ddof = self.beta.shape[0] if N > self.beta.shape[0] + 2 else 1
        self.Sig_mean = np.atleast_2d(np.cov(Rm.T, ddof=ddof))
        D = S - Sb[:, None]
        var_j = (D ** 2).sum(1) / max(Kk - 1, 1)
        Xv = poly_feats(U, self.dv)
        self.gamma = np.linalg.lstsq(Xv, var_j, rcond=None)[0]
        self.var_floor = np.maximum(0.1 * var_j.mean(0), 1e-12)
        Zw = D / np.sqrt(self.var(U))[:, None]
        Cw = np.einsum("nki,nkj->ij", Zw, Zw) / (N * max(Kk - 1, 1))
        dd = np.sqrt(np.maximum(np.diag(Cw), 1e-12))
        self.corr = Cw / np.outer(dd, dd)
        _, R, V = cv[self.dm]
        Sig_j = self.cov(U)
        E = np.einsum("ni,nj->nij", R, R) - Sig_j / Kk - V[:, None, None] * self.Sig_mean[None]
        Bm = E.mean(0)
        w, Q = np.linalg.eigh((Bm + Bm.T) / 2)
        self.Bm = (Q * np.maximum(w, 0)) @ Q.T
        self.jit = 1e-9 * np.eye(q) * max(float(np.trace(Sig_j.mean(0))) / q, 1e-12)
        tot = Sig_j / Kk + V[:, None, None] * self.Sig_mean[None] + self.Bm[None] + self.jit
        chi = np.einsum("ni,nij,nj->n", R, np.linalg.inv(tot), R)
        self.diag = {"N_theta": int(N), "K": int(Kk), "q": int(q), "d": int(d), "deg_mean": int(self.dm),
                     "deg_var": int(self.dv), "cv_rel_err_by_degree": {str(g): cv[g][0] for g in cv},
                     "cv_chi2_mean_with_misfit": float(chi.mean()), "chi2_expected": float(q),
                     "cv_r2_of_mean": (1 - R.var(0) / np.maximum(Sb.var(0), 1e-30)).tolist(),
                     "misfit_sd_over_episode_sd": (np.sqrt(np.diag(self.Bm)) / np.sqrt(var_j.mean(0))).tolist()}
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
        S = self.cov(u) / n + self.emu_var(u)[:, None, None] * self.Sig_mean[None] + self.Bm[None] + self.jit
        r = np.asarray(sbar, float)[None] - self.mean(u)
        L = np.linalg.cholesky(S)
        z = np.linalg.solve(L, r[..., None])[..., 0]
        return -0.5 * (z ** 2).sum(-1) - np.log(np.diagonal(L, axis1=-2, axis2=-1)).sum(-1) \
            - 0.5 * len(sbar) * math.log(2 * math.pi)


def posterior(em, pv, sbar, n, rng, M=40_000, stages=6, target=1500, n_out=2000):
    """sbi_lib.posterior on the box [-1, 1]^d for any d: self-normalised importance sampling with prior
    p_v(u); stage 0 from the uniform box, then truncated multivariate-t (df 5) proposals fitted to the
    previous stage's weighted draws."""
    d = em.d
    u = rng.uniform(-1, 1, (M, d))
    logq = np.zeros(M)
    hist = []
    for s in range(stages + 1):
        logw = pv.logp(u) + em.loglik(u, sbar, n) - logq
        ess, w = SL._ess(logw)
        hist.append(ess)
        if ess >= target or s == stages:
            break
        if ess < 20:
            top = np.argsort(-logw)[:50]
            mu = u[top].mean(0)
            cov = np.atleast_2d(np.cov(u[top].T)) + 1e-4 * np.eye(d)
        else:
            mu = w @ u
            cov = (u - mu).T @ ((u - mu) * w[:, None]) + 1e-6 * np.eye(d)
        cov = cov * (1.5 ** 2)
        L = np.linalg.cholesky(cov)
        df = 5.0
        out, tries = [], 0
        while sum(len(o) for o in out) < M and tries < 200:
            z = rng.standard_normal((M, d)) @ L.T
            g = rng.chisquare(df, M) / df
            x = mu + z / np.sqrt(g)[:, None]
            out.append(x[(np.abs(x) <= 1).all(1)])
            tries += 1
        got = np.concatenate(out)[:M]
        if len(got) < M:                                    # proposal almost outside the box: keep the old draws
            break
        u = got
        mz = (u - mu) @ np.linalg.inv(L).T
        logq = -0.5 * (df + d) * np.log1p((mz ** 2).sum(1) / df)
    cw = np.cumsum(w)
    pos = (rng.random() + np.arange(n_out)) / n_out
    idx = np.minimum(np.searchsorted(cw, pos), len(w) - 1)
    mean = w @ u
    sd = np.sqrt(np.maximum(w @ (u - mean) ** 2, 0))
    return {"u": u[idx], "ess": ess, "ess_stages": hist, "mean_u": mean, "sd_u": sd, "u_all": u, "w_all": w}


def prior_draws(pv, d, n, rng, M=200_000):
    """Draws from the viability-conditioned prior (box draws resampled with weights p_v) and its moments."""
    ub = rng.uniform(-1, 1, (M, d))
    wb = np.exp(pv.logp(ub))
    wb /= wb.sum()
    pm = wb @ ub
    psd = np.sqrt(wb @ (ub - pm) ** 2)
    return ub[rng.choice(M, size=n, p=wb)], pm, psd


# ----------------------------------------------------------------------------- data-only ridges per view
def block_ridge(obs, U, hs):
    return SL.fit_ridge(obs, U, sorted(hs))


def block_ridge_samples(model, items, m, seed, hs):
    pred = PL.ridge_predictor(model)
    return np.stack([pred({**it, "queries": {1: list(hs)}}, m, seed)[1] for it in items])    # (n, m, nh, 192)


def _slot_feats(O3, w, pthr):
    """O3 (N, 3, K, NF) scaled lags [t, t-1, t-2]; w (N, K, 2) summed wind at the slot's block (sigma_w
    units) -> X (N, K, 52), present (N, K)."""
    N = O3.shape[0]
    pres = O3[:, 0, :, 0] > pthr
    cnt = pres.sum(1, keepdims=True).astype(float)
    ctx = (O3[:, 0] * pres[..., None]).sum(1) / np.maximum(cnt, 1.0)
    X = np.concatenate([O3.transpose(0, 2, 1, 3).reshape(N, K, 3 * NF), w,
                        np.broadcast_to(ctx[:, None], (N, K, NF)),
                        np.broadcast_to((cnt / K)[:, None], (N, K, 1)), np.ones((N, K, 1))], -1)
    return X, pres


def _slot_rows(Os, blk, CU, j, t, h, pthr):
    O3 = np.stack([Os[j, t], Os[j, t - 1], Os[j, t - 2]], 1)
    us = CU[j, t + h] - CU[j, t]                                           # (N, 2, GG)
    b = blk[j, t]
    w = np.stack([np.take_along_axis(us[:, 0], b, 1), np.take_along_axis(us[:, 1], b, 1)], -1)
    return _slot_feats(O3, w, pthr)


def slot_ridge(obs, U, hs, SCF, lam=1.0, max_res=20000, seed=0):
    """Data-only ridge for the object view, shared over slots: change of a slot's 12 scaled features over h
    ticks on its features at 3 lags, the program's summed wind at its block, the mean present slot and the
    count; separate weights for slots present / absent at the anchor; empirical residual rows per group."""
    Os = (objects(obs).astype(float).reshape(obs.shape[0], obs.shape[1], K, NF)) / SCF
    blk = slot_blocks(Os * SCF)
    Ug = np.asarray(U, float).reshape(U.shape[0], U.shape[1], 2, G * G) / SIG
    CU = np.concatenate([np.zeros_like(Ug[:, :1]), np.cumsum(Ug, 1)], 1)
    J, T1 = Os.shape[:2]
    pthr = 0.5 / SCF[0]
    rng = np.random.default_rng(seed)
    model = {}
    for h in hs:
        jj, tt = np.meshgrid(np.arange(J), np.arange(2, T1 - h), indexing="ij")
        jj, tt = jj.ravel(), tt.ravel()
        X, pres = _slot_rows(Os, blk, CU, jj, tt, h, pthr)
        Tg = Os[jj, tt + h] - Os[jj, tt]                                   # (N, K, NF)
        out = []
        for grp in (True, False):
            sel = pres == grp
            A, Bt = X[sel], Tg[sel]
            if len(A) == 0:
                A, Bt = np.zeros((1, X.shape[-1])), np.zeros((1, NF))
            Wt = np.linalg.solve(A.T @ A + lam * np.eye(A.shape[1]), A.T @ Bt)
            res = Bt - A @ Wt
            if len(res) > max_res:
                res = res[rng.choice(len(res), max_res, replace=False)]
            out += [Wt, res]
        model[h] = tuple(out)
    return model


def slot_ridge_samples(model, items, m, seed, hs, SCF):
    """(n_items, m, len(hs), 144) in the object view's units."""
    hist = np.stack([np.asarray(it["history"], float) for it in items])
    n, P1, _ = hist.shape
    Os = objects(hist).reshape(n, P1, K, NF) / SCF
    blk = slot_blocks(Os * SCF)
    Hm = max(hs)
    Up = np.stack([program_dense(it["program"], Hm, NW) for it in items]).reshape(n, Hm, 2, G * G) / SIG
    CU = np.concatenate([np.zeros_like(Up[:, :1]), np.cumsum(Up, 1)], 1)
    pthr = 0.5 / SCF[0]
    t = P1 - 1
    out = np.zeros((n, m, len(hs), K * NF))
    for a, h in enumerate(hs):
        Wp, rp, Wa, ra = model[h]
        O3 = np.stack([Os[:, t], Os[:, t - 1], Os[:, t - 2]], 1)
        us = CU[:, h]
        b = blk[:, t]
        w = np.stack([np.take_along_axis(us[:, 0], b, 1), np.take_along_axis(us[:, 1], b, 1)], -1)
        X, pres = _slot_feats(O3, w, pthr)
        mu = np.where(pres[..., None], X @ Wp, X @ Wa)                    # (n, K, NF)
        for i in range(n):
            rng = np.random.default_rng([seed, int(items[i]["id"]) % (2 ** 32), h])
            r = np.where(pres[i][None, :, None], rp[rng.integers(0, len(rp), (m, K))],
                         ra[rng.integers(0, len(ra), (m, K))])
            out[i, :, a] = ((Os[i, t] + mu[i])[None] + r).reshape(m, -1) * np.tile(SCF, K)
    return out


def pop_ridge(obs, U, hs, SCP, POPM, lam=1.0, max_res=20000, seed=0):
    """Data-only ridge for the population view: change of the 5 scaled numbers over h ticks on 3 lags and
    the program's nats over the window; empirical residual vectors."""
    p = (pop5(obs) - POPM) / SCP
    nt = 0.5 * (np.asarray(U, float) ** 2).sum(-1) / SIG ** 2 / 100.0
    CN = np.concatenate([np.zeros((len(nt), 1)), np.cumsum(nt, 1)], 1)
    J, T1 = p.shape[:2]
    rng = np.random.default_rng(seed)
    model = {}
    for h in hs:
        jj, tt = np.meshgrid(np.arange(J), np.arange(2, T1 - h), indexing="ij")
        jj, tt = jj.ravel(), tt.ravel()
        X = np.concatenate([p[jj, tt], p[jj, tt - 1], p[jj, tt - 2], (CN[jj, tt + h] - CN[jj, tt])[:, None],
                            np.ones((len(jj), 1))], 1)
        Tg = p[jj, tt + h] - p[jj, tt]
        Wt = np.linalg.solve(X.T @ X + lam * np.eye(X.shape[1]), X.T @ Tg)
        res = Tg - X @ Wt
        if len(res) > max_res:
            res = res[rng.choice(len(res), max_res, replace=False)]
        model[h] = (Wt, res)
    return model


def pop_ridge_samples(model, items, m, seed, hs, SCP, POPM):
    hist = np.stack([np.asarray(it["history"], float) for it in items])
    n = len(hist)
    praw = pop5(hist)
    p = (praw - POPM) / SCP
    Hm = max(hs)
    Up = np.stack([program_dense(it["program"], Hm, NW) for it in items])
    CN = np.concatenate([np.zeros((n, 1)), np.cumsum(0.5 * (Up ** 2).sum(-1) / SIG ** 2 / 100.0, 1)], 1)
    out = np.zeros((n, m, len(hs), 5))
    for a, h in enumerate(hs):
        Wt, res = model[h]
        X = np.concatenate([p[:, -1], p[:, -2], p[:, -3], CN[:, h][:, None], np.ones((n, 1))], 1)
        mu = X @ Wt
        for i in range(n):
            rng = np.random.default_rng([seed, int(items[i]["id"]) % (2 ** 32), h])
            out[i, :, a] = praw[i, -1] + (mu[i][None] + res[rng.integers(0, len(res), m)]) * SCP
    return out


def ridge_fit(view, obs, U, hs, SC):
    if view == "block":
        return block_ridge(obs, U, hs)
    if view == "object":
        return slot_ridge(obs, U, hs, SC["SCF"])
    return pop_ridge(obs, U, hs, SC["SCP"], SC["POPM"])


def ridge_samples(view, model, items, m, seed, hs, SC):
    if view == "block":
        return block_ridge_samples(model, items, m, seed, hs)
    if view == "object":
        return slot_ridge_samples(model, items, m, seed, hs, SC["SCF"])
    return pop_ridge_samples(model, items, m, seed, hs, SC["SCP"], SC["POPM"])


# ----------------------------------------------------------------------------- scoring through the exam's scorer
class ViewCells:
    """A HistoryExam restricted to the cells of one level: the same truths, scales and scorer
    (HistoryExam._per_cell with vw.scoring.energy_fair), so no score is computed outside the library."""
    _per_cell = HistoryExam._per_cell

    def __init__(self, ex, level):
        self.n, self.level = ex.n, int(level)
        self.queries = {self.level: ex.queries[self.level]}
        self.truths, self.scales = ex.truths, ex.scales
        self.cells = [(self.level, t) for t in ex.queries[self.level]]

    def score(self, S):
        """S (n_items, m, n_times, d) samples in the level's units -> fair energy score (n_items, n_times)."""
        S = np.asarray(S, float)
        want = (self.n, S.shape[1], len(self.queries[self.level]), self.truths[self.level].shape[-1])
        if S.shape != want:
            raise ValueError(f"samples have shape {S.shape}, expected {want}")
        if not np.all(np.isfinite(S)):
            raise ValueError("non-finite samples")
        smp = [{self.level: S[i]} for i in range(self.n)]
        return self._per_cell(lambda X, Y, s, l: energy_fair(X, Y, s), samples=smp)


def view_columns(ex, level):
    return [j for j, (l, _) in enumerate(ex.cells) if l == level]


def load_acceptance():
    """round5/agentenv/evaluator/acceptance.py (sigma, rho) loaded by path: the evaluator package itself
    pulls in the Lab service, which this study does not need."""
    f = os.path.join(PROG, "round5", "agentenv", "evaluator", "acceptance.py")
    spec = importlib.util.spec_from_file_location("agentenv_acceptance", f)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
