"""Q2 difficulty check: re-read the round-4 sbi summary (no simulation) and split the
identification headroom by exam cell, estimate the interaction a data-only learner needs to
match the simulate-to-train learner at 2 episodes, and the information gained about theta."""
import json, math, os
S = "/home/user/physim/research/alife/vecworld/program/round4/sbi/results/summary.json"
d = json.load(open(S))
pc, oes = d["prediction"]["oes_per_cell"], d["prediction"]["oes"]
cells = d["prediction"]["cells"]
out = {"source": S, "cells_level_horizon": cells}
for fam in ("amort", "net", "ridge"):
    t, pp, pm = pc[f"{fam}|true"], pc[f"{fam}|prior_pred"], pc[f"{fam}|prior_mean"]
    g_pp = [a - b for a, b in zip(t, pp)]
    g_pm = [a - b for a, b in zip(t, pm)]
    l2 = [i for i, c in enumerate(cells) if c[0] == 2]
    out[fam] = {
        "true_minus_prior_pred_per_cell": [round(x, 4) for x in g_pp],
        "true_minus_prior_mean_per_cell": [round(x, 4) for x in g_pm],
        "aggregate_true_minus_prior_pred": round(sum(g_pp) / len(g_pp), 4),
        "aggregate_true_minus_prior_mean": round(sum(g_pm) / len(g_pm), 4),
        "level2_share_of_true_minus_prior_pred": round(sum(g_pp[i] for i in l2) / sum(g_pp), 3),
        "level2_share_of_true_minus_prior_mean": round(sum(g_pm[i] for i in l2) / sum(g_pm), 3),
        "level1_h_le_4_max_true_minus_prior_pred": round(max(g_pp[:3]), 4),
        "true_ceiling_per_cell": t,
    }
# data-only episodes needed to match the simulate-to-train learner at 2 episodes (log-linear interpolation)
bud = [2, 8, 32, 128, 512]
for fam in ("net", "ridge"):
    target = oes[f"{fam}|post@2"]["mean"]
    real = [oes[f"{fam}|real@{b}"]["mean"] for b in bud]
    need = None
    for i in range(len(bud) - 1):
        if real[i] < target <= real[i + 1]:
            f = (target - real[i]) / (real[i + 1] - real[i])
            need = math.exp(math.log(bud[i]) + f * (math.log(bud[i + 1]) - math.log(bud[i])))
    p0 = oes[f"{fam}|prior_pred"]["mean"]
    need0 = None
    for i in range(len(bud) - 1):
        if real[i] < p0 <= real[i + 1]:
            f0 = (p0 - real[i]) / (real[i + 1] - real[i])
            need0 = math.exp(math.log(bud[i]) + f0 * (math.log(bud[i + 1]) - math.log(bud[i])))
    out[f"{fam}_data_only_episodes_to_reach_prior_predictive_training"] = need0
    out[f"{fam}_value_of_theory"] = {
        "target_oes_post_at_2": target, "real_by_budget": dict(zip(bud, real)),
        "prior_pred_no_interaction": oes[f"{fam}|prior_pred"]["mean"],
        "data_only_episodes_to_match": need if need else f"> {bud[-1]} (real@512 {real[-1]} < target)",
        "ratio_to_2_episodes": (need / 2) if need else f"> {bud[-1] // 2}",
    }
# information about theta from marginal contraction (a lower bound on the Gaussian information gain)
pb = d["identification"]["per_budget"]
info = {}
for b in ("2", "8", "32", "128", "512"):
    r = pb[b]["contraction_sd_ratio_mean"]
    info[b] = {"ticks": pb[b]["ticks"], "charged_nats": round(pb[b]["nats_mean_over_truths"], 1),
               "sum_minus_log_sd_ratio_nats": round(-sum(math.log(x) for x in r), 2),
               "predicted_residual_headroom_fraction_mean_r2": round(sum(x * x for x in r) / len(r), 3)}
out["theta_information"] = info
print(json.dumps(out, indent=1))
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "q2_sbi_split.json"), "w"), indent=1)
