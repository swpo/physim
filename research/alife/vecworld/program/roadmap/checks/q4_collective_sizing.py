"""Q4 sizing checks (closed form / quadrature, CPU-seconds, no simulation).

(a) Wilson 95% intervals for 'k of n planted defects caught': how many canaries a pilot needs before an
    auditor catch rate means anything.
(b) Selection inflation E[max of N iid N(0,1)]: how far the best of N candidates sits above its true value,
    in standard errors, when the selector and the certifier share data.
(c) Exam resolution: OES standard errors measured in round4/sbi (512 pooled items, 8 truths), rescaled to a
    64-item single-instance exam, and the apparent gain from keeping the best of k graded submissions.
Inputs for (c) are read from the committed summary; nothing is re-simulated.
"""
import json
import math
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "q4_collective_sizing.json")
SBI = "/home/user/physim/research/alife/vecworld/program/round4/sbi/results/summary.json"


def wilson(k, n, z=1.959964):
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(c - h, 3), round(c + h, 3)]


def phi(x):
    return math.exp(-0.5 * x * x) / math.sqrt(2 * math.pi)


def Phi(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def emax(n, lo=-10.0, hi=10.0, m=40001):
    # E[max] = integral x * n * phi(x) * Phi(x)^(n-1) dx (trapezoid)
    h = (hi - lo) / (m - 1)
    s = 0.0
    for i in range(m):
        x = lo + i * h
        w = 0.5 if i in (0, m - 1) else 1.0
        s += w * x * n * phi(x) * Phi(x) ** (n - 1)
    return s * h


res = {}
res["a_wilson95_caught_of_planted"] = {
    f"{k}/{n}": wilson(k, n) for n, ks in {8: (6, 7, 8), 12: (9, 10, 11, 12), 16: (12, 14, 16), 20: (15, 17, 20),
                                           30: (24, 27)}.items() for k in ks}
# the collective's inside-review record, for scale: 7 Contradicted of 877 verdicts (summary_final.md section 6)
res["a_collective_contradicted_share"] = {"7/877": wilson(7, 877)}
res["a_false_reject_of_clean_controls"] = {f"{k}/{n}": wilson(k, n) for n, k in ((6, 0), (6, 1), (8, 1))}

res["b_expected_max_in_se"] = {str(n): round(emax(n), 3) for n in (2, 3, 5, 10, 20, 80, 166, 1000)}

j = json.load(open(SBI))
oes = j["prediction"]["oes"]
# competitive predictors only: simulate-to-train at the truth, the posterior or the prior predictive
comp = lambda name: ("real@" not in name) and ("prior_mean" not in name) and name not in ("climatology", "oracle")
se512 = sorted(v["se"] for k, v in oes.items() if isinstance(v, dict) and "se" in v and comp(k))
gaps = j["prediction"]["gaps"]
gse512 = sorted(v["se"] for k, v in gaps.items() if isinstance(v, dict) and comp(k))
tc = j["checker"]["truth_clustered_gaps"]
ratio = sorted(round(v["z_items"] / v["z_cluster"], 2) for k, v in tc.items()
               if isinstance(v, dict) and v.get("z_cluster") and comp(k))
sc = math.sqrt(512 / 64)
res["c_exam_resolution"] = {
    "oes_se_512_items_range": [se512[0], se512[-1]],
    "oes_se_64_items_range": [round(se512[0] * sc, 4), round(se512[-1] * sc, 4)],
    "paired_gap_keys": sorted(k for k in gaps if comp(k)),
    "paired_gap_se_512_items_range": [gse512[0], gse512[-1]],
    "paired_gap_se_64_items_range": [round(gse512[0] * sc, 4), round(gse512[-1] * sc, 4)],
    "item_z_over_truth_cluster_z_range": [ratio[0], ratio[-1]],
    "inference_step_gliders_net": j["prediction"]["extra_gaps"]["net|true - net|prior_pred"]["gap"],
    "best_of_k_apparent_paired_gain_64_items": {
        str(k): [round(emax(k) * gse512[0] * sc, 4), round(emax(k) * gse512[-1] * sc, 4)] for k in (2, 5, 10, 20)},
    "note": "best-of-k assumes k equally good submissions with independent paired-gap errors: an upper bound for "
            "correlated submissions; item-level SEs understate truth-clustered ones by the ratio above",
}
json.dump(res, open(OUT, "w"), indent=1)
print(json.dumps(res, indent=1))
