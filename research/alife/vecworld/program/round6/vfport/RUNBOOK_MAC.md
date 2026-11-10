# RUNBOOK for the Mac session: PhySim v2 on verifiers

**HOLD.** Do not start before the coordinator says the independent host-safety audit of this folder is done
(task "Host-safety audit of the verifiers port"). This file describes the code of the commit that carries it.

What this is: the exact commands to (1) install, (2) run the scripted, model-free smoke test on Docker at $0,
(3) run ONE rollout of a cheap model on the ring smoke exam with a stock harness. Steps 1 and 2 were run in the
cloud container (Linux, Docker 29.9.2) on 10 Nov 2026 with this code; **nothing here was run on a Mac**, and step 3
was not run anywhere (no model call was made in this study). Ask the lead before step 3.

## Safety: what this runbook does to the Mac itself

- **Nothing in this runbook kills a process or deletes a file of the Mac outside the two folders named below.**
  Everything the exam does to processes and files (running the predictor, killing what it leaves, deleting its
  files) happens inside Docker containers that verifiers creates for this run and removes afterwards.
- Why this is spelled out: on 10 Nov 2026 a unit test in the cloud container started the exam's item driver as
  root directly on that machine, and the driver's cleanup deleted the home directory of an unused account there
  (README section 8). The driver now refuses to do anything of the kind unless four separate conditions hold
  that only a container prepared by this environment meets, and no command below starts it on the host.
- **Do NOT run on the Mac:** `tools/check_units.py` (it refuses to start outside the build container),
  `tools/check_driver.py` (not needed; it only works inside a container it starts), anything under `redteam/`
  (attack scripts of the red team, written for the cloud container). Do not run any command with `sudo`.
- Folders this runbook creates and, in step 4, deletes. They are written out in full in every command, never
  through a variable:
  - `$HOME/physim2-pilot-20261110/store` (the hidden side of the pilot instances)
  - `$HOME/physim2-pilot-20261110/scratch` (run outputs: traces, logs)
- Every command or tool below that REMOVES something:

  | Who | What it removes | Where |
  |---|---|---|
  | `docker run --rm ...` (step 1; the control of step 2b) | the test container it just started | Docker |
  | verifiers, during every rollout | the containers it created itself, named `vf-<32 hex digits>` (`docker rm -f`): the agent's box, the verifier box, and one box per exam item | Docker |
  | `tools/vfrun.py` (called by the two tools of step 2) | `$HOME/physim2-pilot-20261110/scratch/<proof or probe>/runs/<run name>` of an earlier call with the same name, and only if that folder holds nothing but vf-eval's own files (`traces.jsonl`, `configs`, `logs`) | scratch |
  | `tools/prove.py` | `$HOME/physim2-pilot-20261110/store/<instance>/work/reference_<policy>` (its own copy of a reference submission) | store |
  | `tools/make_instances.py` | `.../store/<instance>/hidden/examples.npz`, a file it wrote a moment before | store |
  | Python's `tempfile` | temporary folders the same process created (under `$TMPDIR`) | temp |
  | step 4, by hand | the two folders above; optionally the Docker images | disk, Docker |

- What runs on the Mac itself, as your user, outside any container: `uv`, `docker` (client), `vf-eval` with this
  taskset (it starts one laboratory process per rollout, which simulates the hidden world and answers the agent's
  requests), and the two tools of step 2. They create files in the two folders and in `./.venv`; they change
  nothing else. `tools/check_probe.py` opens one TCP listener on 127.0.0.1 for the minutes it runs (it accepts a
  connection, records the peer address and closes it; on Linux it must bind every interface, on the Mac it
  does not).
- If anything asks for a password, wants `sudo`, or reports "refused: not a disposable box", stop and report.

All commands run from the study folder:

```sh
cd <physim checkout>/research/alife/vecworld/program/round6/vfport
```

The package reuses round 5's `agentenv` by import, so it must be installed from a checkout of the repository
(`../../round5/agentenv` and `../../../vw1` must exist next to it), not from a wheel.

## 0. What you need

- Docker Desktop running (`docker info` answers). The coordinator's note says 28.3.3 is installed.
- `uv`. Python 3.12 (uv fetches it).
- About 1.5 GB of disk for the image and its build cache; 4 free cores for about half an hour.
- For step 3 only: Prime inference credentials in the environment, as for the PhySim v1 rollouts.

## 1. Install (about 3 minutes)

```sh
uv sync --locked --python 3.12        # fresh .venv here: verifiers 0.3.2.dev163 (the wheel v1 pins), numpy, scipy, jax
: > docker/extra-ca.crt               # empty file: no TLS-intercepting proxy on the Mac
docker build -f docker/Dockerfile.ring -t physim2-ring:1 docker/
docker run --rm physim2-ring:1 python -c "import numpy, scipy, jax; print(numpy.__version__, scipy.__version__, jax.__version__)"
```

Expected last line: `2.5.4 1.18.1 0.12.0.1`. The image is the ONE image of every box (python:3.12-slim plus numpy,
scipy, jax; about 560 MB on Linux x86_64). Do not build `docker/Dockerfile.network`: on the Mac verifiers builds
its own network helper (`localhost/verifiers-network:1`, from alpine) at the first run.

The hidden side lives in a store OUTSIDE the repository. Make one fresh ring instance (a new 256-bit secret and
a new hidden theta are drawn now; about 10 s):

```sh
mkdir -p "$HOME/physim2-pilot-20261110/scratch"
export PHYSIM2_STORE="$HOME/physim2-pilot-20261110/store"     # read by vf-eval in steps 2 and 3
uv run --no-sync python -B tools/make_instances.py --store "$HOME/physim2-pilot-20261110/store" --world ring --config smoke_ring --n 1 --prefix mac-ring
```

Expected: one JSON line with `"instance_id": "mac-ring-w0"`, `"n_items": 64`, `"R": 16`, and a
`secret_commitment` (public). `$HOME/physim2-pilot-20261110/store/index.json` now lists the instance (pointers only).

## 2. Scripted smoke test on Docker ($0, no model, no upload; about 30 minutes)

Both tools call `vf-eval physim2-env --env.id isolated-verifier` with the Docker runtime and the
`physim2-script` harness; they set `push = false`, `PRIME_RUNS_MODE=disabled` and remove `PRIME_API_KEY` from the
child's environment (tools/vfrun.py).

```sh
# (a) one world, three policies through the whole route, then C once more with one box per exam item (about 10 minutes)
uv run --no-sync python -B tools/prove.py --store "$HOME/physim2-pilot-20261110/store" --scratch "$HOME/physim2-pilot-20261110/scratch/proof" \
    --worlds 1 --prefix mac-ring --policies D,P0,C --box-check C --no-cross-check --out "$HOME/physim2-pilot-20261110/scratch/proof_mac.json"
# (b) the boundary checks and the probes, on their own small instance (37 short rollouts; 16 minutes in the cloud container)
uv run --no-sync python -B tools/check_probe.py --store "$HOME/physim2-pilot-20261110/store" --scratch "$HOME/physim2-pilot-20261110/scratch/probe" \
    --out "$HOME/physim2-pilot-20261110/scratch/probe_mac.json"
```

Both tools can be started again after an interruption: a finished rollout is never repeated.
`--no-cross-check` leaves out the comparison with round 5's own grader, which would run a reference predictor in
round 5's Linux sandbox on the Mac itself; that comparison was made in the cloud container (README section 4.1).

Expected from (a): lines `D: [..]`, `P0: [..]`, `C: [..]` (one skill per world, on the K-to-O scale), a line
`C (one box per item, world 0): ..`, then the table on the K-to-C scale, for example (cloud container, one world)
`{"O": 1.10, "K": 0.0, "D": 0.45, "C": 1.0, "P0": 0.90}`. The numbers differ on the Mac: the hidden world is new.
What must hold, in `$HOME/physim2-pilot-20261110/scratch/proof_mac.json`:

- `all_graded` and `all_ok` are `true`; `n_failed_items_total` is `0`;
- `per_world[0].rollouts.D.lab_ticks_used` is `392` (8 episodes of 49 ticks), `.P0.lab_ticks_used` is `0`;
- `per_world[0].rollouts.*.grade.layers` is `{"rlimits": true, "uid": <a number from 20000 to 59999>, "cleanup": true}`;
- `one_box_per_item_check_world_0.C`: `identical_per_item_scores` is `true`, `grade.item_boxes` is `64`,
  `grade.infrastructure_failed_items` is `0`. Report `grade.item_box_wall_s_mean` (2.7 s in the cloud container):
  it is the price of the default grading mode on the Mac;
- D below P0 below C, O above C (ordering, not values).

Expected from (b): the last line reports `"failed_round5": []` and `"failed_new": []`. Open questions that only
the Mac can answer are in `$HOME/physim2-pilot-20261110/scratch/probe_mac.json`:

- `checks_new.c_*`: the network cut on macOS Docker (memo unknown 4). On Linux the box reaches its proxy on
  127.0.0.1; on macOS it goes through an alias of the host and one iptables rule
  (verifiers/v1/runtimes/docker/__init__.py:431-446). `c_control_uncut_container_reaches_host_listener` must be
  `true` for the other `c_*` checks to mean anything: the control container looks for the listener at its default
  gateway and at `host.docker.internal`. If the control fails on Docker Desktop, say so and judge the cut from
  `evidence.c_agent_box_net` and `evidence.c_verifier_box_net_all_items` alone. This part of the tool was written
  for the Mac without a Mac to try it on.
- `evidence.verifier_box_staging.container_evidence`: what told the driver it was inside a container (in the cloud
  container: `/.dockerenv` and the control group of pid 1). If the list is empty on the Mac, every grading rollout
  stops with "the box is not recognised as a disposable box": report it; nothing is damaged.
- `evidence.verifier_box_staging.world_writable_paths_fixed` and `.box_limits`: report both (in the cloud container
  `docker exec` ran with umask 0, and Docker set no process limit: `pids_max` is `max`).
- `evidence.a2_channels_one_box_per_item`: `mark_was_read` all `false`, `dirs_touched_after_staging` all empty,
  `lo_rx_packets` all below 1000, `pid_step` all small. These are the four between-item channels the reviews
  found; with one box per item they must not carry on the Mac either.

If a run stops with `docker run failed: ... net.ipv6.conf.all.disable_ipv6`, the Docker VM has no IPv6: put
`tools/docker_shim` first on PATH (`tools/vfrun.py` does it by itself on Linux only) and report it.

A single scripted rollout without the tools (policy D on the instance named in the config; it can run once:
a second run of the same agent on the same instance is refused, see `single_use` in README section 7):

```sh
uv run --no-sync vf-eval @ configs/scripted_ring.toml --no-rich -o "$HOME/physim2-pilot-20261110/scratch/single"
```

## 3. ONE rollout of a cheap model, stock harness (ask the lead first)

Model: `qwen/qwen3.5-35b-a3b` (the coordinator's cheap Qwen). Harness: the stock `bash` harness of verifiers (it
supports MCP tools, so the model sees the laboratory as the tool `call` of server `lab`, next to `bash` and
`edit`). Exam: the ring smoke exam, one hidden world, one hour of envelope.

```sh
uv run --no-sync vf-eval @ configs/qwen_ring_bash.toml --dry-run -o "$HOME/physim2-pilot-20261110/scratch/qwen-dry"   # resolves the config, calls nothing
uv run --no-sync vf-eval @ configs/qwen_ring_bash.toml --no-rich -o "$HOME/physim2-pilot-20261110/scratch/qwen"
```

(Without `-o`, vf-eval writes `outputs/` inside the public checkout, and every trace names the worker's Prime team
id; `outputs/` is ignored by git here, but keep run outputs out of the checkout anyway.)

The config sets `push = false`, no retries at any level (a rerun would give the agent a fresh laboratory
budget), `max_turns = 40`, `max_total_tokens = 1500000`, `max_output_tokens = 60000`. The token caps are checked
before each model call (verifiers/v1/session.py:88-89), so the real bound is the cap plus one request. The run can
be made ONCE on this instance: `single_use` (on by default) refuses a second rollout of the same model and
harness on `mac-ring-w0`, before any model call. To use `claude_code` or `codex` as in the v1 rollouts, change
`[env.agent.harness]` (`id`, `version`) and nothing else; those harnesses were not read for this study.

**Cost.** The caps bound the spend at 1.5 M tokens in total, of which at most 60 k are output, plus one request.
With p_in and p_out dollars per million tokens, the bound is 1.5 x p_in + 0.06 x p_out dollars. The price of this
model was not available in the cloud container: read it from Prime's Models API before the run. As an
illustration only, at $0.20 in and $0.60 out per million the bound is $0.34. The scripted S policy needs 4
laboratory calls per episode and 8 episodes, so a model that works from Python scripts should stay far below the
cap. Evaluator compute after the model stops: 3 validation calls, then 64 exam items, each in a fresh container:
about 3 minutes of wall time in the cloud container (2.7 s per item box), about 1 CPU-minute.

**What to check in the trace** (`$HOME/physim2-pilot-20261110/scratch/qwen/<run>/traces.jsonl`, one line; `traces[0]`):

1. `ok` is `true` and `rewards.skill.score` exists. If the reward is missing the rollout is ungraded (for example
   the model killed its own harness): run
   `uv run --no-sync python -B tools/settle.py --store "$HOME/physim2-pilot-20261110/store" --run-dir "$HOME/physim2-pilot-20261110/scratch/qwen/<run>"`,
   which records it as K, and do NOT rerun on the same instance (the environment would refuse anyway).
2. `info.physim2.network_restricted` and `info.physim2.verifier_box.network_restricted` are `true`;
   `info.physim2.single_use` is `true`; `info.physim2.item_isolation` is `box`.
3. `info.physim2.lab`: `ticks_used` at most 400, `infrastructure_errors` equal to 0, `submitted` true or false.
   Whether the model reached the laboratory from its own Python (`physim2.Lab()`), through direct tool calls, or
   both, is visible in the tool calls of the transcript: this is the half of memo unknown 2 that only a model
   run can settle. Report which route it used, and what the tool operations `validate` and `submit` answered
   (they now run the public check in the model's box and return its report).
4. `info.physim2.submission.source`: `agent_submission` (the model's submit was accepted) or `final_collection`;
   `stop_condition`: `frozen` means the rollout was ended by the task's stop hook right after the submit (that
   hook has never run before this rollout: confirm it fired at the next model call, as the memo inferred).
5. `info.physim2.grade`: `validation.ok` (`true` unless the predictor fails one of the three public example calls,
   in which case every item is K and `reason` says which call), `n_failed` (0 for a valid predictor), `layers` as
   above, `isolation` equal to `box`, `item_boxes` equal to 64, `infrastructure_failed_items` equal to 0,
   `skill_vs_O` equal to the reward.
6. The task row `task.data` holds an instance id and a commitment, no theta, no secret: `grep` the run directory
   for the first 10 characters of each theta value and for the secret from
   `$HOME/physim2-pilot-20261110/store/mac-ring-w0/hidden/instance.json`; expect no hit.
7. Token counts (`num_input_tokens`, `num_output_tokens`) against the caps, and the wall time per stage in `timing`.

For the table next to the model's score, the references of step 2a ran on the same instance (add S, PM and null
with `--policies S,D,P0,PM,C,null`; policies already run are not repeated); the model's per-item scores are in
`$HOME/physim2-pilot-20261110/store/mac-ring-w0/hidden/grades/<trace id>.npz`.

## 4. After the pilot

The store holds theta and the secret of a pilot that must never be reused. Remove exactly the two folders, each
only if it is what this runbook made (the first command checks that; if it prints nothing, stop and look):

```sh
test -f "$HOME/physim2-pilot-20261110/store/index.json" && test -d "$HOME/physim2-pilot-20261110/scratch" && echo "both folders are the pilot's"
rm -rf "$HOME/physim2-pilot-20261110/store" "$HOME/physim2-pilot-20261110/scratch"
rmdir "$HOME/physim2-pilot-20261110"
docker ps -a --filter name=vf- --format '{{.Names}}'      # expected: nothing (verifiers removed its containers)
# optional, frees about 700 MB: docker rmi physim2-ring:1 localhost/verifiers-network:1
```

Results that leave the Mac carry scores, counters and commitments only, with `PILOT_NEVER_REUSE_AS_EXAM`.
