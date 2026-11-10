"""ssummary -- results/summary.json of the round-5 study `slots` (local; every number with its source).

usage: python -B ssummary.py RESULTS_DIR JOB_ID [PILOT_JOB_ID ...]
Reads RESULTS_DIR/<JOB_ID>/{combined.json, sim_A.json, sim_B.json, train_done.json, status.json} (copied from
origin/gpu-jobs:jobs/<JOB_ID>/out/ and the job's status.json), the same for the pilot jobs if given (job records
only), and RESULTS_DIR/interpretation.json (the hand-written reading: a list of {"claim", "refs"}; each ref is a key
path into the main job's combined.json, or {"mean": [paths]} for a mean over seeds / replicas). Writes
RESULTS_DIR/summary.json: job records (state, GPU, hours, billed cost), platform, sizes, one row per Phi and per
learned config (seed means with both seeds' sources), objective values, and the claims with their values resolved
from the source keys (so a claim cannot drift from its source).
Source strings: "<job>:out/<file>:<key path>" (the file on origin/gpu-jobs:jobs/<job>/out/; copies under results/).
"""
import json
import os
import re
import sys

import numpy as np

R, JOB = sys.argv[1], sys.argv[2]
PILOTS = sys.argv[3:]
C = json.load(open(os.path.join(R, JOB, "combined.json")))
src = lambda f, k: f"{JOB}:out/{f}:{k}"
HZ = C["horizons"]


def r4(v):
    if v is None:
        return None
    if isinstance(v, (list, tuple, np.ndarray)):
        return [r4(x) for x in v]
    if isinstance(v, (int, float, np.floating, np.integer)):
        return round(float(v), 4)
    return v


def get(path, tree=None):
    """Dotted key path with [i] indices; a key that contains dots is written in double quotes, e.g.
    phis."sam_set_s0@mp6".families.S.ceiling[0]."""
    cur = C if tree is None else tree
    for tok in re.findall(r'"[^"]+"|[^.\[\]]+|\[\d+\]', path):
        if tok.startswith("["):
            cur = cur[int(tok[1:-1])]
        else:
            cur = cur[tok.strip('"')]
    return cur


def job_record(job):
    p = os.path.join(R, job, "status.json")
    if not os.path.exists(p):
        return {"job_id": job, "note": "no status.json copied"}
    st = json.load(open(p))
    pods = st.get("pods") or ([st["pod"]] if st.get("pod") else [])
    rec = {"job_id": job, "state": st.get("state"), "exit_code": st.get("exit_code"), "message": st.get("message"),
           "cost": st.get("cost"), "cap_usd": st.get("cap_usd"),
           "pods": [{k: p_.get(k) for k in ("gpu", "gpu_type", "provider", "rate_usd_hr", "name", "spot") if k in p_} for p_ in pods],
           "source": f"origin/gpu-jobs:jobs/{job}/status.json (copy results/{job}/status.json)"}
    for k in ("started_at", "finished_at", "pod_times", "pod_hours_created_to_terminated", "run_hours_started_to_finished",
              "billing_window_hours", "hours"):
        if k in st:
            rec[k] = st[k]
    return rec


out = {"what": "Round-5 study 'slots' (track 1): slot encoders with memory on raw Flow-Lenia gliders states; do objects "
               "emerge from an objective plus an object-centric architecture?",
       "jobs": {j: job_record(j) for j in [JOB] + PILOTS}, "main_job": JOB, "meta": {}, "phis": {}, "configs": {},
       "objective_values": {}, "claims": [], "review": None}
for h in ("A", "B"):
    p = os.path.join(R, JOB, f"sim_{h}.json")
    if os.path.exists(p):
        s = json.load(open(p))
        out["meta"][f"sim_{h}"] = dict({k: s[k] for k in ("designer_seed", "J_ALL", "J_CERT", "T", "test_ticks", "TB", "R_BR",
                                                          "member_ticks", "member_ticks_per_s", "platform", "seconds",
                                                          "tracker_pass_check", "objects", "mass_drift_max_rel") if k in s},
                                       source=src(f"sim_{h}.json", "*"))
p = os.path.join(R, JOB, "train_done.json")
if os.path.exists(p):
    out["meta"]["train_done"] = dict(json.load(open(p)), source=src("train_done.json", "*"))
out["meta"]["layout"] = C["layout"]
out["meta"]["horizons"] = HZ
out["meta"]["problems"] = C.get("problems")


def phi_row(phi, r):
    if not r["families"]:          # agreement only: the 12-number layout of a learned Phi was not certified
        row = {"q": r["q"], "layout": r["layout"], "family": None, "ceiling": None,
               "note": "not certified (S5_CERT_O=refs); ceilings on the 6-number sub-view " + phi + "@mp6",
               "source": src("combined.json", f'phis."{phi}"')}
    else:
        fam = "O" if "O" in r["families"] else ("S" if "S" in r["families"] else "GL")
        row = {"q": r["q"], "layout": r["layout"], "n_items": r["n_items"], "family": fam,
               "ceiling": r4(r["families"][fam]["ceiling"]), "ceiling_se": r4(r["families"][fam]["se"]),
               "best": r["families"][fam]["best"], "ceiling_G": r4(r["families"]["G"]["ceiling"]),
               "I_avail_logdet": r4(r["logdet"].get("I_avail")), "I_capt_logdet": r4(r["logdet"].get(f"I_capt_{fam}")),
               "I_avail_diag": r4(r.get("I_avail_diag")), "I_capt_diag": r4(r["families"][fam].get("I_capt_diag")),
               "source": src("combined.json", f'phis."{phi}"')}
    if "S" in r["families"] and row["family"] != "S":
        row["ceiling_S"] = r4(r["families"]["S"]["ceiling"])
    a = r.get("agreement")
    if a:
        row["agreement"] = {"ari": r4(a["ari_hard_matter_weighted"]), "recall": r4(a["recall"]), "precision": r4(a["precision"]),
                            "clean_match_rate": r4(a["clean_match_rate(recall,precision>=0.9)"]),
                            "slots_per_object": r4(a["slots_per_object"]), "objects_per_slot": r4(a["objects_per_slot"]),
                            "identity_persistence": r4(a["identity_persistence"]),
                            "direct": r4(a["direct"]), "probe_linear": r4(a.get("probe_linear")), "probe_rff": r4(a.get("probe_rff")),
                            "by_ticks_since_event": a["by_ticks_since_event"]}
    if r.get("territory"):
        row["territory"] = r4(r["territory"])
    if r.get("nontriv"):
        row["nontriv"] = r4(r["nontriv"])
    return row


for phi, r in C["phis"].items():
    out["phis"][phi] = phi_row(phi, r)


def seed_mean(phis, f):
    v = [f(out["phis"][p]) for p in phis if p in out["phis"]]
    v = [x for x in v if x is not None]
    if not v:
        return None
    return r4(np.mean(np.asarray(v, float), 0))


for name, c in C["configs"].items():
    ph = sorted(c["phis"])
    row = {"obj": c["obj"], "readout": c["readout"], "phis": ph, "n_seeds": len(ph),
           "ceiling": seed_mean(ph, lambda r: r.get("ceiling")), "ceiling_family": out["phis"][ph[0]].get("family"),
           "ceiling_seeds": [out["phis"][p].get("ceiling") for p in ph],
           "ari": seed_mean(ph, lambda r: r["agreement"]["ari"]), "recall": seed_mean(ph, lambda r: r["agreement"]["recall"]),
           "precision": seed_mean(ph, lambda r: r["agreement"]["precision"]),
           "slots_per_object": seed_mean(ph, lambda r: r["agreement"]["slots_per_object"]),
           "identity_persistence": seed_mean(ph, lambda r: r["agreement"]["identity_persistence"]),
           "direct_mass_R2": seed_mean(ph, lambda r: r["agreement"]["direct"]["mass_R2"]),
           "direct_pos_R2": seed_mean(ph, lambda r: r["agreement"]["direct"]["pos_R2"]),
           "direct_vel_R2": seed_mean(ph, lambda r: r["agreement"]["direct"]["vel_R2"]),
           "probe_rff_mass_R2": seed_mean(ph, lambda r: (r["agreement"]["probe_rff"] or {}).get("mass_R2")),
           "probe_rff_pos_R2": seed_mean(ph, lambda r: (r["agreement"]["probe_rff"] or {}).get("pos_R2")),
           "probe_rff_vel_R2": seed_mean(ph, lambda r: (r["agreement"]["probe_rff"] or {}).get("vel_R2")),
           "territory_resultant_length": seed_mean(ph, lambda r: (r.get("territory") or {}).get("resultant_length")),
           "seed_pair": r4(c.get("seed_pair")), "ari_vs_km_s6": r4(c.get("ari_vs_km_s6")),
           "val_best": r4(c.get("val_best")), "best_step": c.get("best_step"), "moved_from_kmeans": r4(c.get("moved_from_kmeans")),
           "skipped_steps": c.get("skipped_steps"),
           "source": [src("combined.json", f"configs.{name}")] + [src("combined.json", f'phis."{p}"') for p in ph]}
    sub = [p + "@mp6" for p in ph if p + "@mp6" in out["phis"]]
    if sub:
        row["ceiling_mp6_S"] = seed_mean(sub, lambda r: r["ceiling"])
        row["ceiling_mp6_S_se"] = seed_mean(sub, lambda r: r["ceiling_se"])
        row["I_capt_diag_mp6_S"] = seed_mean(sub, lambda r: r["I_capt_diag"])
        row["I_avail_diag_mp6"] = seed_mean(sub, lambda r: r["I_avail_diag"])
    tp = os.path.join(R, JOB, "train", f"{name}.json")
    if os.path.exists(tp):         # training record: steps, checkpoints, and the masks' agreement with the tracker along training
        tj = json.load(open(tp))
        hist = tj["hist"]
        row["training"] = {"steps_done": hist[-1]["step"], "checkpoints": tj.get("checkpoints"),
                           "cut_by_deadline": tj.get("cut_by_deadline"),
                           "replicas": [f'{i["fit"]}{i["seed"]}' for i in tj["infos"]],
                           "best_step": [i["best_step"] for i in tj["infos"]],
                           "val_by_step": {str(h["step"]): r4(h["val"]) for h in hist if h["step"] % 500 == 0 or h is hist[-1]},
                           "source": src(f"train/{name}.json", "hist, infos")}
        if "val_trk_recall_purity" in hist[0]:
            rp = lambda h: r4(np.asarray(h["val_trk_recall_purity"], float).sum(1))
            row["training"]["val_tracker_recall_plus_purity_by_step"] = {
                str(h["step"]): rp(h) for h in hist if h["step"] % 500 == 0 or h is hist[-1]}
    out["configs"][name] = row
for nm, o in C.get("objval", {}).items():
    out["objective_values"][nm] = {k: {"mean": r4(np.mean(o[k]["val"])), "replicas": r4(o[k]["val"]),
                                       "per_horizon_mean": r4(np.mean(o[k]["val_h"], 0)) if k != "rec" else None}
                                   for k in ("set", "self", "rec") if o.get(k)}
    for k in ("set", "self"):          # the dead-direction term of the frozen readout and the guarded value
        if o.get(k) and o[k].get("dead_pen") is not None:
            out["objective_values"][nm][k]["dead_pen"] = r4(np.mean(o[k]["dead_pen"]))
            out["objective_values"][nm][k]["mean_guarded"] = r4(np.mean(o[k]["val"]) + np.mean(o[k]["dead_pen"]))
    out["objective_values"][nm]["source"] = src(f"objval/{nm}.json", "*") + " (also combined.json:objval." + nm + ")"
p = os.path.join(R, "review.json")
if os.path.exists(p):                  # the code review of the job and what was fixed
    out["review"] = json.load(open(p))
p = os.path.join(R, "interpretation.json")
if os.path.exists(p):
    for cl in json.load(open(p)):
        vals, srcs = {}, {}
        for label, ref in cl.get("refs", {}).items():
            if isinstance(ref, dict) and "mean" in ref:
                vals[label] = r4(np.mean(np.asarray([get(q) for q in ref["mean"]], float), 0))
                srcs[label] = "mean of " + "; ".join(src("combined.json", q) for q in ref["mean"])
            else:
                vals[label] = r4(get(ref))
                srcs[label] = src("combined.json", ref)
        out["claims"].append({"claim": cl["claim"], "values": vals, "sources": srcs})
json.dump(out, open(os.path.join(R, "summary.json"), "w"), indent=1)
print("summary.json:", len(out["phis"]), "phis,", len(out["configs"]), "configs,", len(out["objective_values"]),
      "objective-value rows,", len(out["claims"]), "claims; jobs", {j: (v.get("state"), (v.get("cost") or {}).get("billed_usd")) for j, v in out["jobs"].items()})
