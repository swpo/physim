"""evaluator.acceptance -- the roadmap's two acceptance quantities from per-item fair energy scores.

L(policy) = mean over items of the fair energy score summed over the declared (level, time) cells (the pooled
energy score; one predictor family for D, P0, S and C). Lower is better.
    science share   sigma = (L(null) - L(C)) / (L(K) - L(C)),  null = the better (lower L) of D at budget and P0
    scripted share  rho   = (L(P0) - L(S)) / (L(P0) - L(C))
Bars (ROADMAP section 1): sigma >= 0.15 and rho <= 0.7. C is a lower bound, so shares are not clipped.
Uncertainty: bootstrap over items and, when hidden worlds are given, a cluster bootstrap over worlds
(worlds resampled with replacement, all their items kept).
"""
from __future__ import annotations

import numpy as np


def pooled(S: dict, valid=None) -> dict:
    """name -> per-item pooled score (n,) from name -> (n, n_cells)."""
    out = {}
    for k, v in S.items():
        v = np.asarray(v, float)
        out[k] = (v if valid is None else v[:, np.asarray(valid, bool)]).sum(1)
    return out


def _shares(m: dict) -> dict:
    null = min(m["D"], m["P0"]) if "D" in m else m["P0"]
    out = {"sigma": (null - m["C"]) / (m["K"] - m["C"]), "null_is": "D" if ("D" in m and m["D"] <= m["P0"]) else "P0"}
    if "S" in m:
        den = m["P0"] - m["C"]
        out["rho"] = (m["P0"] - m["S"]) / den if den != 0 else float("nan")
    return out


def shares(S: dict, valid=None, worlds=None, n_boot: int = 2000, seed: int = 0) -> dict:
    """S: name -> (n_items, n_cells) with keys K, P0, C and optionally D, S, O. worlds: (n_items,) labels."""
    L = pooled(S, valid)
    n = len(L["K"])
    pt = _shares({k: float(v.mean()) for k, v in L.items()})
    rng = np.random.default_rng(seed)

    def boot(index_sets):
        sig, rho = [], []
        for idx in index_sets:
            b = _shares({k: float(v[idx].mean()) for k, v in L.items()})
            sig.append(b["sigma"])
            rho.append(b.get("rho", np.nan))
        return np.array(sig), np.array(rho)

    def summ(a):
        a = a[np.isfinite(a)]
        return {"se": float(a.std(ddof=1)), "p05": float(np.quantile(a, 0.05)), "p95": float(np.quantile(a, 0.95))} if a.size > 2 else None

    sig_i, rho_i = boot(rng.integers(0, n, size=(n_boot, n)))
    out = {"L": {k: float(v.mean()) for k, v in L.items()}, "n_items": int(n), "sigma": float(pt["sigma"]),
           "null_is": pt["null_is"], "rho": None if "rho" not in pt else float(pt["rho"]),
           "sigma_items": summ(sig_i), "rho_items": summ(rho_i) if "rho" in pt else None,
           "bars": {"sigma_min": 0.15, "rho_max": 0.7},
           "pass_sigma": bool(pt["sigma"] >= 0.15), "pass_rho": None if "rho" not in pt else bool(pt["rho"] <= 0.7)}
    if worlds is not None:
        worlds = np.asarray(worlds)
        ids = sorted(set(worlds.tolist()))
        groups = [np.flatnonzero(worlds == w) for w in ids]
        if len(ids) >= 2:
            sets = [np.concatenate([groups[j] for j in rng.integers(0, len(ids), size=len(ids))]) for _ in range(n_boot)]
            sig_w, rho_w = boot(sets)
            out.update({"n_worlds": len(ids), "sigma_worlds": summ(sig_w), "rho_worlds": summ(rho_w) if "rho" in pt else None})
            per = [_shares({k: float(v[g].mean()) for k, v in L.items()}) for g in groups]
            out["per_world"] = {"sigma": [float(p["sigma"]) for p in per], "rho": [float(p.get("rho", np.nan)) for p in per]}
    return out


def skill(S: dict, valid=None) -> dict:
    """Pooled skill of every policy on the K-to-O and K-to-C scales: (L(K) - L) / (L(K) - L(ref))."""
    L = {k: float(v.mean()) for k, v in pooled(S, valid).items()}
    out = {}
    for k in L:
        out[k] = {"L": L[k], "vs_C": (L["K"] - L[k]) / (L["K"] - L["C"]) if "C" in L else None,
                  "vs_O": (L["K"] - L[k]) / (L["K"] - L["O"]) if "O" in L else None}
    return out
