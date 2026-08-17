# SLIME LIFECYCLE — starvation-triggered multicellularity (Dictyostelium-style)

## Verdict
**PASS on all five gates.** Best candidate **c30**: a 3-layer hierarchy
(relay waves -> chemotactic aggregation -> feast/famine lifecycle) whose top
law is a near-perfect square-wave oscillator (switch fit r2 = 0.996, 27
flips in 40k ticks) with period set analytically by the resource regen rate.
Robust 8/8 (4 seeds + 4 full-jitter runs), fast (40k ticks ~ 26 s), and
visually cinematic (pulsing target waves -> mound coarsening -> synchronized
dispersal bloom).

## Mechanism (all computed by micro physics; no scripted events)
Fields on a 64x64 torus:
- `R` resource: regrows `rho*(1-R)`, diffuses (Dr=0.2), grazed by fed cells.
- `V` cell density: conservative advection + diffusion (mass-exact).
- `S` fast attractant: excitable relay — hungry cells fire when S > thr
  (refractory T_r), emitting a pulse; spontaneous pacemakers at rate p_spont*V.
- `A` slow pheromone: leaky integral of relay firing; chemotaxis target.
Cell state machine (per-cell hysteresis + commitment timers):
- FED (grazing): eats R, slow diffusion. When local R < R_star -> HUNGRY.
- HUNGRY (developing): stops eating, relays S waves, chemotaxes up grad(A),
  gains density protection (death d0*(1-pd*C), C = crowding). A famine-onset
  S wave also recruits marginal cells (R < R_join) — synchronizer.
- When R regrows above R_wake -> GERMINATING for T_wake ticks: disperses
  (fast diffusion + drift DOWN grad A), does not eat until settled.

The lifecycle: grazing crashes R everywhere (feast, ~800 ticks) -> famine
wave sweeps the lattice; relay waves ignite around pacemakers (L1) -> cells
stream up the wave-marked gradients into ~15 dormant mounds (L2, coarsening)
-> lawn regrows under the sleeping mounds for ~1100 ticks -> R crosses
R_wake, mounds erupt outward as germinating dispersers, remix, and the feast
restarts (L3). Aggregated fraction `aggm` and hungry fraction `hf` trace a
clean square wave.

## Hierarchy (layer -> variable -> timescale) — c30, 40k-tick certification
| layer | variable | timescale | separation |
|---|---|---|---|
| L1 relay waves | fires/tick rhythm; S rings, speed 0.63 cells/tick | period 26 (q=0.88, 17 windows) | — |
| L2 aggregation | aggm 10-90% rise; cluster count decay tau=418 | rise 220 | L2/L1 = 8.5 |
| L3 lifecycle | aggm / hf square wave | period 2320 (ACF q=0.91, 13.7 cyc) | L3/L2 = 10.6 |
Separation product ≈ 89. Micro tick -> top law: 3 decades.

## Best candidate c30 (theory coords -> raw)
T_fam=1856 (rho=3.61e-4), dose=1.97 (d0=1.06e-3), pd=0.933, chi_a=13.1,
g=0.0478, T_r=24, p_spont=7.4e-4, R_star=0.12, R_wake=0.55 (defaults for the
rest; see slime.py DEFAULTS + best_c30.json).

## Gates
- **G1 PASS**: 3 layers, sep 8.5x and 10.6x (>=5x), each measurable
  (fires(t), aggm/ncl, aggm/hf). Wave propagation verified (front tracking:
  0.63 cells/tick; target-wave strips).
- **G2 PASS**: top fit on hf: switch r2=0.9965, 27 flips (>=6). aggm: 0.963.
  ACF confirms oscillation: period 2320, q=0.91, 13.7 cycles.
- **G3 PASS**: period vs 1/rho (5 values, only rho varied):
  | 1/rho | 2767 | 3690 | 5534 | 8300 | 12450 |
  |---|---|---|---|---|---|
  | period | 1260 | 1700 | 2320 | 2960 | 4260 |
  Monotone, smooth: period = 0.695/rho + 405, R2=0.9999. The slope matches
  the ANALYTIC famine length ln((1-R_star)/(1-R_wake)) = 0.671 to 3.7%; the
  405-tick offset is the measured feast+dispersal time. The clock is
  computed, not imposed: nothing in the code contains a period.
  (Second price: g barely moves the period, 2400->2300 for 4.5x g — feast
  length saturates; reported honestly, not counted for G3.)
- **G4 PASS**: 4/4 seeds and 4/4 jitter runs (all 8 searched params
  simultaneously jittered ±10%, fresh seeds) pass G1+G2. 60k-tick seed-5 run:
  26 cycles, same period, r2=0.963.
- **G5 PASS**: L=64; cycle = 2320 ticks (26 cycles in 60k); 40k-tick probe =
  21-27 s single core (60k = 31 s).

## Sweep summary (results.json has every run)
36-candidate theory-coordinate sweep + 8 re-gates + 24 G4 runs + 15 G3 runs
+ 4 controls + 5 tuning probes = 92 logged runs.
- Survivable window: T_fam 1300-3000 with dose 1-5. T_fam >= 4000 fails at
  fixed dose-rate (famines too long -> lawn dies before wake; 0/11 G2 at
  T_fam>=4000 in-sweep — G3 curve passes because dose was held constant).
- dose >= 6.8: extinction (3/36). dose <= 2 with pd=0.97: no aggregation
  need — but c30 shows dose ~2 with pd 0.93 works; boundary is soft.
- High chi_a (>=16) + high p_spont: many small mounds -> sep12 collapses
  (fragmented relay domains fire asynchronously; 6 candidates failed G1 this
  way, e.g. c05/c07/c32 seeds vary).
- 4/36 sweep candidates pass G1+G2 outright (c00, c06, c27, c30); c30 is the
  only one robust 8/8 (c27: 6/8; c00: 1/8 — sits on the fragmentation edge).

## Negative results / honest caveats
- **Mass-conservation bug** (v14): advection+diffusion in a single update
  overdrew cells; clipping V>=0 created mass (V grew 40x in 1k ticks). Fixed
  with sequential conservative updates; now exact to machine precision.
  Any engine port MUST keep the outflow-limited upwind scheme.
- **Frozen-tower trap** (v3-v13): without the germination-dispersal phase
  (commitment timer + drift down grad A + no eating until settled), woken
  mounds instantly re-starve in their own grazed halo and the world freezes
  into permanent towers + dead lawn. This is the load-bearing mechanism.
- Cluster sizes span only 0.96 decades — NOT a power law; no criticality
  claimed. L2 has ordinary coarsening, not broadband structure.
- The lifecycle needs the relay+chemotaxis to SURVIVE, not to oscillate:
  with chi_a=0 or a_s=0 the R-H relaxation cycle persists at V ~ 0.002
  (near-extinct, aggm_range 0.02, no L2 layer). Protection off (pd=0) same.
  So L3 amplitude & viability are emergent from L1+L2, but a bare (spatially
  trivial) feast/famine relaxation is latent in the R-dynamics — the honest
  claim is "lifecycle rescued and spatially organized by multicellularity",
  not "oscillation impossible without it".
- hf (hungry fraction) is arguably a *forcing-adjacent* variable; that is
  why aggm (aggregated dormant biomass fraction, a genuinely spatial L2->L3
  variable) is certified too: switch r2=0.963 standalone.
- S mean-field: relay works in the tested T_r=16-24, p_spont 3e-4..1e-3
  band; outside it, waves fragment (seen in sweep failures).

## Engine-integration sketch
World fields: R, V, S, A (4 float grids) + per-cell ints E, Q, Wd, Ww + bool
H. Params: the 24 DEFAULTS keys. Update order per tick: hunger switch (with
S-recruitment) -> relay fire/decay (2 S-substeps) -> A integrate -> move V
(upwind advect on grad A + var-diffusion, sequential) -> crowding -> eat/
grow/die -> R regen+diffuse. Cost: ~30 ms per 1k ticks at 64^2 in numpy.
Real-world analogue: Dictyostelium discoideum aggregation lifecycle (cAMP
relay waves, slug/fruiting protection, spore dispersal) — named honestly.

## Files
slime.py (engine), measure.py (layer metrics), sweep.py, g3_response.py,
g3_pure.py, g4_robust.py, probe_*.py, best_c30.json, results.json,
strips/ (best_c30_[VRSA], waves_[SV]_zoom, cycle_[VRS], sanity*).
