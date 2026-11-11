"""Derived numbers of DESIGN.md: budgets, item limits, grading time, Mac hours, GPU and model dollars.

Pure arithmetic on recorded numbers; runs anywhere (python3 -B derive.py > derived.json). Every input names its source.
x86 = 2 pinned cores of the cloud container (feasibility/timing.json). The Mac is NOT measured: Mac seconds are the x86
seconds divided by r, the Mac box's speed relative to these cores, unknown (feasibility/FEASIBILITY.md, "Not measured").
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(os.path.join(HERE, "feasibility", "timing.json")))
F_, G_ = T["F"], T["G"]

ALLOW = 9600.0          # vfport tools/vfrun.py GRADING_ALLOWANCE_S
T_BOX = 2.7             # vfport RUNBOOK_MAC.md (cloud container; "report the Mac's number")
T_SETUP = 600.0         # spec section 6, assumed
N_ITEMS = 64            # spec section 2 (graded items)
WALLS = (60, 120, 180)  # minutes; 180 is the request maximum (vfport tools/check_request.py)


def item(brute_s, b_pred, t_jit):
    pred = b_pred * brute_s
    wall = pred + t_jit + 15.0                      # spec section 4
    cpu = 2.0 * (pred + t_jit)
    grading = N_ITEMS * (wall + T_BOX) + T_SETUP    # spec section 6, every item at its wall limit
    # smallest Mac speed ratio r for which grading stays inside the allowance (prediction and compile scale as 1/r)
    r_min = N_ITEMS * (pred + t_jit) / (ALLOW - T_SETUP - N_ITEMS * (15.0 + T_BOX))
    b_max = ((ALLOW - T_SETUP) / N_ITEMS - 15.0 - T_BOX - t_jit) / brute_s
    return dict(predict_s=round(pred, 1), wall_seconds=round(wall, 1), cpu_seconds=round(cpu, 1),
                grading_s_worst=round(grading), grading_h_worst=round(grading / 3600, 2),
                allowance_s=ALLOW, mac_ratio_min_for_allowance=round(r_min, 2), b_pred_max_at_r1=round(b_max, 3))


out = {"what": __doc__.strip().splitlines()[0], "inputs": "feasibility/timing.json and the constants named in this file"}

# ---- F: foundry hidden weights; spec episode 300 + 16 + 32 = 348 ticks; queries 8, 16, 32
R_F = F_["derived"]["member_ticks_per_s_full_episode_batched"]       # 121.9, float64, B = 16
R_F_PLUG = F_["plug_in_item_m256"]["member_ticks_per_s"]             # 104.2, assimilate + forecast, 256 members
TJ_F = F_["plug_in_item_m256"]["T_JIT_item_s"]                       # 8.2
fit_step = F_["recipes"]["fit_step_s_with_respin"]                   # 42.5, job 003's fit shape 8 x 4 x 2
f = {}
f["R_box_x86"] = R_F
f["B_res_full_episodes_x86"] = {w: round(60 * w * R_F / 348) for w in WALLS}
f["U_item"] = 256 * 48
f["brute_force_item_s_x86"] = round(256 * 48 / R_F_PLUG, 1)
f["item_b0.25_x86"] = item(256 * 48 / R_F_PLUG, 0.25, TJ_F)
f["instance_build_s_x86"] = round(152192 / R_F)                     # spec section 2 member-ticks
f["null_pool_s_x86"] = round(64 * 8 * 348 / R_F)                     # spec section 7: 8 episodes x 64 library worlds
f["draw_s_x86"] = round(65000 / R_F)                                 # spec section 1: about 65,000 member-ticks
f["W_box_one_start_143_steps_min"] = round(143 * fit_step / 60)      # job 003's step count (foundrylong PROGRESS.md)
f["W_box_one_start_200_steps_min"] = round(200 * fit_step / 60)
f["P0_box_16_worlds_min"] = round((16 * F_["recipes"]["prior_world_s"] + 6000 * F_["recipes"]["p0_step_s"]) / 60)
# sigma at the box tier if the ridge Dr(32) is the best generic recipe a box reaches (foundrylong README, skill at 16 ticks)
sC, sFT, sDr = 0.581, 0.455, 0.352
f["sigma16_ceiling_from_skills"] = round((sC - sFT) / sC, 3)
f["sigma16_box_if_ridge_is_best"] = round((sC - sDr) / sC, 3)
out["F"] = f

# ---- G: gliders, triggered items; episode 82 ticks; queries 8, 12, 16 after the push
R_G = G_["derived"]["member_ticks_per_s_best"]                       # 8.68 at B = 1
TJ_G = G_["derived"]["T_JIT_sim_item_s"]                             # 11.5
g = {}
g["R_box_x86"] = R_G
g["B_res_full_episodes_x86"] = {w: round(60 * w * R_G / 82) for w in WALLS}
g["U_item"] = 256 * 32
g["brute_force_item_s_x86"] = round(256 * 32 / R_G, 1)
g["item_b0.05_x86"] = item(256 * 32 / R_G, 0.05, TJ_G)
g["instance_build_s_x86"] = round(41664 / R_G)                       # spec section 2 member-ticks
g["null_pool_s_x86"] = G_["derived"]["null_pool_512_s"]
g["family_768x8_h_x86"] = G_["derived"]["P0_family_768_points_h"]
g["three_families_h_x86"] = round(3 * G_["derived"]["P0_family_768_points_h"], 1)   # public, true-form, designed
out["G"] = g

# ---- Mac hours, in x86-equivalent hours (divide by r for the computed parts; the agent's wall time is fixed)
mac = {}
for k, it in (("F", f["item_b0.25_x86"]), ("G", g["item_b0.05_x86"])):
    per_rollout = 3.0 + it["grading_h_worst"] + 20 / 3600
    mac[k] = dict(per_rollout_h_worst=round(per_rollout, 2), box_tier_4_scripts_h_serial=round(4 * per_rollout, 1))
mac["F"]["per_instance_before_h"] = round((f["draw_s_x86"] + f["instance_build_s_x86"]) / 3600, 2)
mac["G"]["per_instance_before_h"] = round(g["instance_build_s_x86"] / 3600, 2)
mac["F"]["per_profile_once_h"] = round(f["null_pool_s_x86"] / 3600, 2)
mac["G"]["per_profile_once_h"] = round(g["null_pool_s_x86"] / 3600, 2)
out["mac_x86_equivalent"] = mac

# ---- GPU dollars per instance for the ceiling rows (A100 40GB at $1.99/h, lambdalabs)
# foundrylong-001 out/full/info.json on origin/gpu-jobs: clock (s, 16 worlds in lockstep groups: upper bounds for one
# world), speed; status.json billed_usd 4.9154 for 'hours' 2.3549 of run; job 003: 1.55 s per W step of 8 fits (PROGRESS.md)
rate, gpu_mt = 1.99, 45613056 / 1094.65
clock = {"C16384 s0": 704.96, "C16384 s1": 688.04, "FT@32": 375.39, "FT@8": 370.68, "D@32": 62.22, "D@8": 36.41,
         "hidden": 117.47, "scores": 101.70}
sim_C = 2 * 16384 * 348 / gpu_mt
W = 143 * 1.55
Wplus = 4096 * 348 / gpu_mt + 336.25                                   # W+ simulation + C4096's training clock
overhead_h = 4.9154 / rate - 2.3549
work_s = sum(clock.values()) + sim_C + W + Wplus
out["gpu"] = {"F_per_instance": dict(work_h=round(work_s / 3600, 2), overhead_h=round(overhead_h, 2),
                                     usd=round(rate * (work_s / 3600 + overhead_h), 2),
                                     cap_usd=round(rate * (work_s / 3600 + overhead_h + 0.5 + 0.25) + 0.10, 2))}

# ---- model dollars per rollout (rollouts/qwen_ring_002/RESULT.md, rollouts/astra_ring_001/RESULT.md, ledger.json)
q_in, q_out, q_turns, q_usd = 7280288, 74233, 143, 0.8050
a_in, a_out, a_turns, a_usd, a_prov = 193826, 10782, 14, 2.4774, 1.0188
m = {}
m["qwen_150_turns_usd"] = round(q_usd * (150 / q_turns) ** 2, 2)       # context grows linearly with turns
m["qwen_150_turns_crude_bound_usd"] = round(150 * 200000 * 0.11e-6 + 150 * 8192 * 1.01e-6, 2)
m["astra_ring_caps_22_turns_listed_usd"] = round((a_in * (22 / a_turns) ** 2) * 10e-6 + a_out * 22 / a_turns * 50e-6, 2)
m["astra_provider_over_listed"] = round(a_prov / a_usd, 3)
m["astra_150_turns_qwen_context_listed_usd"] = round(150 * q_in / q_turns * 10e-6 + 150 * a_out / a_turns * 50e-6, 1)
m["astra_150_turns_provider_usd"] = round(m["astra_150_turns_qwen_context_listed_usd"] * a_prov / a_usd, 1)
m["qwen_share_of_agent_phase_waiting_for_model"] = round(1705 / 2313, 2)
out["model"] = m

print(json.dumps(out, indent=1))
