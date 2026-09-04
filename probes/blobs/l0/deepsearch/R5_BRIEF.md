# ROUND-5 SPEC BRIEF (user-agreed decisions, 2026-09-04)
Write: probes/blobs/l0/deepsearch/TRACKA_R5_ANCHORS.md — the round-5 respec of the
BLOB2 contract system ("BLOB2-v2"). Round-4 numbers stay as the v1 row.

## Decisions (agreed with user — do not relitigate, elaborate into a spec)
(a) BUDGETS -> SAFETY CAPS ONLY. Current BUDGETS (blobcore.py: sensor=40000
    node-tu, adjust=1200, injection=120 amp-tu w/ steep pricing) DID bind in
    round 4: injection frac hit 0.74/0.95/0.70 (E1) 0.58/0.45/0.81 (E2);
    replicas 12/12 in 4/6 rollouts. Replace with ~20-50x caps whose only job is
    runaway protection (like token caps); monitor hit rate (target: exactly 0).
    KEEP task-defining constraints: per-injection AMP_CAP=1.0 (calibrated regime),
    L4D announced dose grid + secret amp, announced-protocol semantics.
(b) TRACK, DON'T TELL. Strip budget/remaining from probe_status, tool returns,
    and refusal/coaching errors ("budget too low... use probe_wait" DELETED).
    Meter everything silently (spend_sensor/adjust/injection, replicas, forks,
    sim-ticks) -> logged per rollout -> post-hoc Pareto frontier (skill vs spend).
    No agent-visible mention of cost anywhere in the surface. No partial credit
    for thrift; efficiency is analysis, not conditioning.
(c) ANCHORS REPLACE THE SPAN + LOCK-AT-INJECT. Kill the uniform T0=1700 preamble
    and LOCK_AT_INJECT. New primitives:
    - anchor = (world line, t): base line at any t, or a saved fork state (hash-id).
    - EXPLORATION forks: agent forks from any anchor, injects/reads/adjusts
      freely, discards/resets at will. Never scored, cannot contaminate truth.
    - SCORED contract instances: harness-issued, fixed per (world, seed) for
      cross-agent comparability. Each instance = (anchor, protocol, observable,
      horizon); protocol = undisturbed | announced dose sequence. Truth = fresh
      replica ensemble spawned from exactly that spec (cache per (world, seed,
      anchor, protocol)). CRPS + baseline ladder (climatology/persistence/AR2
      where applicable) recomputed per anchor.
    - Reset = discard fork, free.
    - Agent-authored contracts: explicitly OUT of scope (later L6 executable-
      theory lane; note the difficulty-normalization open problem).
## Spec must include
1. Motivation (2 short paras: round-4 utilization data above; conditioning
   argument — "best science" vs "thrifty science" confound; span arbitrariness —
   contract can specify any anchor: fork from 0, from step T, etc.).
2. New agent-facing surface: tool list + what probe_status returns now (time,
   interface counts, phase, announced contracts; NO budgets); fork/reset tools;
   how contract instances are presented (anchor+protocol explicit in text).
3. Scoring: unchanged formula skill = clip(1 - CRPS/CRPS_best_rung, -1, +1),
   unsubmitted = -1, reward = mean over menu (cite blobround2.py). What changes:
   truth generation per instance spec; baselines per anchor; floors re-derived.
4. Tier mapping v1->v2: L1/L2/L3F/L3S/L3E/L4/L4D survive with anchors made
   explicit per instance; note which v1 semantics change (lock removal affects
   L1/L2/L3* framing; L4/L4D unchanged in spirit).
5. Scripted actor v2: same play policies re-expressed on the new surface
   (it currently plays at span end; now plays per-instance anchors).
6. Migration/validation plan: A0-style adequacy re-run (does the scripted actor
   still separate worlds), floor tables recomputed (smoke_blob2 equivalent),
   safety-cap monitoring, comparability note (v1 vs v2 rows never mixed).
7. Open questions section (short): anchor selection policy for instance
   generation (spread over t incl. late anchors; avoid all-anchors-equal-t0),
   fork-state anchors in scored instances (v2.0: base-line anchors only —
   RECOMMEND and say why: truth caching + comparability), replica count for
   truth ensembles (keep 12? justify or raise).
## Context files (read for continuity, cite paths)
- probes/blobs/l0/deepsearch/TRACKA_CLEANSLATE_EVAL.md (v1 design)
- environments/physim/physim/blobcore.py (BUDGETS, T0/T_EP, MAX_REPLICAS, AMP_CAP)
- environments/physim/physim/blobround2.py (menus, _skill, LOCK_AT_INJECT)
- environments/physim/physim/servers/blob.py (current agent surface incl. budget
  advertisement to be removed)
- docs/blobs/measuring-evolved-worlds.html (post 11; round-5 will need a post
  update AFTER implementation — note as future work, do not edit)
Style: match TRACKA_CLEANSLATE_EVAL.md's register (decisions, tables, terse).
Do NOT change any code. Output only the new .md file. Do NOT commit.
Reply to parent with: file path, section list, and any decision the brief left
genuinely open that you had to make (list explicitly).