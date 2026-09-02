
=============================================================================
CLEAN-SLATE DESIGN: grading scientific understanding in evolved blob worlds
(design research step — 2026-09-01; compare-then-merge with existing suite)
=============================================================================

PART 0 — WHAT ARE WE GRADING? (first principles, ignoring our history)
'Understanding a world' decomposes into gradeable capabilities:
  ONTOLOGY   carving the world at its joints (what entities/quantities exist)
  DYNAMICS   what happens next (forecast, with honest uncertainty)
  CAUSALITY  what happens IF (interventions, dose-response, propagation)
  TRANSFER   does the model survive new conditions (seeds, poses, regimes)
  ECONOMY    compactness + budget-efficiency (understanding vs lookup table)
Grading principle #1: never grade descriptions (language is gameable); grade
PREDICTIVE CONSEQUENCES of having the right description.
Grading principle #2 (learned from rounds 1-3): contracts ARE the curriculum —
unpriced capabilities go unexercised. Design the contract set to SPAN the
capabilities, or agents rationally skip them.
Grading principle #3: score = SKILL, not raw accuracy: normalize every
contract against a published baseline ladder (climatology / persistence /
AR(2)); skill = 1 - CRPS_agent/CRPS_baseline. Removes world-difficulty
confounds; makes 'beating the bar' explicit per contract. (Round-1 P1 looked
'nearly skill-free' precisely because we scored raw CRPS on a world where
persistence saturates — skill scoring would have shown ~0 honestly.)

PART 1 — THE CAPABILITY LADDER (clean-slate contract families)
 L1 INSTRUMENT: pose-targeted prediction. 'After adjust command U (announced),
    predict your device's streams.' Prices actuator calibration + local
    geometry. Cheap to score (run the replica). NEW.
 L2 NOWCAST (hidden sensor): 'a harness sensor exists somewhere (undisclosed
    pose); given your exploration, predict ITS current reading distribution.'
    Prices spatial world-modeling (interpolation needs a field/object model).
    Variant: predict ANOTHER device's streams from your own (cross-device
    nowcast — already implicitly in P3 controls). NEW.
 L3 FORECAST: current P1/P2, but (a) multi-horizon spanning the world's
    deterministic->stochastic transition (the predictability horizon IS a
    world property agents should discover; honest sigma widening = skill),
    (b) object-flavored targets where the world is particulate (event rates,
    census-like aggregates), (c) slow-observable variant for structurally-
    dynamic worlds (E2: predict long-window aggregate trends — prices the
    frozen-census/reorganizing-structure split the films exposed). KEEP+FIX.
 L4 INTERVENTION: current P3 + two strengthenings: dose-response (predict at
    an UNANNOUNCED amplitude within the calibrated range — tests law-learning
    vs point-matching) and propagation geometry (multi-device arrival). KEEP+.
 L5 CONTROL (preparation): 'drive named sensor observable into band B and
    hold for T' under injection+adjust budget. The strongest causal test; the
    classic prep-track ports directly. Scoring: time-in-band (existing prep
    scoring machinery). PORT from classic suite (was spec'd as P4, unbuilt).
 L6 THEORY (executable): compact predictor submitted as CODE, scored on
    (a) held-out seeds of the same world, (b) held-out poses/sensor layouts,
    (c) budget-free replay (theory runs without the instrument). Size-capped
    (MDL pressure). This is the rich-vs-big engine on evolved worlds: score
    god-probe baseline / compact oracle / budgeted agents on the same grid.
    PORT from classic suite (P5) — heaviest build, phase last.

PART 2 — WORLD-ADAPTIVE CONTRACT SELECTION
Fixed contract menus misprice heterogeneous worlds (E1 needs no geometry;
E2 punishes its absence). The evaluator KNOWS each world's certified
phenomenology (assay records: n_species, succession stages, spatial class,
motion class, timescales). RULE: generate the contract set per world from
its own phenomenology — every certified phenomenon gets >=1 contract that
prices it; no contract references phenomena the world lacks.
  E1 (global oscillator): L3 fast + L4 (geometry-light) — matches round 1-3.
  E2 (champion, reorganizing labyrinth): L1+L2 (geometry load-bearing) +
     L3-slow (structural trends) + L4.
  E3 (swarm): L3-object (census/rates) + L4 + L5 (herd the swarm?).
  v3 economy worlds (walls/sparse): L2 (voids make interpolation hard) +
     L4-propagation (walls block/deflect — prices boundary discovery) + L5.
Barrier note: world-adaptive selection uses evaluator-side knowledge only
(one-directional: the MENU discloses nothing beyond what any contract
necessarily discloses about what is measurable).

PART 3 — OVERLAP AUDIT vs EXISTING SUITE
 KEEP AS-IS: episode structure (replay->T0->replica forks), CRPS + honest-
   sigma scoring, budget system, barrier mechanisms, report-only conduct
   metrics, scripted-baseline reference runs (A0 pattern).
 STRENGTHEN: (1) skill-normalized scoring (baseline ladder inside the score);
   (2) P3 -> +dose-response leg (unannounced amp); (3) P1 -> multi-horizon
   spanning predictability transition; (4) publish per-contract baseline
   table with the env (the scripted actor becomes part of the benchmark).
 ADD (phased): L1 pose-targeted (round 2, cheap), L2 hidden-sensor nowcast
   (round 2, cheap — biggest bang for geometry-pricing), L5 preparation
   (round 3 — port classic machinery), L6 executable theory (round 4 — the
   rich-vs-big reproduction on evolved physics).
 SLIM/REMOVE: (1) P1 on baseline-saturated worlds (report skill~0 honestly
   or drop from the menu per Part 2 rule); (2) the rigid 13-lag P3 grid ->
   fewer announced lags + the dose leg; (3) drop the 'suggested science'
   hints in the system prompt (round-3 evidence: fable follows its own
   program anyway; hints risk anchoring and leak our framing of what's
   interesting).
 REMOVE (nothing else): no other existing piece conflicts with clean-slate.

PART 4 — WHAT THIS BUYS (why not just iterate)
The historical path optimized contracts for point-tap worlds (classic tracks)
then ported them. Clean-slate exposes the two structural gaps that iteration
kept missing: geometry/pose is never priced (L1/L2 absent) and law-vs-point
learning is never separated (L4 dose leg absent). Both are cheap adds. The
expensive historical assets (episode/replica machinery, CRPS, barrier,
baseline-actor pattern) all SURVIVE clean-slate scrutiny — the design was
right; the contract MENU was track-shaped.

NEXT: user review -> spec the round-2 contract set (L1+L2+strengthened L3/L4
on E1r3+E2) -> a1-harness implements -> scripted-actor baselines -> eval.
=============================================================================
