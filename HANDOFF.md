# ACTIVE STATE — 2026-09-05 23:00 UTC (read first)

## GPU continuation: COMPLETE, secured, and terminated
- Both islands finished through gen12 and verified final confirmations.
  Final result rows: isl1 1850, isl2 1756. No pending confirms remain.
- BOTH campaign pods terminated; API listing confirms neither remains.
  Do NOT SSH to or recreate e54975df9f1745e7b3573a625f43d0f8 or
  9e6f440582e94895a549ba44b3ef3288. Other projects' pods are out of scope.
- Immutable final archives, locally verified against remote SHA256, tar
  integrity, settledgen12 marker, and independently copied critical files:
  ~/v3work/isl1_final2.tgz — 7526611213 bytes,1951 members,
  SHA256 7ef7e373677750b16cef373623e1b6bbecd400cea312ba359a940fd5fe3f40c3
  ~/v3work/isl2_final2.tgz — 7667929517 bytes,1970 members,
  SHA256 cb00bc78b38c7edf28cbb0a6128b721eec5a345810b26460f390992f72a68a81
  Verification sidecars are <archive>.verified.json; release receipts and
  exact metadata in ~/v3work/ops/recovery_20260905/state.json.
- Both completed three GPU re-simulation films before backup. Native smoke
  validated3 finite changing frames and fresh-device equality. Record these
  as RE-SIMULATIONS, not exact original traces or reconfirmed scores.
  Helper/pin exception: shipped0.3.5 has two stale lock-table entries;
  all48 deployed source hashes matched explicit reviewed wheel pins. No
  physics/lock table was edited. Helper lives at v3_pilot/film_recovery/.

## Eval resource fix: IMPLEMENTED; fresh cohort RUNNING
- User chose to fix experimentally binding400-fork/8-open limits rather
  than retry the old capped cohort. Fix pushed0a0fc5e; pilot evidence e455715.
- BLOB2v2r2-E1/E2: high PRIVATE7guards,8-resident replayableLRU,128bitforkIDs,
  terminalResourceSafetyError(no science score, no whole-run retries).
  Old tags/limits intact; truth/scoring/physics unchanged. Full native/real
  physics/legacy tests + parent fast gate passed.
- Actual8turn/180s Fable diagnostic verified new syllabus/privatepolicy/zero
  hits, then timed out as designed; DO NOT count it as science.
- Fresh full cohorts launched21:32:25Z, n3/r1/c1 per world, same six seeds:
  ~/v3work/ops/recovery_20260905/eval_fable_r2/E1 (pid27324)
  ~/v3work/ops/recovery_20260905/eval_fable_r2/E2 (pid27323)
  Logs/exitfiles/specs in state.json fresh_resource_cohorts. Saved native
  max_turns=None and timeout={}; diagnosticlimits NOT carried over.
- Original corrected-but-capped runs51d11a68(E2),588029cc(E1) preserved:
  two E2 successes + four402billing failures; capped scores are a separate
  cohort. Their copied retry processes were intentionally stopped; NEVER
  resume them. Earlierbabe2a40/791527b3 runs INVALID(v1surface/v2scorer).
- Parse NESTED ok/errors/readied/submissions/privatepolicy/meters; JSONL
  count or outer errors=[] is not success. Resource errors terminal and
  unscored;402 not a scientific zero. Hub>26MB failures publication-only.

## Local analysis underway (no more GPU work)
- Source of truth: ~/v3work/ops/recovery_20260905/state.json.
- Disk ~16GBfree after final backups. NO full extraction. Bounded metadata
  and films extracted to ~/v3work/harvest2/v3cont-N/islN/out (about200MB per
  island), with EXTRACTION_COMPLETE.json. Raw run NPZs remain compressed.
  Originalgen7snapshots/harvest remain. Deleted only redundant /tmp elite
  upload tars and the optional partial extraction created during recovery.
- Children harvest2-auditor and h9-metric-audit: LOCAL read-only analysis/
  toy tests, no ops/model launches/production edits. Wait explicit reports.
- Important early audit findings (report pending): all2324 baseline rows
  preserved exactly; one c9fill identity has2differentgenomes;11 older seed3
  jobs used same-named donor-v2genomes rather than the v3screen genotype.
  Quarantine invalid genotype-confirmation joins; preserve every raw row.
  Spatial-IC screen + soup confirmation are different IC protocols even
  when ghash matches. Do not call the latter replication of the spatial IC.
- Old .82 'operator hit rate' pooled confirmations over screen lanes. Use
  screen-only rates/denominators, separate selected confirmations, common
  W9 for cross-phase tables, and distinguish full/partial C9.
- h9 is exploratory, not calibrated. Five low examples do not prove no
  evolved world segregates; positional relabel is not an upper bound.
  Review also found h9 stops before d7b persistence pruning. No h9 was
  deployed into evolution. Do not repeat earlier overclaims.
- Next: audited HARVEST2 + corrected post12 with six time-lapse films;
  evaluate h9 review before a full streaming rescore; tag fresh agent
  results separately and update post11 to current implemented policy.
- Heartbeat f80768c7-a2cb-4766-ba37-19c6ce9680cc remains for local eval/analysis
  (15m). Delete only after completion or an explicit successor watch.

---
## Historical handoff (older claims may be superseded above)

# CONTEXT HANDOFF (2026-09-02) — full program state for a fresh prime-agent context
(Repo = single source of truth. Everything below is committed or referenced by path.)

## WHERE EVERYTHING STANDS
1. V2 EVOLUTION CAMPAIGN: COMPLETE. Final union 423 cells (230 minted), champion 91.16
   (3|grow|rotor|liquid). Analysis in probes/blobs/l0/deepsearch/v2_analysis/ (LINEAGE,
   OPERATOR_STATS, COMPLEXITY_TRAJECTORY, CAP_RIDERS + film_candidates). Posts 10
   (evolving-at-scale) + slow-mo clips live. Total spend ~$515.
2. BLOBKIT: 0.3.4 (devrec+async engine, 2.18x claim, battery timeout guard). Perf suite
   probes/blobs/blobkit/perf/ (bench tiers, frozen workloads, HYPOTHESES/GAINS).
   Roadmap 0.4: driver-native devrec, CREC phase 2, research_overlay for make_bundle
   (IDEAS.md), in-runner gen limits. RETROSPECTIVE.md + check taxonomy in MANIFEST.
3. V3 EVOLUTION (Track B): metrics_v3/assay_v3/operators_v3 VALIDATED (gate table in
   probes/blobs/l0/complexity/VALIDATION_V3.md; C9 = t9/s9/e9/r9 spatial economy;
   merge_spatial_ic). PILOT RUNNING NOW: 2 pods (v3pilot-1/2, /tmp/v3pilot_fleet.json
   — COPY BELOW since /tmp dies), islands 1-2 x 12 gens from v2 top-100 + atlas
   immigrants. Concurrency fix for ic-lanes deployed mid-run (takes effect next gen).
   Success = >=5 economy cells C9>=0.4 & interest>=60. Budget cap $150 (~$3/h burn).
   PILOT PODS: v3pilot-1 = pod f6a99cd30aae4c... ip 150.136.214.95 island 1;
               v3pilot-2 = pod 2d1c7688beee4c... ip 130.210.31.82 island 2.
   Bundle+workspace: ~/v3work/v3bundle (durable); venv ~/.venvs/bk3.
4. AGENT ENV (Track A): environments/physim BLOB tiers. History: round1 (BLOB-E1, leaky
   iface) fable 0.689/sol 0.08 vs scripted 0.60; round3 (BLOB-E1r3, tight iface) fable
   0.632/sol 0.05 — leak value ~0.06; ZERO actuator use except one u1-identification
   test (fable r3-2). ROUND 2 CONTRACT SYSTEM (clean-slate design,
   TRACKA_CLEANSLATE_EVAL.md): L1 pose-targeted, L2 hidden-sensor nowcast, L3F/L3S/L3E,
   L4+dose-leg, skill-normalized scoring, world-adaptive menus (BLOB2-E1/E2, commit
   bcac15d). ROUND 4 EVALS RUNNING: sol DONE (negative skill everywhere: -0.42..-0.67
   E1, -0.22..-0.67 E2); fable partial (E1: 0.29 + errors; E2: 0.16 + errors);
   RESUMES IN FLIGHT for fable E1+E2 (transient pinference 5xx HarnessErrors;
   logs probes/blobs/agentenv/round4/). Scripted baselines: E1 +0.238, E2 +0.233
   (results/smoke_blob2_*.json). L2 is open headroom (scripted actor ties baseline).
5. DESIGN DOCS (all in probes/blobs/l0/deepsearch/): V3_TRACKB_SPEC.md,
   TRACKA_AGENTENV_SPEC.md (probe-device design), TRACKA_R2_CONTROLS.md (control-
   surface evolution R1->R3-final: fixed global undocumented convention),
   TRACKA_CLEANSLATE_EVAL.md (capability ladder + overlap audit).

## KEY USER POLICIES (standing)
- Parallelize-max at flat cost; budget ceilings advisory-then-discuss ($600-era done;
  pilot cap $150); measure-don't-guess (benchmark rows before claims); science changes
  only for order-of-magnitude wins; simple != documented (barrier by undocumentation,
  fixed global conventions); no /tmp for anything durable; harness = verifiers coding
  harnesses (claude_code/codex); eval models = frontier-first (fable-5 + gpt-5.6-sol).
- RED protocol for underperforming engines: stop production, instrument, extract
  minutes-scale repro, iterate offline, gated relaunch.

## IN-FLIGHT / NEXT ACTIONS
- [ ] fable round-4 resumes complete -> full BLOB2 table -> narrate + post 11 results
      section update.
- [ ] v3 pilot: monitor gens (concurrency fix pace), unions at 7/final, harvest,
      verdict vs success criteria, terminate pods (cap $150).
- [ ] post 11 results + round-2 findings writeup.
- [ ] Later: L5 preparation + L6 executable-theory tiers (round 3-4 of clean-slate);
      E2 eval read; v4 gluing after agent-eval phase settles; blobkit 0.4.
- Local processes RIGHT NOW: 2 eval resumes (pids in round4/*.pid), 1 local smoke
  (~/v3work/smoke.pid — verifying ic-concurrency patch; informational only, pods
  already patched).

## OPERATIONAL GOTCHAS (hard-won this context)
- ssh+nohup: launch via SCRIPT FILES only; never pkill patterns matching your own ssh
  cmdline; never trust remote watchers — poll from controller.
- macOS: no `timeout` cmd; /tmp GC kills venvs/workspaces; BLAS threads MUST be pinned
  (OMP_NUM_THREADS=1 etc) or 800%-CPU thrash.
- Children die in setup/reading phases: revive write-first with extracted facts
  embedded; after 3-4 deaths do it inline.
- eval runner: .venv/bin/eval physim -n 3 -m <model> --env.taskset.difficulty <tag>
  --env.scientist.harness.id <claude_code|codex> --env.scientist.runtime.type docker;
  --resume <output-dir> reruns errored rollouts only.
- pinference transient 5xx = HarnessError mid-rollout; resume fixes; not our env.


## UPDATE 2026-09-04 (post prime-agent-update context)
1. V3 PILOT: COMPLETE + TERMINATED. RED-protocol mid-flight: launch was 10-20x too
   slow (ic lanes serial on CPU pre-GPU-batch; C9 rescore serial on main thread).
   Fix = blobkit 0.3.5 (job dicts carry per-lane "ic" -> init_soup_gpu_batch ics
   hook) + pilot-2 worker (ic lanes ride GPU tensor, version-gated; C9 rescore in
   spawn ProcessPool; commits 9a07779). Gated tests green (ic-injection differ test,
   6-job end-to-end, rescore exact-match). Both islands ran gens 1-7 (~3.5-4.5h/gen),
   confirms settled through gen 7 (two-stage async drain: s3g6+s2g7 -> ingest3 6 +
   ingest2 7 -> s3g7 -> ingest3 7; CONFIRM7_SETTLED in driver.log both islands).
   SNAPSHOTS: ~/v3work/isl1_final.tgz (7.7GB, 1103 entries), isl2_final.tgz (6.7GB,
   1053) — full out/ (results, archive, jobs, elite npzs), configs, campaign.log.
   Pods TERMINATED ~03:00/05:45Z Sep 4. Total spend ≈ $110-115 of $150 cap.
   SUCCESS CRITERION MET AT GEN 3: >=5 economy cells target vs 45 (isl1) + 34 (isl2)
   distinct cells with C9>=0.4 & I>=60 (from results.json rows; archive entries lack
   C9 — ingest field subset — join results.json at harvest). Continuation to gens
   8-12 possible from snapshots: restore ~/islN, pod_run_batch.sh 8 12.
2. ROUND 4: FINAL + PUBLISHED. fable E1 +0.308 / E2 +0.287 (n=3) vs scripted
   +0.238/+0.233; sol negative everywhere. probes/blobs/agentenv/round4/ROUND4_FINAL.md.
   POST 11 rewritten current-first (BLOB2 ladder w/ shipped semantics from
   blobround2.py) + pushed (a1d1123). Local eval resumes done; launch detached
   (start_new_session) or agent restarts kill them — pids die with prime-agent.
3. ROUND 5 DIRECTION (user-agreed, spec doc pending): (a) budgets -> huge
   unadvertised safety caps (utilization data: injection hit 0.95, replicas 12/12 —
   limits DID bind in round 4); (b) spend metered silently -> post-hoc Pareto
   (skill vs spend); strip budget from probe_status/tool returns/coaching errors;
   (c) span/lock-at-inject removed -> anchor-parameterized contracts (anchor =
   (world line, t)): free exploration forks + reset; scored contract instances
   harness-issued (fixed per world+seed) for comparability; truth = fresh replicas
   per (anchor, protocol); baselines per anchor. Scripted actor re-played, floors
   re-derived; round-4 numbers stay as BLOB2-v1 row. Agent-authored contracts =
   later L6 lane.
4. NEXT: harvest (untar snapshots -> merge islands, join C9 from results.json,
   economy-cell census, C9 trajectory by gen, operator stats esp. merge_spatial_ic,
   film candidates) -> pilot verdict doc -> v3 full-campaign go/no-go + round-5 spec.

5. POST-11 REPUBLISH AFTER v2.1 IMPLEMENTATION (user request 2026-09-04): once the
   round-5/v2.1 contract system (TRACKA_R5_ANCHORS.md: category-anchored contracts,
   closed-book agent-triggered reveal, silent caps) is IMPLEMENTED and floors are
   re-derived, update docs/blobs/measuring-evolved-worlds.html (live at
   swpo.github.io/physim/blobs/measuring-evolved-worlds.html) to describe v2.1 as
   the current instrument (v1 + round-4 numbers stay as the tagged historical row).
