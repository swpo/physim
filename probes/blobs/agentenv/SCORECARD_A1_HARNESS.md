# SCORECARD — a1-harness (Track A round-1: BLOB env + post 11)

MISSION: ship Track A round 1 as a physim difficulty family — the probe-device
environment as a verifiers/MCP world-server tier — verify it with a scripted
null-harness actor AND one real-model episode, and publish the setup post.
The Fable-5 / gpt-5.6-sol evaluation episodes are NOT launched here (separate
controller decision on this scorecard).

## Deliverables (each committed + pushed)
- **B1 environment** (`db6970e`):
  - `environments/physim/physim/blobcore.py` — evaluator core. Episode registry
    (BLOB-E1 live on p4g2_044 s928/929/930; BLOB-E2/-E3 registered but GATED),
    A0 reuse (agentenv `device.py` imported via path bootstrap — ProbeDevice /
    CachedRun / step_chunk / world_secrets NOT reimplemented; roster = A0 r2
    with hex-19 as the strong witness, `world_key` identical so all cached
    secrets + injection branches match), contracts P1' (respec H=5/15/25tu per
    adequacy F3) / P2 events (A0 announce rule) / P3 flagship (announced amp-3
    protocol = the cached branch), scoring CRPS/MAE vs scripted baselines,
    live replica fork from the T0 f32+RNG snapshot.
  - `environments/physim/physim/servers/blob.py` — the agent surface (MCP
    toolset `probe_*`): status / read_streams / wait / move / dilate / inject /
    submit. Budgets enforced server-side (sensor 40,000 node-tu = 2x A0
    baseline; motion 1,200 cu; injection 120 amp-tu at price
    amp*(1+4*max(0,amp-0.5)), cap amp<=1.0 — the beacon fix). Span hard-stop
    at T0=1700tu; injections = replica forks only; first inject locks P1/P2.
  - `environments/physim/physim/taskset.py` — additive BLOB branch (BlobData/
    BlobTask/_blob_task, load() dispatch, difficulty literals). No
    restructuring of existing tiers.
  - `environments/physim/tools/test_blob_server.py` — 5 gates, ALL PASS:
    T1 tool loop + ledgers + hard-stop; T2 amp-0 replica == cached A0 control
    branch BITWISE (f16; required workers=3 — FFT op order); T3 pricing/caps/
    locks + response detectable at cap; T4 barrier regex audit over every tool
    response + prompt + docstrings + contracts; T5 submit shapes/revision/locks.

- **B2 SMOKE** (`4e76fa7`):
  - SMOKE A (null-harness scripted actor, `tools/smoke_blob.py`): the A0
    informed pipeline re-expressed against the MCP tools ONLY. Seed 928:

    | metric | agent-surface actor | scripted ref (baseline) | A0 grade |
    |---|---|---|---|
    | P3 CRPS | 0.0050 | persistence 0.1545 | ratio 31x (A0 x4/r2: 5.0x)* |
    | P2 MAE | 1.03 | better-of-zero/rate 1.21 | beats ref (A0: 1.8 @ 4x) |
    | P1' CRPS | 0.1366 | persistence 0.1322 | 0.97x = respec headroom |
    | reward_accuracy | 0.60 | 0 by construction | — |
    | budgets | sensor 32,140/40,000 · inj 37.5/120 · motion 0 | | respected |

    *31x > A0's 5x because the actor reads the control replica at the exact
    scored lags (round-1 design allows paying for that) and the persistence
    baseline uses climatology sigma. Verdict: adequacy-grade P3 skill
    reproduces through the agent interface; gates all pass.
  - SMOKE B (real model, cheapest lane): gpt-5-nano / null harness / BLOB-E1
    seed 928, one episode, $0.0146, 4.5 min wall, stop=agent_completed.
    The loop END-TO-END works: tool server boots from sdist, state channel
    carries the episode, the model called status -> (premature submits
    rejected with shape errors) -> wait to span end -> 3 replica injections
    (amps 0.6/0.4/0.5 — it discovered sub-cap calibration!) -> P2 submit
    correctly REJECTED by the P1/P2 lock -> P3 attempt rejected on shape.
    Score honestly 0 (nothing valid submitted) with correct metrics
    (span_frac 1.0, n_replicas 3, spend fracs recorded). nano-grade model,
    expected; the mechanics are what was under test.
  - BARRIER AUDIT on the REAL transcript: all 14 agent-visible strings
    (system+user prompts, tool schemas, tool responses; 162,633 chars)
    grepped against 33 leak patterns (coordinates, lattice words, port/field
    names, blob words, world ids, secret words): ZERO hits.

- **B3 POST 11** (`8df6fdc`): `docs/blobs/measuring-evolved-worlds.html` —
  setup edition: why point taps fail on particulate worlds; the probe-device
  ("learn to use your hands", fixed retinotopy, center-co-located emitter);
  barrier rules + CI leak grep; the A0 study (curves fig, capability table,
  1x-4x knee -> 2x budgets, P1 respec, amp-3 beacon -> cap); contract ladder
  with weights; round-1 roster table (Fable 5 claude_code, gpt-5.6-sol codex,
  scripted null row); Results section stubbed "round 1 in progress".
  Index entry 11 + badge shuffle + home-card mention.
  URL: docs/blobs/measuring-evolved-worlds.html

## Round-1 launch line (for the controller)
```
.venv/bin/eval physim -n 3 -m anthropic/claude-fable-5 \
  --env.taskset.difficulty BLOB-E1 --env.scientist.harness.id claude_code \
  --env.scientist.runtime.type docker --env.scientist.max-turns 120
.venv/bin/eval physim -n 3 -m openai/gpt-5.6-sol \
  --env.taskset.difficulty BLOB-E1 --env.scientist.harness.id codex \
  --env.scientist.runtime.type docker --env.scientist.max-turns 120
```
Notes: tool server runs host-side subprocess (needs the A0 caches at
`probes/blobs/agentenv/cache/`, 11 GB local); the harness containers only
need the MCP URL. Cost anchor: nano smoke = $0.015/9 turns; frontier
episodes with real exploration will be dominated by read-heavy tool
responses (~60k-number cap per read keeps context sane).

## Known limits (honest)
- P1' actor skill ~persistence (0.97x): AR2-on-burst-reads doesn't help at
  H<=25tu on E1 with this read plan; agents have headroom via denser
  end-of-span reads (the contract is deliberately not saturated).
- ReplayEnv path is exercised for the main span via blobcore.sample_at on
  cached frames (equivalent surface); WorldEnv live stepping only in
  replicas. E2/E3 gated: contracts respec needed (A0 F7) before opening.
- Score-time baselines recompute cached-truth streams per call (~seconds);
  fine at round-1 scale.


## R2 addendum (interface change order + amendments, 2026-09-01)
Spec: probes/blobs/l0/deepsearch/TRACKA_R2_CONTROLS.md. Shipped:
- probe_move + probe_dilate REPLACED by probe_adjust(device, u1, u2, u3,
  steps, read): u in [-1,1]^3, per-step pose delta = M @ u with M = secret
  per-world 3x3 mix (Haar SO(3) x row scales 1.0-1.5/1.0-1.5/0.6-1.0;
  cond <= 2.5; salted-hash seeded from world_key, independent of A0 secrets).
  Translation and dilation are MIXED: the control factorization itself is
  now undiscovered science.
- ONE 'adjust' budget (1200 cu, sum|u| per step, charged as COMMANDED).
- Bound behavior (amendment 2): a step that would cross a spacing bound is
  REFUSED — generic result:"adjust_rejected", no reason/channel/value;
  the refused step still charges sum|u| (strain); remaining steps in the
  call do not run and are not charged; refused steps return no streams.
  Translation-only commands cannot be refused (torus), but a refused mixed
  step blocks its translation component too (intended entanglement).
- Emitter co-location disclosure REMOVED everywhere (status, inject docs,
  system prompt): emissions enter through "a fixed emission channel";
  localizing it from transients is intended science.
- Difficulty tag BLOB-E1r2 (BLOB-E1 registered+gated as superseded, so no
  result mixing).
- Regates: 6/6 server gates PASS (new T6: known-M pose math, both walls,
  strain equality via exact ledger, multi-step partial application,
  rejected-step stream absence; T4 barrier list extended with co-locat/
  position/located/center/origin/motion/move/translat/dilat/spacing/zoom/
  scale/scaling/adjacen/pose/emitter + the adjust_rejected response
  key-set check). Scripted smoke rerun: SEE results/smoke_blob_s928.json
  (actor never adjusts; reproduces round-1 scores through the R2 surface).
- Post 11 updated: R2 revision note (the API-shape leak story), actuator
  row in the interface table, emission wording, BLOB-E1r2 repro line.


## R3 addendum (final control revision, 2026-09-01)
User verdicts: (R3) channel mixing = difficulty without depth (like the
rejected sensor shuffle) -> pure per-channel effects; (R3-final) drop the
permutation/sign/scale secrecy too -> FIXED GLOBAL convention u1->dx (x1.5),
u2->dy (x1.5), u3->dlog spacing (x1.0), identical across worlds, simply never
documented (undocumented IS the mechanism; instrument mastery transfers, the
world is what varies — the fixed-retinotopy principle applied to actuators).
Kept from R2: single adjust budget, commanded-|u| cost, generic
adjust_rejected + strain at the (undisclosed) spacing bounds, zero location
language, pure-translation never refused. Tag BLOB-E1r3 (E1r2 gated:
'mixed-control variant, retired before any scored rollouts were kept').
Regates: 6/6 server gates PASS (T6 rewritten for the fixed map: pose math,
both walls incl. wall at exp(1.0)=2.718 from 5x u3=0.5 steps, strain equality,
partial application, pure-translation-at-the-wall). Scripted-actor smoke
EXEMPT this round: the actor never calls probe_adjust and the R3 change is
adjust-only — the r2-surface smoke result (reward 0.6004) remains the valid
null-harness row. Post 11 revision box now tells the full R2->R3 story.


## ROUND-2 addendum (clean-slate contracts, 2026-09-02)
Spec: TRACKA_CLEANSLATE_EVAL.md Parts 1-3. Shipped ADDITIVE (BLOB-E1r3
untouched): tags BLOB2-E1 (p4g2_044) + BLOB2-E2 (p6g8_033, gate OPEN with
its A0-caveat menu). New module physim/blobround2.py; server round-2 branch
(status menu mode + submit contract-id routing + lock set L1/L2/L3* at first
inject, L4/L4D open); taskset Blob2Data/Blob2Task/_blob2_task, slim prompt
(no 'suggested science' hints).

CONTRACTS: L1 pose-targeted (K=3 announced opaque [u1,u2,u3] sequences,
wall-safe by construction; truth = cached main line at the walked pose,
frame T0+steps) | L2 hidden-sensor nowcast (harness-owned square-13 at a
secret pose seeded near the roster midpoint; zero pose language — gated) |
L3F multi-horizon (E1 H=5/25/100/400; E2 drops H5) | L3E events (E1 only) |
L3S slow observables (E2 only: 200tu-windowed global mean+var at T0+400/800)
| L4 response (6 lags, slimmed from 13) | L4D dose leg (table over amps
.30/.45/.60/.75/.90 at 3 lags, scored at ONE secret amp ~ U[0.3,0.9] via
linear interpolation; truth = live replica, disk-cached under
cache/round2/).

SKILL SCORING: skill = clip(1 - CRPS/CRPS_best_baseline, -1, 1); ladder
(climatology/persistence/AR(2) where sensible) computed evaluator-side at
score time and PUBLISHED in detail.baselines; unsubmitted = -1; reward =
mean skill over the world menu.

GATES: round-2 G1-G6 ALL PASS (registry/menus; L1 pose/truth parity through
the agent surface; dose interpolation exactness + announced-port==branch-
port; skill clipping; barrier audit over 10 surfaces with the extended
pattern list + location-hint words; submit/locks). Legacy 6/6 still PASS.

SCRIPTED-ACTOR BASELINE TABLE (the published reference row; smoke_blob2.py):
| contract | E1 skill | E2 skill | note |
|---|---|---|---|
| L1 | +0.15 | +0.11 | executes announced walks on-span, reads, walks back |
| L2 | -0.00 | -0.00 | HONEST GAP: script has no spatial model; ~ties the global-aggregate baseline. This is the measurement — L2 headroom belongs to agents that build one |
| L3F | -0.06 | -0.06 | AR2/climatology blend ~ ladder's own AR2 (expected ~0) |
| L3E | -0.55 | — | trend extrapolation UNDERSHOT this seed's rate lift; honest scripted weakness (round-1 P2 logic, same code) |
| L3S | — | -0.29 | persistence of last window; sigma too tight on the var column |
| L4 | +0.89 | +0.65 | control+calib template, 4 replicas, 41.4/120 inj budget |
| L4D | +0.99 | +0.99 | linear dose law nails the drawn amp (E1 0.882, E2 0.659) |
| REWARD | +0.238 | +0.233 | mean over menu |
Both smokes: budgets respected, all contracts submitted, wall ~225s.
Negative rows are kept as-is: skill-normalized scoring is SUPPOSED to show
scripted weaknesses honestly; agents beating 0 on L2/L3E/L3S is exactly the
signal round 2 exists to measure.

Launch lines (E2 max_turns higher — bigger menu):
```
.venv/bin/eval physim -n 3 -m anthropic/claude-fable-5 \
  --env.taskset.difficulty BLOB2-E1 --env.scientist.harness.id claude_code \
  --env.scientist.runtime.type docker --env.scientist.max-turns 150
# same for BLOB2-E2; and openai/gpt-5.6-sol with codex.
```
Dose-truth caches for all 6 (world,seed) pairs prebuilt under
probes/blobs/agentenv/cache/round2/ (gitignored, rebuild = ~30s each).
