"""se_check.py -- what standard errors can the round-6 dial designs expect? (crit_stats, round 6; CPU, about 1 minute)

Reads only saved round-5 outputs (pilot data, PILOT_NEVER_REUSE_AS_EXAM; no hidden value is written out):
    round5/ladder/results/job/n{1,4,8}/scores.npz   per-item fair energy scores, 8 truths x 48 items x 5 horizons
and writes results/se_check.json. Nothing is simulated or trained.

For each of the nine ladder cells (view x number of hidden parameters):
  A. sigma = (L(P0) - L(C)) / (L(K) - L(C)) pooled over items (acceptance.py's definition, null = P0), the per-world
     influence values psi_w = (num_w - sigma * den_w) / mean(den) (delta method: SE(sigma) = SD(psi_w) / sqrt(n)),
     the share of Var(psi_w) that is item noise at 48 items per world, and the same on the two "input" classes c, d.
  B. what four truths give: sigma on each of the 70 subsets of 4 of the 8 worlds, and the cluster-bootstrap SE
     computed inside each subset against the delta-method SD(psi) / sqrt(4).
  C. rho at two Lab episodes = (L(P0) - L(S@2)) / (L(P0) - L(C)) with its influence SD, and the bar as a linear
     contrast: rho <= 0.7  <=>  mean_w[L(S) - 0.3 L(P0) - 0.7 L(C)] >= 0, t over worlds.
Then, for per-world SDs spanning round 5 (0.085 to 0.17 = the 0.03 to 0.06 seen at eight truths, times sqrt 8) and a
heavier-tailed case, the operating characteristics of three decision rules at n truths (Monte Carlo, normal and
lognormal-mixture per-world values): point estimate >= 0.15; lower one-sided 90% t bound >= 0.15; upper bound < 0.15.

Run:  OMP_NUM_THREADS=1 nice -n 10 python -B se_check.py   (from this folder)
"""
import itertools
import json
import os

import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
R5 = os.path.normpath(os.path.join(HERE, "..", "..", "..", "round5", "ladder", "results"))
VIEWS = ["block", "object", "pop"]


def load(nh):
    z = np.load(os.path.join(R5, "job", f"n{nh}", "scores.npz"))
    summ = json.load(open(os.path.join(R5, "summary.json")))
    out = {}
    for view in VIEWS:
        valid = np.asarray(summ["cells"][f"n{nh}|{view}"]["valid_cells"], bool)
        pol = {}
        for name in ["K", "C", "P0", "S@2", "S@8", "O"]:
            pol[name] = np.stack([z[f"t{t}|{view}|{name}"][:, valid].sum(1) for t in range(8)])  # (8 worlds, 48 items)
        out[view] = pol
    classes = np.stack([z[f"t{t}|classes"] for t in range(8)])
    return out, classes


def sigma_of(P, mask=None):
    """pooled sigma and per-world influence values; P[name] is (worlds, items); mask selects items."""
    def wm(a):
        if mask is None:
            return a.mean(1)
        return np.array([a[w][mask[w]].mean() for w in range(a.shape[0])])
    num_w = wm(P["P0"] - P["C"])
    den_w = wm(P["K"] - P["C"])
    s = num_w.mean() / den_w.mean()
    psi = (num_w - s * den_w) / den_w.mean()
    return float(s), psi, num_w / den_w


def item_noise_share(P, s):
    """share of Var(psi_w) explained by item sampling at the given items per world (one-way components)."""
    den = (P["K"] - P["C"]).mean()
    psi_i = ((P["P0"] - P["C"]) - s * (P["K"] - P["C"])) / den  # (worlds, items)
    n_items = psi_i.shape[1]
    within = psi_i.var(axis=1, ddof=1).mean() / n_items
    total = psi_i.mean(1).var(ddof=1)
    return float(min(1.0, within / total)), float(np.sqrt(within)), float(np.sqrt(max(total - within, 0.0)))


def boot_se(P, idx, rng, n_boot=400):
    k = len(idx)
    draws = rng.integers(0, k, size=(n_boot, k))
    num = (P["P0"] - P["C"]).mean(1)[idx]
    den = (P["K"] - P["C"]).mean(1)[idx]
    return float((num[draws].mean(1) / den[draws].mean(1)).std(ddof=1))


def rho_of(P, key="S@2"):
    a_w = (P["P0"] - P[key]).mean(1)
    b_w = (P["P0"] - P["C"]).mean(1)
    r = a_w.mean() / b_w.mean()
    psi = (a_w - r * b_w) / b_w.mean()
    con = (P[key] - 0.3 * P["P0"] - 0.7 * P["C"]).mean(1)  # >= 0 iff rho <= 0.7 (when P0 - C > 0)
    t = con.mean() / (con.std(ddof=1) / np.sqrt(len(con)))
    den_t = b_w.mean() / (b_w.std(ddof=1) / np.sqrt(len(b_w)))
    return float(r), psi, float(t), float(den_t)


def oc(true_sigma, sd, n, rng, heavy=False, n_mc=40000):
    """operating characteristics of three rules for n per-world values with mean true_sigma and SD sd."""
    if heavy:  # 80% of worlds near zero effect, 20% carry the mean (as vortex pilot B); same mean and SD
        p = 0.2
        hi = true_sigma + sd * np.sqrt((1 - p) / p)
        lo = true_sigma - sd * np.sqrt(p / (1 - p))
        x = np.where(rng.random((n_mc, n)) < p, hi, lo) + 0.02 * rng.standard_normal((n_mc, n))
    else:
        x = true_sigma + sd * rng.standard_normal((n_mc, n))
    m = x.mean(1)
    se = x.std(1, ddof=1) / np.sqrt(n)
    tq = stats.t.ppf(0.90, n - 1)
    return {"P_point_ge_0.15": float((m >= 0.15).mean()),
            "P_lower90_ge_0.15": float((m - tq * se >= 0.15).mean()),
            "P_upper90_lt_0.15": float((m + tq * se < 0.15).mean())}


def main():
    rng = np.random.default_rng(20261111)
    out = {"what": "expected standard errors for the round-6 dial designs, from round-5 ladder per-item scores",
           "PILOT_NEVER_REUSE_AS_EXAM": True,
           "source": "round5/ladder/results/job/n{1,4,8}/scores.npz; command: python -B se_check.py",
           "cells": {}}
    for nh in (1, 4, 8):
        data, classes = load(nh)
        for view in VIEWS:
            P = data[view]
            s, psi, per_world = sigma_of(P)
            sd = float(psi.std(ddof=1))
            share, sd_item_part, sd_world_part = item_noise_share(P, s)
            mask = np.isin(classes, ["c", "d"])
            s_cd, psi_cd, _ = sigma_of(P, mask)
            subs = list(itertools.combinations(range(8), 4))
            est4 = np.array([sigma_of({k: v[list(c)] for k, v in P.items()})[0] for c in subs])
            bse4 = np.array([boot_se(P, np.array(c), rng) for c in subs])
            dse4 = np.array([sigma_of({k: v[list(c)] for k, v in P.items()})[1].std(ddof=1) / 2.0 for c in subs])
            r, rpsi, t_con, den_t = rho_of(P)
            out["cells"][f"n{nh}|{view}"] = {
                "sigma_P0_null": s,
                "per_world_sigma_min_median_max": [float(per_world.min()), float(np.median(per_world)), float(per_world.max())],
                "sd_world_influence": sd,
                "se_8_worlds": sd / np.sqrt(8),
                "cv_per_world": sd / abs(s) if abs(s) > 1e-9 else None,
                "item_noise_share_of_world_variance_at_48_items": share,
                "sd_parts_item_noise_and_between_world": [sd_item_part, sd_world_part],
                "input_classes_c_d_24_items": {"sigma": s_cd, "sd_world_influence": float(psi_cd.std(ddof=1))},
                "four_of_eight_truths": {
                    "sigma_min_max_over_70_subsets": [float(est4.min()), float(est4.max())],
                    "sd_of_subset_estimates": float(est4.std(ddof=0)),
                    "cluster_bootstrap_se_median": float(np.median(bse4)),
                    "delta_se_median": float(np.median(dse4)),
                    "bootstrap_over_delta_se_median_ratio": float(np.median(bse4 / dse4)),
                    "note": "bootstrap of 4 clusters uses SD with divisor n: expected ratio sqrt(3/4) = 0.87",
                },
                "rho_at_2_episodes": {"rho": r, "sd_world_influence": float(rpsi.std(ddof=1)),
                                      "se_8_worlds": float(rpsi.std(ddof=1) / np.sqrt(8)),
                                      "t_contrast_rho_le_0.7_7df": t_con,
                                      "t_of_denominator_P0_minus_C_7df": den_t},
            }
    sds = [c["sd_world_influence"] for c in out["cells"].values()]
    out["sd_world_influence_range_over_nine_cells"] = [min(sds), max(sds)]
    # expected SE of sigma at n truths for per-world SDs spanning round 5
    span = {"round5_block_object_max": max(c["sd_world_influence"] for k, c in out["cells"].items() if "pop" not in k),
            "0.03_at_8_truths": 0.03 * np.sqrt(8), "0.06_at_8_truths": 0.06 * np.sqrt(8),
            "vortex_B_short_history_0.157_at_10_truths": 0.157 * np.sqrt(10)}
    ns = [4, 8, 10, 12, 16, 24, 32]
    out["expected_se_of_sigma"] = {k: {"sd_world": float(v), **{f"n{n}": float(v / np.sqrt(n)) for n in ns}}
                                   for k, v in span.items()}
    # smallest n at which a true sigma is separated from the bar by the one-sided 90% t bound with probability 0.8
    need = {}
    for label, sd in [("sd0.085", 0.03 * np.sqrt(8)), ("sd0.17", 0.06 * np.sqrt(8))]:
        need[label] = {}
        for true in (0.0, 0.05, 0.25, 0.30):
            key = "P_upper90_lt_0.15" if true < 0.15 else "P_lower90_ge_0.15"
            got = None
            for n in (3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 48):
                if oc(true, sd, n, rng, n_mc=20000)[key] >= 0.8:
                    got = n
                    break
            need[label][f"true_{true}"] = got
    out["smallest_n_for_power_0.8_one_sided_90pct_t_bound"] = need
    table = {}
    for label, sd, heavy in [("normal_sd0.085", 0.03 * np.sqrt(8), False), ("normal_sd0.17", 0.06 * np.sqrt(8), False),
                             ("tail_worlds_sd0.17", 0.06 * np.sqrt(8), True)]:
        table[label] = {}
        for n in (4, 8, 12, 16, 24):
            table[label][f"n{n}"] = {f"true_{t}": oc(t, sd, n, rng, heavy) for t in (0.0, 0.10, 0.15, 0.20, 0.30)}
    out["decision_rules_operating_characteristics"] = table
    # per design: expected SE and the band around the bar inside which the design cannot decide (power < 0.8 for
    # the one-sided 90% t bound; noncentral t). The seed term is an estimate from ONE round-5 pair: vortex pilot
    # A's sigma was -0.003 on the pod and 0.045 on a CPU retraining (round5/vortexexam summary, checker finding
    # 11), i.e. an SD of |0.048| / sqrt 2 = 0.034 per training; C and P0 are single nets shared by all truths, so
    # this term does not shrink with the number of truths.
    sd_seed = abs(0.045 - (-0.003)) / np.sqrt(2)

    def band(n, sd):
        tq = stats.t.ppf(0.90, n - 1)
        lo, hi = 0.0, 2.0
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            if stats.nct.sf(tq, n - 1, mid * np.sqrt(n) / sd) >= 0.8:
                hi = mid
            else:
                lo = mid
        return float(hi)

    rho_sd = sorted(c["rho_at_2_episodes"]["sd_world_influence"] for k, c in out["cells"].items() if k != "n8|object")
    designs = {}
    for name, n, seeds in [("defect_gliders_stage1_4_truths", 4, 2), ("defect_gliders_8_truths", 8, 2),
                           ("defect_gliders_8_truths_3_seeds", 8, 3), ("sublevel_second_12_truths", 12, 2),
                           ("sublevel_second_16_truths_3_seeds", 16, 3), ("compute_limit_10_truths_ridge", 10, 0),
                           ("any_16_truths_3_seeds", 16, 3), ("any_24_truths_3_seeds", 24, 3)]:
        row = {"n_truths": n, "n_seeds": seeds, "t_0.90_one_sided": float(stats.t.ppf(0.90, n - 1))}
        for label, sd in [("sd0.085", 0.03 * np.sqrt(8)), ("sd0.17", 0.06 * np.sqrt(8))]:
            se_w = sd / np.sqrt(n)
            se_s = sd_seed / np.sqrt(seeds) if seeds else 0.0
            row[label] = {"se_worlds": float(se_w), "se_seed": float(se_s), "se_total": float(np.hypot(se_w, se_s)),
                          "undecided_within_plus_minus_of_bar_worlds_only": band(n, sd)}
        row["rho_se_from_round5_spread_min_max"] = [float(rho_sd[0] / np.sqrt(n)), float(rho_sd[-1] / np.sqrt(n))]
        designs[name] = row
    out["sd_seed_estimate_one_pair"] = float(sd_seed)
    out["design_expectations"] = designs
    os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
    with open(os.path.join(HERE, "results", "se_check.json"), "w") as f:
        json.dump(out, f, indent=1)
    for k, c in out["cells"].items():
        f4 = c["four_of_eight_truths"]
        print(f"{k:10s} sigma {c['sigma_P0_null']:+.4f} sd_w {c['sd_world_influence']:.4f} se8 {c['se_8_worlds']:.4f} "
              f"item-noise share {c['item_noise_share_of_world_variance_at_48_items']:.2f} | cd: {c['input_classes_c_d_24_items']['sigma']:+.4f} "
              f"sd {c['input_classes_c_d_24_items']['sd_world_influence']:.4f} | 4 of 8: [{f4['sigma_min_max_over_70_subsets'][0]:+.3f}, "
              f"{f4['sigma_min_max_over_70_subsets'][1]:+.3f}] boot/delta {f4['bootstrap_over_delta_se_median_ratio']:.2f} | "
              f"rho2 {c['rho_at_2_episodes']['rho']:+.2f} se8 {c['rho_at_2_episodes']['se_8_worlds']:.2f} "
              f"t_con {c['rho_at_2_episodes']['t_contrast_rho_le_0.7_7df']:+.1f} t_den {c['rho_at_2_episodes']['t_of_denominator_P0_minus_C_7df']:+.1f}")
    print(json.dumps(out["expected_se_of_sigma"], indent=1))
    print(json.dumps(out["smallest_n_for_power_0.8_one_sided_90pct_t_bound"], indent=1))
    for label, tab in table.items():
        for n, row in tab.items():
            print(label, n, {t: (round(v["P_point_ge_0.15"], 2), round(v["P_lower90_ge_0.15"], 2), round(v["P_upper90_lt_0.15"], 2)) for t, v in row.items()})


if __name__ == "__main__":
    main()
