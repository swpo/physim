# Q3. Which properties of natural science can the framework exhibit?

For the lead, 9 Nov 2026. Paths: `P/` = `/home/user/physim/research/alife/vecworld/program/`, `V/` = `/home/user/physim/research/alife/vecworld/vw1/`, `R/` = `/home/user/evalwork/vecworld/program/roadmap/`. New closed-form check: `R/checks/q3_hydro_scaling.py` and `.json` (6 CPU-seconds). Costs are one CPU thread at 128² (`P/inventory/WORLDS.md`); new worlds are unmeasured. New citations: VERIFIED (web search this session) or MEMORY.

## Answer in brief

1. **Almost the whole list fits.** Our certificates are the theories' own quantities under other names (section 1). Quantum mechanics, reversible Hamiltonian mechanics and true limits do not fit (section 5).
2. **Our worlds have no tested reference law.** In gliders, vortices and the membrane a low score can mean a weak agent, a weak certificate or no law to find. A textbook world supplies the level-k law, its error and the certificate values.
3. **Theory gives three kinds of answer.** Exact zeros (conservation, exchangeable counts, fluctuation theorems) calibrate estimators. Rates (1/b in block size b, N^(−1/2) in population N, ε in timescale ratio) calibrate dials. Breakdowns (vortex merger, criticality, extinction) test whether an agent knows where its theory stops.
4. **New check.** Under the stationary law, the closure ceiling of block sums in a diffusive world does not improve with block size. For prepared macroscopic states the deficit falls as 1/b. The hydrodynamic limit is a property of the reference law, not of the map (section 3).
5. **Scoring discovery** needs a theory predictor as a new reference, and transfer items under a compute cap (section 4).
6. **Build first** (section 7): a conserved lattice with a hidden free energy, a count lattice with selection, clean vortices, Ising with block spins, a two-timescale world. They calibrate; agents will recognise them, so they should not be the exam.

## 1. Dictionary

| ours (source) | the theory's name for it |
|---|---|
| exact morphism onto a level whose law is the identity (`V/note/CATEGORY.md` §3) | conservation law |
| automorphism of level 0; its orbit map is strongly lumpable (Atay, in `P/lit/lit2_emergence-closure.md`) | symmetry and symmetry reduction |
| metric defect δ against a declared law (Def. 7) | the limit theorem's error term |
| closure defect Γ and ceiling c(h) (Def. 8), split into what level-k history recovers and what it cannot | unresolved flux: memory kernel plus orthogonal noise (Mori-Zwanzig) |
| defect propagation e(t+1) ≤ K e(t) + δ (Prop. 5d); the horizon where c crosses ½ | Lyapunov growth; predictability time |
| nats charge, half the squared input in noise units (`P/track2/EXAM.md` §3.1) | Girsanov cost, the cost in KL control; for a Langevin force, the work it would do on a free particle, divided by 4kT (derived here) |
| Fisher spectrum per level (`vw.fisher`; `R/Q2_difficulty.md` §3) | sloppiness; relevance under renormalisation |
| `stack` with `stride`, iterated; `refine` with a defect | a renormalisation step; a deeper theory under an effective one |

Missing on our side: irreversibility per level, the KL divergence between forward and time-reversed level-k path laws. For memoryless maps it can only fall as k rises (data processing).

## 2. Catalogue

**1. Conservation laws and symmetries.** *Level 0:* any; mass in Flow-Lenia (drift 10⁻¹⁴), ∫e in CIPS, mass and momentum in lattice Boltzmann. *Map:* totals and block sums. *Law:* totals are constant and block sums obey a continuity equation, both exactly; only the flux law is approximate. Symmetry and conservation are separate objects here: fed vortices are Euclidean-equivariant yet circulation drifts (`WORLDS.md` §1-2), because noisy dissipative laws have no Noether theorem. We exhibit this already: closure and local-law encoders learn a mass-like block variable unprompted (R² up to 0.995 with block mass; `P/README.md`, round 4). *Exam adds:* a hidden invariant, such as a conserved mixture of channels. *Discovery:* skill on that statistic stays at 1 at every horizon while data-only skill decays.

**2. Hydrodynamic limits and transport.** *Level 0:* conserved lattices with local noisy exchange: the linear ring (`vw.lingauss`, closed form); a Ginzburg-Landau lattice with a hidden on-site potential V (new); lattice Boltzmann (1.8 ms/step). *Map:* block sums of size b, time in units of b². *Law:* nonlinear diffusion with D(ρ) = mobility/χ(ρ), χ being the static variance per site (Guo-Papanicolaou-Varadhan); fluctuations of relative size b^(−1/2). Lattice Boltzmann: Navier-Stokes with viscosity (τ − ½)/3 (MEMORY). *Certificates:* section 3. *Exam adds:* a hidden function that collapses to one macroscopic function; the Einstein relation ties static fluctuations, relaxation and response. *Discovery:* predict how a large prepared profile relaxes, from stationary data plus pushes that reach other densities.

**3. Mass action, population dynamics, selection.** *Level 0:* integer counts per site with reactions and hopping (new; expected near Ising's 0.21 ms/sweep). Instances: Moran replacement with hidden fitnesses; Gray-Scott kinetics, which puts a particle level under the inventory's Gray-Scott field. *Map:* site counts, then global frequencies. *Law:* counts in a well-mixed site are exactly lumpable by exchangeability, a certified zero for Γ. As site size N grows, frequencies follow mass-action or replicator equations with Gaussian corrections of order N^(−1/2) (Kurtz). Stoichiometry fixes the noise covariance, so fluctuations reveal mechanism. Closed forms (MEMORY): Price's identity at every tick; fixation probability (1 − r^(−i))/(1 − r^(−N)) for i copies of relative fitness r. *Exam adds:* a level-2 law with a known predictable fraction. We lack one: at 128² the oracle says 51-56% of the kind-share change in fed vortices is predictable, and a linear level-2 predictor reaches none of it even given the true selection coefficient (`P/track1/vortex128/results/summary.json`, `decisions.closure_128`). *Discovery:* the fate of a rare type never seen in the lab; noise at another N.

**4. Quasi-particles.** *Level 0:* 2D Navier-Stokes. Setting gain k and decay μ to zero in `P/track1/vortex_world/vortex_jax.py` leaves it, with the exact-nats stirring channel (2.4 ms per native step; needs a new initial law; untested). *Map:* the existing vortex list. *Law:* Kirchhoff's point-vortex equations: Hamiltonian, integrable for three vortices, chaotic for four (Aref). Error of order (core/separation)²; like-signed vortices merge near core/separation 0.3 (MEMORY). *Certificates:* the object-view ceiling as a function of that ratio; `commutation_error` against the Kirchhoff law measures δ directly. *Exam adds:* an interaction law between objects, object-level invariants and a predicted breakdown; gliders offer none. *Discovery:* the lab shows pairs; the exam asks about quadruples and mergers.

**5. Renormalisation, universality, sloppiness; phase transitions and order parameters.** *Level 0:* heat-bath Ising or Potts (0.21 ms/sweep). *Map:* block-spin majority, stacked; magnetisation. *Law (MEMORY):* near T_c = 2/ln(1+√2), block statistics depend on the couplings only through reduced temperature times b and field times b^(15/8); other directions decay. Susceptibility diverges with exponent 7/4; domains grow as time^(1/2), or time^(1/3) if conserved. *Certificates:* Fisher eigenvalues along irrelevant directions shrink per level at known rates (Machta, in `P/lit/lit2_levels-universality.md`). We have such spectra for gliders, without a reference (`R/Q2_difficulty.md` §3). Input effect per nat peaks at T_c. The ceiling is high only because the world is slow, the artefact `R/Q1_worlds.md` §1 found. *Exam adds:* universality as transfer (a predictor fitted on one hidden lattice must work on another of its class), and regime shift (lab above T_c, exam below). *Discovery:* data collapse at sizes 2L and 4L; T_c located from one side. *Weakness:* the exact answers are asymptotic, and 128² shows crossovers.

**6. Memory.** *Level 0:* any linear-Gaussian world (closed form); a heavy particle in an oscillator bath; two-scale Lorenz-96 (new, negligible cost). *Map:* projection on slow variables. *Law:* a generalised Langevin equation whose kernel equals the autocovariance of its noise. *Certificates:* the split of the one-step leak into memory and residual, already in `ClosedForms.closure` (`V/vw/lingauss.py`). In the conserved ring, history recovers about 40% of the Markov deficit (section 3). *Exam adds:* a timescale ratio ε as an exact dial; Markov fits at fine sampling return wrong constants (Pavliotis-Stuart, in `P/lit/lit2_probing-depth.md`). *Discovery:* skill as a function of allowed history follows the closed-form curve.

**7. Chaos and predictability.** *Level 0:* gliders (twin variance doubles every 2.3 ticks, `EXAM.md` §1), four point vortices, Lorenz-96. *Law:* errors grow as e^(λt), so the horizon is (1/λ) ln(tolerance/initial error). *Certificates:* the tick where c(h) crosses ½. *Exam adds:* beyond the horizon the right answer is the invariant measure. *Discovery:* spread matches error at every horizon, and the horizon moves by the predicted logarithm when observation noise changes.

**8. Thermodynamics and fluctuation relations.** *Level 0* must be reversible with respect to a Gibbs measure: heat-bath Ising, the Ginzburg-Landau lattice, Langevin particles with symmetric forces. Gliders, vortices and the membrane are not. *Map:* block densities, and work when the input couples to an observed variable. *Law:* fluctuation-response; Jarzynski's and Crooks's relations, exact at any driving speed (MEMORY); out of equilibrium, the violation of fluctuation-response equals the dissipation (Harada-Sasa). *Certificates:* `vw.nats.shift_llr` is already the path log-ratio these theorems concern; the irreversibility measure of section 1. *Exam adds:* constraints that hold whatever the mechanism. *Discovery:* predict the reversed protocol's work distribution from forward runs.

**9. Intervention under an information limit; back-action.** *Level 0:* any world with a nats budget. *Law:* with budget C, no policy shifts the mean of a statistic f by more than inf over β of [log E₀ exp(β(f − E₀f)) + C]/β (E₀: no input), which is sd(f)·√(2C) for Gaussian f (Donsker-Varadhan, MEMORY; Gaussian case in `EXAM.md` §3.2). Control with a KL cost is linearly solvable (Todorov). Feedback extracts at most kT of work per nat measured (Sagawa-Ueda). *Exam adds:* control items (`P/CRITIQUE.md` §5) with an exact optimum to normalise by. *Back-action is absent:* our observation port reads without disturbing. To exhibit it, make observation an input: an illumination channel charged in nats.

**10. Effective theories and their breakdown.** *Construction:* `refine` with a declared defect (`R/Q2_difficulty.md`, option G). *Instances with known corrections:* particles under Gray-Scott, defect N^(−1/2); a selection front whose speed 2√(sD) is lowered by a term in 1/ln²N that no affordable N removes (Brunet-Derrida); vortex merger. *Certificates:* defects compose (`CATEGORY.md` Prop. 11c). *Exam adds:* items stratified by distance to the breakdown. *Discovery:* the agent's spread widens where the theory fails, which the energy score already pays for.

## 3. New check: what the hydrodynamic limit says about our ceiling

World: the conserved linear ring of the pooling pilot (`P/track1/DESIGN.md` §2.3), 8 blocks of b sites, closed form; it reproduces the pilot's block-sum ceilings (0.981, 0.949, 0.916). Macroscopic time is s = Dτ/b². The world is linear and one-dimensional; world 1 of section 7 would test whether the result generalises.

| | b = 8 | 16 | 32 | 64 |
|---|---|---|---|---|
| stationary law: ceiling at s = 0.05, whole level-1 past | 0.922 | 0.929 | 0.932 | |
| stationary law: the same, present value only | 0.877 | 0.883 | 0.887 | |
| prepared profile (two longest waves; per-site variance 1, fluctuations 2.5-4.2): deficit 1 − c at s = 0.05 | 0.0236 | 0.0124 | 0.0063 | 0.0031 |

- **Block size is not a closure dial under the stationary law.** The ceilings collapse onto one curve in s (0.93, 0.93 and 0.97 at s = 0.05, 0.2 and 0.8). Equilibrium fluctuations are nearly white at every scale, so larger blocks resolve no more of them.
- **The limit theorem appears only for prepared states,** where the deficit halves with each doubling of b. In such a world, exams that start from the burnt-in law sit where the effective law is weakest. Prepared-state items (`EXAM.md` §1, type P) are where theory separates from data.
- **Fluctuation-response at level 1 holds only for pushes spread evenly over a fibre** (b = 16, s = 0.05). The passive level-1 correlation predicts the response exactly for the Markov-projection lift of a block push, to 1.3% for a block-uniform push, to 20% for one site at a block centre and to 58% at a block edge. For a push inside one block it predicts zero; the true response is 27% of the block push's. This qualifies `R/Q2_difficulty.md` §4: linearity is not enough for fluctuations to show the response. Experiments carry new information below block scale.

## 4. What "discovering the theory" means in scored terms

- **Theory predictor T.** The level-k effective law with constants fitted from the lab budget, never running level 0. In a textbook world it is exact up to a known error. T joins climatology, data-only D, simulate-to-train and the oracle.
- **Transfer cells,** where D fails by construction: scale (size or block ×2 to ×16), regime (densities, temperatures or amplitudes outside the lab's stationary range), response (a push's effect from passive data), composition (pairs in the lab, quadruples in the exam).
- **Theory ratio** on those cells: (agent − D)/(T − D), in oracle-normalised energy skill.
- **Compute cap.** The frozen predictor (`EXAM.md` §1) gets less compute than one level-0 rollout at exam scale. Brute simulation is then unaffordable on scale-transfer cells, and the effective law is the only route.
- **Consilience.** One constant from two channels, scored as cross-prediction.

## 5. What the framework cannot express, or distorts

- **Quantum mechanics.** Levels are classical Markov kernels and observation is a passive readout: no incompatible observables, no entanglement. Only classical probe-disturbance trade-offs can be built.
- **Reversible Hamiltonian mechanics.** The information budget needs noise where inputs enter; deterministic levels have infinite KL (`EXAM.md` §3.3). Noise destroys energy conservation, time reversal and integrability (soliton invariants decay). We get stochastic thermodynamics with a bath, not mechanics.
- **Limits.** Thermodynamic, continuum and ε → 0 limits become 128² and finite steps. Transitions become crossovers, and the continuum equation is itself an effective theory of the code.
- **Fundamental law and explanation.** Level 0 is public: what can be discovered is the effective law, hidden parameters and, under Q2's options, hidden structure. Scores see predictions, so a derivation earns nothing unless a transfer item makes it pay.
- **Rare events.** Fixation, nucleation and large deviations lie below what 64-member energy scores resolve; they need event-count scores.
- **Closed loop.** Certificates are defined for open-loop programs (`CATEGORY.md` §5), so feedback results can be examined but not yet certified.

## 6. Where round 6 would change the shortlist

World numbers are those of section 7.

- **Bias map on two more worlds.** If closure-trained encoders find slow variables where nothing is conserved (vortices, membrane; `WORLDS.md` §1), entry 1's reading weakens, and world 1 becomes the positive control.
- **Slot encoders.** If they fail on gliders, world 3 moves to rank 2: it separates a failing method from a world without clean objects.
- **Vortex exam pilot.** If the hidden selection coefficient is worth under 0.05 at level 2, world 2 is the diagnostic: its theory gives the predictable fraction at 30 individuals. If it is worth 0.1 or more, world 2 calibrates a result we will lean on.
- **Foundry and difficulty ladder.** A foundry pass rate under 1% makes textbook ports the main near-term supply of certified worlds. If depth alone is no dial, as Q2 predicts, they supply the regime-shift items.
- **Agent environment.** Run world 1 first. If no agent beats D on its transfer cells, the exam format is the bottleneck.

## 7. Five textbook worlds, in build order

Ranked by exactness of the answers and by how doubtful the calibrated thing is in our record, against build cost.

| rank | world | exact answers | calibrates |
|---|---|---|---|
| 1 | **Conserved lattice with hidden potential V** (new; the nonlinear ring). Gaussian bond-flux noise gives flux inputs exact nats; an Euler step keeps the Gibbs measure to O(dt) | conservation; D(ρ) from χ(ρ); the curves of section 3; fluctuation-response; work relations | closure ceilings and band gates, the block view, prepared-state items. Entries 1, 2, 6, 8, 9 |
| 2 | **Count lattice** (new): Moran selection first, Gray-Scott kinetics second. Inputs through a matched Gaussian channel (`EXAM.md` §3.3) | zero closure defect for counts; replicator law with N^(−1/2) noise; fixation probabilities; front-speed correction | level-2 selection claims; a hidden sub-level with known defect. Entries 3, 10 |
| 3 | **Clean vortices** (a parameter setting of the existing solver; lattice Boltzmann as alternative) | point-vortex law and invariants, chaos at four vortices, merger | trackers and learned object views. Entries 4, 7 |
| 4 | **Ising with block spins** | T_c, exponents, which directions are relevant | Fisher spectra per level; universality as transfer. Entry 5 |
| 5 | **Two-timescale world** (two-scale Lorenz-96; a linear bath is expressible in `vw.lingauss` today) | memory kernel; averaging error in ε | history-length cells, horizons, defect accounting under `refine`. Entries 6, 7, 10 |

Each is one CPU study with its own checker, as the vortex and membrane ports were. None needs the GPU budget.

Agents know these systems from training, so a textbook world tests recognition and application. Use them for calibration and as the control arm: an agent that fails on world 1 is failing at the exam format, not at science. Exam-grade versions hide the family inside a public grammar (Q2's option C), or couple textbook parts through coarse signals, which preserves exactness (`CATEGORY.md` Prop. 12c): composites with exact answers that appear in no textbook.

## References (new to the project record)

- Guo, Papanicolaou, Varadhan, Commun. Math. Phys. 118:31-59, 1988. VERIFIED (abstract); the explicit D-χ form is MEMORY.
- Kurtz, J. Appl. Probab. 7:49-58, 1970, and 8:344-356, 1971. VERIFIED (bibliographic); content MEMORY.
- Harada, Sasa, PRL 95:130602, 2005. VERIFIED (abstract).
- Todorov, "Linearly-solvable Markov decision problems", NIPS 2006. VERIFIED (abstract).
- Sagawa, Ueda, PRL 104:090602, 2010. VERIFIED (abstract).
- Brunet, Derrida, PRE 56:2597, 1997. VERIFIED (abstract).
- Lorenz, "Predictability: a problem partly solved", ECMWF, 1996. VERIFIED (secondary sources).
- Aref, Annu. Rev. Fluid Mech. 15:345-389, 1983. VERIFIED (bibliographic); content MEMORY.
- Statements marked MEMORY in the text are textbook results not checked this session.
