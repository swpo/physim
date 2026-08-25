# PATCHWORLDS LITREVIEW — coupling heterogeneous RD/PDE models across space

**Question.** What is known about combining/coupling heterogeneous reaction–diffusion
(or general PDE) models across spatial domains — and does it change how we should
implement partition-of-unity (PoU) world composition (`theta(x) = rho_A theta_A + rho_B theta_B`)?

**Scope.** Focused pass (~3h), 51 sources across four areas. Sources: arXiv API +
Crossref + primary pages (Serper key not configured; no Google layer). Full source
list: `sources.jsonl`. Our plan under review: IDEAS.md "BLOBS: PATCHWORLDS".

**One-line verdict.** The literature strongly supports *modified PoU on one grid*:
blend the wiring (RHS/reaction parameters) with wide smooth weights, keep vacua
aligned (this is exactly "ghost-force removal"), and write the diffusion operator in
conservative flux form `div(D(x) grad u)` — but treat the seam as a first-class
dynamical object (it pins, refracts, blocks, and hosts new states), not as a passive
interpolation region. Do NOT go to two-grid interface matching; that imports an
entire literature of transmission-condition problems we don't have.

---

## A. Domain decomposition, overlapping grids, PoU-FEM — smooth blending vs interface matching

### What the field says

- **Melenk & Babuška 1996; Babuška & Melenk 1997** (PoU-FEM founders,
  doi:10.1016/S0045-7825(96)01087-0, doi:10.1002/(SICI)1097-0207...). PoU glues *local
  approximation spaces* into a global one; all error bounds require `|grad rho| <=
  C/diam(patch)`. Translation: the extra terms a PoU injects are controlled by the
  *weight gradient* — seam width is the rigor knob, and every guarantee in this
  literature is about approximating ONE PDE, not blending two different ones.
- **Chessa, Wang & Belytschko 2003** (doi:10.1002/nme.777): the *blending-element
  problem*. In the transition ring where an enrichment is only partially active, the
  PoU property fails and **parasitic terms** appear that neither description can
  represent; they degrade convergence *globally*, not just locally. **Fries 2008**
  (doi:10.1002/nme.2259) fixes it by pre-multiplying the enrichment with a smooth ramp
  that vanishes at the ring's edge — i.e., *modify what is blended* so the blend zone
  carries no orphaned terms. This is the canonical "naive PoU has a disease; modified
  PoU cures it" story, 450+ cites.
- **Arlequin method** (Ben Dhia & Rateau, doi:10.1002/nme.1229): the rigorous way to
  *superpose two different mechanical models* on an overlap: PoU-blend their
  **energies**, then tie the two states together with Lagrange multipliers (weak
  matching) on the overlap. Works, but requires an explicit coupling operator and a
  second copy of the state — the heavyweight fallback if one-field blending fails.
- **Atomistic-to-continuum blending** — the sharpest theory of blending two
  *different physics*: **Badia, Parks, Bochev, Gunzburger & Lehoucq 2008**
  (doi:10.1137/07069969X) prove that energy-blending produces **ghost forces**
  (spurious forces in the blend zone even when both models agree on the homogeneous
  ground state's neighborhood), while force/RHS-blending avoids them. **Luskin &
  Ortner 2013** (Acta Numerica, doi:10.1017/S0962492913000068) quantify: ghost-force
  error scales with `|grad rho|`; wide smooth blends + ghost-force correction reach
  optimal accuracy. *RD translation:* blending the reaction RHS ("wiring") is the
  good kind of blending, and demanding the two worlds share the ground state (our
  iso-vacuum constraint `k1(x) = u0^3 - lam(x) u0`) is precisely ghost-force removal.
- **Chimera/overset grids** (Chesshire & Henshaw 1990, doi:10.1016/0021-9991(90)90196-8;
  1994, doi:10.1137/0915051): two grids + interpolation in overlaps works for smooth
  fields but is **non-conservative**; steep fronts crossing the overlap need special
  conservative interpolation. One shared grid with one flux-form operator (our plan)
  sidesteps this entire failure class.
- **Nonlinear Schwarz / SWR**: overlapping Schwarz converges for semilinear elliptic
  RD-type problems (Lui 1999, doi:10.1137/S1064827597327553); for time-dependent
  semilinear RD the *transmission conditions should themselves be nonlinear* and
  problem-adapted (Caetano, Gander, Halpern & Szeftel 2010, DD19). OSWR explicitly
  supports "a different model in different subdomains" (Bennequin–Gander et al.,
  arXiv:1407.1074). Nonlinear reaction terms are not an obstruction — but interface
  matching for nonlinear RD is a *craft* with per-problem tuning.
- **Buffer zones in production** (numerical weather prediction): Davies 1976
  relaxation (doi:10.1002/qj.49710243210) nudges the interior toward the exterior
  solution across a 5–10-cell ramp; 50 years of practice. Known artifacts (Warner et
  al. 1997 tutorial, BAMS): partial reflection at buffer edges, over-specification
  noise, and a hard empirical rule — **the ramp must be wide compared to the
  wavelengths crossing it**.

### STEAL / WARNING → our plan

- **STEAL (load-bearing):** *Blend the RHS, align the ground states.* The a/c
  literature says RHS/force blending + shared equilibrium = no ghost forces. Our
  vacuum-safe wiring PoU + iso-vacuum constraint is exactly this recipe, discovered
  independently. Keep it; cite it as principled, not hacky.
- **STEAL:** *Seam-width scaling.* Every rigorous bound goes through `|grad rho| ~ 1/w`.
  Our measured seam source `~ Du |du0| / w^2` matches the pattern (second-order term).
  Publish seam width in units of the longest intrinsic length (blob tail 2–15 px,
  w-halo ~ sqrt(Dw*theta) ≈ 4–20 px) — that ratio is THE validity parameter.
- **WARNING (blending-element disease):** in the ring where `0 < rho < 1`, the
  effective world is a *third model* neither A nor B certified. Do not assume
  certified-A + certified-B = certified seam (see also Tanaka–Sugeno in area C).
  Concretely: scan the 1-D homotopy `theta(s) = s theta_A + (1-s) theta_B, s in [0,1]`
  BEFORE any 2-D patch run — if any s crosses a death/cancer boundary, the seam will
  manufacture that pathology in a strip.
- **WARNING:** interface matching (two grids, transmission conditions) for our
  nonlinear system would demand problem-adapted nonlinear transmission operators
  (Caetano et al.) and conservative interpolation (Chesshire–Henshaw). Nothing in our
  goals requires it. Stay on one grid.

---

## B. Heterogeneous media in reaction–diffusion — expected seam phenomenology

### What the field says

- **Our exact lineage already did the 1-D version.** Purwins' own group:
  **Schütz, Bode & Purwins 1995** (Physica D 82:382) — spatial parameter
  inhomogeneities act on fronts as an effective potential: pinning, oscillation
  around the defect, transmission, and inhomogeneity-induced front *generation*.
  **Kulka, Bode & Purwins 1995** (Phys. Lett. A 203:33) — parameter bumps act as
  attractive/repulsive centers for dissipative solitons. **Bode 1997** (Physica D
  106:270) — front position obeys an ODE forced by the local parameter *gradient*;
  smooth gradients = smooth forces. Seams-as-force-fields is house physics.
- **Nishiura's program is a complete predicted phenomenology for our seams.**
  Yuan–Teramoto–Nishiura 2007 (PRE 75:036220), Nishiura–Teramoto–Yuan–Ueda 2007
  (Chaos 17:037104), Nishiura–Teramoto–Yuan 2012 (CPAA 11:307, 2-D spots): at bump/
  jump heterogeneities, traveling pulses/spots exhibit **penetration, rebound,
  pinning, oscillatory bound states**, organized by unstable saddle solutions
  ("scattors") living AT the defect; jumps also create **heterogeneity-induced
  ordered patterns (HIOPs)** — genuinely new stationary/oscillatory states localized
  at the interface. Outcome switches are near-discontinuous in parameter/incidence
  angle near criticality. In 2-D, spots additionally **slide along** jump lines.
- **Rigor for the pinning window:** van Heijster, Doelman, Kaper & Nishiura 2010
  (Nonlinearity 24:127) — in the 3-comp FHN model a parameter jump pins fronts inside
  an explicitly computable window of jump heights; van Heijster et al. 2018 (JDDE
  31:153) extend to smooth heterogeneities: pinned states persist, softened. So:
  small mismatch = transparent seam; medium = sticky/oscillatory; large = fence.
  Width smooths but does not remove the effect.
- **Wave-block:** Lewis & Keener 2000 (SIAM JAM 61:293) — a wave entering a less
  excitable region fails to propagate beyond a threshold contrast (geometry-dependent).
  Seams can silently one-way-block activity even when both bulks support it.
- **Optics of seams:** Zhabotinsky, Eager & Epstein 1993 (PRL 71:1526) — chemical
  waves crossing a speed interface obey **Snell's law refraction** and show total
  internal reflection. Expect refraction of wave trains and moving-blob trajectories
  at oblique seam incidence.
- **Ecology = patchy RD at scale.** Shigesada–Kawasaki–Teramoto 1986 (Theor. Popul.
  Biol. 30:143): alternating patches set invasion speed; propagation FAILS when bad
  patches exceed critical width. Keitt–Lewis–Holt 2001 (Am. Nat. 157:203, 364 cites):
  bistable invasion fronts **pin at habitat gradients** — species range borders ARE
  pinned fronts. Maciel & Lutscher 2013 (Am. Nat. 182:42): correct edge matching can
  make *density discontinuous* at an interface (flux continuous, density jumps by a
  behavior-dependent factor) — interface conditions are a modeling CHOICE with
  macroscopic consequences. Smith et al. 1997 (Science 276:1855): **ecotones generate
  divergent selection and novelty** — empirical support for seams as productive zones.
- **Turing-side theory of heterogeneity:** Page–Maini–Monk 2003/2005 (Physica D):
  spatially varying parameters localize patterns and create new dynamics (including
  oscillations) near parameter boundaries. Kozák–Gaffney–Klika 2019 (PRE 100:042220):
  with piecewise kinetics, instability is a LOCAL property; the jump acts as an
  effective BC for each side. Krause et al. 2019–2022 (WKBJ program, J. R. Soc.
  Interface 17:20190621; Phil. Trans. A 379:20200268; arXiv:2210.10155): for *slowly
  varying* heterogeneity there is a local dispersion relation (space = frozen
  parameter); validity requires gradients "not too sharp" — sharp seams host modes
  with no homogeneous counterpart.
- **Blob-specific bonus:** Parra-Rivas, Gomila, Matías & Colet 2013 (PRL 110:064103)
  — dissipative soliton + pinning site + drift = **excitable unit** (saddle-loop):
  a blob held at a seam under bias can fire. Seams can turn blobs into spiking
  elements.

### STEAL / WARNING → our plan

- **STEAL (the big one):** the seam-behavior menu is already catalogued:
  {penetrate, rebound, pin, oscillate, slide-along, block, refract, host-new-states}.
  Use it as the *assay checklist* for patchworld M1: build one seam, throw one moving
  blob at it at several incidence angles and mismatch levels, and classify which of
  the eight behaviors occur. This is a known-physics validation, not exploration.
- **STEAL:** treat seam-localized states (HIOPs) as expected FIRST-CLASS fauna.
  If a blob-like object forms ON the seam, that is Nishiura's predicted class —
  a feature (seam-dwellers / membrane species), and a publishable connection.
- **STEAL:** the pinning window gives our |b_eff| <= 0.03 level-limit a theoretical
  identity: it is the transparent side of a computable pinning threshold. M1 should
  MEASURE the pinning window (mismatch level where a moving blob first sticks) as the
  seam's primary calibration number.
- **WARNING:** near regime boundaries, outcomes flip discontinuously with tiny
  parameter changes (scattor-mediated). Do not average seam behavior over a genome
  ensemble; map it per genome pair.
- **WARNING:** one-way seams are real (wave-block asymmetry): test BOTH crossing
  directions in every seam assay.
- **WARNING (density jump):** even a "transparent" seam generically carries a static
  profile deformation (density offset/kink at the ramp). Detectors tuned to absolute
  u-levels (thr crossings) will misfire in the seam strip; either mask the strip in
  census metrics or use local-background-corrected detection there.

---

## C. Multi-model coupling in scientific computing — buffers, fluxes, and THE D(x) question

### The D(x) discretization question (answered)

Three inequivalent PDEs exist for "diffusion with spatially varying D":

| form | expands to | uniform state u≡u0 | flux | microscopic origin |
|---|---|---|---|---|
| (i) `D(x) lap u` | — | **preserved** (term = 0) | not conservative: `d/dt ∫u = -∫ grad D · grad u ≠ 0` when a structure overlaps the ramp (zero on vacuum) | no clean particle model (velocity-jump limits) |
| (ii) `div(D(x) grad u)` — Fick | `D lap u + grad D · grad u` | **preserved** | conservative, flux `-D grad u` | jump rates set by the BOND (Fick/Stratonovich-like) |
| (iii) `lap(D(x) u)` — Fokker–Planck | `D lap u + 2 grad D · grad u + u lap D` | **NOT preserved** (`u0 lap D ≠ 0` at seams) | conservative, flux `-grad(Du)` | jump rates set by DEPARTURE site (Itô); "ecological diffusion" |

- **van Kampen 1988** (J. Phys. Chem. Solids 49:673): there is NO universal inhomogeneous
  diffusion equation; (i)/(ii)/(iii) arise from different microphysics. The choice is
  physics, not notation. **van Milligen et al. 2005** (Eur. J. Phys. 26:913) and
  **Andreucci et al. 2019** (J. Stat. Phys. 174:469) work out the differences; (iii)
  drives mass out of high-D regions and makes NONUNIFORM steady states from uniform
  ICs. Ecology picked (iii) deliberately to get pile-up in low-motility habitat
  (Garlick–Powell et al. 2011, Bull. Math. Biol. 73:2088).
- **Numerics:** for (ii) the standard is the conservative face-flux stencil with
  **harmonic-mean face diffusivities** (Patankar 1980, ch. 4) — harmonic beats
  arithmetic when D contrasts are sharp; for smooth wide ramps (dx << w) the
  difference is O((dx/w)^2) and negligible.
- **Verified for our system (this review, 1-D check):** on the vacuum u≡u0=-0.7 with
  a tanh D-ramp (amp 1.0, w=8, dx=1): forms (i) and (ii) give identically ZERO seam
  source; form (iii) injects `|u0|·max|lap D| ≈ 4e-3` k1-units — same order as the
  vacuum-mismatch seam source we already computed (2e-3) and would silently violate
  the iso-vacuum design. For a moving blob crossing the ramp, the (i)-vs-(ii)
  difference term `grad D · grad u` peaks at ~1e-2 — 100x below the reaction scale
  (~2.6), but it is a *directed* force on every crossing object, and (i) additionally
  leaks total mass at exactly this order along the seam strip.
- **Consequence for the current engine:** the factory/l0 integrator applies diffusion
  spectrally as `exp(-D k^2 dt)` with SCALAR per-field D — spatially varying D cannot
  enter that exponential at all. Varying Du/Dv/Dw under PoU therefore requires an
  integrator change (split off the D-variation as `div(D grad u) - Dbar lap u` treated
  explicitly, or drop to explicit conservative stencils). Varying only reaction/wiring
  parameters needs NO integrator change (they already live in the explicit RHS).

### Multiphysics coupling lessons

- **Weather/climate physics–dynamics coupling** (Gross et al. 2018, MWR 146:3505):
  ad-hoc blending between schemes generates spurious sources/sinks; conservation must
  be built in by coupling FLUXES, not by averaging tendencies and hoping. Community
  consensus: smooth state blending for regularity, flux matching for budgets.
- **Ocean–atmosphere** (Lemarié–Blayo–Debreu 2015): even for linear diffusion, naive
  (lagged) interface exchanges are inconsistent with the coupled problem unless
  iterated (Schwarz); interface schemes have their own stability theory. This is the
  tax of TWO-solver coupling — avoided entirely by one-grid PoU.
- **Two-regime stochastic RD coupling** (Flegg–Chapman–Erban 2011): coupling two
  *descriptions* of identical chemistry still produces seam-localized density
  artifacts unless the exchange rule is derived, not guessed. Seam artifacts are a
  property of the SEAM RULE, not of the bulk models.
- **Hybrid RANS/LES "grey area"** (Spalart 2009, Annu. Rev. 41:181): the blend region
  simulates a third, unintended model; a named pathology class with a 20-year
  mitigation literature. Same message as XFEM blending elements.
- **Control-theory twins:** gain scheduling (Shamma & Athans 1990) is PoU-over-models
  in time — guarantees only for SLOW scheduling; Takagi–Sugeno fuzzy blending
  (Tanaka & Sugeno 1992): a PoU blend of individually stable models can be UNSTABLE
  without a common Lyapunov function. Certification does not commute with blending.

### STEAL / WARNING → our plan

- **RED FLAG RESOLVED (the discretization):** use **form (ii), conservative flux
  `div(D(x) grad u)`** with harmonic-mean (or, for our smooth wide ramps, arithmetic ≈
  fine) face diffusivities whenever any D varies in space. NEVER form (iii) (it
  breaks iso-vacuum by u0·lapD at every seam). Form (i) `D(x) lap u` is vacuum-safe
  and *looks* fine, but it is non-conservative — it slowly creates/destroys u-mass in
  the seam strip wherever gradients overlap, and our own global memory
  (pde_mass_conservation) says exactly this class of sin compounds. At w=8, dx=0.5–1
  the (i)/(ii) difference is ~1e-2 forcing worst-case — invisible in short runs,
  structural in 10^4-tu runs.
- **STEAL (cheap v1):** for PATCHWORLDS v1, hold Du/Dv/Dw GLOBAL (equal across worlds)
  and PoU only reaction/wiring params. This keeps the spectral integrator exact,
  dodges the whole area-C minefield, and still delivers the interesting physics
  (Nishiura seams are kinetic-parameter seams). Introduce D(x) only in v2 with a
  flux-form operator + mass-budget assay on the seam strip.
- **STEAL:** budget assay = run vacuum-only patchworld (no blobs) for 10^3 tu; any
  drift of ∫u, ∫v, ∫w or any static structure growing at the seam is an
  implementation artifact by definition (both bulks are quiescent). This is the
  weather-model 'spin-up noise' test adapted to us.
- **WARNING (Tanaka–Sugeno):** certified-stable A and B do not certify the s-homotopy
  between them. The 1-D genome-interpolation scan (area A) is mandatory pre-flight.

---

## D. PoU used generatively — composing trained/evolved dynamical systems

### What the field says

- **FBPINNs** (Moseley, Markham & Nissen-Meyer 2021, arXiv:2107.07871; Dolean,
  Heinlein, Mishra & Moseley 2022, arXiv:2211.05560): the PDE solution is BUILT as
  `u(x) = sum_i rho_i(x) u_i(x)` with smooth compactly-supported PoU windows; provably
  an overlapping-Schwarz method. Generative PoU works because ONE global PDE residual
  disciplines all windows. For us the analogue discipline is automatic: the composed
  world is integrated by the actual PDE — seams cannot 'lie', they can only misbehave
  physically.
- **POUnets / parameter-varying neural ODEs** (Lee, Trask et al. 2021, arXiv:2101.11256;
  Lee & Trask 2022, arXiv:2210.00368): dynamical-system parameters represented as
  learned PoU mixtures `theta(x) = sum_i rho_i(x) theta_i` — literally our formula,
  used as a trainable ansatz for hybrid/switching dynamics; the partition itself is
  learnable. Precedent for putting rho(x) into the genome and letting evolution move
  seams.
- **Flow-Lenia** (Plantec et al. 2022, arXiv:2212.07906; Hamon et al. 2025,
  arXiv:2505.15998): the closest ALife relative. Update-rule parameters become a
  spatial FIELD advected with mass ('parameter localization'), so multiple rule-sets
  coexist in one world and MIX where creatures meet; the mixing zones are where the
  novel ecosystem dynamics concentrate. Key difference: their theta(x) moves with
  matter (Lagrangian), ours is static geography (Eulerian). Both are spatial PoU over
  update rules; nobody has done the static-geography version in an RD dissipative-
  soliton system — that is our gap.
- **NCA grafting** (Catrina et al. 2026, arXiv:2605.13630; also multi-texture NCA
  work): spatially compositing independently trained NCA genomes on one grid; seams
  heal because each genome is homeostatic. Weak but direct 'compose-then-run' precedent.
- **Ecotone biology** (Smith et al. 1997, Science): natural transition zones are
  engines of divergent selection — evolution exploits seams. Supports the
  'PoU as evolve-v3 merge operator' idea: place elites side by side and let selection
  own the seam.

### STEAL / WARNING → our plan

- **STEAL:** cite FBPINN/POUnet as the formal frame: PATCHWORLDS = additive-Schwarz
  composition where the 'solver' is the physics itself. Also gives the natural
  generalization (learnable/evolvable rho(x)) for evolve-v3.
- **STEAL (framing for writeup):** Flow-Lenia's authors explicitly motivate parameter
  localization as THE enabler of multi-species open-ended evolution. Our static-
  geography PoU is the complementary experiment (species meet across a fixed ecotone
  rather than carrying their rules). Position it as such; the comparison is novel.
- **WARNING:** in Flow-Lenia, interesting != safe: mixing zones also breed rule-sets
  that outcompete via the mixing dynamics itself (seam exploits). In ecotone-evolution
  runs, guard the fitness function against seam-parasites (score inside patch cores,
  not on seams, at least initially).

---

## Synthesis — does the literature change the implementation?

Yes, in three concrete ways; otherwise it validates the plan.

1. **Diffusion operator (area C).** If/when any D varies in space, the equation must
   be written `div(D(x) grad u)` in conservative flux form. `D(x) lap u` silently
   violates conservation in the seam strip; `lap(D(x) u)` violates iso-vacuum. The
   current spectral integrator cannot host D(x) at all → v1 should hold D global and
   PoU only kinetics/wiring (no integrator change, no artifact class).
2. **Certify the homotopy, not the endpoints (areas A+C).** Blending-element disease
   + Tanaka–Sugeno: the seam strip runs a third model `theta(s)`, s∈[0,1]. Mandatory
   cheap pre-flight: 0-D/1-D scan of the straight-line genome interpolation for
   death/cancer/Turing crossings before any 2-D patch run; if it crosses, either
   widen the seam is NOT a fix — reroute the path (nonlinear PoU: blend in a
   reparametrized space that detours) or accept and study the seam belt as its own world.
3. **Seams are dynamical objects (area B).** Ship the M1 seam assay with the known
   phenomenology as checklist: {penetrate, rebound, pin, oscillate, slide, block
   (both directions!), refract, HIOP formation}, measure the pinning window
   (calibrates our |b_eff|-style level limit), and mask the seam strip in absolute-
   threshold census metrics.

**Recommendation: modified PoU on one grid.**
- Naive PoU (blend everything incl. vacuum-moving params, D(x) lap u): rejected —
  ghost-force analogue + conservation leak.
- Interface matching / two-solver coupling: rejected — imports nonlinear transmission
  -condition craft, conservative-interpolation machinery, and consistency/stability
  theory (Lemarié) that one-grid composition makes unnecessary.
- **Modified PoU** = one grid, one flux-form operator, PoU on vacuum-safe wiring,
  iso-vacuum-constrained activator params (ghost-force removal), wide smooth rho
  (w >> max(tail length, w-halo range 4–20 px ⇒ w ≳ 32–48 px at dx=1), homotopy
  pre-flight, seam assay + seam-strip masking. This inherits the a/c-blending
  optimality results and the WKB 'local dispersion relation' regime, and every
  listed failure mode has a named test.

**Confidence:** High on C (multiple independent primary sources + our own numerical
check). High on B (house lineage + Nishiura + rigorous pinning results). Medium-high
on A (mature fields, standard results). Medium on D (young literature, few systems).

**Method note.** Serper/Google was unavailable (no API key); coverage built from
arXiv API + Crossref + primary pages. Cite-counts from Crossref. Two sources
(Patankar interface-mean details; Spalart grey-area) cited from standard-reference
knowledge with DOIs verified; specific page-level claims there should be spot-checked
if quoted verbatim in a publication.
