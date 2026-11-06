# VW-0: the vector-world contract

VW-0 defines a PhySim world as a hierarchy of hidden vectors, independent of any particular level-0 law. The coarse-graining map Φ replaces hand-designed apparatus, and a few declared numbers replace arbitrary device choices. The reference implementation is `vecworld.py`; its estimators are calibrated against the closed forms in `lingauss.py` (`calibrate.py`; results in `calibration/summary.md`).

## 1. Objects and timeline

**Level 0.** The hidden state h0(t) ∈ R^n0 evolves under a fixed, autonomous law h0(t+1) = F0(h0(t)⁺, ξ(t)), with ξ(t) ~ N(0, I) i.i.d.
- F0 depends neither on t nor on the agent. It may take many internal sub-steps; that is where scale separation lives.
- Following the review, worlds should declare conservation laws and symmetries in F0 (they fix which slow variables a coarse level can carry and make it transferable) and should include process noise.

**Input.** The agent issues a command a(t) ∈ R^n_in. A hidden injection B places agent coordinate j on actuator π_in(j), and the kick is h0(t)⁺ = κ(h0(t), B a(t)).
- By default the actuators are the level-0 coordinates and κ is addition. The actuable set (size n_in) may be a strict subset.
- A world may supply its own κ to express physical limits ("you cannot remove mass that is not there"). Such limits are physics, never rejections (§3).

**Level 1** is supervenient: h1(t) = Φ(h0(t), m(t)) ∈ R^n1.
- Φ is fixed and many-to-one in h0 for every m.
- The optional tracking memory follows m(0) = M0(h0(0)), m(t+1) = M(m(t), h0(t+1)). It is a deterministic function of the level-0 history: no independent state or noise, and inputs reach it only through h0. Hence X(t) = (h0(t), m(t)) is a Markov state.
- Memory holds what a level-1 description needs from the past, such as persistent identities of tracked objects.

**Observation.** o(t) = Q(clip(S·P·h1(t) + σ_o η(t))): P is a hidden permutation, S the identity or hidden signs (§2), Q a quantiser.

**Tick order.** Reset returns o(0). Each tick t: validate a(t), kick, run F0, update m, emit o(t+1). An input at tick t first shows in o(t+1).

**Initial state and noise.** A seeded draw from a declared ρ0, then a declared burn-in. All noise is a deterministic function of (stream, seed, member, tick): branches sharing a seed get identical noise (common random numbers); a fresh seed gives independent noise.

**Legibility.** The designer ships an un-permuted render of h1 (never shown to the agent), graded with the ALife RUBRIC rung codes and evidence rules. Target at level 1: L2 (persistent individuals, made trackable by m), L4b (self-propelled motion), L5 (interaction). The canonical Φ is coarse density blocks plus K tracked-object slots (presence, position, mass, velocity), with identity carried by m. Level 0 need not be legible.

## 2. Anonymisation

The hidden maps B (with π_in), P and S are drawn from the world seed, fixed per instance and identical across episodes. The agent is told n_in, n_obs and the constraint numbers, nothing about coordinate meanings, and not n0.

**Why permutations.** A constraint declared in agent coordinates must say the same thing in level-0 coordinates, so the hidden linear map T must carry the admissible set onto itself.
- The linear bijections that map 1-sparse vectors to 1-sparse vectors are exactly the monomial maps (permutation times invertible diagonal); sparsity k means nothing under any other map.
- Among these, preserving a box with equal per-coordinate bounds and an L1 ball leaves the signed permutations.
- Also preserving the zero-sum hyperplane 1ᵀa = 0 and the non-negative orthant leaves only permutations: the largest linear group under which every VW-0 input constraint is a public, basis-free statement.

**No rotations or sign flips on inputs.** A rotation keeps only the L2 ball. A k-sparse kick becomes a dense smear over all of level 0, so k, per-coordinate bounds and zero-sum lose meaning, and the agent can no longer poke one place, which is how it discovers locality, transport and objects. Sign flips break zero-sum and positivity: an agent that believes it moves mass would be creating it.

**Observation side.** An invertible linear map of o leaves every information-theoretic certificate unchanged (under isotropic noise and orthogonal maps, o is identical in distribution), so the choice is about structure. A permutation keeps the coordinate-wise meaning of noise, quantisation and saturation, and keeps each coordinate a local aggregate whose neighbourhood graph the agent can rediscover from correlations and responses; a rotation destroys this. Sign flips keep locality and are a declared option (`sign_flip`, off by default) that hides which coordinates are non-negative densities.

**Replicas.** Same law, different world seed: isomorphic up to anonymisation. An agent that learned structure, not coordinates, should re-identify a replica cheaply.

## 3. Input constraints

All declared on the world card; all permutation invariant.

| number | meaning |
|---|---|
| k | at most k non-zero coordinates per tick |
| [lo, hi] | bound on every non-zero value |
| total | Σ\|a_j\| ≤ total per tick |
| zero_sum | Σ a_j = 0: inputs move mass, never create it |
| min_interval | ticks between non-empty inputs |
| quantum | values are integer multiples of q |
| episode_budget | bound on the episode's summed \|a\| |
| noise | multiplicative actuation noise σ_a on the support |

Rules:
1. **Public decidability.** Admissibility depends only on the input, the card and the agent's own past inputs, never on hidden state; a state-dependent rejection would be an observation channel. State-dependent limits belong inside κ.
2. **Rejection is free.** A violation raises an error naming the constraint; no tick, budget or state changes. Programs are validated as a whole before any of them runs.
3. **Constraints bind the command, not the realisation.** Under zero-sum the noisy kick is projected back to zero sum, so declared conservation holds exactly.
4. **Exchangeable actuators.** Σa = 0 is basis-free only if all actuable coordinates share one physical type (densities, not momenta). Worlds should make only one type actuable.
5. **Command information.** With a quantum a tick carries at most log₂ N_adm bits, N_adm ≤ Σ_{j≤k} C(n_in, j)·n_q^j. The effective capacity through the world is §6.3.

## 4. Observation constraints

σ_o (noise), q_o (quantum), clip (saturation), `sign_flip`, max_queries per program, max_ticks (exploration budget), and replay:
- `none`: each reset is a fresh sample;
- `initial` (default): a seed reproduces h0(0) with fresh noise, like a lab preparing identical samples;
- `full`: identical noise.

Partial observation of level 1 belongs in Φ. Certificates require finite resolution, σ_o² + q_o²/12 > 0: deterministic continuous observation makes information quantities infinite and invites Takens-style reconstruction.

## 5. The agent's task and the exam

**Exploration.** `reset(seed)`, `step(a)` and `run(program, query_times)` within the budget. The agent learns what inputs do only through their emergent effects at level 1.

**Exam item** (seed from a reserved namespace the agent cannot reset to). The harness runs a prefix program of P ticks and reveals o(0..P) and the prefix inputs, then an open-loop test program and query times q ∈ (0, H]. The agent predicts o(P+q).

**Scoring.** Expected squared error over R replicate futures branched from the item's hidden state with fresh noise (this removes most scoring noise), per horizon, against three references:
- *persistence*, the baseline;
- the *ceiling*, the designer's best level-1-only predictor (exact for linear-Gaussian worlds: Kalman under the true law);
- the *oracle*, the replicate variance (h0 known).

Skill = (MSE_pers − MSE)/(MSE_pers − MSE_ceil); the oracle exposes each item's closure gap.

**Held-out strata.** Free evolution; single pulses; dense random programs like exploration; compositional (coordinate combinations and timings never together in the agent's log, checked by the designer); extremal (constraints at their bounds). Also stratified by horizon and required depth (ceiling far above oracle). Optional predictive variances are scored by Gaussian NLL. VW-0 exams are open-loop only.

## 6. Designer certificates

**Conventions.** Everything is conditional on an open-loop program π (inputs independent of hidden state) and measured under the exam's state distribution, since closure can depend on it (the review's weak-lumpability warning). Pasts are windows W_p(t) = o(t−p+1..t), p = 0 meaning none, at several horizons τ: the corrected informational-closure definition (Rosas et al. 2024) uses whole pasts and every future length.

### 6.1 Closure ceiling

- V0(τ) = E‖o(t+τ) − E[o(t+τ)|π]‖²
- Vε(τ,p) = E‖o(t+τ) − E[o(t+τ)|W_p(t),π]‖² (level-1-only predictor)
- Vυ(τ) = E‖o(t+τ) − E[o(t+τ)|X(t),π]‖² (oracle with privileged level-0 access)

Derived:
- **Ceiling** c(τ,p) = (V0 − Vε)/(V0 − Vυ): the fraction of predictable variance that level-1 pasts recover; 1 means closed at that horizon in mean square.
- **Gap** Γ(τ,p) = I(X(t); o(t+τ) | W_p(t), π); Gaussian proxy ½ log det Σε/Συ.
- **Block gap** Γ_L(p) over o(t+1..t+L). Informational closure holds exactly when Γ_L(∞) = 0 for every L.
- **One-step split** (Atay et al.): Γ(1,1) = M + R, with memory M = Γ(1,1) − Γ(1,∞) (recoverable from longer level-1 history) and residual R = Γ(1,∞) (needs level-0 access).

Estimators: the oracle is Monte Carlo over R fresh-noise branches from X(t) (model-free, unbiased). The ε-predictor is fitted on W_p, linear by default; it can only do worse than the true ε-predictor, so Γ̂ over-states the gap in nonlinear worlds (better predictors plug in). Log-determinants are Wishart bias-corrected; standard errors come from folds.

Reading: Γ ≈ 0 everywhere is a closed level (a universal law that also hides level 0). A large Γ(τ,1) falling toward Γ(τ,∞) is memory a long-past agent can recover. Γ(τ,∞) is beyond any level-1 agent.

### 6.2 Leak: how readable level 0 is from level 1

- The posterior covariance of h0(t) given W_p(t), in prior-whitened coordinates, has eigenvalues μ_i ∈ (0,1]: near 1 a hidden direction, toward 0 a direction read off.
- Information ℓ(p) = −½ Σ log μ_i (= I(h0(t); W_p(t)) for Gaussian variables); leak dimension d_ℓ(p) = #{μ_i < ½}; hidden fraction 1 − d_ℓ/rank.
- Growth of ℓ from p = 1 to larger p is the history (Takens) channel: micro detail reconstructed over time.
- Guards against a Φ so wide that level 0 is effectively observed (the critique's leakage pitfall).
- The estimator is a linear decoder, so in nonlinear worlds it is a lower bound on readability. For large n0, restrict to the top principal components.

### 6.3 Input capacity

- **Excitable directions per tick** (structural): d_exc = min(k, n_in) − [zero_sum].
- **Response** G: the one-tick effect of a unit command on each agent coordinate on the noise-free level-1 future o(t+1..t+L), from branch pairs sharing noise (exact for linear worlds, a local average otherwise; the designer may apply inadmissible probes).
- **Whitened** by Σε,L(p), the part of that future an agent with past p cannot otherwise predict: singular values s_i on the admissible subspace (1^⊥ under zero-sum).
- **Visible dimension** d_vis = #{b·s_i ≥ 1}; usable per tick: min(d_exc, d_vis).
- **Capacity bound** C_in: water-filling over s_i² with power ρ², where ρ bounds ‖a‖₂ over admissible commands; bits per isolated tick (an upper bound).
- **Atoms**: SNR of each elementary admissible move (+b on one coordinate, or ±b on a pair under zero-sum), and the fraction with SNR ≥ 1.

### 6.4 Observation capacity

- **Rate** r(p) = I(o(t+1); X(t+1) | W_p(t), π) = ½ log det Σε(1,p) − ½ log det R: what each new observation teaches about the hidden state (bits per tick).
- **Channel bound** Σ_j ½ log₂(1 + Var h1_j/(σ_o² + q_o²/12)).
- **Instantaneous visible directions** d_ℓ(1).

### 6.5 Admission (provisional thresholds)

Finite resolution; non-trivial, (V0 − Vε(1,p_max))/V0 ≥ 0.1 (rules out levels "closed because they are noise"); is a level, c(1, p_max) ≥ 0.5; level 0 hidden, hidden fraction ≥ ½ at p_max; inputs visible, some atom SNR ≥ 1; declared invariants conserved under free evolution; legibility, RUBRIC codes on the level-1 render (≥ L2 when individuals are claimed); F0 passes the RUBRIC numerical-validity tests (dt/2 and a resolution change). Every estimator was first calibrated on the linear-Gaussian family, where all of these have closed forms (`calibration/summary.md`).

## 7. Composition

- **Direct sum W_a ⊕ W_b** (`product`): concatenate h0, Φ, memory and actuators; anonymise jointly. Two independent subsystems; the agent must discover the factorisation (block structure in responses and correlations). Gaps, leak information and capacities add (checked to 1e-15 on the linear-Gaussian family). Default k_a + k_b; a zero-sum over the union lets inputs move mass between blocks.
- **Coupled product**: a direct sum plus an exchange term J(h0), e.g. `diffusive_coupling`, which relaxes declared coordinates along graph edges and conserves their sum. Tiles a cell world into a larger one or lets two worlds interact. Gaps no longer add; stability needs a small-gain bound on J.
- **Stacking** (`stack`): level 2 = Φ2(h1, m2), observed instead of level 1; the agent still acts on level 0. Supervenience is transitive and, by the data-processing inequality, leak and input visibility can only fall. Report the gap with respect to X and with respect to level 1; the difference says whether level 1 is closed relative to level 2.
- **Stride** (`stride`): temporal coarse-graining, one tick = s level-0 ticks; inputs and memory updates once per tick.
- **Downward refinement to level −1** (`refine`): a finer state x with law F₋₁ and a map Ψ: x ↦ h0; the new world is (F₋₁, Φ∘Ψ), memory through Ψ.
  - *Lifted actuation* uses Λ with Ψ(x + Λu) = Ψ(x) + u: same agent interface, comparable exams. *Fine actuation* on x is a finer device, hence a different world.
  - Certificate: the distributional commutation error δ²_T = E‖E[Ψx(T)|x] − E[h0(T)|h0 = Ψx]‖², measured by branching.
  - Exact lumpability (δ = 0 and matching noise) makes the refinement invisible at level 1, with identical closure tables: universality. δ ≠ 0 raises the gap. A family of refinements of one level 0 is the universality test.

## 8. Open questions

1. **Thresholds.** Which gap and leak values keep a level both universal and probeable? Map with agents as a function of gap, leak and scale ratio.
2. **Replay default.** `initial` resembles lab practice; `full` hands the agent common random numbers, a strong counterfactual tool. Should exams depend on the choice?
3. **Nonlinear ceilings.** The designer's level-1 reference (linear, learned, or a particle filter under the true law) only bounds Vε from above, so agents could exceed skill 1. How should the ceiling be certified?
4. **Tracked slots.** Identity swaps make squared error harsh; slot-matched (permutation-invariant) losses for memory-bearing coordinates?
5. **Closed-loop exams** need directed information instead of conditioning on inputs. Allow them in VW-1?
6. **High dimensions.** Estimators degrade for large n0 and n_obs·L: PCA truncation, neural decoders, or bounds instead of point values.
7. **Actuators.** How to choose the actuable subset and its type; is lifted actuation the right default when refining?
8. **Learned Φ.** Designer-chosen, or the closure-optimal coarse-graining (the agent's levels may then differ from the designer's)?
