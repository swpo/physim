"""a3_stats -- study dialsA3: the declared criteria from per-item scores (numpy only).

dialsA2's criteria (`../dialsA2/a2_stats.py`, imported unchanged: T1 to T5, the statistics, the picks) with the zero
point re-declared (DECLARED.md A3-3): at eta 0, N = 8, in units of mean_t [L(K) - L(public-form C)], |mean_t of the
pair's difference| <= 0.02 for (i) true-form C - public-form C, (ii) G* - S(8), (iii) H(8) - S(8); all three must
hold. G* - P0 and H - P0 are reported, not in the rule; dialsA2's zero point (with G* - P0 in place of G* - S) is
reported beside it. The verdict: PASS = T1-T5 and the zero point; FAIL = T1's upper bound < 0.15 or T2's lower bound
> 0.7 (read whatever the zero point); otherwise UNDECIDED.
"""
from __future__ import annotations

import os
import sys

import numpy as np

_A2 = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dialsA2")
if _A2 not in sys.path:
    sys.path.insert(0, _A2)
import a2_stats as A2S  # noqa: E402
from a_stats import Scores, ratio, stat  # noqa: E402,F401

G_names, C_names, picked, shares, recoveries, skills = (A2S.G_names, A2S.C_names, A2S.picked, A2S.shares,
                                                        A2S.recoveries, A2S.skills)
TOL = 0.02


def zero_point(S, nb=8, e0=0):
    """DECLARED A3-3 (in the rule) and the pairs reported beside it."""
    z = {}
    Kz, Cp = S.L("K", e0), S.L("Cpub", e0)
    unit = float((Kz - Cp).mean())
    Gz = picked(S, G_names(nb), e0)["L"]
    Sz = S.L(f"S@{nb}", e0) if S.has(f"S@{nb}") else None
    Hz = S.L(f"H@{nb}", e0) if S.has(f"H@{nb}") else None
    terms = {"trueformC_vs_publicC": (S.L("Ctrue", e0), Cp, True),
             "Gstar_vs_S": (Gz, Sz, True),
             "H_vs_S": (Hz, Sz, True),
             "Gstar_vs_P0 (reported; dialsA2's pair)": (Gz, S.L("P0", e0), False),
             "H_vs_P0 (reported)": (Hz, S.L("P0", e0), False)}
    zok = []
    for k, (a, b, rule) in terms.items():
        if a is None or b is None:
            z[k] = {"available": False, "holds": False, "in_rule": rule}
            if rule:
                zok.append(False)
            continue
        st = stat(a - b)
        v = st["mean"] / unit
        z[k] = {"value": v, "se": st["se"] / abs(unit), "median": st["median_truths"] / unit,
                "loo": [st["loo_min"] / unit, st["loo_max"] / unit], "lower90": st["lower90"] / unit,
                "upper90": st["upper90"] / unit, "per_truth": (np.asarray(st["per_truth"]) / unit).tolist()
                if "per_truth" in st else None, "tolerance": TOL, "holds": bool(abs(v) <= TOL), "in_rule": rule}
        if rule:
            zok.append(z[k]["holds"])
    z["unit_K_minus_publicC"] = unit
    z["holds"] = bool(all(zok))
    z["dialsA2_rule_holds (reported)"] = bool(z["trueformC_vs_publicC"].get("holds", False)
                                              and z["Gstar_vs_P0 (reported; dialsA2's pair)"].get("holds", False)
                                              and z["H_vs_S"].get("holds", False))
    return z


def criteria(S, nb=8, e0=0, e4=1):
    """Every declared criterion with its number and verdict (DECLARED Part 1, R17, A3-3, A3-11)."""
    out = A2S.criteria(S, nb, e0, e4)
    out["zero_point_dialsA2_rule (reported)"] = out.pop("zero_point")
    z = zero_point(S, nb, e0)
    out["zero_point"] = z
    T1, T2 = out["T1"], out["T2"]
    passed = all([T1["holds"], T2["holds"], out["T3"]["holds"], out["T4"]["holds"], out["T5"]["holds"], z["holds"]])
    failed = T1["fails"] or T2["fails"]
    out["verdict"] = "PASS" if passed and not failed else ("FAIL" if failed else "UNDECIDED")
    out["verdict_parts"] = {"T1": T1["holds"], "T2": T2["holds"], "T3": out["T3"]["holds"], "T4": out["T4"]["holds"],
                            "T5": out["T5"]["holds"], "zero_point": z["holds"], "T1_fails": T1["fails"],
                            "T2_fails": T2["fails"]}
    return out


def first_look(d, classes, etas, nb=8):
    """A few numbers for the job's log (never stops the job)."""
    S = Scores(d, classes, etas)
    out = {f"eta{e:g}": {k: round(v["skill_vs_O"], 3) for k, v in skills(S, i).items() if "@r" not in k}
           for i, e in enumerate(S.etas)}
    try:
        c = criteria(S, nb, 0, len(S.etas) - 1)
        out["verdict"] = c["verdict"]
        out["parts"] = c["verdict_parts"]
        out["sigma_G"] = round(c["T1"]["sigma_G"]["value"], 3)
        out["rho_G"] = round(c["T2"]["rho_G"]["value"], 3)
        out["zero_point"] = {k: round(v["value"], 4) for k, v in c["zero_point"].items()
                             if isinstance(v, dict) and "value" in v}
        if c["T3"].get("recovery"):
            out["H_recovery"] = round(c["T3"]["recovery"]["value"], 3)
            out["H_t"] = round(c["T3"]["t"], 2)
    except Exception as exc:
        out["criteria"] = f"not yet: {exc!r}"[:160]
    return out
