# BLOBS literature review
2026-02-20/21, lit-reviewer agent. Sources logged in `sources.jsonl`.
Compared against: `docs/blobs.html` + `probes/blobs/PROGRAM.md` (M0-M7, L0-L3, genesis, machine).

Verdict vocabulary used below:
- **already-known**: the phenomenon/law exists in the literature in essentially our form.
- **novel-combination**: pieces exist separately; our assembly/quantification appears new.
- **new-as-far-as-found**: nothing found after honest search (bounded confidence — a few
  hours of API search, no library access to full texts).

---

## A. Dissipative solitons in 2/3-component reaction-diffusion systems

**Our model IS the literature's model.** The equations in `blobs.html` §1 are, symbol for
symbol, the three-component activator/two-inhibitor system introduced by the Münster
group (Purwins school) to model planar dc gas discharges. They call the localized objects
*dissipative solitons* (older Soviet literature: *autosolitons*). Everything in our M0-M2
ladder has a named ancestor here; our quantitative laws are house-made but the phenomena
are canonical.

### Key references

1. **Schenk, Or-Guil, Bode, Purwins (1997)** "Interacting Pulses in Three-Component
   Reaction-Diffusion Systems on Two-Dimensional Domains", *PRL* 78:3781.
   [doi:10.1103/PhysRevLett.78.3781] — The origin of our exact equations (u,v,w with
   tau, theta, Du, Dv, Dw, kappa couplings). Shows stationary & traveling spots and
   spot molecules in 2D. Our M0 is their Fig. 1.
2. **Or-Guil, Bode, Schenk, Purwins (1998)** "Spot bifurcations in three-component
   reaction-diffusion systems: The onset of propagation", *PRE* 57:6432. — Drift
   (propagation-onset) bifurcation theory for these spots: the slow inhibitor's
   time constant tau is the drift dial; velocity grows as sqrt(tau - tau_c). Our
   M1 law c = sqrt(0.0299(tau-4.78)) is this normal form with fitted constants.
3. **Krischer, Mikhailov (1994)** "Bifurcation to Traveling Spots in Reaction-Diffusion
   Systems", *PRL* 73:3165. — Earlier drift bifurcation of spots (2-comp + global
   coupling); the c ∝ sqrt(ε) supercritical pitchfork for spot velocity.
4. **Bode, Liehr, Schenk, Purwins (2002)** "Interaction of dissipative solitons:
   particle-like behaviour of localized structures in a three-component
   reaction-diffusion system", *Physica D* 161:45. — THE reference for our whole
   program: derives reduced particle ODEs (position + amplitude of propagator mode)
   for many-blob dynamics; scattering, molecule formation, generation, annihilation.
   Their reduction is the formal version of our measured F(d) bond curves.
5. **Liehr (2013)** *Dissipative Solitons in Reaction Diffusion Systems* (Springer
   Series in Synergetics 70). — Book-length treatment of exactly our system:
   existence, drift bifurcation, interaction, molecules, rotation, generation,
   annihilation, plus the stochastic data-analysis methods.
6. **Purwins, Bödeker, Amiranashvili (2010)** "Dissipative solitons", *Advances in
   Physics* 59:485. [doi:10.1080/00018732.2010.498228] — The definitive review;
   taxonomy of DS behaviors across gas discharge, semiconductors, optics, chemistry.
7. **Purwins, Stollenwerk (2014)** "Synergetic aspects of gas-discharge: lateral
   patterns in dc systems with a high ohmic barrier", *PPCF* 56:123001. — Modern
   experimental review (the physical blobs: current filaments).
8. **Astrov, Purwins (2001)** "Plasma spots in a gas discharge system: birth,
   scattering and formation of molecules", *Phys. Lett. A* 283:349. — Experimental
   blob molecules at discrete separations.
9. **Bödeker, Röttger, Liehr, Frank, Friedrich, Purwins (2003)** "Noise-covered drift
   bifurcation of dissipative solitons in a planar gas-discharge system", *PRE*
   67:056220. — Drift bifurcation detection UNDER NOISE by stochastic data analysis
   (Kramers-Moyal reconstruction of the deterministic drift from noisy tracks).
   Directly relevant to our M6 "sub-threshold creep under noise" caveat.
10. **Bödeker, Liehr, Frank, Friedrich, Purwins (2004)** "Measuring the interaction
    law of dissipative solitons", *New J. Phys.* 6:62 (2004). — Experimental
    reconstruction of the blob-blob force law F(d) from tracking data: oscillatory,
    with discrete equilibria. Our M2 bond-curve protocol is the simulation twin.
11. **Moskalenko, Liehr, Purwins (2003)** "Rotational bifurcation of localized
    dissipative structures", *EPL* 63:361. [doi:10.1209/epl/i2003-00532-1] —
    **A stationary bound pair of dissipative solitons spontaneously starts to
    ROTATE; the rotation bifurcation can PRECEDE the drift bifurcation.** In the
    same 3-component system. This is the same-species version of our M7 headline
    (rotation as attractor, rotor-only zone below single/pair drift onset).
12. **Liehr, Moskalenko, Astrov, Bode, Purwins (2004)** "Rotating bound states of
    dissipative solitons in systems of reaction-diffusion type", *EPJ B* 37:199. —
    Numerical + experimental rotating molecules (gas discharge).
13. **Gurevich, Amiranashvili, Purwins (2006)** "Breathing dissipative solitons in
    three-component RD system", *PRE* 74:066201. — Breathing (radial-oscillation)
    mode; cf. our metastable "breathing dimer" honest negative.
14. **Nishiura, Teramoto, Ueda (2003)** "Scattering and separators in dissipative
    systems", *PRE* 67:056210; and (2005) "Scattering of traveling spots in
    dissipative systems", *Chaos* 15:047509. — Collision outcomes (merge, repel,
    annihilate) organized by unstable saddle solutions ("scattors") whose stable
    manifolds separate outcome basins. Explains why our encounter tables are sharp.
15. **Kerner, Osipov (1994)** *Autosolitons* (Kluwer). — The Soviet-school book;
    "autosoliton" taxonomy: static, traveling, pulsating; splitting and spike
    solutions. Prior art for nearly every qualitative blob behavior.

### STEAL / COMPARE (Area A)

- **M0 existence — already-known.** Stationary stable spot in this exact system:
  Schenk et al. 1997. Our contribution is only the audited parameter bookkeeping.
- **M1 drift bifurcation + sqrt law — already-known** (Or-Guil 1998; Krischer &
  Mikhailov 1994; Bode et al. 2002 derive it). Purwins school also measured it in
  experiment (Gurevich 2004, "due to change of shape"). Our IMEX-FFT unpinning
  check is good practice the sim literature also worries about (see TRICKS).
- **M2 discrete bond distances via oscillatory v-tails — already-known.**
  Bode et al. 2002 §5 and Bödeker 2004 measure exactly this F(d) with discrete
  zeros; Buryak & Akhmediev 1995 give the general tail-interference stability
  rule (alternating stable/unstable separations — predicts our d1*, d2* ladder
  AND why saddles sit between shells). Our two-sided convergence protocol +
  dx-refinement discipline is a solid reproduction with better honesty about
  lattice pinning (the literature's simulations rarely report pinning checks).
- **M2 molecules (3-chain, triangle) — already-known** (Schenk 1997 shows
  molecules; Astrov & Purwins 2001 experimental clusters; Liehr book chapter 5).
- **M4 traveling bond, pair bifurcation at tau_c < single — PARTLY known.**
  Traveling molecules exist in the literature (Liehr's "intergradient" simulations,
  Bode 2002 show co-propagating pairs). We did not find a published statement of
  a **pair-only drift zone** (molecule drifts at tau where the single blob is
  static, tau_c^pair = 5.636 < tau_c^single = 5.748) for translation. The CLOSEST
  published fact is Moskalenko/Liehr 2003: the ROTATION bifurcation of a pair can
  precede the drift bifurcation — same physics (composite soft mode goes unstable
  before single-blob propagator mode), different symmetry channel. A second
  precedent from optics: in the quintic complex Ginzburg-Landau equation the
  π/2-phase-difference soliton PAIR moves at constant velocity while the single
  soliton is stationary (Afanasjev, Akhmediev, Soto-Crespo 1996, PRE 53:1931) —
  there the composite motion comes from broken pair symmetry, not a shifted
  threshold. Verdict: **novel-combination, mechanism family already known.**
  Cite Moskalenko 2003 + Afanasjev 1996 and claim the translation-channel
  threshold-shift version + its machine use (selectivity dial, parking brake).
- **M4 statics depend on (tau,Dv) only via A = tau*Dv — already-known in essence.**
  The steady-state elimination v = (1 - tau*Dv*lap)^{-1} u is standard in the
  field's fixed-point analyses (it is how the 3-comp system reduces to a
  Swift-Hohenberg-like effective equation near onset). We have not seen it stated
  as a practical invariance-of-statics DESIGN RULE ("move along constant A to
  change dynamics keeping chemistry fixed") — that's a nice engineering statement
  worth keeping, verdict **novel-as-stated** (though trivially derivable, and
  surely folklore among practitioners).
- **Scattering tables (merge/repel outcomes) — already-known** and better
  organized: Nishiura's scattor theory would classify our AA-merge at d0=6.
- **Replication cascades ("spot soup") — already-known**: this is the
  self-replicating-spot regime of Gray-Scott/FIS (Pearson 1993; Lee et al. 1994),
  and in the 3-comp system Purwins school calls it generation/self-completion.
  Their "replication by many-particle interaction" (Liehr et al. 2003) = our
  "osc-dominant corners replicate on pairing".
- **Breathing dimer metastability — related-known**: breathing modes are a known
  co-dimension away (Gurevich 2006); our observation that the breather reorganizes
  to a tandem is consistent but specific to our corner; low-stakes claim.


---

## B. Localized states, homoclinic snaking, spatial dynamics

This is the theory world our G0/G0c "algebraic funnel" lives in: treat the steady-state
ODE in x as a dynamical system ("spatial dynamics"), classify the fixed point (vacuum)
by its spatial eigenvalues, and read off localized-state existence and tail shape.
Saddle-focus eigenvalues (complex quartet) ⇒ oscillatory tails ⇒ pinning, multiplicity
of bound states, snaking. Our funnel computes exactly these eigenvalues; the field has
40 years of refinements on what happens next.

### Key references

1. **Champneys (1998)** "Homoclinic orbits in reversible systems and their
   applications in mechanics, fluids and optics", *Physica D* 112:158. — The
   classification we use: real vs complex spatial eigenvalues of the vacuum,
   Belyakov-Devaney transition, infinite multiplicity of homoclinics near
   saddle-focus. Our G0c "tail eigenvalue" test is this paper as a filter.
2. **Woods, Champneys (1999)** "Heteroclinic tangles and homoclinic snaking in the
   unfolding of a degenerate reversible Hamiltonian-Hopf bifurcation", *Physica D*
   129:147. — Birth of "snaking" terminology; localized states near a subcritical
   pattern-forming (Turing) bifurcation.
3. **Burke, Knobloch (2006)** "Localized states in the generalized Swift-Hohenberg
   equation", *PRE* 73:056211; **(2007)** "Homoclinic snaking: structure and
   stability", *Chaos* 17:037102. — The canonical snaking diagrams: two
   intertwined branches of odd/even localized states + "ladder" rungs of
   asymmetric states; stability alternates along the snake.
4. **Kozyreff, Chapman (2006)** "Asymptotics of Large Bound States of Localized
   Structures", *PRL* 97:044502; **Chapman, Kozyreff (2009)**, *Physica D* 238:319.
   — Beyond-all-orders computation of the pinning-region width (exponentially small
   in the pattern amplitude). Explains quantitatively why bound states exist in a
   PARAMETER WINDOW, not a point — relevant to why our basins ~[14.5,19.5] are wide.
5. **Knobloch (2015)** "Spatial Localization in Dissipative Systems", *Annu. Rev.
   Cond. Mat. Phys.* 6:325; **(2008)** "Spatially localized structures in
   dissipative systems: open problems", *Nonlinearity* 21:T45. — Reviews; the
   2008 one lists open problems several of which our program touches (dynamics of
   localized states in 2D, interaction with heterogeneity).
6. **Lloyd, Sandstede, Avitabile, Champneys (2008)** "Localized Hexagon Patterns of
   the Planar Swift-Hohenberg Equation", *SIADS* 7:1049; **Avitabile et al (2010)**
   "To Snake or Not to Snake in the Planar SH Equation", *SIADS* 9:704. — 2D
   localized patches: snaking is messier in 2D, fronts can depin along different
   lattice directions.
7. **McCalla, Sandstede (2013)** "Spots in the Swift-Hohenberg Equation", *SIADS*
   12:831. — Spot A/B classification, amplitude scalings near onset in 2D/3D.
8. **Makrides, Sandstede (2014)** "Predicting the bifurcation structure of
   localized snaking patterns", *Physica D* 268:59. — Normal-form-level predictions
   of which snaking structure appears.
9. **Buryak, Akhmediev (1995)** "Stability criterion for stationary bound states of
   solitons with radiationless oscillating tails", *PRE* 51:3572. — Simple and
   general: bound separations quantized by tail oscillation period; every second
   equilibrium is a saddle. **This is the theory statement of our d* ladder and of
   the "n=1 stable / midpoints saddle" structure we measured.**
10. **Gorshkov, Ostrovsky (1981)** "Interactions of solitons in nonintegrable
    systems", *Physica D* 3:428. — The original effective-particle formalism:
    solitons as particles in an interaction potential given by tail overlap.
11. **Ei, Mimura, Nagayama (2002)** "Pulse-pulse interaction in reaction-diffusion
    systems", *Physica D* 165:176. — Rigorous center-manifold reduction to ODEs for
    pulse positions; weak-interaction regime; also 2D spots (2006, DCDS).
12. **Verschueren, Champneys (2021)** "Dissecting the snake: from localized patterns
    to spike solutions", *Physica D* 419:132858; **Al Saadi, Champneys, Verschueren
    (2021)** "Localized patterns and semi-strong interaction", *IMA J. Appl. Math*
    86:1031; **(2025)** "Snakes, Ladders, and Breathers", *SIADS* 24. — Recent
    program unifying snaking-type localized states with far-from-onset spike
    (semi-strong) states in RD systems — the bridge between our "funnel" regime
    and Gray-Scott-type spike regimes.
13. **Parra-Rivas, Knobloch, Gomila, Gelens (2016-2021)** (PRA 93:063839, PRE
    97:042204, IMA J Appl Math) — snaking + collapsed snaking for driven optical
    cavities (Lugiato-Lefever); shows the same funnel math organizes localized
    states in a completely different physical domain.
14. **Rademacher, Sandstede, Scheel (2007)** "Computing absolute and essential
    spectra using continuation", *Physica D* 229:166. — How to compute stability
    spectra of localized/traveling states properly (see TRICKS).

### STEAL / COMPARE (Area B)

- **G0c funnel (vacuum spatial eigenvalues → tail wavelength → shell spacing) —
  already-known method** (Champneys 1998 formalism; standard in snaking papers).
  Using it as a cheap PRE-FILTER for equation-space search (2 ms/candidate before
  any PDE run) is, as far as found, **a novel use** — the literature uses spatial
  dynamics to analyze given equations, not to triage random ones at scale.
- **d*/wavelength ≈ const transferable law (l0-sampler headline) — consistent with
  known theory**: Buryak-Akhmediev/Gorshkov-Ostrovsky predict d* locked to tail
  period with order-unity offset fixed by core phase. Literature would predict the
  BAND (our 1.2-1.5 measured) rather than a constant — matches our audit widening.
- **Multiplicity of shells (d1*, d2* = wake-locked tandem at 14.78/25.68 ≈ +1
  wavelength) — already-known** (tail quantization; wake-locked trains in optics
  literature "soliton bound states"; Purwins molecules).
- **Pinning/lattice artifacts — known in spirit**: snaking pinning is PHYSICAL
  pinning to the pattern wavelength; our dx-pinning is a NUMERICAL artifact the
  PDE-numerics community warns about. Our systematic "dx→dx/2 or it didn't happen"
  gate + the M2/M5 catalog of pinning artifacts (saddle masquerading as stable,
  lattice-stabilized species A) is stricter than common practice — keep it.
- **Fold-proximity organizing observation (L0: blobs live at 1-|k1/k1max| ≈ 0.03)
  — related-known**: localized states in subcritical systems live between the fold
  of the pattern branch and the Maxwell point (snaking region is anchored near
  folds); our cubic-fold distance is a crude scalar for the same fact.
  Verdict: novel-as-coordinate, folklore-as-physics. Literature refinement to
  import: the pinning region is exponentially thin near onset (Kozyreff-Chapman),
  so jittering in LOG fold-distance (which l0 already adopted) is the right move.


---

## C. Self-propelled objects + self-generated fields (our M6)

The "lagging self-generated field" propulsion mechanism has at least four independent
literatures: camphor/Marangoni boats, autophoretic droplets/colloids, cell-biology
self-generated gradients, and bouncing-droplet pilot waves. Our M6 self-launch is a
clean instance of a very well-established bifurcation type. What appears less explored
in those literatures: the field WRITING PERSISTENT INFRASTRUCTURE (tracks/rings) that
then functions as a machine part — that is closer to stigmergy/trail-formation models.

### Key references

1. **Nagayama, Nakata, Doi, Hayashima (2004)** "A theoretical and experimental study
   on the unidirectional motion of a camphor disk", *Physica D* 194:151. — Camphor
   disk + its own diffusing surfactant field; rest state destabilizes via a
   PITCHFORK to steady motion (drift bifurcation); velocity ∝ sqrt(supercriticality).
   Mathematically our M6 self-launch with b ↔ camphor concentration.
2. **Kitahata, Koyano, Iida, Nagayama (2018)** "Mathematical Model and Analyses on
   Spontaneous Motion of Camphor Particle" (RSC book ch. 2). — Reduction recipes for
   object+field systems; delay of the deposited field ⇒ effective negative friction.
3. **Michelin, Lauga, Bartolo (2013)** "Spontaneous autophoretic motion of isotropic
   particles", *Phys. Fluids* 25:061701. — ISOTROPIC particle in its own solute
   field self-propels above a critical Péclet number: instability of the symmetric
   state, no built-in asymmetry. The colloid version of our "parked blob below
   drift threshold launches for gamma ≥ 0.005".
4. **Maass, Krüger, Herminghaus, Bahr (2016)** "Swimming Droplets", *Annu. Rev.
   Cond. Mat. Phys.* 7:171. — Review of droplet swimmers (micelle-mediated,
   self-generated gradients).
5. **Jin, Krüger, Maass (2017)** "Chemotaxis and autochemotaxis of self-propelling
   droplet swimmers", *PNAS* 114:5089. — Droplets REPELLED by their own spent-fuel
   trails (negative autochemotaxis): trail-mediated self-avoidance, mazes. Our
   negative-gamma trails (self-trapping at g ≤ -0.07, repulsive stigmergy) live
   here; our positive-gamma attractive trails = classic ant-pheromone sign.
6. **Vajdi Hokmabad et al (2022)** "Spontaneously rotating clusters of active
   droplets", *Soft Matter* 18:2731. — Bound droplet clusters that spontaneously
   ROTATE, chirality from symmetry breaking of the chemical field. Active-matter
   twin of our M7 rotor (theirs: identical units, rotation from spontaneous
   symmetry breaking; ours: engineered heterodimer via nonreciprocal cross-v).
7. **Yoshinaga (2014)** "Spontaneous motion and deformation of a self-propelled
   droplet", *PRE* 89:012913. — Weakly nonlinear amplitude equations for
   translation/deformation coupling of a droplet in its own concentration field.
8. **Schweitzer, Schimansky-Geier (1994)** "Clustering of active walkers in a
   two-component system", *Physica A* 206:359. — Active Brownian walkers depositing
   a diffusing, decaying field they respond to: aggregation transition. The
   particle-based ancestor of our b-field architecture (deposition gamma,
   relaxation tau_b, diffusion D_b — same three dials).
9. **Helbing, Keltsch, Molnár (1997)** "Modelling the evolution of human trail
   systems", *Nature* 388:47; + **Helbing, Schweitzer, Keltsch, Molnár (1997)**,
   *PRE* 56:2527. — Walkers + ground-potential field with deposition & decay ⇒
   self-organized trail NETWORKS as attractors of the coupled dynamics. This is
   our genesis result ("landscapes are L1 fixed points") in a social-physics
   setting, including the direct analog of our racetrack/ring digging.
10. **Couder, Protière, Fort, Boudaoud (2005)** "Walking and orbiting droplets",
    *Nature* 437:208; **Fort et al (2010)** PNAS 107:17515; **Bush (2015)**
    *Annu. Rev. Fluid Mech.* 47:269. — Bouncing droplet + its own standing-wave
    field ("path memory"): walking bifurcation, ORBITING BOUND PAIRS at DISCRETE
    radii, quantized self-orbits in rotating frames. The pilot-wave community has
    our exact trio: self-launch (walking threshold), discrete bond distances
    (from wave-field oscillations), and self-written confining landscapes
    (memory-induced quantization). Strongest single external analog to M2+M6.
11. **Tweedy, Susanto, Insall (2016)** "Self-generated chemotactic gradients —
    cells steering themselves", *Curr. Op. Cell Biol.* 42:46. — Cells consume
    attractant to build their own gradients; solve mazes (Tweedy et al 2020,
    Science 369:eaay9792). Biology's M6.
12. **Gurevich, Friedrich (2013)** "Instabilities of Localized Structures in
    Dissipative Systems with Delayed Feedback", *PRL* 110:014101 (+ Pimenov 2013
    PRA 88:053830 "delayed feedback control of self-mobile cavity solitons"). —
    DELAY of a self-influencing field generically induces drift/oscillation of
    localized states; the abstract theorem behind "lagging hill ⇒ launch".
13. **Krischer, Mikhailov (1994)** (see A3): their traveling spot is destabilized
    by coupling to a slow global field — same slow-field-lag logic.

### STEAL / COMPARE (Area C)

- **M6 self-launch (autophoresis) — already-known as a mechanism class.**
  Camphor (Nagayama 2004), isotropic autophoresis (Michelin 2013), walking
  droplets (Couder 2005), delayed-feedback DS (Gurevich 2013). Our specific
  embedding (4th field through the isok channel with exact vacuum, c ∝ gamma^0.34
  law, drag/plow ±asymmetry, self-trapping threshold) is house engineering; the
  bifurcation is textbook. **Cite Michelin & Nagayama & Couder when publishing;
  the c(gamma) exponent and trail law b(s)=B0 exp(-s/(c tau_b)) are worth stating
  as new quantitative results for the RD-blob embedding** (the trail law is the
  standard advection-relaxation solution, but its 0.002% verification is a nice
  certificate).
- **Stigmergy / trail-mediated interaction (BF3) — already-known** (Schweitzer,
  Helbing; ant-trail models; autochemotaxis droplets). Our contribution: doing it
  with FIELD-solitons (no particles anywhere) with controls. Verdict:
  novel-combination.
- **Self-written sawtooth + ring racetrack (genesis) — novel-combination with
  strong priors.** Helbing trails and droplet path-memory show self-written
  landscapes; asymmetric standing profile from ONE-WAY circulation matches
  "footprints lag the walker". A self-dug closed RACETRACK that later guides a
  fresh immobile blob into orbit — we found no direct equivalent published.
  Closest: pilot-wave memory-quantized orbits (Fort 2010) where the droplet
  orbits in its OWN live field (not a frozen one).
- **Amplitude ladder park→mush→circulate→diode and chi=v/slope efficiency (self-
  written beats hand-built by 10-40x) — new-as-far-as-found** as explicit design
  laws. Related folklore: "systems tune their own environments to marginal
  stability", but we found no quantitative statement of self-written-landscape
  efficiency vs exogenous landscapes in RD.
- **b-ASSEMBLY (3 distant blobs collapse via shared halo well) — related-known:**
  chemotactic collapse (Keller-Segel aggregation) and Schweitzer clustering are
  the field-mediated version; our observation that assembly lands exactly on M4
  shells then self-launches as a trimer is a nice composite but the ingredients
  are known.
- **BLOB-FROM-NOISE theory-backed NO — matches literature**: nucleation of DS
  needs finite-amplitude perturbation (subcritical); known since Kerner-Osipov;
  in gas discharge blobs are ignited by finite fluctuations or boundaries. Our
  vacuum-exact-coupling argument (quadratic deviation ⇒ no linear destabilization)
  is a clean local proof of a known expectation.


---

## D. Collision-based & soliton computing; transport machines from waves

The computing-with-mobile-localized-states program is 30+ years old. It gives us
vocabulary (gates, diodes, memory) and honest caution: most demonstrated "machines" are
one-shot gates in structured media, and general-purpose architecture claims outpace
implementations. Our RELAY TUG sits in an odd, mostly empty niche: not logic, but
sustained mechanical WORK (upstream transport) by an emergent composite in an
unstructured (well, self-consistent) field theory.

### Key references

1. **Adamatzky (ed.) (2002)** *Collision-Based Computing* (Springer). — Framing
   volume: computation via ballistic mobile patterns (gliders, solitons, wave
   fragments); includes Jakubowski/Steiglitz/Squier "Computing with Solitons".
2. **Jakubowski, Steiglitz, Squier (1998)** "State transformations of colliding
   optical solitons and possible application to computation in bulk media",
   *PRE* 58:6752. — Manakov-soliton collisions implement state machines; "particle
   machine" architecture (Steiglitz et al. 1988 IEEE ToC) = compute by injecting
   particle streams that collide.
3. **Adamatzky (2004)** "Collision-based computing in Belousov-Zhabotinsky medium",
   *Chaos Solitons Fractals* 21:1259; **De Lacy Costello & Adamatzky (2005)**
   experimental gates. — Sub-excitable BZ wave-fragments as billiard-ball logic.
4. **Tóth, Showalter (1995)** "Logic gates in excitable media", *JCP* 103:2058;
   **Gorecki et al (2009)** "Information processing with structured excitable
   medium", *Nat. Computing* 8:473. — Channel-and-junction (structured-medium)
   chemical logic: signals = excitation pulses in engineered geometry. Our
   rails/tracks/forks are the DS analog of their etched channels.
5. **Suzuki, Yoshinobu, Iwasaki (2000)** "Unidirectional propagation of chemical
   waves through microgaps between zones with different excitability", *JPC A*
   104:6602; **Tóth, Horváth, Yoshikawa (2001)** *CPL* 345:471. — CHEMICAL DIODES:
   asymmetric junction/heterogeneity ⇒ one-way wave passage. Prior art for our
   genesis DIODE (kicked-against-tooth reverses) — same asymmetry logic, but ours
   is written by the physics itself.
6. **Teramoto, Yuan, Bär, Nishiura (2009)** "Onset of unidirectional pulse
   propagation in an excitable medium with asymmetric heterogeneity", *PRE*
   79:046205. — Theory of the diode in RD pulses: which asymmetric defects
   transmit one way. The 3-component-model version of our tooth asymmetry.
7. **Adamatzky (2010)** *Physarum Machines* (World Scientific); **Tero et al
   (2010)** *Science* 327:439. — Blob-organism computing: network design,
   transport, decision-making by a real amorphous blob + its self-written tube
   infrastructure. Spiritually closest living system to our program (blob +
   self-dug landscape doing logistics).
8. **Barland et al (2002)** "Cavity solitons as pixels in semiconductor
   microcavities", *Nature* 419:699. — DS as movable, writable information
   carriers; **McIntyre et al (2010)** *PRA* 81:013838: cavity-soliton DELAY LINE —
   solitons conveyed by an imposed phase gradient = our P1 gradient conveyor,
   photonic version (and they hit the same "gradient strength window" limits).
9. **Wuensche (2002)** "Finding Gliders in Cellular Automata" (in Collision-Based
   Computing). — Automated glider discovery via input-entropy filtering; early
   "search for mobile objects in rule space" (cf. our l0-sampler assays).

### STEAL / COMPARE (Area D)

- **Machine gate B6 (relay tug: 3-train hauling 3 cargo upstream, self-healing) —
  new-as-far-as-found in RD dissipative-soliton physics.** Literature machines
  are: logic gates (BZ, solitons), memory pixels (optics), delay lines/conveyors
  (imposed gradients), diodes (structured media). We found NO published example of
  an emergent multi-soliton composite doing repeated net transport of other
  solitons AGAINST a load field in an isotropic RD model, let alone with
  power-ceiling/shedding/self-healing phenomenology. Closest relatives: cargo
  towing by camphor boats & droplet swimmers (particle world, not field world);
  cavity-soliton delay lines (external drive does the work). **This is our
  strongest novelty claim in D — but frame it as "engineered demonstration",
  since every COMPONENT (drift zones, tail binding, gradient force, diode) is
  known physics.**
- **Pair-only zone as selectivity dial for machines — new-as-far-as-found**
  (see Area A: rotation-precedes-drift is known; using composite-vs-single motility
  windows as a TRANSPORT SELECTOR/parking brake appears original).
- **Trains (3-blob faster than pair faster than single) — related-known:** wake
  surfing/drafting of pulses; in optics, soliton trains lock at tail distances
  with modified group velocity. Our speed-orders-with-length measurement is a
  small quantitative addition.
- **Walls that self-assemble from a parked blob (P3) — related-known:** transverse
  (zigzag→stripe) instabilities of DS and stripe formation are canonical; using a
  defect-grown stripe as a functional WALL is a cute engineering reuse. Verdict:
  novel-combination.
- **STEAL for a future milestone:** collision LOGIC. Nishiura's scattor framework
  + our certified encounter tables suggest a minimal blob AND/OR gate is within
  reach (input = blob present/absent on two rails, junction geometry from isok
  landscape). The BZ/soliton literature gives acceptance criteria (gate truth
  table + cascadability). Also STEAL: Wuensche-style entropy filters for mobile-
  object detection in l0 assays.


---

## E. Artificial-life continuous worlds (Lenia family, SmoothLife, NCA)

Closest COMMUNITY to our program in spirit (creatures in continuous fields, taxonomy,
machine ambitions), farthest in METHOD (their rules are designed/evolved for richness;
ours is a physics model with theory handles). The trade is clean: they have
self-replication with inheritance, open-ended evolution attempts, and mature automated
discovery; we have exact vacua, bifurcation laws, funnel-predicted structure, and
certified machines. Nothing in the Lenia world resembles our algebraic funnel; nothing
in our world resembles their heritable variation. Both sides know it (Flow-Lenia's
motivation section reads like our M6 brief inverted).

### Key references

1. **Chan (2019)** "Lenia — Biology of Artificial Life", *Complex Systems* 28
   [arXiv:1812.05433]. — Continuous CA; 400+ "species" taxonomy discovered by
   interactive evolution; morphological classification, statistical measures.
2. **Chan (2020)** "Lenia and Expanded Universe" [arXiv:2005.03742]. — Multi-kernel,
   multi-channel Lenia ≈ recurrent conv net; new phenomena incl. polyhedral
   symmetries; semi-automatic genetic search.
3. **Rafler (2011)** "SmoothLife" [arXiv:1111.1567]. — First continuous GoL
   generalization; gliders in continuum.
4. **Plantec, Hamon, Etcheverry, Oudeyer, Moulin-Frier, Chan (2023)** "Flow-Lenia"
   [arXiv:2212.07906, ALIFE'23; expanded: *Artificial Life* 2025,
   doi:10.1162/artl_a_00471]. — Mass-conserving Lenia with PARAMETER LOCALIZATION:
   update-rule parameters become advected fields ⇒ creatures carry genotypes ⇒
   multi-species competition and EMERGENT EVOLUTIONARY DYNAMICS inside the CA.
   The single most important idea to (eventually) steal: make coupling constants
   local fields advected with the matter, and inheritance comes for free.
5. **Hamon, Etcheverry, Chan, Moulin-Frier, Oudeyer (2025)** "Discovering
   sensorimotor agency in cellular automata using diversity search", *Sci. Adv.*
   11:eadp0834. — Lenia creatures that individuate, sense obstacles, navigate;
   found by goal-directed diversity search with curriculum; robustness tests
   (moving/changing environments) close to our jitter/OOG audit ethos.
6. **Mordvintsev, Randazzo, Niklasson, Levin (2020)** "Growing Neural Cellular
   Automata", *Distill*. — Differentiable CA trained for morphogenesis +
   regeneration; spawned the NCA field.
7. **Sinapayen (2023)** "Self-Replication, Spontaneous Mutations, and Exponential
   Genetic Drift in Neural Cellular Automata" [arXiv:2305.13043]. — NCA
   replicators with heritable mutations — the phenomenology our program
   deliberately excludes (we kill replication as a failure mode!).
8. **Davis, Bongard (2022)** "Glaberish" [arXiv:2205.10463]; "Step Size is a
   Consequential Parameter in Continuous CA" [arXiv:2205.12728]. — Continuous-CA
   integrator honesty: dt artifacts change the fauna. Their warning = our
   dt<dx²/(4Dw) + IMEX discipline.
9. **Kojima, Ikegami (2023)** "Implementation of Lenia as a Reaction-Diffusion
   System" [arXiv:2305.13784]. — Explicit bridge: Lenia dynamics recast as RD
   (kernel → diffusion cascade). Confirms our two worlds are formally adjacent;
   route for importing Lenia species into PDE-land with our funnel tools.
10. **Mordvintsev, Randazzo, Niklasson (2021)** "Differentiable Programming of
    Reaction-Diffusion Patterns" [arXiv:2107.06862]; (2023) "...of Chemical
    Reaction Networks" [arXiv:2302.02714]. — Gradient-descent INVERSE DESIGN of RD
    systems for target patterns/textures. Directly relevant to our b_target
    inverse problem (MERGE milestone): they show differentiable-simulator descent
    works for RD targets.

### STEAL / COMPARE (Area E)

- **Their species taxonomy vs our flavors:** Lenia species are search products
  without theory handles (no vacuum analysis, no bifurcation laws, no exact
  conservation guarantees except in Flow-Lenia). Our vvw/xv flavor architectures
  with iso-background construction + port classification are, as far as found,
  **new engineering** (multi-species coexistence in ONE RD world with a shared
  long-range inhibitor and per-species private channels). Multi-channel Lenia
  (Expanded Universe) has multi-species worlds but no exact shared-vacuum
  constraint or conservation table ethos.
- **Self-replication with inheritance — THEIR unique capability.** Flow-Lenia
  parameter localization is the concrete mechanism. For us the analog would be:
  promote a coupling (e.g. d_i on the iso-line, or eta) to a slowly-diffusing
  field advected by blob presence — a "genome field". Our M6 b-field is already
  the scalar prototype (environment memory); a species-parameter memory is the
  next rung. Flag as MERGE-milestone-adjacent, honest cost: replication is
  currently our enemy (cascade trap), inheritance requires taming it.
- **Their search (interactive evolution, CMA-ES, IMGEP diversity) vs our funnel:**
  they sample behavior space blind; we pre-filter equation space by algebra
  (2 ms vs 40 s assay). **Nothing like the G0c funnel exists in the Lenia
  literature** — spatial-dynamics eigenvalues don't even apply to their nonlocal
  kernels without the Kojima-Ikegami recasting. This is our main methodological
  export TO them; their IMGEP/diversity loops are the main import (Area F).
- **Their robustness tests (obstacle courses, damage recovery in NCA) — worth
  importing as assays** for machine certification beyond noise-jitter: cut a
  train in half mid-haul (we already saw self-healing relay), move a wall during
  transport, regeneration gates.
- **Asymptotic Lenia / glider PDE analysis (Davis 2024; Kojima 2025 "glider
  equation")** — they are starting to do OUR kind of analysis on their objects;
  converging fields.


---

## F. Quality-diversity & automated discovery of dynamical systems (our L0 program)

Our l0-sampler/l0-evolver sits squarely in this literature's frame — with one genuine
methodological difference: an ALGEBRAIC pre-filter (spatial-eigenvalue funnel) instead
of (or before) behavioral novelty. QD gives us archive discipline; IMGEP gives us
goal-space exploration; ASAL gives us FM-based behavior descriptors. None of them have
theory-gated sampling.

### Key references

1. **Mouret, Clune (2015)** "Illuminating search spaces by mapping elites"
   [arXiv:1504.04909]. — MAP-Elites: archive over behavior descriptors keeping the
   best per cell. Our "MAP-Elites archive" is literally this; their insight that
   illumination ≠ optimization matches our yield-curve deliverable.
2. **Lehman, Stanley (2011)** "Abandoning Objectives: Evolution Through the Search
   for Novelty Alone", *Evol. Comp.* 19:189. — Novelty search; behavior-space
   distance as the driver. Relevant to our "novel world per 50 core-hours" metric:
   novelty pressure would spend compute at the archive frontier instead of uniform.
3. **Reinke, Etcheverry, Oudeyer (2020)** "Intrinsically Motivated Discovery of
   Diverse Patterns in Self-Organizing Systems", ICLR [arXiv:1908.06663]. — IMGEP
   (goal-conditioned exploration with learned goal spaces, e.g. VAE features) beats
   random/evolution for finding diverse Lenia patterns. THE closest prior work to
   l0-sampler's mission. Their learned descriptors ↔ our hand-built assay battery.
4. **Etcheverry, Moulin-Frier, Oudeyer (2021)** "Hierarchically-organized latent
   modules for exploratory search (HOLMES)" + **(2023)** "Meta-Diversity Search"
   [arXiv:2312.00455]. — Diversity OF diversities: multiple descriptor spaces
   grown hierarchically; answers "diverse in which sense?" — our multi-assay
   (alive/bond/drift/chem) archive is a hand-rolled version.
5. **Faldor, Cully (2024)** "Leniabreeder" [arXiv:2406.04235]. — QD (MAP-Elites +
   AURORA unsupervised descriptors) for Lenia; explicit open-endedness ambitions.
6. **Kumar, Lu, Kirsch, Tang, Stanley, Isola (2024)** "Automating the Search for
   Artificial Life with Foundation Models (ASAL)" [arXiv:2412.17799]. — CLIP-style
   FM embeddings score simulations: target search, open-endedness search
   (novelty in FM space over time), and illumination across substrates (Lenia,
   Boids, Particle Life, GoL). Substrate-agnostic descriptors — could score OUR
   films tomorrow.
7. **Wang, Lehman, Clune, Stanley (2019)** "POET" [arXiv:1901.01753]. — Coevolve
   environments + agents with transfer; our L2/L3 ("landscape discovers what's
   worth wanting") is a POET-shaped loop with physics instead of RL agents.
8. **Grizou, Points, Sharma, Cronin (2020)** "A curious formulation robot enables
   the discovery of a novel protocell behavior", *Sci. Adv.* 6:eaay4237. —
   Curiosity loop over WET droplet experiments; validated that machine-driven
   exploration finds behaviors humans missed. Physical-world sibling of l0.
9. **Etcheverry, Moulin-Frier, Oudeyer, Levin (2024)** "AI-driven automated
   discovery tools reveal diverse behavioral competencies of biological networks",
   *eLife* 92683. — IMGEP on gene-network ODEs; discovery tooling ports across
   substrate classes (their claim, our hope for l0 → pod fan-out).
10. **Lu et al (2024)** "The AI Scientist" [arXiv:2408.06292] (Sakana). — Full
    LLM loop (idea → experiment → paper). Our controller/searcher/scorecard
    architecture is a domain-specialized instance with harder gates (fresh-seed
    audits; their reviewer is an LLM, ours is a rerun).

### STEAL / COMPARE (Area F)

- **G0c algebraic funnel as pre-filter — new-as-far-as-found in this literature.**
  QD/IMGEP methods treat the system as a black box; nobody gates candidates on
  spatial-dynamics eigenvalues before simulating (2ms vs 40s = 20,000x cheap
  filter). This inverts the usual cost structure and is our top methodological
  export. (Caveat: physics-informed priors exist in other guises — e.g. linear
  stability pre-screens in Turing-pattern scans, dispersion-relation filters in
  materials discovery. State the claim as "first use in ALife-style
  equation-space search", not "first ever".)
- **Jitter-vs-uniform yield economics (jitter maps islands 25x faster) — known
  qualitatively** (novelty search literature: local mutation exploits archive
  frontier; MAP-Elites elites as stepping stones). Our numbers are substrate-
  specific but the phenomenon is the standard QD argument. Import: QD's
  "curiosity score" (pick parents whose offspring most often land in new cells)
  would formalize our jitter-by-ref scheduling.
- **Assay battery ↔ learned descriptors:** IMGEP/AURORA/ASAL all argue LEARNED
  behavior spaces beat hand-crafted ones for diversity. Our assays are
  interpretable but low-dimensional; a cheap upgrade is appending an FM embedding
  (CLIP on strips) as extra archive axes — zero physics cost, catches "weird"
  worlds our assays alias. (= ASAL illumination bolted onto l0.)
- **Block-composition evolver (merge validated by reconstructing vvw/xv) —
  related-known:** modular/crossover operators and "genotype = operator matrix"
  appear in CPPN/graph evolution; validating merge operators by RECONSTRUCTING
  known jumps is good practice we haven't seen stated; keep it.
- **POET-style co-evolution:** our MERGE milestone (evolve b-landscape while
  evolving blobs to use it) is exactly a POET instance; steal their transfer
  criterion (candidate must outperform natives in target env) as the gate for
  "landscape actually helps".


---

## G. Emergent machines & ratchets in field theories

The ratchet literature supplies exact symmetry theorems for when directed transport is
possible; the active-matter literature shows machines extracting work from agitation.
Both illuminate our M5 machine and our honest negatives.

### Key references

1. **Reimann (2002)** "Brownian motors: noisy transport far from equilibrium",
   *Phys. Rep.* 361:57. — The ratchet bible. Curie's principle sharpened: no
   directed transport without broken spatial or temporal symmetry + out-of-
   equilibrium drive. Taxonomy: flashing, rocking, drift ratchets.
2. **Hänggi, Marchesoni (2009)** "Artificial Brownian motors: controlling transport
   on the nanoscale", *RMP* 81:387. — Updated review; particle sorting by
   ratchets (cf. our species-selective transport ambitions).
3. **Flach, Yevtushenko, Zolotaryuk (2000)** "Directed Current due to Broken
   Time-Space Symmetry", *PRL* 84:2358. — Symmetry classification of drives that
   rectify; biharmonic-drive trick (temporal asymmetry substitutes for spatial).
4. **Salerno, Quintero (2002)** "Soliton ratchets", *PRE* 65:025602; **Quintero,
   Sánchez-Rey, Salerno (2005)** *PRE* 72:016610. — Kink/soliton in asymmetric
   periodic potential + ac drive ⇒ net soliton drift; collective-coordinate
   theory: the ratchet works through coupling of translation to INTERNAL MODES.
   **Directly explains our P4 honest negative**: our blob is "too stiff" — with
   positional diffusion ≈ 0 and no excited internal mode, there is no Kramers/
   harmonic channel to rectify; deterministic overdamped gradient sliding is all
   that remains (which is what our conveyor does).
5. **Kettner, Reimann, Hänggi, Müller (2000)** "Drift ratchet", *PRE* 61:312. —
   Asymmetric pores + oscillatory flow ⇒ particle-size-selective drift; the
   engineering template for "sorting by geometry" (our fork/sorter primitives).
6. **Di Leonardo et al (2010)** "Bacterial ratchet motors", *PNAS* 107:9541;
   **Sokolov et al (2010)** *PNAS* 107:969; **Angelani et al (2009)** *PRL*
   102:048104. — Asymmetric gears in active baths rotate unidirectionally:
   machines extracting work from nonequilibrium agitation. Conceptual cousins of
   our relay tug (work from blob activity), but they need hand-made asymmetric
   hardware; our track is self-writable (genesis).
7. **Gōbel, Mertig (2021)** "Skyrmion ratchet propagation", *Sci. Rep.* 11:3020
   (+ skyrmion racetrack literature, Fert/Sampaio 2013). — Topological-soliton
   transport engineering in magnets: racetracks, pinning sites, diodes — a whole
   parallel industry of "soliton logistics" with the same primitives we built
   (track, dock, diode); theirs are lithographed, ours are field-grown.
8. **Ivlev, Bartnick, Heinen, Du, Nosenko, Löwen (2015)** "Statistical Mechanics
   where Newton's Third Law is Broken", *PRX* 5:011035. — Nonreciprocal
   interactions (wake-mediated, like our eta12/eta21) as a first-class framework;
   action-reaction symmetry breaking yields self-propelled and rotating bound
   states. Our M7 decomposition (eta12-only rotates, eta21-only static) is a
   textbook nonreciprocal-couple experiment; the modern "non-reciprocal phase
   transitions" literature (Fruchart, Hanai, Littlewood, Vitelli, Nature 2021)
   generalizes exactly this (chiral phases from nonreciprocity).

### STEAL / COMPARE (Area G)

- **Stiff-soliton ratchet negative — already-known physics, correctly diagnosed.**
  Soliton-ratchet theory says rectification needs a soft internal mode or noise-
  activated hopping; our blob at machine-safe amplitude has neither. Cite Salerno-
  Quintero when reporting P4. The literature ALSO offers the fix if we ever want
  a noise ratchet: work near the drift bifurcation where the propagator mode is
  soft (large susceptibility — which is exactly what our M5 near-onset adversary
  exploits at 50x) and/or use a flashing (time-modulated) track, or biharmonic
  temporal drive instead of spatial asymmetry.
- **Relay tug vs active-matter machines — novel-combination:** work extraction by
  emergent composites exists (bacterial gears), but the gear is external hardware.
  Our machine's "hardware" (saw track + rails) is (a) exactly zero-footprint in
  vacuum, (b) provably growable by the physics itself (genesis reduction). We
  found no published machine whose track is a fixed point of the same field
  theory that powers the engine. **Strongest program-level novelty claim; phrase
  carefully: components known (Areas A,C,D,G), closed loop appears new.**
- **Nonreciprocity (M7) — connect to the hot literature:** cite Ivlev 2015 +
  Fruchart et al 2021 "Non-reciprocal phase transitions" (Nature 592:363) when
  presenting the rotor; our eta cross-coupling is engineered nonreciprocity, and
  "rotation as attractor" is their chiral phase at N=2. This makes M7 legible to
  a large audience.
- **Sorting (fork/sorter primitives, planned):** steal the ratchet-sorting design
  rules (mobility differences amplified by geometry; Kettner 2000, Hänggi-
  Marchesoni §sorting). Our per-species tau windows and pair-only zones are the
  mobility knobs.


---

## Synthesis — the program in one paragraph of literature

Our substrate and ladder M0→M4 reproduce, with unusually strict numerical honesty, the
1994-2013 Purwins-school program (dissipative solitons in the 3-component RD system:
existence, drift bifurcation, tail-mediated molecules, rotating/traveling bound states)
— with M7's rotor-only zone anticipated in its rotational form by Moskalenko-Liehr-
Purwins 2003, and M6's self-launch a clean RD instance of the self-generated-field
propulsion class (camphor, autophoresis, pilot-wave walkers, delayed feedback). Where
we appear to be genuinely ahead of anything published: (1) the MACHINE — an emergent
soliton train hauling soliton cargo upstream on a ratchet track that is itself a fixed
point of the same field theory (components known; closed loop not found anywhere);
(2) the pair-only TRANSLATION zone used as a transport selector/parking brake; (3) the
genesis reduction map with its quantitative design laws (chi-efficiency of self-written
landscapes, amplitude ladder, speed-matching); (4) the algebraic-funnel-gated
equation-space search (spatial-dynamics eigenvalues as a 20,000x pre-filter for
MAP-Elites illumination). Our biggest known GAPS vs neighboring fields: no
self-replication with inheritance (Flow-Lenia's parameter localization is the import
path), no continuation-grade bifurcation certificates (pde2path/freezing-method are
drop-ins), and no learned-descriptor diversity channel (IMGEP/ASAL bolt-ons).

## Sanity notes / possible contradictions with our laws

- **c ∝ sqrt(τ−τc) near drift onset**: literature-consistent (supercritical
  drift-pitchfork). But Bödeker 2003 shows noise TURNS the sharp bifurcation into
  a crossover (noise-covered bifurcation) — matches our M6 "sub-threshold creep";
  cite them rather than treating creep as an anomaly.
- **Purwins-school reduced dynamics predict** dc/dτ discontinuities when higher
  modes (breathing/deformation) couple: our OOW 6.3% at tau=6.1 may be that, not
  measurement error.
- **Buryak-Akhmediev alternation**: every second tail-equilibrium is a saddle ⇒
  our M2 finding "tau=3.0 d*=14.65 is a continuum saddle" is EXPECTED, not a trap
  peculiar to lattice effects — the lattice merely stabilized what theory says is
  a saddle. Worth one sentence of reframing in the public page.
- **Ratchet caveat for the public page**: a static asymmetric potential + damped
  deterministic particle does NOT rectify by itself (Reimann). Our machine is
  powered by the active drift mode (self-driven particles on a ratchet = active
  ratchet, cf. Di Leonardo's bacterial gears; Ai's active-particle ratchets). Say
  "active-particle ratchet", not "ratchet" bare, or someone will object.
- **"Soliton too stiff for Kramers hops" (P4 negative)**: soliton-ratchet theory
  (Salerno-Quintero) says rectification requires soft internal modes or noise ≈
  translational diffusion; both absent in our regime — negative is theory-
  consistent and worth citing as such.
- **Replication near binding window edge (0.1 in k1)**: Purwins school reports the
  same adjacency (generation via interaction near instability); Liehr's
  "Replication of Dissipative Solitons by Many-Particle Interaction" (2003) is
  the same effect we call the replication edge.

*(End of review. See TRICKS.md for the import list, NAMING.md for terminology,
sources.jsonl for the full consultation log.)*
