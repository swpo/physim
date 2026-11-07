# Track 1: more supervenient worlds (design, 2026-11-07)

A world is a level-0 evolution network F0 (hidden weights θ, explicit noise) plus a coarse-graining Φ, possibly stacked, as in `vw1/note/CATEGORY.md` (Defs. 4 and 9). This note plans how to get many more of them, by design, by search and by training. Citation tags: **VERIFIED** means I checked the source in this session (web, abstract or full text as stated). **MEMORY** means I did not; where an earlier review verified it, the file is named. Earlier reviews are cited by file name in `scratchpad/` (for example `lit2/ml-multilevel.md`).

The one new result is pilot **P0**. It works out the lead's pooling example in closed form (`pilot_pooling.py`, `pooling.json`, `pilot_pooling_tau.py`, `pooling_tau.json`; 8.6 CPU-minutes):
- A reconstruction autoencoder picks the *worst* block feature in a conservative world.
- A closure objective picks a tapered window at short horizons. That window becomes exactly the block sum as the horizon grows.
- Invariance to within-block transport forces the block sum by architecture alone.

## 0. Summary

- **Build first.**
  - Level-0 families parametrised by network weights θ drawn from a prior: a mass-conserving "transport NCA", multi-species Flow-Lenia, and a random RNN as the no-space control.
  - A Φ library: designed (pooled conserved densities and moments, trackers) and learned under declared biases (locality, equivariance, invariance to declared micro moves, closure with a non-collapse term).
  - Selection by gates and a Pareto front computed with the `vw` certificates.
- **Avoid.**
  - Learning Φ by reconstruction alone (P0).
  - Optimising closure without a non-triviality term: constant and near-iid levels are closed.
  - Publishing a Φ trained on the hidden instance: it is a statistic of θ (§5).
- **Experiments, by value per cost:** E1 the pooling result on nonlinear worlds; E2 random transport-NCA families with screening; E3 random RNNs with learned subspaces; E4 a JAX port of one collective world; E5 learned object slots. Pilots E1-E4 fit on CPU. The GPU phase is about 60-250 GPU-hours in total, an estimate to be checked first by a 10-minute throughput benchmark.

## 1. Survey: learning a coarse-graining, and searching for dynamics

**Validity test (our sense).** A CoarseGrain is a deterministic causal transducer of level 0. It has memory m, readout y = φ(x, m), and no noise, input or key arguments (S1-S3 in CATEGORY.md). A learned map qualifies once it is frozen and evaluated deterministically:
- an encoder mean, not a sample;
- slot initialisations fixed or computed from x, not drawn at random;
- no dropout.

A recurrent encoder is a transducer with memory, which is allowed. Cost below means the cost for *our* scale (2 × 128² fields, about 10⁵-10⁶ frames). Data generation dominates it: Flow-Lenia costs 0.136 CPU-s per member-tick (`fresh/closure/results/summary.json`).

**Learning a coarse-graining.**

| Method | Objective | Inductive bias | Valid CoarseGrain? | Cost |
|---|---|---|---|---|
| RSMI (Koch-Janusz & Ringel 2018; MEMORY, verified in `lit2/ml-multilevel.md` [24]). Optimality: Lenggenhager et al. 2020 (VERIFIED, abstract). IB relevance: Gordon et al. 2021 (MEMORY, verified in `lit2/probing-depth.md`) | max I(H; E): block code H against the environment E beyond a buffer | locality (block plus buffer), small code | yes, with a deterministic code (sign or argmax). A perfect RSMI map does not increase interaction range | MI estimation per block; 1-5 GPU-h |
| Neural Information Squeezer, NIS (Zhang & Liu 2022, Entropy 25:26; VERIFIED, full text) | stage 1: one-step micro prediction through a q-dim macro bottleneck (MSE or MAE); stage 2: choose q by sweep, maximising dimension-averaged causal emergence | encoder = invertible net (RealNVP) then projection; decoder = inverse with noise padding | yes, memoryless. The authors reject constant maps ("meaningless") and state "can only work on small data set" | tested only on toys (2-D oscillator, 8-state chain, 16-state Boolean net); a q sweep multiplies cost |
| NIS+ (Yang et al. 2024, Natl Sci Rev nwae279; VERIFIED, full text) | NIS plus maximised effective information by inverse-probability reweighting toward a uniform macro distribution, with a reverse model; Lagrangian with a prediction-error threshold | as NIS; assumes Markov macro dynamics | yes, memoryless | SIR, boids, Game of Life (supplement), fMRI with 100 parcels; KDE-based weights should scale poorly with q (my inference) |
| Dynamical independence (Barnett & Seth 2023, PRE 108:014304; MEMORY, verified in `lit2/emergence-closure.md`) | minimise micro → macro transfer entropy (DD); search the Grassmannian | linear projection; closed form for state-space models | yes, linear and memoryless | CPU for n ≲ 10³ |
| VAMPnets / TICA (Mardt et al. 2018, Nat Commun 9:5; VERIFIED, abstract) | maximise the VAMP score of lag-τ features (slowest processes) | two lobes, soft state assignment | yes. Its optimum is a slow subspace of F0's transfer operator, which is relevant to §5 | 1-10 GPU-h |
| Koopman AE (Lusch, Kutz & Brunton 2018; VERIFIED, abstract); SINDy AE (Champion et al. 2019; VERIFIED, abstract); LED (Vlachas et al.; MEMORY, verified in `ml-multilevel.md` [21]); Chen et al. 2025 (VERIFIED, abstract) | reconstruction + latent dynamics (linear, sparse symbolic, or neural SDE) | latent linearity or sparsity; reconstruction-led | yes (encoder) | 1-10+ GPU-h |
| Self-predictive / bisimulation representations: ZP self-prediction with stop-gradient (Ni et al. 2024, ICLR; VERIFIED, abstract); DBC (Zhang et al. 2021, ICLR; VERIFIED, abstract) | predict own next latent; or match latent distance to bisimulation distance | ZP is closure as a loss; bisimulation is strong lumpability (E2) as a metric | yes; history encoders are transducers | 1-10 GPU-h; prone to collapse (§5) |
| Causal feature learning (Chalupka, Perona & Eberhardt 2016, AISTATS; VERIFIED, abstract) | cluster micro states by their interventional effect distribution | discrete macro variables | yes, as a partition | needs interventions, which we have |
| Object-centric: Slot Attention (Locatello et al. 2020, NeurIPS; VERIFIED, abstract), SAVi (Kipf et al. 2022; MEMORY), C-SWM (Kipf, van der Pol & Welling 2020, ICLR; VERIFIED, abstract) | reconstruction through slots; C-SWM uses a contrastive transition loss with no pixels | permutation-symmetric slots | only with deterministic slot initialisation; SAVi carries slots, which gives memory | 10-100 GPU-h. Our `vw.objects.BlobTracker` is the designed alternative |
| Conserved quantities: AI Poincaré (Liu & Tegmark 2021, PRL 126:180604; VERIFIED, abstract) | find functions constant along trajectories | none | yes. These are exact morphisms onto identity-law levels (CATEGORY §3) | small |
| Exact search for coarse-grainings: Israeli & Goldenfeld 2006 (MEMORY, verified in `lit2/emergence-closure.md`) | exhaustive search for a projection P and rule f_B with P·f_A^T = f_B·P | supercells | yes, exact (E1) | precedent for brute force over Φ |

**Searching for interesting dynamics.**

| Method | Search objective | Notes for us |
|---|---|---|
| IMGEP with a learned goal space (Reinke, Etcheverry & Oudeyer 2020, ICLR; VERIFIED, abstract); IMGEP + curriculum + gradient (Hamon et al. 2025, Sci Adv; MEMORY, verified in `lit_alife-embodied.md`) | diversity in an AE-learned behaviour space | Hamon: 486 movers out of 1,600 searched parameter sets, against 30 out of 117,000 by random search (earlier review). Search is necessary for rare phenomena |
| Leniabreeder (Faldor & Cully 2024, arXiv:2406.04235; VERIFIED, abstract) | quality-diversity (MAP-Elites with hand descriptors; AURORA with unsupervised descriptors) | QD archives map directly onto "a family of worlds with diverse level-1 behaviour" |
| ASAL (Kumar et al. 2024, arXiv:2412.17799; VERIFIED, abstract) | foundation-model (CLIP or DINOv2) scores: target prompt, open-endedness, illumination | substrates: Boids, Particle Life, Game of Life, Lenia, NCA. It scores appearance, not closure or controllability, so we use it at most for screening |
| Curiosity-driven AI scientist on Flow-Lenia (Michel et al. 2025; MEMORY, verified in `lit_alife-embodied.md`) | open-loop parameter search on global statistics | the closest precedent for an agent-led search |

**Gaps.**
- I found no method that learns a Φ for an *open* (input-driven) system and certifies closure under interventions.
- I found none that learns a *stacked* chain. NIS+ varies q but does not stack (VERIFIED).
- A search for learned CA coarse-graining with closure found only non-CA closure work (Chen et al. 2025).

## 2. Design space

### 2.1 Level-0 families

The thing to hide is θ, so families should be parametrised by weights with a prior. The exam can then draw instances that no one has looked at.

| Family | θ (hidden) | Built-in structure | Status and cost |
|---|---|---|---|
| Linear-Gaussian (`vw.lingauss`) | A, Q | closed-form certificates | done; used to calibrate estimators |
| Flow-Lenia, multi-species | kernel radii, rings, growth μ/σ, local parameter fields | mass conservation, localised bodies | JAX port done (`port/flowlenia_jax.py`); 0.136 CPU-s per member-tick at 128² |
| **Transport NCA** (new): x′_j = Σ_i x_i π_θ(i→j \| N_i), with π a softmax over the 5-point stencil from a small conv net, plus noise on the logits | conv weights | exact mass conservation and positivity by construction (the Flow-Lenia lesson in `lit_alife-embodied.md`); local | about 50 lines of JAX; expected much cheaper than Flow-Lenia |
| Lenia, Particle Lenia, particle systems | kernels, interaction tables | bodies; particle-number conservation | Particle Lenia's rotor is "quite sensitive to small perturbations" (earlier review) |
| Hand-designed physics (collective worlds) | rate constants | rich, rubric-graded behaviour (fed vortices: splitting to generation 9-10; CIPS: dividing cells; Marangoni rods: heritable kinds) | numpy only: needs a JAX port or `vw.opaque.host_level`. Vortices and phase_membrane are easy (spectral or reaction-diffusion); the rods are hardest (Cahn-Hilliard + nematic + Stokes) |
| Random RNN, x′ = (1−α)x + α tanh(gWx + b) + σξ | W, b, gain g | none: no space, no conservation; chaos for g > 1 at large n (Sompolinsky et al. 1988, MEMORY) | the pure black-box end; CPU-cheap |

### 2.2 Coarse-graining families

- **Designed.**
  - Pooled conserved densities and their moments at block size b. Φ_coarse is the block mean of each channel plus the mean of A_sum².
  - Trackers (Φ_objects: 12 slots, with memory).
  - Population statistics at level 2.
  - Exact quotients by symmetries of F0 (Atay's orbit lumping; MEMORY, verified in `lit2/emergence-closure.md`).
- **Learned.** An encoder class plus an objective. The class carries the biases:
  - *locality*: receptive field ≤ block plus halo;
  - *translation equivariance*: shared weights, stride b;
  - *invariance* to declared micro moves, either by architecture or by augmentation;
  - *conservation*: Φ must contain, or let a decoder recover, block sums of conserved densities;
  - *width* or an information bottleneck: q, or β;
  - *memory*: a recurrent encoder or slots;
  - *discreteness*: VQ or argmax.
- **The objective chooses within the class.**
  - reconstruction (AE, PCA);
  - closure (self-prediction, VAMP, contrastive);
  - relevance (RSMI);
  - effective information (NIS+);
  - interventional clustering (Chalupka et al.).

### 2.3 How an inductive bias defines the coarse-graining: the pooling example made precise

Take a lattice field x ≥ 0 with blocks B_j, and a block-local equivariant encoder y_j = φ(x|_{B_j}). Two short arguments and one computation follow.

**(A) Invariance by architecture.**
- If φ is invariant to *permutations* within a block, it is a symmetric function. It can be written ρ(Σ_i ψ(x_i)) (DeepSets, Zaheer et al. 2017, MEMORY). Φ_coarse is the case ψ = (x, x²).
- If φ is invariant to within-block *transports* x ↦ x + t(e_i − e_k), with i, k in B and x kept ≥ 0, it is constant on each slice {x_B ≥ 0 : Σ x_B = m}. Pairwise moves connect any two points of the slice, so φ = g(Σ_{i∈B} x_i).
- If the decoder must also return the block mass ("preserve the local function"), g is injective. Φ is then block-sum pooling up to reparametrisation.
- More generally, requiring the decoder to return the block integrals of a local observable f, with no more width than f has, gives pooled f.
- *Choosing f, or the group of moves to ignore, is choosing Φ.* No training is needed.

**(B) Selection by dynamics.** Now let the objective choose. P0 uses a 64-site ring and 8-site blocks, with one linear feature w per block shared by all blocks. The closure ceiling c(τ) is computed in closed form, with the whole level-1 past and the same Kalman formulas as `vw.lingauss`.

*Conservative world* (A = I − 0.2·Lap, conservative bond noise Q = Lap):

| Feature w | cos to uniform | c(1) | c(4) | c(32) | I(y_≤t; y_{t+1}) |
|---|---|---|---|---|---|
| block sum | 1.00 | 0.981 | 0.949 | 0.916 | 8.0 nats |
| PCA (width-1 linear AE) | 0.00 (alternating) | 0.965 | **0.034** | 0.018 | 0.2 |
| TICA (lag 4) | 0.95 (tapered) | 0.997 | 0.987 | 0.906 | 11.1 |
| closure-optimal for τ* = 4 | 0.91 (tapered) | 0.999 | 0.991 | 0.887 | 11.0 |

Random positive windows have median c(4) = 0.89. Random signed windows have median 0.58.

As the target horizon τ* grows, the closure-optimal window flattens into the block sum. Its cosine to uniform is 0.892, 0.913, 0.959 and 0.9999 at τ* = 1, 4, 16 and 64. At τ* = 64 its ceiling, 0.92483, equals the block sum's (0.92474).

*Damped world* (γ = 0.05): PCA, TICA and the closure optimum all lie within cosine 0.96 of uniform, and the objective is flat (random positive median c(4) = 0.965 against a best of 0.995).

*Fast-forgetting world* (γ = 0.5, D = 0.05):
- every feature has c ≥ 0.975 up to τ = 8;
- c is undefined from τ = 16, because the oracle and the unconditional variances coincide;
- I₁ is only 1.1 nats.

The ceiling carries no information here.

**Reading (B).**
1. **Reconstruction picks the worst feature.** The conservative stationary field is nearly white (top eigenvalue ratio 1.05) and slightly heavier at high wavenumber, so PCA picks the fastest mode.
2. **Closure picks a smooth window** that widens with the horizon until it is block pooling: only the conserved density survives (the hydrodynamic picture; Forster 1975, MEMORY).
3. **The choice is ill-posed** when level 0 forgets faster than the horizon of interest.

**The lead's example, precisely.** An autoencoder whose encoder is local and equivariant has block averaging as its optimum in two cases:
- it must be invariant to within-block transport, and its decoder must return the block mass (exact, by architecture); or
- it is trained for long-horizon closure on local conservative dynamics (asymptotically).

It does *not* have block averaging as its optimum when trained for reconstruction.

**Beyond pooling.** Pooling fails when sub-block structure persists. In Flow-Lenia gliders, bodies (12.7 px) are as large as blocks (16 px) and carry heading. The coarse ceiling falls to 0.49 at τ = 8. The right quotient there is by body-shape fluctuations: keep the moduli (position, heading, mass) and drop the rest. That is the object view. The general recipe:

> Φ = quotient by a declared set of irrelevant micro moves + a choice of what to keep, with the objective tuning what the declaration leaves open.

## 3. Selection criteria (computable)

A world passes gates, then sits on a Pareto front. The reference values are the gliders world's (`fresh/*/results/summary.json`).

| Criterion | Quantity | Tool | Target | Gliders |
|---|---|---|---|---|
| Closure profile | ceiling c(τ, p), τ = 1..32, best-of predictors; closure horizon τ½ (first τ with c < 0.5); Atay split (leak versus memory) | `vw.closure` (linear) + the fresh best-of predictors | c(1) ≥ 0.8 and 4 ≤ τ½ ≤ 64 (neither ≈1 forever nor ≈0 at once) | coarse: 0.991 / 0.495 at τ = 8 / 0.078 at 32; objects: 0.833 / 0.434 / 0.048 |
| Non-triviality | predictive information I(y_≤t; y_{t+1}); entropy rate; participation ratio of Cov y; V0 > 0; NTIC (Bertschinger et al., MEMORY, CATEGORY [B]) | Gaussian proxy from `vw.closure` residuals | well above the constant map; reject when I₁ ≈ 0 or when the level is iid | to compute |
| Hiddenness | leak: hidden fraction of level 0 and nats recovered from level-1 pasts | `vw.leak` | most of level 0 unreadable | 16597-number tracker memory: audit |
| Input visibility within budget | input capacity (bits per episode under `Admissible`); blind versus aimed response | `vw.input_capacity`, twin runs | blind inputs visible within 1-4 ticks | blind ≤ 0.013 (fails); aimed flank kicks turn the body toward the source in 19 of 24 cases |
| Observation rate | r(p) | `vw.observation_capacity` | finite, port part reported separately (Prop. 7) | — |
| Conservation | drift of declared invariants; discovered invariants | `vw.invariant_drift`; AI-Poincaré-style search | ≤ 1e-10 for declared invariants | 1.9e-14 |
| Life-like structure | rubric rung (`alife/RUBRIC.md`: L2 individuals … L7 heredity) | tracker statistics | ≥ L2 for an object view | L4b-L5 by my reading (not judged); fusions and fissions 23 per 100 ticks |
| Identifiability of θ | Fisher of the observed trajectory with respect to θ (sloppiness spectrum) | `vw.fisher` (1-2 ticks only in chaotic cores) | a few stiff directions, not zero and not full rank | to compute |
| Diversity over θ | behavioural distance between B_W for θ, θ′ from the prior | ensemble statistics of level 1 | instances differ, so the exam cannot be memorised | — |
| Cost | member-ticks per second at batch | timing | ≥ 10³/s on GPU | 7/s on one CPU process |
| Robustness to resolution | closure profile under dt/2 and dx/2 (refine, stride) | `vw.refine(check=)`, `vw.stride` | unchanged within SE | memory Φ must be re-declared per stride (Prop. 10e) |

Closure is relative to a process law (CATEGORY Def. 8). It must be certified under the exam's input distribution (programs from `random_program`), not only under free runs.

## 4. Pipeline and first experiments

**Pipeline.** Each stage feeds the next; stages 2-5 repeat per level when stacking.
1. **Calibrate** the estimators on `vw.lingauss` closed forms. This is done for P0's quantities.
2. **Generate level 0**: a family with a prior on θ.
3. **Screen** cheaply over about 10⁴ draws: no blow-up, no death, activity above a floor, conserved quantities exact, spatial structure present.
4. **Search** (QD or IMGEP) on the survivors. Its descriptors are our criteria (closure horizon, I₁, rung), not VLM appearance.
5. **Propose Φ**:
   - the designed library (pooled conserved densities and moments at b ∈ {4, 8, 16}, tracker);
   - learned encoders under declared biases, trained on draws from the *family*, never on the instance to be examined.
6. **Certify** with the §3 table.
7. **Freeze and publish**: F0's code, the prior, Φ and the ports. Hold θ and the keys.

Stacking applies stages 5-6 to level 1, and the closure defects add by the chain rule (Prop. 6).

**Experiments, ranked by value per cost.**

**E1. The pooling result on nonlinear worlds.**
- *Setup.* Transport NCA and Flow-Lenia, b = 8. Train block-local equivariant encoders of width q ∈ {1, 2, 4} under four objectives:
  - reconstruction;
  - closure (VAMP-2 or ZP with stop-gradient);
  - closure + variance (anti-collapse) term;
  - transport-invariance augmentation.

  Compare each with pooled densities and moments.
- *CPU pilot.* Transport NCA at 64², about 2·10⁴ frames, linear and tiny MLP encoders. About 1 CPU-hour, with one process under nice (the cost is assumed and must be measured).
- *GPU.* Flow-Lenia at 128², 10⁵-10⁶ frames, conv encoders, 3 seeds × 4 objectives × 3 widths, plus certification of each Φ (about 3·10⁶ member-ticks). Estimate 10-30 GPU-h.
- *Changes the plan if:*
  - a learned Φ beats Φ_coarse's c(8) = 0.49 by more than 0.1 at matched width and I₁, with readable features (momentum- or heading-like). The learned route then becomes the default for new worlds.
  - nothing beats pooling. We then keep designed Φ and use learning only to *audit* them.

**E2. Random transport-NCA families with screening and QD.**
- *Setup.* Draw θ from the prior. Screen, run MAP-Elites over the descriptors (τ½, I₁, number of bodies), certify the top candidates, and Φ = pooled densities plus a tracker.
- *CPU pilot.* 300 draws × 200 ticks at 64², with screens only. About 1-2 CPU-hours.
- *GPU.* 10⁴-10⁵ draws, certify about 100. Estimate 20-80 GPU-h.
- *Changes the plan if:*
  - the gate pass rate is ≥ 10%. Random families then suffice, and each exam instance can draw a fresh θ, which is the best answer to hiding θ.
  - it is ≤ 1%. We then invest in search (IMGEP or QD) and the selection leak of §5 grows.

**E3. The black-box end: random RNN, learned subspaces.**
- *Setup.* n = 256, a gain sweep g ∈ [0.5, 3]. Φ by dynamical-independence subspaces (Barnett-Seth), by VAMP, and by random projections. Measure the closure profile against I₁.
- *Cost.* CPU minutes; no GPU needed.
- *Changes the plan if:* no learned Φ shows a closure band with non-trivial I₁ in any g regime. Then locality and conservation are *necessary* biases, and the "arbitrary level 0" track should require them.

**E4. Design track: JAX port of fed vortices.**
- *Setup.* A pseudo-spectral vorticity solver with fuel, with Φ = block-pooled vorticity and fuel plus a vortex tracker.
- *CPU.* The port and certificates at 64² take a few CPU-hours and about a day of agent time. GPU is optional.
- *Changes the plan if:* a non-Lenia physics with natural invariants (circulation) gives a better closure band and input visibility than gliders. Hand design then stays a first-class source of worlds.

**E5. A learned object view.**
- *Setup.* A SAVi-style slot encoder with deterministic slot initialisation and a C-SWM-style contrastive transition loss, on gliders, against `BlobTracker`. Measure slot closure and how events (fusion or fission) are handled.
- *Cost.* Only a toy pilot fits on CPU (32², 1-3 bodies). GPU: 30-100 GPU-h.
- *Changes the plan if:* learned slots beat the tracker's c(4) = 0.63 and handle events. Trackers would then no longer need hand rules per world.

**GPU throughput.** The only measured cost is CPU: 0.136 s per member-tick for Flow-Lenia at 128², 20 substeps, float64. My FLOP-count estimate for an H100-class GPU in float32 is 10³-10⁴ member-ticks per second. *Measure it first*: a 10-minute benchmark on a rented Prime GPU. The world must then be *defined* with its float32 GPU presentation (CATEGORY Prop. 1); otherwise CPU and GPU runs are different worlds.

## 5. Risks

- **Degenerate coarse-grainings.**
  - Constant maps are exactly closed. In P0's conservative world the total mass (b = 64) has an undefined ceiling and I₁ = 0.005 nats.
  - Exact but thin levels also exist. The damped world's global mean is exactly closed (c = 1, an eigenvector of A) with I₁ = 1.2 nats.
  - Pooling trades closure against content. In P0, block size against I₁ runs 32.4 (b = 1), 21.7 (2), 8.0 (8), 1.4 (32). The gap at τ = 1 runs 0 (identity), 1.61 (b = 2), 0.51 (8), 0.07 (32).
  - Self-predictive objectives collapse unless the optimiser prevents it; Ni et al. analyse the stop-gradient technique (VERIFIED, abstract). The NIS authors reject constant maps by a prediction constraint (VERIFIED).
  - *Mitigation.* Always optimise and report closure *together with* I₁, rank and leak. Use contrastive or variance terms. Report the whole trade-off curve, not one point.
- **Reconstruction misleads.** P0's PCA feature has c(4) = 0.03. Never select Φ by reconstruction error.
- **Leakage of θ through a learned Φ** (for track 2).
  - A Φ trained on the hidden instance is a statistic of θ. VAMP features approximate F0's slow eigenfunctions, and NIS learns F0's macro dynamics. Publishing Φ publishes part of θ.
  - *Mitigations:*
    - train Φ on the *family* (amortised over θ drawn from the prior) or on sibling instances;
    - prefer designed, θ-free Φ such as pooled conserved densities;
    - measure the residual leak by predicting θ from Φ's weights across the family.
  - *Selection leaks too.* Accepting a world because it passed criteria narrows the posterior on θ. Publish the criteria and draw exam instances uniformly from the accepted set.
  - *Beyond θ, I would also hide:*
    - the noise keys and seeds (with them, replay is presentation-level; Prop. 1);
    - the instance's identity within the family;
    - Φ's training data and run;
    - the hidden port permutations (already hidden).
- **Ill-posedness.**
  - Learned Φ are unique only up to reparametrisation; NIS sweeps q by hand.
  - Objectives are flat when level 0 forgets fast (P0, fast-forgetting world).
  - Closure is law-relative: a Φ learned on free runs can lose closure under agent inputs, which is exactly the exam regime. Train and certify under the exam's program distribution.
- **The world is the network.** A trained or random F0 is ground truth by definition. The earlier concern about emulator fidelity (`ml-multilevel.md`, "no faithful long-horizon emulation of Lenia") therefore disappears. Numerical reproducibility across hardware takes its place.
- **Compute and disk.** Certificates need about 10⁴ trajectories plus oracle branches: hours per Flow-Lenia world on CPU (the gliders closure run took 2 × 55 CPU-min for 47k member-ticks). Keep npz outputs small (about 3.5 GB free).
- **Goodhart.** Searching on τ½ and I₁ will find odd worlds. Keep human review of videos and the RUBRIC anti-Goodhart gating.
- **Chaos.** Pathwise derivatives hold for about 1 tick (median error ≤ 2.2e-4 at 1 tick, disagreement from 4); use finite differences or likelihood ratios beyond that.

## Files

- `/home/user/evalwork/vecworld/program/track1/DESIGN.md`: this note.
- `/home/user/evalwork/vecworld/program/track1/pilot_pooling.py` and `pooling.json`: P0, 428 s on CPU. Three linear worlds; block-size sweep; uniform, PCA, TICA and closure-optimal windows at b = 4 and 8.
- `/home/user/evalwork/vecworld/program/track1/pilot_pooling_tau.py`, `pooling_tau.json` and `pooling_tau.log`: the τ* sweep, 88 s.

## References

- **VERIFIED (this session).**
  - Full text: Zhang & Liu 2023, Entropy 25:26, arXiv:2201.10154; Yang et al. 2024, Natl Sci Rev nwae279, arXiv:2308.09952.
  - Abstract: Mardt et al. 2018, Nat Commun 9:5; Lusch et al. 2018, Nat Commun 9:4950; Champion et al. 2019, PNAS, arXiv:1904.02107; Locatello et al. 2020, arXiv:2006.15055; Kipf et al. 2020, arXiv:1911.12247; Ni et al. 2024, arXiv:2401.08898; Zhang et al. 2021, arXiv:2006.10742; Lenggenhager et al. 2020, PRX 10:011037; Liu & Tegmark 2021, PRL 126:180604; Chalupka et al. 2016, arXiv:1512.07942; Chen et al. 2025, arXiv:2511.12842; Reinke et al. 2020, arXiv:1908.06663; Kumar et al. 2024, arXiv:2412.17799; Faldor & Cully 2024, arXiv:2406.04235.
- **MEMORY, verified in an earlier review.**
  - `lit2/ml-multilevel.md`: Koch-Janusz & Ringel 2018, Nat Phys 14:578; Vlachas et al., arXiv:2006.13431; Mordvintsev et al. 2020.
  - `lit2/probing-depth.md`: Gordon et al. 2021, PRL 126:240601.
  - `lit2/emergence-closure.md`: Barnett & Seth 2023, PRE 108:014304; Israeli & Goldenfeld 2006, PRE 73:026203; Atay et al. 2016.
  - `lit_alife-embodied.md`: Plantec et al., arXiv:2212.07906; Hamon et al. 2025; Michel et al. 2025, arXiv:2505.15998.
  - CATEGORY.md: Rosas et al. 2024 [R]; Bertschinger et al. 2006 [B].
- **MEMORY, not verified.** Zaheer et al. 2017 (Deep Sets); Kipf et al. 2022 (SAVi); Sompolinsky, Crisanti & Sommers 1988; Forster 1975.
