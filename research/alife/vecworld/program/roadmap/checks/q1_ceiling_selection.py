"""Q1 check: what does selecting WORLDS by closure ceiling alone pick?

Closed form, numpy only, a few CPU-seconds. Family: random linear-Gaussian worlds
    x' = A x + w, w ~ N(0, Q);  y = C x;  o = y + r eta
(n0 = 16 micro numbers, n1 = 4 macro numbers), spectral radius rho ~ U(0.2, 0.99), as vw.lingauss.random_lg
but with rho drawn. For each world, with the whole observed past (steady-state Kalman filter):
    V0  = stationary variance of o                (long-run average predictor)
    Ve  = error of the best predictor from the observed past at horizon tau
    Vu  = error of the oracle (given the micro state) at horizon tau
    ceiling c(tau) = (V0 - Ve) / (V0 - Vu)        per-coordinate standardised, averaged
    share s(tau)   = 1 - Ve / V0                  how much of o is predictable at all from its past
    I1             = 0.5 (logdet S0 - logdet Se(1))   predictive information, nats per tick
Question: among worlds ranked by c(4), what content do the top ones have?
"""
import json
import sys

import numpy as np

N, n0, n1, r, TAU = 4000, 16, 4, 0.05, 4
rng = np.random.default_rng(20261109)


def dlyap(A, Q, it=4000):
    S, M = Q.copy(), Q.copy()
    for _ in range(it):
        M = A @ M @ A.T
        S = S + M
        if np.abs(M).max() < 1e-14:
            break
    return S


def world_stats(A, Q, C):
    R = r ** 2 * np.eye(n1)
    Sig = dlyap(A, Q)
    S0 = C @ Sig @ C.T + R
    P = Sig.copy()                                   # steady-state predicted covariance (Riccati)
    for _ in range(2000):
        G = P @ C.T @ np.linalg.inv(C @ P @ C.T + R)
        F = P - G @ C @ P
        Pn = A @ F @ A.T + Q
        if np.abs(Pn - P).max() < 1e-13:
            P = Pn
            break
        P = Pn
    G = P @ C.T @ np.linalg.inv(C @ P @ C.T + R)
    F = P - G @ C @ P                                # filtered covariance given o(<= t)
    d0 = np.diag(S0)
    out = {}
    M, At = np.zeros((n0, n0)), np.eye(n0)
    for tau in range(1, TAU + 1):
        M = M + At @ Q @ At.T
        At = A @ At
        Se = C @ (At @ F @ At.T + M) @ C.T + R
        Su = C @ M @ C.T + R
        if tau == 1:
            out["I1"] = 0.5 * (np.linalg.slogdet(S0)[1] - np.linalg.slogdet(Se)[1])
        if tau == TAU:
            Ve, Vu = np.mean(np.diag(Se) / d0), np.mean(np.diag(Su) / d0)
            out["c"] = (1 - Ve) / (1 - Vu)
            out["share_past"] = 1 - Ve               # predictable from the observed past
            out["share_oracle"] = 1 - Vu             # predictable from the micro state
    return out


rows = []
for i in range(N):
    rho = rng.uniform(0.2, 0.99)
    A = rng.standard_normal((n0, n0)) / np.sqrt(n0)
    A *= rho / np.max(np.abs(np.linalg.eigvals(A)))
    Gm = rng.standard_normal((n0, n0)) / np.sqrt(n0)
    Q = 0.09 * (Gm @ Gm.T + 0.1 * np.eye(n0))
    C = rng.standard_normal((n1, n0)) / np.sqrt(n0)
    s = world_stats(A, Q, C)
    s["rho"] = rho
    rows.append(s)

keys = ["c", "share_past", "share_oracle", "I1", "rho"]
X = {k: np.array([row[k] for row in rows]) for k in keys}


def spearman(a, b):
    ra, rb = np.argsort(np.argsort(a)), np.argsort(np.argsort(b))
    return float(np.corrcoef(ra, rb)[0, 1])


def med(mask):
    return {k: round(float(np.median(X[k][mask])), 4) for k in keys}


order = np.argsort(-X["c"])
top = np.zeros(N, bool)
top[order[: N // 20]] = True
# a two-part rule: ceiling in a band AND at least 10% of the variance predictable from the past at tau
band = (X["c"] >= 0.5) & (X["share_past"] >= 0.10)
thin = X["share_oracle"] < 0.05                      # nothing to predict at tau even for the oracle
res = {
    "family": {"N": N, "n0": n0, "n1": n1, "r": r, "tau": TAU, "rho": "U(0.2, 0.99)", "seed": 20261109},
    "median_all": med(np.ones(N, bool)),
    "median_top5pct_by_ceiling": med(top),
    "median_two_part_rule": med(band),
    "frac_two_part_rule": round(float(band.mean()), 4),
    "frac_thin_all": round(float(thin.mean()), 4),
    "frac_thin_in_top5pct_by_ceiling": round(float(thin[top].mean()), 4),
    "frac_top5pct_with_share_past_below_0.10": round(float((X["share_past"][top] < 0.10).mean()), 4),
    "spearman_ceiling_vs": {k: round(spearman(X["c"], X[k]), 3) for k in keys if k != "c"},
    "ceiling_quantiles": [round(float(q), 4) for q in np.quantile(X["c"], [0.05, 0.25, 0.5, 0.75, 0.95])],
    "note": "closed form (steady-state Kalman filter); the ceiling is exact here, not a lower bound",
}
json.dump(res, open(sys.argv[1], "w"), indent=1)
print(json.dumps(res, indent=1))
