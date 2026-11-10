"""inference -- the scripted policy's parameter inference: a shrunk synthetic likelihood (after round4/sbi).

features     phase-insensitive level-1 statistics of an episode (per world)
Projection   linear-regression summaries (Fearnhead & Prangle 2012): s = W^T z(features), fitted by ridge
             regression of the unit-box parameters u on standardised features over HALF of the design (penalty by
             cross-validation); the likelihood below is fitted on the OTHER half, so its covariance is honest
             even when the design is small (an in-sample projection made a 12-point design confidently wrong)
LinSL        Gaussian synthetic likelihood (Wood 2010) with a polynomial emulator of the summary mean
             (quadratic when the design allows, else linear), a per-episode covariance pooled within design
             points, and a misfit covariance from the emulator's residuals:
             mean of n episodes ~ N(mu(u), Sigma / n + Sigma_misfit)
posterior    self-normalised importance sampling on the prior box, one adaptive refinement
"""
import itertools

import numpy as np


# ----------------------------------------------------------------------------- features
def _lg(x):
    return np.log(np.maximum(x, 1e-6))


def features_ring(obs):
    """obs (B, T + 1, 6) -> (B, 15): log variance and lagged, shifted correlations of the block values."""
    y = np.asarray(obs, float)
    y = y - y.mean((1, 2), keepdims=True)
    v = (y ** 2).mean((1, 2))
    out = [np.log(v)]
    for lag in (0, 1, 2, 4, 8):
        for s in (-1, 0, 1):
            if lag == 0 and s == 0:
                continue
            a, b = y[:, lag:], np.roll(y, s, -1)[:, :y.shape[1] - lag]
            out.append((a * b).mean((1, 2)) / v)
    return np.stack(out, 1)


def features_gliders(obs, sc1):
    """round4/sbi/sbi_lib.episode_features: obs (B, T + 1, 336) -> (B, 22)."""
    G, NC, K, NF = 8, 192, 12, 12
    y = np.asarray(obs, float)
    B, T1, _ = y.shape
    C = y[..., :NC].reshape(B, T1, 3, G, G)
    O = y[..., NC:NC + K * NF].reshape(B, T1, K, NF)
    pres = O[..., 0] > 0.5
    npres = np.maximum(pres.sum((1, 2)), 1)
    n = pres.sum(-1).astype(float)

    def pm(v):
        return np.where(pres, v, 0.0).sum((1, 2)) / npres
    mass, frac, rg, q1, q2, vx, vy = (O[..., i] for i in (1, 2, 7, 8, 9, 10, 11))
    spd = np.hypot(vx, vy)
    mb, sp = pm(mass), pm(spd)
    sc = np.asarray(sc1, float).reshape(3, G, G)

    def dC(k):
        return np.sqrt((((C[:, k:] - C[:, :-k]) / sc) ** 2).mean((2, 3, 4))).mean(1)
    c0 = C[:, :, 0].reshape(B, T1, -1)
    c1 = C[:, :, 1].reshape(B, T1, -1)
    c0c, c1c = c0 - c0.mean(-1, keepdims=True), c1 - c1.mean(-1, keepdims=True)
    corr = (c0c * c1c).sum(-1) / np.maximum(np.sqrt((c0c ** 2).sum(-1) * (c1c ** 2).sum(-1)), 1e-12)
    f = [n.mean(1), n.std(1), np.abs(np.diff(n, axis=1)).mean(1), _lg(mb),
         np.sqrt(np.maximum(pm(mass ** 2) - mb ** 2, 0)) / np.maximum(mb, 1e-6), pm(frac), _lg(pm(rg)),
         pm(np.hypot(q1, q2)), sp, np.sqrt(np.maximum(pm(spd ** 2) - sp ** 2, 0)),
         _lg(np.where(pres, mass, 0.0).sum(-1).mean(1)), C[:, 0, 0].mean((1, 2)), C[:, 0, 1].mean((1, 2)),
         _lg(C[:, :, 2].mean((2, 3))).mean(1), _lg(c0.std(-1)).mean(1), _lg(c1.std(-1)).mean(1), corr.mean(1),
         _lg(C[:, :, 2].std((2, 3))).mean(1), _lg(dC(1)), _lg(dC(min(4, T1 - 1))), _lg(C[:, :, 2].max((2, 3))).mean(1),
         pm(_lg(mass) - 2 * _lg(rg))]
    return np.stack(f, 1)


def features(world, obs, scales):
    return features_ring(obs) if world == "ring" else features_gliders(obs, scales[1])


# ----------------------------------------------------------------------------- summaries and likelihood
class Projection:
    """s = W^T z(features): ridge regression of u on standardised features; the penalty is chosen by 5-fold
    cross-validation over the design rows (a small design gets a strong penalty instead of an interpolating fit)."""
    LAMS = (1e-3, 1e-2, 1e-1, 1.0, 10.0)

    def fit(self, F, U, groups=None):
        F, U = np.asarray(F, float), np.asarray(U, float)
        self.mu, self.sd = F.mean(0), np.maximum(F.std(0), 1e-9)
        Z = np.concatenate([(F - self.mu) / self.sd, np.ones((len(F), 1))], 1)
        pen = np.diag(np.r_[np.ones(Z.shape[1] - 1), 0.0])
        g = np.arange(len(F)) if groups is None else np.asarray(groups)
        fold = g % 5
        best = None
        for lam in self.LAMS:
            err = 0.0
            for f in range(5):
                tr, te = fold != f, fold == f
                if not te.any() or tr.sum() < 2:
                    continue
                Wk = np.linalg.solve(Z[tr].T @ Z[tr] + lam * tr.sum() * pen + 1e-9 * np.eye(Z.shape[1]), Z[tr].T @ U[tr])
                err += float(((U[te] - Z[te] @ Wk) ** 2).sum())
            if best is None or err < best[0]:
                best = (err, lam)
        self.lam = best[1]
        self.cv_r2 = 1.0 - best[0] / float(((U - U.mean(0)) ** 2).sum())
        self.W = np.linalg.solve(Z.T @ Z + self.lam * len(F) * pen + 1e-9 * np.eye(Z.shape[1]), Z.T @ U)
        return self

    def __call__(self, F):
        F = np.asarray(F, float)
        return np.concatenate([(F - self.mu) / self.sd, np.ones(F.shape[:-1] + (1,))], -1) @ self.W


def poly(u, deg):
    u = np.asarray(u, float)
    cols = [np.ones(u.shape[:-1])]
    for k in range(1, deg + 1):
        for c in itertools.combinations_with_replacement(range(u.shape[-1]), k):
            cols.append(np.prod([u[..., i] for i in c], 0))
    return np.stack(cols, -1)


def _psd(S):
    w, Q = np.linalg.eigh((S + S.T) / 2)
    return (Q * np.maximum(w, 0)) @ Q.T


class LinSL:
    def fit(self, U, S):
        """U (N, d) unit-box design, S (N, K, q) per-episode summaries."""
        U, S = np.asarray(U, float), np.asarray(S, float)
        N, K, q = S.shape
        d = U.shape[1]
        self.deg = 2 if N >= 4 * poly(np.zeros(d), 2).shape[0] else 1
        Sb = S.mean(1)
        X = poly(U, self.deg)
        self.beta = np.linalg.lstsq(X, Sb, rcond=None)[0]
        Rm = Sb - X @ self.beta
        Cm = Rm.T @ Rm / max(N - X.shape[1], 1)
        if K > 1:
            D = (S - Sb[:, None]).reshape(-1, q)
            self.Sw = D.T @ D / (N * (K - 1))
            self.Sm = _psd(Cm - self.Sw / K)
        else:                                               # one episode per design point: noise and misfit pooled
            self.Sw, self.Sm = Cm, np.zeros((q, q))
        self.Sw = self.Sw + 1e-9 * np.trace(self.Sw) / q * np.eye(q)
        return self

    def loglik(self, u, sbar, n):
        r = np.asarray(sbar, float)[None] - poly(u, self.deg) @ self.beta
        L = np.linalg.cholesky(self.Sw / n + self.Sm)
        z = np.linalg.solve(L, r.T)
        return -0.5 * (z ** 2).sum(0)


def posterior(sl, sbar, n, d, rng, M=100_000, n_out=1000):
    """Draws from p(u | s_bar) on [-1, 1]^d under the flat prior; returns (draws (n_out, d), diagnostics)."""
    u = rng.uniform(-1, 1, (M, d))
    logq = np.zeros(M)
    ess_hist = []
    for stage in range(2):
        lw = sl.loglik(u, sbar, n) - logq
        w = np.exp(lw - lw.max())
        w /= w.sum()
        ess = 1.0 / (w ** 2).sum()
        ess_hist.append(float(ess))
        if ess >= 500 or stage == 1:
            break
        top = np.argsort(-lw)[:max(50, int(ess))]
        mu = u[top].mean(0) if ess < 20 else w @ u
        cov = (np.cov(u[top].T) if ess < 20 else (u - mu).T @ ((u - mu) * w[:, None])) * 4.0 + 1e-4 * np.eye(d)
        Lc = np.linalg.cholesky(cov)
        out = []
        while sum(len(o) for o in out) < M:
            x = mu + rng.standard_normal((M, d)) @ Lc.T
            out.append(x[(np.abs(x) <= 1).all(1)])
            if len(out) > 200:
                break
        u = np.concatenate(out)[:M]
        z = np.linalg.solve(Lc, (u - mu).T)
        logq = -0.5 * (z ** 2).sum(0)
    mean = w @ u
    sd = np.sqrt(np.maximum(w @ (u - mean) ** 2, 0))
    idx = rng.choice(len(u), size=n_out, p=w)
    return u[idx], {"ess": ess_hist, "mean_u": mean.tolist(), "sd_u": sd.tolist(), "sd_over_prior_sd": (sd * np.sqrt(3)).tolist()}
