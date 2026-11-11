"""recompute -- member-ticks, GPU hours, dollars, caps and compute budgets of the three dial designs (arithmetic only).

Every input is a number already measured in the program (its source is written beside it) or a size declared in
a design (round6/dials/<design>/DESIGN.md). Nothing is simulated. Estimates of mine are marked "estimate".
usage: python -B recompute.py  -> results/recompute.json
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
A100, H200 = 1.99, 6.69          # $/h: gpu/LEDGER.md (lambdalabs A100 40GB; nebius H200 as billed)


def cap(rate, max_hours):
    """gpu/LEDGER.md, lessons of round 5: rate x (max_hours + 0.25), plus $0.10."""
    return round(rate * (max_hours + 0.25) + 0.10, 2)


def max_hours(rate, cap_usd):
    return round((cap_usd - 0.10) / rate - 0.25, 2)


def usd_per_million(rate_usd_h, mt_per_s):
    return round(rate_usd_h / (mt_per_s * 3600 / 1e6), 3)


out = {"what": "cost and feasibility recomputation of the round-6 dial designs", "cap_rule": "rate x (max_hours + 0.25) + 0.10"}

# ----------------------------------------------------------------------------- measured rates
ladder_design_rate = 768 * 10 * 82 / 480.0          # n=4 design stage of r5-ladder-002
ladder_lab_rate = 8 * 640 * (33 + 50) / 323.0
ladder_exam_rate = (449280 / 3) / 197.0
ladder_all_in = 3650912 / (1.2146 * 3600)
rates = {
    "gliders_A100_40GB": {
        "ladder_harness_design": round(ladder_design_rate), "ladder_harness_lab": round(ladder_lab_rate),
        "ladder_harness_exam_stage": round(ladder_exam_rate), "ladder_whole_script_incl_nets": round(ladder_all_in),
        "bias2_and_cards": [617, 734],
        "usd_per_million": {"ladder_design": usd_per_million(A100, ladder_design_rate), "bias2_and_cards": [usd_per_million(A100, 734), usd_per_million(A100, 617)],
                            "ladder_billed_all_in": round(2.5555 / 3.650912, 3)},
        "source": "round5/ladder/results/job/progress.txt (n=4: 'D design done in 480s', 'E Lab done in 323s', 'G exams done in 197s') with "
                  "round5/ladder/results/summary.json [job.member_ticks: design 1,574,400 = (384 + 768 + 768) points x 10 episodes x 82 ticks; "
                  "exam 449,280 over 3 sets; member_ticks_total; hours_in_script; status.cost.billed_usd; status.pod.gpu = A100_40GB]; "
                  "round5/bias2/results/gliders_w/sim_{A,B}.json [member_ticks_per_s] (batch 64, fields copied to the host); "
                  "round6/cards/results/jobs/r6-cards-001/review.md ('measured 617-734'), round6/cards/results/cards/gliders/card.md section 9 (687)"},
    "gliders_80GB_cards": {"value": [1400, 1700], "usd_per_million_H200": [usd_per_million(H200, 1700), usd_per_million(H200, 1400)],
                           "source": "gpu/bench/README.md (A100 80GB, B >= 64: 1,486-1,707); round5/bias2/results/gliders/sim_{A,B}.json (1,212-1,399)"},
    "membrane_128px_A100_40GB": {
        "with_tracker_cards": 7091, "usd_per_million": usd_per_million(A100, 7091),
        "bias2_batch64": [598, 2717], "usd_per_million_bias2": [usd_per_million(A100, 2717), usd_per_million(A100, 598)],
        "source": "round6/cards/results/cards/membrane/card.md section 9 (lattice [4,128,128], 20 substeps per tick, tracker on every member, "
                  "compile excluded; two runs of about 6 s each: r6-cards-002 progress.txt 'membrane__A: sim 17.4+9.4s' is the first call); "
                  "round5/bias2/results/membrane_w/sim_A.json [member_ticks_per_s] (batch 64; 'base/branch rates include the host transfer of the "
                  "float64 records')"},
    "vortex_128px": {"A100_40GB": 169.4, "H200": 444.1, "usd_per_million": {"A100_40GB": usd_per_million(A100, 169.4), "H200": usd_per_million(H200, 444.1)},
                     "source": "round5/vortexexam/results/summary.json [status_job_B.value.rate], [platform_job1.value.rate]"},
    "vortex_64px": {"H200": [1388, 1577], "A100_40GB_cards": 209,
                    "A100_40GB_if_the_128px_card_ratio_holds_estimate": [round(1388 * 169.4 / 444.1), round(1577 * 169.4 / 444.1)],
                    "exam_equivalents_per_s_A100": [round(209 / 4, 1), round(1577 * 169.4 / 444.1 / 4, 1)],
                    "usd_per_million_exam_equivalents_A100": [usd_per_million(A100, 1577 * 169.4 / 444.1 / 4), usd_per_million(A100, 209 / 4)],
                    "source": "round5/vortexexam/results/summary.json [headline.member_ticks_per_s_H200]; round6/cards/results/cards/vortex64/card.md section 9"},
    "vortex_32px": {"value": None, "source": "not measured on any card (compute_limit DESIGN.md section 6 says so)"},
}
out["rates_member_ticks_per_s"] = rates

# ----------------------------------------------------------------------------- defect_gliders
EP = 82                                   # burn 50 + P 16 + H 16: ladder summary.json [config]
st1_worlds = 2 * 4                        # eta 0 and 4 x 4 truths
train8, train10 = 2 * 768 * 8 * EP, 2 * 768 * 10 * EP
lab = st1_worlds * (32 + 32) * (33 + 50)  # 33 charged ticks + the designer's 50-tick burn-in per reset, as in the ladder
exam = st1_worlds * (96 * (50 + 16 + 12 * 16) + 96 * (50 + 16))   # items x (burn + history + 12 replicates x 16) + climatology (n_clim = items, the ladder's 96 for 48: assumption)
plug = st1_worlds * 96 * 8 * 16
misc = 10496 + 7200
st1 = train8 + lab + exam + plug + misc
st1_10 = train10 + lab + exam + plug + misc
per_world = (lab + exam + plug) // st1_worlds
st2 = 24 * per_world + 32 * 32 * 83 + 32 * 16 * (50 + 16 + 12 * 16) + 768 * 8 * EP
nets1, nets2, over = (0.25, 0.40), (0.5, 0.8), 0.10      # estimates: ladder block view = 337 s per hidden set (progress.txt); more nets here
sim1 = (st1 / 1312 / 3600, st1_10 / 650 / 3600)
h1 = (sim1[0] + nets1[0] + over, sim1[1] + nets1[1] + over)
sim2 = (2.2e6 / 1312 / 3600, 2.2e6 / 650 / 3600)
h2 = (sim2[0] + nets2[0] + over, sim2[1] + nets2[1] + over)
out["defect_gliders"] = {
    "stage1_member_ticks": {"training_2_families_768x8": train8, "the_same_at_10_episodes_per_point_as_the_ladder": train10, "lab": lab, "exam_with_climatology": exam,
                            "plugins": plug, "scales_and_truths": misc, "total": st1, "total_at_10_episodes": st1_10, "designer": 1.4e6},
    "stage2_member_ticks": {"recomputed_without_overheads": st2, "designer": 2.2e6},
    "stage1_hours_A100_40GB": [round(x, 2) for x in h1], "stage1_usd": [round(A100 * x, 2) for x in h1], "designer_stage1_usd": 1.5,
    "stage1_cap_by_rule": [cap(A100, round(h1[0] * 1.25, 2)), cap(A100, round(h1[1] * 1.25, 2))], "declared_stage1_cap": 5,
    "stage1_max_hours_under_declared_cap": {"A100_40GB": max_hours(A100, 5), "H200": max_hours(H200, 5)},
    "stage1_hours_needed_on_H200_estimate": [round(st1 / 1700 / 3600 + 0.2 + over, 2), round(st1_10 / 1400 / 3600 + 0.3 + over, 2)],
    "stage1_cap_if_H200": cap(H200, 0.75),
    "stage2_hours_A100_40GB": [round(x, 2) for x in h2], "stage2_usd": [round(A100 * x, 2) for x in h2], "designer_stage2_usd": 3.5,
    "stage2_max_hours_under_declared_cap_15": {"A100_40GB": max_hours(A100, 15), "H200": max_hours(H200, 15)},
    "study_caps_sum": 20,
    "stats_critic_minimum_stage1": {"what": "8 truths x eta 0 and 4, three seeds (crit_stats/CRITIQUE.md)", "member_ticks": train8 + 16 * per_world + misc,
                                    "hours_A100_40GB_estimate": [round((train8 + 16 * per_world) / 1312 / 3600 + 0.4 + over, 2), round((train8 + 16 * per_world) / 650 / 3600 + 0.6 + over, 2)]},
    "research_budget": {"declared_episodes": 8192, "member_ticks": 8192 * EP, "core_hours_at_0.15_to_0.164": [round(8192 * EP * 0.15 / 3600, 1), round(8192 * EP * 0.164 / 3600, 1)],
                        "P0_set_of_this_design_episodes": 768 * 8, "budget_over_P0_set": round(8192 / (768 * 8), 2),
                        "round4_P0_set_episodes": 1024, "budget_over_round4_P0_set": 8.0,
                        "H_needs_episodes": {"true_form_family": 768 * 8, "emulator_designed": 768 * 8, "sum": 2 * 768 * 8},
                        "H_fits": 2 * 768 * 8 <= 8192,
                        "source": "DESIGN.md section 6; round5/agentenv/results/summary.json [cost.value.recipes_gliders.P0_set_round4.episodes] = 1024, "
                                  "[cost.value.cpu_s_per_member_tick.gliders]"},
    "prediction_budget": {"declared_fraction": 0.05, "question_cpu_s_if_32_members_x_16_ticks": round(32 * 16 * 0.15, 1),
                          "allowed_cpu_s_per_item": round(0.05 * 32 * 16 * 0.15, 2), "allowed_if_question_is_one_member": round(0.05 * 16 * 0.15, 2),
                          "note": "the design does not say how many members a 'question' is"},
    "largest_array": {"declared": 7e7, "ladder_reviewed": 1.1e8, "ladder_peak_gb_compile_level": 4.3,
                      "source": "round5/ladder/results/summary.json [job.status.review.summary]; the ladder ran on the 40 GB card without a memory failure"},
}

# ----------------------------------------------------------------------------- sublevel_second
EPM = 198
per_world_m = {"lab": 96 * EPM, "exam": 64 * (150 + 16 + 12 * 32), "climatology": 64 * EPM, "screen": 64 * 12 * 32}
pw = sum(per_world_m.values())
shared = (2048 + 4096 + 1536 + 1536 + 2048) * EPM
tot = 60 * pw + shared
sim_card = (tot / 7091 / 3600, tot / (7091 * 0.45) / 3600)      # upper: carrier field and small exam batches (ladder: exam stage ran at 0.58 of the design rate), estimate
sim_designer = (tot / 2717 / 3600, tot / 598 / 3600)
nets = (1.5, 2.0)                                               # the designer's estimate; no membrane net exists to time
hm = (sim_card[0] + nets[0] + 0.1, sim_card[1] + nets[1] + 0.1)
stage1_mt = (2048 + 4096) * EPM + 4 * pw
ft = {"fine_tunes_per_world_and_seed_leave_one_episode_out": (4 + 1) + (16 + 1) + (64 + 1)}
ft["total_60_worlds_2_seeds"] = ft["fine_tunes_per_world_and_seed_leave_one_episode_out"] * 60 * 2
out["sublevel_second"] = {
    "member_ticks": {"per_world": per_world_m, "per_world_total": pw, "worlds": 60, "shared": shared, "total": tot, "designer": 7.7e6},
    "simulation_hours_A100_40GB": {"at_the_cards_rate": [round(x, 2) for x in sim_card], "at_the_designers_bracket": [round(x, 2) for x in sim_designer]},
    "simulation_usd": {"at_the_cards_rate": [round(A100 * x, 2) for x in sim_card], "designer": [1.6, 7.1]},
    "job_hours_A100_40GB": [round(x, 2) for x in hm], "job_usd": [round(A100 * x, 2) for x in hm], "designer_usd": [5, 11],
    "cap_by_rule_A100": cap(A100, 3.5), "declared_cap": 20, "max_hours_under_declared_cap": {"A100_40GB": max_hours(A100, 20), "H200": max_hours(H200, 20)},
    "two_jobs_proposed": {"stage1_cap": cap(A100, 2.0), "main_cap": cap(A100, 3.5), "sum": round(cap(A100, 2.0) + cap(A100, 3.5), 2)},
    "stage1": {"member_ticks_without_H_designs": stage1_mt, "share_of_all_simulation": round(stage1_mt / tot, 2),
               "usd_estimate": [1.5, 2.5], "designer_usd": 1.0,
               "note": "stage 1 needs both shared training families (public 2,048 and extended 4,096 episodes) and their nets, whatever the number of truths"},
    "fine_tuning_F": ft,
    "state_given_screen_share": round(60 * per_world_m["screen"] / tot, 2), "D64_extra_lab_share": round(60 * 48 * EPM / tot, 2),
    "arms_lam_0.5_and_0.75_share": round(24 * pw / tot, 2),
    "research_budget": {"declared_episodes": 8192, "cpu_s_per_episode": round(EPM * 0.0123, 2), "core_hours": round(8192 * EPM * 0.0123 / 3600, 2),
                        "core_hours_at_vmap16": round(8192 * EPM * 0.0201 / 3600, 2), "P0": 2048, "S": 1536 + 2048, "H": 4096 + 2048, "H_fits_in_simulation": True,
                        "source": "track1/membrane_world/results/summary.json [timing.world_tick_L0_L1_L2_B1_per_member_s] = 0.01227 (128 px, one core), "
                                  "[timing.world_tick_L0_L1_L2_B16_per_member_s] = 0.0201"},
    "prediction_budget": {"declared_fraction": 0.1, "question_cpu_s_if_32_members_x_32_ticks": round(32 * 32 * 0.0123, 1),
                          "allowed_cpu_s_per_item": round(0.1 * 32 * 32 * 0.0123, 2)},
    "largest_array": {"declared": 6e7, "check": "768 members (64 items x 12) x 5 fields x 128 x 128 = %d" % (768 * 5 * 128 * 128),
                      "gpu_memory": "r6-cards-001 review.md: membrane at device batch 480 peaks at about 5 GB or less on the A100 40GB"},
}

# ----------------------------------------------------------------------------- compute_limit
T = 404
design_eq = 256 * T                      # 256 points x one exam-equivalent each (4 boxes at 64 px, 16 at 32 px), per side
truth_eq = 10 * (4 + 16) * T             # per side
eq = 2 * (design_eq + truth_eq)
mt64, mt32 = 4 * (design_eq + truth_eq), 16 * (design_eq + truth_eq)
redo = 190000
r64 = (209, round(1577 * 169.4 / 444.1))
h64 = (mt64 / r64[1] / 3600, mt64 / r64[0] / 3600)
h32 = h64                                 # if the cost per pixel-tick at 32 px equals that at 64 px: NOT measured
hs = (h64[0] + h32[0] + 0.15, h64[1] + h32[1] + redo / 169.4 / 3600 + 0.15)
hH = (mt64 / 1577 / 3600) * 2 + redo / 444.1 / 3600 + 0.15
full_eq = 1.6e6
zero_arm = 1045664
rest = full_eq - zero_arm            # the capped settings, in exam-equivalents, at 150 (card ratio) to 52 (cards job) exam-equivalents per second
hf = (zero_arm / 169.4 / 3600 + rest / 169.4 / 3600 + 0.3, zero_arm / 169.4 / 3600 + rest / (209 / 4) / 3600 + 0.3)
out["compute_limit"] = {
    "stop_rule_job": {
        "exam_equivalent_member_ticks": eq, "designer": 0.37e6, "member_ticks_64px": mt64, "member_ticks_32px": mt32, "items_redone_128px": redo,
        "hours_A100_40GB": [round(x, 2) for x in hs], "usd": [round(A100 * x, 2) for x in hs], "designer_usd": 2.5,
        "cap_by_rule_at_the_upper_hours": cap(A100, round(hs[1], 2)), "declared_cap": 5,
        "max_hours_under_declared_cap": {"A100_40GB": max_hours(A100, 5), "H200": max_hours(H200, 5)},
        "hours_on_H200_estimate": round(hH, 2), "cap_by_rule_H200": cap(H200, round(hH, 2)),
        "cut_32px_design_to_128_points_saves_member_ticks": 128 * 16 * T,
        "cards_job_64px_detail": "r6-cards-001 progress.txt vortex64__B: main 16 members x 500 ticks in 78.5 s (102/s, batch 16), branch 32 x 30 x 32 member-ticks in 92.4 s (332/s, device batch 960)",
        "share_of_member_ticks_at_32px": round(mt32 / (mt64 + mt32), 2),
        "note": "the 32 px rate is not measured on any card; the 64 px rate on the A100 40GB is measured only in the cards job (209)"},
    "full_study": {"exam_equivalent_member_ticks": full_eq, "zero_arm": zero_arm, "zero_arm_hours_A100": round(zero_arm / 169.4 / 3600, 2),
                   "zero_arm_usd_A100": round(A100 * zero_arm / 169.4 / 3600, 2), "zero_arm_billed_in_round5": 3.7164,
                   "hours_A100_40GB": [round(x, 2) for x in hf], "usd": [round(A100 * x, 2) for x in hf], "designer_usd": [5, 7],
                   "cap_by_rule": cap(A100, round(hf[1], 2)), "declared_cap": 12, "max_hours_H200_under_12": max_hours(H200, 12),
                   "source": "round5/vortexexam/results/summary.json [status_job_B.value.member_ticks_total], [headline.exam_job_B.value.billed_usd]"},
    "stored_pilot_B": {"design_series": "origin/gpu-jobs:jobs/r5-vortexexam-006/out/design_S_00.npz and design_S_01.npz, S (512, 405, 14) float16 each",
                       "design_npz": "holds parameters, classes, nats and the input programs, no series",
                       "exam": "exam.npz S (10, 12, 405, 14) float16, Y (10, 12, 4, 8, 3, 2)", "checked_by": "git show origin/gpu-jobs:...; numpy.load of each file"},
    "budgets": {"R_declared": 64, "R_core_hours": round(64 * T * 0.5294 / 3600, 2), "R_zero_point": 1350, "R_zero_point_core_hours": round(1350 * T * 0.5294 / 3600, 1),
                "envelope_core_hours_4_cores_24_h": 96,
                "pooled_design_exam_equivalents_per_side": 256, "over_R_at_r_quarter": 256 / 64, "over_R_at_r_sixteenth": 256 / 16,
                "f_declared": 0.05, "question_cpu_s_32_members_8_to_32_ticks": [round(32 * 8 * 0.5294), round(32 * 32 * 0.5294)],
                "allowed_cpu_s_per_item": [round(0.05 * 32 * 8 * 0.5294, 1), round(0.05 * 32 * 32 * 0.5294, 1)],
                "exam_size_episodes_R_64_buys": 64,
                "source": "round5/vortexexam/results/summary.json [headline.P0_cost_envelope.value.cpu_s_per_member_tick_128px] = 0.5294"},
    "largest_array": {"declared": 4096 * 32 * 32 * 5, "at_64px": 1024 * 64 * 64 * 5,
                      "gpu_memory": "round5/vortexexam summary.json [review_of_job2]: peak about 10 GB at batch 1024, 128 px"},
}

# ----------------------------------------------------------------------------- caps by the rule at the upper hour estimate, and first-job spend
st1h_m = (stage1_mt / 7091 / 3600 + 0.5 + 0.1, (stage1_mt + (1536 + 1536 + 2048) * EPM) / (7091 * 0.45) / 3600 + 0.8 + 0.1)   # nets 0.5-0.8 h: estimate
out["caps_by_rule_A100_40GB_at_upper_hours"] = {
    "defect_gliders_stage1": cap(A100, round(h1[1], 2)), "defect_gliders_stage2": cap(A100, round(h2[1], 2)),
    "defect_gliders_stage1_stats_minimum": cap(A100, out["defect_gliders"]["stats_critic_minimum_stage1"]["hours_A100_40GB_estimate"][1]),
    "sublevel_second_whole": cap(A100, round(hm[1], 2)), "sublevel_second_main_at_3.5_h": cap(A100, 3.5),
    "sublevel_second_stage1": {"hours_estimate": [round(x, 2) for x in st1h_m], "usd": [round(A100 * x, 2) for x in st1h_m], "cap": cap(A100, round(st1h_m[1], 2))},
    "compute_limit_stop_rule": cap(A100, round(hs[1], 2)), "compute_limit_full": cap(A100, round(hf[1], 2))}
half32_h = hs[1] - (128 * 16 * T) / (r64[0] * 4) / 3600        # 32 px at the same cost per pixel-tick as the cards job's 64 px rate: not measured
out["compute_limit"]["stop_rule_job"]["if_the_32px_design_halves"] = {"upper_hours": round(half32_h, 2), "cap_by_rule": cap(A100, round(half32_h, 2))}
out["compute_limit"]["stop_rule_job"]["max_hours_under_a_cap_of_6"] = max_hours(A100, 6)
first = (A100 * (h1[0] + st1h_m[0] + hs[0]), A100 * (h1[1] + st1h_m[1] + hs[1]))
out["first_jobs_expected_usd"] = {"value": [round(x, 1) for x in first], "what": "defect_gliders stage 1 + sublevel_second stage 1 + compute_limit stop rule, A100 40GB",
                                  "billed_by_the_end_of_round5": 46.27, "approved": 1000, "source": "gpu/LEDGER.md"}

# ----------------------------------------------------------------------------- enforcement of decision 2 as the port stands
net = None
p = os.path.join(HERE, "results", "net_cpu_cost.json")
if os.path.exists(p):
    net = json.load(open(p))
    b = net["cases"][0]
    out["net_training_inside_the_research_budget"] = {
        "block_net_cpu_s_per_step": b["cpu_s_per_step"], "first_step_cpu_s_with_compilation": b["first_step_cpu_s"],
        "conditioned_net_6000_steps_cpu_hours": round(6000 * b["cpu_s_per_step"] / 3600, 2),
        "gliders_episode_equivalents": int(round(6000 * b["cpu_s_per_step"] / (0.15 * EP))),
        "share_of_8192_gliders": round(6000 * b["cpu_s_per_step"] / (0.15 * EP) / 8192, 3),
        "membrane_episode_equivalents_if_the_same_net_estimate": int(round(6000 * b["cpu_s_per_step"] / (0.0123 * EPM))),
        "share_of_8192_membrane_estimate": round(6000 * b["cpu_s_per_step"] / (0.0123 * EPM) / 8192, 2),
        "source": "results/net_cpu_cost.json (net_cpu_cost.py, this folder: the ladder's block-view step, batch 128 x 4, one thread, shared machine)"}
out["enforcement_in_the_port"] = {
    "prediction": "per-item grading box takes --cpu (CPU seconds), --wall and --mem-gib: round6/vfport/physim2_env/grading.py:185",
    "research": "the agent box gets cpus and memory (round6/vfport/physim2_env/taskset.py:379) and a time limit; 'CPU metering: not studied', the agent box's "
                "counter is 'agent_box_cpu_s_unverified' (round6/vfport/README.md section 4, item 5)",
    "item_box_overhead_cpu_s": round(66 / 64, 2),
    "item_box_overhead_source": "round6/vfport/README.md line 268: 'the item boxes use 66 CPU-seconds' for 64 items (ring, policy C)"}

# ----------------------------------------------------------------------------- build time (calibration from commit timestamps)
out["build_time"] = {
    "calibration_hours_first_to_last_commit": {"round5/vortexexam (a new exam on a world with none; 31 commits; three GPU jobs)": 6.3,
                                               "round5/ladder (a variation of the gliders exam; 16 commits; one GPU job of 1.3 h)": 4.1},
    "calibration_source": "git log --format=%ci origin/claude/fisim-agent-world-research-hepmlz -- <folder>",
    "estimate_agent_hours": {"defect_gliders_stage1": [4, 5], "defect_gliders_stage2": [3, 4], "sublevel_second": [10, 14], "compute_limit_stop_rule_job": [3, 4]},
    "lines_of_existing_code_for_scale": {"ladder_lib": 649, "ladder_net": 493, "run_ladder": 666, "vxlib": 487, "vxnet": 452, "vxsbi": 286, "vortexexam_job2": 972}}

os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
json.dump(out, open(os.path.join(HERE, "results", "recompute.json"), "w"), indent=1)
for k in ("defect_gliders", "sublevel_second", "compute_limit"):
    print(k, json.dumps(out[k], indent=1)[:2600])
print(json.dumps(out.get("net_training_inside_the_research_budget"), indent=1))
print(json.dumps(rates["gliders_A100_40GB"]["usd_per_million"]), json.dumps(rates["vortex_64px"]))
