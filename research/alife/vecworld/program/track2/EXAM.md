# PhySim-v2 exam: design draft (track 2)

Draft of 2026-11-07. Builds on the VW-1 note (`vw1/note/CATEGORY.md`, cited as "the note"), the gliders results (`vw1/fresh/*/results/summary.json`), PhySim v1 (`residency-environments/environments/physim`) and the earlier literature reviews. Citations are marked VERIFIED (checked this session, or in the cited earlier review) or MEMORY. The one new computation is `checks/kl_ring.py`, with output in `checks/kl_ring.json`.

## 0. Recommendations in brief

1. **Task.** Predict the joint law of level-k observations (k ≥ 1) at query times under a held-out open-loop program. Primary items reveal a level-k history, so the predictor must filter as well as know the law. Deliverable: a predictor program returning samples, as in v1.
2. **Hidden set.** Hiding θ (the level-0 weights) is necessary but not sufficient. Also hidden: a high-entropy secret behind all real-world randomness, and exam instances (states, histories, programs, truths) until grading. Nothing computed from θ or the secret may reach the agent except through the ports. Drop the permutations.
3. **Interaction limits.** Charge inputs in nats, c(u) = ½‖u‖²_{Σ_a⁻¹}, with Σ_a the covariance of noise entering through the same channel as the input. By data processing this bounds the KL between perturbed and unperturbed path laws at every level. For gliders, a coarse "wind" force channel instead of the matter kick. Ticks, resets and nats are budgeted separately; no common-random-number replay.
4. **Primary metric.** Oracle-normalised energy skill (OES): fair energy-score estimator, averaged over declared (level, horizon) cells, with the designer's level-1 ceiling on the same scale.
5. **Harness.** Reuse v1's Verifiers task, MCP process, sandboxes and bundles. New: the public simulator in the agent sandbox, a nats accountant, history-conditioned items, the fair energy score, stored oracle references.
6. **Pilot.** Gliders with four hidden global Flow-Lenia parameters. Baselines must bracket the range before any agent runs: climatology < data-only level-1 predictor < simulation-based inference (SBI) at budget < true-θ ceiling < oracle.

## 1. The task

**Objects.** A world is W = (L0_θ, Φ₁…Φ_k, P_in, P_obs) (note, Def. 9).
- L0_θ is a public step function f(x, u, ω; θ) with hidden θ and an explicit noise law.
- Φ is public.
- The agent observes level k_obs ≥ 1 through P_obs and acts on level 0 through P_in.
- An item never asks for level 0.

**Item types.** Each item fixes a context, a test program π (open loop, admissible) and queries Q = {(level j ≥ k_obs, time q)}. The target is the joint law of the queried values. Samples with the same index form one trajectory, so the law is joint over queries.

| type | conditioning given to the predictor | target law | what it tests |
|---|---|---|---|
| **H (history), primary** | revealed o₀…o_P and the prefix program, from a secret start drawn from μ after burn-in | law(o_{P+q} \| x_P, π), scored against replicate futures; the best possible predictor given the history is law(o_{P+q} \| o_{0:P}, π, θ) | level-k dynamics, filtering, input response |
| **L (law)** | none: start from the public initial law μ, with or without burn-in | law(o_q \| μ, π, θ) | θ through transients and stationary statistics, with no filtering needed |
| **P (prepared), optional** | none: a hidden prepared state x* that the agent could also reset to during the investigation (v1 style) | law(o_q \| x*, π, θ) | continuity with v1, local experimentation |

H items test level-k dynamics and do not reduce to plugging θ̂ into the simulator, because the predictor never receives x_P. L items isolate θ identification. P items bridge to v1 and are not needed for the pilot.

**Horizons (gliders).**
- Block-view closure ceilings are 0.99, 0.97, 0.85, 0.49, 0.14 and 0.08 at 1, 2, 4, 8, 16 and 32 ticks. Object-view ceilings are 0.83, 0.78, 0.63, 0.43, 0.21 and 0.05.
- Twin variance doubles every 2.3 ticks (3.7 for the object view).
- Pointwise queries therefore use h ∈ {1, 2, 4, 8, 16} ticks after a prefix P = 16, which is longer than the 3–4 lags the best closure predictors used.
- Longer horizons {32, 64} are asked only of a declared level-2 statistic (`phi.population`: count, total mass, mean speed, fusion rate). PhySim v1 drew the same lesson: in chaotic worlds, late windows must score statistics.

**Programs.** The program distribution is public; the drawn programs are not. Blind inputs barely register (median effect size ≤ 0.013), so an exam made of random programs would let an "ignore actions" predictor score near the top. Mix four classes in equal shares:
- (a) no input;
- (b) blind random;
- (c) aimed, built by the examiner from the revealed history (for example, pushes on the flank of a body whose position and velocity are visible at tick P);
- (d) large regional pushes at the per-episode budget.

Aimed programs are still open loop: they are functions of revealed information only.

**Deliverable.** A frozen program `predict(history, program, queries, n_samples=64, seed=0)` returning samples of shape (n_samples, n_queries, dim): frozen, compute-bounded, re-gradable on fresh suites, as in v1. A samples-only mode (items given to the agent) suits a smoke pilot but shows the test set and leaves per-item compute unbounded. An optional `theta.npz` of posterior samples is never rewarded; it feeds the θ-plug-in diagnostic (Section 4).

## 2. Threat model: is hiding the level-0 weights enough?

No. The agent may know the architecture, Φ and the ports, but three further things must stay secret (the randomness, the exam instances, any artefact fitted on the hidden world) and side channels must be closed.

| item | decision | reason |
|---|---|---|
| L0 architecture (code), dtype, stride | public | Premise of v2. It makes SBI possible, which is intended (see below). |
| θ (level-0 parameters or weights) | **hidden** | The object of inference. Draw it continuously from the prior: "round" values can be guessed. |
| Φ code | public | Needed to simulate level k from a candidate θ. |
| Φ weights, if learned | public **only if trained on prior-predictive data** | A Φ fitted to hidden-world states summarises their distribution (an autoencoder decoder is nearly a generative model of them; glider size alone pins down the kernel radius R). Train Φ on simulations with θ′ ~ prior, or audit the leak by regressing θ on Φ's parameters across worlds. |
| normalisers, clip ranges, quanta, score scales | public, from the prior predictive | Scales "frozen from a calibration ensemble" of the hidden world (v1 practice) leak stationary variances. |
| initial law μ, burn-in | public | Needed for SBI and for L items. A variant may hide some μ parameters inside θ. |
| noise law | form public. Parameters may be hidden **except where they define the input metric** | If c(u) used a hidden σ, admissibility would depend on θ and would no longer be publicly decidable (note, Prop. 8a). |
| ports, admissibility rules, budgets | public | The agent must be able to plan. Rejection depends only on the command and public counters. |
| permutations, sign flips | **drop** | With Φ public, matching simulated and observed correlation structure undoes them (the page showed structure leaks even without the code). They only add a nuisance step. |
| world seed, noise keys | **hidden, and replaced by a secret** | See "noise keys and replay". |
| exam programs, histories, truths | hidden until grading | Histories reach the predictor sandbox only, one item at a time. |
| exam program generator, scoring rule | public | The agent should know what it will be asked. |
| world generator and selection criterion (track 1) | public | See "selection". |
| compute and budgets | public and enforced | Difficulty is defined relative to them. |

**Noise keys and replay.** VW-1 derives every key from a public salt and small integers (`make_key(_NS_EXAM, world_seed, exam_seed)`), and the gliders initial law `init_patches` does not depend on θ. With the public code and a guessed world seed, an agent could compute every exam start exactly and simulate it pathwise under θ̂; knowing its own episode keys, it could fit θ noise path by noise path, and chaos would pin θ almost to machine precision. Fix: mix a secret of at least 128 bits into every real-world key, and pass reset seeds through a keyed hash so that seeds are labels, not keys.

Full replay (`replay='full'`, common random numbers) is presentation-level (note, Prop. 1): twin differences carry no noise, so input responses come noise-free and the accounting of Section 3 no longer applies. Keep `replay='initial'` (same start, fresh dynamics noise, v1's prepared start); common random numbers, if offered at all, form a separately reported "lab mode".

**Exam leakage.** Exam starts come from a secret namespace that resets cannot reach. Each item's history enters a fresh predictor sandbox (v1), so histories cannot be pooled. Validation checks only format and reproducibility. The bundle identity must not expose an unsalted hash of θ: with four parameters on a coarse grid, a published hash can be brute-forced.

**Selection effects.** A track-1 search that keeps "interesting" θ makes the hidden θ a draw from the prior conditioned on selection. Public selection code lets the agent reproduce that prior (legitimate information); hidden selection misspecifies its prior undetectably. Rules: publish the criterion as code; select only on world-level properties (viability, closure ceiling, input efficacy), never on baseline-agent scores, which would push θ into regions hard for SBI; draw the secret and the exam after selection.

**Simulation-based inference.** With the architecture public, the agent can run any candidate θ: synthetic likelihood [W10] or neural posterior estimation [CBL20] on summaries (glider count, speed, size, fusion rate, block spectra) is the natural route. Is the task then only parameter fitting? Partly, and that is acceptable:
1. Under H items, θ gives a level-0 simulator but no state. The agent must still build a level-k filter and predictor, for example trained on simulations from its posterior; in the closure study predictor quality alone moved the ceiling by up to 0.12.
2. Scoring is predictive, so only parameter combinations stiff at level k matter and sloppy ones are free [M13, VERIFIED in `hierarchical_worlds_litreview.md`]. Finding those combinations is the emergent-level part of the job.
3. dim θ is the difficulty dial. Four global scalars may be easy for SBI; all 261 Flow-Lenia parameters, or a track-1 neural level 0, are not, and then level k must be modelled mostly from data with the architecture as a prior.
4. Interaction is limited (Section 3), so experiment design [R24, VERIFIED in `lit2/cross-level-control.md`] counts.

A declared compute envelope guards against "most compute wins", and calibration must show that SBI at budget sits clearly below the ceiling. For more than fitting, add a public generator over architectures with a hidden draw; hiding the code itself would turn v2 back into v1.

**Side channels.** Rejection messages use only public information (the kick's "a cell cannot give up more than it holds" is physics, visible at level 1, not a message). Non-finite numerics from admissible inputs would be a state-dependent signal, so v1's envelope check must pass. Use the fixed-shape JAX tracker, not the numpy one, whose cost grows with the number of components, and return results per request, not per tick. Quantisation (10⁻³) removes low-bit fingerprints. Grader errors are reported as infrastructure failures without detail (v1 policy).

**Minimal hidden set.** θ, the real-world secret (agent episodes and exam), and exam instances until grading, with one hygiene rule: no artefact fitted to the hidden world crosses the boundary.

## 3. Interaction limits

### 3.1 Derivation

Let inputs enter as a state-independent shift before Gaussian process noise: x_{t+1} = g_θ(x_t) + B u_t + ξ_t, with ξ_t ~ N(0, Σ). Both runs have the same initial law. By the chain rule for KL over Markov paths,

KL(P_u ‖ P_0) = Σ_t E_{P_u} KL(N(g(x_t) + B u_t, Σ) ‖ N(g(x_t), Σ)) = ½ Σ_t (B u_t)ᵀ Σ⁻¹ (B u_t),

because the per-tick term does not depend on x_t. An information budget in nats is therefore a Mahalanobis norm budget. The continuous-time version is Girsanov: dx = (b(x) + B u) dt + σ dW gives KL = ½ ∫ ‖σ⁻¹ B u_t‖² dt, with σ⁻¹ on the range of B (MEMORY, textbook). For a closed-loop policy, KL is the expectation of the same sum, so a pathwise cap on the charged sum still bounds it.

Check: on the VW-1 ring (`vw.lingauss.ring()`), a 3-tick program has closed-form KL 7.521 nats against a Monte Carlo log-likelihood ratio of 7.519 ± 0.027 (`checks/kl_ring.json`).

### 3.2 What a nats budget guarantees, and what it does not

Let C = Σ_t c(u_t) be an episode's charge. For every θ and hidden start:
- **Every level.** By data processing, KL(law(o^u) ‖ law(o^0)) ≤ C at any level and port (MEMORY, standard).
- **Input to observation.** For a random program U, I(U; O) ≤ E_U KL(P_U ‖ P_0) ≤ C, which caps the agent's empowerment [S14, VERIFIED in `lit2/cross-level-control.md`].
- **Effect size.** For open-loop programs χ² tensorises over ticks, so for any scalar statistic f, (E_u f − E_0 f)² ≤ (e^{2C} − 1) Var_0 f, and ≤ 2C Var_0 f for a linear-Gaussian response: the page's effect-size measure, bounded by the budget.
- It does **not** bound information about θ, which passive observation already reveals (limited by the tick budget). A Fisher budget would, but it depends on θ and x, so it cannot be an admissibility rule.
- **The bound is loose, and the looseness depends on aim.** On the ring (one ±1 pair at tick 0, 6 block sums observed with noise 0.2), the share of level-0 path KL reaching the observations within 64 ticks is:

| input | level-0 KL (nats) | observed KL (nats) | share |
|---|---|---|---|
| sites in blocks 0 and 3 | 4.41 | 0.49 | 11% |
| sites in neighbouring blocks | 2.01 | 0.24 | 12% |
| two sites in the same block | 4.01 | 0.049 | 1.2% |

  A coarse-graining discards information about within-fibre pushes. This share, the *information efficiency* of an experiment, is a designer-side diagnostic of aiming. (Structurally this is privacy accounting with the Gaussian mechanism, the world's noise playing the privacy noise; Mironov 2017, MEMORY.)

### 3.3 When inputs do not enter that way

**Gliders.** The kick moves matter: it removes min(−u, A) at sources and gives the pooled matter to sinks. Process noise then enters the *flow* (std 0.5 per component, channel, cell and substep; dt = 0.2). A deposit on an empty cell has no counterpart in the unperturbed law, so the path laws are mutually singular and KL = ∞. Three options:

1. **Matched actuation channel (recommended).** The world always applies ũ_t = u_t + η_t, η_t ~ N(0, Σ_a), also when u = 0, followed by any kernel K(x, ũ). The conditional laws of x given ũ coincide under both programs, so KL(P_u ‖ P_0) ≤ ½ Σ_t ‖u_t‖²_{Σ_a⁻¹} for *any* downstream dynamics: clipping, discrete trackers, deterministic levels. For gliders, a coarse "wind": a ∈ ℝ^{2×8×8} (a force per 16-px block and component), upsampled by a public smooth kernel and added to the flow of both channels for all 20 substeps of a tick, with background η drawn once per tick. A force f held for 20 substeps displaces matter by 20·dt·f = 4f px, so a 1-px extra displacement of one block costs ½(0.25/σ_w)² nats: 12.5 nats at an illustrative σ_w = 0.05, whose background drift is 0.2 px per tick against a body speed of 1.6. σ_w is calibrated in the pilot.
2. **Use the existing flow noise** (exact Girsanov, no new physics): per-cell forces charged against std 0.5 per cell and substep. A coherent 1-px push over a 16 × 16 region costs ½·20·2·256·(0.25/0.5)² = 1280 nats, nearly all of it information level 1 never sees. Correct, but the budgets become uninterpretable.
3. **Keep the matter kick with a norm budget only** (today's L1 `total` and `episode_budget`): simplest, no information meaning.

**Deterministic levels** have infinite KL between any two distinct inputs, so they must declare a matched actuation channel or fall back to norm budgets that do not compare across worlds. **Rule for track 1:** put inputs where the noise is, at the scale of the actuators; if there is no such noise, add a low-dimensional actuation channel to the declared law.

### 3.4 Alternatives

These serve as designer certificates. None can be an admissibility rule: each depends on θ or hidden state, and reporting it would leak.

| measure | estimand | role |
|---|---|---|
| I(U; O) at level k, input capacity (`vw.input_capacity`) | how much inputs can show up in observations | efficacy check: inputs must matter for exam programs |
| Fisher information or expected information gain about θ (`vw.fisher`, valid for about 1 tick by autodiff; likelihood-ratio estimators beyond that) | how much a budget can reveal about θ | sets the tick budget T_max to a target posterior contraction |
| empowerment; directed information I(U → O) for closed loop | control bandwidth | bounded by the nats budget; cross-world comparison |

### 3.5 Budgets

| resource | unit | charged on | why |
|---|---|---|---|
| real-world ticks T_max | member-ticks | every tick of the agent's episodes | caps passive information (v1: 50,000 tu) |
| resets | r ≥ 1 ticks each | each new start | free in vw today, giving unlimited stationary samples |
| per-tick nats c_max | nats | each command | envelope: numerics and the level-1 description stay valid |
| per-episode nats κ_ep | nats | Σ within an episode | the KL guarantee is per episode |
| total nats κ_tot | nats | Σ over the investigation | total intervention information |
| replays | — | `replay='initial'` only | Section 2 |
| agent compute | GPU- or CPU-hours, memory, disk | the agent sandbox | SBI cost |

Exam programs obey the same per-tick and per-episode caps.

### 3.6 Recommended scheme

- Per tick: c(u_t) = ½ u_tᵀ M u_t with M = Eᵀ Σ_a⁻¹ E, E the public embedding from agent coordinates into the input channel (restricted to the zero-sum subspace under zero_sum).
- Admissible iff c(u_t) ≤ c_max, Σ_{episode} c ≤ κ_ep and Σ_{all} c ≤ κ_tot, together with T_max and the reset charge; charged on the canonical command before actuation noise, so every term is a public function of the command and counters.
- Guarantee printed on the card: "for any admissible program, the law of everything you can observe differs from the no-input law by at most C nats of KL; any statistic's mean shift is at most √(e^{2C} − 1) of its spread".

### 3.7 What vw needs

- `Admissible`: a public quadratic `metric` M with `tick_nats` and `episode_nats` caps (the existing `episode_budget` is L1); `public()` shows M or its generator, the caps and the nats used.
- `World`: a global `total_nats` beside `max_ticks`; a `reset_cost`; a 256-bit `secret` mixed into `make_key`; reset seeds through a keyed hash; identity in/out maps by default.
- `InputPort.noise` is multiplicative and acts only on the support, so a zero command carries no noise and no data-processing bound exists. Add an additive actuation channel present at every tick on its own key stream, or let `Level` declare `input_channel=(E, Σ_a)` and draw η itself.
- `vw.stride` applies the input at the first substep only; a wind needs a "held input" stride.
- Certificates: `kl_check` (Monte Carlo log-likelihood ratio of η against the declared c, as in `checks/kl_ring.py`) and `info_efficiency(program)` (Gaussian-proxy KL at level k over the charge).
- `Exam`: the fair energy score, score groups, oracle (leave-one-out), climatology and ceiling references, and withheld histories (today `Exam.public()` reveals the items).

## 4. Scoring

### 4.1 Rules

Coordinates are divided by public scales and the norm is RMS, as in v1.
- **Energy score** [GR07, VERIFIED]: ES(F, y) = E‖X − y‖ − ½ E‖X − X′‖, strictly proper for laws with finite first moment; v1's rule. Its reported weakness, low sensitivity to misspecified correlation [PT13], is disputed [ZB19].
- **Variogram score** [SH15, VERIFIED]: VS_p = Σ_{i<j} w_ij (|y_i − y_j|^p − E|X_i − X_j|^p)², p = 0.5, spatial weights w_ij = 1/(1 + d_ij). It targets dependence, but is proper not strictly proper and blind to a common bias, so secondary.
- **Log score.** Needs a density, which exists only if the port adds Gaussian noise (a mixture of N(sample, σ_o² I)); with 64 components in 192 dimensions the nearest sample dominates, so only for low-dimensional level-2 groups. The gliders port only quantises, so not there.
- **CRPS per coordinate** (fair version [F14, VERIFIED]): diagnostic maps of where predictors fail.

### 4.2 References

For each item and declared cell (level j, horizon h):
- **S_oracle.** The true simulator from the true x_P (replicate futures, fresh noise): a lower bound for every predictor, but conditioned on hidden state, so not behaviour-level (note, Prop. 9d).
- **S_ceil.** The designer's best level-k-only predictor trained on unlimited true-θ simulations (the closure-ceiling predictor, rescored with the energy score; the MSE ceilings above must be recomputed). Behaviour-level but only as good as the designer's fit, so frozen and versioned. The best history-based predictor, law(future | o_{0:P}, θ), lies between S_oracle and S_ceil.
- **S_clim.** The stationary no-input law of o, from a pool of 256 post-burn-in true-θ states. Persistence is a control, not a reference.

The agent's shortfall splits into two parts: (S_agent − S_ceil), the agent's identification and modelling gap, plus (S_ceil − S_oracle), the closure gap that no level-k predictor can close.

### 4.3 Estimation with finite ensembles

- **Truths.** R = 16 replicate futures per item, branched from x_P with fresh secret noise under the same test program.
- **Agent.** S_agent = (1/R) Σ_r ES_fair(samples, y_r).
- **Fair estimator** (a U-statistic, after [F14]): ES_fair = (1/m) Σ_i ‖x_i − y‖ − (1/(2m(m−1))) Σ_{i≠j} ‖x_i − x_j‖. v1's estimator, which takes ordered pairs including self, is biased upward by E‖X − X′‖/(2m), about 1/m of the score of a perfect forecast. That would penalise a 15-member oracle about 5% more than a 64-sample agent.
- **Oracle, leave one out.** For each r, ES_fair({y_s}_{s≠r}, y_r) uses m = R − 1. This is unbiased and costs no extra simulation.
- **Variogram score.** Its plug-in estimate of E|X_i − X_j|^p biases the square upward by O(1/m). Compare at equal m by subsampling the agent to R − 1, or bias-correct.
- **Uncertainty.** A paired bootstrap over items, with agent, references and truths sharing items. Proposed sizes are n = 64–128 items with R = 16.

### 4.4 Aggregation

Per cell, OES_c = (S̄_clim − S̄_agent) / (S̄_clim − S̄_oracle), with S̄ an item mean. A ratio of means is more stable than a mean of ratios.
- Cells: level k_obs at h ∈ {1, 2, 4, 8, 16}, plus level 2 at h ∈ {16, 32, 64}.
- Cells whose denominator is not at least 3 SE above zero in calibration are left out of the primary aggregate. This is decided before any agent is scored.
- The primary aggregate weights the remaining cells equally.
- Also report the (level × horizon) skill profile, the same profile for S_ceil, and the per-program-class breakdown, with class (c), aimed, shown separately.

### 4.5 Primary metric, reward, diagnostics

**Primary metric: OES**, the equal-weight mean over declared cells.
- It is exact up to Monte Carlo error and needs no fitted normaliser.
- 1 is unreachable from level k alone. The frozen ceiling OES(S_ceil) is printed alongside it.
- For RL, a monotone map such as clip(OES / OES_ceil, 0, 1) is an open decision. v1's −log₁₀ S has no oracle reference.

**Diagnostics.** θ-plug-in (if θ̂ is submitted): S_oracle(θ̂) − S_oracle(θ), the oracle run from the true x_P with θ̂, is parameter error weighted by its dynamical consequence (stiff directions count, sloppy ones do not), at n·R simulations per agent. Information efficiency: the designer-side KL the agent's experiments delivered to level k, divided by the nats charged.

## 5. Harness

| PhySim v1 | PhySim v2 |
|---|---|
| `R6Taskset`/`R6Task` (Verifiers), Prime sandboxes, limit audit, finalisation and collection | reuse |
| trusted MCP process: `experiment`, `usage`, `validate`, `submit` | reuse the process. `experiment(start, program, queries)` with start ∈ {fresh, replay:<label>, prepared:<i>}, queries as (level, times). Add `episode_open`/`episode_step_many`/`episode_close` for closed-loop exploration. `usage` adds nats |
| agent sandbox **without** the simulator | agent sandbox **with** the public simulator (vw, world module, Φ, μ, prior or generator, scoring code), pinned JAX, optional GPU |
| every experiment starts from the hidden prepared state | fresh secret starts from μ, replay of a labelled start, optional prepared states |
| devices (inject, adjust, sensor slots) | vw `InputPort` with the nats accountant; `ObservePort` on level k (quantised or noisy) |
| `predict(actions, queries, n_samples, seed)` | `predict(history, program, queries, n_samples, seed)` |
| fresh predictor sandbox per grading experiment | same, one item per sandbox (or a batch with no state carried between items) |
| `score_case`: energy score per hidden group, self-pairs included | fair energy score per public (level, horizon) group, with VS and CRPS diagnostics |
| reward max(0, min(−log₁₀ S, K))/K | OES, with the reward map open |
| `LabBundle` (world files, declaration, apparatus, preparation, suite, truths, checks) | `VWBundle`: `public/` (code, declaration, prior, program generator, scales), `hidden/` (θ, secret; evaluator only), `suite/`, `truth/` (R futures per item), `references/` (oracle LOO, climatology, frozen ceiling), `checks.json` (acceptance). Identity hashes θ only with a secret salt |
| numpy/scipy steppers in the grader | the same public JAX code in the grader. The trusted-code question becomes simpler: the grader runs only hashed public code |

**Agent tools.** The real world (`experiment`, `episode_*`) within budget; its own copy of the public simulator, run with any θ and its own noise inside its compute envelope; `validate` (format and reproducibility only); `submit`.

**Resource limits** (pilot proposal): T_max = 10,000 real ticks (about 23 min of grader CPU at 0.136 s per member-tick); reset cost 1 tick; κ_ep and κ_tot from calibration; agent compute one GPU for 8 h plus 4 CPU cores; 24 h wall clock and v1's turn limits; predictor 64 samples, at most 120 s per item on one GPU. Simulating level 0 inside the predictor costs 64 × 16 × 0.136 ≈ 140 CPU-seconds per item at a 16-tick horizon, so a CPU-only predictor would have to be an amortised level-k model.

## 6. Calibration plan

### 6.1 Baselines and controls

| id | agent | uses |
|---|---|---|
| B0 | climatology and persistence from the agent's own budgeted data | nothing |
| B1 | data-only level-k predictor (ridge, patchnet/slotnet from the closure study) trained on budgeted real-world data | no simulator |
| B2 | SBI: synthetic likelihood [W10] or neural posterior estimation on level-k summaries → posterior over θ → the B1 architecture trained on simulations from posterior draws | public simulator, budget, compute |
| B2p / B2a | B2 with passive data only / with designed experiments under κ | value of interaction |
| B3 | B2's predictor trained with true θ: the ceiling | designer |
| B4 | θ-plug-in oracle (true x_P, θ̂ from B2) | diagnostic |
| B5 | oracle | designer |

Controls:
- ignore-actions: B3 trained without inputs;
- prior-mean θ: B3 at the prior mean;
- platform null: the oracle run with lax.map instead of vmap, or on another device;
- native band: two independent oracle ensembles.

Flow-Lenia is a discrete map whose step is part of its definition, so v1's halved-dt null is replaced by the platform null.

### 6.2 Acceptance before any agent is run

1. **Ordering.** B0 < B1 < B2 < B3 < B5 on OES, each gap at least 3 paired SE.
2. **θ matters.** The prior-mean control falls below B3 at h ≥ 2. If it does not, identification is pointless: widen the prior or choose other parameters.
3. **Actions matter.** Ignore-actions falls below B3 on program classes (c) and (d).
4. **The budget binds.** B2 at budget lies between B1 and B3, ideally near the middle, and B2 with 10× the budget closes part of the gap.
5. **Envelope.** Maximal admissible programs keep the numerics finite and do not wipe out bodies.
6. **Audits.** Φ is θ-independent (hand-designed here); keys are secret; no θ hash is exposed; response time does not depend on state; the platform null stays inside the native band.

### 6.3 First pilot: gliders with hidden Flow-Lenia parameters

- **θ** = (R, Δm, λ_s, λ_h), applied to all 20 kernels: m ← m + Δm, s ← λ_s·s, h ← λ_h·h. This is 4 of the 261 parameters.
  - Prior: boxes of about ±15% around A_gliders, trimmed by a viability scan (4–12 bodies after burn-in, none lost to extinction or blow-up in 300 ticks, speed above 0.5 px per tick).
  - Ladder for later rounds: 4 → 20 (per-kernel h) → 261 → a neural level 0 from track 1.
- **Flow noise 0.5 stays public.**
- **Port.** Build the wind channel from Section 3.3, option 1.
  - Calibrate σ_w by requiring that background wind keeps the viability statistics within the native band.
  - Express aimed steering in nats per degree of heading change (the hand-written rule turned gliders 19°, 35 of 46 runs the same way).
  - Set c_max, κ_ep and κ_tot from those numbers.
  - Keep the matter-kick world as a norm-budget variant for comparison.
- **Views.** Block view (192 numbers) as the primary observed level; object view as a second world with the same θ and a different secret; `population` as level 2.
- **Suite.**
  - 64 H items: P = 16, h ∈ {1, 2, 4, 8, 16} at level 1 and {16, 32, 64} at level 2, R = 16, program classes (a)–(d).
  - 32 L items: from μ without burn-in, queried during the 50-tick formation of gliders, a strongly θ-sensitive transient.
- **Compute.**
  - Truths: about 64 × (16 + 16 × 64) ≈ 67k member-ticks, 2.5 CPU-hours.
  - Ceiling training data: at least the closure study's 47k member-ticks; more helped.
  - B2: for example 1,000 θ draws × 4 members × 100 ticks = 400k member-ticks, about 15 CPU-hours.
  - Use a rented Prime GPU for B2, B3 and the viability scan. The truths fit on CPU.
- **Order of work.** Viability scan and prior; wind port and σ_w; suite, truths and references; baselines B0–B5 and controls; budgets chosen by the acceptance checks; a scripted-provider smoke test through the v1 harness path; first model rollouts.

### 6.4 Open decisions for the lead

1. H items primary, L items as the θ stratum, P items out of the pilot?
2. The minimal hidden set, including dropping permutations and requiring prior-predictive training for any learned Φ?
3. "SBI plus amortised filtering" as the core task at low dim θ, with dim θ as the dial toward emergent-level modelling, or a public generator over architectures now?
4. Gliders port: wind channel (information budget) or matter kick (norm budget)? Must every track-1 world declare a matched input-noise channel?
5. Budget values (T_max, reset cost, c_max, κ_ep, κ_tot); closed-loop exploration allowed; common random numbers off or a separate lab mode?
6. OES as the primary metric, and the RL reward map (for example clip(OES / OES_ceil, 0, 1), or a v1-style log map).
7. Predictor program (recommended) or samples-only for the smoke pilot; a GPU in the predictor sandbox?
8. The agent's compute envelope, which sets how far brute-force SBI goes.
9. Aimed exam programs built from revealed histories (recommended, since blind programs barely register)?
10. Suites of several worlds from one public generator, making the prior part of the task?

## References

- [GR07] T. Gneiting, A. E. Raftery, "Strictly proper scoring rules, prediction, and estimation", JASA 102(477):359–378, 2007. VERIFIED (citation; energy score strictly proper for finite first moment, via a citing source).
- [SH15] M. Scheuerer, T. M. Hamill, "Variogram-based proper scoring rules for probabilistic forecasts of multivariate quantities", Mon. Wea. Rev. 143(4):1321–1334, 2015. VERIFIED (NOAA abstract; propriety and bias blindness via citing sources).
- [F14] C. A. T. Ferro, "Fair scores for ensemble forecasts", QJRMS 140:1917–1923, 2014. VERIFIED (abstract). The fair energy-score U-statistic is the multivariate analogue of his fair CRPS.
- [PT13] P. Pinson, J. Tastu, "Discrimination ability of the energy score", DTU working paper, 2013. VERIFIED only through citing papers.
- [ZB19] F. Ziel, K. Berk, "Multivariate forecasting evaluation: on sensitive and strictly proper scoring rules", arXiv:1910.07325, 2019. VERIFIED (abstract: the energy score detects errors "also regarding dependencies" comparably well, contradicting earlier studies).
- [CBL20] K. Cranmer, J. Brehmer, G. Louppe, "The frontier of simulation-based inference", PNAS 117(48):30055–30062, 2020. VERIFIED.
- [W10] S. N. Wood, "Statistical inference for noisy nonlinear ecological dynamic systems", Nature 466:1102–1104, 2010. VERIFIED (synthetic likelihood from phase-insensitive summaries for chaotic dynamics).
- [M13] B. B. Machta, R. Chachra, M. K. Transtrum, J. P. Sethna, "Parameter space compression underlies emergent theories and predictive models", Science 342:604, 2013. VERIFIED in `hierarchical_worlds_litreview.md`.
- [S14] C. Salge, C. Glackin, D. Polani, "Empowerment – an introduction", arXiv:1310.1863, 2014. VERIFIED in `lit2/cross-level-control.md`.
- [R24] T. Rainforth, A. Foster, D. R. Ivanova, F. Bickford Smith, "Modern Bayesian experimental design", Stat. Sci., 2024. VERIFIED in `lit2/cross-level-control.md` (expected information gain about parameters differs from that aimed at predictions; adaptive design can fail under misspecification).
- Alchemy (Wang et al. 2021, arXiv:2102.02926): information revealed is not information used, so never reward expected information gain. VERIFIED in `lit2/cross-level-control.md`.
- The Gaussian KL chain rule, Girsanov, data processing for KL and χ², χ² tensorisation, and the Cauchy–Schwarz χ² mean-shift bound: MEMORY (standard: Cover and Thomas; Liptser and Shiryaev).
- I. Mironov, "Rényi differential privacy", CSF 2017. MEMORY.
- Project numbers: closure ceilings, divergence, effect sizes and steering from `vw1/fresh/closure|inputs|media/results/summary.json`; cost 0.136 s per member-tick from `closure/results/summary.json`; v1 rules from `physim/README.md`, `LABWORLDS.md`, `blobround6_eval.py` and `rewards.py`.
