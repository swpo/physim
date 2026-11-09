"""Arithmetic behind ROADMAP.md: compute thresholds on the gliders pilot, the two
acceptance ratios, and rollout costs. Reads the round-4 SBI summary; no simulation.

Run: /home/user/evalwork/vecworld/vw1/.venv/bin/python roadmap_envelope.py
"""
import json
import pathlib

SBI = pathlib.Path(
    "/home/user/physim/research/alife/vecworld/program/round4/sbi/results/summary.json"
)
OUT = pathlib.Path(__file__).with_suffix(".json")

CPU_S_PER_MEMBER_TICK = 0.136  # program/track2/EXAM.md section 5 (bench: 0.13-0.16)
GPU_MEMBER_TICKS_PER_S = 1600  # program/gpu/bench/README.md
ROLLOUT_TOKENS_USD = (7.6, 23.0)  # evals/labworlds/rollout_kit/README.md (Sol, Astra)
GPU_8H_USD = (15.92, 18.80)  # 8 h at $1.99-2.35 per hour

d = json.loads(SBI.read_text())
mt = d["job"]["member_ticks"]
n_truth = d["config"]["n_truth"]
oes = {k: v["mean"] for k, v in d["prediction"]["oes"].items()}


def core_hours(member_ticks):
    return member_ticks * CPU_S_PER_MEMBER_TICK / 3600.0


# Simulation a contestant needs for each policy, for ONE hidden world.
p0_set = mt["sims_prior_pred"]  # 1,024 episodes at prior draws
design = mt["design"]  # 8,192 design episodes (also the amortised net's set)
post_set = mt["sims_post2"] // n_truth  # 1,024 episodes at posterior draws
pipeline = design + post_set
envelope = 4 * 24 * 3600 / CPU_S_PER_MEMBER_TICK  # 4 cores for 24 h

compute = {
    "prior_predictive_set_member_ticks": p0_set,
    "prior_predictive_set_core_hours": round(core_hours(p0_set), 2),
    "scripted_pipeline_member_ticks_per_hidden_world": pipeline,
    "scripted_pipeline_core_hours": round(core_hours(pipeline), 1),
    "scripted_pipeline_hours_on_4_cores": round(core_hours(pipeline) / 4, 1),
    "envelope_4cores_24h_member_ticks": int(envelope),
    "envelope_over_pipeline": round(envelope / pipeline, 2),
    "envelope_over_prior_predictive_set": round(envelope / p0_set, 1),
    "gpu_seconds_for_pipeline": round(pipeline / GPU_MEMBER_TICKS_PER_S),
}

# Acceptance ratios from the pilot's OES table (same world, so the oracle
# normalisation is common to numerator and denominator).
ratios = {}
for fam in ("net", "amort", "ridge"):
    c = oes[f"{fam}|true"]
    p0 = oes[f"{fam}|prior_pred"]
    data512 = oes.get(f"{fam}|real@512")
    null = max(p0, data512) if data512 is not None else p0
    s2 = oes[f"{fam}|post@2"]
    s8 = oes[f"{fam}|post@8"]
    ratios[fam] = {
        "C": c,
        "P0": p0,
        "D_512": data512,
        "science_share_vs_P0": round((c - p0) / c, 3),
        "science_share_vs_better_null": round((c - null) / c, 3),
        "scripted_share_at_2_episodes": round((s2 - p0) / (c - p0), 2),
        "scripted_share_at_8_episodes": round((s8 - p0) / (c - p0), 2),
    }

# Rollout batch: 2 models x 3 hidden worlds x 3 arms.
n_roll = 18
rollouts = {
    "n_rollouts": n_roll,
    "tokens_usd": [round(n_roll * ROLLOUT_TOKENS_USD[0]), round(n_roll * ROLLOUT_TOKENS_USD[1])],
    "tokens_usd_half_each_model": round(9 * ROLLOUT_TOKENS_USD[0] + 9 * ROLLOUT_TOKENS_USD[1]),
    "gpu_arm_usd_6_rollouts": [round(6 * GPU_8H_USD[0]), round(6 * GPU_8H_USD[1])],
}

# Depth: one more field level with block factor b at fixed statistical resolution.
depth = {f"b={b}": b**4 for b in (2, 4, 8)}

out = {
    "source": str(SBI),
    "compute_gliders": compute,
    "acceptance_ratios_gliders": ratios,
    "rollout_batch": rollouts,
    "depth_cost_factor_area_times_time": depth,
}
OUT.write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
