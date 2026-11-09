"""Second-reader check: how many hidden worlds does it take to separate two solvers on the gliders pilot,
and how much level-0 simulation fits in the sandbox EXAM.md section 5 proposes?
Reads only round4/sbi/results/summary.json (per-truth aggregate OES); no simulation."""
import json, itertools, math
import numpy as np
P = "/home/user/physim/research/alife/vecworld/program/round4/sbi/results/summary.json"
d = json.load(open(P))
pt = d["prediction"]["per_truth_aggregate"]
truths = sorted(pt, key=int)
names = [k for k in pt[truths[0]] if k not in ("climatology", "oracle")]
M = {n: np.array([pt[t][n] for t in truths]) for n in names}
pairs = {
    "amort|post@8 - net|post@8": ("amort|post@8", "net|post@8"),
    "net|post@8 - ridge|post@8": ("net|post@8", "ridge|post@8"),
    "net|post@8 - net|prior_pred": ("net|post@8", "net|prior_pred"),
    "net|true - net|prior_mean": ("net|true", "net|prior_mean"),
    "net|post@8 - net|real@128": ("net|post@8", "net|real@128"),
    "net|real@512 - net|real@128": ("net|real@512", "net|real@128"),
    "ridge|real@128 - ridge|real@32": ("ridge|real@128", "ridge|real@32"),
}
out = {"source": P, "n_truths": len(truths), "pairs": {}}
for k, (a, b) in pairs.items():
    diff = M[a] - M[b]
    sd = float(diff.std(ddof=1))
    out["pairs"][k] = {"mean_gap": round(float(diff.mean()), 4), "sd_across_truths": round(sd, 4),
                       "truths_for_z3_at_gap_0.03": math.ceil((3 * sd / 0.03) ** 2),
                       "truths_for_z3_at_gap_0.05": math.ceil((3 * sd / 0.05) ** 2)}
sds = [v["sd_across_truths"] for v in out["pairs"].values()]
out["sd_range"] = [min(sds), max(sds)]
# sandbox arithmetic, EXAM.md section 5: 4 CPU cores, 24 h, 0.136 s per member-tick; optional one GPU for 8 h
cpu_mt = 4 * 24 * 3600 / 0.136
gpu_mt = 8 * 3600 * 1600
mt = d["job"]["member_ticks"]
out["sandbox"] = {"cpu_only_member_ticks_24h_4cores": round(cpu_mt), "gpu_8h_member_ticks_at_1600_per_s": gpu_mt,
                  "sbi_pilot_total_member_ticks": d["job"]["member_ticks_total"],
                  "sbi_design_plus_one_posterior_set": mt["design"] + mt["sims_post2"],
                  "gpu_8h_cost_usd_at_1.99_2.35": [round(8 * 1.99, 2), round(8 * 2.35, 2)],
                  "q4_12_rollouts_gpu_usd": [round(12 * 8 * 1.99), round(12 * 8 * 2.35)]}
json.dump(out, open(__file__.replace(".py", ".json"), "w"), indent=1)
print(json.dumps(out, indent=1))
