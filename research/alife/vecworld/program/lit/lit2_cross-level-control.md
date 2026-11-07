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