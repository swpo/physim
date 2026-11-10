# Running a PhySim-v2 rollout with an LLM (Mac session)

Written in the cloud container, which has no Docker daemon and no model access: the Python side below is
tested there end to end with scripted agents (`results/proof_*.json`); the container files in this folder are
**not run** and the first use is their test. Paths are relative to
`research/alife/vecworld/program/round5/agentenv/` in a checkout of swpo/physim.

## What a rollout is

| piece | where it runs | what it holds |
|---|---|---|
| hidden instance | `lab` container, named volume `hidden` | theta, the 256-bit secret, the frozen exam (items, truths) |
| Lab server | `lab` container, no network | the real world behind `/ipc/lab.sock` (ticks, nats, validate, submit) |
| agent | `agent` container, 4 CPUs, 8 GiB | `/workspace`: `TASK.md`, the public `physim2` package, `submission/` |
| grader | `lab` container after the agent stops | one process per item, unprivileged uid, CPU and memory limits |

The agent never sees the `hidden` volume. Nothing hidden is written to the repository; `rollout_<name>.json` and
the table hold scores, counters and commitment hashes only. Delete the `hidden` volume when the instance is
retired (`docker volume rm`), or keep it sealed for re-grading.

## Once

```sh
cd research/alife/vecworld/program/round5/agentenv
docker build -t physim2:cpu -f mac/Dockerfile mac
# add your harness CLI (the one used for PhySim v1: codex or prime-agent) to mac/Dockerfile.agent, then
docker build -t physim2-agent:cpu -f mac/Dockerfile.agent mac
export REPO=/path/to/physim COMPOSE="docker compose -f $PWD/mac/compose.yaml"
```

Check the simulator speed in the container. The task statement quotes 0.15 CPU-s per gliders member-tick
(0.16 measured in the cloud container); if the Mac's number differs by more than 1.5x, say so in the report,
because the envelope then buys a different amount of simulation:

```sh
RUN=/tmp/none NAME=x $COMPOSE run --rm lab python -B run_rollout.py bench --world gliders
```

## Stage 0: mechanics test (ring world, small model, minutes, cents)

```sh
export RUN=$HOME/physim2-runs/mech-ring NAME=qwen; mkdir -p $RUN
$COMPOSE run --rm lab python -B run_rollout.py prepare --world ring --config configs/smoke_ring.json --run /run_dir
$COMPOSE run --rm lab python -B run_rollout.py workspace --run /run_dir --name $NAME --owner 0
$COMPOSE up -d lab
$COMPOSE run --rm agent <HARNESS COMMAND with the prompt below>      # stop it after 45 minutes at most
$COMPOSE stop lab
$COMPOSE run --rm lab python -B run_rollout.py finalize --run /run_dir --name $NAME
$COMPOSE run --rm lab python -B run_rollout.py table --run /run_dir --names $NAME
```

Pass: the agent's turns start, `lab.card()` answers, ticks and nats are charged (`usage` in
`rollout_<name>.json`), `submit` or the final collection freezes a predictor, grading writes a score. The
scripted reference on the same instance, for comparison (no model, 10 s each):

```sh
for P in S D P0 PM C null; do
  $COMPOSE run --rm lab python -B run_rollout.py rollout --run /run_dir --name $P --policy $P \
    --sizes '{"n_lab": 8, "n_design": 256, "k_design": 2, "n_train": 512}'; done
$COMPOSE run --rm lab python -B run_rollout.py table --run /run_dir --names $NAME,S,D,P0,PM,C,null
```

(`rollout --policy` runs the scripted agent inside the lab container through the same socket and sandbox code;
it is for references only. In a container without CAP_SYS_ADMIN the sandbox falls back to uid drop and
resource limits, which the result records under `layers`.)

## Stage 1: first dry run (gliders, one fresh hidden world, 4 cores x 8 h)

```sh
export RUN=$HOME/physim2-runs/dry-gliders-w0 NAME=sol; mkdir -p $RUN
$COMPOSE run --rm lab python -B run_rollout.py prepare --world gliders --config configs/dryrun_gliders.json --run /run_dir
#   draws theta and the secret, checks viability, builds 64 items x 16 truths + 128 climatology runs:
#   about 29,000 member-ticks = 1.2 core-hours on one core. To build it on a GPU instead, see README "Next steps".
$COMPOSE run --rm lab python -B run_rollout.py workspace --run /run_dir --name $NAME --owner 0
$COMPOSE up -d lab
$COMPOSE run --rm agent <HARNESS COMMAND>        # wall-clock limit 8 h (the envelope in TASK.md)
$COMPOSE stop lab
$COMPOSE run --rm lab python -B run_rollout.py finalize --run /run_dir --name $NAME
```

A second model on the same hidden world: repeat from `workspace` with another NAME (each name has its own
tick and nats budget; the exam items are the same). The exam profile is `configs/exam_gliders.json` (24 h).

The reference ladder (K, D, P0, prior mean, S, C, O; sigma and rho) for the same instance: on CPU it is
about 12 core-hours per world at 1,024 training episodes per policy, so run it as one GPU job (README, next
steps) or at reduced size with `rollout --policy ... --sizes '{"n_train": 256, "n_design": 128, "chunk": 8}'`.

## Prompt for the harness

    You are in /workspace. Read TASK.md and complete the task it describes. You have 4 CPU cores, no GPU and
    8 hours. Work autonomously; when your predictor is ready, call lab.submit("submission").

Nothing else is needed: the agent uses Python (`import physim2`), not MCP tools. Record from the harness: model
id, turns, input and output tokens, wall clock; from `rollout_<name>.json`: `usage`,
`submitted_before_finalization`, `grade`.

## What to send back

`rollout_<name>.json` and the `table` output for each rollout (no hidden values in either), the harness's token
counts, and `workspaces/<name>/` (the agent's code and notes) as an archive outside git.

## Known gaps

- Network: the agent container has open outbound network (the harness needs the model API). v1 restricted the
  sandbox to the framework's routes; an egress allowlist for the model endpoint is the missing piece.
- Limits on the agent are the container's `cpus`/`mem_limit` and your wall-clock stop; turn and token limits
  are the harness's.
- A Verifiers taskset (Prime sandboxes, as v1) is not written. The mapping is direct: task setup =
  `evaluator.build_workspace.build` + upload + the pinned `pip install` of mac/Dockerfile; the trusted tool
  process = `evaluator.lab_service.LabService` (its seven operations in place of v1's four MCP tools, or the
  socket forwarded into the sandbox); reward = `run_rollout.finalize`. About a day for the Mac session, after
  stage 1 has shown what agents need.
