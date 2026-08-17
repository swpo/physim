# FIRE FOREST — world-search summary (2026-02-17)

## Verdict
**PASS on all gates G1–G5.** Best candidate **W7**; runner-up W6 (identical family,
sparser sparks). 70 candidates logged in `results.json` (including failures).

## Mechanism (ff_core.py v3 — continuous fields, torus, dt = 1 tick)
- **Fuel B ∈ [0.01, 1]** — slow: `dB = g_i (rho + B)(1−B) − eta·F·B`, static
  site-quality map `g_i = g·exp(U(−gsig, gsig))`.
- **Fire F ∈ [0, 1]** — fast excitable: `dF = beta·<F>_nn·sig(B)(1−F) − delta·F`,
  flammability gate `sig(B) = logistic((B−theta)/w)`, **quench** F<0.02 → 0.
- **Lightning** — Poisson sparks (rate f per site·tick) set `F = 0.9·sig(B)`:
  sparks only take hold on mature fuel. External climate drive (like E1), not
  a counted layer.
- No agent coupling, no scripted macro events. The fire-return clock is
  COMPUTED: it is the time for the fuel field to regrow through the
  percolation/ignition threshold after each burn.

## Hierarchy (layer → variable → timescale, W7 numbers, L=64)
| layer | variable | timescale | separation |
|---|---|---|---|
| L1 fire front | cell hot-residence (F>0.1) | tau1 ≈ 2 ticks | — |
| L2 fire events | burn clusters: size, duration | tau2 ≈ 85–90 ticks | sep21 ≈ 38–48× |
| L3 fuel cycle (TOP) | phi = frac(B>theta) mature cover | tau3 ≈ 1425–1751 ticks | sep32 ≈ 16–21× |

Top law: **switch** (two-state relaxation oscillator on phi): burn-flat ↔
regrown-flat, r2 = 0.86–0.90, 30+ flips per 60k-tick run. The S-shaped
regrowth (seed-rain rho kills the low-B crawl) is what makes the top law
compact — pure logistic regrowth from the floor gives a crawling sawtooth
that no simple model fits (v2 failures, r2 ≈ 0.65–0.75).

## Best candidate W7 (theory coords)
theta=0.78, Lam=9 (sparks per regrow time per field; f_abs=3.05e-6/site/tick),
M=2 (spread margin beta/4delta), D=8 (burn depth eta/delta), gsig=0.35,
rho=0.03, g=2e-3, delta=0.2, w=0.05, L=64, T=60k, drop 10k, coarse=50.

## Gates
- **G1 PASS** 3 layers, adjacent separations 38–48× and 16–21× (≥5 required),
  83–102 events/run.
- **G2 PASS** switch top on phi, r2 = 0.860–0.895 (4 seeds), n_flips 30–60.
- **G3 PASS** response curve tau3 vs g with ABSOLUTE spark rate fixed
  (6 values × 3 seeds, medians): g=1e-3→2202, 1.4e-3→1948, 2e-3→1467,
  2.8e-3→1127, 4e-3→947, 5.6e-3→765. Monotone, smooth, tau3 ~ g^−0.64
  (sublinear because the spark-wait share of the cycle shrinks as regrowth
  speeds up). Same monotonicity holds for the W1 family (g^−0.53).
- **G4 PASS** W7: 4/4 seeds, 3/3 ±10%-jitter draws (all searched params
  jittered). W6: 4/4 + 3/3. W1–W4: 4/4 + 3/3. W5: 4/4 + 2/3.
- **G5 PASS** 6.3–7.5 s per 60k-tick L=64 run (single core) — well under 3 min;
  full cycle visible in ≤ 2k ticks.

## Ranking extras
- Intermediate-layer statistics: pooled event sizes (6 seeds, W1) span
  **~3.1 decades**, MLE alpha ≈ 1.2, but the rank plot shows a clear
  spanning-event bump at s = L² = 4096. **Honest reading: broadband, NOT
  certified SOC** — the classic DS-FFM double separation (theta→1 with
  Lam→0 simultaneously) is outside our G2 window: those regions (v2-A,
  sweep1 ids 8–9) give perfect sawtooths but too few events and worse r2.
- Visual drama: expanding ring fronts that collide and annihilate
  (strips/W7_L1_fire_front.png), whole-field green-up/burn-down cycle
  (strips/W7_L3_fuel_cycle.png, macro_layers.png).
- Real-world analogue: Drossel–Schwabl forest-fire model / chaparral
  fire-return intervals — honest: our regime is the "fire-cycle" (percolation
  oscillator) regime, not the SOC limit.

## Negative results (deliverables)
1. **No-quench smouldering death (v1):** without `F<0.02→0`, fire never goes
   extinct; the world settles into a homogeneous smouldering equilibrium with
   flat meanB — 0 events. The quench floor is essential for event structure.
2. **Pure-logistic crawl (v2, sweep1 group A2):** with rho=0, regrowth from
   the burn floor is exponentially slow at first; the macro wave becomes an
   asymmetric sawtooth that neither oscillator nor switch fits (r2 ≤ 0.81).
   Seed-rain rho ≈ 0.03 squares up the waveform (r2 → 0.86–0.93).
3. **Spark-rich SOC corner kills the top law:** Lam ≥ 15 (ids 202–205,
   sweep1 group B): sizes broaden (3+ decades) but phi never rebuilds
   coherently — r2 drops to 0.65–0.81. Trade-off between L2 breadth and L3
   law; Lam ≈ 6–9 is the compromise window.
4. **Rare-spark corner starves G1:** Lam ≤ 0.7 (ids 8–9): beautiful global
   relaxation oscillator (r2 0.89–0.95) but < 12 events / 50k ticks — layer 2
   is statistically empty on budget. G5 forces the middle.
5. **High spread margin M hurts:** M=3→5 raises tau1 (longer smoulder at
   fronts) and lowers r2 slightly; M=2 (just above the propagation margin)
   gives the sharpest scale separation (sep21 ≈ 40).
6. **Spiral regime not found (group D):** low theta + shallow burn (D=2) does
   not sustain rotating fire ecology at L=64 — waves either die or become
   system-wide flashes with 7 events / 30k ticks. Not pursued (budget).

## Engine-integration sketch
Two World fields: `fuel` (B) and `fire` (F). Per-tick kernel: 4-neighbor
mean of F (existing diffusion stencil works), logistic map for sig(B),
multiplicative growth update for B, Poisson point-ignitions (rng already in
engine), clamp + quench. Params: g, rho, gsig (static per-cell map), theta,
w, beta, delta, eta, f, Fq. Macro observables: mean(B), frac(B>theta),
sum(F>0.1) per tick. All O(L²) numpy ops, ~9 µs/tick at L=64 in the probe.

## Files
- `ff_core.py` (model+metrics), `sweep1/2/3.py`, `gate_runs.py`, `gate2.py`,
  `g3_curve*.py`, `make_strips.py`, `strips_w7.py`, `g3_plot.py`
- `results.json` (70 candidates incl. failures, 7 gate-certified families,
  both G3 curves, pooled size stats)
- `strips/`: W7_L1_fire_front, W7_L3_fuel_cycle, W7_macro_layers,
  G3_response_curve, + W1 equivalents, sanity strips
