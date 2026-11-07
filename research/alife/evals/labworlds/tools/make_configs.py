"""Rollout configs for the lab bundles, limits sized from the cost survey (/home/user/evalwork/costs/costs.json).

    python make_configs.py OUT_DIR          writes <bundle>.codex.toml and <bundle>.prime-agent.toml per bundle, limits.json

Modelled on configs/physim/eval.toml (budgets, attempts, agent limits, runtime, retries) and bf_trail_lab.toml (one
selected preparation, one task; its num_tasks key is not an EvalConfig field in the pinned Verifiers, so it is omitted); the bundle is a local path (env.taskset.task.tools.bundle). A TOML holds one harness
block, so each bundle has two files: Codex (shell coding interface, as in the BF case study) and Prime Agent (IPython
interface, PRIME_AGENT.md). Rules:

- predictor cpus 4; memory_gib = max(2, ceil(3 x (64-member batch arrays + 110 MiB interpreter) / 1024)), with
  4 GiB for the rods (whose 64-member batch is ~0.85 GiB);
- cpu_seconds = 3 x the faithful predictor's longest case at 64 members, rounded up to 100 s (fed vortex: the measured
  552 CPU-s run of c015, which exceeds the survey's 456 estimate);
- wall_seconds = ceil(cpu_seconds / cpus x 1.5) to 10 s;
- scoring_timeout derived (taskset.scoring_timeout: max(7200, cases x (wall_seconds + 60) + 900));
- agent_timeout: at least eval.toml's 86400 s and at least 2x the evaluator time of a heavy investigation
  (300 experiments of 50 tu, run serially at the survey's CPU-s per member-tu), rounded up to an hour;
- max_total_tu: eval.toml's 50000 unless simulating it would take more than 75% of the agent timeout (the rest is
  left for model turns, analysis and predictor development); then the largest multiple of 5000 tu that fits.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

COSTS = json.loads(Path("/home/user/evalwork/costs/costs.json").read_text())
B = Path("/home/user/evalwork/bundles")
IMAGE = "python:3.11-slim@sha256:db3ff2e1800a8581e2c48a27c3995339d47bdf046da21c7627accd3d51053a93"
BUNDLES = {   # config name: (bundle dir, costs.json suite key, label)
    "fedvortex": ("/home/user/evalwork/vortex_eval/suite/bundle", "vortex_bundle", "c53 fed vortices (committed fed-vortex bundle, 15 cases)"),
    "vortex_main": (str(B / "vortex_main"), "vortex_main", "fed vortices with heredity and selection, main suite"),
    "vortex_formation": (str(B / "vortex_formation"), "vortex_formation", "fed vortices with heredity and selection, formation suite"),
    "pm_main": (str(B / "pm_main"), "pm_main", "phase_membrane, main suite (iter2)"),
    "pm_formation": (str(B / "pm_formation"), "pm_formation", "phase_membrane, formation suite"),
    "cips_main": (str(B / "cips_main"), "cips_main", "CIPS-iso, main suite (iter2)"),
    "cips_formation": (str(B / "cips_formation"), "cips_formation", "CIPS-iso, formation suite"),
    "rods_main": (str(B / "rods_main"), "rods_main", "Marangoni rods, main suite (iter2)"),
    "rods_formation": (str(B / "rods_formation"), "rods_formation", "Marangoni rods, formation suite"),
}
CPUS = 4
HEAVY_TU = 300 * 50
BUDGET_TU = 50000
AGENT_FLOOR = 86400


def limits(key):
    c = COSTS["suites"][key]
    fp = c["faithful_predictor"]
    longest = fp["longest_case_cpu_s"]
    if key == "vortex_bundle":
        longest = max(longest, COSTS["faithful_bundle_run"]["cpu_s"])
    cpu_s = int(math.ceil(3 * longest / 100.0) * 100)
    wall_s = int(math.ceil(cpu_s / CPUS * 1.5 / 10.0) * 10)
    batch = fp["batched64_array_memory_mb"]
    mem = max(2, math.ceil(3 * (batch + 110) / 1024))
    if key.startswith("rods"):
        mem = max(mem, 4)
    per_tu = c["cpu_s_per_member_tu"]["used"]
    heavy = HEAVY_TU * per_tu
    agent = max(AGENT_FLOOR, int(math.ceil(2 * heavy / 3600.0) * 3600))
    budget = BUDGET_TU
    if BUDGET_TU * per_tu > 0.75 * agent:
        budget = int((0.75 * agent / per_tu) // 5000 * 5000)
    cases = c["cases"]
    return dict(cases=cases, cpu_s_per_member_tu=per_tu, faithful_longest_case_cpu_s=longest,
                batch64_mib=batch, predictor=dict(cpu_seconds=cpu_s, wall_seconds=wall_s, cpus=CPUS, memory_gib=mem,
                                                  artifact_mib=64, file_mib=20),
                heavy_investigation_s=heavy, agent_timeout=agent, max_total_tu=budget,
                full_budget_sim_h=budget * per_tu / 3600, faithful_wall_single_process_s=longest,
                derived_scoring_timeout=max(7200.0, cases * (wall_s + 60.0) + 900.0))


def toml(name, bundle, label, lim, harness):
    p = lim["predictor"]
    shell = harness == "codex"
    # tool_timeout bounds one laboratory call; validate/submit run the 7 public cases in a fresh predictor sandbox.
    harness_block = ('[env.agent.harness]\nid = "codex"\ntool_timeout = 1800\n' if shell else
                     '[env.agent.harness]\nid = "prime-agent"\ntool_timeout = 1800\n')
    return f'''# PhySim lab bundle "{name}": {label}.
# Harness: {"Codex (shell coding interface; the BF case study's harness for GPT models)" if shell else "Prime Agent (IPython coding interface, PRIME_AGENT.md)"}.
# Select the model on the CLI (--model). This configuration makes model API calls and uses Prime sandboxes when executed.
# Limits from /home/user/evalwork/costs/costs.json via /home/user/evalwork/bundles/scripts/make_configs.py; see
# /home/user/evalwork/bundles/README.md. Faithful predictor, longest case at 64 members: {lim["faithful_longest_case_cpu_s"]:.0f} CPU-s.
model = "YOUR_MODEL_ID"
num_rollouts = 1
max_concurrent = 1
push = false

[env.taskset]
id = "physim"

[env.taskset.task]
output_root = "outputs/r6/artifacts"
agent_image = "{IMAGE}"
coding_interface = "{"shell" if shell else "ipython"}"
setup_timeout = 900
# 2x a heavy investigation (300 experiments x 50 tu = {lim["heavy_investigation_s"] / 3600:.1f} h of serial evaluator time), at least 24 h.
agent_timeout = {lim["agent_timeout"]}
finalize_timeout = 900
# scoring_timeout is left unset: derived by taskset.scoring_timeout = max(7200, cases x (wall_seconds + 60) + 900) = {lim["derived_scoring_timeout"]:.0f} s.

[env.taskset.task.agent_resources]
cpu = 4
memory = 8

[env.taskset.task.tools]
bundle = "{bundle}"
max_experiments = 1000
# Simulating the full budget takes {lim["full_budget_sim_h"]:.1f} h of evaluator time.
max_total_tu = {lim["max_total_tu"]}
max_validation_attempts = 128
max_submission_attempts = 128
reward_precision = 2.0

[env.taskset.task.tools.predictor_limits]
# 3x the faithful predictor's longest case (CPU); wall = cpu / cpus x 1.5; memory for a 64-member batch ({lim["batch64_mib"]:.0f} MiB) with margin.
cpu_seconds = {p["cpu_seconds"]}
wall_seconds = {p["wall_seconds"]}
cpus = {p["cpus"]}
memory_gib = {p["memory_gib"]}
artifact_mib = {p["artifact_mib"]}
file_mib = {p["file_mib"]}

[env.agent]
# Generous exploration defaults; increase these together for longer investigations.
max_turns = 1024
max_output_tokens = 1048576

[env.agent.timeout]
# Overrides the task's agent timeout when set (verifiers agent.py); kept equal to agent_timeout above.
rollout = {lim["agent_timeout"]}

{harness_block}
[env.agent.runtime]
type = "prime"
image = "{IMAGE}"
workdir = "/workspace"
cpu = 4
memory = 8
allow = []

[env.agent.retries]
max_retries = 0

[env.retries]
max_retries = 0
'''


def main(out: Path):
    out.mkdir(parents=True, exist_ok=True)
    table = {}
    for name, (bundle, key, label) in BUNDLES.items():
        lim = limits(key)
        table[name] = dict(lim, bundle=bundle, costs_key=key, label=label)
        for harness in ("codex", "prime-agent"):
            (out / f"{name}.{harness}.toml").write_text(toml(name, bundle, label, lim, harness))
    (out / "limits.json").write_text(json.dumps(table, indent=1) + "\n")
    for name, row in table.items():
        p = row["predictor"]
        print(f"{name:17s} cpu {p['cpu_seconds']:6d} wall {p['wall_seconds']:5d} mem {p['memory_gib']} GiB  "
              f"scoring {row['derived_scoring_timeout']:7.0f}  agent {row['agent_timeout']}  tu {row['max_total_tu']}  "
              f"heavy {row['heavy_investigation_s'] / 3600:.1f} h  full budget {row['full_budget_sim_h']:.1f} h")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
