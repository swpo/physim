"""vxsbi -- scripted inference of the hidden parameters of the fed-vortex exam pilot (synthetic likelihood).

The numerical classes (Projection, Emulator, ViabilityPrior, posterior, posterior_checks, poly_feats) are those of
round4/sbi/sbi_lib.py (gliders), copied with the number of parameters d taken from the data instead of fixed at 4;
nothing else in them is changed. New here: the episode summary features of the vortex world.

Box units: u = (theta - centre) / half-width in [-1, 1]^d.
"""
from __future__ import annotations

import itertools
import math

import numpy as np


# ----------------------------------------------------------------------------- episode features
def _lgt(p):
    p = np.clip(p, 0.02, 0.98)
    return np.log(p / (1 - p))


WINDOWS = ((60, 130), (130, 200), (200, 270), (270, 341))


def episode_features(S, names, level=1):
    """Per-episode summary statistics from the per-tick level-1 summaries S (E, T+1, n) (vxlib.S2_NAMES).
    level=1: statistics of the vortex list; level=2: functions of (N, s_b) only.
    Returns (F (E, nf), feature names)."""
    S = np.asarray(S, float)
    ix = {n: i for i, n in enumerate(names)}
    T1 = S.shape[1]
    wins = [(a, min(b, T1)) for a, b in WINDOWS if a < T1 - 1]
    cols, lab = [], []

    def add(name, v):
        cols.append(v)
        lab.append(name)
    pre = (20, min(60, T1))
    add("N_pre", S[:, pre[0]:pre[1], ix["N"]].mean(1))
    for k, (a, b) in enumerate(wins):
        add(f"N_w{k}", S[:, a:b, ix["N"]].mean(1))
        add(f"sb_w{k}", S[:, a:b, ix["s_b"]].mean(1))
        add(f"lgt_sb_w{k}", _lgt(S[:, a:b, ix["s_b"]].mean(1)))
    add("N_sd", S[:, 60:, ix["N"]].std(1))
    add("N_absdiff", np.abs(np.diff(S[:, 60:, ix["N"]], axis=1)).mean(1))
    add("sb_absdiff", np.abs(np.diff(S[:, 60:, ix["s_b"]], axis=1)).mean(1))
    if level == 1:
        for nm in ("log_mass_mean", "speed_mean", "rg_mean", "turnover", "mass_cv", "log_mass_tot"):
            add(f"{nm}_pre", S[:, pre[0]:pre[1], ix[nm]].mean(1))
        for k, (a, b) in enumerate(wins):
            for nm in ("fb_mass", "fb_sd", "mixed", "log_mass_mean", "speed_mean", "rg_mean", "turnover", "mass_cv"):
                add(f"{nm}_w{k}", S[:, a:b, ix[nm]].mean(1))
            add(f"lgt_fb_mass_w{k}", _lgt(S[:, a:b, ix["fb_mass"]].mean(1)))
    return np.nan_to_num(np.stack(cols, 1), nan=0.0, posinf=0.0, neginf=0.0), lab


# ----------------------------------------------------------------------------- from round4/sbi/sbi_lib.py
def poly_feats(u, deg):
    """Monomials of u (..., d) up to total degree deg (1, u_i, u_i u_j, ...)."""
    u = np.asarray(u, float)
    d = u.shape[-1]
    cols = [np.ones(u.shape[:-1])]
    for k in range(1, deg + 1):
        for c in itertools.combinations_with_replacement(range(d), k):
            cols.append(np.prod([u[..., i] for i in c], 0))
    return np.stack(cols, -1)


class Projection:
    """Linear regression summaries (Fearnhead & Prangle 2012): s = W^T z(f) + b, z = standardised
    features, fitted by ridge regression of u on z over the design."""

    def fit(self, F, U, lam=1e-2):
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

    def state(self, feature_names=None):
        return {"mu": self.mu.tolist(), "sd": self.sd.tolist(), "W": self.W.tolist(), "r2_per_param": self.r2,
                "features": feature_names}


class Emulator:
    """Gaussian synthetic likelihood with a regression emulator over the design (sbi_lib.Emulator).

    Design: theta_j (N), K episodes each, summaries S (N, K, q). mean mu(theta) = polynomial in u (OLS on
    per-theta means); per-episode covariance Sigma(theta) = D(u) Corr D(u), with variances a polynomial
    regression on the unbiased within-theta variances (floored) and Corr the pooled within-theta correlation;
    emulator error v(u) Sigma_mean plus a misfit covariance Bm from 5-fold cross-validation.
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
        d = U.shape[1]
        while self.dm > 1 and N < 4 * poly_feats(np.zeros(d), self.dm).shape[0]:
            self.dm -= 1                                    # small designs
        while self.dv > 0 and N < 4 * poly_feats(np.zeros(d), self.dv).shape[0]:
            self.dv -= 1
        Sb = S.mean(1)
        self.beta, self.XtX_inv = self._fit_mean(U, Sb)
        Rm = Sb - poly_feats(U, self.dm) @ self.beta
        self.Sig_mean = np.atleast_2d(np.cov(Rm.T, ddof=self.beta.shape[0]) if N > self.beta.shape[0] + 2
                                      else np.cov(Rm.T))
        D = S - Sb[:, None]
        var_j = (D ** 2).sum(1) / (K - 1)                                    # (N, q) unbiased
        Xv = poly_feats(U, self.dv)
        self.gamma = np.linalg.lstsq(Xv, var_j, rcond=None)[0]
        self.var_floor = 0.1 * var_j.mean(0)
        Zw = D / np.sqrt(np.maximum(self.var(U), 1e-12))[:, None]
        Cw = np.einsum("nki,nkj->ij", Zw, Zw) / (N * (K - 1))
        dd = np.sqrt(np.maximum(np.diag(Cw), 1e-12))
        self.corr = Cw / np.outer(dd, dd)
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
        w, Qm = np.linalg.eigh((Bm + Bm.T) / 2)
        self.Bm = (Qm * np.maximum(w, 0)) @ Qm.T
        jit = 1e-9 * np.eye(q)
        tot = Sig_j / K + V[:, None, None] * self.Sig_mean[None] + self.Bm[None] + jit
        chi = np.einsum("ni,nij,nj->n", R, np.linalg.inv(tot), R)
        chi0 = np.einsum("ni,nij,nj->n", R, np.linalg.inv(Sig_j / K + V[:, None, None] * self.Sig_mean[None] + jit), R)
        self.diag = {"N_theta": int(N), "K": int(K), "q": int(q), "deg_mean": self.dm, "deg_var": self.dv,
                     "cv_chi2_mean_with_misfit": float(chi.mean()),
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
        S = self.cov(u) / n + self.emu_var(u)[:, None, None] * self.Sig_mean[None] + self.Bm[None] \
            + 1e-9 * np.eye(mu.shape[1])
        r = np.asarray(sbar, float)[None] - mu
        L = np.linalg.cholesky(S)
        z = np.linalg.solve(L, r[..., None])[..., 0]
        return -0.5 * (z ** 2).sum(-1) - np.log(np.diagonal(L, axis1=-2, axis2=-1)).sum(-1) \
            - 0.5 * len(sbar) * math.log(2 * math.pi)


class ViabilityPrior:
    """p_v(u) = P(viable | theta): logistic regression on quadratic monomials of u (L2 penalty), Newton's method."""

    def fit(self, U, y, lam=1e-2, iters=50):
        X = poly_feats(U, 2)
        y = np.asarray(y, float)
        w = np.zeros(X.shape[1])
        P = lam * np.eye(X.shape[1])
        P[0, 0] = 0
        for _ in range(iters):
            p = 1 / (1 + np.exp(-np.clip(X @ w, -30, 30)))
            g = X.T @ (p - y) + P @ w
            Hm = (X * (p * (1 - p))[:, None]).T @ X + P + 1e-9 * np.eye(len(w))
            step = np.linalg.solve(Hm, g)
            step = step * min(1.0, 5.0 / max(np.abs(step).max(), 1e-12))        # damped (all-viable designs)
            w -= step
            if np.abs(step).max() < 1e-8:
                break
        self.w = w
        p = 1 / (1 + np.exp(-np.clip(X @ w, -30, 30)))
        self.diag = {"n": int(len(y)), "frac_viable": float(y.mean()),
                     "mean_loglik": float(np.mean(y * np.log(p + 1e-12) + (1 - y) * np.log(1 - p + 1e-12)))}
        return self

    def logp(self, u):
        z = poly_feats(u, 2) @ self.w
        return -np.logaddexp(0.0, -z)


def _ess(logw):
    w = np.exp(logw - logw.max())
    return float(w.sum() ** 2 / (w ** 2).sum()), w / w.sum()


def posterior(em, pv, sbar, n, rng, d, M=100_000, stages=5, target=3000, n_out=4000):
    """Self-normalised importance sampling of p(u | s_bar) on the box [-1, 1]^d with prior p_v(u)
    (sbi_lib.posterior): stage 0 from the uniform box, then multivariate-t (df 5) proposals fitted to the
    previous stage's weighted draws, truncated to the box."""
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
        u = np.concatenate(out)[:M]
        if len(u) < M:                                    # proposal almost outside the box: pad with box draws
            u = np.concatenate([u, rng.uniform(-1, 1, (M - len(u), d))])
            Li = np.linalg.inv(L)
            mz = ((u - mu) @ Li.T)
            logq = np.logaddexp(-0.5 * (df + d) * np.log1p((mz ** 2).sum(1) / df), -20.0)
        else:
            Li = np.linalg.inv(L)
            mz = ((u - mu) @ Li.T)
            logq = -0.5 * (df + d) * np.log1p((mz ** 2).sum(1) / df)
    cw = np.cumsum(w)
    pos = (rng.random() + np.arange(n_out)) / n_out
    idx = np.minimum(np.searchsorted(cw, pos), len(w) - 1)
    mean = w @ u
    sd = np.sqrt(np.maximum(w @ (u - mean) ** 2, 0))
    return {"u": u[idx], "ess": ess, "ess_stages": hist, "mean_u": mean, "sd_u": sd, "u_all": u, "w_all": w}


def posterior_checks(post, em, pv, sbar, n, u_true):
    """Marginal PIT of the truth, central-interval coverage flags and the HPD level of the truth."""
    u, w = post["u_all"], post["w_all"]
    pit = [(w * (u[:, i] <= u_true[i])).sum() for i in range(len(u_true))]
    lp = lambda x: pv.logp(x) + em.loglik(x, sbar, n)       # noqa: E731
    lt = lp(np.asarray(u_true)[None])[0]
    hpd = float((w * (lp(u) > lt)).sum())
    return {"pit": [float(p) for p in pit], "hpd_level": hpd,
            "in50": [bool(0.25 <= p <= 0.75) for p in pit], "in90": [bool(0.05 <= p <= 0.95) for p in pit]}


def prior_draws(pv, d, n, rng, M=200_000):
    """Draws from the viability-conditioned prior on the box, and its mean and sd (box units)."""
    ub = rng.uniform(-1, 1, (M, d))
    wb = np.exp(pv.logp(ub))
    wb /= wb.sum()
    pm = wb @ ub
    psd = np.sqrt(wb @ (ub - pm) ** 2)
    return ub[rng.choice(M, size=n, p=wb)], pm, psd
