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