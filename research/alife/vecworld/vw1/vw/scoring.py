"""vw.scoring -- proper scores for ensemble forecasts and oracle-normalised skill (EXAM.md section 4).

Conventions (as PhySim v1): coordinates are divided by public scales, and the energy-score norm is
RMS (|v| / sqrt(d)). Samples X have shape (..., m, d), truths Y (..., R, d); leading axes (items,
cells) are looped over, so memory stays O(m^2 d) per item.

energy_fair     ES_fair = (1/(mR)) sum_{i,r} |x_i - y_r| - 1/(2m(m-1)) sum_{i!=j} |x_i - x_j|
                the U-statistic (Ferro 2014 for the CRPS): unbiased for ES(F, y) for any m >= 2.
energy_v1       v1's estimator (ordered pairs including i = j): biased up by E|X - X'| / (2m).
energy_loo      the oracle reference from R replicate truths: for each r, the other R - 1 truths
                are the ensemble (m = R - 1); unbiased with fair=True, no extra simulation.
variogram       VS_p = sum_{i<j} w_ij (|y_i - y_j|^p - E|X_i - X_j|^p)^2 (Scheuerer & Hamill 2015);
                fair=True subtracts the plug-in variance s_ij^2/m, which makes it unbiased.
crps_fair       per-coordinate fair CRPS (diagnostic maps).
oes / skill     OES_c = (S_clim - S) / (S_clim - S_oracle) per cell, a ratio of item means; cells
                whose denominator is < z SE above zero are dropped (decided on the references only);
                the aggregate is the equal-weight mean over kept cells (EXAM 4.4); also reported:
                'floor0', the mean of max(OES_c, 0) (climatology floor per cell), and 'pooled',
                sum_c (S_clim - S) / sum_c (S_clim - S_oracle); paired bootstrap over items.
"""
from __future__ import annotations

import math
from typing import Mapping, Optional, Sequence

import numpy as np


def _pd(X: np.ndarray, Y: np.ndarray) -> np.ndarray:
    """RMS distances between rows: (m, d), (n, d) -> (m, n)."""
    d = X.shape[-1]
    D = np.sqrt(((X[:, None, :] - Y[None, :, :]) ** 2).sum(-1))
    return D / math.sqrt(d)


def _scaled(A, scale):
    A = np.asarray(A, float)
    return A if scale is None else A / np.asarray(scale, float)


def _loop(fn, X, Y, *args):
    """Apply fn(x (m, d), y (R, d)) over the leading axes of X and Y (which must agree)."""
    lead = X.shape[:-2]
    if Y.shape[:-2] != lead:
        raise ValueError(f"scoring: leading axes differ: {X.shape} vs {Y.shape}")
    Xr = X.reshape((-1,) + X.shape[-2:])
    Yr = Y.reshape((-1,) + Y.shape[-2:])
    out = [fn(x, y, *args) for x, y in zip(Xr, Yr)]
    out = np.asarray(out)
    return out.reshape(lead + out.shape[1:])


# ----------------------------------------------------------------------------- energy score
def _es_one(x, y, fair):
    m = x.shape[0]
    t1 = _pd(x, y).mean()
    Dxx = _pd(x, x)
    t2 = Dxx.sum() / (2.0 * m * (m - 1)) if fair else Dxx.sum() / (2.0 * m * m)
    return t1 - t2


def energy_fair(X, Y, scale=None) -> np.ndarray:
    """Mean over truths of the fair energy score of the ensemble X (..., m, d) at Y (..., R, d)."""
    X, Y = _scaled(X, scale), _scaled(Y, scale)
    if X.shape[-2] < 2:
        raise ValueError("energy_fair: need m >= 2 samples")
    return _loop(_es_one, X, Y, True)


def energy_v1(X, Y, scale=None) -> np.ndarray:
    """PhySim v1's estimator (self-pairs included)."""
    return _loop(_es_one, _scaled(X, scale), _scaled(Y, scale), False)


def _es_loo_one(y, _unused, fair):
    R = y.shape[0]
    D = _pd(y, y)
    row = D.sum(1)                       # sum_s D_rs (D_rr = 0)
    P = D.sum() / 2.0                    # sum_{s<t} D_st
    m = R - 1
    t1 = row / m
    rest = P - row                       # sum_{s<t; s,t != r} D_st
    t2 = rest / (m * (m - 1)) if fair else rest / (m * m)
    return float((t1 - t2).mean())


def energy_loo(Y, scale=None, fair: bool = True) -> np.ndarray:
    """Oracle reference: leave-one-out energy score of the R replicate truths (..., R, d)."""
    Y = _scaled(Y, scale)
    if Y.shape[-2] < (3 if fair else 2):
        raise ValueError("energy_loo: need R >= 3 truths (fair)")
    return _loop(_es_loo_one, Y, Y, fair)


# ----------------------------------------------------------------------------- variogram score
def _vs_one(x, y, p, w, fair):
    d = x.shape[1]
    iu = np.triu_indices(d, 1)
    W = np.ones((d, d)) if w is None else np.asarray(w, float)
    wi = W[iu]
    gx = np.abs(x[:, iu[0]] - x[:, iu[1]]) ** p          # (m, npairs)
    g = gx.mean(0)
    a = np.abs(y[:, iu[0]] - y[:, iu[1]]) ** p           # (R, npairs)
    sq = (a - g[None]) ** 2
    if fair:
        sq = sq - gx.var(0, ddof=1)[None] / x.shape[0]
    return float((sq * wi[None]).sum(1).mean())


def variogram(X, Y, p: float = 0.5, w=None, scale=None, fair: bool = True) -> np.ndarray:
    """Mean over truths of the variogram score of order p (fair: bias-corrected)."""
    return _loop(_vs_one, _scaled(X, scale), _scaled(Y, scale), p, w, fair)


def _vs_loo_one(y, _unused, p, w, fair):
    R = y.shape[0]
    out = [_vs_one(np.delete(y, r, 0), y[r:r + 1], p, w, fair) for r in range(R)]
    return float(np.mean(out))


def variogram_loo(Y, p: float = 0.5, w=None, scale=None, fair: bool = True) -> np.ndarray:
    Y = _scaled(Y, scale)
    return _loop(_vs_loo_one, Y, Y, p, w, fair)


def ring_weights(d: int) -> np.ndarray:
    """w_ij = 1 / (1 + ring distance(i, j)) for d sites on a ring."""
    i = np.arange(d)
    dist = np.abs(i[:, None] - i[None, :])
    dist = np.minimum(dist, d - dist)
    return 1.0 / (1.0 + dist)


# ----------------------------------------------------------------------------- CRPS
def crps_fair(X, Y, scale=None) -> np.ndarray:
    """Per-coordinate fair CRPS: X (..., m, d), Y (..., R, d) -> (..., d)."""
    X, Y = _scaled(X, scale), _scaled(Y, scale)

    def one(x, y):
        m = x.shape[0]
        t1 = np.abs(x[:, None, :] - y[None]).mean((0, 1))
        t2 = np.abs(x[:, None, :] - x[None]).sum((0, 1)) / (2.0 * m * (m - 1))
        return t1 - t2
    return _loop(one, X, Y)


# ----------------------------------------------------------------------------- skill
def cells_ok(clim: np.ndarray, oracle: np.ndarray, z: float = 3.0) -> np.ndarray:
    """Cells whose denominator mean(S_clim - S_oracle) is more than z standard errors above zero.
    clim, oracle: (n_items, n_cells)."""
    d = np.asarray(clim, float) - np.asarray(oracle, float)
    n = d.shape[0]
    se = d.std(0, ddof=1) / math.sqrt(n)
    return d.mean(0) > z * se


def oes(S, clim, oracle) -> np.ndarray:
    """Per-cell oracle-normalised energy skill (ratio of item means)."""
    S, clim, oracle = (np.asarray(a, float).mean(0) for a in (S, clim, oracle))
    with np.errstate(divide="ignore", invalid="ignore"):
        return (clim - S) / (clim - oracle)


def skill_report(scores: Mapping[str, np.ndarray], clim: str = "climatology", oracle: str = "oracle",
                 cells: Optional[Sequence] = None, valid: Optional[np.ndarray] = None, z: float = 3.0,
                 n_boot: int = 2000, seed: int = 0, groups: Optional[np.ndarray] = None,
                 floor: Optional[float] = None) -> dict:
    """OES per cell and aggregate for every entry of `scores` (name -> (n_items, n_cells)), with a
    paired bootstrap over items (all entries share the resampled items).

    valid   cells in the aggregate (default: cells_ok on the references, decided before any agent)
    groups  optional item labels (e.g. program class) for a per-group aggregate
    floor   if given, also report max(aggregate, floor) (a reward map; the raw OES stays primary)
    Returns cells, valid, oes[name] (per cell), aggregate[name], se[name], boot (aggregate draws)."""
    names = list(scores)
    S = {k: np.asarray(v, float) for k, v in scores.items()}
    n, c = S[clim].shape
    if valid is None:
        valid = cells_ok(S[clim], S[oracle], z)
    valid = np.asarray(valid, bool)
    if not valid.any():
        raise ValueError("skill_report: no cell has a significant denominator")
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, n, size=(n_boot, n))

    def agg(means, mode="mean"):     # means: name -> (..., c)
        den = means[clim] - means[oracle]
        out = {}
        for k in names:
            num = means[clim] - means[k]
            if mode == "pooled":
                out[k] = num[..., valid].sum(-1) / den[..., valid].sum(-1)
                continue
            with np.errstate(divide="ignore", invalid="ignore"):
                o = num / den
            if mode == "floor0":
                o = np.maximum(o, 0.0)
            out[k] = o[..., valid].mean(-1)
        return out
    point = {k: S[k].mean(0) for k in names}
    boot_means = {k: S[k][idx].mean(1) for k in names}       # (n_boot, c)
    a_pt, a_bt = agg(point), agg(boot_means)
    rep = {"cells": [list(cc) if isinstance(cc, tuple) else cc for cc in (cells or range(c))],
           "valid": valid.tolist(), "n_items": int(n),
           "oes": {k: oes(S[k], S[clim], S[oracle]).tolist() for k in names},
           "aggregate": {k: float(a_pt[k]) for k in names},
           "se": {k: float(a_bt[k].std(ddof=1)) for k in names},
           "mean_score": {k: S[k].mean(0).tolist() for k in names}}
    rep["_boot"] = a_bt
    # alternatives: per-cell floor at climatology (max(OES_c, 0)) and the pooled ratio of sums
    for mode in ("floor0", "pooled"):
        p_, b_ = agg(point, mode), agg(boot_means, mode)
        rep[f"aggregate_{mode}"] = {k: float(p_[k]) for k in names}
        rep[f"se_{mode}"] = {k: float(b_[k].std(ddof=1)) for k in names}
        rep[f"_boot_{mode}"] = b_
    if floor is not None:
        rep["floored"] = {k: max(float(a_pt[k]), floor) for k in names}
    if groups is not None:
        groups = np.asarray(groups)
        rep["by_group"] = {}
        for g in sorted(set(groups.tolist())):
            sel = groups == g
            sub = {k: S[k][sel] for k in names}
            pt = agg({k: sub[k].mean(0) for k in names})
            rep["by_group"][str(g)] = {k: float(pt[k]) for k in names}
    return rep


def paired_gap(report: dict, a: str, b: str, mode: str = "") -> dict:
    """Aggregate OES gap a - b with its paired bootstrap SE (from skill_report's draws).
    mode '' (equal-weight mean of per-cell OES), 'floor0' or 'pooled'."""
    sfx = f"_{mode}" if mode else ""
    g = report["aggregate" + sfx][a] - report["aggregate" + sfx][b]
    se = float((report["_boot" + sfx][a] - report["_boot" + sfx][b]).std(ddof=1))
    return {"gap": g, "se": se, "z": g / se if se > 0 else math.inf}


def public_report(report: dict) -> dict:
    """skill_report without the bootstrap draws (JSON-ready)."""
    return {k: v for k, v in report.items() if not k.startswith("_")}
