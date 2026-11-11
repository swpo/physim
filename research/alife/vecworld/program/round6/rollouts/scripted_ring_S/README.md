# scripted_ring_S: a scripted-agent trace, kept as a test input for the report tool

PILOT_NEVER_REUSE_AS_EXAM: instance `pilot-qwen-ring-001-r2-w0` is public pilot material and is never to be used
as an exam. Every file of this folder is of that instance.

No model and no new rollout: this is the rollout of the scripted reference agent S (agentenv's
`reference_agent.py --policy S`, run in the agent's box by the port's `physim2-script` harness) that the runner
of `qwen_ring_001` made with `../vfport/tools/prove.py` when it built the reference table of the pilot instance
(11 Nov 2026, run `proof-s`, trace `d889a4f4df2445a19c1f5dfb90c2951b`). Its score is the S row of
`../qwen_ring_001/reference/proof_pilot.json`. The trace was copied from the runner's scratch folder; the port's
own `results/` keep no raw trace, and no new instance was opened for this.

| file | what it is |
|---|---|
| `trace.redacted.jsonl` | vf-eval's saved trace of that rollout, passed through `extract.py`'s removal of credential-like fields (none were present). A scripted trace has no messages and no tool calls. |
| `lab_record.json` | the laboratory's own log of the rollout from the store (29 requests: operation, ticks, nats; no observation, no input, no hidden value) |
| `rollout_report.md`, `rollout_report.json` | what `../tools/rollout_report.py` makes of the two files above and the reference table (command in `../tools/README_rollout_report.md`) |

Counted before the commit: 0 occurrences of the instance's secret or of its hidden parameters in these files,
0 credentials, 0 account identifiers.
