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