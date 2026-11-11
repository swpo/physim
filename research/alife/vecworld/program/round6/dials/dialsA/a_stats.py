"""a_stats -- study A: the declared criteria from per-item scores (numpy only; DECLARED.md R1-R15).

Scores: name -> (n_eta, n_truth, n_seed, 2, n_items, n_h) fair energy scores (half 0 = `sel`, picks only;
half 1 = `score`); classes (n_eta, n_truth, 2, n_items) in 'a' none, 'b' blind, 'c' aimed, 'd' regional.
L of a policy = mean over items of the score summed over the horizons (acceptance.py); lower is better.
Every statistic is a per-truth contrast averaged over seeds; SE^2 = SD_truths^2 / n + SD_seeds^2 / n_seeds
(SD_seeds over the seeds' across-truth means); one-sided 90% bounds with t(0.90, n_truths - 1).
"""
from __future__ import annotations

import numpy as np

_T90 = {1: 3.078, 2: 1.886, 3: 1.638, 4: 1.533, 5: 1.476, 6: 1.440, 7: 1.415, 8: 1.397, 9: 1.383, 10: 1.372,
        11: 1.363, 12: 1.356, 13: 1.350, 14: 1.345, 15: 1.341, 16: 1.337, 17: 1.333, 18: 1.330, 19: 1.328,
        20: 1.325, 23: 1.319, 31: 1.309}
ALL, TRIG = ("a", "b", "c", "d"), ("c", "d")


def t90(df):
    if df in _T90:
        return _T90[df]
    return _T90[max(k for k in _T90 if k <= df)] if df > 1 else float("inf")


class Scores:
    def __init__(self, d, classes, etas):
        self.d = {k: np.asarray(v, float) for k, v in d.items()}
        self.cl = np.asarray(classes)
        self.etas = [float(e) for e in etas]

    def has(self, *names):
        return all(n in self.d and np.isfinite(self.d[n]).any() for n in names)

    def L(self, name, ei, half=1, cls=ALL, hsel=None):
        """(n_truth, n_seed): mean over the items of the classes of the score summed over horizons."""
        a = self.d[name][ei][:, :, half]                              # (T, S, I, H)
        a = a.sum(-1) if hsel is None else a[..., hsel].sum(-1)
        m = np.isin(self.cl[ei][:, half], cls)                        # (T, I)
        out = np.full(a.shape[:2], np.nan)
        for t in range(a.shape[0]):
            out[t] = a[t][:, m[t]].mean(-1)
        return out

    def pick(self, names, ei, cls=ALL, hsel=None):
        """Per truth and seed the candidate with the lowest L on `sel` (all classes, all horizons); returns
        its L on `score` for the classes asked, and the index picked (n_truth, n_seed)."""
        names = [n for n in names if self.has(n)]
        if not names:
            raise KeyError("no candidate scored")
        sel = np.stack([self.L(n, ei, half=0) for n in names])
        sel = np.where(np.isfinite(sel), sel, np.inf)
        idx = np.argmin(sel, 0)
        sc = np.stack([self.L(n, ei, half=1, cls=cls, hsel=hsel) for n in names])
        return np.take_along_axis(sc, idx[None], 0)[0], idx, names


def stat(c):
    """Per-truth contrast c (n_truth, n_seed) -> mean, SE (truths + seeds), bounds, median, leave-one-out."""
    c = np.asarray(c, float)
    ct = c.mean(1)
    n, ns = c.shape
    se_t = float(ct.std(ddof=1) / np.sqrt(n)) if n > 1 else float("nan")
    sd_s = float(c.mean(0).std(ddof=1)) if ns > 1 else 0.0
    se = float(np.sqrt(se_t ** 2 + sd_s ** 2 / max(ns, 1)))
    loo = [(ct.sum() - ct[i]) / (n - 1) for i in range(n)] if n > 1 else [float("nan")]
    tq = t90(n - 1)
    m = float(ct.mean())
    return {"mean": m, "se": se, "se_truths": se_t, "sd_seeds": sd_s, "median_truths": float(np.median(ct)),
            "loo_min": float(min(loo)), "loo_max": float(max(loo)), "lower90": m - tq * se, "upper90": m + tq * se,
            "t90": tq, "n_truths": int(n), "n_seeds": int(ns), "per_truth": ct.tolist(), "per_seed": c.mean(0).tolist()}


def ratio(a, b):
    """Ratio of means over truths of a and b (n_truth, n_seed), SE from the linearised contrast a - r b."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    ma, mb = a.mean(), b.mean()
    r = float(ma / mb) if mb != 0 else float("nan")
    e = stat(a - r * b)
    se = e["se"] / abs(mb) if mb != 0 else float("nan")
    at, bt = a.mean(1), b.mean(1)
    n = len(at)
    loo = [float((at.sum() - at[i]) / (bt.sum() - bt[i])) for i in range(n)] if n > 1 else [float("nan")]
    with np.errstate(divide="ignore", invalid="ignore"):
        per = at / bt
        per_seed = a.mean(0) / b.mean(0)
    return {"value": r, "se": float(se), "lower90": r - e["t90"] * se, "upper90": r + e["t90"] * se,
            "median_of_per_truth_ratios": float(np.median(per)), "loo_min": float(min(loo)), "loo_max": float(max(loo)),
            "per_truth": per.tolist(), "per_seed": per_seed.tolist(), "numerator": stat(a), "denominator": stat(b),
            "n_truths": int(n)}


def C_of(S, ei, nb, cls=ALL, hsel=None):
    """C of DECLARED R7: the better on `sel` of the true-form net at the truth and its fine-tune at N = nb."""
    L, idx, names = S.pick(["Ctrue", f"CFT@{nb}"], ei, cls, hsel)
    return L, {"candidates": names, "share_fine_tuned_picked": float(np.mean(np.array(names)[idx] == f"CFT@{nb}"))}


def G_of(S, ei, nb, cls=ALL, hsel=None, suffix=None):
    suffix = f"@{nb}" if suffix is None else suffix
    L, idx, names = S.pick([f"FT{suffix}", f"RES{suffix}"], ei, cls, hsel)
    return L, {"candidates": names, "share_FT_picked": float(np.mean(np.array(names)[idx] == f"FT{suffix}"))}


def D_of(S, ei, nb, cls=ALL):
    L, idx, names = S.pick([f"Dnet@{nb}", f"Dridge@{nb}"], ei, cls)
    return L, {"candidates": names, "share_net_picked": float(np.mean(np.array(names)[idx] == f"Dnet@{nb}"))}


def g_rule(S, ei, nb, cls, hsel=None, c_fixed=None):
    """g = (L(P0) - L(G)) / (L(P0) - L(C)) with the declared rule on d_t = a_t - 0.7 b_t."""
    P0 = S.L("P0", ei, cls=cls, hsel=hsel)
    Lg, gi = G_of(S, ei, nb, cls, hsel)
    if c_fixed is None:
        Lc, ci = C_of(S, ei, nb, cls, hsel)
    else:
        Lc, ci = S.L(c_fixed, ei, cls=cls, hsel=hsel), {"candidates": [c_fixed]}
    a, b = P0 - Lg, P0 - Lc
    r, d, sb = ratio(a, b), stat(a - 0.7 * b), stat(b)
    read = bool(sb["mean"] > 2 * sb["se"])
    verdict = "not read (L(P0) - L(C) within 2 SE): undecided" if not read else \
        ("confirmed" if d["lower90"] >= 0 else "refuted" if d["upper90"] < 0 else "undecided")
    return {"g": r["value"], "g_se": r["se"], "g_lower90": r["lower90"], "g_upper90": r["upper90"],
            "g_median_of_per_truth_ratios": r["median_of_per_truth_ratios"], "g_loo_range": [r["loo_min"], r["loo_max"]],
            "g_per_truth": r["per_truth"], "g_per_seed": r["per_seed"],
            "contrast_d": d, "gap_P0_minus_C": sb, "gap_exceeds_2se": read, "verdict": verdict, "G": gi, "C": ci,
            "classes": list(cls), "budget": int(nb)}


def skills(S, ei, cls=ALL):
    """(L(K) - L) / (L(K) - L(O)) of every scored policy, pooled over truths and seeds (`score` half)."""
    K, O = S.L("K", ei, cls=cls).mean(), S.L("O", ei, cls=cls).mean()
    out = {}
    for n in sorted(S.d):
        if S.has(n):
            L = S.L(n, ei, cls=cls)
            if np.isfinite(L).all():
                out[n] = {"L": float(L.mean()), "skill_vs_O": float((K - L.mean()) / (K - O))}
    return out


def criteria(S, nb=8, d_col=32, r5_sigma=0.018, r5_se=0.004):
    """Every declared criterion with its number and verdict. eta = 0 is index 0, eta = 4 the last index."""
    e0, e4 = 0, len(S.etas) - 1
    out = {"etas": S.etas, "primary_budget": int(nb)}
    # ---- zero point (R13)
    z = {}
    K, Cp, P0 = S.L("K", e0), S.L("Cpub", e0), S.L("P0", e0)
    den = K - Cp
    if S.has(f"Dnet@{d_col}") or S.has(f"Dridge@{d_col}"):
        D, di = D_of(S, e0, d_col)
        null_is = "D" if D.mean() <= P0.mean() else "P0"
    else:
        D, di, null_is = None, None, "P0"
    sg = ratio((D if null_is == "D" else P0) - Cp, den)
    comb = float(np.sqrt(r5_se ** 2 + sg["se"] ** 2))
    z["sigma_0"] = {**sg, "null_is": null_is, "D": di, "round5": [r5_sigma, r5_se], "se_of_difference": comb,
                    "holds": bool(abs(sg["value"] - r5_sigma) <= 2 * comb),
                    "holds_stricter_within_2_round5_se": bool(abs(sg["value"] - r5_sigma) <= 2 * r5_se)}
    pairs = {"trueformC_vs_publicC": ("Ctrue", "Cpub"), f"FT{nb}_vs_P0": (f"FT@{nb}", "P0"), f"RES{nb}_vs_P0": (f"RES@{nb}", "P0")}
    ok = [z["sigma_0"]["holds"]]
    for k, (x, y) in pairs.items():
        if not S.has(x, y):
            z[k] = {"available": False}
            ok.append(False)
            continue
        r = ratio(S.L(x, e0) - S.L(y, e0), den)
        z[k] = {**r, "tolerance": 0.02, "holds": bool(abs(r["value"]) <= 0.02)}
        ok.append(z[k]["holds"])
    z["holds"] = bool(all(ok))
    out["zero_point"] = z
    # ---- s (R14)
    s = {}
    if S.has("Ctrue"):
        for key, cls in (("aimed_regional", TRIG), ("all_classes", ALL)):
            P0c, Kc = S.L("P0", e4, cls=cls), S.L("K", e4, cls=cls)
            Lc, ci = C_of(S, e4, nb, cls)
            s[key] = {**ratio(P0c - Lc, Kc - Lc), "C": ci}
            Lt = S.L("Ctrue", e4, cls=cls)
            s[key + "_trueform_net_alone"] = ratio(P0c - Lt, Kc - Lt)
            s[key + "_at_eta0"] = ratio(S.L("P0", e0, cls=cls) - S.L("Ctrue", e0, cls=cls), S.L("K", e0, cls=cls) - S.L("Ctrue", e0, cls=cls))
        v = s["aimed_regional"]["value"]
        s["value"], s["forecast"] = v, 0.20
        s["standin_holds"] = bool(0.10 <= v <= 0.30)
        s["study_fails_s_below_0.05"] = bool(v < 0.05)
    out["s"] = s
    # ---- g (R15)
    g = {}
    if S.has("P0", "Ctrue") and (S.has(f"FT@{nb}") or S.has(f"RES@{nb}")):
        g["primary_all_classes"] = g_rule(S, e4, nb, ALL)
        g["secondary_aimed_regional"] = g_rule(S, e4, nb, TRIG)
        g["verdict"] = g["primary_all_classes"]["verdict"]
    out["g"] = g
    fails = (not z["holds"]) or bool(s.get("study_fails_s_below_0.05", False))
    out["study_fails"] = {"value": bool(fails), "why": [w for w, c in (("zero point misses", not z["holds"]),
                                                                    ("s < 0.05", bool(s.get("study_fails_s_below_0.05", False)))) if c]}
    return out


def first_look(d, classes, etas, nb, d_col):
    """A few numbers for the job's log (no SE)."""
    S = Scores(d, classes, etas)
    out = {}
    for ei, eta in enumerate(S.etas):
        sk = skills(S, ei)
        out[f"eta{eta:g}"] = {k: round(v["skill_vs_O"], 3) for k, v in sk.items() if "@r" not in k}
    try:
        c = criteria(S, nb, d_col)
        out["zero_holds"] = c["zero_point"]["holds"]
        out["sigma_0"] = round(c["zero_point"]["sigma_0"]["value"], 4)
        if c["s"]:
            out["s"] = round(c["s"]["value"], 3)
        if c["g"]:
            p = c["g"]["primary_all_classes"]
            out["g"] = [round(p["g"], 3), round(p["g_lower90"], 3), round(p["g_upper90"], 3), p["verdict"]]
    except Exception as exc:                              # not every policy is scored yet
        out["criteria"] = f"not yet: {exc!r}"[:120]
    return out
