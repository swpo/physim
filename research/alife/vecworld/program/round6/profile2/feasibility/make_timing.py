"""make_timing -- profile2 feasibility: raw/*.json (f_time.py, g_time.py, the wheel download) -> timing.json.

    python3 -B make_timing.py            (standard library only)

Every number in timing.json is either measured (raw file and key) or computed from measured numbers and the
pilots' recorded sizes (formula and sources written next to it). Times are seconds of wall clock on 2 x86 cloud
cores (Intel Xeon @ 2.10GHz, taskset, XLA intra-op threads 2) unless a key says otherwise.
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")


def load(name):
    p = os.path.join(RAW, name + ".json")
    return json.load(open(p)) if os.path.exists(p) else None


def med(d, k):
    return None if d is None or k not in d else d[k]["median"]


def spread(d, k):
    return None if d is None or k not in d else [d[k]["min"], d[k]["max"]]


R = lambda x, n=3: None if x is None else round(float(x), n)
BOX_MIN = (60, 120, 180)
OUT = {"what": "profile2 feasibility: cost of candidate worlds F (foundry hidden weights) and G (gliders, hidden stress "
               "conversion) in the agent's box and the grading boxes; 2 x86 cloud cores of the cloud container",
       "protocol": "one mode per process (f_time.py, g_time.py; run_f.sh, run_g.sh), taskset -c 0,1, XLA_FLAGS="
                   "'--xla_cpu_multi_thread_eigen=true intra_op_parallelism_threads=2', /home/user/evalwork/vecworld/vw1/"
                   ".venv/bin/python (jax 0.12.0.1); compile timed apart (lower().compile()); timed calls repeated 3 times "
                   "(median, [min, max]) unless n says otherwise; peak memory = ru_maxrss of the process (includes about "
                   "0.25 GB of imports)",
       "mac": "NOT MEASURED. The Mac's boxes are Linux aarch64 under Docker Desktop on Apple Silicon. No timing of this "
              "code on the Mac exists in the repository (rollouts so far ran in the cloud container). Inferred only: "
              "one Apple M-series performance core is usually 1.0 to 2.0 times one 2.1 GHz Xeon core on scalar code, "
              "and float64 SIMD is narrower on NEON (2 lanes) than AVX-512 (8 lanes, used by XLA here), so the ratio "
              "for these float64 kernels may be below 1. Running run_f.sh, run_g.sh and run_f32.sh once in a Mac box (about 45 min) "
              "replaces this guess with a factor."}

# =========================================================================== F
f1, f16, f64, f256 = (load(f"f_sim_B{b}") for b in (1, 16, 64, 256))
fp, ff32, ff48 = load("f_plug_m256"), load("f_fit_T32"), load("f_fit_T48")
fn = {k: load(f"f_net_{k}") for k in ("C48_b256", "C24_b256", "C48_b64")}
F = {"world": "round5/foundry/tnca.py: 64 x 64, 2 kinds, 4 substeps per tick, float64; exam shapes of round6/foundryexam "
              "(DESIGN.md section 3): burn-in 300, 17 observed frames, 16-tick test program, queries 1, 2, 4, 8, 16; "
              "a full episode = 300 + 16 + 16 = 332 member-ticks"}
sim = {}
for b, d in ((1, f1), (16, f16), (64, f64), (256, f256)):
    if d is None:
        continue
    sim[str(b)] = {"compile_s_start300": R(d["compile_s_start_300"], 1), "compile_s_run16": R(d["compile_s_run_16"], 1),
                   "run16_s": R(med(d, "run16_s")), "run16_s_range": [R(x) for x in spread(d, "run16_s")],
                   "member_ticks_per_s_run16": R(d["member_ticks_per_s_run16"], 1),
                   "start300_s": R(med(d, "start300_s")), "start300_s_range": [R(x) for x in spread(d, "start300_s")] if "start300_s" in d else None,
                   "start300_n": d.get("start300_s", {}).get("n"),
                   "episode_s": R(med(d, "episode_332_s")), "episode_s_range": [R(x) for x in spread(d, "episode_332_s")] if "episode_332_s" in d else None,
                   "peak_rss_mb": R(d["rss_mb_peak"], 0), "source": f"raw/f_sim_B{b}.json"}
F["sim_measured"] = sim
f32 = {}
for b in (1, 16, 64):
    d = load(f"f_sim_B{b}_f32")
    if d:
        f32[str(b)] = {"member_ticks_per_s_run16": R(d["member_ticks_per_s_run16"], 1), "run16_s": R(med(d, "run16_s")),
                       "run16_s_range": [R(x) for x in spread(d, "run16_s")], "state_dtype": d.get("state_dtype"),
                       "compile_s_run16": R(d["compile_s_run_16"], 1), "peak_rss_mb": R(d["rss_mb_peak"], 0),
                       "source": f"raw/f_sim_B{b}_f32.json"}
F["sim_float32_measured"] = f32 or None
rates = [v["member_ticks_per_s_run16"] for v in sim.values()]
mt_best = max(rates) if rates else None
ep1 = sim.get("1", {}).get("episode_s")
ep_b = None
if "16" in sim and sim["16"].get("episode_s"):
    ep_b = sim["16"]["episode_s"] / 16
F["derived"] = {
    "member_ticks_per_s_best": R(mt_best, 1),
    "member_ticks_per_s_best_from": "max over B of sim_measured.*.member_ticks_per_s_run16",
    "episode_s_one": ep1, "episode_s_one_from": "sim_measured.1.episode_s (one Lab episode alone)",
    "episode_s_batched": R(ep_b), "episode_s_batched_from": "sim_measured.16.episode_s / 16",
    "lab_8_episodes_s": R(8 * ep_b) if ep_b else None, "lab_8_from": "8 x episode_s_batched",
    "item_future_one_member_s": sim.get("1", {}).get("run16_s"),
    "item_future_256_members_s": sim.get("256", {}).get("run16_s"),
    "null_pool_512_s": R(512 * 332 / mt_best, 0) if mt_best else None,
    "null_pool_512_from": "512 episodes x 332 member-ticks / member_ticks_per_s_best (input-free episodes of 512 public "
                          "screened worlds; no screen needed: the screened worlds are public lists, round6/foundryexam/results/pool.json and "
                          "round6/foundrylong/inputs/sel_2028.json)",
    "member_ticks_per_s_full_episode_batched": R(332 / ep_b, 1) if ep_b else None,
    "R_box_note": "the spec's R_box (member-ticks per second of the 2-CPU box, float64): run16 at B = 16 and the full "
                  "episode at B = 16 agree within 3%; batching beyond 16 does not help on CPU (B = 64, 256 are slower)",
    "full_episode_348_ticks_s": R(348 / (332 / ep_b), 2) if ep_b else None,
    "full_episode_348_from": "foundrylong's episode (300 + 16 + 32 ticks) at the batched full-episode speed",
    "instance_build_ring_shape_s": R((64 * 332 + 64 * 16 * 16 + 256 * 332) * ep_b / 332, 0) if ep_b else None,
    "instance_build_ring_shape_from": "exam_configs/ring_r4.json shape (64 items, R 16, n_clim 256): 64 item histories x 332 + "
                                      "64 x 16 replicate futures x 16 ticks + 256 climatology episodes x 332 member-ticks, at the "
                                      "batched full-episode speed",
    "instance_build_pilot_shape_s": R((32 * 332 + 32 * 12 * 16 + 96 * 332) * ep_b / 332, 0) if ep_b else None,
    "instance_build_pilot_shape_from": "foundryexam per hidden world: 32 items, R 12, n_clim 96 (run_fx.py FULL)",
}
if fp:
    imp = fp["seconds_python_start_to_imports_done"]
    F["plug_in_item_m256"] = {
        "what": fp["note"], "source": "raw/f_plug_m256.json",
        "imports_s": R(imp, 2), "compile_s": R(fp["compile_s_predict"], 1), "predict_s": R(med(fp, "predict_s"), 1),
        "predict_s_range": [R(x, 1) for x in spread(fp, "predict_s")], "member_ticks": fp["member_ticks"],
        "member_ticks_per_s": R(fp["member_ticks_per_s"], 1), "peak_rss_mb": R(fp["rss_mb_peak"], 0),
        "T_JIT_item_s": R(imp + fp["compile_s_predict"], 1),
        "T_JIT_from": "imports + compile of the plug-in predictor in a fresh process (the spec's F_T_JIT, x86)",
        "item_wall_s": R(imp + fp["compile_s_predict"] + med(fp, "predict_s"), 0),
        "item_cpu_s_upper": R(2 * (imp + fp["compile_s_predict"] + med(fp, "predict_s")), 0),
        "item_from": "imports + compile + predict (a fresh process per item, as public/_item.py starts one); CPU seconds "
                     "at most 2 x wall on 2 cores",
        "pool_artifact_mb_float32": R(fp["pool_bytes_float32"] / 2 ** 20, 1),
        "ring_limits_for_comparison": "physim2_env/exam_configs/ring_r4.json predictor: cpu_seconds 30, wall_seconds 60, memory_gib 4, artifact_mib 64",
        "oracle_style_plug_from_hidden_state_s": sim.get("256", {}).get("run16_s"),
        "oracle_style_from": "sim_measured.256.run16_s (256 members x 16 ticks from a given state; the grader's O and plug-in references)"}
F["nets"] = {}
for k, d in fn.items():
    if d:
        F["nets"][k] = {"ms_per_step": R(med(d, "ms_per_step"), 0), "ms_per_step_range": [R(x, 0) for x in spread(d, "ms_per_step")],
                        "compile_s": R(d["compile_s_step_dispatch"], 1), "n_params": d["n_params"], "peak_rss_mb": R(d["rss_mb_peak"], 0),
                        "batch": d["examples_per_step"], "what": d["note"], "source": f"raw/f_net_{k}.json"}
for T, d in ((32, ff32), (48, ff48)):
    if d:
        F[f"fit_step_T{T}"] = {"grad_step_s": R(med(d, "grad_step_s"), 1), "grad_step_s_range": [R(x, 1) for x in spread(d, "grad_step_s")],
                               "n": d["grad_step_s"]["n"], "compile_s": R(d["compile_s_value_and_grad"], 1), "peak_rss_mb": R(d["rss_mb_peak"], 0),
                               "shape": d["shape"], "n_fit_coordinates": d["n_fit_coordinates"], "grad_finite": d["grad_finite"],
                               "what": d["note"], "source": f"raw/f_fit_T{T}.json"}
# the agent's recipes (pilots' sizes) and the box
SRC_FX = "round6/foundryexam/run_fx.py FULL and SB_FULL (job 004/005 sizes); GPU speed: results/job/r6-foundryexam-004_full_progress.txt ('P P0 g0: 9.6 ms per step (2 nets, batch 256)')"
SRC_FL = "round6/foundrylong/run_fl.py FULL (p0_steps, batch_p0) and run_fl2.py FULL (w_cands, w_starts, w_steps, w_eb, w_M, w_A, w_k, w_pool, w_respin)"
step256 = F["nets"].get("C48_b256", {}).get("ms_per_step")
step64 = F["nets"].get("C48_b64", {}).get("ms_per_step")
step_small = F["nets"].get("C24_b256", {}).get("ms_per_step")
fit_s = F.get("fit_step_T32", {}).get("grad_step_s")
spin16 = sim.get("16", {}).get("start300_s")
if ep_b and step256 and fit_s:
    world_s = 72 * ep_b                                                  # 64 training episodes + 8 gate episodes
    screen_s = 40910 / mt_best                                           # member-ticks per screened world found, with the pre-screen
    fit_eff = fit_s + (spin16 or 0) / 50.0                               # respin of the pool every 50 steps
    F["recipes"] = {
        "prior_world_s": R(world_s, 0), "prior_world_from": "72 episodes (the pilot's 64 training episodes per world + 8 gate episodes, "
                                                             "run_fx.py FULL epw, gate_M) x episode_s_batched",
        "screen_per_world_found_s": R(screen_s, 0), "screen_from": "40,910 member-ticks per screened world found with the weights-only pre-screen "
                                                                "(foundryexam/results/summary.json compute.member_ticks_per_candidate.with_prescreen) / member_ticks_per_s_best; "
                                                                "not needed when the screened prior is handed over as a public list",
        "p0_step_s": R(step256 / 1e3, 3), "p0_step_small_net_s": R(step_small / 1e3, 3) if step_small else None,
        "fit_step_s_with_respin": R(fit_eff, 1), "fit_from": "fit_step_T32.grad_step_s + sim_measured.16.start300_s / 50 (pool respin every 50 steps, fl_w.fit_batch)",
        "pilot_recipes_cpu_hours": {
            "P0_foundryexam_armP": {"worlds": 210, "episodes": 210 * 64, "steps": 12000, "batch": 256, "nets": 2,
                                    "sim_h": R(210 * world_s / 3600, 1), "train_h_one_net": R(12000 * step256 / 3.6e6, 1),
                                    "gpu_note": "A100: 9.6 ms per step for 2 nets in lockstep", "source": SRC_FX},
            "P0_16_worlds_foundryexam": {"worlds": 16, "steps": 6000, "batch": 256, "sim_h": R(16 * world_s / 3600, 2),
                                         "train_h_one_net": R(6000 * step256 / 3.6e6, 2), "source": SRC_FX + " (P0w: 6,000 steps; nw_curve 16, 64)"},
            "P0_1000_worlds_foundrylong": {"worlds": 1000, "episodes": 64000, "steps": 40000, "batch": 256,
                                           "sim_h": R(1000 * world_s / 3600, 0), "train_h_one_net": R(40000 * step256 / 3.6e6, 0), "source": SRC_FL},
            "FT_32_foundryexam": {"steps": 400, "batch": 64, "train_h": R(400 * step64 / 3.6e6, 2) if step64 else None, "source": "round6/foundryexam/run_fx.py FULL steps_FT[32], batch_world"},
            "FT_512_foundryexam": {"steps": 2400, "batch": 64, "train_h": R(2400 * step64 / 3.6e6, 2) if step64 else None, "source": "round6/foundryexam/run_fx.py FULL steps_FT[512], batch_world"},
            "W_fit_foundrylong_stage2": {"starts": 4, "steps": 200, "fit_h": R(4 * 200 * fit_eff / 3600, 1),
                                         "plus_prescreen": "32 candidate weight vectors scored on 8 Lab episodes (eval_batch), not timed",
                                         "source": SRC_FL}},
        "box": {}}
    for mins in BOX_MIN:
        s = 60.0 * mins
        F["recipes"]["box"][str(mins)] = {
            "full_episodes_if_only_simulating": int(s / ep_b),
            "prior_worlds_listed_if_only_simulating": int(s / world_s),
            "prior_worlds_screened_by_agent_if_only_simulating": int(s / (world_s + screen_s)),
            "p0_steps_batch256_if_only_training": int(s / (step256 / 1e3)),
            "p0_steps_small_net_if_only_training": int(s / (step_small / 1e3)) if step_small else None,
            "fit_steps_if_only_fitting": int(s / fit_eff),
            "from": "box seconds / (episode_s_batched, prior_world_s, prior_world_s + screen_per_world_found_s, p0_step_s, "
                    "p0_step_small_net_s, fit_step_s_with_respin); each column assumes the whole box does that one thing"}
    F["research_budget"] = {
        "one_full_episode_s": R(ep_b, 3), "unit": "a full level-0 episode = 332 member-ticks at the batched speed",
        "box_in_full_episodes": {str(m): int(60 * m / ep_b) for m in BOX_MIN},
        "pilot_P0_210_worlds_in_full_episodes": 65492,
        "pilot_P0_from": "foundryexam/results/summary.json compute.with_prescreen.P0[210].total_episodes_with_burn_in (screen + gate + training)",
        "pilot_P0_16_worlds_in_full_episodes": 4990,
        "lab_512_in_full_episodes": 512}
    if fp:
        pr = fp["member_ticks"] / med(fp, "predict_s")                  # member-ticks per second of the plug-in (nudge included)
        F["prediction_budget"] = {
            "U_item": "256 samples x (P + H) member-ticks: 256 x 32 = 8,192 (foundryexam shape, H = 16); 256 x 48 = 12,288 (foundrylong, H = 32)",
            "brute_force_s_H16_measured": F["plug_in_item_m256"]["predict_s"],
            "brute_force_s_H32_from_measured_rate": R(256 * 48 / pr, 0),
            "brute_force_from": "f_plug_m256 predict_s (assimilate 16 ticks + forecast 16, 256 members); H = 32 at the same member-tick rate",
            "from_hidden_state_256x16_s": sim.get("256", {}).get("run16_s"),
            "ring_item_limit": "30 CPU-s and 60 s wall (exam_configs/ring_r4.json); 30 CPU-s is at most 15 s of a 2-core box",
            "ring_cpu_limit_as_fraction_of_brute_force_H16": R(15.0 / F["plug_in_item_m256"]["predict_s"], 2)}
OUT["F"] = F

# =========================================================================== G
g = {b: load(f"g_sim_B{b}") for b in (1, 16, 64, 256)}
gn = {k: load(f"g_net_{k}") for k in ("C48_b128", "C24_b128")}
G = {"world": "round6/dials/dialsA/xlaw.XRunner: 128 x 128 Flow-Lenia gliders with wind (gworld), 20 substeps per tick, "
              "hidden stress conversion at eta 4, object tracker every tick, float64; exam shapes of round6/dials/dialsA2 "
              "(DECLARED.md R2, R5): burn-in 50, 17 observed frames, 16-tick held-out program, answers at 8, 12, 16; "
              "a full episode = 50 + 16 + 16 = 82 member-ticks"}
gs = {}
for b, d in g.items():
    if d is None:
        continue
    T = d["args"]["T"]
    gs[str(b)] = {"T": T, "compile_s_start50": R(d["compile_s_start_50"], 1), "compile_s_run": R(d["compile_s_run_T"], 1),
                  "run_s": R(med(d, "run_T_s"), 2), "run_s_range": [R(x, 2) for x in spread(d, "run_T_s")],
                  "member_ticks_per_s": R(d["member_ticks_per_s_run"], 2), "core_s_per_member_tick": R(d["core_s_per_member_tick_run"], 4),
                  "start50_s": R(med(d, "start50_s"), 2), "start50_n": d.get("start50_s", {}).get("n"),
                  "episode_s": R(med(d, "episode_82_s"), 2), "episode_s_range": [R(x, 2) for x in spread(d, "episode_82_s")] if "episode_82_s" in d else None,
                  "peak_rss_mb": R(d["rss_mb_peak"], 0), "source": f"raw/g_sim_B{b}.json"}
G["sim_measured"] = gs
grates = [v["member_ticks_per_s"] for v in gs.values()]
gmt = max(grates) if grates else None
if gmt:
    gep = 82 / gmt
    G["derived"] = {
        "member_ticks_per_s_best": R(gmt, 2), "core_s_per_member_tick_best": R(2 / gmt, 4),
        "earlier_figure": "0.15 CPU-s per member-tick (round5/agentenv/results/cost.json cpu_s_per_member_tick.gliders.value)",
        "episode_s_one": gs.get("1", {}).get("episode_s"), "episode_s_best": R(gep, 2),
        "episode_from": "82 / member_ticks_per_s_best (B = 1; batching is slower on CPU, and B = 256 peaks at 4.6 GB)",
        "lab_8_episodes_s": R(8 * gep, 0), "lab_96_episodes_s": R(96 * gep, 0),
        "lab_96_from": "dialsA2 DECLARED R5: 32 mix + 32 free + 32 designed per truth",
        "item_future_16_ticks_one_member_s": gs["1"]["run_s"] if gs.get("1", {}).get("T") == 16 else R(16 / gmt, 2),
        "item_future_16_ticks_256_members_s": R(256 * 16 / gmt, 0),
        "null_pool_512_s": R(512 * 82 / gmt, 0), "null_pool_from": "512 x 82 / member_ticks_per_s_best",
        "plug_in_item_m256_s": R(256 * 32 / gmt, 0),
        "plug_in_from": "256 members x (16 assimilated + 16 forecast ticks) / member_ticks_per_s_best; no state-assimilation code "
                        "exists for gliders, so this is the simulation alone (a lower bound)",
        "family_point_s": R(8 * gep, 0), "family_point_from": "8 episodes per theta point (dialsA2 R7) x episode_s_best (B = 1 is the fastest on CPU)",
        "P0_family_768_points_h": R(768 * 8 * gep / 3600, 1), "P0_family_from": "768 x 8 episodes (dialsA2 R7, public family)",
        "gpu_note": "A100: about 1,300 member-ticks per second (round6/dials/dialsA/results/job/progress.txt: 'family pub: 768 points x 8 episodes, 385s')",
        "instance_build_dialsA2_shape_s": R(2 * (48 * 82 + 48 * 12 * 16 + 48 * 82) / gmt, 0),
        "instance_build_dialsA2_from": "per truth and eta two exams of 48 items, R 12, n_clim 48 (DECLARED R2): histories x 82 + "
                                       "replicate futures x 16 + climatology x 82 member-ticks / member_ticks_per_s_best",
        "instance_build_ring_shape_s": R((64 * 82 + 64 * 16 * 16 + 256 * 82) / gmt, 0),
        "T_JIT_sim_item_s": R(max([d["seconds_python_start_to_imports_done"] + d["compile_s_run_T"] for d in g.values() if d]), 1),
        "T_JIT_from": "imports + compile of the run (largest over the batch sizes measured; a fresh item process pays it); "
                      "the 50-tick start compiles separately (sim_measured.*.compile_s_start50)"}
G["nets"] = {}
for k, d in gn.items():
    if d:
        G["nets"][k] = {"ms_per_step": R(med(d, "ms_per_step"), 0), "ms_per_step_range": [R(x, 0) for x in spread(d, "ms_per_step")],
                        "n": d["ms_per_step"]["n"], "compile_s": R(d["compile_s_step"], 1), "n_params": d["n_params"],
                        "peak_rss_mb": R(d["rss_mb_peak"], 0), "what": d["note"], "source": f"raw/g_net_{k}.json"}
gstep = G["nets"].get("C48_b128", {}).get("ms_per_step")
gstep_s = G["nets"].get("C24_b128", {}).get("ms_per_step")
if gmt and gstep:
    G["recipes"] = {"base_net_24000_steps_h_one_net": R(24000 * gstep / 3.6e6, 1),
                    "base_net_from": "dialsA2 run_a2.py FULL rungs[0] = 24,000 steps (up to 192,000), batch 128 x 4 draws; 3 seeds, 6 base nets",
                    "box": {}}
    for mins in BOX_MIN:
        s = 60.0 * mins
        G["recipes"]["box"][str(mins)] = {"full_episodes_if_only_simulating": int(s / gep),
                                          "theta_points_x8_if_only_simulating": int(s / (8 * gep)),
                                          "net_steps_batch128_if_only_training": int(s / (gstep / 1e3)),
                                          "net_steps_small_net_if_only_training": int(s / (gstep_s / 1e3)) if gstep_s else None}
    G["research_budget"] = {"one_full_episode_s": R(gep, 2), "box_in_full_episodes": {str(m): int(60 * m / gep) for m in BOX_MIN},
                            "pilot_P0_in_full_episodes": "about 2,300 (roadmap/DECISIONS.md decision 2); dialsA2's public family is 6,144 (R7)",
                            "S_in_full_episodes": "about 20,000 (roadmap/DECISIONS.md decision 2)"}
OUT["G"] = G
ep_f = 33 * 8 * 8 * 3 * 4 + 2 * 33 * 8 * 8 * 2 * 4 + (16 + 15 + 13 + 9 + 1) * 3 * 4    # fx_net device arrays X, CU, CtU + index
OUT["memory"] = {
    "box_caps": "4 GB memory (docker --memory; physim2_env/profiles.py box_memory_gb), /workspace 1 GiB in memory (tmpfs: its "
                "pages count against the same memory cap)",
    "peak_rss_mb": {"F_sim_B1_B16_B64_B256": [F["sim_measured"].get(b, {}).get("peak_rss_mb") for b in ("1", "16", "64", "256")],
                    "F_plug_m256": F.get("plug_in_item_m256", {}).get("peak_rss_mb"),
                    "F_net_C48_b256_1024_episodes": F["nets"].get("C48_b256", {}).get("peak_rss_mb"),
                    "F_fit_T32": F.get("fit_step_T32", {}).get("peak_rss_mb"), "F_fit_T48": F.get("fit_step_T48", {}).get("peak_rss_mb"),
                    "G_sim_B1_B16_B64_B256": [G["sim_measured"].get(b, {}).get("peak_rss_mb") for b in ("1", "16", "64", "256")],
                    "G_net_C48_b128_1024_episodes": G["nets"].get("C48_b128", {}).get("peak_rss_mb")},
    "F_net_dataset_bytes_per_episode": ep_f,
    "F_net_dataset_from": "fx_net.make_dataset/device_dataset arrays: X (33, 8, 8, 3) + CU, CtU (33, 8, 8, 2) float32 + 54 index rows x 3 int32",
    "F_net_dataset_gb": {"P0[16] (1,024 episodes)": R(1024 * ep_f / 1e9, 3), "P0[210] (13,440 episodes)": R(13440 * ep_f / 1e9, 2),
                         "box_180_min_of_episodes (3,967)": R(3967 * ep_f / 1e9, 2),
                         "note": "the host numpy copy made by make_dataset can double this until it is freed"},
    "saved_episode_bytes": {"F_obs_float32": 33 * 192 * 4, "F_program_dense_float32": 32 * 128 * 4, "F_program_4_ticks": 4 * 128 * 4,
                            "G_obs_float32": 33 * 336 * 4, "G_program_dense_float32": 32 * 128 * 4},
    "states": {"F_member_float64_bytes": 2 * 64 * 64 * 8, "F_pool_256_float32_mb": R(256 * 2 * 64 * 64 * 4 / 2 ** 20, 1),
               "G_member_field_float64_bytes": 2 * 128 * 128 * 8, "G_pool_256_float32_mb_field_only": R(256 * 2 * 128 * 128 * 4 / 2 ** 20, 1)},
    "checkpoints": "nets of 40k to 150k float32 parameters (n_params in nets.*): under 2 MB with Adam's moments"}
OUT["image"] = load("wheels")
json.dump(OUT, open(os.path.join(HERE, "timing.json"), "w"), indent=1)
print(json.dumps(OUT, indent=1)[:6000])
