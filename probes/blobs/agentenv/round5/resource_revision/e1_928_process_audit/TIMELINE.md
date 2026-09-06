# Annotated timeline — E1 #928

Trace `0bdd699154ee4e1d96aac4e0961bc11d` only. Node and model-call indices are zero-based. Each action below is linked to a distinct tool ID from a sampled model response. Context copies do not add actions.

**Timestamp caution:** UTC times below are sampled node timestamps. A tool-result node can be recorded when the next model response completes; it is not a reliable server completion time. Ready is tightly bounded by the ready model response ending at00:58:27.142Z and the next, reveal-bearing request starting at00:58:27.172Z.

## Exploration → prepared artifacts → reveal

| UTC | Node → result | Tool-call ID | Annotation |
|---|---:|---|---|
| 2026-09-05 21:32:52.355Z | 3→6 | `toolu_01YJXJiXkZXjfiKy8f3x5LS4` | **Start.** Reads status and the syllabus before experiments. |
| 2026-09-05 21:33:38.945Z | 7→9 | `toolu_01KzPUAcEYyWQ89XwrasHQB7` | **Setup failure.** Workspace/Python check returns `ModuleNotFoundError: No module named 'numpy'`. |
| 2026-09-05 21:35:31.185Z | 20→23 | `toolu_01RwfNZMebZu5TE2gYrgGGsr` | **Capture.** Reads base t=10..130; large output is persisted, not a failed read. |
| 2026-09-05 21:39:56.763Z | 80→105 | `toolu_01NZnq7CPfNt1pNmJ6kxRZce` | **Apparatus range tests.** Multi-step actuator trials include ordinary apparatus refusals. These are not resource stops. |
| 2026-09-05 21:40:06.643Z | 93→95 | `toolu_01AfN4V2FuJWcZW8KjVgHhr4` | **State anomaly.** Five distinct one-step base reads in this response yield t=160,165,165,165,165. See CONCURRENCY.md. |
| 2026-09-05 21:44:35.258Z | 152→161 | `toolu_014KgdhqCrqxKGbF42JEgZdz` | **Parallel experiments.** Delegates L1 trials and fork divergence while base capture and other world work continue. |
| 2026-09-05 21:50:42.208Z | 341→361 | `toolu_01Ky9wm8jV5giqhb4vz1MihC` | **Emission scan.** Delegates ports 0–5 and 6–11 at anchor 1600, amp=1, dur=10; port 2 later stands out. |
| 2026-09-05 22:00:15.074Z | 670→677 | `toolu_019HrrsqkepWErgE3qaYePh4` | **State anomaly.** Same response requests anchors 200 and 600 with distinct IDs; both matched replies name the same fork ID. |
| 2026-09-05 22:25:01.039Z | 1282→1283 | `toolu_018EztD3wcq4ksv2cTBJXeum` | **Base capture complete.** Final base chunk reaches t=2500; later status confirms the head. Most large-output full files are absent from this archive. |
| 2026-09-05 22:26:59.865Z | 1326→1347 | `toolu_017tt4dbLMo8fCNyKhrBPmW3` | **Coverage extension.** Delegates post-base continuation and a long global-statistics sweep before knowing hidden anchors. |
| 2026-09-05 22:43:23.742Z | 1886→1951 | `toolu_012zf2bshEozD16t2cEqsyUH` | **Sustained failures.** Five read calls in this batch time out; later read/status/inject/reset calls also time out. |
| 2026-09-05 22:43:32.974Z | 1892→1905 | `toolu_01EZL11gDR2nUHJoKzPuyumZ` | **State anomaly.** Four distinct fork calls for anchors730/1210/1875/2450 return one ID, with four different anchor fields. |
| 2026-09-05 23:05:27.477Z | 2063→2064 | `toolu_01GKjj9Mafvz4CFomtbnoJor` | **Change of strategy.** Stops four background agents. Quote: “Stopping all background agents to relieve pressure, then retesting.” This is an action in the recorded run, not this audit. |
| 2026-09-05 23:22:14.969Z | 2084→2085 | `toolu_013DTE1Wn5GfRTJjYtKcJhXY` | **Recovery attempt.** Status returns again (12 contexts); continuation/global collection resumes. Some later timeouts remain. |
| 2026-09-05 23:52:32.659Z | 2347→2351 | `toolu_01T3b94JJAuTpyPVasHJRuS1` | **Data rejection.** After a conflicting port-2@900 recheck, script removes eight rows from L4_A900.jsonl; output says `remaining lines: 0`. |
| 2026-09-05 23:52:47.127Z | 2352→2365 | `toolu_011kEfaXgvygQSrSwNrbdQcT` | **More controlled collection.** Launches anchor-2100 response templates. Later major port-2 and L1 batches are run one delegated batch at a time. |
| 2026-09-06 00:17:27.273Z | 2521→2527 | `toolu_012sz8Xh5MZgh3WwuABchYVs` | **Dose calibration.** Runs port-2 amplitude/duration series. Quote: “running serially on one agent, then L1 batch 3, then QC”. |
| 2026-09-06 00:47:07.810Z | 2820→2823 | `toolu_01Ux2NdFLRzeo1tAT9NzFcEZ` | **Offline fit.** Fits actuator contraction from 81 reported command-step observations; every fourth is held out (60 fit, 21 calibration). |
| 2026-09-06 00:47:21.328Z | 2824→2834 | `toolu_018GMRNUsedmRdREXxefwZSE` | **Quality checks.** Delegates eight lag-zero fork-vs-record checks. All eight report zero differences; these checks do not prove all trial data are sound. |
| 2026-09-06 00:57:50.671Z | 2955→2956 | `toolu_015ErnWe9Mta1iSq4zTQ4iKs` | **Last world action.** Resets final continuation-check fork. The same response writes the submission playbook. |
| 2026-09-06 00:58:27.141Z | 2970→2971 | `toolu_01UJUVLKFPZJwjCTUQWafJko` | **Ready.** Quote: “Everything is in place. Opening the envelope.” Persisted ready counters: 11,495 sim tu /884 turns. |
| 2026-09-06 00:59:31.902Z | 2972→2974 | `toolu_017uK4JgPMqyKmAsFk6SS5SR` | **Closed-book adaptation.** Two offline edits: sequential u3 clipping for L1; larger L3E uncertainty. No new world experiment tests these changes. |
| 2026-09-06 00:59:40.292Z | 2976→2977 | `toolu_01G4vFFgH79Dk5KzAtzuymJ1` | **Payload construction.** Writes revealed parameters and runs saved `build_payloads.py`; all six shapes print successfully. |

## Six accepted submissions

Each accepted payload exactly equals the corresponding archived `app/probe/payload_*.json` object. There are no rejected submits and no resubmissions.

| Instance | UTC call-node time | Node → result | Tool-call ID | Accepted shape |
|---|---|---:|---|---|
| L3E@i1 | 2026-09-06 01:00:15.186Z | 2989→2990 | `toolu_01Xokr2M25eGPdGxCWWWB79N` | `[16]` |
| L1@i1 | 2026-09-06 01:00:45.387Z | 2993→2994 | `toolu_012BTyTdFxh9kf37bhPSsocZ` | `[12, 13]` |
| L2@i1 | 2026-09-06 01:01:09.699Z | 2997→2998 | `toolu_0192k357iYNLZN3Vh1M255ha` | `[12, 13]` |
| L3F@i1 | 2026-09-06 01:02:55.263Z | 3001→3002 | `toolu_01WTLCNGj2cQ5Kok9Y7J5ByY` | `[4, 12, 19]` |
| L4@i1 | 2026-09-06 01:05:28.229Z | 3005→3006 | `toolu_01DNpxZqnFWT7fGsfyRhHkTS` | `[6, 12, 19]` |
| L4D@i1 | 2026-09-06 01:06:47.811Z | 3012→3013 | `toolu_01BZBJcKHM1jMWwEKDZN3ein` | `[3, 12, 19]` |

Final status: node3014→3015, `toolu_01VTthavKkTPer266Fj5KkVf`, **2026-09-06T01:06:52.441Z**. All six submission flags are true and `contexts=[]`.

Scoring completes at **2026-09-06T01:07:17.178Z**. The trace marks completion by the agent, not truncation. All seven resource cap counters are zero.

## Closed-book boundary audit

- Last world-tool request: node2955 at00:57:50.671Z, reset. Ready: node2970 at00:58:27.141Z.
- After ready: 2 Edit, 10 Bash, 6 submit, 1 status calls. No read, wait, adjust, fork, inject, or reset calls.
- The ten Bash commands only write revealed.json, run saved predictors/builders, inspect payloads, or print file sizes. The embedded submitted code loads local arrays/models and computes offline forecasts. No world/network client appears in that post-ready path.
- Post-ready model work: 19 completed calls; reported prompt92,542, cache-read7,065,361, output48,103, reasoning4,773 (part of output). One additional429 request has no usage.
- Environment turns884→891 equal six submits plus one status. Final sim meter equals ready sim meter,11,495tu.

## Token schema evidence

Completed model call0 points to sampled node3; its usage is `prompt_tokens=8498`, `completion_tokens=44`, `cached_input_tokens=29906`, `reasoning_tokens=12`. The installed `verifiers/v1/types.py:107–167` defines input as prompt+cache-read and total as input+completion. It does not add reasoning again.

`verifiers/v1/dialects/anthropic.py:150–157` maps prompt to provider input+cache-creation, output to completion, and cache-read separately. The archived fields cannot recover cache-write tokens independently. This rule is applied to all1,216 completed calls in `audit_counts.py`.

For scientific code citations, failed hypotheses, and data gaps, see SCIENTIFIC_PROCESS.md. For exact same-response fork anomalies and native state semantics, see CONCURRENCY.md.
