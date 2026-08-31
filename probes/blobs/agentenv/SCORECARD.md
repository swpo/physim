# SCORECARD — a0-adequacy (Track A probe-device + A0 measurement adequacy study)

MISSION: build the agent-environment probe-device layer (measurement v3 spec)
and answer, BEFORE any agent trials: can scripted reference pipelines see,
calibrate, track, and forecast through the anonymized sensor surface at sane
budgets — and where are the curves steep?

## Deliverables
- device.py (W1): ProbeDevice (square/squareC/hex/tri lattices, secret
  rotation+reflection, secret node perm, dilation 0.5-3x, bilinear sampling),
  WorldEnv (live sim via local verbatim-op stepper, bitwise-gated vs locked
  sim_cpu.advance), center injection through the poke pathway under integral
  budget, ReplayEnv + run_cached (sim-once/replay-many; f16 frames @5tu, truth
  blob lists, f32+RNG snapshots for live branches). 9/9 gates.
- refpipes.py (W2): R1 geometry bootstrap (diff-corr distances -> isomap ->
  gap adjacency -> lattice class; dilation radial probe -> template snap;
  drift-canceled motion-basis probe with LK matching), R2 particulateness
  (polarity-aware bimodality/Fano/event stats) + dilation size scan,
  R3 watch/track P-controller (online core threshold, prediction-gated
  association, velocity coasting, excursion leash), R4 contract baselines
  (persistence/AR2-clamped/informed advection; duty-corrected event rates;
  amplitude-scaled injection-response templates). 7/7 gates on synthetic.
- adequacy.py (W3): 54-cell study (E1/E2/E3 x r1/r2 rosters x 4x/1x/quarter
  budgets x 3 seeds), evaluator-side scoring vs cached truth, aggregate +
  curves. 4/4 gates; 54/54 cells green.
- ADEQUACY.md (W4): curves, verdict table, round-1 recommendation, honest
  failure list.

## Verdict table (means over 3 seeds; r1 = hex-19 solo, r2 = square-13 + hex-19)

| capability | E1 sparse | E2 champion | E3 swarm | budget shape |
|---|---|---|---|---|
| R1 lattice class | 1x 100%, 1/4x 0% | same | same | CLIFF below 1x |
| R1 adjacency F1 (r1) | 4x .84 / 1x .42 / q .47 | .55/.41/.31 | .55/.49/.64 | steep |
| R1 motion basis | 67/33/0 % | 100/33/0 % | 33/33/0 % | needs ~4x |
| R2 particulate verdict | 100% all tiers | 4x only | 4x sure | E1 flat, E2 steep |
| R3 hold after lock | 4x 100% | 64% | 10% | steep + world-graded |
| R3 same-blob retention | 4x 79% | 51% | 10% | world-graded |
| P1 AR2 skill vs climatology H50 | +.07 | +.00 | -.01 | FLAT (weak contract as spec'd) |
| P2 rate-MAE vs zero baseline | beats 4.5x | ties | ties | steep on E1 |
| P3 informed vs persistence | 5.0x better | 3.4x | 3.2x | steep, robust everywhere |
| P3 response z | 620-960 | ~5.9k | ~8-10k | detectable at ALL tiers |

## Headline answers
1. YES — blobs are visible and trackable through anonymous sensor nets at 4x
   (E1: 100% hold, 79% identity retention over 360tu), and the geometry
   bootstrap (incl. secret lattice type, node adjacency, motion basis up to
   chart rotation) is recoverable without any spatial disclosure.
2. The steep budget region is BETWEEN 1x and 4x for everything closed-loop;
   1/4x is below the measurement floor (recommend round-1 = 2x baseline).
3. P3 (announced injection -> cross-device response) is the strongest
   contract: budget-sensitive, causal, robust on all three worlds. P1 at
   H=50-200tu is nearly skill-free for point streams — respec with shorter
   horizons or slow-channel targets before round 1.
4. Honest failures: E3 swarm tracking (10% — neighbor-stealing at 151
   organisms), absolute size via dilation (skirt-biased ~4x under on E1),
   motion calibration at <=1x, open-loop pursuit beyond ~2 patch radii,
   E2 'blob identity' frays conceptually (stripes reorganize; prefer P4-style
   preparation contracts there).
5. Roster: 2 devices confirmed (cross-device P3 needs it); make hex the
   mobile prober; square-13 is a measurably weaker solo instrument.

## Cost & compliance
Local CPU only, ~4.5 h wall total (9 sim caches in 3 parallel batches, ~22 min
each; 54 pipeline cells at 5-11 s each thanks to sim-once/replay-many).
No locked blobkit files edited (local stepper gated bitwise instead). No GPU,
no rentals. Caches (7-11 GB) gitignored; code+results+report committed.

## Verification
- test_device.py: lattice counts/unit-NN, bilinear exactness, BITWISE parity
  of step_chunk vs locked advance() (25tu), obs anonymity, secret basis
  orthonormality, injection budget+effect+rejection, replay==live (4.6e-4,
  f16), snapshot-branch bitwise vs uninterrupted, secret determinism.
- test_refpipes.py: geometry/motion/particulate/track/P1/P2/P3 on synthetic
  worlds with exact truth (angle errors <9 deg, tri/square/hex classified).
- test_adequacy.py: dev0 anchor sharing across rosters (branch reuse), read
  plans within budget with anchors always funded, control-branch==main-cache
  parity (0.0), smoke cell.
