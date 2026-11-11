"""make_summary -- study dialsA2: results/summary.json from the job's outputs (CPU, seconds; numpy only).

usage: python -B make_summary.py [--job results/job] [--job-id r6-dialsa2-001] [--out results/summary.json]
Every number carries its source (job id, file, key). The criteria are a2_stats.criteria (DECLARED.md Part 1, R17);
everything under "reported" is never a criterion.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import a2_stats as ST  # noqa: E402
from a_stats import Scores, ratio, stat  # noqa: E402

PILOT = "PILOT_NEVER_REUSE_AS_EXAM"
ap = argparse.ArgumentParser()
ap.add_argument("--job", default=os.path.join(HERE, "results", "job"))
ap.add_argument("--job-id", default="r6-dialsa2-001")
ap.add_argument("--out", default=os.path.join(HERE, "results", "summary.json"))
args = ap.parse_args()
J = args.job
SRC = f"{args.job_id}:"


def jl(name):
    p = os.path.join(J, name)
    return json.load(open(p)) if os.path.exists(p) else None


def load(name):
    z = np.load(os.path.join(J, name))
    d = {k: z[k] for k in z.files if k not in ("classes", "etas", "truths", "hs", "axes", PILOT)}
    return Scores(d, z["classes"], z["etas"]), z


def short(r):
    """A ratio or stat dict without the per-truth lists (they stay in the criteria block)."""
    keep = ("value", "mean", "se", "lower90", "upper90", "median_of_per_truth_ratios", "median_truths", "loo_min",
            "loo_max", "n_truths")
    return {k: (round(v, 5) if isinstance(v, float) else v) for k, v in r.items() if k in keep}


S, z = load("scores.npz")
e0, e4 = 0, len(S.etas) - 1
info, tr, ident = jl("info.json"), jl("train_info.json"), jl("identification.json")
status = jl("status.json")
crit = ST.criteria(S, 8, e0, e4)
src_sc = SRC + "scores.npz"

# ---- headline
h = {"verdict": crit["verdict"], "verdict_parts": crit["verdict_parts"], "source": src_sc + " via a2_stats.criteria",
     "T1_sigma_G": short(crit["T1"]["sigma_G"]), "T1_contrast": short(crit["T1"]["contrast"]),
     "T2_rho_G": short(crit["T2"]["rho_G"]), "T2_contrast": short(crit["T2"]["contrast"]),
     "T2_gap_P0_minus_C": short(crit["T2"]["gap_P0_minus_C"]), "T2_read": crit["T2"]["read"]}
if crit["T3"].get("recovery"):
    h["T3_H_recovery"] = short(crit["T3"]["recovery"])
    h["T3_G_minus_H"] = short(crit["T3"]["G_minus_H"])
    h["T3_t"] = crit["T3"]["t"]
if crit["T4"].get("blind_loss_share"):
    h["T4_blind_loss_share"] = short(crit["T4"]["blind_loss_share"])
h["T5"] = {k: v for k, v in crit["T5"].items() if not isinstance(v, dict) or "sigma_G_full" not in v}
for k in ("heaviest_left_out", "at_8_ticks", "at_16_ticks"):
    v = crit["T5"][k]
    h["T5"][k] = {"sigma_G": v["sigma_G"], "rho_G": v["rho_G"], "sigma_ok": v["sigma_ok"], "rho_ok": v["rho_ok"]}
h["zero_point"] = {k: (short(v) | {"holds": v.get("holds"), "in_rule": v.get("in_rule")} if isinstance(v, dict) else v)
                   for k, v in crit["zero_point"].items()}
h["picks"] = crit["picks"]

# ---- reported
rep = {"source": src_sc + " (a2_stats.recoveries, shares, skills)"}
pol8 = ["H@8", "H_mix@8", "S@8", "FT@8", "RES@8", "RESfix@8", "Dnet@8", "Dridge@8", "Cpub", "Ctrue", "CFT@8"]
rep["recovery_of_P0_to_C_eta4_N8"] = {k: short(v) for k, v in ST.recoveries(S, e4, 8, pol8).items()}
if S.has("FT@32"):
    pol32 = [p.replace("@8", "@32") for p in pol8]
    rep["recovery_of_P0_to_C_eta4_N32"] = {k: short(v) for k, v in ST.recoveries(S, e4, 32, pol32).items()}
    try:
        s32 = ST.shares(S, e4, 32)
        rep["shares_N32"] = {"sigma_G": short(s32["sigma_G"]), "rho_G": short(s32["rho_G"]), "G_share_picked": s32["G_share_picked"]}
    except Exception as exc:
        rep["shares_N32"] = f"not available: {exc!r}"
rep["by_class_eta4_N8"] = {}
for c, nm in (("c", "aimed"), ("d", "regional")):
    r = ST.shares(S, e4, 8, cls=(c,))
    rep["by_class_eta4_N8"][nm] = {"sigma_G": short(r["sigma_G"]), "rho_G": short(r["rho_G"]),
                                   "H_recovery": short(ST.recoveries(S, e4, 8, ["H@8"], cls=(c,))["H@8"])}
rep["by_horizon_eta4_N8"] = {}
for hi, hh in enumerate((8, 12, 16)):
    r = ST.shares(S, e4, 8, hsel=[hi])
    Lch = ST.picked(S, ST.C_names(8), e4, hsel=[hi])["L"]
    rep["by_horizon_eta4_N8"][str(hh)] = {"sigma_G": short(r["sigma_G"]), "rho_G": short(r["rho_G"]),
                                          "s_P0_to_C_share": short(ratio(S.L("P0", e4, hsel=[hi]) - Lch,
                                                                         S.L("K", e4, hsel=[hi]) - Lch)),
                                          "H_recovery": short(ST.recoveries(S, e4, 8, ["H@8"], hsel=[hi])["H@8"])}
Lc8 = ST.picked(S, ST.C_names(8), e4)["L"]
rep["s_P0_to_C_share_of_K_to_C_eta4"] = short(ratio(S.L("P0", e4) - Lc8, S.L("K", e4) - Lc8))
if S.has("H@8", "H_mix@8"):
    rep["H_mix_against_H_eta4_N8"] = {"L_Hmix_minus_L_H": short(stat(S.L("H_mix@8", e4) - S.L("H@8", e4))),
                                      "in_units_of_P0_to_C": short(ratio(S.L("H_mix@8", e4) - S.L("H@8", e4),
                                                                         S.L("P0", e4) - Lc8))}
    if S.has("H@32", "H_mix@32"):
        Lc32 = ST.picked(S, ST.C_names(32), e4)["L"]
        rep["H_mix_against_H_eta4_N32"] = {"in_units_of_P0_to_C": short(ratio(S.L("H_mix@32", e4) - S.L("H@32", e4),
                                                                              S.L("P0", e4) - Lc32))}
rep["skill_vs_oracle"] = {f"eta{S.etas[i]:g}": {k: round(v["skill_vs_O"], 4) for k, v in ST.skills(S, i).items() if "@r" not in k}
                          for i in range(len(S.etas))}
# base-net rungs (the training rule's curve)
rungs = sorted({int(k.split("@r")[1]) for k in S.d if "@r" in k})
rep["base_schedule_rungs"] = {}
for r in rungs:
    P0r, Ctr, Cpr = (f"P0@r{r}", f"Ctrue@r{r}", f"Cpub@r{r}")
    if not S.has(P0r, Ctr, Cpr):
        continue
    K4, K0 = S.L("K", e4), S.L("K", e0)
    rep["base_schedule_rungs"][str(r)] = {
        "s_trueform_net_alone_eta4": short(ratio(S.L(P0r, e4) - S.L(Ctr, e4), K4 - S.L(Ctr, e4))),
        "sigma_P0_vs_publicC_eta0": short(ratio(S.L(P0r, e0) - S.L(Cpr, e0), K0 - S.L(Cpr, e0))),
        "skill_vs_O_eta4": {n: round(float((K4.mean() - S.L(x, e4).mean()) / (K4.mean() - S.L("O", e4).mean())), 4)
                            for n, x in (("P0", P0r), ("Ctrue", Ctr), ("Cpub", Cpr))}}
# eta 1 and 2 arm
if os.path.exists(os.path.join(J, "scores_eta12.npz")):
    S12, z12 = load("scores_eta12.npz")
    rep["eta12_truths_0_3"] = {"source": SRC + "scores_eta12.npz", "truths": z12["truths"].tolist()}
    for i, e in enumerate(S12.etas):
        try:
            r = ST.shares(S12, i, 8)
            Lci = ST.picked(S12, ST.C_names(8), i)["L"]
            rep["eta12_truths_0_3"][f"eta{e:g}"] = {
                "sigma_G": short(r["sigma_G"]), "rho_G": short(r["rho_G"]),
                "s_P0_to_C": short(ratio(S12.L("P0", i) - Lci, S12.L("K", i) - Lci)),
                "recoveries": {k: short(v) for k, v in ST.recoveries(S12, i, 8, ["H@8", "H_mix@8", "S@8", "FT@8", "RES@8"]).items()}}
        except Exception as exc:
            rep["eta12_truths_0_3"][f"eta{e:g}"] = f"not available: {exc!r}"
# identification
if ident:
    rows = ident["rows"]
    idn = {}
    for row in rows:
        k = f"{row['kind']}|eta{row['eta']:g}|N{row['n_episodes']}"
        idn.setdefault(k, []).append(row)
    rep["identification"] = {"source": SRC + "identification.json [rows]", "emulators": ident.get("emulators")}
    for k, rs in idn.items():
        err = np.array([r["abs_err_over_prior_sd"] for r in rs])
        d = {"n_worlds": len(rs), "median_abs_err_over_prior_sd_per_param": np.round(np.median(err, 0), 3).tolist(),
             "mean_ess": float(np.mean([r["ess"] for r in rs]))}
        if rs[0].get("eta_post_mean") is not None:
            d["eta_post_mean_mean"] = float(np.mean([r["eta_post_mean"] for r in rs]))
            d["eta_post_mean_range"] = [float(np.min([r["eta_post_mean"] for r in rs])), float(np.max([r["eta_post_mean"] for r in rs]))]
            d["eta_post_sd_mean"] = float(np.mean([r["eta_post_sd"] for r in rs]))
        rep["identification"][k] = d
# study A's whole exam, quoted (DEVIATIONS entry 1)
try:
    A = json.load(open(os.path.join(os.path.dirname(HERE), "dialsA", "results", "summary.json")))
    ss = A["reported"]["science_share_eta4"]
    rep["study_A_whole_exam_quoted"] = {
        "source": "../dialsA/results/summary.json (job r6-dialsa-003, 8 truths, all four classes, horizons 1-16) "
                  "[reported.science_share_eta4], [reported.g_per_horizon_eta4], [headline]",
        "sigma_against_P0|all": short(ss["sigma_against_P0|all"]),
        "sigma_against_G@8|all": short(ss["sigma_against_G@8|all"]),
        "sigma_against_P0|aimed_regional": short(ss["sigma_against_P0|aimed_regional"]),
        "sigma_against_G@8|aimed_regional": short(ss["sigma_against_G@8|aimed_regional"]),
        "g_per_horizon_eta4": A["reported"].get("g_per_horizon_eta4")}
except Exception as exc:
    rep["study_A_whole_exam_quoted"] = f"not available: {exc!r}"

# ---- training
trn = {"source": SRC + "train_info.json"}
if tr:
    trn["base"] = [{"steps": b["steps"], "best_step": b["best_step"], "rule_met": b["rule_met"],
                    "best_val": b["best_val"], "ms_per_step": b.get("ms_per_step"), "stopped_early": b["stopped_early"],
                    "net_order": b["net_order"],
                    "curve_step": [hh["step"] for hh in b["hist"]], "curve_val": [hh["val"] for hh in b["hist"]]}
                   for b in tr["base"]]
    trn["base_rule_met_at_scored_rung"] = bool(tr["base"][-1]["rule_met"]) if tr["base"] else None
    trn["ft"] = {k: [{"steps": v["steps"], "rates": v["rates"], "interior": v["interior"],
                      "groups": {g: {kk: r[kk] for kk in ("best_steps", "best_rate", "widen", "interior",
                                                           "share_nets_pick_at_edge", "share_nets_zero_steps", "mean_curves")}
                                 for g, r in v["rule"].items()},
                      "ms_per_lockstep_step": v["timing"]["ms_per_lockstep_step_median"]} for v in vs]
                 for k, vs in tr["ft"].items()}
    trn["D"] = {k: [{"steps": v["steps"], "rule_met": v["rule_met"], "best_step_hist_per_eval": v["best_step_hist"]}
                    for v in vs] for k, vs in tr["D"].items()}
    lam = tr.get("res_cv_ridge", {})
    trn["res_cv_ridge_counts"] = {b: {c: dict(zip(*np.unique([v.get(c) for v in d.values() if c in v], return_counts=True)))
                                      for c in ("c", "d")} for b, d in lam.items()}
    trn["res_cv_ridge_counts"] = json.loads(json.dumps(trn["res_cv_ridge_counts"], default=lambda o: o.item() if hasattr(o, "item") else str(o)))

# ---- what ran
ran = {"source": SRC + "info.json"}
if info:
    ran.update({k: info.get(k) for k in ("backend", "devices", "versions", "x64", "max_hours", "secret_commitment",
                                         "truths", "truths_rule", "law", "designed_arms", "base_final_steps",
                                         "base_rule_met", "member_ticks_planned", "hours", "failed", "skipped", "notes",
                                         "stage_done", "family_check")})
    ran["config"] = info.get("config")
    ran["stage_seconds"] = {k: round(v, 1) for k, v in (info.get("times") or {}).items() if isinstance(v, (int, float))}
    ran["family_rates"] = (info.get("times") or {}).get("family_rates")
job = {"id": args.job_id, "outputs": os.path.relpath(J, HERE)}
if status:
    job["status"] = {k: status.get(k) for k in ("state", "message", "cap_usd", "cost", "billing_window_hours",
                                                "started_at", "finished_at", "exit_code", "review")}
    job["status"]["pod"] = status.get("pod")
    job["status"]["ref"] = (status.get("bundle") or {}).get("ref")
    pods = status.get("pods") or []
    if pods:
        job["pod_hours"] = round(sum((np.datetime64(p["terminated_at"][:19]) - np.datetime64(p["created_at"][:19])).astype(float)
                                     for p in pods if p.get("terminated_at") and p.get("created_at")) / 3600.0, 3)

out = {"study": "round6/dials/dialsA2: the gliders stress-conversion exam reopened with a triggered bar", PILOT: True,
       "declared": "DECLARED.md (commit 3fd4076c5, 19:26 UTC, before any code or request)", "job": job,
       "what_ran": ran, "headline": h, "criteria": crit, "reported": rep, "training": trn}


def conv(o):
    if isinstance(o, (np.floating, np.integer)):
        return o.item()
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, np.bool_):
        return bool(o)
    return str(o)


os.makedirs(os.path.dirname(args.out), exist_ok=True)
with open(args.out, "w") as f:
    json.dump(out, f, indent=1, default=conv)
print(json.dumps({"verdict": crit["verdict"], "parts": crit["verdict_parts"],
                  "sigma_G": crit["T1"]["sigma_G"]["value"], "rho_G": crit["T2"]["rho_G"]["value"],
                  "H_recovery": crit["T3"].get("recovery", {}).get("value"), "H_t": crit["T3"].get("t")}, default=conv))
