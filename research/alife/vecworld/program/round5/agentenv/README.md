# agentenv: the PhySim-v2 exam as an agent-facing environment (round 5, track 2)

Prepares the first dry run with a real LLM agent. No GPU and no model calls were used ($0). Everything below
ran on CPU in the cloud container with scripted agents. Numbers and their sources: `results/summary.json`.

## What is here

| path | role |
|---|---|
| `TASK.md.tmpl` | the task statement for an agent with no background; rendered per world and config into `TASK.md` (declares the compute envelope, budgets, submission format, scoring, limits) |
| `physim2/` | the **public** package copied into the agent's workspace: `Lab` client, world modules (`world_ring.py`, `world_gliders.py`: law, coarse-grainings, prior, program mix, `Simulator`), `predict_runner.py` |
| `evaluator/` | the **hidden side**: `instance.py` (secret and theta drawn at run time, frozen exam), `lab_service.py` (the real world behind a socket: ticks, nats, validate, submit), `submission.py` + `sandbox.py` (one sandboxed process per request), `grader.py`, `acceptance.py` (sigma, rho), `build_workspace.py` |
| `agents/` | `reference_agent.py` (policies S, D, P0, PM, C and the null agent, all through the agent's interface), `ridge_family.py` (the one predictor family), `inference.py` (shrunk synthetic likelihood), `probe_agent.py` (misbehaves on purpose) |
| `run_rollout.py`, `prove.py`, `check_probe.py`, `tests_tcp.py` | one rollout; the end-to-end proof; the boundary test; the TCP transport test |
| `acceptance_round4.py`, `cost_model.py`, `make_summary.py` | sigma and rho on gliders at full size from round 4's saved scores; costs; the summary |
| `configs/` | `smoke_ring.json` (mechanics), `smoke_gliders.json`, `dryrun_gliders.json` (4 cores x 8 h), `exam_gliders.json` (4 cores x 24 h), `probe_ring.json` |
| `mac/` | `RUNBOOK.md`, `Dockerfile`, `Dockerfile.agent`, `compose.yaml` for the Mac session (not run here) |

## The interface

- **Agent side** (`TASK.md`): `physim2.Lab()` with `card`, `usage`, `reset(label)`, `advance(inputs)`,
  `experiment(label, inputs)`, `validate(path)`, `submit(path)`; `physim2.load_world()` for the public law and
  `Simulator`; deliverable `submission/predict.py` with
  `predict(history, program, queries, n_samples, seed) -> {level: (n_samples, n_times, d)}`.
- **Hidden side**: a separate process holds theta and a 256-bit secret (`vw.secret`); every block of inputs is
  validated as a whole (bounds, nats per tick, per episode and in total, ticks) before anything runs.
  `validate` runs the predictor on two public example requests (format, limits, reproducibility; no accuracy
  feedback); `submit` freezes a hashed copy; without a submit the grader collects `submission/` (as v1).
- **Grader**: frozen `HistoryExam` items (history items, R replicate truths, climatology pool), one fresh
  process per item with CPU, memory, wall-clock and size limits; a failed request is scored as K. Reference
  table: K, D(N), P0, PM (prior mean), S(N), C, O, with pooled L, skill, per-cell OES, sigma and rho.
- **Isolation** (`evaluator/sandbox.py`): resource limits always; as root also a mount namespace in which only
  the workspace and the socket exist, no network, and an unprivileged uid. In a container deployment the same
  boundary is two containers (`mac/compose.yaml`).

## Run it

```sh
PY=/home/user/evalwork/vecworld/vw1/.venv/bin/python; S=/some/scratch/dir
$PY -B prove.py --world ring --config configs/smoke_ring.json --worlds 4 --scratch $S/ring \
    --sizes '{"n_lab": 8, "n_design": 256, "k_design": 2, "n_train": 512}' --out results/proof_ring.json
$PY -B check_probe.py --scratch $S --out results/probe_ring.json
$PY -B prove.py --world gliders --config configs/smoke_gliders.json --worlds 1 --policies S,D,P0,C,null \
    --sizes '{"n_lab": 4, "n_design": 24, "k_design": 1, "n_train": 12, "chunk": 4}' --scratch $S/gl --out results/proof_gliders.json
$PY -B acceptance_round4.py; $PY -B cost_model.py; $PY -B make_summary.py
rm -rf $S        # the scratch directory holds the hidden instances
```

## Results (9-10 Nov 2026; CPU, x86_64, jax 0.12.0.1 float64; scratch instances deleted)

Skill is `(L(K) - L) / (L(K) - L(C))` with L the pooled fair energy score; sources in `results/summary.json`.

| run | size | S | P0 | prior mean | D at budget | null agent | O | sigma | rho |
|---|---|---|---|---|---|---|---|---|---|
| ring proof | 4 hidden worlds, 256 items, R 16; budget 400 ticks (8 episodes); 512 training episodes | 0.988 | 0.964 | 0.970 | 0.343 | 0.008 | 1.083 | 0.036 (SE 0.009 over worlds) | 0.67 (SE 0.38) |
| gliders smoke | 1 world, 8 items, R 6; 4 lab episodes; 12 training episodes | 0.963 | 0.978 | not run | 0.770 | -0.236 | 1.862 | 0.02 (noise) | undetermined |

- Every policy went through the agent's interface inside the sandbox (unprivileged uid, mount, network and PID
  namespaces, the repository and the hidden directory absent), submitted itself, and was graded with no failed
  item. The gliders bundle is 37 files, 418 kB, and imports with the source trees hidden.
- `results/probe_ring.json`: an agent that misbehaves on purpose; 34 of 34 boundary checks pass (budgets
  charge nothing on rejection, limits kill, hidden files and the network are unreachable from the agent and
  from a predictor, the laboratory closes on submit).
- The gliders run is a smoke test: with 8 items and 12 training episodes its ordering of S and P0 is noise.
  Full-size acceptance on gliders, recomputed with `evaluator/acceptance.py` from round 4's saved scores
  (512 items, 8 worlds): sigma = 0.065 (SE 0.007) for the ridge family at 2 to 8 episodes, 0.030 for the net,
  0.039 for the amortised net; rho = 0.78 (SE 0.09) at 2 episodes and 0.95 (SE 0.03) at 8 for the ridge.
  Both bars fail, as the roadmap says; the roadmap's own arithmetic (per-cell OES means) is reproduced beside it.
- Costs (`results/cost.json`): 0.164 CPU-s per gliders member-tick measured in the agent sandbox. Four cores
  for 8 hours buy 768,000 member-ticks (9,365 exam-shaped episodes): 9.1 times P0's training set, 6.1 times the
  shrunk scripted recipe, 1.0 times round 4's full recipe; 24 hours buy three times that.

## Choice for the first dry run

1. **Mechanics test on the ring world** with a small model (`configs/smoke_ring.json`): minutes, cents.
2. **Dry run on gliders**, one fresh hidden world, 4 cores x 8 h (`configs/dryrun_gliders.json`: 64 items,
   R 16, 4,000 lab ticks). Gliders is the only world with an exam (prior, viability rule, program mix, scales,
   reference ladder), and it fits a CPU sandbox. The phase membrane is 12 times cheaper per tick but about 5.5
   times per episode (150 ticks of formation before an episode can start) and has no exam yet: cost is not a
   reason to wait for it.
3. Commands and container files: `mac/RUNBOOK.md`.

## What failed or is untested

- The first scripted inference fitted its summaries and its likelihood on the same 12 design episodes and
  collapsed on a wrong point (`results/gliders_S_insample_failure.json`); it now cross-fits. At smoke size the
  inference is still uninformative (cross-validated R^2 of the summaries below zero), so S equals P0 there.
- A process that is PID 1 of a PID namespace ignores the soft CPU limit; the limit is now hard (probe check).
- The null agent is at 0.008 on the ring but -0.24 on the gliders smoke run (a pool of 12 frames, 8 items).
- Not run: the Docker files, any LLM harness, a Verifiers taskset, gliders at dry-run size (about 12
  core-hours per world for the reference ladder on CPU).
- JAX used about 1.5 cores with thread caps set (FFT threads); CPU accounting needs `taskset` or a container limit.
- A pilot secret of an earlier study is committed at `program/track2/harness/hidden/secret.hex` (not this
  study's file): that pilot must never serve as an exam.

## Next steps

1. Mac: stage 0, then stage 1 with the two pilot models on one hidden gliders world (tokens about $31 if v1's
   $7.60 and $23 per rollout carry over; evaluator CPU 1.2 core-hours for the exam and 25 minutes for the lab).
2. References for a live exam: P0 and the prior-mean policy do not depend on the hidden world, so one public
   GPU job can train them (168,000 member-ticks, under $1). S and D run on the Mac through this code (1.3 h on
   4 cores at the shrunk size). C needs theta: compute it after the instance is retired, or behind the sealer of
   workstream D. Job outputs go to a public branch, so no live theta may pass through the GPU runner.
3. A batched (`jax.vmap`) path in `world_gliders.Simulator` for GPU use; an egress allowlist for the agent
   container; a Verifiers taskset if Prime sandboxes are wanted (about a day on the Mac).
4. New worlds plug in as one module with the interface of `physim2/world_ring.py` (about 200 lines).
