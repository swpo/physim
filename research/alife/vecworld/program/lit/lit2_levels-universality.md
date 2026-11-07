**Literature lens: levels of description, universality and effective theories (for the PhySim block-world architecture)**

V = VERIFIED (I read the relevant part). M = MEMORY (not opened; for these, only the DOI and title were checked against Crossref).

**1. Key works and what they show**

- **Anderson, P.W. (1972). "More Is Different."** Science 177:393. https://doi.org/10.1126/science.177.4047.393 [V, pp. 393–394]
  - Reductionism holds, but constructionism does not: "The ability to reduce everything to simple fundamental laws does not imply the ability to start from those laws and reconstruct the universe."
  - Constructionism "breaks down when confronted with the twin difficulties of scale and complexity."
  - The mechanism for new laws at each level is broken symmetry: the laws are "not repealed, but broken."
- **Simon, H.A. (1962). "The Architecture of Complexity."** Proc. Am. Philos. Soc. 106:467. https://homes.cs.washington.edu/~ztatlock/599z-17sp/papers/complexity-simon-62.pdf [V]
  - Near-decomposability has two parts: (a) in the short run, each subsystem behaves nearly independently of the others; (b) in the long run, each depends on the others "in only an aggregate way."
  - Lower levels carry the fast, high-frequency dynamics; higher levels carry the slow ones.
  - A "restricted alphabet" of building blocks (the ninety-odd elements) generates unbounded variety. This is Simon's version of constructive universality.
- **Simon, H.A. & Ando, A. (1961). "Aggregation of Variables in Dynamic Systems."** Econometrica 29:111. https://doi.org/10.2307/1909285 [M] — the formal version for block-dominant linear systems.
- **Wilson, K.G. (1983). "The renormalization group and critical phenomena"** (Nobel lecture). Rev. Mod. Phys. 55:583. https://www.nobelprize.org/uploads/2018/06/wilson-lecture-2.pdf [V]
  - Repeated coarse-graining drives the free energy toward a fixed point "independent of details of the system at the atomic level." This explains why very different systems share critical exponents.
  - Departures from the fixed point that grow under iteration are the relevant directions.
  - Kadanoff's block-spin Hamiltonians generate all local couplings, ordered by how local they are.
- **Kadanoff, L.P. (1966). "Scaling laws for Ising models near Tc."** Physics 2:263. https://doi.org/10.1103/PhysicsPhysiqueFizika.2.263 [M]
- **Appelquist, T. & Carazzone, J. (1975). "Infrared singularities and massive fields."** Phys. Rev. D 11:2856. https://doi.org/10.1103/PhysRevD.11.2856 [M] — heavy fields decouple, except through renormalized couplings and power-suppressed terms.
- **Georgi, H. (1993). "Effective Field Theory."** Annu. Rev. Nucl. Part. Sci. 43:209. https://doi.org/10.1146/annurev.ns.43.120193.001233 [M]
- **Manohar, A. (2018). "Introduction to Effective Field Theories"** (Les Houches lectures). https://arxiv.org/abs/1804.05863 [V, sections 3–4 and 7]
  - Low-energy physics is insensitive to short-distance physics only if its inputs are measured at low energy. If the high-energy inputs are fixed instead, low-energy quantities become sensitive to them (proton mass ∝ m_t^(2/27)).
  - "Symmetry restrictions from the high-energy theory feed down."
  - A symmetry violated at high energy shows up as higher-dimension operators: baryon-number violation at dimension six gives a very long proton lifetime.
  - One high-energy theory yields several EFTs depending on the setting (QCD gives χPT, HQET, NRQCD, SCET).
  - The lectures cite Appelquist–Carazzone for decoupling.
- **Laughlin, R.B. & Pines, D. (2000). "The Theory of Everything."** PNAS 97:28. https://pmc.ncbi.nlm.nih.gov/articles/PMC26610/ [V]
  - A protectorate is a stable state of matter whose generic low-energy properties are fixed by a higher organizing principle "and nothing else."
  - The Josephson and quantum Hall quanta are exact, and would stay exact "even if the Theory of Everything were changed."
  - "One learns little about the atomic structure of a crystalline solid by measuring its acoustics."
  - The Standard Model may itself be such a low-energy phenomenology, from which little about deeper physics can be inferred until experiments fall outside its region of validity.
  - They describe "a hierarchy of Theories of Things."
- **Batterman, R. (2002). *The Devil in the Details*.** Oxford University Press. https://doi.org/10.1093/0195146476.001.0001 [M], checked via **Palacios, P. (2024). "Intertheory Relations in Physics,"** Stanford Encyclopedia of Philosophy. https://plato.stanford.edu/entries/physics-interrelate/ [V]
  - Universality is physics' version of multiple realizability.
  - Emergence is tied to singular limits (the thermodynamic limit, the renormalization group).
  - Critics argue that finite systems suffice.
- **Machta, B.B., Chachra, R., Transtrum, M.K. & Sethna, J.P. (2013). "Parameter Space Compression Underlies Emergent Theories and Predictive Models."** Science 342:604. https://arxiv.org/abs/1303.6738 [V]
  - Hopping model of diffusion: observed after one step, the Fisher information matrix (FIM) is the identity, so every microscopic parameter is equally visible.
  - Observed after t steps, growth rate and drift become easier to measure, diffusion harder, and higher moments harder still, "each with a higher negative power of t."
  - Ising model: the RG-relevant directions are exactly the FIM eigenvalues that do not shrink under coarsening.
  - FIM eigenvalues are spread roughly geometrically.
- **Kadanoff, L.P. & Martin, P.C. (1963). "Hydrodynamic equations and correlation functions."** Ann. Phys. 24:419. https://doi.org/10.1016/0003-4916(63)90078-2 [M] — hydrodynamic variables are conserved densities, and transport coefficients are integrals of correlation functions.
- **Zwanzig, R. (1961).** Phys. Rev. 124:983. https://doi.org/10.1103/PhysRev.124.983 and **Mori, H. (1965).** Prog. Theor. Phys. 33:423. https://doi.org/10.1143/PTP.33.423 [M] — removing the fast variables leaves a memory kernel plus noise.
- **Deng, Y., Hani, Z. & Ma, X. (2025). "Hilbert's sixth problem: derivation of fluid equations via Boltzmann's kinetic theory."** https://arxiv.org/abs/2503.01800 [V, abstract] — a rigorous chain from hard spheres to the Boltzmann equation to Euler and Navier–Stokes–Fourier. Getting from particles to fluid goes through an intermediate kinetic level.
- **Isobe, M. (2008). "Long Time Tail of the Velocity Autocorrelation Function in a Two-Dimensional Moderately Dense Hard Disk Fluid."** Phys. Rev. E 77:021201. https://arxiv.org/abs/0801.4094 [V, abstract] — in 2-D the Green–Kubo diffusion coefficient diverges logarithmically (the "2D long-time-tail problem").
- **E, W. & Engquist, B. (2003). "The heterogeneous multiscale methods."** Commun. Math. Sci. 1:87. https://doi.org/10.4310/CMS.2003.v1.n1.a8 [M] — a macro solver queries micro simulations for the constitutive data it lacks.
- **De las Cuevas, G. & Cubitt, T.S. (2016). "Simple universal models capture all classical spin physics."** Science 351:1180. https://arxiv.org/abs/1406.5955 [V]
  - The 2-D Ising model with fields is universal: its low-energy sector reproduces any classical spin model's spectrum, configurations and partition function, with polynomial overhead.
  - They describe this as "an inversion of the usual renormalisation group flow": a fine-graining rather than a coarse-graining.
- **Cubitt, T., Montanaro, A. & Piddock, S. (2018). "Universal quantum Hamiltonians."** PNAS. https://doi.org/10.1073/pnas.1804949115 [V, overview]
  - The quantum analogue of the above. They state explicitly that this is "a very different notion of 'universality' from that of universality classes."
  - Universality requires that the couplings can be varied individually.
- **Gonda, T., Reinhart, T., Stengele, S. & De les Coves, G. (2024). "A Framework for Universality in Physics, Computer Science, and Beyond."** Compositionality 6(3). https://arxiv.org/abs/2307.06851 [V, abstract and introduction]
  - Universality is the top element of a simulation preorder.
  - Universality combined with negation implies unreachability, such as uncomputability.
  - Universal spin models cannot be finite.
- **Gu, M., Weedbrook, C., Perales, A. & Nielsen, M.A. (2009). "More really is different."** Physica D 238:835. https://doi.org/10.1016/j.physd.2008.12.016 [M] — macroscopic properties of computationally universal lattice models can be undecidable.
- **Cotler, J., Hongler, C. & Hudcová, B. (2025). "Self-replication and Computational Universality."** https://arxiv.org/abs/2510.08342 [V, abstract]
  - They build a Turing-universal cellular automaton that cannot sustain non-trivial self-replication.
  - The cost of encoding a computation into the dynamics is part of any universality claim.
- **Rosas, F.E. et al. (2024). "Software in the natural world: A computational approach to hierarchical emergence."** https://arxiv.org/abs/2402.09090 [V]
  - Informational closure: I(Z_t; Z_{t+1}) = I(X_t; Z_{t+1}), i.e. knowing the micro state adds nothing to predicting the macro state.
  - Computational closure: coarse-graining commutes with building the ε-machine.
  - Causally closed levels exist if and only if the causal states are strongly lumpable.
- **Koch-Janusz, M. & Ringel, Z. (2018). "Mutual information, neural networks and the renormalization group."** Nat. Phys. 14:578. https://arxiv.org/abs/1704.06279 [V] — learn a block's coarse variable H by maximizing I(H; E) with the distant environment E (a buffer zone is excluded). This recovers the relevant degrees of freedom and the Ising critical exponent.

**2. Implications for designing levels, coupling and agent access**

*What makes a level a level.* The literature converges on four properties:
1. **Scale separation** (Simon; Appelquist–Carazzone; Mori–Zwanzig).
2. **Closure:** the level predicts itself as well as the micro level would (Rosas; Simon–Ando).
3. **Compression:** only a few stiff or relevant parameter combinations matter (Wilson; Machta).
4. **Variables set from below:** which variables the level has is fixed by the deeper level's conservation laws and broken symmetries (Anderson; Kadanoff–Martin; Laughlin–Pines; Manohar).

The fourth matters most for design. A generic RNN block has no conserved quantities, so it has no slow modes and nothing universal emerges from it.

*Channels from deep to shallow.* The deeper level can show through at the shallow level in six ways:
- (a) The values of a few constants, such as transport coefficients and renormalized couplings. These can be measured but not derived.
- (b) Which symmetries and conservation laws hold.
- (c) Power-suppressed corrections, and rare events that are forbidden at leading order (proton decay at dimension six).
- (d) Fluctuations and memory: noise amplitude and memory kernels.
- (e) Probe resolution: as the probe's scale approaches the deep scale, the FIM moves from a few stiff directions toward the identity (Machta).
- (f) Interventions on deep parameters: shallow constants do move when deep inputs change (Manohar's m_t example).

A true protectorate closes (a) through (d) almost exactly. Only (e) and (f) remain.

*How constructive and emergent universality differ formally.*
- **Emergent universality is a contraction.** A coarse-graining map acts on the space of theories. A universality class is the basin of a fixed point. Its invariants are the number of relevant directions, the symmetries and the dimension. Information about the micro level is destroyed.
- **Constructive universality is an embedding.** One model U simulates every target in a class through an encoding, with bounded overhead, reproducing the target's low-energy sector (De las Cuevas–Cubitt; Cubitt et al.; Gonda et al.). It is a fine-graining.
- **They compose.** A constructive deep level can produce many emergent upper levels (different phases), and each of them hides it. This is Anderson's asymmetry: reduction holds, but construction is intractable and can even be undecidable (Gu et al.).
- **Two kinds of constructive universality need to be kept apart:**
  - *Parameter-programmed:* universal Hamiltonians need couplings set site by site.
  - *State-programmed, with a fixed law:* Simon's alphabet, chemistry built on fixed QED, the Rule 110 automaton.

  The lead's "the Standard Model and QED build everything" is the state-programmed kind.
- **The distinction is relative to level.** Laughlin and Pines suggest the Standard Model may itself be emergent, so one level can be emergent from the level below and constructive for the level above.

*Consequence for the proposed architecture.* In physics, levels are descriptions of the same degrees of freedom (macro = Φ(micro)), not separate systems. If each h_i is an independent hidden state, the proposal gives Simon-style coupled modules or a heterogeneous multiscale method, not levels of description. Recommendations:
- Make each upper state mostly supervenient, h_{i+1} ≈ Φ_i(h_i), plus a small autonomous residual whose size is measured.
- Make the upward map g a narrow bottleneck that carries only aggregates.
- Make the downward map g′ act as control parameters, boundary conditions or sources for the deeper block, not as arbitrary injection of state.
- Run the deeper block for many substeps per shallow step.

**3. Design principles and measurable quantities**

1. **Scale-separation ratio** ε_i = τ_relax(i) / τ_step(i+1), taken from the Jacobian spectra. This works as a difficulty knob.
2. **Closure gap** C_i = I(h_i(t); z(t+1)) − I(z(t); z(t+1)), with z = Φ_i(h_i) (Rosas). Also measure the commutation error ‖Φ(F_i(h)) − F_{i+1}(Φ(h))‖.
3. **Memory length:** how long the shallow-level memory kernel takes to decay, in shallow steps.
4. **Visibility spectrum:** the FIM of each instrument's outputs with respect to the deep-block parameters, computed by autodiff, as a function of the instrument's resolution and duration. The number of eigenvalues above the noise floor is the number of "visible deep dimensions." Check that the relevant eigenvalues do not shrink under coarsening.
5. **Relevance check (RSMI):** confirm that the designed shallow observables are the ones with maximal mutual information with the distant environment.
6. **Universality test:** swap the deep block for one with the same relevant parameters. Shallow-level predictors should transfer; deep-probing tasks should not.
7. **Constructive reach:** count the distinct shallow-level regimes reachable by varying the deep state under a fixed law, and record the encoding overhead.
8. **Instrument pricing:** price instruments by resolution, so that access deepens with investment. Score deep understanding by counterfactual predictions under interventions on deep parameters, not by recovering parameter labels.

**4. Pitfalls**

- **Pseudo-levels:** without scale separation and closure, the world is one large RNN and the task becomes system identification rather than science.
- **Leakage:** a wide upward map g makes the deep state directly readable. A strong downward map g′ makes the shallow law depend on micro details, which destroys universality.
- **Perfect protectorates:** the deep level can become unidentifiable in principle. Held-out deep tasks are then unfair unless some instrument escapes the protectorate. Check identifiability (item 4) before scoring.
- **2-D hydrodynamics:** transport coefficients may not exist (logarithmic divergence), which is exactly PhySim's dimension. Closure there may need nonlocal or memory terms.
- **Singular limits:** emergent laws hold only in the limits N→∞ and ε→0. Finite blocks show crossovers instead (Batterman).
- **Learned blocks:** fits to Lenia or Flow-Lenia can match trajectories but miss conservation laws or symmetries, and so land in a different universality class. Flow-Lenia's mass conservation should be enforced by the architecture.
- **Undecidability:** constructive universality brings undecidability with it (Gu et al.; Gonda et al.), so keep evaluation tasks in decidable regimes.
- **Universality is not self-replication** (Cotler et al.). A constructive deep block does not guarantee life-like entities.
- **Criticality:** near a critical point, scale separation fails even though universality persists.

**5. Open questions**

- Should level states be supervenient or autonomous, and how large an autonomous residual is acceptable?
- Do bidirectional couplings preserve renormalization fixed points? Is there an RG for coupled-level RNNs?
- How can the deep level be made constructively universal while the tasks stay tractable?
- Should Φ be specified by the designer, or discovered as the closure-optimal coarse-graining? If discovered, the agent's levels and the designer's may differ.
- Does an information-theoretic cap on access correspond to a physical cost of coupling an instrument?
- How should "depth of understanding" be scored: by information gained per unit of instrument cost, or by accuracy on deep interventions?
- Can each block be built to be emergent from the block below and constructive for the block above (Laughlin and Pines' "hierarchy of Theories of Things")?

Downloaded sources are in /tmp/claude-0/-home-user/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/lit2/levels/