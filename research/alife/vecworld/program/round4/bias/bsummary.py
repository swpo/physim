"""bsummary -- results/summary.json of the round-4 study `bias` (local; every number with its source).

usage: python -B bsummary.py JOB_ID RESULTS_DIR
Reads RESULTS_DIR/{combined.json, sim_A.json, sim_B.json, train_done.json, status.json, interpretation.json}
(copied from origin/gpu-jobs:jobs/<JOB_ID>/out/ and the job's status.json) and writes RESULTS_DIR/summary.json:
meta (sizes, platform, cost), per-config rows (seed means), hand designs, linear-window statistics (mean over the
four replicas), and the hand-written reading (interpretation.json) with each claim's source keys.
"""
import json
import os
import sys

import numpy as np

JOB, R = sys.argv[1], sys.argv[2]
C = json.load(open(os.path.join(R, "combined.json")))
src = lambda f, k: f"{JOB}:out/{f}:{k}"
r3 = lambda v: None if v is None else (np.round(np.asarray(v, float), 4).tolist() if np.ndim(v) else round(float(v), 4))
out = {"meta": {}, "configs": {}, "hand": {}, "windows": {}, "claims": []}
st = json.load(open(os.path.join(R, "status.json")))
out["meta"]["job"] = {"job_id": JOB, "state": st.get("state"), "gpu": (st.get("pod") or {}).get("gpu"), "provider": (st.get("pod") or {}).get("provider"),
                      "cost": st.get("cost"), "source": f"origin/gpu-jobs:jobs/{JOB}/status.json"}
for k in ("pod", "rate_usd_per_h", "started_at", "finished_at", "billing_window_hours"):
    if k in st:
        out["meta"]["job"][k] = st[k]
for h in ("A", "B"):
    p = os.path.join(R, f"sim_{h}.json")
    if os.path.exists(p):
        s = json.load(open(p))
        out["meta"][f"sim_{h}"] = {k: s[k] for k in ("designer_seed", "J_ALL", "J_CERT", "T", "test_ticks", "TB", "R_BR",
                                                      "member_ticks", "member_ticks_per_s", "platform", "mass_drift_max_rel")}
        out["meta"][f"sim_{h}"]["source"] = src(f"sim_{h}.json", "*")
p = os.path.join(R, "train_done.json")
if os.path.exists(p):
    out["meta"]["train_done"] = dict(json.load(open(p)), source=src("train_done.json", "*"))
out["meta"]["layout"] = C["layout"]
out["meta"]["horizons"] = C["horizons"]
for nm, r in C["configs"].items():
    row = {k: r[k] for k in ("enc", "h", "obj", "c", "n_seeds")}
    for k in ("ceiling_G", "ceiling_G_se_mean", "ceiling_G_seed_diff", "ceiling_GL", "I_capt", "tau_half_G"):
        if k in r:
            row[k] = r3(r[k])
    row["r_dyn"] = r3(r["nontriv"]["r_dyn"])
    row["participation_ratio"] = r3(r["nontriv"]["participation_ratio"])
    row["agreement"] = {k: {d: r3(v) for d, v in a.items()} for k, a in r["agreement"].items()}
    row["seed_R2"] = r3(r["seed_agreement"].get("mean"))
    row["source"] = src("combined.json", f"configs.{nm}")
    out["configs"][nm] = row
for k, r in C["hand"].items():
    out["hand"][k] = {"ceiling_G": r3(r["G"]["ceiling"]), "se": r3(r["G"]["se"]), "ceiling_GL": r3(r["GL"]["ceiling"]) if "GL" in r else None,
                      "I_capt": r3(r["logdet"]["I_capt"]), "r_dyn": r3(r["nontriv"]["r_dyn"]),
                      "agreement": {kk: {d: r3(v) for d, v in a.items()} for kk, a in r["agreement"].items()},
                      "source": src("combined.json", f"hand.{k}")}
groups = {}
for key, w in C["windows"].items():
    if "per_channel" not in w:
        continue
    cfg = key.rsplit("_s", 1)[0]
    groups.setdefault(cfg, []).append(w)
for cfg, ws in groups.items():
    pc = [w["per_channel"][0] for w in ws]
    g = {"n_replicas": len(ws)}
    for k in ("cos_block_mass", "cos_tent", "cos_block_c0", "cos_block_c1", "share_abs_in_block", "channel_balance_c0"):
        v = [p[k] for p in pc if p.get(k) is not None]
        g[k] = {"mean": r3(np.mean(v)), "min": r3(np.min(v)), "max": r3(np.max(v))} if v else None
    for k in ("span_alignment_block_mass", "span_alignment_block_channels", "span_alignment_tent"):
        v = [w[k] for w in ws]
        g[k] = {"mean": r3(np.mean(v)), "min": r3(np.min(v)), "max": r3(np.max(v))}
    g["source"] = src("combined.json", f"windows.{cfg}_s*__fit*")
    out["windows"][cfg] = g
p = os.path.join(R, "interpretation.json")
if os.path.exists(p):
    out["claims"] = json.load(open(p))
json.dump(out, open(os.path.join(R, "summary.json"), "w"), indent=1)
print("summary.json:", len(out["configs"]), "configs,", len(out["hand"]), "hand,", len(out["windows"]), "window groups,",
      len(out["claims"]), "claims")
