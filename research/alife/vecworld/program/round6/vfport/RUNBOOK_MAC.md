# RUNBOOK for the Mac session: PhySim v2 on verifiers

What this is: the exact commands to (1) install, (2) run the scripted, model-free smoke test on Docker at $0,
(3) run ONE rollout of a cheap model on the ring smoke exam with a stock harness. Steps 1 and 2 were run in the
cloud container (Linux, Docker 29.9.2) on 10 Nov 2026; nothing here was run on a Mac, and step 3 was not run
anywhere (no model call was made in this study). Ask the lead before step 3.

All commands run from the study folder:

```sh
cd <physim checkout>/research/alife/vecworld/program/round6/vfport
```

The package reuses round 5's `agentenv` by import, so it must be installed from a checkout of the repository
(`../../round5/agentenv` and `../../../vw1` must exist next to it), not from a wheel.

## 0. What you need

- Docker Desktop running (`docker info` answers). The coordinator's note says 28.3.3 is installed.
- `uv`; Python 3.12 (uv fetches it).
- About 1.5 GB of disk for the image and its build cache; 4 free cores for a few minutes.
- For step 3 only: Prime inference credentials in the environment, as for the PhySim v1 rollouts.

## 1. Install (about 3 minutes)

```sh
uv sync --locked                      # fresh .venv here: verifiers 0.3.2.dev163 (the wheel v1 pins), numpy, scipy, jax
: > docker/extra-ca.crt               # empty file: no TLS-intercepting proxy on the Mac
docker build -f docker/Dockerfile.ring -t physim2-ring:1 docker/
docker run --rm physim2-ring:1 python -c "import numpy, scipy, jax; print(numpy.__version__, scipy.__version__, jax.__version__)"
```

Expected last line: `2.5.4 1.18.1 0.12.0.1`. The image is the ONE image of both boxes (python:3.12-slim plus
numpy, scipy, jax; about 560 MB on Linux x86_64). Do not build `docker/Dockerfile.network`: on the Mac verifiers
builds its own network helper (`localhost/verifiers-network:1`, from alpine) at the first run.

The hidden side lives in a store OUTSIDE the repository. Make one fresh ring instance (a new 256-bit secret and
a new hidden theta are drawn now; about 10 s):

```sh
export PHYSIM2_STORE=$HOME/physim2-store          # hidden values: never inside the checkout, delete after the pilot
uv run --no-sync python -B tools/make_instances.py --store $PHYSIM2_STORE --world ring --config smoke_ring --n 1 --prefix mac-ring
```

Expected: one JSON line with `"instance_id": "mac-ring-w0"`, `"n_items": 64`, `"R": 16`, and a
`secret_commitment` (public). `$PHYSIM2_STORE/index.json` now lists the instance (pointers only).

## 2. Scripted smoke test on Docker ($0, no model, no upload; about 15 minutes)

Both tools call `vf-eval physim2-env --env.id isolated-verifier` with the Docker runtime and the
`physim2-script` harness; they set `push = false`, `PRIME_RUNS_MODE=disabled` and remove `PRIME_API_KEY` from the
child's environment (tools/vfrun.py).

```sh
export SCRATCH=$HOME/physim2-scratch
# (a) one world, three policies through the whole route (about 5 minutes)
uv run --no-sync python -B tools/prove.py --store $PHYSIM2_STORE --scratch $SCRATCH/proof --worlds 1 \
    --prefix mac-ring --policies D,P0,C --out $SCRATCH/proof_mac.json
# (b) the boundary checks and the probes, on their own small instance (about 10 minutes)
uv run --no-sync python -B tools/check_probe.py --store $PHYSIM2_STORE --scratch $SCRATCH/probe --out $SCRATCH/probe_mac.json
```

Expected from (a): three lines `D: [..]`, `C: [..]`, `P0: [..]` (one skill per world, on the K-to-O scale), then
the table on the K-to-C scale, for example (cloud container, one world) `{"O": 1.10, "K": 0.0, "D": 0.45, "C": 1.0,
"P0": 0.90}`. The numbers differ on the Mac: the hidden world is new. What must hold, in `$SCRATCH/proof_mac.json`:

- `all_graded` and `all_ok` are `true`; `n_failed_items_total` is `0`;
- `per_world[0].rollouts.D.lab_ticks_used` is `392` (8 episodes of 49 ticks), `.P0.lab_ticks_used` is `0`;
- `per_world[0].rollouts.*.grade.layers` is `{"rlimits": true, "uid": 1000, "cleanup": true}`;
- `per_world[0].same_submission_through_round5_grader.identical` is `true` (the same frozen submission graded by
  round 5's own grader and by this route gives the same 64 x 7 scores). This check runs agentenv's local
  sandbox, written for Linux (namespaces, prlimit); on the Mac it may record an error or differ in the last
  digits (another numpy build than the box's). Report what it says; it is not a blocker there.
- D below P0 below C, O above C (ordering, not values).

Expected from (b): the last line reports `"failed_round5": []` and `"failed_new": []`. Open questions that only
the Mac can answer are in `$SCRATCH/probe_mac.json`:

- `checks_new.c_*` : the network cut on macOS Docker (memo unknown 4). On Linux the box reaches its proxy on
  127.0.0.1; on macOS it goes through `host.docker.internal` and one iptables rule
  (verifiers/v1/runtimes/docker/__init__.py:431-446). `c_control_uncut_container_reaches_host_listener` must be
  `true` for the other `c_*` checks to mean anything; if the control fails on Docker Desktop, say so (the
  listener is bound on the Mac, the container looks for it at its default gateway) and judge the cut from
  `evidence.c_agent_box_net` and `evidence.c_verifier_box_net_all_items` alone.
- `evidence.verifier_box_staging.world_writable_paths_fixed`: in the cloud container `docker exec` ran with umask
  0, so setup files were world-writable until staging fixed them. Report the number seen on the Mac.

If a run stops with `docker run failed: ... net.ipv6.conf.all.disable_ipv6`, the Docker VM has no IPv6: put
`tools/docker_shim` first on PATH (`tools/vfrun.py` does it by itself on Linux only) and report it.

A single scripted rollout without the tools:

```sh
uv run --no-sync vf-eval @ configs/scripted_ring.toml --no-rich -o $SCRATCH/single
```

## 3. ONE rollout of a cheap model, stock harness (ask the lead first)

Model: `qwen/qwen3.5-35b-a3b` (the coordinator's cheap Qwen). Harness: the stock `bash` harness of verifiers (it
supports MCP tools, so the model sees the laboratory as the tool `call` of server `lab`, next to `bash` and
`edit`). Exam: the ring smoke exam, one hidden world, one hour of envelope.

```sh
uv run --no-sync vf-eval @ configs/qwen_ring_bash.toml --dry-run          # resolves the config, calls nothing
uv run --no-sync vf-eval @ configs/qwen_ring_bash.toml --no-rich -o $SCRATCH/qwen
```

The config sets `push = false`, no retries at any level (a rerun would give the agent a fresh laboratory
budget), `max_turns = 40`, `max_total_tokens = 1500000`, `max_output_tokens = 60000`. To use `claude_code` or
`codex` as in the v1 rollouts, change `[env.agent.harness]` (`id`, `version`) and nothing else; those harnesses
were not read for this study.

**Cost.** The caps bound the spend at 1.5 M tokens in total, of which at most 60 k are output. With p_in and
p_out dollars per million tokens, the bound is 1.5 x p_in + 0.06 x p_out dollars. The price of this model was not
available in the cloud container: read it from Prime's Models API before the run. As an illustration only, at
$0.20 in and $0.60 out per million the bound is $0.34. The scripted S policy needs 4 laboratory calls per episode
and 8 episodes, so a model that works from Python scripts should stay far below the cap. Evaluator compute is
about 1.5 CPU-minutes (64 items in the verifier box).

**What to check in the trace** (`$SCRATCH/qwen/<run>/traces.jsonl`, one line; `traces[0]`):

1. `ok` is `true` and `rewards.skill.score` exists. If the reward is missing the rollout is ungraded: record it
   as K and do NOT rerun on the same instance.
2. `info.physim2.network_restricted` and `info.physim2.verifier_box.network_restricted` are `true`.
3. `info.physim2.lab`: `ticks_used` at most 400, `infrastructure_errors` equal to 0, `submitted` true or false.
   Whether the model reached the laboratory from its own Python (`physim2.Lab()`), through direct tool calls, or
   both, is visible in the tool calls of the transcript: this is the half of memo unknown 2 that only a model
   run can settle. Report which route it used.
4. `info.physim2.submission.source`: `agent_submission` (the model called `lab.submit`) or `final_collection`;
   `stop_condition`: `frozen` means the rollout was ended by the task's stop hook right after the submit (that
   hook has never run before this rollout: confirm it fired at the next model call, as the memo inferred).
5. `info.physim2.grade`: `n_failed` (0 for a valid predictor), `layers` as above, `items_with_leftovers`,
   `skill_vs_O` equal to the reward.
6. The task row `task.data` holds an instance id and a commitment, no theta, no secret: `grep` the run directory
   for the first 10 characters of each theta value and for the secret from
   `$PHYSIM2_STORE/mac-ring-w0/hidden/instance.json`; expect no hit.
7. Token counts (`num_input_tokens`, `num_output_tokens`) against the caps, and the wall time per stage in `timing`.

For the table next to the model's score, run the references on the same instance (step 2a with
`--policies S,D,P0,PM,C,null`); the model's per-item scores are in
`$PHYSIM2_STORE/mac-ring-w0/hidden/grades/<trace id>.npz`.

## 4. After the pilot

```sh
rm -rf $PHYSIM2_STORE $SCRATCH          # the store holds theta and the secret of a pilot that must never be reused
```

Results that leave the Mac carry scores, counters and commitments only, with `PILOT_NEVER_REUSE_AS_EXAM`.
