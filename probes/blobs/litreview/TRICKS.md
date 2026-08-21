# TRICKS.md — concrete techniques worth importing
Each: WHAT → WHERE FROM → HOW IT PLUGS INTO OUR STACK.

## Numerics & continuation
1. **Numerical continuation of localized states + fold tracking (pde2path / AUTO).**
   Uecker, Wetzel, Rademacher, NMTMA 7:58 (2014); Knobloch's group practice.
   → Replace bisection hunts for tau_c, k1 windows, and d* with Newton continuation
   of the steady/traveling blob in (tau, Dv, k1): get the WHOLE branch + folds +
   drift onset in one run. Biggest single upgrade to l0 stage-2 ("adaptive tau
   ladder" becomes a continuation run); also converts our corridor maps into
   certified bifurcation diagrams.
2. **Freezing method / template matching for traveling & rotating waves**
   (Beyn & Thümmler, "Freezing Solutions of Equivariant Evolution Equations", SIADS 3:85 (2004); also Beyn, Selle, Thümmler SIADS 7:577 (2008) for multipulses). → Solve in the co-moving/co-rotating frame
   with c (or ω) as an unknown: measures speed to machine precision, removes
   domain-length limits on longruns, and turns our rotor ω(tau1) curve into an
   eigenvalue-clean branch. Perfect for pair-only-zone boundaries (solve pair and
   single branches, compare fold locations exactly).
3. **Absolute/essential spectrum computation by continuation** (Rademacher,
   Sandstede, Scheel, Physica D 229:166 (2007)). → Certify blob/bond/rotor
   stability spectra instead of longrun-survival gates; distinguishes convective
   vs absolute instability (relevant to wake-locked tandems).
4. **Exponential time differencing (ETDRK4) with FFT** (Kassam & Trefethen, SISC
   26:1214 (2005)). → Drop-in upgrade over IMEX-Euler for stiff linear parts
   (high Dw, D_b): larger dt at same accuracy; cheap because our nonlinearity is
   pointwise cubic. Worth benchmarking vs current IMEX-FFT at B7 budget.
5. **Peierls–Nabarro barrier diagnostics** (discrete-soliton literature). → Our
   lattice-pinning trap has a quantitative observable: the PN energy barrier vs dx.
   Fit E_PN(dx) once; then "continuum-clean" gets a number, not a dx-halving ritual
   (keep the ritual as the gate, use E_PN as the early warning).

## Model reduction & theory
6. **Order-parameter / particle reduction of DS dynamics** (Bode et al, Physica D
   161:45 (2002); Gurevich; Ei-Mimura-Nagayama Physica D 165:176 (2002); Ohta).
   → Derive the 2-3 ODEs per blob (position + propagator amplitude) at our working
   points: gives analytic c(tau), F(d), and — key — predicts machine behavior
   (train speed vs length, power ceiling) without PDE runs. The literature has
   the recipe; our stack has the operating points. This is the cheapest route to
   a "max-train-length law" (open item).
7. **Tail-interference bound-state rule** (Buryak & Akhmediev PRE 51:3572;
   Gorshkov-Ostrovsky). → Analytic d* ladder: d*_n ≈ (phase offset + n·π)/k_im
   with alternating stability. Use as l0 assay: predicted vs measured d* is a
   1-number chemistry certificate (we already do this — cite it, and use their
   saddle-alternation to auto-flag pinning artifacts: a "stable" state at a
   predicted SADDLE distance = lattice artifact detector).
8. **Beyond-all-orders pinning-width scaling** (Kozyreff & Chapman PRL 97:044502).
   → Predicts how binding windows shrink near onset: exp(-C/amp). Explains why
   near-fold worlds (our funnel favorites) have wide basins; use as prior on
   jitter step size per fold-distance.
9. **Nonreciprocity framework** (Ivlev PRX 5:011035; Fruchart Nature 592:363).
   → Express eta12/eta21 as reciprocal+nonreciprocal parts; the rotor is the
   nonreciprocal part's chiral phase. Predicts: tuning eta21/eta12 through -1
   should give exceptional-point-style transitions (rotor ↔ oscillating bond) —
   a concrete M7-extension experiment.
10. **Scattor analysis of collisions** (Nishiura et al, Chaos 13:962 (2003)).
    → For encounter tables: find the unstable saddle between merge/repel outcomes
    (edge tracking / bisection on initial separation). Gives basin boundaries +
    explains outcome flips; directly reusable for gate design (collision logic).

## Stochastics & measurement
11. **Kramers–Moyal drift reconstruction from noisy tracks** (Bödeker et al PRE
    67:056220; Friedrich-Peinke school; Liehr book ch. 4). → Extract deterministic
    drift law c(x) + noise amplitude from ONE noisy trajectory: certifies our
    sub-threshold-creep story, measures the drift bifurcation under noise (their
    exact use case), and gives F(d) from bond-length fluctuation data (their NJP
    6:62 method) — cheaper than our escape-time censoring.
12. **Interaction-law reconstruction from pair trajectories** (Bödeker NJP 6:62).
    → Fit dd/dt = F(d)+noise on wandering-pair data: turns every longrun into a
    bond-curve measurement for free.
13. **Input-entropy / compression filters for interestingness** (Wuensche 2002;
    Lenia-lit compression metrics; ASAL FM-embeddings arXiv:2412.17799).
    → l0 assay upgrade: cheap information-theoretic novelty channel (zlib ratio of
    field snapshots, or CLIP embedding drift) appended to archive descriptors;
    catches qualitatively-new dynamics our hand assays alias.

## Search
14. **IMGEP / goal-space exploration** (Reinke et al ICLR 2020 arXiv:1908.06663).
    → For l0-evolver: sample a GOAL in behavior space (e.g. target d*/wl, target
    c, target ω), pick nearest archive elite, jitter toward goal. Finds behavior-
    space holes uniform/jitter never target. Drop-in on top of existing archive.
15. **MAP-Elites curiosity/success bookkeeping** (Cully et al; QD practice).
    → Track per-elite offspring-success; allocate jitter budget by curiosity
    score. Formalizes "jitter maps islands 25x faster" into an adaptive scheduler.
16. **POET-style transfer gate** (Wang et al arXiv:1901.01753). → For the MERGE
    milestone: a grown landscape counts only if machines evolved WITH it beat
    machines transplanted INTO it (and vice versa) — their transfer test is the
    right currency for "landscape helps".
17. **Differentiable-simulator inverse design** (Mordvintsev et al
    arXiv:2107.06862, arXiv:2302.02714). → b_target inverse problem: our IMEX/FFT
    step is differentiable (linear solve + pointwise cubic); JAX port of the
    b-forward map + gradient descent on ||b_final - b_target||² is exactly their
    demonstrated pipeline. Also usable to design isok landscapes that produce a
    desired F(x) force field.
18. **FM/CLIP scoring of films** (ASAL arXiv:2412.17799). → Zero-physics-cost
    open-endedness metric for pod fan-out triage: embed strips, keep candidates
    whose embedding trajectory keeps moving. (Their "open-endedness search".)

## Assays & certification
19. **Robustness curricula from ALife** (Hamon et al Sci. Adv. 2025: obstacle
    randomization; NCA damage/regeneration tests). → Machine certification
    upgrades: mid-haul train bisection, moving walls, track amputation (we saw
    self-healing once — make it a gate), cargo swap mid-run.
20. **Curie-symmetry audit for any transport claim** (Reimann Phys. Rep. 361:57).
    → Standing checklist item: for every net-displacement result, name the broken
    symmetry that permits it (our saw asymmetry, wake asymmetry, nonreciprocity,
    IC asymmetry). Anything transporting WITHOUT an identifiable broken symmetry
    is a bug (mass-creation trap class). Cheap and catches artifacts early.
