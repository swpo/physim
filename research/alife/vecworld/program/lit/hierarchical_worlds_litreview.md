# Hierarchical block worlds for PhySim: literature review (5 Nov 2026)

Five surveys, an adversarial critique and a citation check. Where a survey and the check or critique disagree, the check and critique win (see their correction lists).

---

## Survey: levels-universality

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
---

## Survey: emergence-closure

# Lens report: closure, coarse-graining and leakage for a multi-level block world

## (1) Key works and what each shows

**Hoel, Albantakis, Tononi (2013).** "Quantifying causal emergence shows that macro can beat micro." PNAS 110(49):19790–95. https://pmc.ncbi.nlm.nih.gov/articles/PMC3856819/ (VERIFIED, read through a fetch summary of the full text)
- The measure is effective information (EI): mutual information between causes and effects when the system is set uniformly into every state (a maximum-entropy intervention). EI splits into determinism minus degeneracy.
- In toy logic-gate systems, a spatial or temporal coarse-graining can have higher EI than the micro level, because it removes noise or degeneracy.
- The result depends on that maximum-entropy intervention choice. Eberhardt and Lee (2022), "Causal emergence: when distortions in a map obscure the territory," Philosophies 7(2):30, criticise this for the later 2017 version of the framework (MEMORY: abstract seen in search only).

**Rosas, Mediano, Jensen, Seth, Barrett, Carhart-Harris, Bor (2020).** "Reconciling emergences." PLOS Comput Biol 16(12):e1008289. https://arxiv.org/abs/2004.08220 (VERIFIED)
- Defines causal emergence, downward causation and "causal decoupling" through an information decomposition (ΦID).
- Gives cheap pairwise criteria. Ψ = I(V_t;V_t') − Σ_j I(X^j_t;V_t') > 0 is *sufficient* for emergence of a feature V. Δ > 0 indicates downward causation. Ψ > 0 together with Γ = 0 indicates decoupling.
- Redundancy pushes Ψ negative, so the criterion can miss real emergence.

**Rosas, Geiger, Luppi, Seth, Polani, Gastpar, Mediano (2024).** "Software in the natural world: a computational approach to hierarchical emergence." arXiv:2402.09090. https://arxiv.org/abs/2402.09090 (VERIFIED; no journal version found)
- For a macro process Z = f(X):
  - The υ-machine is the optimal predictor of Z's future built from X's past.
  - The ε-machine is the optimal predictor built from Z's own past.
- *Causal closure* means the two machines coincide. *Informational closure* means I(Z⃗past; Z⃗future) = I(X⃗past; Z⃗future) at every horizon. The paper proves these two are equivalent.
- *Computational closure* means the macro ε-machine is a coarse-graining of the micro ε-machine. Informational closure implies computational closure, but not the reverse.
- Strongly lumpable coarse-grainings of the causal states give closed levels. Weakly lumpable ones give only computational closure, which breaks when the process leaves its stationary distribution.
- The closed levels form a lattice. A pure-noise component is "closed" but computationally trivial.

**Barnett and Seth (2023).** "Dynamical independence: discovering emergent macroscopic processes in complex dynamical systems." Phys Rev E 108:014304. https://arxiv.org/abs/2106.06511 (VERIFIED, arXiv v2 text)
- Dynamical dependence (DD) is the transfer entropy from micro to macro, conditioned on an environment E: T(X→Y|E) = I(Y_t; X_past | Y_past, E_past). It is unchanged by reparametrisation and it is transitive across scales.
- After a change of coordinates, Y is independent exactly when the causal graph has no edges coming into Y's coordinates (eq. 2.12). The authors use this to build systems with prescribed independent macro variables.
- Linear state-space models give DD in closed form, and an optimiser searches the Grassmannian for the most independent subspace (their "emergence portrait").
- For deterministic continuous dynamics, transfer entropy diverges. Their functional version of independence reduces to invariants of the flow (via Noether), and they suggest injecting small noise.

**Bertschinger, Olbrich, Ay, Jost.** Two works, both MEMORY:
- 2006, "Information and closure in systems theory," in *Explorations in the Complexity of Possible Life*, IOS Press.
- 2008, "Autonomy: an information theoretic perspective," BioSystems 91:331–345.
- The definitions below were VERIFIED only second-hand, through Barnett–Seth §5.1. A system is informationally closed when T(E→Y) = 0. Non-trivial informational closure is NTIC = I(Y_t;Y_past) − I(Y_t;Y_past|E_past).

**Atay, Banisch, Blanchard, Cessac, Olbrich (2016).** "Perspectives on multi-level dynamics." arXiv:1606.05665 (VERIFIED)
- If micro X is Markov and Y = π(X), the one-step leak splits into two parts:
  - I(Y_{t+1}; X_t | Y_t) = I(Y_{t+1}; Y_past | Y_t) + I(Y_{t+1}; X_t | Y_whole past).
  - The first term is the macro's memory (non-Markovianity). The second is information no amount of macro history can recover.
  - So the leak bounds the memory, and closure implies a Markov macro level.
- They also restate Kemeny and Snell's strong-lumpability theorem: a partition is lumpable exactly when the probability of jumping into each block is the same for every state within a block. (Kemeny and Snell, *Finite Markov Chains*, is MEMORY; the theorem was VERIFIED as restated here.)
- A transition matrix that is invariant under a group G yields a lumpable partition.
- Heterogeneity in agents or rules breaks the symmetries and produces macro memory. Markov macro dynamics is "exceptional."
- They give a commutation-error measure δ = sup‖πφ − ψπ‖, which can go to zero only in a limit such as large system size.

**Shalizi and Crutchfield (2001).** "Computational mechanics: pattern and prediction, structure and simplicity." J Stat Phys 104:817–79. arXiv:cond-mat/9907176 (VERIFIED; venue MEMORY)
- Causal states are maximally predictive, minimal and unique.
- Statistical complexity C_μ bounds excess entropy (E ≤ C_μ).
- The control theorem bounds how much a controller can reduce uncertainty about the next symbol by C_μ.

**Shalizi and Moore.** "What is a macrostate? Subjective observations and objective dynamics." arXiv:cond-mat/0303625 (2003, revised 2024) (VERIFIED; the Foundations of Physics version is MEMORY)
- Macrostates are the unique coarsest refinement of what an observer can see that is Markov. They coincide with causal states.
- Observers whose observations are non-Markov "develop instruments" and refine their states until the process becomes Markov.
- Their emergence criterion: the coarse level is a coarse-graining *and* has higher predictive efficiency E/C_μ.

**Wolpert, Grochow, Libby, DeDeo (2014/15).** "Optimal high-level descriptions of dynamical systems." arXiv:1409.7403 (VERIFIED)
- State Space Compression (SSC) chooses the compression map π, the macro dynamics φ and the readout ρ to minimise accuracy cost plus computation cost.
- They warn that transfer entropy between scales of *one* system is biased: the one-step macro→micro transfer entropy is identically zero when the macro is a function of the micro.

**Israeli and Goldenfeld (2006).** "Coarse-graining of cellular automata, emergence, and the predictability of complex systems." PRE 73:026203. arXiv:nlin/0508033 (VERIFIED; the 2004 PRL 92:074105 is MEMORY)
- The exact commutation condition is P·f_A^T = f_B·P, built from supercells of size N and a projection P.
- Rule 146 coarse-grains to rule 128, and rule 128 to itself.
- Rule 110, which is computationally universal, coarse-grains to a 63-state CA (N = 6) and also to rule 0, through "Garden of Eden" patterns that cannot be reached after the first steps.
- Removing *irrelevant* degrees of freedom keeps the complexity class. Removing *relevant* ones can change it.
- There is no small parameter, so approximate coarse-graining is hard.

**Chorin, Hald, Kupferman (2001).** "Non-Markovian optimal prediction." arXiv:math/0101022 (VERIFIED; the PNAS 97:2968 (2000) version is MEMORY, abstract only)
- The Mori–Zwanzig split, with projection P = conditional expectation under the invariant measure, gives a generalised Langevin equation with three terms: a Markov term, a memory integral, and a noise term from the "orthogonal dynamics." The memory kernel is correlations of that orthogonal dynamics (fluctuation–dissipation).
- Under strong under-resolution, the Markov term alone fails over time.
- Related MEMORY items: Lin and Lu (2021, J Comput Phys 424:109864, arXiv:1908.07725), data-driven Mori–Zwanzig and NARMAX models; Pfante et al. (2014, Adv Complex Syst 17:1450007), a comparison of closure criteria; Geiger and Temmel (2014, J Appl Prob 51:1114, arXiv:1212.4375), lumpability and preservation of entropy rate.

## (2) Implications for the block world

- **The proposed blocks are coupled subsystems, not coarse-grainings.** In every work above, the macro level *is a function of* the micro level (supervenience). In the block world each h_i is its own state.
  - The joint state H = (h_1…h_n) is the Markov micro state, and "level i" is a coordinate projection.
  - By Barnett–Seth (2.12), that projection is exactly closed only when the coupling g or g′ into level i is zero. Exact closure by projection therefore means the level is disconnected.
  - Non-trivial closure needs one of two things. Either the incoming coupling depends only on functions of level i's own history (the deep level is slaved, or lumpable with respect to its influence). Or the "level" is defined in rotated coordinates that mix blocks.
- **Downward arrows are real here.** Shallow→deep coupling (g′) is a genuine causal path, unlike the supervenient case where macro→micro transfer entropy is trivially zero (Wolpert; Barnett–Seth). That path is how instruments and interventions can reach the depths. It also means an agent's actions can break closure.
- **Universality ≈ lumpability under symmetry.** If a deep block is equivariant under a group G, its orbit partition is strongly lumpable (Atay Theorem 3.2). Different deep blocks with the same symmetry share one lumped shallow law, which is Rosas's "multiple realisability." This is a direct way to build "universal emergent" high levels and to test universality by swapping the deep block.
- **"Constructive universal" deep levels can still have closed shallow levels.** Rule 110 is the existence proof (Israeli–Goldenfeld).
- **Memory and noise are designable.** Hidden deep levels show up at the shallow level as a memory kernel plus orthogonal noise (Mori–Zwanzig). Atay's identity separates what history can recover from what only deeper access can.
  - A fast, mixing deep block gives a short kernel: near-Markov shallow dynamics with noise.
  - A slow deep block gives a long kernel, which looks like hidden parameters or drift.
  - The ratio of time scales is the dial.

## (3) Quantities to build in (each block world ships its exact values)

Levels run 1 (deepest) to n (shallowest). The agent observes y_t = O(h_n) and takes actions a_t.

1. **Leak into level i:** L_i = I(h_i(t+1); h_{−i}(≤t) | h_i(≤t), a(≤t)). This is Barnett–Seth DD with the agent's actions as the environment.
2. **Memory/residual split:** I(h_i(t+1); h_{−i}(t) | h_i(t)) = M_i + R_i.
   - M_i = I(h_i(t+1); h_i(<t) | h_i(t)) is recoverable from history.
   - R_i is irreducible without deeper access.
3. **Depth gain for the agent:** G_L = I(H(≤t); y⃗_L) − I(y(≤t); y⃗_L), the υ-machine minus ε-machine predictive information over horizon L.
   - This is the maximum reward available from building instruments. Instruments can be scored by the fraction of G_L they recover.
   - Held-out experiments should require part of G_L, otherwise depth is never needed.
4. **NTIC of each level**, to rule out "closed because it is noise."
5. **C_μ, E, entropy rate h_μ and predictive efficiency E/C_μ per level** (Shalizi–Moore emergence criterion).
   - h_μ of y is the scoring floor for a purely shallow agent.
   - C_μ bounds how much control is achievable (control theorem).
6. **Commutation error** δ_T = E‖π(Φ^T H) − ψ(π H)‖ against a declared reference shallow law ψ, plus the Israeli–Goldenfeld exact test for discrete blocks.
7. **Ψ / Δ / Γ** as cheap checks that a shallow feature is synergistic over deep components rather than a copy of one of them.
8. **A linear-Gaussian calibration family.** Every quantity above has a closed form via state-space models (Barnett–Seth). Use it to validate estimators before using neural or Lenia blocks.

**Ways to get closure by construction:**
- Make deep blocks equivariant (lumpability).
- Satisfy P·A^N = B·P³ for discrete blocks.
- Prescribe a causal graph with no edges into a subspace, then rotate coordinates to hide it.
- Use a time-scale separation sized to give a target kernel length.

## (4) Pitfalls

- **Trivial closure:** an iid-noise level is closed (Rosas 2024). Rule 110 → rule 0 is a closed but empty level. Require NTIC > 0 or a non-trivial ε-machine.
- **Closure depends on the distribution of states.** Weak lumpability holds only for some initial distributions, and agent-prepared states leave the stationary distribution. Measure closure under the held-out experimental distribution, not only at stationarity.
- **Deterministic continuous blocks** (PDEs, neural nets) make transfer entropy diverge. Add calibrated noise or finite-resolution observation, and state which one.
- **Hoel's EI depends on the maximum-entropy intervention distribution.** Treat it as one diagnostic, not ground truth.
- **Ψ is only sufficient** and is biased by redundancy.
- **Estimation scales badly:** the lattice of coarse-grainings grows super-exponentially and ε-machines get large. Ship designer-side exact values rather than estimating them.
- **Heterogeneity destroys Markov macro dynamics** (Atay). Small asymmetries in learned blocks will quietly add memory.
- **Exact closure means isolation** (Barnett–Seth 2.12). Aim for small, tuned leak, not zero.

## (5) Open questions

- With two-way coupling there is no supervenience. Is "level" best defined by coordinate blocks, or by the most independent subspaces of the joint H (Barnett–Seth's emergence portrait)? Should the two be designed to coincide or deliberately to differ?
- Approximate closure: which threshold or norm (leak in bits per step, δ_T, or the υ/ε gap) best predicts whether agents can do science at that level?
- Instrument back-action: coupling shallow to deep perturbs the deep level through g′. How should depth gain be scored when measuring changes the measured level?
- How can closure be estimated for trained Lenia or Flow-Lenia blocks? Candidates are neural estimators (Neural Information Squeezer, Zhang and Liu 2022, Entropy 25:26, arXiv:2201.10154, MEMORY) and data-driven Mori–Zwanzig.
- Can kernel length and noise amplitude be read off analytically from the block parameters, so the hiddenness of the depths is a controlled variable of the world generator?

Downloaded sources are in /tmp/claude-0/-home-user/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/lit2/emergence-closure/
---

## Survey: ml-multilevel

**ML architectures for multi-level, multi-timescale dynamics: literature review for the PhySim block-world design**

VERIFIED means I read the relevant part (the full text, or the abstract where marked "abs"). MEMORY means the item was not opened; it is used only for some venues and one paper. Downloaded files are in /tmp/claude-0/-home-user/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/lit2/ml-multilevel/

**1. Key works and what they show**

*A. Multi-timescale recurrent hierarchies*
- [1] Koutník, Greff, Gomez, Schmidhuber 2014, "A Clockwork RNN", ICML (venue MEMORY), https://arxiv.org/abs/1402.3511. VERIFIED.
  - The hidden layer is split into modules with periods T_i = 2^(i-1).
  - Recurrent connections run only from slower modules to faster ones (one-way, top-down).
  - It has fewer parameters and is faster, and beat RNNs and LSTMs on audio generation and TIMIT.
- [2] Chung, Ahn, Bengio 2017, "Hierarchical Multiscale Recurrent Neural Networks", ICLR, https://arxiv.org/abs/1609.01704. VERIFIED.
  - Each layer has a learned binary boundary detector and three operations: UPDATE, COPY and FLUSH.
  - Each layer takes bottom-up input from layer l-1 and top-down input from layer l+1.
  - It is trained with the straight-through estimator plus slope annealing, and finds word-like boundaries without supervision.
- [3] Yamashita, Tani 2008, "Emergence of functional hierarchy in a multiple timescale neural network model", PLoS Comput Biol 4, doi:10.1371/journal.pcbi.1000220. VERIFIED (abs). A functional hierarchy self-organizes from different neuron time constants alone, with no explicit modules.
- [4] Saxena, Ba, Hafner 2021, "Clockwork Variational Autoencoders", NeurIPS (venue MEMORY), https://arxiv.org/abs/2102.09532. VERIFIED.
  - Latent level l ticks every k^l steps (k = 2 to 8). Conditioning is top-down only, with a KL term per level.
  - Slower levels store slower content, and the KL per level tracks the speed of the data (Fig. 8).
  - In a 4-level model the top level's KL is 0.0001 nats (Table 2), so it is effectively unused. The authors say "a 2-level model may be sufficient" for GQN Mazes.
  - Rolling out in latent space beat feeding generated images back in. VTA, which resets the low level whenever the high level ticks, produces sudden jumps.
- [5] Gregor, Papamakarios, Besse, Buesing, Weber 2019, "Temporal Difference Variational Auto-Encoder", ICLR (venue MEMORY), https://arxiv.org/abs/1806.03107. VERIFIED (abs). It keeps belief states, trains on pairs of time points far apart, and can roll out in jumps that skip steps.
- [6] Hafner, Lee, Fischer, Abbeel 2022, "Deep Hierarchical Planning from Pixels" (Director), NeurIPS (venue MEMORY), https://arxiv.org/abs/2206.04114. VERIFIED. A manager picks a discrete latent goal every K = 8 steps and a worker pursues it. This is a hierarchy on the agent side, not the world side.

*B. Bidirectional coupling and modularity*
- [7] Rao, Ballard 1999, "Predictive coding in the visual cortex", Nature Neuroscience 2:79-87, doi:10.1038/4580. VERIFIED (abs). Feedback carries predictions of lower-level activity; feedforward carries only the residual errors.
- [8] Lotter, Kreiman, Cox 2016, PredNet, arXiv / ICLR 2017 (venue MEMORY), https://arxiv.org/abs/1605.08104. VERIFIED (abs). Each layer predicts locally and passes only its errors upward.
- [9] Goyal et al. 2019, "Recurrent Independent Mechanisms", arXiv (ICLR 2021 MEMORY), https://arxiv.org/abs/1909.10893. VERIFIED (abs). Modules evolve almost independently, talk through an attention bottleneck and update only when relevant. This generalizes better when only some factors change.
- [10] Mittal et al. 2020, "Learning to Combine Top-Down and Bottom-Up Signals in RNNs with Attention over Modules" (BRIMs), ICML, https://arxiv.org/abs/2006.16981. VERIFIED.
  - A module at layer l attends over three inputs: bottom-up from l-1 at time t, top-down from l+1 at time t-1, and a null vector.
  - Only some modules activate each step (sparse activation).
  - It is more robust to noise. The authors say modularity is what stops top-down signals from interfering.

*C. Hierarchical latent-variable models and collapse*
- [11] Sønderby et al. 2016, "Ladder Variational Autoencoders", NeurIPS (venue MEMORY), https://arxiv.org/abs/1602.02282. VERIFIED. In a vanilla VAE, the layers above the second were "completely collapsed" onto the prior. The LVAE, with KL warm-up and batch norm, used all five layers.
- [12] Zhao, Song, Ermon 2017, "Learning Hierarchical Features from Generative Models", ICML, https://arxiv.org/abs/1702.08396. VERIFIED. If a stacked hierarchy is trained to optimality, the bottom layer alone reconstructs the data, so the upper layers can be ignored.
- [13] Two deep-hierarchy papers, both VERIFIED (abs):
  - Vahdat, Kautz 2020, NVAE, NeurIPS, https://arxiv.org/abs/2007.03898. Spectral regularization and a residual parameterization of the Normal distributions stabilize deep hierarchies.
  - Child 2021, Very Deep VAEs (ICLR MEMORY), https://arxiv.org/abs/2011.10650. Stochastic depth matters.

*D. Learned coarse-graining and multiscale operators*
- [14] Bar-Sinai, Hoyer, Hickey, Brenner 2019, "Learning data-driven discretizations for PDEs", PNAS 116:15344, https://arxiv.org/abs/1808.04930. VERIFIED (abs). Learned derivative estimates allow grids 4-8x coarser, on 1-D nonlinear PDEs.
- [15] Kochkov et al. 2021, "Machine learning-accelerated computational fluid dynamics", PNAS (volume MEMORY), https://arxiv.org/abs/2102.01010. VERIFIED.
  - Learned corrections inside a solver match baselines run at 8-10x finer resolution per dimension, a 40-80x speedup.
  - Training used 4800-step trajectories with the loss unrolled over 32 steps; tests ran for tens of thousands of steps.
  - It generalizes to new forcings and Reynolds numbers.
  - Metrics: time until correlation drops below 0.95, spectral error, and fraction of runs still stable.
- [16] Um et al. 2020, "Solver-in-the-Loop", NeurIPS, https://arxiv.org/abs/2007.00016. VERIFIED (abs). Training through the solver beats supervised training and gives stable rollouts of several hundred steps.
- [17] Brandstetter, Worrall, Welling 2022, "Message Passing Neural PDE Solvers", ICLR, https://arxiv.org/abs/2202.03376. VERIFIED.
  - The pushforward trick unrolls 2 steps and backpropagates only through the last one.
  - Temporal bundling predicts K steps at once.
  - The paper frames rollout error as a distribution-shift problem and links it to zero-stability, ||A(u+e) - u1|| < κ||e||.
- [18] Lippe et al. 2023, "PDE-Refiner", NeurIPS, https://arxiv.org/abs/2308.05732. VERIFIED. One-step MSE training neglects low-amplitude, often high-wavenumber, modes. Nonlinearity then carries those errors into the dominant modes, and long rollouts fail.
- [19] Sanchez-Gonzalez et al. 2020, "Learning to Simulate Complex Physics with Graph Networks", ICML, https://arxiv.org/abs/2002.09405. VERIFIED (abs). Trained on single steps, it generalizes to thousands of steps; adding noise to the training inputs limits error build-up.
- [20] Three multiscale operator papers:
  - Li et al. 2020, Multipole Graph Neural Operator (NeurIPS MEMORY), https://arxiv.org/abs/2006.09535. VERIFIED (abs). A multi-level graph captures interactions at all ranges in linear time and does not depend on the discretization.
  - Li et al. 2020, Fourier Neural Operator, https://arxiv.org/abs/2010.08895. VERIFIED (abs). Zero-shot super-resolution.
  - Lam et al., GraphCast (Science 2023 MEMORY), https://arxiv.org/abs/2212.12794. VERIFIED. A multi-mesh built from icosahedral meshes of increasing resolution carries long-range information in few message-passing steps.
- [21] Vlachas, Arampatzis, Uhler, Koumoutsakos, "Learning the Effective Dynamics" (LED) (Nature MI 2022 MEMORY), https://arxiv.org/abs/2006.13431. VERIFIED (abs). An autoencoder maps between fine and coarse; an RNN evolves the latent; coupling follows the equation-free approach.

*E. Renormalization group (RG) and deep learning*
- [22] Mehta, Schwab 2014, "An exact mapping between the variational renormalization group and deep learning", arXiv, https://arxiv.org/abs/1410.3831. VERIFIED (abs). The mapping is specific: Kadanoff variational RG to RBMs, shown on the Ising model.
- [23] Lin, Tegmark, Rolnick 2017, "Why does deep and cheap learning work so well?", J Stat Phys, https://arxiv.org/abs/1608.08225. VERIFIED (RG section).
  - RG is feature extraction relative to chosen targets, usually long-wavelength ones.
  - Under b×b block averaging, couplings scale as y_i' = b^(2-2i) y_i, so all but the first few are irrelevant.
- [24] Koch-Janusz, Ringel 2018, "Mutual information, neural networks and the renormalization group", Nature Physics 14:578, https://arxiv.org/abs/1704.06279. VERIFIED. The coarse variable H for a block V is chosen to maximize I(H; E), where E is the environment beyond a buffer B. This recovers the RG flow and the Ising exponent with no prior knowledge.
- [25] Li, Wang 2018, "Neural Network Renormalization Group", PRL 121:260601, https://arxiv.org/abs/1802.02840. VERIFIED (abs). A hierarchical normalizing flow is used. Its inverse maps independent Gaussian latents to configurations, so generation runs as an inverse RG.

*F. Cellular automata, neural CA, Lenia*
- [26] Gilpin 2019, "Cellular automata as convolutional neural networks", PRE 100:032402, https://arxiv.org/abs/1809.02942. VERIFIED (abs). Any CA is a CNN, and the rules can be learned from video.
- [27] Springer, Kenyon 2020, "It's Hard for Neural Networks to Learn the Game of Life", arXiv, https://arxiv.org/abs/2009.01398. VERIFIED (abs). Networks of the minimal 2n+1-layer size rarely converge; overcomplete networks are needed.
- [28] Mordvintsev, Randazzo, Niklasson, Levin 2020, "Growing Neural Cellular Automata", Distill, doi:10.23915/distill.00023. VERIFIED.
  - With naive training, patterns "explode" or "decay" after the training horizon.
  - Training from a pool of past states makes the target pattern an attractor.
  - Damaging states during training produces regeneration.
- [29] Richardson, Antal, Blythe, Schumacher, "Learning spatio-temporal patterns with Neural Cellular Automata", PLOS Comput Biol 2024 (venue from a search result), https://arxiv.org/abs/2310.14809. VERIFIED.
  - A Gray-Scott NCA trained on 1024 steps extrapolates to 2048 steps from an unseen initial condition.
  - Sampling every 32 steps worked best; fine time sampling was unstable.
  - Without a little noise in the data, gradients diverged.
  - Stated limits: purely local rules, learned rules are not unique, and multiscale systems are not handled.
- [30] Two Lenia papers, both VERIFIED:
  - Chan 2020, "Lenia and Expanded Universe" (ALIFE MEMORY), https://arxiv.org/abs/2005.03742. Multi-channel Lenia "approaches a recurrent convolutional neural network".
  - Plantec et al., "Flow-Lenia" (ALIFE 2023 MEMORY), https://arxiv.org/abs/2212.07906. Mass is conserved, and rule parameters become local fields in the dynamics, which allows several species.
- Gap: my searches found no paper that trains a network to reproduce Lenia or Flow-Lenia trajectories faithfully over long horizons. The closest are [26], [29] and Béna et al. 2025, "A Path to Universal Neural Cellular Automata", https://arxiv.org/abs/2505.13058 (MEMORY, not opened).

**2. What this implies for levels, coupling and agent access**

- **The level ordering is inverted relative to ML.**
  - In [1-6], slow, abstract levels sit above fast observations.
  - In physics, and in PhySim's framing, the deep constructive level is fast and fine, and the observed level is slow and coarse.
  - So going deeper is best modelled by the closure and effective-dynamics work [14, 15, 21]. The clockwork models [1, 4] fit levels above the one the agent observes (populations, lineages).
  - Each block should own its dt and grid. Inter-level maps become restriction (fine to coarse pooling, [23, 24]) and prolongation (the coarse state acts as forcing or as a parameter field for the fine level, as in Flow-Lenia's local parameters [30]).
- **Coupling direction.**
  - One-way slow-to-fast coupling [1, 4] is the simplest and most stable.
  - Bidirectional coupling works when it is gated by attention and the upper level is read at t-1 [10]. That makes simultaneous updates independent of update order, which composable blocks need.
  - Predictive coding [7, 8] suggests a principled upward channel: send only what the upper level failed to predict.
- **Universality is irrelevance [23, 24].**
  - Under restriction, most deep detail should die out, and a known few deep parameters should survive as shallow effective parameters (compare the learned corrections in [15]).
  - The rest of the deep state should be reachable only through instruments.
- **Modularity.** Typed ports with an attention bottleneck, a null option and sparse activation [9, 10] make blocks swappable. Operators that work at any resolution [20] let blocks on different grids be joined.

**3. Quantities and design rules to build in**

1. **Information budget per level.**
   - Track KL or mutual information per level [4], and the deep-to-shallow predictive information I(h_deep(t); o(t+τ) | o(≤t)) as a function of τ.
   - Reject a world in which a level carries close to zero (compare 0.0001 nats in [4]).
2. **Universality checks.**
   - RSMI, I(coarse variable; environment) [24], certifies that the shallow level is a good coarse-graining.
   - A relevance spectrum certifies which deep parameters matter: the Fisher-information eigenvalues of shallow observable statistics with respect to deep parameters. A few large eigenvalues means a universal shallow law, and the designer chooses which deep parameters are relevant.
3. **Timescale separation.** Measure autocorrelation-time ratios between levels. Clock ratios of 2-8 worked in [1, 4, 6].
4. **Stability certificate for every learned block.**
   - Estimate zero-stability κ [17].
   - Use the metrics from [15]: time until correlation drops below 0.95, spectral error, and fraction of runs still stable.
   - Check spectral fidelity at all wavenumbers [18].
   - Test at 10x or more of the training horizon [15, 29].
5. **Training recipe.**
   - Use an unrolled or solver-in-the-loop loss [15, 16], the pushforward trick and input noise [17, 19].
   - Train from a pool of past states with damage [28].
   - Sample training data coarsely in time [29] and use overcomplete widths [27].
   - Hard-wire conservation laws [30].
6. **Treat an instrument as a coupling operator.**
   - An instrument maps a deep block to the agent's observation port, with a stated capacity in bits per experiment.
   - Deeper access then means adding operators with higher capacity or finer resolution.

**4. Pitfalls**

- **The hierarchy collapses into one level [4, 11, 12].** In a world generator this shows up two ways:
  - The shallow block is closed on itself, so the deep levels cannot be identified and there is nothing to discover.
  - The shallow block is slaved to the deep levels, so there is no emergent law.
  - Measure 3.1 detects both.
- **Errors grow or the spectrum drifts under distribution shift [17, 18].** Agent interventions are exactly such a shift: they push learned blocks off the states they were trained on. Mitigations:
  - project or clamp states, and conserve invariants;
  - stress-test with adversarial interventions.
- **Emulator artifacts become the physics.** The agent is scored against the emulator, learned rules are not unique [29], and glitches could be exploited.
- **Resetting the lower state when the upper level ticks causes jumps [4]**, and re-encoding observations during rollouts makes errors grow faster [4].
- **Exact discrete rules are hard to learn [27].**
- **"Level" is not intrinsic.** RG coarse-graining is defined relative to chosen observables [23], and the Mehta-Schwab "exact" mapping is narrow [22].

**5. Open questions**

- How do we measure the deepest level's "constructive universality" (a small rule set that builds many shallow phenomena), as opposed to emergent universality (many deep rules giving one shallow law)?
- Should blocks be trained jointly or separately? Co-adaptation may open hidden side channels that break modularity and access limits.
- Long-horizon fidelity of learned Lenia or Flow-Lenia blocks is not established in anything I found.
- Is bidirectional coupling stable when the deep level is fast and chaotic? How much time-averaging should restriction do (the equation-free question raised by [21])?
- Can information-theoretic limits on access be enforced when the couplings are learned, without information leaking through unintended channels?
---

## Survey: probing-depth

# Lens: how science reaches deeper levels from the top, and what limits it

## 1. Key works

**Fluctuations.**
- **Einstein [1]:** a visible particle's mean-square displacement determines Avogadro's number N, through D = RT/(6πηaN).
- **Perrin [2]:** five independent methods gave N between 60 and 68 ×10^22. What settled the reality of molecules was that the methods agreed, not any single value.
- **Kubo [3]:** a system's linear response is fixed by its equilibrium fluctuations. A generalized Nyquist relation ties frequency-dependent friction to coloured noise.
- **Mori [4]:** projecting the dynamics onto chosen variables gives a memory kernel equal to the correlation of the random force. To the observer, an eliminated level shows up as memory plus noise, in a fixed ratio.

**Probes.**
- **Van Hove [5]:** scattering measures the space-time pair correlation function, which becomes long-range near a critical point.
- **Manohar [6]:** a distant observer reads multipole coefficients b_lm ~ c_lm/Λ^l, and finite resolution caps l_max.
  - The short scale can be reached by more precise measurement at long distance, or by cruder measurement at short distance.
  - Coefficients that vanish reveal symmetries.
  - Processes forbidden at low order expose high scales: the proton decay rate goes as M_G^-4.
- **Gordon–Webb–Wolpert [7]:** different shapes can have the same spectrum.

**Amplification.**
- **Wilson [8]:** ions seed drops only above a critical expansion ratio: 1.25 for negative ions, about 1.31 for positive ions. This made single ions visible, and the threshold sorts them by sign.
- **Allahverdyan et al. [9]:** a metastable magnet, tipped by a weak coupling to the measured spin, registers the outcome.

**Dynamics.**
- **Sugihara et al. [10]:** the history of a driven variable carries redundant information about the state of its driver (Takens [11]).
  - Their example: "fish time series can be used to estimate weather, but not conversely."
  - Very strong forcing causes synchrony.
  - Causation is transitive along chains.
- **Liu et al. [12]:** every root strongly connected component of the system's inference graph needs its own sensor.
- **Schreiber [13]:** transfer entropy measures the direction of information flow.

**Irreversibility.**
- **Barato–Seifert [14]:** measuring a current to precision ε costs at least 2k_BT/ε² of dissipation.
- **Martínez et al. [15]:** asymmetry in waiting times gives a lower bound on hidden entropy production, even when no current is visible. The bound is tight only if all nonequilibrium variables are observed.

**Limits.**
- **Gutenkunst et al. [16]:** parameter-sensitivity eigenvalues span more than 10^6. A model whose every parameter was uncertain by more than 50× still predicted well.
- **Machta et al. [17], Transtrum et al. [18]:** argue that this Fisher-information (FIM) hierarchy is why universal and continuum theories exist.
- **Raju et al. [19]:** under coarse-graining, FIM distances along irrelevant directions shrink at rates set by the RG exponents.
- **Gordon et al. [20]:** what the information bottleneck keeps as relevant matches the operators with the lowest scaling dimension.
- **Laughlin–Pines [21]:** "one therefore learns little about the atomic structure of a crystalline solid by measuring its acoustics." The underlying theory is "unknowable until one raises the energy scale sufficiently to escape protection." Yet protected effects (Josephson, quantum Hall) give exact constants.
- **Apgar et al. [22]:** five complementary perturbations identified parameters that no single experiment could.
- **Pavliotis–Stuart and Papavasiliou et al. [23]:** fitting homogenized models to finely sampled data gives wrong parameters, unless the data are subsampled at an interval between the two timescales.

**Leaks.**
- **Touchette [24]:** large-deviation theory refines Gaussian fluctuation theory. My own reading: the tails keep more of the microscopic law than the central limit theorem does.
- **Jarzynski [25]:** free-energy estimates are dominated by rare realizations.
- **del Campo–Zurek [26]:** local symmetry-breaking choices freeze in as defects, with a density set by the quench rate.
- **Har Shemesh et al. [27]:** in Gray–Scott, the Fisher information peaks on the lines where pattern type changes.

## 2. Implications

**Each channel is a design choice.**
- **Fluctuation channel:** needs a finite, stochastic deep level. A deterministic mean-field g closes it.
- **Probes:** need perturbations the agent applies at scales it chooses.
- **Amplification:** needs metastable shallow states the agent can prepare.
- **Irreversibility:** needs a driven deep level.
- **Dynamical channel:** appears automatically whenever upward coupling is deterministic and injective.

**Coupling direction decides what is observable [10,12].**
- **Upward-only coupling:** the deep state can generally be recovered from shallow history when noise is low.
- **Downward-only coupling:** the deep level is invisible.
- **Strong two-way coupling:** synchronizes the levels and merges them.

**Bottleneck.** With coupling only between adjacent levels, everything the agent learns about h_0 has to pass through the trajectory of h_1. Transfer entropy per edge is therefore a hard budget, by the data-processing inequality (MEMORY).

**Define a level by contraction.** A many-to-one, local g plus separated timescales makes the Fisher information about deep parameters decay geometrically with depth [16–19]. A generic RNN block will tend to leak either everything or nothing.

**This fits the lead's framing.** Universal shallow levels expose only a few stiff combinations of deep parameters. Constructive deep levels are blocks with few parameters whose compositions generate everything above them.

## 3. Design principles and quantities

1. **Fisher-information audit.** Use autodiff through the world to get the Fisher information of the observations with respect to each level's parameters θ_i, for each instrument set. The number of eigenvalues above the noise floor is the "reachable depth". Tune basic instruments to reach 1–3 per level.
2. **Information budget.** Track I(h_i; o_{0:T}) with designer-side probes, plus transfer entropy on each edge.
3. **Gated amplifiers.** Add threshold or metastable units to the shallow block. Deep events register only after the agent prepares a unit, and the threshold selects which kind of event registers [8].
4. **Resolution ladders.** Give instruments settings for q, ω, precision and cost, with deep effects suppressed as (scale ratio)^n [6].
5. **Engineered leaks.** Make rare events, critical lines, quench defects and symmetry-forbidden processes the regimes where deep parameters become stiff. Check with the Fisher information that they actually do [27].
6. **Depth score.**
   - Predict the shallow consequences of held-out deep interventions do(θ_i), scored as predictions rather than as parameter values [16].
   - Check consilience: two independent channels must give the same deep constant, as in Perrin's work.
   - Ask for calibrated bounds, for example on hidden dissipation [14,15].

## 4. Pitfalls

- **Takens trap:** with low-noise deterministic coupling, a sequence model can recover the deep state without understanding anything. Add intrinsic deep noise or a many-to-one g.
- **Over-contraction:** held-out tasks may ask for quantities that cannot be identified. Check identifiability first.
- **Synchrony:** strong coupling merges levels.
- **Multiscale fitting bias [23]:** affects the designers' reference predictors as well as the agent.
- **Same spectrum, different structure [7]:** different deep structures can give identical spectra.
- **Weak channels:** some channels give only lower bounds [15], and rare-event channels need exponentially many samples [25].
- **Learned blocks:** blocks trained to reproduce known dynamics (Lenia-like) may lack the structure that makes deep details irrelevant at the top.

## 5. Open questions

- Should information about deep levels decay geometrically per level, or reach the top only through gates?
- Can universality be tested operationally, as the dimension of the set of deep blocks whose shallow statistics are indistinguishable?
- Should instruments be structures the agent builds inside the world, or tools with a cost?
- Are mutual-information estimates in high dimensions reliable enough to score with?
- How do we stop agents from memorizing the signatures of rare regimes?

## Sources (VERIFIED = I read the relevant part, MEMORY = not opened)

[1] A. Einstein (1905) Über die von der molekularkinetischen Theorie der Wärme geforderte Bewegung… Ann. Phys. 17:549. https://doi.org/10.1002/andp.19053220806 MEMORY
[2] J. Perrin (1926) Discontinuous structure of matter, Nobel lecture. https://www.mit.edu/~kardar/research/seminars/motility/PerrinNobelLecture.html VERIFIED
[3] R. Kubo (1966) The fluctuation-dissipation theorem. Rep. Prog. Phys. 29:255. https://doi.org/10.1088/0034-4885/29/1/306 VERIFIED (abstract)
[4] H. Mori (1965) Transport, collective motion, and Brownian motion. Prog. Theor. Phys. 33:423. https://doi.org/10.1143/PTP.33.423 VERIFIED (abstract)
[5] L. Van Hove (1954) Correlations in space and time and Born approximation scattering in systems of interacting particles. Phys. Rev. 95:249. https://doi.org/10.1103/PhysRev.95.249 VERIFIED (abstract, from a search excerpt; the APS page was blocked)
[6] A. V. Manohar (2018) Introduction to effective field theories (Les Houches). https://arxiv.org/abs/1804.05863 VERIFIED (sec. 2, proton decay)
[7] C. Gordon, D. L. Webb, S. Wolpert (1992) One cannot hear the shape of a drum. Bull. AMS 27:134. https://arxiv.org/abs/math/9207215 VERIFIED (abstract)
[8] C. T. R. Wilson (1927) On the cloud method of making visible ions and the tracks of ionizing particles, Nobel lecture. https://www.nobelprize.org/uploads/2018/06/wilson-lecture.pdf VERIFIED
[9] A. E. Allahverdyan, R. Balian, T. M. Nieuwenhuizen (2013) Understanding quantum measurement from the solution of dynamical models. Phys. Rep. 525:1. https://arxiv.org/abs/1107.2138 VERIFIED (abstract)
[10] G. Sugihara, R. May, H. Ye, C. Hsieh, E. Deyle, M. Fogarty, S. Munch (2012) Detecting causality in complex ecosystems. Science 338. https://doi.org/10.1126/science.1227079 VERIFIED (full text)
[11] F. Takens (1981) Detecting strange attractors in turbulence. Lect. Notes Math. 898. https://doi.org/10.1007/BFb0091924 MEMORY
[12] Y.-Y. Liu, J.-J. Slotine, A.-L. Barabási (2013) Observability of complex systems. PNAS 110:2460. https://pmc.ncbi.nlm.nih.gov/articles/PMC3574950 VERIFIED
[13] T. Schreiber (2000) Measuring information transfer. PRL 85:461. https://arxiv.org/abs/nlin/0001042 VERIFIED (abstract)
[14] A. C. Barato, U. Seifert (2015) Thermodynamic uncertainty relation for biomolecular processes. PRL 114:158101. https://arxiv.org/abs/1502.05944 VERIFIED (abstract)
[15] I. A. Martínez, G. Bisker, J. M. Horowitz, J. M. R. Parrondo (2019) Inferring broken detailed balance in the absence of observable currents. Nat. Commun. 10:3542. https://pmc.ncbi.nlm.nih.gov/articles/PMC6684597 VERIFIED
[16] R. N. Gutenkunst, J. J. Waterfall, F. P. Casey, K. S. Brown, C. R. Myers, J. P. Sethna (2007) Universally sloppy parameter sensitivities in systems biology models. PLoS Comput. Biol. 3:e189. https://doi.org/10.1371/journal.pcbi.0030189 VERIFIED
[17] B. B. Machta, R. Chachra, M. K. Transtrum, J. P. Sethna (2013) Parameter space compression underlies emergent theories and predictive models. Science, doi:10.1126/science.1238723. https://arxiv.org/abs/1303.6738 VERIFIED (abstract)
[18] M. K. Transtrum, B. B. Machta, K. S. Brown, B. C. Daniels, C. R. Myers, J. P. Sethna (2015) Sloppiness and emergent theories in physics, biology, and beyond. J. Chem. Phys. 143:010901 (venue MEMORY). https://arxiv.org/abs/1501.07668 VERIFIED (abstract)
[19] A. Raju, B. B. Machta, J. P. Sethna (2018) Information loss under coarse graining: a geometric approach. PRE 98:052112. https://arxiv.org/abs/1710.05787 VERIFIED (abstract)
[20] A. Gordon, A. Banerjee, M. Koch-Janusz, Z. Ringel (2021) Relevance in the renormalization group and in information theory. PRL 126:240601. https://arxiv.org/abs/2012.01447 VERIFIED (abstract)
[21] R. B. Laughlin, D. Pines (2000) The theory of everything. PNAS 97:28. https://pmc.ncbi.nlm.nih.gov/articles/PMC26610/ VERIFIED
[22] J. F. Apgar, D. K. Witmer, F. M. White, B. Tidor (2010) Sloppy models, parameter uncertainty, and the role of experimental design. Mol. BioSyst. 6:1890. https://dspace.mit.edu/handle/1721.1/76208 VERIFIED (abstract)
[23] G. A. Pavliotis, A. M. Stuart (2007) Parameter estimation for multiscale diffusions. J. Stat. Phys. 127. https://arxiv.org/abs/math/0603668; and A. Papavasiliou, G. A. Pavliotis, A. M. Stuart (2009) Maximum likelihood drift estimation for multiscale diffusions. Stoch. Proc. Appl. 119:3173. https://arxiv.org/abs/0806.3248 VERIFIED (both abstracts)
[24] H. Touchette (2009) The large deviation approach to statistical mechanics. Phys. Rep. 478:1. https://arxiv.org/abs/0804.0327 VERIFIED (abstract)
[25] C. Jarzynski (2006) Rare events and the convergence of exponentially averaged work values. PRE 73:046105. https://arxiv.org/abs/cond-mat/0603185 VERIFIED (abstract)
[26] A. del Campo, W. H. Zurek (2014) Universality of phase transition dynamics: topological defects from symmetry breaking. IJMPA 29:1430018. https://arxiv.org/abs/1310.1600 VERIFIED (abstract)
[27] O. Har Shemesh, R. Quax, A. G. Hoekstra, P. M. A. Sloot (2016) Information geometric analysis of phase transitions in complex patterns: the Gray-Scott reaction-diffusion model. J. Stat. Mech. 043301. https://arxiv.org/abs/1512.02077 VERIFIED (abstract)

Downloaded source texts are in /tmp/claude-0/-home-user/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/lit2/deep-access/
---

## Survey: cross-level-control

**Lens: control and observation across levels, and how to structure and measure agent access**

Notation: L0 is the shallow level, where the agent acts and observes, and Lk is deeper. Up-coupling means a deep state appears in the update of a shallower one. Down-coupling is the reverse.

**(1) Key works**

*Structure of control and observation*
- Liu, Slotine, Barabási (2013). *Observability of complex systems*. PNAS 110:2460. https://pmc.ncbi.nlm.nih.gov/articles/PMC3574950 — VERIFIED.
  - The "inference diagram" has an edge i→j when x_j appears in x_i's equation.
  - At least one sensor in each root strongly connected component is necessary.
  - In the nonlinear systems they tested, the sensors chosen from the graph were also sufficient, because symmetries are rare.
- Liu, Slotine, Barabási (2011). *Controllability of complex networks*. Nature 473:167. https://doi.org/10.1038/nature10011 — MEMORY.
  - The minimum number of driver nodes is set by a maximum matching.
- Lin (1974). *Structural controllability*. IEEE TAC 19:201. https://doi.org/10.1109/TAC.1974.1100557 — MEMORY.
  - Controllability is treated as a generic property of the system's graph.
- Pasqualetti, Zampieri, Bullo (2014). *Controllability metrics, limitations and algorithms for complex networks*. IEEE TCNS 1:40. https://arxiv.org/abs/1308.1201 — VERIFIED (abstract).
  - Gramian-based control-energy metric.
  - With a fixed, small number of control nodes, energy grows exponentially with network size (stable symmetric networks).
- Kokotovic & Haddad (1975). *Controllability and time-optimal control of systems with slow and fast modes*. IEEE TAC. https://doi.org/10.1109/TAC.1975.1100852 — MEMORY.
  - If the slow and fast subsystems are each controllable, the full system is controllable for small ε. The converse does not hold.
  - Background: Kokotovic, Khalil, O'Reilly (1986), *Singular Perturbation Methods in Control* — MEMORY.
- Krener & Ide (2009). *Measures of unobservability*. IEEE CDC, pp. 6401–6406. URL not confirmed — MEMORY.
  - Local observability Gramian, which needs only simulation.
  - The reciprocal of its minimum eigenvalue serves as an "unobservability index".

*Limits on information*
- Touchette & Lloyd (2000). *Information-theoretic limits of control*. PRL 84:1156. https://arxiv.org/abs/chao-dyn/9905039 — VERIFIED (abstract).
- Touchette & Lloyd (2004). *Information-theoretic approach to the study of control systems*. Physica A 331:140. https://arxiv.org/abs/physics/0104007 — VERIFIED (full text).
  - Closed-loop entropy reduction is bounded: ΔH_closed ≤ ΔH_open^max + I(X;C). Each bit sensed buys at most one extra bit of control.
  - Perfect observability holds if and only if H(X|C)=0.
  - Controlling a chaotic map needs information that scales with its Lyapunov exponent.
- Tishby, Pereira, Bialek (1999). *The information bottleneck method*. https://arxiv.org/abs/physics/0004057 — VERIFIED (abstract).
- Rosas, Geiger, Luppi, Seth, Polani, Gastpar, Mediano (2024). *Software in the natural world: a computational approach to hierarchical emergence*. https://arxiv.org/abs/2402.09090 — VERIFIED (relevant sections).
  - Theorem 1: informational closure, I(X_past; Z_future | Z_past)=0, is equivalent to causal closure and to computational closure.
  - Closed levels nest in a lattice and link to strong lumpability.
  - Closed levels can be optimally controlled by macro interventions alone.
  - Counterfactual guarantees need full observation.
- Ay & Polani (2008). *Information flows in causal networks*. Adv. Complex Syst. 11:17. https://uhra.herts.ac.uk/id/eprint/162 — VERIFIED.
  - Defines an information flow under intervention.
  - In their example, transfer entropy is zero both for a one-bit exchange between two chains and for no coupling at all. The interventional flow tells them apart.
- Sugihara et al. (2012). *Detecting causality in complex ecosystems*. Science 338:496. https://doi.org/10.1126/science.1227079 — MEMORY.
- Takens (1981). *Detecting strange attractors in turbulence*. LNM 898 — MEMORY.
  - Together: a driven variable's delay embedding reconstructs its driver, but not the other way round.
- Chorin, Hald, Kupferman (2002). *Optimal prediction with memory*. Physica D 166:239. https://doi.org/10.1016/S0167-2789(02)00446-3 — MEMORY.
  - Eliminating variables leaves memory terms (Mori–Zwanzig).

*Experimental design*
- Chaloner & Verdinelli (1995). *Bayesian experimental design: a review*. Stat. Sci. 10:273. https://doi.org/10.1214/ss/1177009939 — MEMORY (only the bibliographic details were checked).
- Rainforth, Foster, Ivanova, Bickford Smith (2024). *Modern Bayesian experimental design*. Stat. Sci. https://arxiv.org/abs/2302.14545 — VERIFIED.
  - Expected information gain (EIG) is I(θ;y|ξ), where θ can be any function of the model parameters; the rest are nuisance.
  - Adaptive design uses incremental EIG.
  - A joint simulator of (θ, y) is all that is needed.
  - Adaptive design can fail badly under misspecification.
  - EIG about parameters is distinct from EIG aimed at predictions.
- Foster, Ivanova, Malik, Rainforth (2021). *Deep Adaptive Design*. ICML. https://arxiv.org/abs/2103.02438 — VERIFIED (abstract).
- Ivanova, Foster, Kleinegesse, Gutmann, Rainforth (2021). *Implicit Deep Adaptive Design*. NeurIPS. https://arxiv.org/abs/2111.02329 — VERIFIED (abstract).
  - Both train design policies in advance using contrastive EIG bounds. The implicit version needs only a simulator with differentiable samples.
- Gandhi, Li et al. (2025). *BoxingGym*. https://arxiv.org/abs/2501.01540 — VERIFIED (abstract).
  - Scores agents' experiments by EIG, and scores their models by how well another agent predicts from the explanation.
  - LLMs struggle on both.

*Measuring control*
- Salge, Glackin, Polani (2014). *Empowerment — an introduction*. https://arxiv.org/abs/1310.1863 — VERIFIED.
  - Empowerment is the channel capacity from n-step actuator sequences to a later sensor state.
- Klyubin, Polani, Nehaniv (2005). *Empowerment: a universal agent-centric measure of control*. IEEE CEC, pp. 128–135 — MEMORY.

*Downward causation*
- Ellis (2012). *Top-down causation and emergence: some comments on mechanisms*. Interface Focus 2:126. https://pmc.ncbi.nlm.nih.gov/articles/PMC3262299 — VERIFIED.
  - Five classes of top-down causation, from algorithmic to intelligent.
  - Higher levels act through constraints, boundary conditions and context.
  - Test: an equivalence class of lower-level states yields the same higher-level outcome.
- SEP, *Emergent Properties*. https://plato.stanford.edu/entries/properties-emergent/ — VERIFIED.
  - States Kim's exclusion premises: supervenience, reality, efficacy, distinctness, physical causal closure. Together these give overdetermination.
- Kim (1998). *Mind in a Physical World*. MIT Press — MEMORY.
- Campbell (1974). "'Downward causation' in hierarchically organised biological systems", in Ayala & Dobzhansky (eds) — MEMORY.
- Hoel, Albantakis, Tononi (2013). *Quantifying causal emergence shows that macro can beat micro*. PNAS 110:19790 — MEMORY.
- Flack (2017). *Coarse-graining as a downward causation mechanism*. Phil. Trans. A 375:20160338 — MEMORY.
- Rubenstein et al. (2017). *Causal consistency of structural equation models*. UAI. https://arxiv.org/abs/1707.00819 — VERIFIED (abstract).
  - Micro and macro models are consistent when they agree on what interventions do ("exact transformations").

*Benchmarks with hidden mechanisms or gating*
- Wang et al. (2021). *Alchemy*. NeurIPS Datasets & Benchmarks. https://arxiv.org/abs/2102.02926 — VERIFIED.
  - A latent causal "chemistry" is resampled each episode.
  - A Bayesian ideal observer scores 284. The two deep-RL agents score 140 and 156, close to the random heuristic's 146.
  - The agents' actions did reveal the latent state (the ideal observer's posterior entropy fell), but the agents did not use it.
  - Failures were diagnosed by granting privileged information step by step.
- Jansen et al. (2024). *DiscoveryWorld*. NeurIPS. https://arxiv.org/abs/2406.06769 — VERIFIED.
  - Hidden properties are read through instruments.
  - In the hard variants the agent must validate an instrument against known samples.
  - Tasks with "novel instruments" are hard for agents.
- Nikulin et al. (2024). *XLand-MiniGrid*. NeurIPS Datasets & Benchmarks. https://arxiv.org/abs/2312.12044 — VERIFIED.
  - Production-rule trees are hidden from the agent, and tree depth is the difficulty dial.
  - Distractor rules create irreversible dead ends that stop brute force.
- Hafner (2022). *Crafter*. ICLR. https://arxiv.org/abs/2109.06780 — VERIFIED (abstract).
  - Agents unlock achievements, which requires deep exploration.
- Denil et al. (2017). *Learning to perform physics experiments via deep reinforcement learning*. https://arxiv.org/abs/1611.01843 — VERIFIED (abstract).
  - Agents learn experiments that reveal hidden mass and cohesion, trading the cost of information against the cost of errors.

**(2) What this implies for the design**

- **The coupling direction decides the access type.** Up-coupling (deep→shallow) is the observation channel; down-coupling (shallow→deep) is the agent's control channel. In the lead's framing, down-coupling is Ellis-style top-down causation. Kim's "physical closure" premise corresponds to no down-coupling: then the agent can watch the depths but never steer them.
- **Structure alone cannot hide anything that matters.**
  - In Liu's inference diagram, any deep level that influences L0 is structurally observable from L0, and for nonlinear blocks that is generically also sufficient (Takens, CCM).
  - A deep level that never feeds L0 is invisible, but it is also irrelevant to scoring.
  - So access limits must be quantitative: channel capacity, noise, coarse-graining, timescale separation (ε) and control energy.
- **Universality is roughly closure.**
  - A shallow level with universal emergent behaviour is an approximately informationally closed coarse-graining: Rosas's closure, Ellis's equivalence classes, multiple realisability.
  - The small leakage away from closure is exactly what lets the agent probe the depths. It should be a per-level design dial.
- **Coupled layers are not the same as levels of description.**
  - Blocks that each have their own hidden state are coupled subsystems.
  - In physics, macro levels supervene on micro levels.
  - Decide which one PhySim wants. If the shallow block should count as a "description" of a deeper one, test how closely it approximates an exact transformation (Rubenstein) or a closed coarse-graining (Rosas).
- **Down-coupling should act as a constraint.** Following Ellis, g′ should modulate parameters or boundary conditions of f_deep (fields, confinement, temperature) rather than overwrite deep states. That is how real apparatus works.
- **Physical versus explicit gating.**
  - Physical gating (instruments built from cross-level coupling):
    - Pro: it reveals none of the designer's intent.
    - Pro: depth then follows from understanding, since an instrument must be calibrated (DiscoveryWorld's validation stage).
    - Con: it cannot be made leak-proof, because of embedding side channels.
    - Con: it is hard to sequence as a curriculum.
  - Explicit gating (XLand-, Crafter-style unlocks):
    - Pro: reproducible and cheap to measure.
    - Con: it encodes the designer's ontology, so the agent may learn the gate rather than the physics.
  - Hybrid: physical channels whose capacity, resolution and energy cost are declared, verified by evaluator-side metrics.

**(3) Concrete principles and measurable quantities**

1. **Declare a level graph for each world.** It has labelled up- and down-channels. At generation time, check structural observability and controllability from L0 using root SCCs and maximum matching.
2. **Make each inter-level map g an explicit channel.** Build it from coarse-graining, quantisation, noise and a timescale ratio ε, with a declared capacity C in bits per step.
   - The data-processing inequality then caps what L0 can learn.
   - For memoryless passive channels, that cap is about T·C over T steps. With feedback, a directed-information bound is needed.
3. **Closure leakage per level:** Λ_i = I(h_{≥i, past}; o_future | o_past). Estimate it as the predictive gain of an evaluator model that is given privileged access to the deep state.
4. **Interventional coupling** between levels (Ay–Polani), computed with do() on the hidden states. Do not use transfer entropy for this.
5. **Empirical Gramians from the agent's ports**, per level: the unobservability index (Krener–Ide) and the control energy (Pasqualetti).
6. **Privileged empowerment over hidden states:** E_i(n) = max I(A^{1:n}; h_i(t+n)). Track how it rises as the agent builds instruments.
7. **Depth profile of the agent's experiment log:** EIG_i = I(θ_i; y_{1:T} | ξ_{1:T}), with the other levels treated as nuisance.
   - Compute it with the evaluator's simulator, using implicit or contrastive bounds.
   - Normalise against a reference designer (a DAD/iDAD policy or an ideal observer).
   - "Depth reached" is the deepest level i whose EIG_i exceeds a threshold.
   - Report separately the depth the experiments revealed (EIG) and the depth the agent used (held-out prediction on experiments sensitive to level i). Alchemy shows these two come apart.
8. **Diagnostic privileged-access ladder** (Alchemy): rerun with level i revealed to locate where the agent fails. Use this for diagnosis, not for scoring.

**(4) Pitfalls**

- Any up-coupling makes the deep level reconstructable in principle. Hiding it by architecture is an illusion.
- Integrating out a level leaves memory (Mori–Zwanzig). An agent with long histories can extract deep information, and trained blocks may carry unintended shortcut channels.
- Passive information measures misreport coupling, so use interventional measures.
- Deep levels can be controllable in principle yet cost exponential energy. Budget for this explicitly.
- Estimates of EIG and empowerment are biased in high dimensions. Report them as bounds.
- EIG about parameters is not the same as predictive value. Keep held-out prediction as the score, and do not reward EIG directly (Goodhart).
- Explicit gates leak the answer.
- If blocks do not supervene on each other, "levels" may just be coupled layers.

**(5) Open questions**

- How should "depth" be defined when the levels form a single SCC because coupling runs both ways? Hop count weighted by capacity, or the EIG threshold above?
- Can trained RNN blocks be pushed toward near-closure (universality) with a tunable leakage?
- What action affordances let an agent build couplings, that is instruments, without the designer listing them in advance?
- Can the timescale ratio ε and the channel capacities produce a physical curriculum that is still controllable?
- How tight are bounds based on directed information once the agent's feedback crosses levels?
---

## Adversarial critique

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
---

## Citation check

Each source was checked against arXiv API metadata, Crossref, and the primary text where noted. The files I downloaded are in /tmp/claude-0/-home-user/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/lit2/citecheck/. Survey keys: LU = levels-universality, EC = emergence-closure, ML = ml-multilevel, PD = probing-depth, CLC = cross-level-control. "Text" means I read the relevant passage.

| Source (survey) | Exists | Year / venue | Description | URL |
|---|---|---|---|---|
| Rosas et al. 2024, "Software in the natural world" (LU, EC, CLC) | Yes | arXiv only (v2, Jun 2024); no journal version found | EC accurate (text). LU: "closed iff strongly lumpable" is accurate, but the closure equation is simplified (C2). **CLC wrong** (C1) | arxiv.org/abs/2402.09090 |
| Israeli & Goldenfeld 2006 (EC) | Yes | PRE 73:026203, correct | Accurate (text): 146→128 (N=3); 128→itself; 110→63-state CA (N=6) and →rule 0 via Garden-of-Eden patterns (N=5, 13). P·A_N = B·P³ is their Eq. 5 | arxiv.org/abs/nlin/0508033 |
| Hoel, Albantakis, Tononi 2013 (EC) | Yes | PNAS 110:19790, correct | Slightly overstated (C4) | pmc.ncbi.nlm.nih.gov/articles/PMC3856819 |
| Eberhardt & Lee 2022 (EC) | Yes | Philosophies 7(2):30, correct | Accurate (targets Hoel 2017) | mdpi.com/2409-9287/7/2/30 |
| Barnett & Seth 2023 (EC) | Yes | PRE 108:014304, correct | Accurate (text) except that the transitivity is a property of dynamical *independence*, not of the DD measure (C7). Eq. 2.12, the deterministic divergence and the NTIC formula are correct | arxiv.org/abs/2106.06511 |
| Atay et al. (EC) | Yes | Add venue: Discontinuity, Nonlinearity, and Complexity 5(3):313–339 (2016) | Accurate (text): Thm 3.2 links automorphisms to lumpable partitions; Markov macro dynamics only "in exceptional cases"; δ = sup‖πφ−ψπ‖ | arxiv.org/abs/1606.05665 |
| Shalizi & Crutchfield 2001 (EC) | Yes | J Stat Phys 104:817–879, correct | Accurate. The Control Theorem gives H[next] − H[next given rival state] ≤ C_μ | arxiv.org/abs/cond-mat/9907176 |
| Shalizi & Moore (EC) | Yes | Add venue: Found. Phys. 55:2 (2025) | Accurate ("develop instruments", "unique coarsest refinement") | arxiv.org/abs/cond-mat/0303625 |
| Wolpert et al. 2014 (EC) | Yes | arXiv, correct | Accurate: the one-step macro→micro transfer entropy is "identically zero" | arxiv.org/abs/1409.7403 |
| Chorin, Hald, Kupferman (EC) | Yes | **Corrected** (C5) | Accurate | arxiv.org/abs/math/0101022 |
| Zhang & Liu, Neural Information Squeezer (EC) | Yes | Entropy 25(1):26 is the 2023 issue (online Dec 2022) | Not checked | arxiv.org/abs/2201.10154 |
| Bertschinger 2008; Lin & Lu 2021; Geiger & Temmel 2014; Pfante 2014 (EC) | Yes | Correct per Crossref/arXiv | Not checked | Crossref |
| Isobe 2008 (LU) | Yes | PRE 77:021201, correct | **Overstated** (C3) | arxiv.org/abs/0801.4094 |
| Machta et al. 2013 (LU, PD) | Yes | Science 342:604, correct | Accurate (text): FIM is the identity after one step; "each with a higher negative power of t"; relevant directions are the eigenvalues that do not shrink | arxiv.org/abs/1303.6738 |
| De las Cuevas & Cubitt 2016 (LU) | Yes | Science 351:1180, correct | Accurate, including "inversion of the usual renormalisation group flow" | arxiv.org/abs/1406.5955 |
| Cubitt, Montanaro, Piddock 2018 (LU) | Yes | Add volume: PNAS 115:9497 | Both quotes verified | arxiv.org/abs/1701.05182 |
| Gonda et al. (LU) | Yes | Compositionality 6:3 (2024), correct; "De les Coves" is correct | Accurate | arxiv.org/abs/2307.06851 |
| Cotler et al. 2025; Deng, Hani, Ma 2025 (LU) | Yes | arXiv, correct | Accurate | arxiv.org/abs/2510.08342 ; arxiv.org/abs/2503.01800 |
| Laughlin & Pines 2000 (LU, PD) | Yes | PNAS 97:28, correct | All quotes verified | pmc.ncbi.nlm.nih.gov/articles/PMC26610 |
| K.G. Wilson 1983; Simon 1962 (LU) | Yes | Correct | Quotes verified | nobelprize.org wilson-lecture-2.pdf |
| Manohar 2018 (LU, PD) | Yes | Correct | Accurate (m_t^(2/27); "feed down"; Appelquist–Carazzone). PD's section reference is wrong: proton decay is §4.4, not §2 | arxiv.org/abs/1804.05863 |
| Koch-Janusz & Ringel 2018 (LU, ML) | Yes | Nat Phys 14:578, correct | Accurate | arxiv.org/abs/1704.06279 |
| Lin, Tegmark, Rolnick 2017 (ML) | Yes | J Stat Phys, correct | y_i′ = b^(2−2i) y_i verified | arxiv.org/abs/1608.08225 |
| CW-VAE, Saxena et al. (ML) | Yes | Correct | Mostly accurate (C8) | arxiv.org/abs/2102.09532 |
| Kochkov et al. 2021 (ML) | Yes | Add: PNAS 118(21):e2101784118 | Accurate: 4800-step trajectories, 32-step unroll, correlation threshold 0.95 | arxiv.org/abs/2102.01010 |
| Ladder VAE; Springer & Kenyon; Bar-Sinai; Gilpin; Richardson (ML) | Yes | Correct | Accurate ("completely collapsed"; 2n+1 layers; 4–8x coarser; 1024→2048 steps) | arXiv |
| Perrin 1926 Nobel lecture (PD) | Yes | Correct | Accurate: the emulsion methods gave 68, 62, 60, 64 and 65 ×10^22 | mit.edu/~kardar/.../PerrinNobelLecture.html |
| C.T.R. Wilson 1927 Nobel lecture (PD) | Yes | Correct | Accurate: 1.25 for negative ions, about 1.31 for positive | nobelprize.org wilson-lecture.pdf |
| Sugihara et al. 2012 (PD, CLC) | Yes | Science 338:496, correct | Quote is verbatim; synchrony and transitivity are both in the text | doi.org/10.1126/science.1227079 |
| Gutenkunst et al. 2007 (PD) | Yes | Correct | Slightly overstated (C9) | doi.org/10.1371/journal.pcbi.0030189 |
| Apgar et al. 2010 (PD) | Yes | Mol BioSyst 6:1890, correct | Accurate but disputed (C6) | doi.org/10.1039/b918098b |
| Martínez et al. 2019 (PD) | Yes | Correct | Accurate: the bound is equal to the full entropy production only when all nonequilibrium variables are observed | PMC6684597 |
| Raju 2018; Gordon 2021; Har Shemesh 2016; Pavliotis–Stuart; Barato–Seifert; Touchette; Jarzynski; del Campo–Zurek (PD) | Yes | Correct | Accurate per abstracts | arXiv |
| Van Hove 1954 (PD) | Yes | Correct | Plausible (his §IV treats the critical point); not confirmed | doi.org/10.1103/PhysRev.95.249 |
| Liu, Slotine, Barabási 2013 (PD, CLC) | Yes | Correct | Accurate: edge i→j when x_j appears in x_i's equation. Sufficiency was shown only for rational dynamics | PMC3574950 |
| Pasqualetti et al. 2014; Krener & Ide 2009 (CLC) | Yes | Correct; Krener & Ide DOI is 10.1109/CDC.2009.5400067 | Pasqualetti accurate | arxiv.org/abs/1308.1201 |
| Ay & Polani 2008 (CLC) | Yes | ACS 11:17, correct | Accurate (Example 6: transfer entropy is 0 in both cases; the interventional flow is 1 bit vs 0) | uhra.herts.ac.uk/id/eprint/162 |
| Alchemy 2021 (CLC) | Yes | Correct | Scores verified: 284.4, 156.2, 140.2, 145.7 | arxiv.org/abs/2102.02926 |
| Palacios 2024, SEP (LU) | Yes | Correct | Accurate | plato.stanford.edu/entries/physics-interrelate |

Bibliographic details matched Crossref for: Anderson, Simon–Ando, Kadanoff 1966, Kadanoff–Martin, Appelquist–Carazzone, Georgi, Zwanzig, Mori, Kubo, Einstein, Takens, Gu et al., E–Engquist, Rao–Ballard, Yamashita–Tani, Mordvintsev, Chaloner–Verdinelli, Lin 1974, Liu 2011, Kokotovic–Haddad (IEEE TAC 20:111), Ellis, Flack, Chorin 2002 (Physica D) and Batterman. For the remaining arXiv items (the rest of the ML list, the DAD papers, Rainforth, BoxingGym, XLand-MiniGrid, DiscoveryWorld, Crafter, Denil, Empowerment, Rubenstein, Tishby), titles and authors matched arXiv; I did not check their content.

**The 10 most important corrections**

1. **CLC, Rosas 2024: wrong.** Theorem 1 says only that informational closure and causal closure are equivalent. Theorem 2 says informational closure implies computational closure for Z_t = f(X_t), and Counterexample 4 shows the converse fails. Computational closure can break when the process leaves its stationary distribution; informational closure cannot. EC states this correctly, so the two surveys contradict each other.
2. **LU, Rosas closure definition.** The paper's condition is I(Z⃗_t; Z⃗^L_{t+1}) = I(X⃗_t; Z⃗^L_{t+1}) for every horizon L, using whole pasts. LU writes a one-step, present-state version I(Z_t;Z_{t+1}) = I(X_t;Z_{t+1}), which is a different, weaker condition. LU's "closure gap" metric C_i should use pasts and several horizons.
3. **LU, Isobe 2008: overstated.** The logarithmic divergence is the textbook problem the abstract sets out. Isobe's result is that the tail decays slightly faster than 1/t, and he compares it with the self-consistent mode-coupling prediction 1/(t√ln t). Under that prediction D still grows without bound, but only as about √ln t. The 2-D pitfall still holds in direction.
4. **EC, Hoel 2013: imprecise.** The 2013 paper writes EI as effectiveness times repertoire size (ΔEI = ΔI_eff + ΔI_size), with effectiveness "a function of determinism minus degeneracy". EI written directly as determinism minus degeneracy comes from Hoel 2017.
5. **EC, Chorin, Hald, Kupferman: two papers merged.** arXiv math/0101022 is "Non-Markovian optimal prediction," Monte Carlo Methods Appl. 7:99–110 (2001). PNAS 97:2968 (2000) is a separate paper, "Optimal prediction and the Mori–Zwanzig representation of irreversible processes," not a version of it.
6. **PD, Apgar et al. 2010: disputed.** Chachra, Transtrum and Sethna's 2011 comment in the same journal argues that much of the reduction in uncertainty comes from many more effective data points, and that the parameters stay sloppy. This weakens its use as evidence that complementary experiments beat sloppiness.
7. **EC, Barnett & Seth.** The transitivity result is for dynamical independence (zero DD), under their assumption (2.8). The DD measure itself is not shown to be transitive.
8. **ML, CW-VAE.** Level l ticks every k^(l−1) steps, not k^l. The 0.0001 figure is Table 2's KL summed over a training sequence. The "a 2-level model may be sufficient" remark comes from a separate experiment that reset the lower or middle level.
9. **PD, Gutenkunst et al. 2007.** The paper says "all but one" of the 17 models have eigenvalues spanning more than 10^6, not all of them. The factor-of-50 statement is accurate.
10. **Venues to add or fix:**
    - Shalizi & Moore: Found. Phys. 55:2 (2025).
    - Atay et al.: DNC 5(3):313–339 (2016).
    - Kochkov et al.: PNAS 118(21).
    - Cubitt et al.: PNAS 115:9497.
    - Zhang & Liu: Entropy, 2023 issue.
    - PD's Manohar reference: proton decay is §4.4 (the multipole example is §2.2).