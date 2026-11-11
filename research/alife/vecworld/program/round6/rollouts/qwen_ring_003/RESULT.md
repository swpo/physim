# qwen_ring_003: rehearsal job of the round-4 second-pass pin

PILOT_NEVER_REUSE_AS_EXAM. Instance `pilot-qwen-ring-003`; public pilot material, never an exam.

**What it was for.** Not a measurement of the model. The second pass of round 4 (`../../vfport/README.md`, section
8.16) put byte bounds between a box and the processes on the host and made the spend stop's request keys an
allow-list. This one short job shows, with the real provider, that an ordinary model run passes through them as
before: every request the stock harness sent was admitted, nothing was refused, the run ended by its own limit and
was graded and packed. It was run in the cloud container from a fresh clone of the pin
`841b4a1e1d12afc7cd60b8b184b451d278895b1d` (sha256 of `PIN.sha256` `898089fc...108f`), every runbook command as
ONE `sh -c` line (`../../vfport/results/rehearsal_round4.json`, key `second_pass`).

| | |
|---|---|
| request | `../../vfport/rehearsal/round4_jobs/qwen-ring-003.json` (not under a `requests/` folder), config `../configs/qwen_ring_003.toml` |
| model, caps | `qwen/qwen3.6-35b-a3b`; 30 turns, 15 minutes, 8,192 tokens per reply, context 100,000, `cap_usd` 0.5 |
| bound | one worst-case call $0.0193; bound on the bill $0.5193 (`cap_usd` + one worst-case call) |
| how it ended | the wall time (`agent_timeout`) after 24 turns (24 model calls, all streamed with usage, none refused, none with an error) |
| what was graded | the final collection of `submission/` (2 files, 73,795 bytes), whose score equals the null policy's to the last digit: the baseline the box started with; 64 items in one box each, no failed item, no fallback |
| skill (0 = K, 1 = O) | **-0.029**, the null policy's own score on this instance (reference table: C 0.927, S 0.922, PM 0.917, P0 0.896, D 0.161, null -0.029) |
| laboratory | 306 ticks, 9 episodes, 14 requests, none rejected |
| counted cost | **$0.0318** (254,533 prompt tokens, 207,034 of them cache reads; 5,792 completion tokens; per call the listed prices or the provider's own higher cost field) |
| publication | 17 files, key scan clean (`key_scan.json`, `MANIFEST.json`) |

The provider's bill for this job was not read here; the count is the tool's.
