"""make_summary4 -- results/summary.json from the job outputs copied to results/ (every number with its source).

usage: python -B make_summary4.py JOB_ID   (results/<files> copied from origin/gpu-jobs:jobs/JOB_ID/out/,
                                           results/status.json from jobs/JOB_ID/status.json)
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.environ.get("W4_RES", os.path.join(HERE, "results"))
JOB = sys.argv[1]
def rnd(v, k):
    if v is None or isinstance(v, (str, bool)):
        return v
    if isinstance(v, dict):
        return {a: rnd(b, k) for a, b in v.items()}
    if isinstance(v, np.ndarray):
        v = v.tolist()
    if isinstance(v, (list, tuple)):
        return [rnd(b, k) for b in v]
    return round(float(v), k)


r3 = lambda v: rnd(v, 3)
r4 = lambda v: rnd(v, 4)


def J(fn):
    return json.load(open(os.path.join(RES, fn)))


def src(fn, key):
    return {"job": JOB, "file": f"origin/gpu-jobs:jobs/{JOB}/out/{fn}", "copy": f"results/{fn}", "key": key}


def val(v, fn, key, rnd=r4):
    return {"value": rnd(v), "source": src(fn, key)}


def closure_block(S, view):
    fn = f"closure_{S}_{view}.json"
    if not os.path.exists(os.path.join(RES, fn)):
        return None
    d = J(fn)
    b = {"horizons": d["horizons_ticks"], "n_items": d["n_test_states"], "replicates": d["replicates"],
         "J": d["data"]["J"], "T": d["data"]["T"], "seed": d["data"]["seed"],
         "ceiling": val(d["ceiling"], fn, "ceiling"), "ceiling_se": val(d["ceiling_se"], fn, "ceiling_se"),
         "best_name": {"value": d["best_name"], "source": src(fn, "best_name")},
         "V_best": val(d["best_level1"], fn, "best_level1"), "V_oracle": val(d["V_oracle"], fn, "V_oracle"),
         "V0": val(d["V0_mean_predictor"], fn, "V0_mean_predictor"),
         "copy_check_max_abs_diff": val(d["copy_check_max_abs_diff"], fn, "copy_check_max_abs_diff")}
    if "selection_check" in d:
        b["selection_checked_ceiling"] = val(d["selection_check"]["ceiling_mean"], fn, "selection_check.ceiling_mean")
        b["vw0_set_only_ceiling"] = val(d["vw0_set_only"]["ceiling"], fn, "vw0_set_only.ceiling")
    if "learning_curve" in d:
        lc = d["learning_curve"]
        b["learning_curve"] = {"ceiling": {k: val(v, fn, f"learning_curve.ceiling.{k}") for k, v in lc["ceiling"].items()},
                               "fit_trajectories_per_fold": lc["fit_trajectories_per_fold"],
                               "saturated": {"value": lc["saturated"], "source": src(fn, "learning_curve.saturated")},
                               "rel_drop_half_to_all": val(lc["rel_drop_half_to_all"], fn, "learning_curve.rel_drop_half_to_all")}
    if "MW" in d:
        m = d["MW"]
        b["MW"] = {k: val(m[k], fn, f"MW.{k}") for k in ("V_oracle", "ceiling_wind_free_predictors", "oracle_cost_dV_over_Vbest_M",
                                                       "oracle_cost_dV_over_Vbest_M_se", "best_M_predictor_error_increase")}
    if "error_by_feature_group" in d and d["error_by_feature_group"]:
        b["oracle_by_group"] = {g: val(v["oracle"], fn, f"error_by_feature_group.{g}.oracle")
                                for g, v in d["error_by_feature_group"].items()}
    return b


def main():
    S = {"what": "Round-4 study 'wind' (track 2): full-size certification of the gliders wind world (sigma_w = 0.05) on "
                 "one GPU: free-run closure F vs the wind-free M at the fresh layout (36 trajectories, h = 1-32, JAX nets, "
                 "learning curves), a second independent F/M pair for the objects view, the paired oracle cost MW, and the "
                 "program-mix set P (36 trajectories, 324 items, input-aware patchnet/slotnet, exam effect, energy scores)",
         "job": JOB, "code": {k: f"research/alife/vecworld/program/round4/wind/{k}" for k in
                              ("w4.py", "sim4.py", "check4.py", "clos4.py", "p4lib.py", "combine4.py", "job.sh", "make_summary4.py")}}
    st = J("status.json") if os.path.exists(os.path.join(RES, "status.json")) else {}
    S["status"] = {"source": f"origin/gpu-jobs:jobs/{JOB}/status.json (copy results/status.json)",
                   **{k: st.get(k) for k in ("state", "exit_code", "cost", "pod", "started_at", "finished_at", "message")}}
    if st.get("pods"):
        from datetime import datetime
        p = st["pods"][0]
        t = lambda x: datetime.fromisoformat(x.replace("Z", "+00:00"))
        S["status"]["pod_times"] = {k: p.get(k) for k in ("requested_at", "created_at", "ready_at", "terminated_at")}
        S["status"]["pod_hours_created_to_terminated"] = round((t(p["terminated_at"]) - t(p["created_at"])).total_seconds() / 3600, 3)
        S["status"]["run_hours_started_to_finished"] = round((t(st["finished_at"]) - t(st["started_at"])).total_seconds() / 3600, 3)
    fm = J("sim_FM.json")
    S["platform"] = {"value": fm["platform"], "source": src("sim_FM.json", "platform")}
    S["simulation"] = {"FM": {"member_ticks": val(fm["member_ticks"], "sim_FM.json", "member_ticks", r3),
                              "member_ticks_per_s": val(fm["member_ticks_per_s"], "sim_FM.json", "member_ticks_per_s", r3),
                              "seconds": val(fm["seconds"], "sim_FM.json", "seconds", r3)}}
    for tag in ("FM2", "P"):
        fn = f"sim_{tag}.json"
        if os.path.exists(os.path.join(RES, fn)):
            d = J(fn)
            S["simulation"][tag] = {"member_ticks": val(d.get("member_ticks"), fn, "member_ticks", r3),
                                    "seconds": val(d.get("seconds"), fn, "seconds", r3)}
    if os.path.exists(os.path.join(RES, "check4.json")):
        c = J("check4.json")
        S["runner_check"] = {k: val(c[k], "check4.json", k, lambda v: v) for k in c if k != "devices"}
    S["closure"] = {f"{s}_{v}": closure_block(s, v) for s in ("F", "M", "F2", "M2", "P") for v in ("coarse", "objects")
                    if closure_block(s, v) is not None}
    cb = J("combine.json")
    fnc = "combine.json"
    S["F_vs_M"] = {}
    for view, r in cb["views"].items():
        b = {k: val(r[k], fnc, f"views.{view}.{k}") for k in ("ceiling_F", "ceiling_M", "dceiling_F_minus_M", "dceiling_se", "dceiling_z")}
        b["common_scale"] = {k: val(r["common_scale"][k], fnc, f"views.{view}.common_scale.{k}") for k in
                             ("V_oracle_F", "V_oracle_M", "dV_oracle", "dV_oracle_se", "dV_oracle_over_Vbest_M",
                              "dV_best", "dV_best_se", "dV_best_over_Vbest_M")}
        b["event_split"] = {k: val(r["event_split"][k], fnc, f"views.{view}.event_split.{k}") for k in r["event_split"]}
        for s in ("F", "M"):
            ch = r.get(f"chaos_{s}")
            if ch:
                b[f"chaos_{s}"] = {k: val(ch[k], fnc, f"views.{view}.chaos_{s}.{k}") for k in
                                   ("cross_half_natural", "cross_0.9_natural", "natural_uncond")}
                b[f"chaos_{s}"]["curve_at_h"] = val([ch["curve_mean"][h - 1] for h in (1, 2, 4, 8, 16, 32, 64, 96)], fnc,
                                                    f"views.{view}.chaos_{s}.curve_mean[h-1], h = 1,2,4,8,16,32,64,96")
        if "feature_groups" in r:
            b["feature_groups"] = {g: {k: val(x[k], fnc, f"views.{view}.feature_groups.{g}.{k}") for k in ("dceiling", "dceiling_se")}
                                   for g, x in r["feature_groups"].items()}
        S["F_vs_M"][view] = b
    if "objects_pair2" in cb:
        r = cb["objects_pair2"]
        S["F_vs_M"]["objects_pair2"] = {k: val(r[k], fnc, f"objects_pair2.{k}") for k in
                                        ("ceiling_F", "ceiling_M", "dceiling_F_minus_M", "dceiling_se", "dceiling_z")}
        S["F_vs_M"]["objects_pair2"]["common_scale"] = {k: val(r["common_scale"][k], fnc, f"objects_pair2.common_scale.{k}")
                                                        for k in ("dV_oracle", "dV_oracle_se", "dV_best", "dV_best_se")}
    if "objects_pooled_pairs" in cb:
        p = cb["objects_pooled_pairs"]
        S["F_vs_M"]["objects_pooled"] = {k: val(p[k], fnc, f"objects_pooled_pairs.{k}") for k in p
                                         if k not in ("note", "feature_groups")}
        if "feature_groups" in p:
            S["F_vs_M"]["objects_pooled"]["feature_groups"] = {
                g: {k: val(x[k], fnc, f"objects_pooled_pairs.feature_groups.{g}.{k}") for k in x} for g, x in p["feature_groups"].items()}
    # ---- P
    S["P"] = {}
    for view in ("coarse", "objects"):
        fn = f"closure_P_{view}.json"
        if not os.path.exists(os.path.join(RES, fn)):
            continue
        d = J(fn)
        ee, tw, es, rec = d["exam_effect"], d["twin_effect"], d["energy_score"], d["recovered"]
        b = {"V": {nm: val(v, fn, f"V.{nm}") for nm, v in d["V"].items()},
             "items": {"value": d["items_meta"], "source": src(fn, "items_meta")},
             "best_all": {"value": ee["best_all"], "source": src(fn, "exam_effect.best_all")},
             "best_blind": {"value": ee["best_blind"], "source": src(fn, "exam_effect.best_blind")},
             "ceiling_by_class": {kl: {k: val(v[k], fn, f"exam_effect.by_class.{kl}.{k}") for k in ("ceiling_all", "ceiling_blind")}
                                  for kl, v in ee["by_class"].items()},
             "true_effect_over_Vbest": {kl: val(v["crn_effect_over_Vbest"], fn, f"twin_effect.{kl}.crn_effect_over_Vbest")
                                        for kl, v in tw.items() if "crn_effect_over_Vbest" in v},
             "true_effect_se_over_Vbest": {kl: val(v["crn_effect_se_over_Vbest"], fn, f"twin_effect.{kl}.crn_effect_se_over_Vbest")
                                           for kl, v in tw.items() if "crn_effect_se_over_Vbest" in v},
             "ideal_loss": {kl: {k: val(v[k], fn, f"twin_effect.ideal_loss_detectability.{kl}.{k}") for k in
                                 ("loss_over_Vbest", "z_n64_R1", "z_n128_R1", "z_n64_R6", "z_n128_R6")}
                            for kl, v in tw["ideal_loss_detectability"].items()},
             "achieved_best_blind_to_best_all": {kl: {k: val(ee["best_vs_best"][kl][k], fn, f"exam_effect.best_vs_best.{kl}.{k}")
                                                      for k in ("loss_over_Vbest", "loss_se", "z_n64_R1", "z_n128_R1", "z_n64_R6",
                                                                "z_n128_R6", "mde80_over_Vbest_n64_R1")}
                                                 for kl in ("all", "programs_only", "aimed_regional", "blind", "aimed", "regional")},
             "fixed_pairs": {pn: {kl: {k: val(v[kl][k], fn, f"exam_effect.fixed_pairs.{pn}.{kl}.{k}") for k in
                                       ("loss_over_Vbest", "z_n64_R1", "z_n128_R1")} for kl in ("all", "aimed_regional")}
                             for pn, v in ee["fixed_pairs"].items()},
             "recovered_share": {pn: {kl: {k: val(x[k], fn, f"recovered.{pn}.{kl}.{k}") for k in x} for kl, x in v.items()}
                                 for pn, v in rec.items()},
             "energy": {"oes": {nm: val(v, fn, f"energy_score.oes.{nm}") for nm, v in es["oes"].items()},
                        "best_by_es_all": {"value": es["best_by_es_all"], "source": src(fn, "energy_score.best_by_es_all")},
                        "best_by_es_blind": {"value": es["best_by_es_blind"], "source": src(fn, "energy_score.best_by_es_blind")},
                        "pairs": {pn: {kl: {k: val(x[k], fn, f"energy_score.pairs.{pn}.{kl}.{k}") for k in
                                            ("loss_mean", "loss_se", "loss_over_ref", "z_n64_R1", "z_n128_R1", "z_n64_R6", "z_n128_R6")}
                                       for kl, x in v.items() if isinstance(x, dict)}
                                  for pn, v in es["pairs"].items()},
                        "share_of_ideal": {pn: val(v["share_of_ideal_all"], fn, f"energy_score.pairs.{pn}.share_of_ideal_all")
                                           for pn, v in es["pairs"].items() if "share_of_ideal_all" in v},
                        "ideal": {kl: {k: val(x[k], fn, f"energy_score.ideal.{kl}.{k}") for k in
                                       ("loss_mean", "loss_over_ref", "z_n64_R1", "z_n128_R1")} for kl, x in es["ideal"].items()}}}
        S["P"][view] = b
    # derived: one-sided 95% bound on an objects-view ceiling loss under wind (pooled pairs): max(0, -(d - 1.645 se))
    if "objects_pooled_pairs" in cb:
        p = cb["objects_pooled_pairs"]
        d, se = np.asarray(p["dceiling_F_minus_M"], float), np.asarray(p["dceiling_se"], float)
        S["F_vs_M"]["objects_pooled"]["loss_upper95_one_sided"] = {
            "value": r4(np.maximum(0.0, -(d - 1.645 * se)).tolist()),
            "source": src(fnc, "derived: max(0, -(objects_pooled_pairs.dceiling_F_minus_M - 1.645 * dceiling_se))")}
    ip = os.path.join(HERE, "interpretation.json")
    if os.path.exists(ip):
        S["interpretation"] = json.load(open(ip))
    json.dump(S, open(os.path.join(RES, "summary.json"), "w"), indent=1)
    print("wrote", os.path.join(RES, "summary.json"))


if __name__ == "__main__":
    main()
