# qwen_ring_004: rehearsal job of the round-5 pin

PILOT_NEVER_REUSE_AS_EXAM. Instance `pilot-qwen-ring-004`; public pilot material, never an exam. Written by the fixer
of port round 5 after the pack; not part of the packed folder (`MANIFEST.json` does not list this file).

**What it was for.** Not a measurement of the model. Round 5 (`../../vfport/README.md`, section 8.17) bounded what a
box can make the host hold through verifiers' interception server (K9) and told the agent that one `bash` command
holds it until it returns, up to the harness's 3,600 s (X13), with the rest of the disclosure sweep. This one job
shows, with the real provider, that an ordinary model run passes through the new bounds and how the agent met the
new text. It was run in the cloud container from a fresh sparse clone of the pin
`c48eb6dc28b31f798a8c75f3b9612c8895570278` (sha256 of `PIN.sha256` `025a9da6...4eed`), every runbook command as
ONE `sh -c` line (`../../vfport/results/rehearsal_round5.json`).

| | |
|---|---|
| request | `../../vfport/rehearsal/round5_jobs/qwen-ring-004.json` (not under a `requests/` folder), config `../configs/qwen_ring_004.toml` |
| model, caps | `qwen/qwen3.6-35b-a3b`; 60 turns, 18 minutes, 8,192 tokens per reply, context 100,000, `cap_usd` 1.0 |
| bound | one worst-case call $0.0193; bound on the bill $1.0193 (`cap_usd` + one worst-case call) |
| how it ended | the turn limit (`max_turns`, 60 model calls, all streamed with usage, none refused, none with an error) after 790 s of its 1,080 s |
| what was graded | the final collection of `submission/` (4 files, 12.4 MB); 64 items in one box each, **no failed item, no fallback, no infrastructure failure** |
| skill (0 = K, 1 = O) | **0.316** |
| reference table, same instance (0 = K, 1 = O) | C 0.881, S 0.874, PM 0.788, P0 0.785, D 0.264, null -0.004; the instance's sigma 0.109 and rho 0.924 are outside the program's own bars (sigma at least 0.15, rho at most 0.7): the score is above D and far below P0, and it says nothing about how hard the ring is (exam audit X18) |
| laboratory | 400 of 400 ticks, 12 episodes, 22 requests, 1 rejected; 3 `lab.validate` calls, all as graded |
| tool calls | 57 `bash`, 3 `lab_call`; the longest wait for a command 219 s, then 188 s (every training command ran under the agent's own `timeout` of 120 to 600 s); no background job |
| counted cost | **$0.2026** (1,696,119 prompt tokens, 1,666,429 of them cache reads; 33,274 completion tokens; per call the listed prices or the provider's own higher cost field) |
| publication | 19 files, key scan clean (`key_scan.json`, `MANIFEST.json`) |

The provider's bill for this job was not read here; the count is the tool's.
