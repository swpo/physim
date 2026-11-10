"""make_summary -- results/summary.json for round 5 study vortexexam: every number with its source.

    python -B make_summary.py        (reads results/analysis1.json, results/job1/*, results/job2/*, prior.json)

results/job1 and results/job2 hold the files copied from origin/gpu-jobs:jobs/<job_id>/ (status.json and the small
JSON outputs; the arrays stay on the gpu-jobs branch).
"""
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.environ.get("VX_RES", os.path.join(HERE, "results"))
J1, J2 = "r5-vortexexam-002", os.environ.get("VX_JOB2", "r5-vortexexam-003")
JD2 = os.environ.get("VX_JOB2_DIR", "job2")          # folder under results/ with job 2's small files
J3 = os.environ.get("VX_JOB3", "r5-vortexexam-006")       # the follow-up exam job, pilot B (results/job3)


def load(*p):
    f = os.path.join(RES, *p)
    return json.load(open(f)) if os.path.exists(f) else None


def V(value, source, note=None):
    d = {"value": value, "source": source}
    if note:
        d["note"] = note
    return d


def r(x, n=3):
    if isinstance(x, (list, tuple)):
        return [r(v, n) for v in x]
    if isinstance(x, dict):
        return {k: r(v, n) for k, v in x.items()}
    if isinstance(x, float):
        return round(x, n)
    return x


def job_cost(st):
    if st is None:
        return None
    pods = st.get("pods") or []
    from datetime import datetime
    hrs = 0.0
    for p in pods:                                   # GPU-hours = pod lifetime (created to terminated), summed
        if p.get("created_at") and p.get("terminated_at"):
            t0, t1 = (datetime.strptime(p[k], "%Y-%m-%dT%H:%M:%SZ") for k in ("created_at", "terminated_at"))
            hrs += (t1 - t0).total_seconds() / 3600
    hrs = round(hrs, 3) if hrs else None
    run_h = None
    if st.get("started_at") and st.get("finished_at"):
        run_h = round((datetime.strptime(st["finished_at"], "%Y-%m-%dT%H:%M:%SZ")
                       - datetime.strptime(st["started_at"], "%Y-%m-%dT%H:%M:%SZ")).total_seconds() / 3600, 3)
    return {"state": st.get("state"), "billed_usd": (st.get("cost") or {}).get("billed_usd"),
            "conservative_usd": (st.get("cost") or {}).get("conservative_usd"), "pod_hours": hrs,
            "run_hours_started_to_finished": run_h, "exit_code": st.get("exit_code"),
            "gpu": [p.get("gpu") for p in pods], "provider": [p.get("provider") for p in pods],
            "rate_usd_hr": [p.get("rate_usd_hr") for p in pods], "cap_usd": st.get("cap_usd"),
            "pods": [{k: p.get(k) for k in ("created_at", "ready_at", "terminated_at", "billed_usd", "state")} for p in pods]}


S = {"study": "round 5, vortexexam (track 2): exam pilot on the fed-vortex world", "date": "2026-11-09/10",
     "PILOT_NEVER_REUSE_AS_EXAM": True}
A1 = load("analysis1.json")
st1, st2, st3 = load("job1", "status.json"), load(JD2, "status.json"), load("job3", "status.json")
old = [load("job_r5-vortexexam-001_status.json")]
S["gpu"] = V({J1: job_cost(st1), J2: job_cost(st2), **({J3: job_cost(st3)} if st3 else {}),
              "billed_usd_total": round(sum(((x or {}).get("cost") or {}).get("billed_usd") or 0.0
                                            for x in (st1, st2, st3, load("job_r5-vortexexam-005_status.json"))), 4),
              "conservative_usd_total": round(sum(((x or {}).get("cost") or {}).get("conservative_usd") or 0.0
                                                  for x in (st1, st2, st3, load("job_r5-vortexexam-005_status.json"))), 4),
              "pod_hours_total": round(sum((job_cost(x) or {}).get("pod_hours") or 0.0 for x in (st1, st2, st3)), 3),
              "r5-vortexexam-004": {"state": "rejected", "billed_usd": 0.0,
                                    "why": "invalid request: purpose line over 300 characters; resubmitted as r5-vortexexam-005"},
              "r5-vortexexam-005": dict(job_cost(load("job_r5-vortexexam-005_status.json")) or {},
                                        why="infra_error at provisioning: cap $19.40 was 0.1 cent under $6.69/h x (2.65 + 0.25) h; "
                                            "no job time; resubmitted as r5-vortexexam-006 with cap $19.60"),
              "cap_usd_study": 25.0,
              "r5-vortexexam-001": {"state": (old[0] or {}).get("state"), "billed_usd": ((old[0] or {}).get("cost") or {}).get("billed_usd")}},
             f"origin/gpu-jobs:jobs/<job>/status.json (copied to results/job1, results/job2)")

if A1:
    src = f"results/analysis1.json (analyse1.py on origin/gpu-jobs:jobs/{J1}/out)"
    S["platform_job1"] = V(A1["info"], src + " info")
    S["throughput"] = V(r(A1["bench"], 4), src + " bench (job out bench.json)",
                        "member-ticks per second, float64 world with the vortex tracker, jax.vmap batch B; "
                        "one tick = 250 native steps = 5 time units")
    for tag in ("law", "law128"):
        if A1.get(tag):
            L = A1[tag]
            S[tag] = V({"H": L["H"], "J_per_eps": L["J"], "T_ticks": L["T"], "eps": L["eps"],
                        "member_ticks_per_s": r(L["member_ticks_per_s"], 1),
                        **{var: {"b1_per_eps": r([q["b1"] for q in v["per_eps"]], 4),
                                 "b1_se": r([q["b1_se"] for q in v["per_eps"]], 4),
                                 "b2_per_eps": r([q["b2"] for q in v["per_eps"]], 4),
                                 "b1_line": r(v["b1_line"], 4),
                                 "b1_proportional": r(v.get("b1_proportional"), 4),
                                 "b1_line_eps_positive": r(v.get("b1_line_eps_positive"), 4),
                                 "share_of_change_variance_explained_by_law": r([q["explained_by_law"] for q in v["per_eps"]]),
                                 "by_binned_drift": r([q["explained_by_binned_drift"] for q in v["per_eps"]]),
                                 "shape_r2": r([q["shape_r2"] for q in v["per_eps"]]),
                                 "mean_by_tick": [r(q["mean_by_tick"]) for q in v["per_eps"]],
                                 "first_tick_mean_above_half": [q["first_tick_mean_above_half"] for q in v["per_eps"]],
                                 "integrated_law_max_abs_error_of_mean": r([q["integrated"]["max_abs_error"] for q in v["per_eps"]]),
                                 "integrated_law_out_of_sample": {
                                     "max_abs_error": r([q["integrated"]["out_of_sample"]["max_abs_error"] for q in v["per_eps"]]),
                                     "max_abs_z": r([q["integrated"]["out_of_sample"]["max_abs_z"] for q in v["per_eps"]], 1),
                                     "se_of_actual_mean": r([q["integrated"]["out_of_sample"]["mean_se_of_actual"] for q in v["per_eps"]])}}
                           for var, v in L["vars"].items()},
                        "N_mean_by_eps": r(L["N_mean_ticks_100_on_by_eps"], 2)},
                       src + f" {tag} (job out {tag}.npz)",
                       "x(t+16) - x(t) = b1 x(1-x) + b2 (1-2x) + e per eps, pooled over members and ticks >= 64; "
                       "b1_line: weighted straight line b1 = c0 + c1 eps over the eps values; b1_proportional: b1 = c eps; "
                       "b1_line_eps_positive: the line fitted without eps = 0 (chi2 against the member-bootstrap SEs); "
                       "integrated_law: every member's share at tick 100 iterated with the fitted map every 16 ticks to tick "
                       "436 (1,680 time units), error of the ensemble mean; out_of_sample: constants fitted on the first half "
                       "of the members, applied to the second half (z against the SE of that half's mean)")
    SCAN_SRC = {"scan": f"job {J1}: scan_main.npz" , "scan2": f"the --scan-only rerun ({os.environ.get('VX_SCAN2', J2 + ' out/scan')})"}
    for key in ("scan", "scan2"):
        if key not in A1:
            continue
        sc = A1[key]
        br = sc.get("branch", {})
        noisy = sc["J"] * max(len(br.get("anchors_done") or []), 1) < 12
        S[key] = V({"H": sc["H"], "J": sc["J"], "T": sc["T"], "anchors": br.get("anchors_done"),
                    "R": sc["R"], "Mc": sc["Mc"], "box": sc["box"], "has_branches": bool(br),
                    "states_per_setting": sc["J"] * len(br.get("anchors_done") or []),
                    "null_floor": r(sc.get("null_floor")),
                    "table": r(sc.get("table")),
                    "null_D_h_level2": r(br.get("null_D_h_level2"), 4),
                    "null_D_h_level1_raster": r(br.get("null_D_h_level1_raster"), 4),
                    "paired_shift_z_main_runs": {p: {st: r(sc["shift"][f"{p}@{e}"][st]["z_paired"], 1)
                                                     for e in ("lo", "hi") for st in ("N", "s_b_late")
                                                     if f"{p}@{e}" in sc["shift"]} | {
                                                         "max_abs_z": r(max(abs(v["z_paired"]) for e in ("lo", "hi")
                                                                            for v in sc["shift"].get(f"{p}@{e}", {}).values()), 1)}
                                                 for p in sc["box"] if f"{p}@lo" in sc["shift"]} if sc["J"] > 1 else None,
                    "viability": {k: [v["viable_members"], v["of"], r(v["N_mean"], 1), v["N_min"], v["N_max"]]
                                  for k, v in sc["viability"].items()}},
                   f"results/analysis1.json {key} (analyse1.py on {SCAN_SRC[key]}, {sc.get('branch_file') or 'no branch file'})",
                   "headroom = theta-plug-in deficit / D_h of the null setting; L2 = mean over h 8, 16, 32 ticks of "
                   "level 2 (N, s_b); L1 = mean over h 1, 2, 4, 8 of the block raster of the vortex list; L2_se, L1_se = "
                   "SE over the (member, anchor) states of the setting; viability entries: [viable members, of, mean N, "
                   "min N, max N]; paired_shift_z_main_runs: paired z of trajectory statistics against the null setting "
                   "(z of N at ticks 100 on and of s_b at ticks 250 on, lo and hi edge; max |z| over 9 statistics)"
                   + ("; NOISY: under 12 states per setting (this rerun shrank to its smallest design: the Mac's review "
                      "of r5-vortexexam-003), level-1 climatology from J - 1 other members" if noisy and br else ""))
PR = json.load(open(os.path.join(HERE, "prior.json"))) if os.path.exists(os.path.join(HERE, "prior.json")) else None
if PR:
    S["prior"] = V({k: PR[k] for k in ("H", "names", "lo", "hi", "T_ep", "prog_ticks", "c_prog", "hs", "viability", "const",
                                       "selection", "mutation")}, "prior.json (select_prior.py)")

PRB = json.load(open(os.path.join(HERE, "prior_B.json"))) if os.path.exists(os.path.join(HERE, "prior_B.json")) else None
if PRB:
    S["prior_B_rule_on_branch_headroom"] = V(
        {k: PRB[k] for k in ("names", "lo", "hi", "selection")}, "prior_B.json (select_prior.py --out prior_B.json)",
        "the declared rule applied to the level-2 plug-in deficits of job 1's branches (available only after job 2 was "
        "requested): eps plus the two families with the largest min-edge headroom; everything else as prior.json")

def exam_sections(tag, jdir, jid, afile):
    """The sections of one exam job: tag "" = job 2 (prior.json), "_B" = the follow-up (prior_B.json)."""
    S = {}
    P = load(jdir, "prediction.json")
    if P:
        src2 = f"origin/gpu-jobs:jobs/{jid}/out/"
        info, ident, truths, lab, vp = (load(jdir, f) for f in ("info.json", "identification.json", "truths.json", "lab.json",
                                                                  "viability_prior.json"))
        S["platform_job"] = V({k: info.get(k) for k in ("backend", "devices", "versions", "rate", "bmax", "preset", "config",
                                                         "member_ticks", "member_ticks_total", "hours", "failed",
                                                         "secret_commitment")}, src2 + "info.json")
        S["truths"] = V({"names": truths["names"], "truths": r(truths["truths"], 4), "n_candidates": len(truths["candidates"]),
                         "n_viable": truths["n_viable"], "PILOT_NEVER_REUSE_AS_EXAM": True}, src2 + "truths.json",
                        "pilot truths are public by design; never to be reused as an exam")
        S["viability_prior"] = V(r(vp), src2 + "viability_prior.json")
        S["lab"] = V({"per_budget_truth0": lab[0]["per_budget"], "caps": lab[0]["caps"],
                      "nats_at_largest_budget_by_truth": [r(x["usage_final"]["total_nats"], 1) for x in lab]}, src2 + "lab.json")
        if ident:
            S["identification"] = V({"names": ident["names"], "prior_sd_theta": r(ident["prior_sd_theta"], 4),
                                     "state": r(ident["state"]), "coverage": r(ident["coverage"])},
                                    src2 + "identification.json",
                                    "L1 = summaries of level-1 histories, L2 = of (N, s_b) only; contraction = posterior sd / "
                                    "prior sd per parameter, mean over truths; in90 = share of (truth, parameter) pairs inside "
                                    "the central 90% interval")
        names = sorted(P["oes"])
        fams = ("net", "ridge", "law", "lin2")
        S["scores"] = V({"n_truths": P["n_truths"], "n_items": P["n_items_pooled"], "primary_cells": P["primary_cells"],
                         "items_by_program_class": P.get("items_by_program_class"),
                         "L_pooled": r(P["L_pooled"], 4), "oes": r(P["oes"]), "oes_se_items": r(P["oes_se_items"]),
                         "oes_per_cell": {k: r(P["oes_per_cell"][k]) for k in names if k.split("|")[-1] in
                                          ("P0", "C", "PM", "Cded", "K", "K0", "O_noinput") or k in ("oracle",)},
                         "cells": P["cells"]},
                        src2 + "prediction.json (L_pooled, oes, oes_se_items, oes_per_cell)",
                        "L = mean fair energy score (vw.scoring.energy_fair) over items and the primary cells (level 2 = (N, s_b) "
                        "jointly, scaled, at h = 8, 16, 32 ticks); OES = (L(K) - L) / (L(K) - L(O)), equal-weight mean over the "
                        "primary cells (vw.scoring.skill_report); K = the truth's other main runs at the same tick, K0 = design "
                        "episodes at the same tick (prior climatology), O_noinput = replicates from the hidden state without "
                        "the test program")
        acc = P["acceptance"]

        def short(a):
            return None if a is None else {
                "sigma": r(a["sigma"]), "sigma_se_worlds": r((a.get("sigma_worlds") or {}).get("se")),
                "sigma_p05_p95_worlds": r([(a.get("sigma_worlds") or {}).get(q) for q in ("p05", "p95")]),
                "null_is": a["null_is"], "rho": r(a.get("rho")), "rho_se_worlds": r((a.get("rho_worlds") or {}).get("se")),
                "rho_p05_p95_worlds": r([(a.get("rho_worlds") or {}).get(q) for q in ("p05", "p95")]),
                "pass_sigma": a["pass_sigma"], "pass_rho": a.get("pass_rho"), "n_worlds": a.get("n_worlds")}
        S["acceptance"] = V({k: short(v) for k, v in acc.items()}, src2 + "prediction.json acceptance",
                            "computed by round5/agentenv/evaluator/acceptance.py (shares): sigma = (L(null) - L(C)) / (L(K) - "
                            "L(C)), null = the better of D@n and P0; rho = (L(P0) - L(S@n)) / (L(P0) - L(C)); one predictor "
                            "family per row 'family@n'; '|S2' = posterior from level-2 histories only; '|ded' = dedicated "
                            "models (C = Cded, S = Sded); SE and 5-95% range from the bootstrap clustered by truth; bars "
                            "sigma >= 0.15 and rho <= 0.7")
        S["acceptance_per_world"] = V({k: r(v.get("per_world")) for k, v in acc.items() if "|" not in k},
                                      src2 + "prediction.json acceptance[*].per_world")
        S["gaps"] = V({k: r(v) for k, v in P["gaps_oes_item_bootstrap"].items()}, src2 + "prediction.json gaps_oes_item_bootstrap",
                      "OES gaps with a paired bootstrap over items (not clustered by truth)")
        cc = P["cchg"]
        keep = [k for k in cc["reached"] if k in ("K", "K0", "anchor", "O_noinput") or k.split("|")[-1] in ("P0", "C", "PM", "Cded")
                or k.endswith("@16") or k.endswith("@4")]
        S["cchg"] = V({"hs_ticks": cc["hs"], "coords": cc["coords"],
                       "pooled": {"oracle_predictable_share": r(cc["oracle_predictable_share"]), "V_change": r(cc["V_change"], 5),
                                  "Vu": r(cc["Vu"], 5), "reached": {k: r(cc["reached"][k]) for k in keep}},
                       "within_truth": {"oracle_predictable_share": r(cc["within_truth"]["oracle_predictable_share"]),
                                        "oracle_predictable_share_per_truth": r(cc["within_truth"]["oracle_predictable_share_per_truth"]),
                                        "reached": {k: r(cc["within_truth"]["reached"][k]) for k in keep}}},
                      src2 + "prediction.json cchg",
                      "share of the oracle-predictable change reached, (V_change - Ve) / (V_change - Vu), per horizon (rows) "
                      "and coordinate (N, s_b): V_change = variance of y(a + h) - y(a) about its mean, Vu = within-item "
                      "replicate variance, Ve = mean squared error of the predictive mean (64 samples); 'pooled' over all "
                      "items as in round 3 (track1/vortex128), 'within_truth' about each truth's own mean change, summed over truths")
        if P.get("oes_by_program_class"):
            bg = P["oes_by_program_class"]
            cols = [k for k in ("K0", "O_noinput", "net|P0", "net|C", "net|Cded", "ridge|P0", "ridge|C", "law|C", "lin2|C") if k in P["oes"]]
            S["by_program_class"] = V({g: {k: r(bg[g][k]) for k in cols} for g in bg}, src2 + "prediction.json oes_by_program_class",
                                      "OES per program class of the test program (a none, b blind, c aimed, d regional); "
                                      "1 - OES(O_noinput) = the share of the K-to-O skill that needs the test program")
    A2 = load(afile)
    if A2:
        src3 = f"results/{afile} (analyse2.py on origin/gpu-jobs:jobs/{jid}/out: scores.npz, items.npz, design*.npz)"
        S["status_job"] = V(A2["status"], src3 + " status",
                             "job2 exits 0 even if its report stage fails (the Mac's review, point 5): prediction_final and "
                             "report_failures_in_progress_txt are the check")
        S["ladder"] = V(r(A2["ladder"], 4), src3 + " ladder",
                        "L = fair energy score pooled over items and the primary cells (level 2 jointly at h = 8, 16, 32 ticks); "
                        "skill = (L(K) - L) / (L(K) - L(O)); families net / ridge / law / lin2; D, S, S2 by Lab episodes")
        S["gaps_by_truth"] = V(r(A2["gaps_L_by_truth"]["pairs"], 4), src3 + " gaps_L_by_truth", A2["gaps_L_by_truth"]["note"])
        S["acceptance_variants"] = V(r(A2["acceptance"]["rows"], 3), src3 + " acceptance.rows", A2["acceptance"]["note"])
        S["acceptance_best_over_families"] = V(r(A2["acceptance"]["best_over_families"], 3), src3 + " acceptance.best_over_families",
                                               "a sensitivity outside the roadmap's one-family rule: the best null (any D@n "
                                               "or P0), the best C (any C, Cded or Cft) and the best S over the families; "
                                               "full_history = net, ridge, law, lin2; short_history = net~3, ridge~3, law")
        S["theory_T"] = V(r(A2["theory_T"]["by_budget"], 4), src3 + " theory_T", A2["theory_T"]["note"])
        S["cchg_by_truth"] = V(r(A2["cchg"], 3), src3 + " cchg", A2["cchg"]["note"])
        if "law_design" in A2:
            S["law_design"] = V(r(A2["law_design"], 4), src3 + " law_design", A2["law_design"]["note"])
        if "identification" in A2:
            S["identification_digest"] = V(r(A2["identification"], 3), src3 + " identification", A2["identification"]["note"])
    return {k + tag: v for k, v in S.items()}


S.update(exam_sections("", JD2, J2, "analysis2.json"))
S.update(exam_sections("_B", "job3", J3, "analysis2_B.json"))
for tag_ in ("A", "B"):
    OV = load(f"offline_views_{tag_}.json")
    if not OV:
        continue
    sk = OV["skill"]
    by_budget = {}
    for view in OV["views"]:
        by_budget[view] = {}
        for n in OV["budgets"]:
            fams_ = OV.get("families", ["ridge", "net"])
            nulls = {f"{f}[{view}]|{q}": sk[f"{f}[{view}]|{q}"] for f in fams_ for q in ("P0", f"D@{n}")}
            cs = {f"{f}[{view}]|C": sk[f"{f}[{view}]|C"] for f in fams_}
            kn, kc = max(nulls, key=nulls.get), max(cs, key=cs.get)
            by_budget[view][str(n)] = {"sigma": round(1 - nulls[kn] / cs[kc], 3), "null": kn, "C": kc}
    S[f"offline_views_{tag_}"] = V(
        {"views_lags_kept": OV["views"], "lags_ticks": OV["lags_ticks"], "n_truths": OV["n_truths"], "steps": OV["steps"],
         "skill": r(sk), "pod_skill_for_comparison": r(OV["pod_skill_for_comparison"]),
         "sigma_same_family": r(OV["sigma"]), "rho": r(OV["rho"]), "pm_loss": r(OV["pm_loss"]),
         "history_value": r(OV["history_value"]), "sigma_best_null_by_budget": by_budget},
        f"results/offline_views_{tag_}.json (offline_views.py on the arrays of origin/gpu-jobs:jobs/"
        f"{J2 if tag_ == 'A' else J3}/out; CPU)",
        OV["note"] + "; sigma_best_null_by_budget = 1 - skill(best null) / skill(best C), null over ridge and net P0 and D@n of "
        "the view, C over ridge and net of the view (point estimates); in sigma_same_family the 'best[view]' rows also "
        "admit the law fitted to Lab data (T) as a null, which never was the best")
S["review_of_job2"] = V({
    "major: the closing scan shrank to J = 3, one anchor": "as predicted by the review (job1.py's rate table in --scan-only "
        "mode); fixed in job1.py after the run (rate table of two rows or job 1's bench rows, flat 0.8 x below the smallest "
        "measured batch down to B = 64, explicit --J and --anchors); the scan of job 2 is reported as 'scan2' and marked "
        "noisy unless the scan-only job replaced it",
    "2 pilot marker": "job2.py now writes PILOT_NEVER_REUSE_AS_EXAM into every JSON and npz output (after the run); the "
        "copies in results/job2 carry it (fetch_job.py); the files on gpu-jobs:jobs/r5-vortexexam-003/out other than "
        "info.json and truths.json do not, and are pilot data never to be reused as an exam",
    "3 size limit checked by construction": "job2.py now records a file over the per-file limit and exits non-zero",
    "4 out-of-memory ends job 2": "not changed (peak about 10 GB at batch 1024)",
    "5 exit 0 if the final report fails": "job2.py now exits non-zero in that case (after the run); for the run itself "
        "see status_job (prediction_final, report_failures_in_progress_txt)",
    "6 _paths.py of track1/vortex_world puts /home/user/evalwork first on sys.path": "not changed (not this study's file); "
        "vxlib imports vw from the repository copy first; the two vw copies were compared file by file on 10 Nov (identical)"},
    "origin/gpu-jobs:jobs/r5-vortexexam-003/review.md")
S["review_of_job1"] = V({
    "1 GPU-backend check": "fixed: job2.py and job1.py --scan-only assert jax.default_backend() == 'gpu' unless --smoke",
    "2 output size": "fixed: every file written atomically and under 20 MB (design summaries in parts, programs sparse, level-1 "
                     "rasters of the scan scored on the pod); job 2 audits its total",
    "3 turnover at chunk starts": "fixed: vxlib.summaries takes the previous list (job 2, scan rerun); job 1's arrays keep the "
                                  "zeros and analyse1.py / select_prior.py drop those ticks from turnover statistics",
    "4 bench memory": "relabelled process_peak_bytes_so_far in results/analysis1.json (bench.json of job 1 is unchanged)",
    "5 stage sizers": "not changed in job 1 (finished); job 2 takes its sizes from presets against the measured rate and the "
                      "scan rerun from job 2's measured rate",
    "info: atomic npz": "fixed in job1.py and job2.py (temporary name, then os.replace)"},
    "origin/gpu-jobs:jobs/r5-vortexexam-002/review.md and the coordinator's relay of it")


# ----------------------------------------------------------------------------- headline: the numbers of the report
def headline():
    """Each entry: value + the summary section (and through it the job file and key) it is taken from."""
    Hd = {}

    def put(name, value, section, note=None):
        Hd[name] = {"value": value, "from": f"summary.json {section}", "source": S[section.split(" ")[0]]["source"]}
        if note:
            Hd[name]["note"] = note
    if "throughput" in S:
        rows = S["throughput"]["value"]
        put("member_ticks_per_s_H200", {f"{q['H']}px_B{q['B']}": round(q["member_ticks_per_s"]) for q in rows if q.get("track")},
            "throughput", "job 1, H200, float64, with the vortex tracker")
        t128 = [q for q in rows if q["H"] == 128 and q["B"] == 1024]
        if len(t128) == 2:
            put("tracker_and_host_pipeline_cost_128px", round(1 - t128[0]["member_ticks_per_s"] / t128[1]["member_ticks_per_s"], 4)
                if t128[1]["track"] is False else round(1 - t128[1]["member_ticks_per_s"] / t128[0]["member_ticks_per_s"], 4),
                "throughput", "1 - rate with the tracker / rate without, batch 1024")
    for tag, jid, st in (("", J2, st2), ("_B", J3, st3)):
        if "platform_job" + tag in S:
            pj = S["platform_job" + tag]["value"]
            gpu = ((st or {}).get("pods") or [{}])[0]
            rate_usd = gpu.get("rate_usd_hr")
            put("exam_job" + tag, {"job": jid, "gpu": gpu.get("gpu"), "provider": gpu.get("provider"), "usd_per_hour": rate_usd,
                                  "member_ticks_per_s": round(pj["rate"], 1), "preset": pj["preset"],
                                  "member_ticks": pj["member_ticks_total"], "hours_in_job": r(pj["hours"]),
                                  "usd_per_million_member_ticks": round(rate_usd / 3600 / pj["rate"] * 1e6, 2) if rate_usd else None,
                                  "billed_usd": ((st or {}).get("cost") or {}).get("billed_usd")}, "platform_job" + tag)
    if st1 and "throughput" in S:
        rr = [q for q in S["throughput"]["value"] if q["H"] == 128 and q["B"] == 1024 and q.get("track")]
        rate1 = (st1.get("pods") or [{}])[0].get("rate_usd_hr")
        if rr and rate1:
            put("usd_per_million_member_ticks_H200_128px", round(rate1 / 3600 / rr[0]["member_ticks_per_s"] * 1e6, 2), "throughput",
                f"at the billed ${rate1}/h of job 1")
    if "law" in S:
        L = S["law"]["value"]["s_b"]
        put("law_b1_per_eps", {"eps": S["law"]["value"]["eps"], "b1": L["b1_per_eps"], "se": L["b1_se"]}, "law")
        put("law_b1_line_eps_positive", L["b1_line_eps_positive"], "law")
        put("law_b1_proportional_chi2", L["b1_proportional"], "law")
        put("law_shape_r2", L["shape_r2"], "law")
        put("law_share_of_change_variance", L["share_of_change_variance_explained_by_law"], "law")
        put("law_integrated_mean_max_abs_error", {"in_sample": L["integrated_law_max_abs_error_of_mean"],
                                                  "out_of_sample": L["integrated_law_out_of_sample"]}, "law")
    if "scan" in S and S["scan"]["value"].get("table"):
        tb = S["scan"]["value"]["table"]
        put("headroom_level2_lo_hi", {q: [tb[q]["L2_lo"], tb[q]["L2_hi"]] for q in tb}, "scan")
        put("headroom_level1_lo_hi", {q: [tb[q]["L1_lo"], tb[q]["L1_hi"]] for q in tb}, "scan")
        put("headroom_null_floor", {q: S["scan"]["value"]["null_floor"][q] for q in ("L2_mean", "L2_mean_se", "L1_mean", "L1_mean_se")}, "scan")
    for tag in ("", "_B"):
        if "ladder" + tag not in S:
            continue
        lad, gp, ac = S["ladder" + tag]["value"], S["gaps_by_truth" + tag]["value"], S["acceptance_variants" + tag]["value"]
        nb = str(lad["budgets_episodes"][-1])
        fam = lad["families"]
        sk = {}
        for f in fam:
            sk[f] = {q: fam[f][q]["skill"] for q in ("P0", "C", "PM", "Cded", "Cft") if q in fam[f]}
            for q in ("D", "S", "S2", "Sded", "Sft"):
                if q in fam[f]:
                    sk[f][q] = {n: v["skill"] for n, v in fam[f][q].items()}
        put("skill" + tag, sk, "ladder" + tag, "(L(K) - L) / (L(K) - L(O)), pooled over items and the primary cells")
        put("refs" + tag, {q: lad[q] for q in ("L_K", "L_O", "skill_K0", "skill_O_noinput", "n_truths", "n_items_per_truth")}, "ladder" + tag)
        acc = {}
        for k, v in ac.items():
            parts = k.split("|")
            if parts[0].endswith("@" + nb) and (k.endswith("|K|joint") or k.endswith("|finetuned") or k.endswith("|dedicated")
                                                or k.endswith("|C_full_history")):
                acc[k] = {q: v[q] for q in ("sigma", "sigma_se_worlds", "null_is", "rho", "rho_se_worlds", "pass_sigma", "pass_rho",
                                            "worlds_passing_sigma", "n_worlds")}
        put("acceptance_at_largest_budget" + tag, acc, "acceptance_variants" + tag)
        put("acceptance_best_over_families" + tag, S["acceptance_best_over_families" + tag]["value"], "acceptance_best_over_families" + tag)
        keep = {}
        for k, v in gp.items():
            if k in ("net|PM - net|C", "net|P0 - net|C", "net|PM - net|P0", "ridge|PM - ridge|C", "net|P0 - net|Cft", "net|C - net|Cft",
                     "net|Cded - net|Cft", "net~3|P0 - net~3|C", "net~3|P0 - net~3|Cft", "net~3|PM - net~3|C", "net~3|P0 - net|P0",
                     "net~3|C - net|C", "net~3|Cft - net|Cft", "lin2|P0 - net|P0", "ridge|P0 - net|P0", "law|P0 - net|P0", "K0 - K",
                     "O_noinput - oracle", f"net|D@{nb} - net|P0", f"net~3|D@{nb} - net~3|P0", f"ridge~3|D@{nb} - net~3|P0"):
                keep[k] = {q: v[q] for q in ("in_skill_units", "z_truths", "truths_with_sign_of_mean", "n_truths")}
        put("gaps" + tag, keep, "gaps_by_truth" + tag, "first minus second in skill units (positive: the second is better)")
        put("theory_T" + tag, {n: {"skill_T": v["skill_T"], "share_of_D_to_C_gap_closed_by_T": v.get("share_of_D_to_C_gap_closed_by_T"),
                                   **{q: {"in_skill_units": v[q]["in_skill_units"], "z_truths": v[q]["z_truths"]} for q in v
                                      if isinstance(v[q], dict)}} for n, v in S["theory_T" + tag]["value"].items()}, "theory_T" + tag)
        cc = S["cchg_by_truth" + tag]["value"]
        put("predictable_change_s_b" + tag, {
            "hs_ticks": cc["hs_ticks"], "oracle_share_pooled": [x[1] for x in cc["oracle_predictable_share_pooled"]],
            "oracle_share_within_truth": [x[1] for x in cc["oracle_predictable_share_within_truth"]],
            "reached_pooled": {q: [x[1] for x in v] for q, v in cc["reached_pooled"].items()
                               if q.split("|")[-1] in ("P0", "C", "Cft", "Cded") or q in ("anchor",)},
            "reached_within_truth": {q: {"value": [x[1] for x in v["value"]], "se_truths": [x[1] for x in v["se_truths"]]}
                                     for q, v in cc["reached_within_truth"].items()
                                     if q.split("|")[-1] in ("P0", "C", "Cft", "Cded")}}, "cchg_by_truth" + tag)
        if "identification_digest" + tag in S:
            idg = S["identification_digest" + tag]["value"]
            put("identification" + tag, {"names": idg["names"], "contraction": idg["contraction_by_level_and_budget"],
                                         "in90": idg["in90"]}, "identification_digest" + tag)
        if "law_design" + tag in S:
            ld = S["law_design" + tag]["value"]
            put("law_on_design" + tag, {q: ld[q] for q in ("share_explained", "b1_at_box_centre", "b1_slope_per_unit_eps",
                                                           "b1_zero_crossing_eps_at_centre_of_others", "b1_relative_change_across_box",
                                                           "b2_relative_change_across_box", "per_theta_b1", "n_thetas")}, "law_design" + tag)
        if "by_program_class" + tag in S:
            put("oracle_without_program_by_class" + tag, {g: v.get("O_noinput") for g, v in S["by_program_class" + tag]["value"].items()},
                "by_program_class" + tag, "OES of the oracle that ignores the test program (a none, b blind, c aimed, d regional)")
    # what the prior-predictive training set (P0) costs on CPU: the envelope question of the roadmap
    v128 = os.path.join(os.path.dirname(os.path.dirname(HERE)), "track1", "vortex128", "results", "summary.json")
    if os.path.exists(v128):
        cpu = json.load(open(v128))["timing"]["value"]["main128_sel"]["cpu_s_per_member_tick"]
        env = {"cpu_s_per_member_tick_128px": cpu, "envelope_core_hours_4_cores_24_h": 96, "gliders_P0_core_hours": 3.2}
        for tag in ("", "_B"):
            if "platform_job" + tag in S and PR:
                cfg = S["platform_job" + tag]["value"]["config"]
                mt = cfg["N_theta"] * cfg["K_d"] * PR["T_ep"]
                env["P0_design" + tag] = {"episodes": cfg["N_theta"] * cfg["K_d"], "member_ticks": mt,
                                          "core_hours": round(mt * cpu / 3600, 1),
                                          "usd_on_the_job_gpu": Hd.get("exam_job" + tag, {}).get("value", {}).get("usd_per_million_member_ticks")
                                          and round(mt / 1e6 * Hd["exam_job" + tag]["value"]["usd_per_million_member_ticks"], 2)}
        Hd["P0_cost_envelope"] = {"value": env, "from": "track1/vortex128/results/summary.json timing.main128_sel.cpu_s_per_member_tick "
                                  "(one CPU core, round 3) x the design size of each exam job (summary.json platform_job.config); "
                                  "gliders: roadmap/ROADMAP.md section 3"}
    Hd["gliders_reference"] = {"value": {"prior_mean_plug_in_loss_oes": [0.03, 0.09], "sigma_max": 0.05, "rho_range": [0.77, 0.94],
                                         "usd_per_million_member_ticks_A100": 0.40},
                               "from": "program/README.md (round 4, round4/sbi) and roadmap/ROADMAP.md sections 1-2; not recomputed here"}
    return Hd


S["headline"] = headline()
json.dump(S, open(os.path.join(RES, "summary.json"), "w"), indent=1)
print("wrote", os.path.join(RES, "summary.json"), "keys", list(S))
