# qwen_ring_005: rehearsal job of the round-5 second-pass pin

PILOT_NEVER_REUSE_AS_EXAM. Instance `pilot-qwen-ring-005`; public pilot material, never an exam. Written by the fixer
of port round 5, second pass, after the pack; not part of the packed folder (`MANIFEST.json` does not list this file).

**What it was for.** Not a measurement of the model. The second pass of round 5 (`../../vfport/README.md`, section
8.18) changed the box's run line (`--log-driver none`, K13), how the box's proxy finds the route of every request,
the model's included (K11), and what the agent is told about how a run ends (X20) and what `lab.usage()` counts as
its context (X21). This one job shows, with the real provider, that an ordinary model run passes through the changed
route and box, and what `lab.usage()` now reports. It was run in the cloud container from a fresh sparse clone of
the pin `19b6beb836874f9f938c51367849e2442bd6af4e` (sha256 of `PIN.sha256` `41da66d6...78c8`), every runbook command
as ONE `sh -c` line (`../../vfport/results/rehearsal_round5.json`, `second_pass`).

| | |
|---|---|
| request | `../../vfport/rehearsal/round5_jobs/qwen-ring-005.json` (not under a `requests/` folder), config `../configs/qwen_ring_005.toml` |
| model, caps | `qwen/qwen3.6-35b-a3b`; 40 turns, 15 minutes, 8,192 tokens per reply, context 100,000, `cap_usd` 0.5 |
| bound | one worst-case call $0.0193; bound on the bill $0.5193 (`cap_usd` + one worst-case call) |
| how it ended | the turn limit (`max_turns`, 40 model calls, all streamed with usage, none refused, none with an error) after 367 s of its 900 s; the agent never ended its run by a reply without a tool call |
| the box | Docker's record of the agent's box during the run: log driver `none`, no log path, `docker logs` refused (read back by the environment at the start, and by hand with `docker inspect`) |
| what was graded | the final collection of `submission/` (5 files, 2.7 MB); 64 items, **all 64 failed and were scored with the null policy's forecast**: the grader's first call on the public example 0 raised in the agent's own predictor (`ValueError` from `jax.vmap` on a scalar), so every item got the baseline (`grades.json`, `fallback.by_reason`). The agent never called `lab.validate`, which would have shown the same error; it spent its last turns debugging that code. No infrastructure failure (`n_errors` 0) |
| skill (0 = K, 1 = O) | **0.006**, the null policy's score |
| reference table, same instance (0 = K, 1 = O) | C 0.929, S 0.926, PM 0.920, P0 0.897, D 0.296, null 0.006 (`reference.json`; against C: P0 0.965, D 0.318); the instance's sigma 0.035 and rho 0.896 are outside the program's bars (sigma at least 0.15, rho at most 0.7): this instance does not separate the policies, and no score on it is a result (exam audit X18) |
| `lab.usage()` (X21) | called 4 times from the agent's own scripts: `context_tokens_used` 11,918, 12,669, 13,410, 16,671. Each equals the provider's prompt, cache reads included, plus the reply of the call before it (calls 9, 11, 12 and 15 of the trace); the first pass's count (verifiers' `prompt_tokens` alone) would have shown 1,258, 177, 12,962 and 304 there |
| laboratory | 400 of 400 ticks, 12 episodes, 21 requests, 3 rejected; no `lab.validate`, no `lab.submit` |
| tool calls | 40 `bash`; the longest wait between two replies 41 s |
| counted cost | **$0.0978** (788,804 prompt tokens, 706,653 of them cache reads; 18,080 completion tokens, 0 reasoning; per call the listed prices or the provider's own higher cost field) |
| publication | 20 files, key scan clean (`key_scan.json`, `MANIFEST.json`); the fixer's own scan of this folder and of the rehearsal's record: 3 secrets read from the environment, 21 needles, no hit |

The provider's bill for this job was not read here; the count is the tool's.
