"""analyse2 -- analysis of GPU job 2 (the fed-vortex exam pilot) beyond the report written on the pod.

    python -B analyse2.py JOB2_OUT_DIR        -> results/analysis2.json   (VX_TAG=B: results/analysis2_B.json)

PILOT: the truths of job 2 are public by design; never to be reused as an exam.

Reads info.json, prediction.json, identification.json, scores.npz, items.npz, design.npz, design_S_*.npz.
  status       did every stage finish (job2 exits 0 even if the report stage fails: the Mac's review, point 5)
  ladder       pooled fair energy score L per policy (mean over items of the mean over the primary cells) and
               its skill (L(K) - L) / (L(K) - L(O)), per family; D@n, S@n, S2@n by budget
  gaps         differences of L between policies with the truth (hidden world) as the unit: mean, SE over
               truths, z = mean / SE, number of truths with the sign of the mean; item-level SE beside it
  acceptance   sigma and rho (round5/agentenv/evaluator/acceptance.py) per family and budget, with the
               references varied: K = the truth's own climatology (the job's choice) or K0 = the prior
               climatology; cells = joint (the job's primary cells), s_b only, N only; per horizon
  theory       roadmap policy T = the level-2 effective law with constants fitted to n Lab episodes
               (law|D@n) against the data-only net and ridge (D@n) and against P0
  cchg         share of the oracle-predictable change of (N, s_b) reached by each predictor's mean, within
               truths, with a bootstrap over truths (the round-3 question: linear against nonlinear)
  law_design   the replicator-mutator law on the design episodes (prior draws of theta, public keys):
               d s_b over 16 ticks = b1(theta) s (1 - s) + b2(theta) (1 - 2 s), b linear in theta (box units);
               which hidden parameters set the rate, and how much of the change the law explains
"""
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(1, os.path.join(os.path.dirname(HERE), "agentenv"))
import numpy as np  # noqa: E402

from evaluator import acceptance as ACC  # noqa: E402

D = sys.argv[1]
RES = os.environ.get("VX_RES", os.path.join(HERE, "results"))
MARK = "PILOT_NEVER_REUSE_AS_EXAM"
FAMS = ("net", "ridge", "law", "lin2", "net~3", "ridge~3")   # those present in the job's scores are used


def J(name):
    p = os.path.join(D, name)
    return json.load(open(p)) if os.path.exists(p) else None


info, P, ident = J("info.json"), J("prediction.json"), J("identification.json")
prog = open(os.path.join(D, "progress.txt")).read() if os.path.exists(os.path.join(D, "progress.txt")) else ""
out = {MARK: True, "source_dir": os.path.basename(os.path.normpath(D)),
       "note": "pilot truths are public by design; never to be reused as an exam"}

# ----------------------------------------------------------------------------- status
scan_info = J(os.path.join("scan", "info.json"))
scan_json = J(os.path.join("scan", "scan.json"))
out["status"] = {
    "backend": info.get("backend"), "devices": info.get("devices"), "preset": info.get("preset"), "rate": info.get("rate"),
    "bmax": info.get("bmax"), "hours": info.get("hours"), "failed": info.get("failed"), "fatal": info.get("fatal"),
    "member_ticks_total": info.get("member_ticks_total"), "member_ticks": info.get("member_ticks"),
    "prediction_final": None if P is None else bool(P.get("final")),
    "report_failures_in_progress_txt": prog.count("report failed"),
    "stage_failures_in_progress_txt": [ln[:160] for ln in prog.split("\n") if "FAILED" in ln or "SKIP" in ln][:20],
    "outputs": info.get("outputs"),
    "scan_only_run": None if scan_info is None else {
        "failed": scan_info.get("failed"), "fatal": scan_info.get("fatal"), "hours": scan_info.get("hours"),
        "rate_used": scan_info.get("rate"), "J": (scan_json or {}).get("J"), "anchors": (scan_json or {}).get("anchors"),
        "note": "sized by the old rate table (one row at B = bmax, linear below): J and the anchors fell back to the "
                "smallest design (the Mac's review of r5-vortexexam-003, major point)"}}
PR = info["prior"]
HS = list(PR["hs"])
NAMES = list(PR["names"])

# ----------------------------------------------------------------------------- scores
Z = np.load(os.path.join(D, "scores.npz"))
SC = {k: Z[k].astype(float) for k in Z.files if k != MARK and not k.startswith("mean|")}          # (nT, nI, n_cells)
MU = {k[5:]: Z[k].astype(float) for k in Z.files if k.startswith("mean|")}                        # (nT, nI, nh, 2)
nT, nI, nC = SC["oracle"].shape
CELLS = [(h, c) for h in range(len(HS)) for c in ("joint", "N", "s_b")]
assert nC == len(CELLS)


def cellmask(coord="joint", hsel=None):
    return np.array([(c == coord) and (hsel is None or h == hsel) for h, c in CELLS])


PRIM = cellmask("joint")
Lit = {k: v[:, :, PRIM].mean(2) for k, v in SC.items()}              # (nT, nI) pooled over the primary cells
L = {k: float(v.mean()) for k, v in Lit.items()}
LK, LO = L["K"], L["oracle"]


def skill(k):
    return (LK - L[k]) / (LK - LO)


budgets = sorted({int(k.split("@")[1]) for k in SC if "|D@" in k})
ladder = {"L_K": LK, "L_K0": L.get("K0"), "L_O": LO, "L_O_noinput": L.get("O_noinput"),
          "skill_K0": skill("K0") if "K0" in L else None,
          "skill_O_noinput": skill("O_noinput") if "O_noinput" in L else None,
          "n_truths": nT, "n_items_per_truth": nI, "budgets_episodes": budgets, "families": {}}
for fam in FAMS:
    row = {}
    for pol in ("P0", "PP", "PM", "C", "Cded", "Cft"):
        if f"{fam}|{pol}" in L:
            row[pol] = {"L": L[f"{fam}|{pol}"], "skill": skill(f"{fam}|{pol}")}
    for pol in ("D", "S", "S2", "Sded", "Sft"):
        r_ = {str(n): {"L": L[f"{fam}|{pol}@{n}"], "skill": skill(f"{fam}|{pol}@{n}")} for n in budgets
              if f"{fam}|{pol}@{n}" in L}
        if r_:
            row[pol] = r_
    if row:
        ladder["families"][fam] = row
out["ladder"] = ladder


# ----------------------------------------------------------------------------- gaps clustered by truth
def gap(a, b):
    """L(a) - L(b) (positive: b is better). Unit = truth."""
    if a not in Lit or b not in Lit:
        return None
    d = (Lit[a] - Lit[b])                       # (nT, nI)
    dt = d.mean(1)
    se_t = dt.std(ddof=1) / np.sqrt(nT) if nT > 1 else float("nan")
    se_i = d.std(ddof=1) / np.sqrt(d.size)
    m = float(dt.mean())
    return {"dL": m, "se_truths": float(se_t), "z_truths": float(m / se_t) if se_t > 0 else None,
            "se_items": float(se_i), "z_items": float(m / se_i) if se_i > 0 else None,
            "truths_with_sign_of_mean": int((np.sign(dt) == np.sign(m)).sum()), "n_truths": int(nT),
            "in_skill_units": float(m / (LK - LO))}


gaps = {}
for fam in FAMS:
    for a, b in (("P0", "C"), ("PM", "C"), ("PP", "C"), ("C", "Cded"), ("P0", "Cded"), ("PP", "P0"), ("P0", "Cft"),
                 ("C", "Cft"), ("Cded", "Cft"), ("PM", "P0")):
        g = gap(f"{fam}|{a}", f"{fam}|{b}")
        if g:
            gaps[f"{fam}|{a} - {fam}|{b}"] = g
    for n in budgets:
        for a, b in ((f"S@{n}", "C"), ("P0", f"S@{n}"), (f"D@{n}", "P0"), (f"D@{n}", "C"), (f"D@{n}", f"S@{n}"),
                     (f"S2@{n}", f"S@{n}"), (f"Sded@{n}", "Cded"), ("P0", f"Sded@{n}"), (f"Sft@{n}", "Cft"),
                     ("P0", f"Sft@{n}")):
            g = gap(f"{fam}|{a}", f"{fam}|{b}")
            if g:
                gaps[f"{fam}|{a} - {fam}|{b}"] = g
for pol in ["P0", "C", "PM", "Cded"] + [f"D@{n}" for n in budgets]:
    for a, b in (("lin2", "net"), ("lin2", "law"), ("lin2", "ridge"), ("ridge", "net"), ("law", "net"), ("law", "ridge")):
        g = gap(f"{a}|{pol}", f"{b}|{pol}")
        if g:
            gaps[f"{a}|{pol} - {b}|{pol}"] = g
for pol in ["P0", "C", "PM", "Cded", "Cft"] + [f"D@{n}" for n in budgets] + [f"S@{n}" for n in budgets]:
    for a, b in (("net~3", "net"), ("ridge~3", "ridge"), ("law", "net~3"), ("ridge~3", "net~3")):
        g = gap(f"{a}|{pol}", f"{b}|{pol}")
        if g:
            gaps[f"{a}|{pol} - {b}|{pol}"] = g
for a, b in (("K0", "K"), ("O_noinput", "oracle"), ("K", "net|P0"), ("K", "net|C"), ("net|C", "oracle"), ("net|Cded", "oracle"),
             ("net|Cft", "oracle"), ("net~3|P0", "net|C"), ("net~3|P0", "net|Cft")):
    g = gap(a, b)
    if g:
        gaps[f"{a} - {b}"] = g
out["gaps_L_by_truth"] = {"note": "dL = L(first) - L(second), pooled over the primary cells; positive = the second is "
                                  "better; se_truths = sd over truths of the per-truth mean / sqrt(n_truths)",
                          "pairs": gaps}

# ----------------------------------------------------------------------------- acceptance with varied references
worlds = np.repeat(np.arange(nT), nI)


def flat(k):
    return SC[k].reshape(nT * nI, nC)


ANCH = list(PR["prog_ticks"])
anchor_of = np.tile(np.arange(len(ANCH)), nT * nI // len(ANCH)) if nI % len(ANCH) == 0 else None   # item = (run, anchor)


def acc_row(fam, n, K="K", valid=PRIM, s=None, c=None, d=None, rows=None):
    pol = {"K": K, "D": d or f"{fam}|D@{n}", "P0": f"{fam}|P0", "S": s or f"{fam}|S@{n}", "C": c or f"{fam}|C"}
    if any(pol[q] not in SC for q in ("K", "P0", "C")):
        return None
    sel = slice(None) if rows is None else rows
    a = ACC.shares({q: flat(v)[sel] for q, v in pol.items() if v in SC}, valid, worlds=worlds[sel], n_boot=1000)
    return {"sigma": a["sigma"], "sigma_se_worlds": (a.get("sigma_worlds") or {}).get("se"),
            "sigma_p05_p95_worlds": [(a.get("sigma_worlds") or {}).get(q) for q in ("p05", "p95")],
            "null_is": a["null_is"], "rho": a.get("rho"), "rho_se_worlds": (a.get("rho_worlds") or {}).get("se"),
            "rho_p05_p95_worlds": [(a.get("rho_worlds") or {}).get(q) for q in ("p05", "p95")],
            "pass_sigma": a["pass_sigma"], "pass_rho": a.get("pass_rho"),
            "L": {q: a["L"][q] / max(int(np.sum(valid)), 1) for q in a["L"]},
            "worlds_passing_sigma": int(np.sum(np.array(a["per_world"]["sigma"]) >= 0.15)) if "per_world" in a else None,
            "worlds_passing_rho": int(np.sum(np.array(a["per_world"]["rho"]) <= 0.7)) if "per_world" in a and a.get("rho") is not None else None,
            "n_worlds": a.get("n_worlds")}


acc = {}
variants = {"K|joint": ("K", PRIM), "K0|joint": ("K0", PRIM), "K|s_b": ("K", cellmask("s_b")), "K|N": ("K", cellmask("N")),
            **{f"K|joint|h{HS[j]}": ("K", cellmask("joint", j)) for j in range(len(HS))}}
for fam in FAMS:
    for n in budgets:
        for vn, (Kn, valid) in variants.items():
            if Kn not in SC:
                continue
            r_ = acc_row(fam, n, Kn, valid)
            if r_:
                acc[f"{fam}@{n}|{vn}"] = r_
        if f"{fam}|Cded" in SC:
            r_ = acc_row(fam, n, "K", PRIM, s=f"{fam}|Sded@{n}", c=f"{fam}|Cded")
            if r_:
                acc[f"{fam}@{n}|K|joint|dedicated"] = r_
        if f"{fam}|Cft" in SC:
            r_ = acc_row(fam, n, "K", PRIM, s=f"{fam}|Sft@{n}", c=f"{fam}|Cft")
            if r_:
                acc[f"{fam}@{n}|K|joint|finetuned"] = r_
        if fam.endswith("~3") and f"{fam.split('~')[0]}|C" in SC:
            # short-history null against the full-history C of the same base family: what the item's history is
            # worth to a policy that cannot infer the parameters (reported, not an acceptance quantity)
            b = fam.split("~")[0]
            cbest = f"{b}|Cft" if f"{b}|Cft" in SC else f"{b}|C"
            r_ = acc_row(fam, n, "K", PRIM, c=cbest)
            if r_:
                acc[f"{fam}@{n}|K|joint|C_full_history"] = r_
        if anchor_of is not None and n == budgets[-1]:           # by anchor tick (history length), largest budget
            for ai, a_ in enumerate(ANCH):
                r_ = acc_row(fam, n, "K", PRIM, rows=np.flatnonzero(anchor_of == ai))
                if r_:
                    acc[f"{fam}@{n}|K|joint|anchor{a_}"] = r_
# the strongest null and the strongest C over the families (not the roadmap's one-family rule; a sensitivity),
# separately for the full-history view and the short-history view (net~3, ridge~3 and the law family)
best = {}
rng_b = np.random.default_rng(5)
for n in budgets:
    for view, ok in (("full_history", lambda k: "~" not in k), ("short_history", lambda k: "~" in k or k.startswith("law|"))):
        cands_null = [k for k in SC if ok(k) and (k.endswith("|P0") or k.endswith(f"|D@{n}"))]
        cands_c = [k for k in SC if ok(k) and k.split("|")[-1] in ("C", "Cded", "Cft")]
        cands_s = [k for k in SC if ok(k) and k.split("|")[-1] in (f"S@{n}", f"Sded@{n}", f"Sft@{n}")]
        if cands_null and cands_c:
            kn, kc = min(cands_null, key=lambda k: L[k]), min(cands_c, key=lambda k: L[k])
            kp0 = min([k for k in SC if ok(k) and k.endswith("|P0")], key=lambda k: L[k])
            ks = min(cands_s, key=lambda k: L[k]) if cands_s else None
            dn, dc = (Lit[kn] - Lit[kc]).mean(1), (Lit["K"] - Lit[kc]).mean(1)       # per truth
            bsig = np.array([dn[q].mean() / dc[q].mean() for q in rng_b.integers(0, nT, size=(1000, nT))])
            best.setdefault(view, {})[str(n)] = {
                "null": kn, "C": kc, "P0": kp0, "S": ks, "sigma": (L[kn] - L[kc]) / (LK - L[kc]),
                "sigma_se_truths": float(bsig.std()),
                "rho": None if ks is None or L[kp0] == L[kc] else (L[kp0] - L[ks]) / (L[kp0] - L[kc])}
out["acceptance"] = {"note": "rows 'family@n|K reference|cells'; sigma = (L(null) - L(C)) / (L(K) - L(C)), null = the "
                             "better of D@n and P0; rho = (L(P0) - L(S@n)) / (L(P0) - L(C)); SE and 5-95% range from the "
                             "bootstrap clustered by truth; L per cell (mean over the cells used); 'anchor<t>' = only the items "
                             "whose history ends at tick t (largest budget)",
                     "rows": acc, "best_over_families": best}

# ----------------------------------------------------------------------------- theory policy T = law|D@n
theory = {}
for n in budgets:
    t = f"law|D@{n}"
    if t not in L:
        continue
    row = {"L_T": L[t], "skill_T": skill(t)}
    for other in (f"net|D@{n}", f"ridge|D@{n}", f"lin2|D@{n}", "net|P0", "law|P0", "net|C", "law|C", f"net|S@{n}"):
        g = gap(other, t)
        if g:
            row[f"{other} - T"] = {k: g[k] for k in ("dL", "se_truths", "z_truths", "in_skill_units", "truths_with_sign_of_mean")}
    if f"net|D@{n}" in L and "net|C" in L and L[f"net|D@{n}"] != L["net|C"]:
        # how far T goes from the data-only net towards the net trained at the truth (1 = as good as C)
        row["share_of_D_to_C_gap_closed_by_T"] = (L[f"net|D@{n}"] - L[t]) / (L[f"net|D@{n}"] - L["net|C"])
    theory[str(n)] = row
out["theory_T"] = {"note": "T = the replicator-mutator law for s_b and linear relaxation for N with constants fitted to the "
                           "first n Lab episodes (vxnet.fit_law); it never runs level 0", "by_budget": theory}

# ----------------------------------------------------------------------------- share of the predictable change reached
items = np.load(os.path.join(D, "items.npz"))
Yt = items["Y"].astype(float)                                         # (nT, nI, R, nh, 2)
La = items["L2a"].astype(float)                                       # (nT, nI, 2)
chg = Yt - La[:, :, None, None, :]
Vc_t = ((chg - chg.mean((1, 2), keepdims=True)) ** 2).mean((1, 2))     # (nT, nh, 2) about each truth's own mean change
Vu_t = Yt.var(2, ddof=1).mean(1)                                      # (nT, nh, 2)
chg_all = chg.reshape(nT * nI, -1, len(HS), 2)
Vc_p = ((chg_all - chg_all.mean((0, 1), keepdims=True)) ** 2).mean((0, 1))
Vu_p = Vu_t.mean(0)
rng = np.random.default_rng(0)
boots = rng.integers(0, nT, size=(1000, nT))
cchg = {"hs_ticks": HS, "coords": ["N", "s_b"],
        "oracle_predictable_share_within_truth": (1 - Vu_t.sum(0) / Vc_t.sum(0)).tolist(),
        "oracle_predictable_share_pooled": (1 - Vu_p / Vc_p).tolist(),
        "between_truth_share_of_pooled_change_variance": (1 - Vc_t.mean(0) / Vc_p).tolist(),
        "reached_within_truth": {}, "reached_pooled": {},
        "note": "reached = (V_change - Ve) / (V_change - Vu), Ve = mean squared error of the predictive mean; "
                "se = bootstrap over truths; rows = horizons, columns = (N, s_b)"}
keep = [k for k in MU if k in ("K", "K0", "anchor", "O_noinput") or k.split("|")[-1] in ("P0", "C", "PM", "Cded", "Cft")
        or k.split("@")[-1] in (str(budgets[-1]) if budgets else "", "4")]
for k in keep:
    Ve_t = ((Yt - MU[k][:, :, None]) ** 2).mean((1, 2))               # (nT, nh, 2)
    num, den = Vc_t - Ve_t, Vc_t - Vu_t
    val = num.sum(0) / den.sum(0)
    bs = np.array([num[b].sum(0) / den[b].sum(0) for b in boots])
    cchg["reached_within_truth"][k] = {"value": val.tolist(), "se_truths": bs.std(0).tolist()}
    Ve_p = Ve_t.mean(0)
    cchg["reached_pooled"][k] = ((Vc_p - Ve_p) / (Vc_p - Vu_p)).tolist()
# nonlinear against linear at the true parameters: difference of reached shares with the truth bootstrap
for a, b in (("net|C", "lin2|C"), ("law|C", "lin2|C"), ("ridge|C", "lin2|C"), ("net|Cded", "lin2|Cded"), ("net|C", "law|C"),
             ("net|C", "net|P0"), ("net|Cded", "net|P0"), ("net|Cft", "net|P0"), ("net|P0", "lin2|P0"), ("net|P0", "ridge|P0"),
             ("net|Cft", "lin2|Cded"), ("net|P0", "net~3|P0")):
    if a in MU and b in MU:
        na = Vc_t - ((Yt - MU[a][:, :, None]) ** 2).mean((1, 2))
        nb = Vc_t - ((Yt - MU[b][:, :, None]) ** 2).mean((1, 2))
        den = Vc_t - Vu_t
        d = (na.sum(0) - nb.sum(0)) / den.sum(0)
        bs = np.array([(na[q].sum(0) - nb[q].sum(0)) / den[q].sum(0) for q in boots])
        cchg.setdefault("differences_within_truth", {})[f"{a} - {b}"] = {
            "value": d.tolist(), "se_truths": bs.std(0).tolist(), "z": (d / np.maximum(bs.std(0), 1e-12)).tolist()}
out["cchg"] = cchg

# ----------------------------------------------------------------------------- the law on the design episodes
dz = np.load(os.path.join(D, "design.npz"))
parts = sorted(glob.glob(os.path.join(D, "design_S_*.npz")))
if parts:
    Sd = np.concatenate([np.load(p)["S"].astype(np.float32) for p in parts])            # (E, T+1, 14)
    u = dz["u"].astype(float)                                                             # (N_theta, d)
    Kd = int(dz["K_d"])
    E = Sd.shape[0]
    th_of = np.repeat(np.arange(len(u)), Kd)[:E]
    viable = dz["viable"].reshape(-1)[:E].astype(bool)
    T1 = Sd.shape[1]
    h = 16 if T1 > 100 else 2
    t0 = 100 if T1 > 100 else 4
    stride = 4 if T1 > 100 else 1
    tt = np.arange(t0, T1 - h, stride)
    s = Sd[:, :, 1].astype(float)
    a = s[:, tt]
    dsb = s[:, tt + h] - a
    g, m = a * (1 - a), 1 - 2 * a
    d_th = u.shape[1]

    def design(cols_theta, quad_eps=False):
        """Columns: g, m, and g u_i, m u_i for i in cols_theta (b1, b2 linear in theta)."""
        cs = [g, m]
        for i in cols_theta:
            ui = u[th_of, i][:, None]
            cs += [g * ui, m * ui]
        if quad_eps:
            cs += [g * (u[th_of, 0][:, None] ** 2)]
        return np.stack(cs, -1)                                                          # (E, nt, p)

    ok = viable
    y = dsb[ok]
    var_y = float(y.var())

    def fit(cols_theta, quad_eps=False):
        A = design(cols_theta, quad_eps)[ok]
        p = A.shape[-1]
        coef = np.linalg.lstsq(A.reshape(-1, p), y.reshape(-1), rcond=None)[0]
        r2 = 1 - float(((y - A @ coef) ** 2).mean()) / var_y
        return coef, r2, A

    coef_all, r2_all, A_all = fit(range(d_th))
    coef_eps, r2_eps, _ = fit([0])
    coef_none, r2_none, _ = fit([])
    coef_q, r2_q, _ = fit(range(d_th), quad_eps=True)
    # bootstrap over design points (thetas): per-theta normal-equation blocks
    p = A_all.shape[-1]
    th_ok = th_of[ok]
    ids = np.unique(th_ok)
    AtA = np.zeros((len(ids), p, p))
    Aty = np.zeros((len(ids), p))
    for q, i in enumerate(ids):
        Ai = A_all[th_ok == i].reshape(-1, p)
        yi = y[th_ok == i].reshape(-1)
        AtA[q], Aty[q] = Ai.T @ Ai, Ai.T @ yi
    bs = []
    for _ in range(300):
        k = rng.integers(0, len(ids), len(ids))
        bs.append(np.linalg.solve(AtA[k].sum(0) + 1e-9 * np.eye(p), Aty[k].sum(0)))
    se = np.array(bs).std(0)
    lab = ["b1_0", "b2_0"] + [f"{b}_{n}" for n in NAMES for b in ("b1", "b2")]
    hw = (np.array(PR["hi"], float) - np.array(PR["lo"], float)) / 2
    cen = (np.array(PR["hi"], float) + np.array(PR["lo"], float)) / 2
    # per-theta rate (own b1, b2 from its episodes) -> how much of its variation over the prior does eps explain
    b_th = np.full((len(ids), 2), np.nan)
    for q, i in enumerate(ids):
        Ai = np.stack([g[ok][th_ok == i].reshape(-1), m[ok][th_ok == i].reshape(-1)], 1)
        b_th[q] = np.linalg.lstsq(Ai, y[th_ok == i].reshape(-1), rcond=None)[0]
    U1 = np.concatenate([np.ones((len(ids), 1)), u[ids]], 1)
    cb = np.linalg.lstsq(U1, b_th[:, 0], rcond=None)[0]
    r2_b1_all = 1 - ((b_th[:, 0] - U1 @ cb) ** 2).sum() / ((b_th[:, 0] - b_th[:, 0].mean()) ** 2).sum()
    ce = np.linalg.lstsq(U1[:, :2], b_th[:, 0], rcond=None)[0]
    r2_b1_eps = 1 - ((b_th[:, 0] - U1[:, :2] @ ce) ** 2).sum() / ((b_th[:, 0] - b_th[:, 0].mean()) ** 2).sum()
    out["law_design"] = {
        "h_ticks": h, "states_from_tick": t0, "stride": stride, "n_episodes_viable": int(ok.sum()), "n_episodes": int(E),
        "n_thetas": int(len(ids)), "var_of_change": var_y,
        "share_explained": {"law_constants_fixed": r2_none, "law_b_linear_in_eps_only": r2_eps,
                            "law_b_linear_in_all_theta": r2_all, "plus_eps_squared_in_b1": r2_q},
        "coefficients_box_units": {k: {"value": float(v), "se_thetas": float(e)} for k, v, e in zip(lab, coef_all, se)},
        "b1_at_box_centre": float(coef_all[0]),
        "b1_slope_per_unit_eps": float(coef_all[2] / hw[0]),
        "b1_zero_crossing_eps_at_centre_of_others": float(cen[0] - coef_all[0] / coef_all[2] * hw[0]) if coef_all[2] else None,
        "b1_relative_change_across_box": {n: float(2 * coef_all[2 + 2 * i] / coef_all[0]) for i, n in enumerate(NAMES)},
        "b2_at_box_centre": float(coef_all[1]),
        "b2_relative_change_across_box": {n: float(2 * coef_all[3 + 2 * i] / coef_all[1]) for i, n in enumerate(NAMES)},
        "per_theta_b1": {"r2_linear_in_all_theta": float(r2_b1_all), "r2_linear_in_eps_only": float(r2_b1_eps),
                         "sd_over_thetas": float(b_th[:, 0].std()),
                         "note": "b1 fitted per design point from its own episodes (noisy), then regressed on theta"},
        "note": "d s_b over h ticks = (b1_0 + sum_i b1_i u_i) s (1 - s) + (b2_0 + sum_i b2_i u_i) (1 - 2 s); u in box "
                "units [-1, 1]; design episodes carry the public program mix; states from the given tick on"}

# ----------------------------------------------------------------------------- identification (digest)
if ident:
    cov = ident["coverage"]
    out["identification"] = {
        "names": ident["names"], "prior_sd_theta": ident["prior_sd_theta"],
        "contraction_by_level_and_budget": {k: v["contraction_mean"] for k, v in cov.items()},
        "abs_err_over_prior_sd": {k: v["abs_err_over_prior_sd_mean"] for k, v in cov.items()},
        "in90": {k: v["in90_frac"] for k, v in cov.items()}, "in50": {k: v["in50_frac"] for k, v in cov.items()},
        "emulator_cv_r2": {str(l): s_["emulator"].get("cv_r2_of_mean") for l, s_ in ident["state"].items()},
        "projection_r2": {str(l): s_["projection_r2"] for l, s_ in ident["state"].items()},
        "note": "contraction = posterior sd / prior sd per parameter (mean over truths); L1 = from level-1 summaries, "
                "L2 = from (N, s_b) only; in90 = share of (truth, parameter) pairs inside the central 90% interval"}


def clean(o):
    if isinstance(o, dict):
        return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    if isinstance(o, (np.floating, np.integer)):
        o = o.item()
    if isinstance(o, np.ndarray):
        return clean(o.tolist())
    if isinstance(o, float) and not np.isfinite(o):
        return None
    return o


TAG = os.environ.get("VX_TAG", "")                 # "" = job 2; "B" = the follow-up exam job -> analysis2_B.json
json.dump(clean(out), open(os.path.join(RES, f"analysis2{'_' + TAG if TAG else ''}.json"), "w"), indent=1, allow_nan=False)
st = out["status"]
print("status:", {k: st[k] for k in ("backend", "preset", "rate", "hours", "failed", "fatal", "prediction_final",
                                     "report_failures_in_progress_txt")})
print(f"ladder: L(K) {LK:.4f} L(O) {LO:.4f} skill K0 {ladder['skill_K0']} O_noinput {ladder['skill_O_noinput']}")
for fam, row in ladder["families"].items():
    print("  ", fam, {k: round(v["skill"], 3) for k, v in row.items() if "skill" in v},
          {k: {n: round(x["skill"], 3) for n, x in v.items()} for k, v in row.items() if "skill" not in v})
for k in ("net|P0 - net|C", "net|PM - net|C", "ridge|P0 - ridge|C", "law|P0 - law|C", "lin2|C - net|C", "law|C - net|C",
          "net|C - net|Cded", "K0 - K", "O_noinput - oracle"):
    if k in gaps:
        g_ = gaps[k]
        print(f"   gap {k}: {g_['in_skill_units']:+.3f} skill, z_truths {g_['z_truths']}, {g_['truths_with_sign_of_mean']}/{nT}")
for k, v in acc.items():
    if k.endswith("|K|joint") or k.endswith("|K0|joint"):
        print(f"   acceptance {k}: sigma {v['sigma']:.3f} (se {v['sigma_se_worlds']}) null {v['null_is']} rho {v['rho']}")
if "law_design" in out:
    ld = out["law_design"]
    print("law on the design:", ld["share_explained"], "b1 slope per eps", round(ld["b1_slope_per_unit_eps"], 3),
          "b1 rel change", {k: round(v, 2) for k, v in ld["b1_relative_change_across_box"].items()})
print("cchg s_b reached within truth:", {k: [round(x[1], 3) for x in v["value"]] for k, v in cchg["reached_within_truth"].items()
                                          if k.split("|")[-1] in ("C", "P0", "Cded") or k in ("K", "anchor")})
