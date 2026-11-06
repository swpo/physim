"""Checker edits to results/summary.json (additive, every value computed from the saved outputs).
Keeps a backup at review/summary_before_check.json."""
import glob
import json
import math
import os
import shutil

import numpy as np

ROOT = "/home/user/evalwork/vecworld/vw1/fresh/inputs"
R0 = f"{ROOT}/results"
fn = f"{R0}/summary.json"
bk = f"{ROOT}/review/summary_before_check.json"
if not os.path.exists(bk):
    shutil.copy(fn, bk)
S = json.load(open(bk))
St = json.load(open(f"{R0}/steer.json"))
Se = json.load(open(f"{R0}/sensitivity.json"))
edits = []

# ---- (a) which states reach 1, per horizon (recomputed from results/vis/state_*.npz)
D = [np.load(f) for f in sorted(glob.glob(f"{R0}/vis/state_*.npz"))]
names = [str(n) for n in D[0]["names"]]
Y = np.stack([d["Y"].astype(float) for d in D])
tw = [names.index(f"twin_{r}") for r in range(6)]
sd = Y[:, tw].reshape(-1, 336).std(0)
ge1 = {}
for v, ix in (("coarse", np.arange(192)), ("objects", np.arange(192, 336))):
    keep = ix[sd[ix] > 1e-6 * sd[ix].max()]
    Z = Y[..., keep] / sd[keep]
    T = Z[:, tw]
    Vu = T.var(1, ddof=1).mean(-1)
    for c in ("rand_x1", "rand_x8", "body_x1", "body_x8same", "k32_x1", "empty_x1"):
        ci = [names.index(f"{c}_{r}") for r in range(6)]
        Dl = Z[:, ci] - T
        snr = ((Dl.mean(1) ** 2) - Dl.var(1, ddof=1) / 6).mean(-1) / Vu
        g = {str(t): np.flatnonzero(snr[:, t] >= 1).tolist() for t in (1, 2, 4, 8, 16, 32)}
        if any(g.values()):
            ge1[f"{v}/{c}"] = g
a = S["a_blind_visibility"]
a["states_ge_1_by_tau"] = ge1
a["worst_state_blind_random"] = {"value": max(a["by_condition"][f"{v}/{c}"]["worst_state"][t] for v in ("objects", "coarse")
                                              for c in ("rand_x1", "rand_x8") for t in a["by_condition"]["objects/rand_x1"]["worst_state"]),
                                 "view": "objects", "condition": "rand_x8", "tau": "8", "n_states_ge_1_any_tau": 0}
a["checker_note"] = ("Default-limit programs: under body_x8same (objects view) exactly one of 32 states exceeds 1 at each of "
                     "tau = 2, 4, 8, 16, but a different state each time (states 31, 14, 3, 5: 4 distinct states); the worst is "
                     "19.6 at tau = 2. Not 'one state from tau 2 to 16'.")
edits.append("a_blind_visibility: added states_ge_1_by_tau, worst_state_blind_random and checker_note (the >= 1 cases are 4 different states, one per horizon)")

# ---- (d) sentinel 99 as a median
dl = S["d_late_differences"]
for blk in ("first_tick_twin_snr_ge_1", "rand_x1_first_tick_twin_snr_ge_1"):
    for v in ("objects", "coarse"):
        r = dl[blk][v]
        r["n_reached_by_32"] = 32 - r["n_never_by_32"]
        r["median_label"] = ">32 (99 = not reached by tick 32)" if r["median"] > 32 else str(r["median"])
edits.append("d_late_differences: added n_reached_by_32 and median_label (the coarse 'median 99.0' is the not-reached sentinel, i.e. > 32)")

# ---- (b) steering: missing page numbers, clustering, direction wording, video run
b = S["b_steering"]
b["all_clean_no_event_mass_within_20pct"] = St["summary"]["all_clean_no_event_mass_within_20pct"]
b["all_with_event_or_mass_change"] = St["summary"]["all_with_event_or_mass_change"]
ok = [r for r in St["rows"] if "heading_change_deg_signed" in r]
by = {}
for r in ok:
    by.setdefault(r["state"], []).append(r["heading_change_deg_signed"] < 0)
ks = sorted(by)
rng = np.random.default_rng(0)
bs = [np.concatenate([by[ks[i]] for i in rng.integers(0, len(ks), len(ks))]).mean() for _ in range(20000)]
b["all"]["frac_se_cluster_bootstrap_over_targets"] = float(np.std(bs))
b["n_targets_with_usable_runs"] = len(ks)
b["n_targets_majority_toward_minus_n"] = int(sum(np.mean(by[k]) > 0.5 for k in ks))
b["direction_note"] = ("-n is the source flank only for the flank programs (19/24 turned toward it). For the lead programs the "
                       "sources are the densest rear cells and the sinks a 2x2 patch ahead on +n, so -n means away from the "
                       "sink patch (16/22). Runs share targets (12 targets carry the 46 runs): binomial SE 0.063, target-resampling SE 0.078.")
z = np.load(f"{R0}/steer_video_frames.npz")
s_ = int(z["slot"])
ev = z["tab_steered"][:, s_, 15]
first_ev = int(np.flatnonzero(ev != 0)[0])
b["video_run"]["checker_note"] = (f"Through tick 22 the target has no tracker event and mass within 1% of its twin's; at tick {first_ev} "
                                  f"the steered target's slot ends with event {ev[first_ev]:g} ('fused': it merged into a neighbour). "
                                  "The video has 24 frames (ticks 0-23), so its last frame shows that fusion.")
edits.append("b_steering: added the clean / event split (22/23, 13/23), target-clustered SE (0.078), 12 contributing targets, "
             "direction_note (-n is the source side only for flank), video_run.checker_note (target fuses at tick 23)")

# ---- (c) ranges the report states, recomputed over the 3 states
ps = Se["per_state"]
E = Se["eps"]


def rng_(vals):
    return [float(min(vals)), float(max(vals))]


best = lambda r, N, k, grp=None: min((r["validation"][f"N{N}_{k}_eps{e:g}"]["rel_err_median_by_group"][grp] if grp else  # noqa: E731
                                      r["validation"][f"N{N}_{k}_eps{e:g}"]["rel_err_median"]) for e in E)
der = {"n_vjps_per_horizon": Se["n_eff_outputs"]}
for N in (1, 2, 4, 8):
    der[f"fd_rel_err_median_best_eps_N{N}"] = rng_([best(r, N, k) for r in ps.values() for k in ("deposit", "move")])
    der[f"fd_rel_err_median_best_eps_top10_cells_N{N}"] = rng_([best(r, N, k, "top") for r in ps.values() for k in ("deposit", "move")])
n = lambda r, N, k: r["ad_norm_median"][f"N{N}_{k}"]  # noqa: E731
der["ad_norm_growth_N1_to_N2"] = rng_([n(r, 2, k) / n(r, 1, k) for r in ps.values() for k in ("deposit", "move")])
der["ad_norm_growth_per_tick_N2_to_N4"] = rng_([math.sqrt(n(r, 4, k) / n(r, 2, k)) for r in ps.values() for k in ("deposit", "move")])
der["ad_norm_growth_per_tick_N4_to_N8"] = rng_([(n(r, 8, k) / n(r, 4, k)) ** 0.25 for r in ps.values() for k in ("deposit", "move")])
der["deposit_s2_n_cells_for_90pct_N1"] = rng_([r["N1"]["deposit"]["shares"]["s2"]["n_cells_for_90pct"] for r in ps.values()])
der["deposit_s2_share_cells_for_90pct_N1"] = rng_([r["N1"]["deposit"]["shares"]["s2"]["share_cells_for_90pct"] for r in ps.values()])
der["direct_block_floor_N1_SD_per_unit"] = rng_([r["N1"]["deposit"]["direct_block_mean_floor"] for r in ps.values()])
der["deposit_excess_share_cells_for_90pct_N1"] = rng_([r["N1"]["deposit"]["shares_excess_over_direct_floor"]["s"]["share_cells_for_90pct"] for r in ps.values()])
der["deposit_excess_top90_within_4px_N1"] = rng_([r["N1"]["deposit"]["shares_excess_over_direct_floor"]["s"]["frac_of_those_within_4px_of_footprint"] for r in ps.values()])
der["footprint_frac_A_sum_gt_1e-3"] = rng_([r["footprint_frac_A_sum_gt_1e-3"] for r in ps.values()])
der["deposit_share_cells_for_90pct_N4"] = rng_([r["N4"]["deposit"]["shares"]["s"]["share_cells_for_90pct"] for r in ps.values()])
der["amp0.5_actual_snr_median_N1"] = rng_([r["amplitude_0.5"][f"N1_{k}"]["actual_snr_median"] for r in ps.values() for k in ("deposit", "move")])
der["amp0.5_actual_over_linear_norm_median_N1"] = rng_([r["amplitude_0.5"][f"N1_{k}"]["actual_over_linear_norm_median"] for r in ps.values() for k in ("deposit", "move")])
der["amp0.5_actual_over_linear_norm_top10_cells_N1"] = rng_([r["amplitude_0.5"][f"N1_{k}"]["by_group"]["top"]["actual_over_linear_norm_median"] for r in ps.values() for k in ("deposit", "move")])
der["note"] = ("Ranges over states 0, 1, 2 and over deposit / move. Corrects the report: 192 VJPs (not 188); FD agreement at 1 tick "
               "<= 2.2e-4 overall but 2e-4 to 3.9e-3 on the 10 most sensitive cells (not 1e-5 to 3e-4); at 2 ticks 2.5e-4 to 1.1e-2 "
               "overall but 0.02 to 0.47 on the most sensitive cells; growth 5-100x from 1 to 2 ticks and 15-230x per tick after "
               "(not 10-100x and 20-60x); footprint 12.6-13.2%; at the most sensitive cells the 0.5 response is 5e-5 to 8e-3 of "
               "the linear prediction (not about 1/500). sensitivity.png: maps are state 0, the FD panel is the median over the 3 states.")
S["c_sensitivity"]["derived_ranges_over_states"] = der
edits.append("c_sensitivity: added derived_ranges_over_states (192 VJPs; FD error ranges incl. the top-10 cells; growth 5-100x then "
             "15-230x per tick; footprint 12.6-13.2%; top-cell actual/linear 5e-5 to 8e-3)")

S["media_checked"] = {"steer.mp4": "h264 yuv420p 900x364, 24 frames at 4 fps (ticks 0-23), 215777 bytes; results/render_steer.log is stale "
                                   "(it records an earlier 41-frame, 329841-byte render)",
                      "steer.jpg": "900x364, tick 22", "visibility.png": "960x360", "sensitivity.png": "960x660"}
edits.append("media_checked: frame count and the stale render log")
S["checker"] = {"report": f"{R0}/check.md", "scripts": f"{ROOT}/review", "backup_of_unedited_summary": bk, "edits": edits,
                "rerun": "visibility state 13 re-run end to end (B = 43, same layout): every saved array identical (max |diff| 0)"}
json.dump(S, open(fn, "w"), indent=1)
print(json.dumps(edits, indent=1))
print(json.dumps(der, indent=1))
print(b["all"]["frac_se_cluster_bootstrap_over_targets"], b["n_targets_majority_toward_minus_n"], b["video_run"]["checker_note"])
