"""make_summary -- results/summary.json of dialsB from the job's published output (numpy-free, seconds).

    python -B make_summary.py JOBDIR [JOB_ID]

JOBDIR is the job's folder as published on the gpu-jobs branch (status.json, out/...), for example extracted with
    git archive origin/gpu-jobs jobs/r6-dialsB-001 | tar -x -C SCRATCH        (JOBDIR = SCRATCH/jobs/r6-dialsB-001)
Copies the small JSON outputs to results/job/ and writes results/summary.json: every number of the README with
its source (job id, file, key). Nothing is recomputed here except sums and ranges of numbers already in the files.
PILOT values, never to be reused as an exam.
"""
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
jobdir = sys.argv[1]
job_id = sys.argv[2] if len(sys.argv) > 2 else os.path.basename(os.path.normpath(jobdir))
out = os.path.join(jobdir, "out")
res = os.path.join(HERE, "results")
dst = os.path.join(res, "job")
os.makedirs(os.path.join(dst, "gate"), exist_ok=True)
os.makedirs(os.path.join(dst, "scan"), exist_ok=True)
for f in ("analysis.json", "ranges.json", "ranges.sha256", "presmoke.json", "align.json", "progress.txt"):
    if os.path.exists(os.path.join(out, f)):
        shutil.copy(os.path.join(out, f), os.path.join(dst, f))
for sub in ("gate", "scan"):
    for f in sorted(os.listdir(os.path.join(out, sub))):
        if f.endswith(".json"):
            shutil.copy(os.path.join(out, sub, f), os.path.join(dst, sub, f))
status = json.load(open(os.path.join(jobdir, "status.json")))
shutil.copy(os.path.join(jobdir, "status.json"), os.path.join(dst, "status.json"))
A = json.load(open(os.path.join(out, "analysis.json")))
R = json.load(open(os.path.join(out, "ranges.json")))
P = json.load(open(os.path.join(out, "presmoke.json")))
AL = json.load(open(os.path.join(out, "align.json"))) if os.path.exists(os.path.join(out, "align.json")) else None
src = lambda f, k: {"job": job_id, "file": f"jobs/{job_id}/out/{f}", "key": k}            # noqa: E731
seeds = A["seeds"]


def cond_row(name):
    c = A["conditions"][name]
    r = {k: c.get(k) for k in ("closed", "share_s", "threshold", "direction", "holds_at_point", "mean", "se", "lower90", "upper90", "reading", "status", "gap_readable") if k in c}
    r["source"] = src("analysis.json", f"conditions.{name}")
    return r


def pooled(arm, view, sub, pol):
    s = A["arms"][arm][view][sub]["pooled_8_16_32"][pol]
    return {"closed": s["closed"], "per_seed": s["per_seed"], "median_seed": s["median_seed"],
            "leave_one_seed_out_range": s["leave_one_seed_out_range"], "bootstrap_seeds_5_95": s["bootstrap_seeds_5_95"],
            "source": src("analysis.json", f"arms.{arm}.{view}.{sub}.pooled_8_16_32.{pol}")}


S = {"PILOT_NEVER_REUSE_AS_EXAM": True,
     "what": "dialsB: stage 0 of the membrane carrier (study B of ../PLAN.md), the CPU gate; state given, 64 px, 8 fresh seeds, "
             "main and control arm; every number with its source. DECLARED.md holds the rule, written before any run.",
     "job": {"id": job_id, "state": status.get("state"), "exit_code": status.get("exit_code", status.get("run_exit_code")),
             "status_fields": {k: status[k] for k in status if any(t in k.lower() for t in ("cost", "rate", "hour", "price", "billed", "pod", "gpu", "offer", "started", "finished", "ended", "elapsed", "seconds"))
                               and not isinstance(status[k], (list,))},
             "source": {"job": job_id, "file": f"jobs/{job_id}/status.json"}},
     "sizes": {"seeds": seeds, "arms": ["main (cat = 1)", "control (cat = 0)"], "px": 64, "lab_episodes": 16, "truths_per_item": 6,
               "test_items_per_seed_arm": {arm: {s: A["arms"][arm]["heaviest"][str(s)]["items"] for s in map(str, seeds)} for arm in A["arms"]},
               "member_ticks_gate": A["cost"]["member_ticks_gate"], "planned_member_ticks": P["planned_member_ticks"],
               "steady_rate_member_ticks_per_s_presmoke": P["steady_rate_member_ticks_per_s"],
               "source": [src("analysis.json", "cost"), src("presmoke.json", "planned_member_ticks")]},
     "truths_pilot": {"values": A["truths_pilot"], "source": src("analysis.json", "truths_pilot")},
     "verdict": dict(A["verdict"], source=src("analysis.json", "verdict")),
     "conditions": {k: cond_row(k) for k in A["conditions"]},
     "table_focus": {}, "table_cell_resolved": {}, "by_horizon": {}, "stand_in": {}, "scans": {}}
for arm in A["arms"]:
    for view, key in (("focus", "table_focus"), ("cr", "table_cell_resolved")):
        S[key][arm] = {sub: {p: pooled(arm, view, sub, p) for p in ("G2", "G3", "A_act", "Gstar", "G1", "G4", "H", "pub0")}
                       for sub in ("all_start_states", "heaviest_left_out")}
        S[key][arm]["Gstar_picks"] = {"picks": A["arms"][arm][view]["Gstar_picks"], "source": src("analysis.json", f"arms.{arm}.{view}.Gstar_picks")}
        S[key][arm]["gap_share_by_horizon_8_16_32"] = {"values": A["arms"][arm][view]["gap_share_by_horizon_8_16_32"],
                                                       "source": src("analysis.json", f"arms.{arm}.{view}.gap_share_by_horizon_8_16_32")}
    S["by_horizon"][arm] = {view: {sub: {"pooled": A["arms"][arm][view][sub]["by_horizon"], "per_seed": A["arms"][arm][view][sub]["by_horizon_per_seed"],
                                         "source": src("analysis.json", f"arms.{arm}.{view}.{sub}.by_horizon / by_horizon_per_seed")}
                                   for sub in ("all_start_states", "heaviest_left_out")} for view in ("focus", "cr")}
    S["by_horizon"][arm]["heaviest"] = {"per_seed": A["arms"][arm]["heaviest"], "source": src("analysis.json", f"arms.{arm}.heaviest")}
    S["by_horizon"][arm]["fits"] = {"A_act_g0_g1_tau_blur": A["arms"][arm]["focus"]["A_act_fits"], "H_lam_rho_DX_a0": A["arms"][arm]["focus"]["H_fits_lam_rho_DX_a0"],
                                    "source": src("analysis.json", f"arms.{arm}.focus.A_act_fits / H_fits_lam_rho_DX_a0")}
    st = A["arms"][arm]["stand_in"]
    S["stand_in"][arm] = {"mix_8_16_32": st["mix_8_16_32"], "by_class_8_16_32": {c: {k: v[k] for k in ("share_s", "state_given_gap", "kept", "skill_Cs_of_oracle")}
                                                                                 for c, v in st["by_class_8_16_32"].items()},
                          "by_horizon_mix": {h: {k: v[k] for k in ("share_s", "state_given_gap", "kept", "skill_Cs_of_oracle")} for h, v in st["by_horizon_mix"].items()},
                          "source": src("analysis.json", f"arms.{arm}.stand_in")}
S["scans"] = {"ranges_sha256": open(os.path.join(out, "ranges.sha256")).read().split()[0],
              "hidden_set": R["hidden_set"], "carrier_ranges": {k: {"range": v["range"], "scan_failed": v["scan_failed"],
                                                                     "rows": [{kk: r[kk] for kk in ("value", "gap_none", "gap_blind", "gap_aimed", "members_with_focus_cell", "admissible")} for r in v["rows"]]}
                                                                for k, v in R["carrier_ranges"].items()},
              "scan_V": {p: {k: r[k] for k in ("family", "viable", "headroom_by_factor", "box_factors", "headroom", "eligible")} for p, r in R["scan_V"].items()},
              "scan_V_default_floor": R["scan_V_default_floor"],
              "source": [src("ranges.json", "hidden_set / carrier_ranges / scan_V"), src("ranges.sha256", "")]}
if AL is not None:
    S["alignment_with_the_pilots"] = dict({k: AL[k] for k in ("max_abs_diff_L_pub_pub0_O", "L_mean_over_items_sum_of_4_horizons", "designer_file_L",
                                                               "closed_by_horizon_4_8_16_32", "adversary_file_closed_by_horizon", "closed_h_8_16_32",
                                                               "adversary_file_closed_h_8_16_32", "A_act_fit", "adversary_A_act_fit", "Gstar_pick")},
                                          source=src("align.json", ""))
with open(os.path.join(res, "summary.json"), "w") as f:
    json.dump(S, f, indent=1)
print("wrote results/summary.json; verdict", A["verdict"])
for k, c in A["conditions"].items():
    print(" ", k, {kk: (round(v, 3) if isinstance(v, float) else v) for kk, v in c.items() if kk in ("closed", "share_s", "lower90", "upper90", "reading", "holds_at_point")})
