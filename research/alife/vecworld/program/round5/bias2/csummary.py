"""csummary -- results/summary.json of the round-5 study `bias2` (local; every number with its source).

usage: python -B csummary.py RESULTS_DIR world=JOB_ID [world=JOB_ID ...]
Reads RESULTS_DIR/<world>/{combined.json, sim_A.json, sim_B.json, train_done.json, closed_forms.json} (copies of
origin/gpu-jobs:jobs/<JOB_ID>/out/<world>/), RESULTS_DIR/status_<JOB_ID>.json (the job's status.json),
RESULTS_DIR/analysis.json (canalyze.py), RESULTS_DIR/pilot_<world>.json (cpilot.py, CPU) and the hand-written
reading RESULTS_DIR/interpretation.json, and writes RESULTS_DIR/summary.json: meta (sizes, seeds, platform, cost),
per world the hand designs, the learned configs (seed means) with their identification by per-block local
readouts, the comparison at matched effective dimension, the closed-form slow features, and the claims, each
with its source keys. A source "JOB:out/<file>:<key>" is a key of a job output file on the gpu-jobs branch;
"analysis:<key>" is derived from those by canalyze.py (documented there).
"""
import json
import os
import sys

import numpy as np

R = sys.argv[1]
JOBS = dict(a.split("=") for a in sys.argv[2:])
A = json.load(open(os.path.join(R, "analysis.json")))
r4 = lambda v: None if v is None else (np.round(np.asarray(v, float), 4).tolist() if np.ndim(v) else round(float(v), 4))   # noqa: E731
out = {"study": "bias2 (round 5, track 1): the map (level-0 theory x inductive bias) -> emergent variables; rows fed-vortex, "
                "phase-membrane, and the gliders anchor under the same judges",
       "meta": {"jobs": {}, "worlds": {}}, "worlds": {}, "claims": []}
for job in sorted(set(JOBS.values())):
    p = os.path.join(R, f"status_{job}.json")
    if not os.path.exists(p):
        continue
    st = json.load(open(p))
    pod = st.get("pod") or {}
    e = {"job_id": job, "state": st.get("state"), "exit_code": st.get("exit_code"), "gpu": pod.get("gpu"), "provider": pod.get("provider"),
         "rate_usd_hr": pod.get("rate_usd_hr"), "cost": st.get("cost"), "cap_usd": st.get("cap_usd"),
         "worlds": [w for w, j in JOBS.items() if j == job], "source": f"origin/gpu-jobs:jobs/{job}/status.json"}
    for k in ("started_at", "finished_at", "billing_window_hours", "ref", "message"):
        if k in st:
            e[k] = st[k]
    b = (st.get("cost") or {}).get("billed_usd")
    if b is not None and pod.get("rate_usd_hr"):
        e["billed_gpu_hours"] = round(b / pod["rate_usd_hr"], 3)
    out["meta"]["jobs"][job] = e
p = os.path.join(R, "job_history.json")          # hand-kept record: every submission, why it was resubmitted, code changes
if os.path.exists(p):
    out["meta"]["job_history"] = dict(json.load(open(p)), source="results/job_history.json")
tot = [j["cost"]["billed_usd"] for j in out["meta"]["jobs"].values() if j.get("cost") and j["cost"].get("billed_usd") is not None]
out["meta"]["billed_usd_total"] = round(float(sum(tot)), 4) if tot else None
for w, job in JOBS.items():
    if w not in A:
        continue
    src = lambda f, k, w=w, job=job: f"{job}:out/{w}/{f}:{k}"            # noqa: E731
    a = A[w]
    m = {"job": job, "layout": a["layout"], "fields": a["fields"]}
    for h in ("A", "B"):
        p = os.path.join(R, w, f"sim_{h}.json")
        if os.path.exists(p):
            s = json.load(open(p))
            m[f"sim_{h}"] = {k: s.get(k) for k in ("designer_seed", "world_seed", "J_ALL", "J_CERT", "J_requested", "T", "burn_ticks",
                                                    "test_ticks", "TB", "R_BR", "member_ticks", "member_ticks_per_s", "seconds",
                                                    "platform", "global_field_means", "field_stats")}
            m[f"sim_{h}"]["world"] = {k: s["world_desc"].get(k) for k in ("module", "tick_time", "stride_world_ticks_per_study_tick",
                                                                          "study_tick_time", "config", "theta")}
            m[f"sim_{h}"]["source"] = src(f"sim_{h}.json", "*")
    p = os.path.join(R, w, "train_done.json")
    if os.path.exists(p):
        m["train_done"] = dict(json.load(open(p)), source=src("train_done.json", "*"))
    p = os.path.join(R, f"pilot_{w}.json")
    if os.path.exists(p):
        pj = json.load(open(p))
        m["cpu_pilot"] = {k: pj.get(k) for k in ("J", "T", "burn", "designer_seed", "tick_time", "lags_world_ticks", "block_autocorr",
                                                 "member_ticks", "seconds", "platform")}
        m["cpu_pilot"]["source"] = f"results/pilot_{w}.json (cpilot.py, CPU; a designer seed never reused)"
    out["meta"]["worlds"][w] = m
    W = {"hand": {}, "configs": {}, "matched_effective_dimension": {}, "hand_block_designs_by_ceiling16": a["hand_block_designs_by_ceiling16"],
         "hand_families_PR": a["families_PR"]}
    for k, r in a["hand"].items():
        W["hand"][k] = dict(r, source=src("combined.json", f"hand.{k}"))
    for k, r in a["configs"].items():
        W["configs"][k] = dict(r, source=src("combined.json", f"configs.{k}") + " (identification: analysis:configs." + k + ")")
    for k, r in a["matched"].items():
        W["matched_effective_dimension"][k] = dict(r, source=f"analysis:{w}.matched.{k} (from " + src("combined.json", "hand.*, configs." + k) + ")")
    p = os.path.join(R, w, "closed_forms.json")
    if os.path.exists(p):
        cf = json.load(open(p))
        W["closed_forms"] = {h: {tag: {kk: (r4(cf[h][tag][kk]) if kk not in ("features", "autocorr_by_lag", "feature_autocorr_by_lag") else cf[h][tag][kk])
                                       for kk in cf[h][tag] if kk != "idx"} for tag in ("sfa", "sfax", "pca")} for h in cf}
        W["closed_forms"]["source"] = src("closed_forms.json", "<fit half>.<sfa|sfax|pca>")
    out["worlds"][w] = W
p = os.path.join(R, "interpretation.json")
if os.path.exists(p):
    out["claims"] = json.load(open(p))
json.dump(out, open(os.path.join(R, "summary.json"), "w"), indent=1)
print("summary.json:", {w: (len(v["configs"]), len(v["hand"])) for w, v in out["worlds"].items()}, len(out["claims"]), "claims; billed",
      out["meta"]["billed_usd_total"])
