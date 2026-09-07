# Session migration — start here

Updated 2026-09-07. The substantive R6 first pass was published in **c06b2fb**.
This migration commit preserves the remaining scoring scratch work and records
local inputs. No active task depends on the previous agent's Python variables,
children, heartbeat, or conversation memory.

**Current action: review the R6 package and decide the next design step with the
user. Do not automatically start another rollout, simulation battery, or pod.**
For current status, this guide and the top of HANDOFF.md supersede its dated
historical sections. Old “running” lines and PID files are not live instructions.

## 1. Read order for a fresh agent

1. [Current handoff](HANDOFF.md), **current section only** initially.
2. [R6 overview](probes/blobs/agentenv/round6/README.md).
3. [R6 predictor spec](probes/blobs/l0/deepsearch/TRACKA_R6_PREDICTOR.md) and
   [runner design](probes/blobs/agentenv/round6/runner/DESIGN.md).
4. The two [p4g2_044](probes/blobs/agentenv/round6/physics/p4g2_044/PHYSICS.md) and
   [p6g8_033](probes/blobs/agentenv/round6/physics/p6g8_033/PHYSICS.md) dossiers.
5. [Curated state](handoff/SESSION_STATE.json),
   [local input inventory](handoff/LOCAL_ASSETS.json), and
   [environment snapshot](handoff/ENVIRONMENTS.json) when operating on files.

No pending worker needs resuming. All three R6 workers handed off, were reviewed,
and were retired. The temporary watchdog was deleted. A fresh check during this
migration found **zero direct children and zero agent-owned active heartbeats**.
Paid evaluations and both campaign GPU pods remain stopped/terminated.

## 2. Preserve the user's research direction

The user rejected using generic baselines or sensitivity thresholds as the
meaning of interesting science. **“Physics is not generic.”** Interesting
behavior is often concentrated in special conditions; exploration must learn
where to look. A random probe can miss the blob entirely. A high score on flat
background, or on readable recorded futures, need not establish discovery.

The proposed loop is:

1. Grow worlds.
2. Find interesting worlds; improve selection metrics from what genuinely matters.
3. Use our privileged rules and full 2D views to write evidence-backed empirical
   physics for a world. That is a check on the interestingness metrics, not merely
   a story attached to a score.
4. Test whether an agent with only instruments/interventions discovers predictive
   knowledge of that physics. It need not name the mechanisms as we do or recover
   the simulator's field equations. A useful empirical theory is acceptable.

Fixed contracts are **not presumed optimal**. They disclose where the oracle
thinks to look. The newer direction is executable theory: an agent supplies code,
and a private evaluator queries it on world-specific consequences. The oracle's
coverage map stays in the grader, not in a mentor syllabus. The agent must still
explore, find phenomena and build its own sense of importance. The aspirational
version also has agents propose tests, make predictions and validate their own
theories. That full autonomous-science loop is not implemented. Oracle-guided
assessment is an evaluation aid, not an assumed optimal endpoint. A finite
battery will not certify prediction of every possible outcome.

Meaningful nulls, selectivity and invariants remain valid science. Do not replace
the previous “dead port” mistake with a rule that every graded target must show a
large effect. Do not reinstall the rejected generic baseline gate under a new name.

## 3. What is implemented, and what is still a proposal

### First-pass implementation and accepted evidence

- Submitted-code interface: `predict(actions, queries, n_samples=64, seed=0)`.
  Return `{"samples": [array_per_query, ...]}` with coherent member trajectories.
  Each scenario starts at a fixed opaque t=0, including initial fields/apparatus.
  **No history, public anchor, geometry or field-equation input.** Action/query
  times are absolute; waits are implicit. Histories may inform exploration and
  private phase selection, not become extra predictor inputs.
- `Predictor` in `blobround6.py` is a structural interface, not a supplied agent
  model. The implemented engine is privileged `OracleRunner.sample_truth` with
  a separate, required `truth_seed`. Public predictor sampling seeds must not
  choose the grader's random realization.
- Isolated scheduler: dt=0.02 grid, strict parser, explicit event ordering/source
  intervals, pose changes, no-op/query/prefix consistency and exact private
  checkpoints. The proposed grammar is bounded in expressiveness, not “anything.”
- Worker and independent root checks: **31/31**, comprising 25 toy/API/checkpoint
  and six native tests. Native trajectories were at most **0.12tu**. This does
  not establish long-time parity, performance or safe arbitrary input handling.
- Both physics dossiers are bounded first passes using existing caches. They
  separate observations, hypotheses and NOT YET TESTED experiments. They are
  not completed universal theories. Root reviewed the key 2D figures.

### Concrete physics candidates

- **p4g2_044 / seed928:** spot/stripe interactions and nonmonotone source-off
  outcomes; u2/u3 negative defects with shared signed feedback; localized gated
  x7 halos that home probes can miss. In one cached common-noise dose series,
  lag250 segment counts are control/amp1/amp2/amp3/amp4 = 5/6/5/7/8.
- **p6g8_033 / seed942:** evolving ridges with candidate delayed-channel effects;
  slowly drifting negative cores missed by home probes; a pulse causes large
  local rearrangement with nearly canceled global-mean change. A quiet gated X9
  is a useful control, not a universally dead field.

These are single-realization/quantized-cache observations. They do not prove
chaos, propagation speed, an organism census, a universal threshold, or noise's
necessity for the patterns. See the dossiers for exact masks, parameters and limits.

### Decisions to resolve before further scientific runs

1. **Causal noise pairing.** Implemented policy A uses base forcing until the
   first effective action, then fresh member forcing. A no-op stays on the base
   stream. This follows the draft but does NOT reproduce the common-noise
   treatment/control comparisons used in the dossiers. Choose a consistent trial
   forcing convention or a separately specified private paired-experiment method.
   Do not silently change policy or interpret mismatched-noise differences as
   isolated intervention effects. Noise enters the activators every solver step;
   we have not established that it causes nucleation or prevents freezing here.
2. **Experimental access.** Prototype eval amplitude[0,3] and dilation clipping
   do not match old exploration amp<=1 and bound rejection. Freeze honest
   exploration/query domains, reachable sensor protocols and any extrapolation
   strata. An above-range case is not automatically learnable in range.
3. **Coverage and confirmation.** Choose one or two dossier hypotheses and the
   smallest controlled experiments. Cost them before running. No broad sensitivity
   battery, new truth ensembles, cross-seed study or new world was approved after
   the first pass. Thousands of oracle runs are not assumed cheap.
4. **Scoring/runtime.** No R6 scorer, safe untrusted-bundle runtime, final resource
   caps or production episode is implemented. Marginal CRPS alone misses joint
   temporal/spatial structure. No universal 0–1 or exact agent-achievable floor
   was adopted. A subprocess/import restriction is not a security sandbox.
5. **Integrity and leakage.** Fix/regression-test the old whole-state GET/PUT
   concurrency defect before any rollout. The new oracle unit tests do NOT test
   that transport. Exclude privileged rules, dossiers, caches and truth from the
   agent's context/filesystem/network. These published worlds are development
   cases; contamination/held-out policy must precede benchmark claims.

An adapter of the old agents' narrow predictor code was proposed, **not built or
scored**. Some generator arrays are missing. Any future adapter must be labeled,
not presented as the original submission or a clean new benchmark.

## 4. Earlier completed work: do not reopen it by mistake

| Thread | Final state / entry point |
|---|---|
| R5 stopped BLOB2v2r2 pilot | E1#928 reported0.68066238; E2#942 reported0.65449844. Both diagnostic due state defects. [Paired notes](probes/blobs/agentenv/round5/resource_revision/e2_942_process_audit/POST11_PAIR_NOTES.md). No cohort mean. |
| E1#929 | Provider/server HarnessError, unscored; not science zero or cap stop. |
| E2#943 | Operator-canceled after about11min; acknowledge startup overshoot, no retained science score. |
| E1#930 / E2#944 | Canceled in setup / never admitted. No automatic resume. |
| Process audits | [E1 audit](probes/blobs/agentenv/round5/resource_revision/e1_928_process_audit/REPORT.md) 30 checks; [E2 audit](probes/blobs/agentenv/round5/resource_revision/e2_942_process_audit/REPORT.md) 43 checks. Complete. |
| Post11 | Paired analysis pushed in16275df: [source](docs/blobs/measuring-evolved-worlds.html), [public page](https://swpo.github.io/physim/blobs/measuring-evolved-worlds.html). No R6 rewrite of the page was done. |
| Absolute scoring exploration | Now preserved with [warnings and original hashes](probes/blobs/agentenv/round5/resource_revision/absolute_scoring/README.md). Raw CRPS matches12 logged values at six decimals; normalized columns are NOT adopted. |
| Round4 | [ROUND4_FINAL.md](probes/blobs/agentenv/round4/ROUND4_FINAL.md). Keep separate from capped/invalid/diagnostic/r2 cohorts. |
| v3 evolution and harvest | Gens1–12 complete on both islands, confirmations settled, final archives secured, both campaign pods terminated. [HARVEST2](probes/blobs/l0/deepsearch/v3_pilot/HARVEST2.md), [post12](docs/blobs/breeding-spatial-economies.html). |
| h9 v0 | [Audit](probes/blobs/l0/complexity/h9_review/REVIEW.md) rejects it as phenotype ranker/threshold. Do not restart a >0.2 search or use descriptor bins as biological proof. |

Old documents may mention superseded pods, cohorts or claims. The current status
and audit corrections take precedence. The cheaper-first validation preference is
native checks, then a cheap wiring smoke, one approved frontier pilot, and only
then a predeclared small panel. That ladder does not authorize any run by itself.

The earlier [L1 contract walkthrough](handoff/CONTRACT_DISCUSSION.md) is also
preserved with corrections. Only L1 was covered before the discussion changed
direction; there is no unfinished background task walking through the other contracts.

Core corrections carried forward: prediction MAE is not paired treatment effect;
local quietness is not global inactivity; spread growth is not chaos; Gaussian
leave-one-out CRPS is not an exact/achievable floor; the exploratory SDs use full
base histories, not per-anchor spans; mixed-horizon ratios need aligned reductions.
Billed dollars cannot be inferred from wall time or incomplete usage buckets.

## 5. Local inputs and a new-machine migration

**Git contains the code, reports, figures and small analysis outputs. It does not
contain all raw traces, full-field caches, GPU archives or sensitive operations
material.** [LOCAL_ASSETS.json](handoff/LOCAL_ASSETS.json) records paths, sizes,
presence and hashes/provenance. The migration inventory streamed hashes of eight
selected cache/truth/trace files; it did not extract or rehash the two big archives.

For another session on this machine, those files remain in place. For another
machine, copy only the inputs needed for the intended task:

- Reading this package or running toy/small native runner tests does not need the
  large A0 field caches or GPU archives. The documented native test binds the
  existing genome/seed and takes only a few solver substeps.
- Reproducing physics plots needs the four base/branch files for p4g2_044/s928 and
  p6g8_033/s942 (~2.49GB total). They are ZIP_STORED arrays; the scripts map them
  read-only in place. No extraction is needed.
- Reproducing R5 absolute scores needs both exact trace archives, base caches and
  frozen R5 truth files. E1's whole trace file grew after its first audit; use the
  exact nested completed trace ID, not a historical byte count or number of lines.
- v3 follow-up needs the selected harvest directories or selected members of
  `~/v3work/isl1_final2.tgz` / `isl2_final2.tgz` (~15.2GB combined). Never fully
  unpack them on this disk. Prior verified hashes and current sizes are recorded.
- The old `~/v3work/ops/recovery_20260905/state.json` is local operational history.
  Its current decisions are summarized in [SESSION_STATE.json](handoff/SESSION_STATE.json).
  Do not copy its entire contents into prompts or Git without a security review.

[UNTRACKED_LOCAL_FILES.json](handoff/UNTRACKED_LOCAL_FILES.json) accounts for the
pre-migration leftover files by category. Old logs, actor outputs, render scratch,
PID records and superseded editorial drafts stay local. **Nine old launch .sh
files may contain credentials: do not read, execute, copy or commit them.**
Do not use `git add -A`. Keys stay in `~/.prime/config.json`, not scripts or docs.
If inputs are absent, report the gap; absence is not permission to regenerate
worlds, run model rollouts, rent pods, or install an unrelated environment.

## 6. Native environments and safe checks

Use the target project's environment, not the agent orchestration kernel.
[ENVIRONMENTS.json](handoff/ENVIRONMENTS.json) records the observed interpreters and
package metadata. The project uses `.venv/bin/python`; cached-field plotting used
`~/.venvs/bk3/bin/python`. Those are different environments. Do not assume package
metadata alone identifies imported code: scripts also add local source paths,
and source hashes are in the evidence. In particular, do not automatically
“repair” the observed blobkit metadata version.

From repo root, optional short checks:

```text
.venv/bin/python handoff/check_migration.py
.venv/bin/python environments/physim/tools/test_blob_round6.py --gates toy native
.venv/bin/python probes/blobs/agentenv/round6/validate_first_pass.py
```

The first is static, with no simulator or model imports. The second runs the
bounded native tests, not a battery. The third checks existing handoff consistency
and writes its validation JSON; it does not regenerate physics. Do not run the
archived absolute_scores.py just to read the results: it runs at import and
rewrites its output JSON. Missing R5 truth raises; its build hint is not approval.
Use one native thread for analysis: OMP_NUM_THREADS, OPENBLAS_NUM_THREADS and
MKL_NUM_THREADS =1. On a new machine, inspect the relevant pyproject/lock and
restore the appropriate project environment; do not install packages into the
agent kernel to make project imports work.

## 7. Coordination and approval safety

- No new paid model rollouts, seeds/cohorts, worlds, truth battery or GPU resources
  without explicit user approval. Documentation and existing-file inspection are
  the current task; further scientific work needs a scoped decision.
- Both campaign GPU pods are terminated; do not SSH to/recreate them. Unrelated
  resources are out of scope. Stale PID files do not authorize killing anything.
- Keep durable work under the repo or `~/v3work`, not `/tmp`. Do not read old
  launchers. If remote process control is ever authorized again, use inspected
  script files and exact process identity, not self-matching shell kill patterns.
- Background command completion did **not** wake a child agent in this runtime.
  A parent's explicit `agent_message.send` did. A registry label “completed” was
  not proof of a completed task. Require explicit DONE/BLOCKED/WAITING handoffs,
  with artifact paths and the next action; inspect actual liveness and ready files.
- For future delegated work, read the installed skill APIs. Use a bounded,
  task-specific heartbeat only when needed/authorized; avoid sleep/poll loops or
  redundant messages to active workers. Retire it after handoff/review or its
  deadline. There is **no heartbeat to revive now**.
- In this build, deleting a child accepted a child-ID string or RLMSubagent, not
  the admission RLMSpawnHandle. All old child sessions have already been removed.

### Paste into the new session

> Read SESSION_MIGRATION.md, then the current HANDOFF.md and R6 overview. The R6
> first pass is reviewed/published; no jobs, workers, heartbeats or pods need
> resuming. Keep the approval limits. Start by discussing causal noise pairing
> and the smallest world-specific confirmation experiments, not launching a new
> benchmark or restoring generic contracts/baseline gates.
