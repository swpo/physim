# IDEAS.md — deferred/parked ideas (scratchpad, not commitments)

## E-track (deferred until E1 observed)
- E1-c: sigmoid/canalized GP map variant (cryptic variation, punctuated change;
  cross-level map datapoint #2)
- E2: wave-regime-dependent selection (evolution x ecowave)
- E3: biogeography (islands/corridors, founder effects, local adaptation)
- E4: multi-locus epistatic genomes, boolean/tree GP maps, recombination on
  tissue merge; rugged fitness landscapes
- Additional measurable-complexity axes: trophic layer (predator/pathogen
  field), multi-modal founder diversity, multiple partially-informative
  phenotype stains
- Aggregate-map tracking: measure effective macro GP map shape per rung
  (micro-linear -> macro-saturating found at E0; test inversions at E1-c)

## Other tracks (parked)
- C-track: tracking-grade apparatus (2-axis stages, closed-loop microscopy
  preps on drifting worlds = C3-era idea); species-resolving contracts;
  GS-aware + wave-aware scripted scientists as certifier upgrades
- B-track: migration/refugia geography contracts; population-resolving
  contracts
- Port mixtures: ports coupling to two (field, mode) targets at once
  ("warms and stirs") as a difficulty dial
- Observability-without-controllability worlds (unreachable fields) as an
  explicitly labeled variant — off standard tracks per v0.13 addendum 5
- Iterated rollouts / research programs across episodes (persistent notebook)
  as a separate future track (rejected for base benchmark)
- Effort/conduct: score-vs-ticks sample-efficiency curves as headline metric
- Infra: HF gallery pagination; retro-oracles for C2/C3; n>=5 stats on hard
  tier; Environments Hub publication; RL training experiments on the
  decomposition curricula


## Parameter-search world screening (user, 2026-02-16) — "anthropic-ish" design

Instead of hand-picking emergent-economics constants (c_max, m0, m1, cap,
storm depth...), run trials over many parameterizations and keep the ones
that yield interesting higher-level phenomena, with the certification battery
(regime flips / bimodality / selection displacement / adequacy ratios) as the
objective function. We accept that we only ever ship worlds that pass the
screen — document the screen as part of the benchmark's design provenance.
Natural pairing: v0.14 enzyme economics (few linear prices, emergent regime
diagrams) + this screen = scalable world search. Related: IDEAS "automated
world search" thread.


## Winner-flip worlds (B3 v2 candidates, parked 2026-02-16)

The ecowave2 probe showed rain-richness produces competitive exclusion, not
selection flips, under kill-rate trade-offs; and FHN anode-break inversion
makes "poison = famine" false in wave-fed worlds. Candidate fixes for a real
selection-by-weather world: (a) birth-rate trade-off (fast-breeder wins rich
CONSTANT rain; stress-tolerator wins intermittent rain — r/K selection
proper), needs per-variant growth-rate laws, not just death rates; (b) rain
shadows: pacemaker geometry creates permanently dry refugia where only the
frugal variant persists — winner becomes a GEOGRAPHY question; (c) driven
Turing switch: wave frequency sets which variant's preferred resource band
is replenished. All need probe campaigns before engine work.

- BLOBS: re-engineer a large CONTINUUM species (A-class) — current A is lattice-stabilized at dx=1, labyrinths at dx=0.5; needed only if a machine wants the 6.8x size contrast (sorting sieves, big-anchor designs). Candidate route: move along iso-line toward deeper k1 with higher Du, or curvature-stabilized annulus species.

- BLOBS phase-2 (user): labyrinth instability as FEATURE — a labyrinth-prone species coupled to dynamical b (deposition/relaxation) as a route to growth/vasculature/territorial phenomenology; 'living systems and space-filling curves'. Revisit after M6 (b-field) characterizes the forward map.

- BLOBS L0 "equation-space search" (user, 2026-02-19 — parallel track, not replacing design):
  GENOTYPE: dF/dt = D lap F + M(F) with D diagonal, M = linear part L(F-F0) + bounded
  compositions (tanh-saturated terms); our whole zoo is points in this space (M0=3x3,
  vvw=5x5, xv=6x6, bfield=4x4 with one tanh edge). Constraints as viability prior:
  exact uniform vacuum (iso-line trick generalizes: keep F0 a root for all couplings),
  bounded sources, sane stiffness (IMEX-compatible).
  PHENOTYPE SCORES: reuse certified gate metrics as the assay battery (seconds-minutes
  each): vacuum dispersion class (microseconds, linear algebra — demo'd: distinguishes
  Turing-unstable soup from stable-vacuum blob worlds and detects oscillatory tails),
  seeded-poke response (die/persist/replicate/travel), pair response (bond/repel/merge
  + d*), periodicity, multistability, trail memory. NOTE subcriticality: blobs invisible
  to vacuum linear analysis — seeded probes are mandatory; linear spectrum is only G0.
  SEARCH: MAP-Elites quality-diversity over behavior descriptors (n_objects, motility
  class, bond count, period) rather than scalar "interestingness" (Goodhart defense;
  novelty niches preserved). Merge/crossover has a NATIVE meaning our history already
  used by hand: block composition (vvw = two M0 blocks sharing w; xv = two M4 blocks +
  one cross edge) — graft species blocks, share/split mediator channels, add one
  off-diagonal edge at a time. Mutation = dial jitter on theory coordinates.
  EIGEN-ANALYSIS: dispersion matrix M(k)=J-k^2 D per candidate = cheap fingerprint
  (max Re lambda(k), k*, oscillatory?, # sign-changing mediator channels a la v-vs-w).
  USES: (1) rapid L0 exploration feeding L1+ certification; (2) uniform genome format
  to compare/diff agent-produced worlds across sessions; (3) screening provenance
  doctrine already exists (E2 anthropic-screening precedent).
  STATUS: parked pending user green-light for a pilot searcher (L0-sampler: random +
  elite-archive over the constrained genotype space, yield curves per behavior cell).

- BLOBS L0 search SHARPENED G0 SCREENS (2026-02-19, from spatial-dynamics analysis):
  blob existence is subcritical (invisible to temporal vacuum linearization) BUT the
  STEADY-STATE equations read as spatial dynamics give algebraic screens in microseconds:
  (G0a) temporal dispersion max Re lambda(k) < 0 — vacuum stable (else Turing soup);
  (G0b) reaction cubic has the upper branch (bistable local structure — root count);
  (G0c) SPATIAL eigenvalues of vacuum (modes e^{mu x} of the steady ODE system):
        complex mu = oscillatory tails = binding shells; computed for our worlds:
        wavelength 10.8-10.9 px vs MEASURED M4 shell spacing 10.9 px (1% match);
        statics depend on tau,Dv only via A=tau*Dv — ANALYTIC in this formalism
        (steady v-eq: v'' = (v-u)/(tau*Dv); the M4 searcher's empirical law is one line).
  Then ONE nonlinear seeded-poke probe confirms existence (homoclinic orbit — a global/
  topological object: no local criterion can fully replace the probe; snaking-region
  theory says families of localized states exist where G0a-c hold near onset).
- BLOBS grounding target: AMAZON FULFILLMENT CENTER world (user, 2026-02-19) — conveyor
  network with forks/merges, control arms, sorters. Inventory already certified: track
  (saw), rails, blocking walls, pickup coupler, parking brake (pair-only zone), ROTOR
  (=roller: seeds motion locally where nothing translates — rotor-only zone!), species-
  selective coupling (sorter). Missing: unload/release, fork/merge switchyards,
  roller->cargo momentum transfer (CONCRETE NEXT PROBE: park B cargo beside a spinning
  heterodimer; measure tangential advection through w/b channels). Too hard in one shot;
  north-star for L3 composition + the L0 evolutionary search's behavior descriptors.
- BLOBS L0 compute: parallelize assay battery on rented Prime compute (prime CLI pods;
  per-candidate assays are independent — embarrassingly parallel).
