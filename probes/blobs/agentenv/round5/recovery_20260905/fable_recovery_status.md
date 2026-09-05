# Round-5 Fable recovery audit — 2026-09-05

**Two successful rollouts, four billing failures, none missing. Both runs remain incomplete.**
All six actual first `probe_status` results pass the BLOB2v2 surface check.
No eval, model request, environment change, or GPU operation was performed by this audit.

## Cohort and terminal results

| Menu | Valid run | Successful | Failed | Missing |
|---|---|---:|---:|---:|
| BLOB2v2-E2 | `51d11a68-92fe-405f-aeb8-3b345bb69469` | 2 | 1 | 0 |
| BLOB2v2-E1 | `588029cc-23dd-4b89-88e9-2813a3fa73b9` | 0 | 3 | 0 |

Both saved configs specify Fable 5, `claude_code`, 3 tasks × 1 rollout,
`shuffle=false`, and `seed0=0`. The task seed mapping selects E1 seeds 928–930
and E2 seeds 942–944. Current project HEAD is `acc310e3feedcf679fab7a676ba11a0b8ec25081`.
Earlier invalid runs are excluded. No v1 score or Haiku result enters this audit.

| Exact task name | Index | Result | Exact rollout trace ID |
|---|---:|---|---|
| `physim-BLOB2v2-E2#942` | 0 | Successful; skill 0.6281614742 | `344a8d7d8b7b433cb7d73cbf8a402aac` |
| `physim-BLOB2v2-E2#943` | 1 | Successful; skill 0.6241622606 | `529feadde86341e5b3ae008c20a24872` |
| `physim-BLOB2v2-E2#944` | 2 | Failed; ProviderError 402 | `0819dd2bf7404901a752a4fa0b2ccec3` |
| `physim-BLOB2v2-E1#928` | 0 | Failed; ProviderError 402 | `759a50b441ef459489edbabd7760323a` |
| `physim-BLOB2v2-E1#929` | 1 | Failed; ProviderError 402 | `45d261304cfd41e1871fe49434a1ce69` |
| `physim-BLOB2v2-E1#930` | 2 | Failed; ProviderError 402 | `829b7b6807fa4f058c374f7482049012` |

Failures have outer `errors=[]` but nested `ok=false`, `stop_condition="error"`,
and `ProviderError` with status 402, type `billing_error`, code `insufficient_funds`:
“Insufficient balance (including overdraft). Please add funds to continue.”
Their `is_completed=true` means execution ended, not success. Their rewards,
metrics, and info are empty. The log's `reward=0.000` is **not a scored zero**.
Successful tasks have nested `ok=true`, no errors, six skill metrics, and six
confirmed submission flags. Full episode IDs and error bodies are in the JSON.

## Actual tool surface

For every task, the first status is the tool-role message at zero-based node 6:
`json.loads(json.loads(node["message"]["content"])["result"])`.
It has `phase="exploration"`, `T_BASE=2500`, and a nonempty `syllabus` beginning
`SYLLABUS — BLOB2v2-E1` or `SYLLABUS — BLOB2v2-E2`, matching its config.
E1 has 12 ports; E2 has 13. Neither `budget` nor `t_end_of_span` occurs as a key
anywhere in those decoded objects. This is evidence from actual returned data,
not prompt text or tool definitions. Full decoded first results are in the JSON.

## Available metrics — incomplete cohort

| E2 completed seed | Skill | L1 | L2 | L3F | L3S | L4 | L4D |
|---|---:|---:|---:|---:|---:|---:|---:|
| 942 | 0.628161 | 0.565450 | -0.021130 | 0.987284 | 0.965223 | 0.289319 | 0.982822 |
| 943 | 0.624162 | 0.108649 | 0.193231 | 0.926431 | 0.911937 | 0.654798 | 0.949928 |

E2's **successful-only partial mean** is 0.6261618674 (2/3 tasks), not a final
mean. E1 has no scored result. Both final means remain unavailable.

- **942:** ready at 15,795 sim tu / 4,542 environment turns. Final meters:
  sensor 536,360; adjust 611.75; injection 1,015.6; sim tu 15,795;
  forks 400; open peak 5; resets 400; reads base/fork 500/3,142; turns 4,552.
  Cap hits: 13, all `fork_spawns`.
- **943:** ready at 3,930 sim tu / 208 environment turns. Final meters:
  sensor 47,820; adjust 32.3; injection 523.8; sim tu 3,930;
  forks 35; open peak 8; resets 34; reads base/fork 191/182; turns 215.
  Cap hits: 1, `open_forks`.
- **Failures:** no final skill, time-to-ready, meters, or cap-hit total exists.
  Last observed statuses remain in exploration. Explicit MCP fork results show
  `instrument saturated` 42 times for E2#944 and 193/87/147 times for E1#928/#929/#930.
  These observed denials are not a replacement for missing final cap telemetry.

Only `probes/blobs/agentenv/results/smoke_blob2v2_aggregate.json` is used as
baseline context: v2 scripted E1 mean 0.2206 (n=3), E2 mean 0.2022 (n=3).
E2 floor tiers L1/L2/L3F/L3S/L4/L4D are
-0.0099/-0.0175/-0.1588/-0.0099/0.5342/0.8749.
E1 floor tiers L1/L2/L3F/L3E/L4/L4D are
0.0010/0.0014/-0.2893/0.0163/0.7582/0.8359.
No complete-cohort delta or final model ranking is supported.

## Provider and publication errors

Logs contain 50 E2 and 81 E1 model-call 429 errors, followed by 2 E2 and 16 E1
402 attempts. E1 also has 33 auxiliary 404 errors. Per-task transport errors,
last tool errors, request IDs, and exact terminal errors are in the JSON.
Failed episodes already recorded 1,233–2,093 model calls without error each;
these are not the environment `meter_turns` values.

`push=true` remains unchanged. Uploads failed on the 26,214,400-byte sample limit:
E2 sample 47,052,338 bytes; E1 sample 40,917,192 bytes. This blocks publication,
not rollout validity.

## Prepared resume copies — commands NOT executed

Installed native `resume.load` was run through project `.venv/bin/python` on
copies only. It confirmed **E2 kept=2 / owed=1** (#944) and
**E1 kept=0 / owed=3** (#928/#929/#930), including native `Episode.ok` checks.
It pruned only the copies. SHA-256, size, and modification-time checks confirm
all original configs, traces, and logs are unchanged.

After billing is funded and root authorizes execution:

```text
cd /Users/spoho/Documents/prime/test/physim
.venv/bin/eval --resume /Users/spoho/v3work/ops/recovery_20260905/eval_resume/E2
.venv/bin/eval --resume /Users/spoho/v3work/ops/recovery_20260905/eval_resume/E1
```

`--resume` takes no other flags and replays saved config. It restarts failed
rollouts; it does not continue their conversations. It rewrites its target trace
file, so use these copies, not the raw runs. Keep task data and the v2 contract
unchanged or content-key matching can cause previous successes to rerun.
The copy state above is the dated pre-launch snapshot in the validation report.

Files: [full audit JSON](fable_recovery_status.json),
[native resume validation](native_resume_load_validation.json),
[copy-only validation helper](validate_resume_copies.py).
