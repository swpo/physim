"""make_summary -- results/summary.json from the outputs of GPU job r4-sbi-002 (copied to results/job/).

Every number carries its source (job id, file, key). Recomputes the headline tables from the saved
outputs: identification per budget (contraction, error, coverage) and prediction (pooled oracle-
normalised fair energy skill per predictor, paired gaps per budget, truth-level gaps).
usage: python -B make_summary.py [job_dir] [status.json] [job_id]
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
JOB = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "results", "job")
STATUS = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "results", "status.json")
JOB_ID = sys.argv[3] if len(sys.argv) > 3 else "r4-sbi-002"
OUTF = sys.argv[4] if len(sys.argv) > 4 else os.path.join(HERE, "results", "summary.json")


def src(f, key=""):
    return f"{JOB_ID}:out/{f}" + (f" [{key}]" if key else "")


def r3(x):
    return None if x is None else (round(float(x), 4) if np.ndim(x) == 0 else [round(float(v), 4) for v in x])


info = json.load(open(os.path.join(JOB, "info.json")))
truths = json.load(open(os.path.join(JOB, "truths.json")))
ident = json.load(open(os.path.join(JOB, "identification.json")))
lab = json.load(open(os.path.join(JOB, "lab.json")))
pred = json.load(open(os.path.join(JOB, "prediction.json")))
vprior = json.load(open(os.path.join(JOB, "viability_prior.json")))
status = json.load(open(STATUS)) if os.path.exists(STATUS) else {}
budgets = info["config"]["budgets"]
P, H = info["config"]["P"], info["config"]["H"]

S = {"what": "round 4 study sbi (track 2): simulate-to-train on the gliders wind world with 4 hidden parameters "
             "(lR, dm_00, ls_00, lh): synthetic-likelihood identification from budgeted Lab data, then level-1 "
             "predictors trained on real data vs simulations",
     "PILOT_NEVER_REUSE_AS_EXAM": True,
     "job": {"id": JOB_ID, "platform": info.get("devices"), "backend": info.get("backend"),
             "versions": info.get("versions"), "hours_in_script": r3(info.get("hours")),
             "member_ticks": info.get("member_ticks"), "member_ticks_total": info.get("member_ticks_total"),
             "failed_or_skipped": info.get("failed"), "source": src("info.json")},
     "config": {**info["config"], "source": src("info.json", "config")},
     "net_config": info.get("net"),
     "truths": {"theta": truths["truths"], "names": truths["names"], "n_viable_of_candidates":
                [truths["n_viable"], len(truths["candidates"])], "secret_commitment": truths["secret_commitment"],
                "source": src("truths.json")},
     "viability_prior": {**vprior["diag"], "source": src("viability_prior.json", "diag")}}
if status:
    pods = status.get("pods", [])
    S["job"]["status"] = {"state": status.get("state"), "exit_code": status.get("exit_code"),
                          "cost": status.get("cost"), "pod": status.get("pod"),
                          "started_at": status.get("started_at"), "finished_at": status.get("finished_at"),
                          "pods": [{k: p.get(k) for k in ("gpu", "provider", "data_center", "rate_usd_hr", "requested_at",
                                                          "ready_at", "terminated_at", "billed_usd")} for p in pods],
                          "source": f"{JOB_ID}:status.json"}
    if status.get("cost", {}).get("billed_usd") and status.get("pod", {}).get("rate_usd_hr"):
        S["job"]["status"]["gpu_hours_billed_equiv"] = round(status["cost"]["billed_usd"] / status["pod"]["rate_usd_hr"], 3)

# identification
idt = {"method": ident["method"], "emulator": ident["emulator"], "projection_r2": ident["projection"]["r2_per_param"],
       "prior_sd_theta": ident["prior_sd_theta"], "per_budget": {}, "source": src("identification.json")}
for n in budgets:
    rr = [r for r in ident["per_truth_budget"] if r["n_episodes"] == n]
    c = ident["coverage"][str(n)]
    nats = [l["per_budget"][str(n)]["nats"] for l in lab]
    idt["per_budget"][str(n)] = {
        "episodes": n, "ticks": n * (1 + P + H), "nats_mean_over_truths": r3(np.mean(nats)),
        "contraction_sd_ratio_mean": r3(c["contraction_mean"]),
        "contraction_sd_ratio_median": r3(np.median([r["contraction_sd_ratio"] for r in rr], 0)),
        "abs_err_over_prior_sd_mean": r3(c["abs_err_over_prior_sd_mean"]),
        "in50_frac": c["in50_frac"], "in90_frac": c["in90_frac"], "n_marginal_checks": 4 * len(rr),
        "hpd_le_50_frac": c["hpd_le_50_frac"], "hpd_le_90_frac": c["hpd_le_90_frac"],
        "hpd_levels": r3([r["hpd_level"] for r in rr]), "ess_min": r3(min(r["ess"] for r in rr)),
        "source": src("identification.json", f"coverage.{n}, per_truth_budget[n_episodes={n}]; lab.json per_budget")}
S["identification"] = idt

# prediction
rep = pred["report"]
agg, se = rep["aggregate"], rep["se"]
names = sorted(agg)
S["prediction"] = {"n_items_pooled": pred["n_items_pooled"], "cells": pred["cells"], "valid_cells": rep["valid"],
                   "oes": {k: {"mean": r3(agg[k]), "se": r3(se[k]), "pooled_ratio": r3(rep["aggregate_pooled"][k])}
                           for k in names},
                   "oes_per_cell": {k: r3(rep["oes"][k]) for k in names},
                   "by_program_class": {g: {k: r3(v) for k, v in d.items()} for g, d in rep.get("by_group", {}).items()},
                   "per_truth_aggregate": pred["per_truth_aggregate"],
                   "gaps": {k: {kk: r3(vv) if isinstance(vv, (int, float)) else vv for kk, vv in v.items()}
                            for k, v in pred["gaps"].items()},
                   "source": src("prediction.json")}
# the headline table: per budget and class, OES of real, post, and the references
tab = {}
for cl in ("ridge", "net", "amort"):
    t = {}
    for k in ("true", "prior_mean", "prior_pred"):
        if f"{cl}|{k}" in agg:
            t[k] = r3(agg[f"{cl}|{k}"])
    for n in budgets:
        row = {}
        for k in ("real", "post"):
            if f"{cl}|{k}@{n}" in agg:
                row[k] = r3(agg[f"{cl}|{k}@{n}"])
        g = pred["gaps"].get(f"{cl}|post@{n} - {cl}|real@{n}")
        if g:
            row["post_minus_real"] = {"gap": r3(g["gap"]), "se_items": r3(g["se"]), "z": r3(g["z"]),
                                      "truth_mean": r3(g.get("truth_mean")), "truth_se": r3(g.get("truth_se"))}
        g = pred["gaps"].get(f"{cl}|true - {cl}|post@{n}")
        if g:
            row["true_minus_post"] = {"gap": r3(g["gap"]), "se_items": r3(g["se"]), "z": r3(g["z"])}
        if row:
            t[f"n{n}"] = row
    if t:
        tab[cl] = t
S["prediction"]["table"] = tab
S["prediction"]["table_source"] = src("prediction.json", "report.aggregate, gaps")
# offline calibration of the synthetic likelihood (CPU, from the job's design summaries)
OC = os.path.join(os.path.dirname(OUTF), "offline_calib.json")
if os.path.exists(OC):
    oc = json.load(open(OC))
    S["identification"]["offline_calibration"] = {
        "what": "held-out design points (uniform on the box), projection + emulator refit on the other 80%, "
                "posterior from the point's own first n episodes under a flat box prior",
        "N_test_theta": oc["N_test_theta"], "N_train_theta": oc["N_train_theta"],
        "per_n": {n: {k: r3(v) for k, v in d.items()} for n, d in oc["per_n"].items()},
        "platform": "CPU (this container), deterministic from r4-sbi-002 design_features.npz",
        "source": "results/offline_calib.json (offline_calib.py)"}


# headline claims, each with its source key
def gap(k):
    g = pred["gaps"][k]
    return {"gap": r3(g["gap"]), "se_items": r3(g["se"]), "z": r3(g["z"]),
            "truth_mean": r3(g.get("truth_mean")), "truth_se": r3(g.get("truth_se")),
            "source": src("prediction.json", f"gaps['{k}']")}


# extra paired gaps recomputed from scores.npz with the job's own report settings (vw.scoring.skill_report,
# seed 0, 2000 paired bootstrap draws over the 512 pooled items); the job's aggregates are reproduced first
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "vw1"))
from vw.scoring import paired_gap, skill_report  # noqa: E402

z = np.load(os.path.join(JOB, "scores.npz"))
tr = [int(t) for t in pred["truths_scored"]]
cols = np.asarray(rep["valid"], bool)
nm = sorted({k.split("|", 1)[1] for k in z.files if k.startswith("t0|")} - {"classes"})
SS = {k: np.concatenate([z[f"t{i}|{k}"] for i in tr]) for k in nm}
cols_ok = ~np.isnan(SS["oracle"]).any(0)
SS = {k: v[:, cols_ok] for k, v in SS.items()}
rr = skill_report(SS, groups=np.concatenate([z[f"t{i}|classes"] for i in tr]), n_boot=2000)
repro = max(abs(rr["aggregate"][k] - agg[k]) for k in agg)
extra = {}
for a, b in (("net|true", "net|prior_pred"), ("ridge|true", "ridge|prior_pred"), ("amort|true", "net|true"),
             ("amort|prior_pred", "net|prior_pred"), ("amort|true", "amort|prior_pred"),
             ("amort|true", "amort|prior_mean"), ("net|post@2", "net|real@512")):
    g = paired_gap(rr, a, b)
    extra[f"{a} - {b}"] = {"gap": r3(g["gap"]), "se_items": r3(g["se"]), "z": r3(g["z"]),
                           "source": "recomputed from r4-sbi-002:out/scores.npz (make_summary.py)"}
S["prediction"]["extra_gaps"] = extra
S["prediction"]["recompute_max_abs_diff_vs_job_aggregate"] = float(repro)

H = {}
for cl in ("net", "ridge"):
    H[cl] = {"true_minus_prior_pred": extra[f"{cl}|true - {cl}|prior_pred"],
             "true_minus_prior_mean": gap(f"{cl}|true - {cl}|prior_mean"),
             "prior_pred_minus_prior_mean": gap(f"{cl}|prior_pred - {cl}|prior_mean")}
    for n in budgets:
        H[cl][f"n{n}"] = {"post_minus_real": gap(f"{cl}|post@{n} - {cl}|real@{n}"),
                          "true_minus_post": gap(f"{cl}|true - {cl}|post@{n}"),
                          "post_minus_prior_pred": gap(f"{cl}|post@{n} - {cl}|prior_pred"),
                          "real_minus_prior_pred": gap(f"{cl}|real@{n} - {cl}|prior_pred")}
for n in budgets:
    H.setdefault("amort_vs_net", {})[f"n{n}"] = gap(f"amort|post@{n} - net|post@{n}")
S["prediction"]["headline_gaps"] = H
S["study_cost"] = {"jobs": {"r4-sbi-001": {"state": "infra_error (provider out of stock)", "billed_usd": 0.0,
                                           "source": "r4-sbi-001:status.json [cost.billed_usd]"},
                            JOB_ID: {"state": status.get("state"), "billed_usd": status.get("cost", {}).get("billed_usd"),
                                     "source": f"{JOB_ID}:status.json [cost.billed_usd]"}},
                   "cap_usd_study": 25.0}
S["study_cost"]["total_billed_usd"] = round(sum(j["billed_usd"] or 0 for j in S["study_cost"]["jobs"].values()), 3)
S["conclusions"] = [
    "Identification: Gaussian synthetic likelihood on 4 regression summaries contracts all 4 parameters "
    "already at 2 episodes (66 ticks; posterior sd / prior sd 0.17-0.44) and to 0.06-0.12 at 512 episodes; "
    "contraction flattens beyond about 128 episodes (emulator misfit floor). Marginal coverage is close to "
    "nominal on 8 truths (in90 0.875-1.0) and on 300 held-out design points at n <= 4 (in50 0.50-0.52, in90 "
    "0.89-0.90); the joint 90% HPD covers 6/8 truths at n = 128 and 512 (slightly overconfident, n too small "
    "to decide). See identification.per_budget, identification.offline_calibration.",
    "Prediction: the net trained on 1,024 simulated episodes at posterior draws matches the net trained at "
    "the true parameters at every budget (true - post within +-0.003 OES, |z| <= 1.03), even at 2 episodes. "
    "The same net on the real Lab data needs 512 episodes to come within 0.019 OES (z 5.8) and is far worse "
    "below (gap post - real 1.04 / 0.52 / 0.22 / 0.10 / 0.019 at 2 / 8 / 32 / 128 / 512 episodes). "
    "See prediction.table, prediction.headline_gaps.",
    "Most of the gain is knowing the simulator, not identifying theta: a net trained on prior-predictive "
    "simulations (no real data) scores 0.544, equal to real@512 (gap +0.002, z 0.4); identification adds "
    "0.021 OES on top (net true - prior_pred, z 5.7; ridge 0.042, z 7.7); the box-centre plug-in loses 0.091 "
    "(net) against the truth. See prediction.extra_gaps, prediction.headline_gaps.",
]
json.dump(S, open(OUTF, "w"), indent=1, default=float)
print(json.dumps({"identification": {n: {k: v for k, v in d.items() if k in ("contraction_sd_ratio_mean", "in50_frac",
                                                                                "in90_frac", "hpd_le_90_frac")}
                                     for n, d in idt["per_budget"].items()}, "table": tab}, indent=1, default=float))
