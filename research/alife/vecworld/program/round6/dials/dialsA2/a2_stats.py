"""a2_stats -- study dialsA2: the declared criteria (DECLARED.md Part 1 and R17) from per-item scores (numpy only).

Scores: name -> (n_eta, n_truth, n_seed, 2, n_items, n_h) fair energy scores, half 0 = `sel` (picks only), half 1 =
`score`; horizons (8, 12, 16); classes 'c' aimed, 'd' regional. L of a policy = mean over items of the score summed
over the horizons asked; lower is better. Statistics, bounds, ratios: study A's (`../dialsA/a_stats.py`: per-truth
contrasts averaged over seeds, SE^2 = SD_truths^2 / n + SD_seeds^2 / 3, one-sided 90% bounds with t(0.90, n - 1)).
Picks are made per truth and seed on `sel`, pooled over items and horizons, and scored on `score`.
"""
from __future__ import annotations

import os
import sys

import numpy as np

_A = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dialsA")
if _A not in sys.path:
    sys.path.insert(0, _A)
from a_stats import Scores, ratio, stat  # noqa: E402

ALL = ("c", "d")
H8, H16 = [0], [2]                                   # horizon indices of 8 and 16 ticks in (8, 12, 16)


def G_names(nb):
    return ["P0", f"Dnet@{nb}", f"Dridge@{nb}", f"S@{nb}", f"FT@{nb}", f"RES@{nb}"]


def C_names(nb):
    return ["Ctrue", f"CFT@{nb}"]


def picked(S, names, ei, cls=ALL, hsel=None, partner=None):
    """L on `score` (n_truth, n_seed) of the candidate picked on `sel`; with `partner` {name: other name} also
    the L of the partner of the picked candidate (the blind copy of C), and the shares picked."""
    names = [n for n in names if S.has(n)]
    L, idx, nm = S.pick(names, ei, cls, hsel)
    out = {"L": L, "idx": idx, "names": nm,
           "share_picked": {n: float(np.mean(idx == i)) for i, n in enumerate(nm)}}
    if partner is not None:
        sc = np.stack([S.L(partner[n], ei, half=1, cls=cls, hsel=hsel) for n in nm])
        out["L_partner"] = np.take_along_axis(sc, idx[None], 0)[0]
    return out


def shares(S, ei, nb, cls=ALL, hsel=None, drop=None):
    """sigma_G, rho_G and their declared contrasts; drop: a truth index left out."""
    K = S.L("K", ei, cls=cls, hsel=hsel)
    P0 = S.L("P0", ei, cls=cls, hsel=hsel)
    G = picked(S, G_names(nb), ei, cls, hsel)
    C = picked(S, C_names(nb), ei, cls, hsel)
    Lg, Lc = G["L"], C["L"]
    if drop is not None:
        keep = np.arange(K.shape[0]) != drop
        K, P0, Lg, Lc = K[keep], P0[keep], Lg[keep], Lc[keep]
    sig = ratio(Lg - Lc, K - Lc)
    rho = ratio(P0 - Lg, P0 - Lc)
    t1 = stat(Lg - 0.85 * Lc - 0.15 * K)
    d2 = stat((P0 - Lg) - 0.7 * (P0 - Lc))
    gap = stat(P0 - Lc)
    return {"sigma_G": sig, "rho_G": rho, "T1_contrast": t1, "T2_contrast": d2, "gap_P0_minus_C": gap,
            "G_share_picked": G["share_picked"], "C_share_picked": C["share_picked"],
            "L": {"K": stat(K), "P0": stat(P0), "Gstar": stat(Lg), "C": stat(Lc)}}


def criteria(S, nb=8, e0=0, e4=1):
    """Every declared criterion with its number and verdict (DECLARED Part 1, R17)."""
    out = {"etas": S.etas, "budget": int(nb)}
    # ---- T1, T2 at eta 4, pooled horizons
    sh = shares(S, e4, nb)
    t1 = sh["T1_contrast"]
    T1 = {"sigma_G": sh["sigma_G"], "contrast": t1, "holds": bool(t1["lower90"] >= 0), "fails": bool(t1["upper90"] < 0)}
    read = bool(sh["gap_P0_minus_C"]["mean"] > 2 * sh["gap_P0_minus_C"]["se"])
    d2 = sh["T2_contrast"]
    T2 = {"rho_G": sh["rho_G"], "contrast": d2, "gap_P0_minus_C": sh["gap_P0_minus_C"], "read": read,
          "holds": bool(read and d2["upper90"] <= 0), "fails": bool(read and d2["lower90"] > 0)}
    out["T1"], out["T2"] = T1, T2
    out["picks"] = {"G": sh["G_share_picked"], "C": sh["C_share_picked"]}
    out["L_eta4"] = sh["L"]
    # ---- T3: H against the gap and against G*
    K = S.L("K", e4)
    P0 = S.L("P0", e4)
    Lc = picked(S, C_names(nb), e4)["L"]
    Lg = picked(S, G_names(nb), e4)["L"]
    if S.has(f"H@{nb}"):
        Lh = S.L(f"H@{nb}", e4)
        rec = ratio(P0 - Lh, P0 - Lc)
        beat = stat(Lg - Lh)
        tval = beat["mean"] / beat["se"] if beat["se"] > 0 else float("inf") * np.sign(beat["mean"])
        out["T3"] = {"recovery": rec, "G_minus_H": beat, "t": float(tval),
                     "holds": bool(rec["value"] >= 0.7 and tval >= 3.0)}
    else:
        out["T3"] = {"available": False, "holds": False}
    # ---- T4: blind C
    partner = {"Ctrue": "Ctrue_blind", f"CFT@{nb}": f"CFT_blind@{nb}"}
    if all(S.has(v) for v in partner.values()):
        C = picked(S, C_names(nb), e4, partner=partner)
        loss = ratio(C["L_partner"] - C["L"], K - C["L"])
        out["T4"] = {"blind_loss_share": loss, "holds": bool(loss["value"] >= 0.10)}
    else:
        out["T4"] = {"available": False, "holds": False}
    # ---- T5: heaviest truth out; 8 and 16 ticks alone
    gap_t = (P0 - Lc).mean(1)
    hv = int(np.argmax(gap_t))
    t5 = {"heaviest_truth_index": hv, "heaviest_truth_gap": float(gap_t[hv])}
    ok = []
    for key, kw in (("heaviest_left_out", {"drop": hv}), ("at_8_ticks", {"hsel": H8}), ("at_16_ticks", {"hsel": H16})):
        r = shares(S, e4, nb, **kw)
        s_ok = bool(r["sigma_G"]["value"] >= 0.15)
        r_ok = bool(r["rho_G"]["value"] <= 0.7)
        t5[key] = {"sigma_G": r["sigma_G"]["value"], "rho_G": r["rho_G"]["value"], "sigma_ok": s_ok, "rho_ok": r_ok,
                   "sigma_G_full": r["sigma_G"], "rho_G_full": r["rho_G"]}
        ok += [s_ok, r_ok]
    t5["worst_single_leave_out"] = {"sigma_G": sh["sigma_G"]["loo_min"], "rho_G": sh["rho_G"]["loo_max"]}
    t5["holds"] = bool(all(ok))
    out["T5"] = t5
    # ---- zero point at eta 0
    z = {}
    Kz, Cp = S.L("K", e0), S.L("Cpub", e0)
    unit = float((Kz - Cp).mean())
    Gz = picked(S, G_names(nb), e0)["L"]
    terms = {"trueformC_vs_publicC": (S.L("Ctrue", e0), Cp, True),
             "Gstar_vs_P0": (Gz, S.L("P0", e0), True),
             "H_vs_S": (S.L(f"H@{nb}", e0) if S.has(f"H@{nb}") else None, S.L(f"S@{nb}", e0) if S.has(f"S@{nb}") else None, True),
             "Gstar_vs_S (reported)": (Gz, S.L(f"S@{nb}", e0) if S.has(f"S@{nb}") else None, False),
             "H_vs_P0 (reported)": (S.L(f"H@{nb}", e0) if S.has(f"H@{nb}") else None, S.L("P0", e0), False)}
    zok = []
    for k, (a, b, rule) in terms.items():
        if a is None or b is None:
            z[k] = {"available": False, "holds": False}
            if rule:
                zok.append(False)
            continue
        st = stat(a - b)
        v = st["mean"] / unit
        z[k] = {"value": v, "se": st["se"] / abs(unit), "median": st["median_truths"] / unit,
                "loo": [st["loo_min"] / unit, st["loo_max"] / unit], "tolerance": 0.02, "holds": bool(abs(v) <= 0.02),
                "in_rule": rule}
        if rule:
            zok.append(z[k]["holds"])
    z["unit_K_minus_publicC"] = unit
    z["holds"] = bool(all(zok))
    out["zero_point"] = z
    # ---- verdict
    passed = all([T1["holds"], T2["holds"], out["T3"]["holds"], out["T4"]["holds"], t5["holds"], z["holds"]])
    failed = T1["fails"] or T2["fails"]
    out["verdict"] = "PASS" if passed and not failed else ("FAIL" if failed else "UNDECIDED")
    out["verdict_parts"] = {"T1": T1["holds"], "T2": T2["holds"], "T3": out["T3"]["holds"], "T4": out["T4"]["holds"],
                            "T5": t5["holds"], "zero_point": z["holds"], "T1_fails": T1["fails"], "T2_fails": T2["fails"]}
    return out


def recoveries(S, ei, nb, names, cls=ALL, hsel=None):
    """Reported: (L(P0) - L(X)) / (L(P0) - L(C)) for each named policy (C of DECLARED R10 at nb)."""
    P0 = S.L("P0", ei, cls=cls, hsel=hsel)
    Lc = picked(S, C_names(nb), ei, cls, hsel)["L"]
    out = {}
    for n in names:
        if S.has(n):
            out[n] = ratio(P0 - S.L(n, ei, cls=cls, hsel=hsel), P0 - Lc)
    if all(S.has(n) for n in G_names(nb)):
        out["Gstar"] = ratio(P0 - picked(S, G_names(nb), ei, cls, hsel)["L"], P0 - Lc)
    return out


def skills(S, ei, cls=ALL, hsel=None):
    K, O = S.L("K", ei, cls=cls, hsel=hsel).mean(), S.L("O", ei, cls=cls, hsel=hsel).mean()
    out = {}
    for n in sorted(S.d):
        if S.has(n):
            L = S.L(n, ei, cls=cls, hsel=hsel)
            if np.isfinite(L).all():
                out[n] = {"L": float(L.mean()), "skill_vs_O": float((K - L.mean()) / (K - O))}
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
        if c["T3"].get("recovery"):
            out["H_recovery"] = round(c["T3"]["recovery"]["value"], 3)
            out["H_t"] = round(c["T3"]["t"], 2)
    except Exception as exc:
        out["criteria"] = f"not yet: {exc!r}"[:160]
    return out
