# R5 SPEC REVISION BRIEF (v2.1 — category-anchored contracts, closed-book reveal)
Revise probes/blobs/l0/deepsearch/TRACKA_R5_ANCHORS.md IN PLACE (still uncommitted
draft). The fork-oracle acceptance is SUPERSEDED by a stronger design the user chose.

## New core mechanic (this becomes the defining feature of v2)
TWO-PHASE EPISODES, category-anchored, instance-hidden:
Phase A (exploration): from t=0 the agent sees the contract CATEGORIES (the
  "syllabus"): per tier, the payload schema, the scoring ladder, and the PUBLISHED
  INSTANCE-SAMPLING DOMAIN (ranges, not values): e.g. "L3F: predict device-i
  streams (t=0 config) from anchor t_a, horizons H; i in devices, t_a uniform-
  continuous in [200, 2300], H in {5,25,100,400}"; "L1: response to a hidden
  adjust-command sequence (len<=3, u in [-1,1]^3 continuous) applied from t=0
  config at hidden anchor"; injections: port x amp(continuous) x dur(continuous).
  Free exploration: forks from any anchor, injections/adjusts/reads, no meters
  (v2 (a)/(b) unchanged). Fork-ensembling during Phase A is legitimate and
  USELESS for rehearsal because instances are unknown.
Phase B (reveal, agent-triggered): agent calls probe_ready() -> concrete
  instances revealed -> ALL world access closes (reads/waits/forks/injections
  return a phase error; probe_status + probe_submit remain). The agent answers
  from its theory artifacts: notes, fitted models, ITS OWN code/simulators run
  in the harness (bash/python fully allowed — only the world itself is closed).
  Submissions revisable until episode end; unsubmitted = -1 unchanged.

## User decisions (verbatim intent, do not weaken)
1. Reveal trigger: agent-declared "ready" ONLY. No fixed reveal time — a set
   time is another cap that makes agents worry about timing while they work.
   Exploration ceiling exists only as the GENEROUS silent safety cap (the
   existing live-sim tu cap; never surfaced, target hit-rate 0).
2. Instance domains MUST make brute-force rehearsal infeasible AND visibly so:
   every tier keeps >=1 effectively-continuous hidden dimension (anchor t_a,
   sequence u-values, injection amp/dur), so gridding the domain is hopeless
   and rational agents do not attempt it. The published domain text states
   continuous sampling explicitly. Enough ambiguity on what will be measured,
   input, adjusted.
3. Post-reveal: NO world access at all (not even base-line re-reads). The agent
   may use anything else in the harness: run code, its own fitted simulator,
   notes. The benchmark thereby scores the PORTABLE ARTIFACT the agent built —
   explicit bridge toward the L6 executable-theory lane.

## Required spec changes
- PART 2: add the two-phase structure + probe_ready tool; tool table gains
  phase column (which tools live in which phase); status shows phase =
  exploration|revealed + per-instance submitted flags after reveal.
- PART 3: fork-oracle section rewritten: oracle is dead by construction
  (Phase A: instances unknown; Phase B: lab closed). Scoring formula unchanged;
  truth ensembles generated AT REVEAL (cache per instance); ladder baselines
  computed from the pre-reveal base record (they are category-generic — floor
  stays classical and fair). E1 H=5 leg un-flagged (meaningful again).
- PART 4: per-tier table gains "hidden instance parameters + published domain"
  column; L4D secret amp becomes the NORMAL case of the general pattern.
- PART 5: scripted actor two-phase play: generic exploration, early ready,
  answers revealed instances from classical stats on its pre-reveal record.
- PART 6: add gates: reveal-leak audit (no instance info derivable pre-reveal),
  post-reveal isolation test (world tools dead), brute-force-infeasibility
  documentation per tier (domain cardinality/continuity), time-to-ready logged
  as a silent meter (Pareto axis).
- PART 7: Q1 (anchor policy) folds into the domain-publication requirement;
  keep Q2/Q3; add Q4: does Phase-B code-running advantage coding harnesses
  over chat tiers (note: BLOB2 is already coding-harness-native; fine).
- DECISIONS AT A GLANCE table: update rows (known instances -> known categories
  + hidden instances; add closed-book reveal row).
Keep register/length discipline; the doc stays one file. Reply to parent with:
revision summary (5 lines), any internal inconsistencies you had to resolve,
and the exact new "syllabus" text you drafted for E1 (verbatim) so the user
can review the published-domain wording directly.