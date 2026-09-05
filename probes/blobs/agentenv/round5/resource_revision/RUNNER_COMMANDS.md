# Runner handoff — commands prepared, not executed

Use the project interpreter and the native v1 `eval` entry point from:

```text
cd /Users/spoho/Documents/prime/test/physim
```

The installed parser accepted the commands below. See
[native_cli_validation.json](native_cli_validation.json). Validation only
constructed configs; it did not run `main`/`run_eval`, call a model, start a
runtime, or allocate a GPU. Endpoint credentials stay in the normal
configured environment. Do not read or source historical launch `.sh` files.

## First real-runner smoke: one short Fable rollout

**Root approval required.** This is a surface/lifecycle diagnostic, not a
scientific score. It allows one task, one rollout, one concurrent episode,
eight native MODEL turns, and a 180-second solve interval. An unfinished
contract menu or a turn-limit stop is expected to be possible and must not
be included in cohort science means.

```text
.venv/bin/python .venv/bin/eval physim --env.taskset.difficulty BLOB2v2r2-E1 -m anthropic/claude-fable-5 -n 1 -r 1 -c 1 --shuffle False --env.taskset.tier tools --env.taskset.seed0 0 --env.scientist.harness.id claude_code --env.scientist.harness.version 2.1.223 --env.scientist.runtime.type docker --env.scientist.retries.max-retries 0 --env.retries.max-retries 0 --env.scientist.retries.exclude ResourceSafetyError --env.retries.exclude ResourceSafetyError --rich False --push False --env.scientist.max-turns 8 --env.scientist.timeout.rollout 180
```

Before authorizing a full cohort, inspect actual returned tool data and the
saved trace/config, not only prompt text or advertised tool names:

- Task name `physim-BLOB2v2r2-E1#928`; new-policy `VF_CONFIG` survives the
  actual runner launch. It has declared `r5_mode=true` and
  `r5_resource_policy="v2r2"`.
- First returned `probe_status`: `phase="exploration"`, `T_BASE=2500`,
  syllabus starting `SYLLABUS — BLOB2v2r2-E1`, 12 ports, and no budget or
  `t_end_of_span`. The v1-only `probe_read_streams` surface must not appear.
- Private trace info identifies `resource_policy.id="v2r2"` and all seven
  configured guards. Normal smoke use has zero raw cap hits. No meters or
  policy values appear in tool results.
- If ready is called, every world tool closes; status and submit remain.
  The smoke does not bypass the agent-triggered reveal rule.
- A real resource stop is `ResourceSafetyError`, `ok=false`,
  `resource_truncated=true`, reason/meter/counters preserved, and no science
  reward. A structural numeric zero from an empty reward map is not a score.
- Both whole-agent and whole-episode retry counts are zero in the saved
  config. The new cohort enforces these zeros; normal SDK per-call retries
  are separate. Do not judge the new ceiling from one short smoke alone.

A cheaper Haiku diagnostic can use the same shape with
`-m anthropic/claude-haiku-4.5`, but it would not test Fable-specific runner
behavior. The first full-cohort decision still belongs to the root.

## Fresh full cohorts, only after the smoke review

These are fresh runs, not resume operations. They use the same six world
seeds and unchanged truth data as v2, but have distinct cohort/task labels.
Each command has `n=3`, `r=1`, concurrency 1, `shuffle=false`, and `seed0=0`.
No model-turn, token, or solve-time cap is added to the full cohort config.
Run the two commands sequentially if total host concurrency must remain 1.

### E1 — seeds 928, 929, 930

```text
.venv/bin/python .venv/bin/eval physim --env.taskset.difficulty BLOB2v2r2-E1 -m anthropic/claude-fable-5 -n 3 -r 1 -c 1 --shuffle False --env.taskset.tier tools --env.taskset.seed0 0 --env.scientist.harness.id claude_code --env.scientist.harness.version 2.1.223 --env.scientist.runtime.type docker --env.scientist.retries.max-retries 0 --env.retries.max-retries 0 --env.scientist.retries.exclude ResourceSafetyError --env.retries.exclude ResourceSafetyError --rich False --push False
```

### E2 — seeds 942, 943, 944

```text
.venv/bin/python .venv/bin/eval physim --env.taskset.difficulty BLOB2v2r2-E2 -m anthropic/claude-fable-5 -n 3 -r 1 -c 1 --shuffle False --env.taskset.tier tools --env.taskset.seed0 0 --env.scientist.harness.id claude_code --env.scientist.harness.version 2.1.223 --env.scientist.runtime.type docker --env.scientist.retries.max-retries 0 --env.retries.max-retries 0 --env.scientist.retries.exclude ResourceSafetyError --env.retries.exclude ResourceSafetyError --rich False --push False
```

Default eval output directories have fresh UUIDs. Never combine these with
the old capped `BLOB2v2-E1/E2` results or their resume copies.

`--push False` keeps initial evidence local and avoids making publication
part of the smoke gate. Root owns publication and can choose `--push True`
after reviewing the sample-size issue in the recovery audit. No launcher
or remote endgame action is included in this patch.

**Do not use `--server --resume`.** That installed path skips the custom
`PhysimEnv.complete` rule for terminal resource failures. In-process resume
keeps strict r2 resource-limit evidence without marking it successful;
other failures use the native resume rules.

`--env.taskset.max-turns` is task metadata on the tools tier, not the native
model-turn control. The short diagnostic intentionally uses
`--env.scientist.max-turns`. Do not copy its diagnostic limits into the
full commands or score the diagnostic as a full science attempt.
