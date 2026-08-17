# WORLD-SEARCH PROCESS LOG (global controller ledger)

Goal of this file: record how the CREATION PROCESS itself behaves — not just
which world wins. Updated by the controller (parent agent) each round.

## Meta-metrics tracked per searcher per round
- candidates tried / passers (raw yield)
- where the yield came from: theory-coordinate choice? seeded from prior
  probe code? literature prior?
- gate-failure distribution (which gate kills most candidates — tells us
  which property is scarce in mechanism-space)
- wall-clock per candidate + total (cost model for scaling estimates)
- iterations of the LOCAL loop (implement -> sweep -> refine) before pass
- controller interventions (feedback given, briefs revised, respawns)

## Round 1 (2026-02-17, launched)
Five directions, chosen to span mechanism-space:
- trophic-tower (sub-7d147585): 3-level food chain -> lynx-hare oscillator
- fire-forest (sub-e4566a4f): slow fuel + fast excitable fire -> sawtooth/SOC
- guild-economy (sub-9189cfb6): E2 prices + allocation gene -> market clearing
- morpho-counter (sub-3d8e06db): Turing count staircase + hysteresis
- slime-lifecycle (sub-9983dfe4): chemotactic aggregation lifecycle

Hypotheses this round should test about the PROCESS:
H1: theory-coordinate sweeps transfer across mechanisms (E2 lesson generalizes)
H2: the scarce property is the SIMPLE TOP (G2), not hierarchy per se (G1)
H3: mechanisms with a known real-world analogue converge faster (priors help)
H4: 5 parallel local searches + 1 global controller >> 1 serial deep search
    at equal compute (to be judged by yield/hour)

Early observations (T+~40min):
- All 5 running; no crashes. fire-forest already at switch-top r2=0.70 with
  sep 9.2x/38.7x (close to G2 bar). trophic-tower mapping cycle-vs-steady
  boundary in (saturation, mortality, rho) space. guild-economy REUSED the
  E2 probe code as its base (good transfer). slime-lifecycle managing
  Keller-Segel blowup with an explicit stability check (ok/why pattern).
- Controller policy: no mid-flight interruptions; feedback lands against
  scorecards. Exception: hard numerical blowup or gate misreading.
