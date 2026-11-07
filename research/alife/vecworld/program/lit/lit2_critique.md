**Critique of the hierarchical block world: the case against, the case for, and recommended design principles**

**Verdict.** As written, the architecture gives each level its own hidden state h_i, a generic law f_i and generic maps g, g′. That produces coupled subsystems, not levels of description. Most sampled worlds would have one of two faults: levels that are not really levels, or a task that reduces to identifying a hidden driver. The architecture still contains a good design as a special case. With constraints, its modularity becomes a decisive advantage over hand-built PDE worlds, and so does the designer's exact knowledge of the hidden state.

**(a) Coupled blocks or coarse-grainings?**

*Against:*
- Every closure and universality result in the surveys assumes the macro state is a function of the micro state, Z = f(X). This covers Wilson's RG, Rosas 2024, Atay, Israeli–Goldenfeld, Shalizi–Moore and Mori–Zwanzig.
- With autonomous h_{i+1}, shallow constants are free parameters of f_{i+1}, not functions of the deep parameters. Reduction is therefore impossible by construction: the agent can never derive viscosity from collisions, as Manohar's m_p ∝ m_t^{2/27} illustrates. "Science of depth" collapses into inferring a hidden driver.
- Universality is decreed, not earned. Swapping the deep block tests nothing if the shallow law was written directly.
- A coordinate block is closed only if its incoming input can be predicted from its own past (Barnett–Seth). A generic g leaks.

*For:*
- The family already contains the right subfamily: f_{i+1} ≈ Φ_i(h_i) plus a residual.
- Coupled models are how multiscale computation is actually done. In the heterogeneous multiscale method (HMM: E–Engquist) and in equation-free methods (Kevrekidis et al. 2003), a macro solver calls micro simulators on small patches.
- This saves compute, because the deep level is simulated only where needed.
- It also gives a natural instrument mechanism: deep patches appear where the agent probes.

*Recommendation:* make the default h_{i+1} = Φ_i(h_i) ⊕ r_{i+1}. Φ_i is fixed, local and many-to-one, and the residual's share of variance is reported. Autonomous blocks become a declared exception, used when the intent is an explicit hidden driver.

**(b) Emergent versus constructive universality**

The levels survey's formalisation is sound and can be built:
- **Emergent universality** is a contraction: a fixed point with few relevant directions.
- **Constructive universality** is an embedding: a fixed law whose states can be prepared to encode targets.

*Against:* neither property can be certified for a learned block, since verifying computational universality is generally undecidable. Within one regime the two pull in opposite directions: constructive needs deep detail to matter, emergent needs it not to. They coexist across regimes. Israeli–Goldenfeld show Rule 110 coarse-grains both to a 63-state CA and to the trivial rule 0.

*How to build them:*
- **Constructive deep blocks:** a fixed law with a zoo of stable localised excitations (Lenia solitons, defects) whose compositions produce the shallow regimes. Measure *constructive reach*: the number of distinct closed shallow laws reachable by preparing deep states under one law, plus the encoding overhead.
- **Emergent upper levels:** hard-wire equivariance (lumpability under a group, per Atay) and conservation laws. Verify by swapping deep blocks within one symmetry and conservation class and checking that the shallow law transfers.

**(c) Direction of inter-level flow**

| Coupling | What the agent gets |
|---|---|
| Deep drives shallow only | The deep level can be identified in principle but not controlled, so only correlational science of the depths |
| Shallow drives deep only | The deep level is invisible and irrelevant |
| Both ways | Needed for experiments, but strong loops synchronise the levels and merge them |

- **What each direction should carry** (following Ellis and Haken's slaving): upward maps carry aggregates. Downward maps carry parameters, constraints and boundary conditions, never injected state.
- **Agent actions:** in the supervenient design, shallow actions must be *lifted* into deep perturbations, as in equation-free methods. That lifting map is non-unique and is itself a design choice.
- **Closure trades against depth:** Rosas 2024 (VERIFIED) shows a closed level is optimally controlled by macro interventions alone. That is exactly why a fully closed top level gives no handle on the deep levels.
- **Composability:** require each block to be input-to-state stable (ISS) with a declared gain, and require loops to satisfy a small-gain condition (Jiang–Teel–Praly). Cascades of contracting systems stay contracting (Lohmiller–Slotine); feedback needs explicit bounds.

**(d) Can the deep levels be learned from the top?**

*Against:*
- Under coarsening, the Fisher-information (FIM) eigenvalues of irrelevant directions shrink with powers of t (Machta, VERIFIED).
- A protectorate makes the deep law unknowable from inside its regime (Laughlin–Pines). A good universal shallow level is uninformative about the deep one by design.
- A high-dimensional chaotic deep level cannot practically be reconstructed from shallow history. Eckmann–Ruelle show that dimension estimates from N points cannot exceed about 2·log10 N. So "hiding by mixing plus noise" is real and can be quantified, as the deep Kolmogorov–Sinai entropy against the upward channel's capacity.

*For:* this is the right difficulty structure, provided routes down are designed in:
- resolution ladders, where the FIM approaches the identity as probe scale approaches deep scale;
- leak regimes: bifurcation lines, rare events, processes forbidden by symmetry, quench defects;
- interventions on deep parameters through downward ports.

*Must-haves:*
- Define "deep parameters" as a small set of physical conditioning inputs to the block. FIM taken with respect to network weights is dominated by reparametrisation symmetries and counts nothing physical.
- Separate estimating the deep state (Takens-style filtering) from discovering the deep law, and score only the latter.

**(e) Agent access and scoring**

- **Explicit gating** is reproducible, but it encodes the designer's ontology, so the agent may learn the gate instead of the physics.
- **Preferred:** physical instruments the agent builds. Examples are metastable amplifiers (as in the cloud chamber) and probes at a scale the agent chooses. Each couples through a port with declared capacity, resolution, cost and back-action.
- **Measure** with designer-side quantities: leak per level, depth gain G_L, and expected information gain (EIG) per level.
- **Score:**
  - Stratify held-out experiments by *required depth*: the deepest level a designer oracle needs in order to come within tolerance of the full oracle. Report accuracy per stratum.
  - Add consilience: two independent channels must agree on a deep constant (Perrin).
  - Ask the agent to predict where the shallow law breaks down.
  - Never reward EIG directly. Alchemy shows that revealing information is not the same as using it.

**(f) Practical risks**

- **Learned blocks:**
  - Rollouts drift or explode over long horizons (Mordvintsev; PDE-Refiner).
  - Learned rules are not unique.
  - A block that loses a conservation law lands in a different universality class.
  - Agent interventions push blocks out of distribution, so emulator artefacts become exploitable physics.
  - The ML survey found no faithful long-horizon emulation of Lenia or Flow-Lenia.
- **Composability:** blocks trained separately see different input distributions once coupled.
- **Compute:** with scale ratio s per level in 2-D plus time, cost multiplies by about s³ per level, so three levels at s = 8 cost about 10⁸ times the shallow level. Mitigations:
  - use 2–3 levels;
  - simulate deep levels as HMM-style patches;
  - start with known PDE or CA families with known invariants;
  - admit learned blocks only after they pass certificates.

**Ranked design principles**

1. **Supervenience by default.** Each upper state is a fixed, many-to-one Φ of the level below plus a measured residual.
2. **Symmetries and conservation laws as hard constraints in deep blocks.** These are what make shallow laws universal and transferable.
3. **Typed, narrow ports.** Upward: aggregates through a noisy, finite-capacity channel. Downward: parameters, boundary conditions and lifted actions. Loops must satisfy small-gain.
4. **A visibility certificate for every world.** It holds the FIM spectrum with respect to physical deep parameters for each instrument tier, the closure gap and leak per level, and the depth gain G_L. Reject worlds where the deep level is trivially readable, or where it cannot be identified for the held-out tasks.
5. **Designed leak regimes and resolution ladders** as the only routes down.
6. **Physical, costed instruments with back-action.** Use gating for diagnosis only.
7. **Scoring by required-depth strata, consilience and breakdown prediction.**
8. **Certificates for learned blocks:** at least 10 times the training horizon, spectral fidelity, invariants, and adversarial interventions.
9. **Calibrate every estimator on a linear-Gaussian family first.**

**Three most important open questions**

1. How large a residual or leak keeps a level both universal and probeable? Map whether agents can still do science at the shallow level, at the deep level, or both, as a function of leak and scale ratio.
2. Can constructive universality be turned into a measurable world property, constructive reach under a fixed law, without making evaluation undecidable or intractable?
3. With two-way coupling and agent back-action, which definition of depth holds up when blocks are composed: graph distance, capacity-weighted distance, or the level the oracle requires?

**Survey claims that look wrong or unsupported**

- **cross-level-control misstates Rosas Theorem 1.** Theorem 1 makes causal and informational closure equivalent, not computational closure. Theorem 2 says spatial causal closure implies computational closure, not the reverse (Counterexample 4), and the implication fails for spatio-temporal coarse-grainings (Counterexample 5). emergence-closure has this right but leaves out "spatial".
- **emergence-closure's "P·A^N = B·P³" is garbled.** Israeli–Goldenfeld's condition (eq. 1) is P·f_A^T = f_B·P.
- **levels-universality overstates "a generic RNN has no conserved quantities, so … nothing universal."** Universal amplitude equations arise without conservation near instabilities (Cross–Hohenberg). Slow modes need a conservation law, a continuous symmetry, or tuning near an instability.
- **levels-universality misreads Isobe.** The tail decays slightly faster than 1/t, consistent with 1/(t·√ln t), so the diffusion coefficient diverges like √ln t, not ln t. It is also of little relevance here, because transport coefficients are inputs in designed PDE blocks.
- **probing-depth: "transfer entropy per edge is a hard budget by the data-processing inequality" is wrong.** Transfer entropy is not a channel capacity, and it can be zero while information flows (Ay–Polani). Use directed information or interventional flow instead.
- **probing-depth and cross-level-control overstate "any upward coupling makes the deep level reconstructable".** This holds in principle for low-dimensional deterministic systems, but not in practice for high-dimensional, chaotic, noisy blocks (Eckmann–Ruelle).
- **ml-multilevel's clock ratios of 2–8 are not evidence of enough scale separation.** They come from ML models fitted to data, not from closure in physics.
- **cross-level-control mismaps Kim's "physical closure" onto "no down-coupling".** The two are different notions.
- **probing-depth misreads Barato–Seifert.** The bound is the dissipation of a process whose current has precision ε, not the cost of measuring that current.
- **emergence-closure overstates "exact closure only with zero coupling".** Its own next bullet gives exceptions.
- **levels-universality drops the conditions on "iff strongly lumpable".** The result needs spatial coarse-grainings and an irreducible, aperiodic ε-machine (Rosas Theorem 3).

**Sources I checked or added** (all others are as cited in the surveys)

- Rosas et al. 2024, "Software in the natural world: a computational approach to hierarchical emergence," arXiv:2402.09090, https://arxiv.org/abs/2402.09090. VERIFIED: Theorems 1–3 and the section on control.
- Machta, Chachra, Transtrum, Sethna 2013, "Parameter space compression underlies emergent theories and predictive models," Science 342:604, https://arxiv.org/abs/1303.6738. VERIFIED.
- Israeli & Goldenfeld 2006, "Coarse-graining of cellular automata, emergence, and the predictability of complex systems," PRE 73:026203, https://arxiv.org/abs/nlin/0508033. VERIFIED: eq. 1.
- Gonda, Reinhart, Stengele, De les Coves 2024, "A framework for universality in physics, computer science, and beyond," Compositionality 6(3), https://arxiv.org/abs/2307.06851. VERIFIED.
- Cotler, Hongler, Hudcová 2025, "Self-replication and computational universality," arXiv preprint, https://arxiv.org/abs/2510.08342. VERIFIED: abstract.
- Isobe 2008, "Long time tail of the velocity autocorrelation function in a two-dimensional moderately dense hard disk fluid," PRE 77:021201, https://arxiv.org/abs/0801.4094. VERIFIED: abstract.
- Pasqualetti, Zampieri, Bullo 2014, "Controllability metrics, limitations and algorithms for complex networks," IEEE TCNS 1:40, https://arxiv.org/abs/1308.1201. VERIFIED: abstract.
- Eckmann & Ruelle 1992, "Fundamental limitations for estimating dimensions and Lyapunov exponents in dynamical systems," Physica D 56:185, https://archive-ouverte.unige.ch/unige:92420. VERIFIED: abstract, via search excerpt.
- Kevrekidis, Gear, Hyman, Kevrekidis, Runborg, Theodoropoulos 2003, "Equation-free, coarse-grained multiscale computation: enabling microscopic simulators to perform system-level analysis," Commun. Math. Sci. 1:715, https://projecteuclid.org/euclid.cms/1119655353. VERIFIED: abstract, via search.
- Jiang, Teel, Praly 1994, "Small-gain theorem for ISS systems and applications," Math. Control Signals Systems 7:95, https://doi.org/10.1007/BF01211469. Bibliography verified; content MEMORY.
- Lohmiller & Slotine 1998, "On contraction analysis for non-linear systems," Automatica 34:683, https://doi.org/10.1016/S0005-1098(98)00019-3. MEMORY.
- Cross & Hohenberg 1993, "Pattern formation outside of equilibrium," Rev. Mod. Phys. 65:851, https://doi.org/10.1103/RevModPhys.65.851. MEMORY.
- Haken, *Synergetics: An Introduction*, Springer (slaving principle). MEMORY.