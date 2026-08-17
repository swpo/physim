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


### slime-lifecycle — scorecard T+~6h, AUDIT PASS (third certified; cleanest top law)
- 92 runs logged; c30 winner. Fresh seeds 41/42: period 2330, switch r2 .997-.999,
  seps 7.7/11.7 — reproduced. G3 out-of-grid AUDIT (dose-preserving path, T_fam=1300/
  6500): predicted within 1-2% by their analytic law period=0.695/rho+405 (which they
  DERIVED from famine-length integration — the top law is literally solvable).
- AUDIT LESSON (process): G3 response curves live on theory-coordinate PATHS (their
  rho sweep co-varies d0 to hold famine dose constant). My naive rho-only variation
  broke the world (no cycles). Controller audits must follow the searcher's path
  convention -> added to audit protocol.
- Process notes: 13 failed mechanism versions (v3-v13 froze into permanent towers)
  before the germination-dispersal commitment fix — deep local iteration, exactly
  what the subagent layer is for (H4 support). Found+fixed a mass-creation bug in
  advect+diffuse clipping (40x mass!) — numerical honesty. Controls prove the
  lifecycle is RESCUED by multicellularity (chi_a=0 crashes to V~0.002): the L2
  layer is load-bearing, not decorative.
- Controller action: ROUND 2 issued — CHEATER EVOLUTION (Dicty social evolution:
  heritable cooperativeness, relay cost private, aggregation benefit shared,
  assortment by clonal growth). Third stacking-coupling type: social-evolution-on-
  lifecycle vs succession-on-clock (fire) and evo-on-cycles (trophic).

### Round-1 stacking experiments now running (the scaling question, three couplings)
fire-forest+succession | trophic-tower+eco-evo | slime-lifecycle+cheaters


### morpho-counter — scorecard T+~9h, AUDIT PASS (fourth certified)
- 279 runs; flagship Dv=11 L=64 kap=.5 eps=3.2e-3 (auto-calibrated kstar2). Fresh
  seeds 51/52: switch r2 .91-.93, seps 6.5-7/11.7-12.2, 8 flips — reproduced.
  Out-of-grid eps=1.2e-3/4.2e-3: measured 2857/857 vs law 3167/905 (5-10% — law is
  approximate but monotone-smooth; weaker than slime's analytic law, stronger than
  none). G4 is the marginal gate (jitter 4/6@60k, pooled 13/18@120k, mechanism alive
  33/36) — honest reporting of a narrow-ish counter window.
- Design-epistemics note: C-servo (wavenumber-error feedback toward forbidden gap)
  is AUTHORED-BUT-INTERNAL feedback — same status as E2 prices. The staircase,
  hysteresis loop widths, defect events are computed. Recorded as acceptable pattern:
  "author feedback laws, not events".
- Process notes: metric-lock discipline (v3 frozen BEFORE certification) — good
  practice worth promoting; auto-calibration step (kstar2 from a calibration run)
  is a reusable trick for Turing-family worlds.
- Controller action: ROUND 2 issued — COUPLED COUNTERS (mutual sync of two integer
  clocks; L4 = phase-slip/rotation-number; expect saddle-node-ghost T_slip law).
  Fourth stacking-coupling type: synchronization-of-equals vs the three
  slower-ingredient stackings already running.


### guild-economy — scorecard T+~11h, AUDIT PASS (fifth certified; 5/5 round-1 worlds real)
- 224 evals; GE-F (rho=2.15 yW=.7 leak=.62 margin=7 over=1.5 r0=.006 hz=4.5e-4 DW=.02
  L96). Controller audit (post-outage rerun), fresh seeds 61/62: guilds+top-law
  reproduce, fr* 0.474 (theirs 0.473), s12 5.0-5.2 PASS, s23-time 4.6-4.7 (the AT-THE-
  LINE marginality they flagged; length-based s23 13-19x clean). Out-of-grid rho=2.75:
  fr*=0.566 — demand curve continues monotonically. CERTIFIED with the s23-time caveat.
- Emergent top law is the most "economic" of round 1: market clearing by marginal-
  return equalization; hazard rate is the market clock (tau3 ~ 1/hz) — externalizing
  hz as a dial is their (good) engine-integration suggestion.
- Honest negatives: over=0 -> generalists win (no guilds); leak window 0.5-0.65.

### INFRASTRUCTURE OUTAGE (user internet, T+~11-12h) — recovery log
- All 5 child sessions ended mid-round-2; my guild-economy audit process was killed
  pre-launch. On-disk state SURVIVED everywhere (results/logs/strips) — the
  file-based deliverable protocol is outage-robust by design. Kernel state survived.
- Recovery: reran guild audit (above); revived 4 children with precise resume
  prompts pointing at their own surviving files ("consolidate, don't redo");
  fire-forest never received round-2 brief (no succession/ dir) -> brief re-sent.
- Round-2 partial state found on disk: trophic ecoevo G*~0.75 attractor + THE BIG
  TENSION (evolution degrades the teacup: ecoTop r2~0.6, ecoG1/G2 False) — the
  stacking question is becoming "can towers coexist with their new layer?";
  slime cheaters: c* 0.10-0.35 polymorphism, high seed variance, regime
  classification needed; morpho sync: LOCKING CONFIRMED (rho=1.0 in tongue, slips
  outside, R_c(kc) edges mapped) — needs slip-scaling law + summary.
- Process lesson: child sessions are ephemeral, disk + controller ledger are the
  real program state. Resume prompts should always point at surviving artifacts.


## Round 2 fan-in

### trophic-tower/ecoevo — scorecard received; AUDIT: headline confirmed, boundary CORRECTED
- L4 attractor REAL (audited): G* from above/below, two clean G3 curves (G* vs price c,
  G* vs mutation m), evolutionary rescue (G0=3.0 -> meanP 0.02 -> recovers), variance
  maintained sd~1.3m. Their m=0/G=1 control reproduces certified TC* exactly.
- HEADLINE NEGATIVE partially confirmed, boundary corrected by audit: on fresh seed 71,
  m=0.15 dissolves the teacup (CONFIRMED: top switch r2~.6, ecoG1/G2 False) but
  m=0.02 KEEPS it coherent (CONTRADICTS their claim). Dissolution boundary lies in
  m in (0.02, 0.15); correction campaign requested (coherent-fraction vs sdG law).
- FIRST AUDIT CORRECTION of the program — the audit layer is earning its cost:
  headline claims survive, boundary claims get sharpened. Process rule reinforced:
  boundary claims need multi-seed fractions, not single-seed thresholds.
- The deep design finding stands either way: variance-for-evolution vs coherence-for-
  clocks is a REAL TENSION in this coupling type (evolution-on-oscillator). Compare:
  fire+succession (competition-on-clock) and slime+cheaters pending; morpho sync
  (clock-on-clock) locking already confirmed — stacking couplings differ in whether
  they preserve the lower tower.


## Round 2 — COMPLETE (all four audited, 2026-02-18)

### fire-forest/succession — AUDIT FULL PASS (the stacking winner)
- Fresh seeds 7/8: all 4 layers reproduce (L4 tau 15.2-15.9k r2 .90-.96; L3 switch
  r2 ~.90 SURVIVES under the tower; seps 46-50/18-20/8.2-8.4; span ~7600x).
- Bistability fresh seed 9: fF(savanna-init)=0.000 vs fF(forest-init)=1.000, identical
  params. Out-of-grid G3 gT=1.35e-4 -> T*=0.890 (predicted 0.885-0.905). CERTIFIED.
- Strongest local modulation: burns 15.45/cell grass vs 0.00 forest — the L3 clock
  lives only in the savanna phase (biome-gated clock, not destroyed clock).
- Honest negatives: flammable canopy kills L4; W>=0.3 kills settling; static site
  quality pins mosaic (no free 5th layer without climate forcing).

### morpho-counter/sync — AUDIT PASS (tongue certified; slip = mapped regime)
- AUDIT ARTIFACT CAUGHT AND FIXED: my first fresh-seed runs used runner DEFAULT
  eps_g=2.77e-3; ALL their certs use eps_g=2.4e-3. With the right convention:
  R=1.3 locked on 2 fresh seeds (rho 1.0000/1.0034, 0 slips), R=1.85 slips,
  and the kc=1.5e-3 tongue edge INTERPOLATES (R=1.40 locked / R=1.48 slips,
  their Rc=1.4406). Lesson repeated from E2: audits must replicate the searcher's
  full coordinate conventions — grab cand dicts from their results files, not
  runner defaults.
- Textbook Arnold phenomenology: rho staircase 1.0000+-0.005 over 1.7x detuning,
  half-width ~linear in kc (r2 .95 weak-4, saturates kc>=4e-3), T_slip divergence
  exponent -0.72 (free) / -1/2 (fixed, r2 .86) — SN-ghost consistent.
- Honest fail kept as finding: slip sawtooth strict G2 fails (CV~0.4 defect jitter,
  noise-independent 1e-5..2e-3) — integer clocks synced through a diffusive scalar
  keep their event jitter. No 3:2 plateau resolvable.

### trophic-tower/ecoevo — boundary campaign VERIFIED; certified as MAPPED NEGATIVE + law
- Their corrected table: coherent 3/3 at sdG<=0.057, 0/3 at sdG>=0.086 — sharp.
  My spot check m=0.05 seed81: sdG=0.075 -> dissolved (consistent, boundary
  sdG*~0.06-0.075). Their original m=0.02 claim was a G0-window confound they
  found and fixed after my audit flagged it — correction loop worked.
- Standing law: teacup coherent iff sd(G) <= ~0.06; strong selection needs m>=0.1
  (sdG~0.13+) -> variance-for-evolution and coherence-for-clocks are mutually
  exclusive HERE. Coexistence regime exists (sdG<=0.06, live L4) but tau4 there
  is >G5-budget slow — recorded untested, not failed.

### slime-lifecycle/cheaters — AUDIT PASS as regime-map world
- Fresh seed 21 tragedy: c_eq=0.124, aggregation dead (their claim: collapse to
  ~0.1, relay marginal). Fresh seed 22 bistability: mosaic_hi holds c*=0.776 with
  lifecycle CYCLING (agg=0.91) vs mosaic_lo collapse c*=0.065 agg=0. CERTIFIED.
- Headliners: tragedy-of-commons computed from physics; Hamilton verified in the
  negative (certified c30 global dispersal = zero assortment = cooperation always
  dies -> sociality REQUIRED a dispersal-physics change, M2 local+bottleneck);
  t_half ~ 1/lam; sd(c)* ~ mu^0.6. Drift-limited at 64^2 (N_e~15 mounds); no
  rescue oscillator in 61 runs (honest negative).

## THE STACKING LAW (round-2 synthesis; H2 sharpened)
Four coupling types tested. Hierarchy STACKS when the new layer's back-action on
the lower layers is (a) spatially COHERENT and slow (succession: biome field gates
the fire clock locally — clock survives in its phase), or (b) PHASE-ONLY
(sync: mode-locking preserves both counters exactly). Hierarchy DISSOLVES when the
new layer injects spatial VARIANCE into oscillator parameters (ecoevo: sd(G)>~0.06
detunes local cycles, global clock decoheres) and is DRIFT-LIMITED when the
effective population of social units is small (cheaters: N_e~15 mounds at 64^2).
=> Design rule for tall towers: couple upward through means/phases, not through
per-unit parameter spread; keep the "social unit" count large or the top layer
goes stochastic.

## Yield accounting (for the scaling question)
- Round 1: 5/5 certified (after audit corrections: 0 retractions, 2 sharpenings).
- Round 2: 2 full stacking passes (succession, sync-tongue) + 2 certified
  mapped-negatives/regimes (ecoevo law, cheaters regime map) = 4/4 deliverable
  yield; 2/4 "clean 4-layer tower" yield. Cost ~1 day wall-clock, 5 children,
  ~500 sim runs. Audit layer: caught 1 boundary confound + 1 audit-side
  convention artifact; both loops closed same-day.
