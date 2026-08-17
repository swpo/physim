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


## Round 1 fan-in (updating as scorecards arrive)

### fire-forest — scorecard received T+~3.5h, AUDIT PASS (first certified world)
- 70 candidates logged; W7 winner (theta=.78 Lam=9 M=2 D=8 gsig=.35 rho=.03 g=2e-3)
- Controller audit: fresh seeds 11/12 via their own ff_core -> switch r2 .873-.886,
  tau 2/85/1440, sep 41x/17x, ~100 events, 3.8s/probe. G3 spot-check beyond their
  sampled range: g=.001 -> tau3=2819; g=.006 -> tau3=520 (monotone, ~g^-0.64). CONFIRMED.
- Process notes: theory coordinates (rate RATIOS + threshold) worked (H1 +1).
  Their negative results show the G2/L2-richness TENSION: SOC corner (Lam>=15)
  kills top-law simplicity (r2<.81) — evidence for H2 (simple top is the scarce
  property, and it TRADES OFF against middle-layer richness).
- Honesty: refused to certify SOC (spanning bump at L^2, only broadband) — the
  honesty rules are being followed under incentive to claim more.
- Controller action: ROUND 2 issued to same agent — SUCCESSION TOWER (4th layer:
  savanna-forest bistability above the fire clock; tests hierarchy STACKING,
  the user's scaling question directly).


### trophic-tower — scorecard T+~5h, AUDIT PASS (second certified world)
- 292 runs / 215 candidates; TC* teacup (sig1=4.5 mu1=.4 d1=.4 sig2=2 eta2=.44
  rho=.034 DH=.05 Delta=4 nu=.03); 6s/candidate.
- Controller audit: fresh seeds 31/32 reproduce T3=165.5 T2=26 tau1=4.9 sep 5.3/6.3.
  G3 out-of-grid: rho=.025 -> T3=227 (their law predicts 232); rho=.055 -> 107 (105).
  CONFIRMED — though rho=.055 shows teacup edge (T2_q .32, sep23 3.8): narrow window
  is real. G1 margins thinnest so far (5.2-6.4x vs fire-forest 41x/17x).
- Process notes: staged sweeps (results_stage1-6) = systematic local iteration; the
  honest 0-D mean-field control (ragged switch r2=.76) proves SPACE CLEANS THE TOP
  LAW — a design principle worth promoting to PROGRAM.md round 2. Warm-start trick
  (skip 700-tu predator ramp) = useful budget lesson. H3 support: lynx-hare prior
  clearly guided the search (Holling-II + saturation window from literature).
- Controller action: ROUND 2 issued — ECO-EVOLUTIONARY TOWER (heritable attack rate
  with linear price on top of the cycles; L4 = mean genotype; tests stacking via a
  DIFFERENT coupling than fire-forest's succession: evolution-on-oscillator vs
  competition-on-oscillator). Two parallel stacking experiments now running.
