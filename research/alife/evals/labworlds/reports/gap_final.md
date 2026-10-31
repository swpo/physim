# How the collective's worlds differ from Blobkit, and what it would take to evaluate them in PhySim

Path prefixes used below:
- `BK/` = `packages/blobkit/blobkit/`
- `PHYSIM/` = `.venv/lib/python3.12/site-packages/physim/` (the installed physim 0.13.0.dev0; its source lives upstream, `environments/physim/README.md:3`)
- `GEN/` = `generators/physim/`
- `C/` = `research/alife/collective/contrib/`
- `T/` = `research/alife/threads/`

The world directories are listed in a key after the table in section C.

## Summary

- **Blobkit is general in its parameters, its wiring and its numerical scheme. It is not general in its operators.**
  - Its simulator is an IMEX-FFT scheme: explicit local terms, then an exact Fourier step for each mode (`BK/genome.py:1, 27-29`; `BK/soup/sim_cpu.py:195-222`).
  - The genome fills that scheme with one fixed set of terms.
  - A labkit world is any Python program.
- **Most of the gap is missing vocabulary inside that scheme, not a different architecture.**
  - Six of the eight met grand challenges are held by worlds that fit Blobkit's scheme: c34 ×2, c29, phase_membrane and c40. Each is a set of real fields on one periodic grid, stepped by explicit local and flux terms plus linear Fourier solves per mode.
  - These worlds need terms Blobkit lacks: products in any equation, conservative flux terms, clips and caps, k⁴ and Stokes symbols, and dealiasing.
  - The other two grand challenges need particles (SIBDH, c14) or labelling of each body (IBRM, c31).
  - x-genome's current keys reach none of the six. A genome widened enough to hold them has become a term list.
- **The collective's scoring pushed away from pure diffusion, but that is not a test against Blobkit.**
  - The rubric rewards non-Laplacian operators (`research/alife/RUBRIC.md:134`).
  - Two of the eight grand challenges require a Laplacian-only twin that fails (`research/alife/collective/STATE.md:110, 114`; `research/alife/collective/SCORE.md:35-41`). That twin replaces the world's own operator inside the same world. It is never compared with Blobkit.
  - Better evidence that Blobkit-family dynamics did not produce these behaviours: x-genome's own negative results (`T/fisim-beyond-laplacian/FINAL.md:17, 53-55`).
- **PhySim's dependence on Blobkit is wider than the bundle layer.**
  - The scheduler, sensors, member seeding and scorer are written against a generic stepper seam.
  - The request grammar and the budget are tied to dt = 0.02 through the module constant `SIM_DT` (`PHYSIM/blobround6.py:20, 60-70`; `PHYSIM/blobround6_explore.py:40, 65`). `adjust` lasts a fixed 250 ticks (`PHYSIM/blobround6.py:23`).
  - The slot counts, dt and the 50-tu horizon are also hard-coded in `PHYSIM/container_worker.py:38` and `PHYSIM/data/agent_spec.txt:36, 68-75`.
  - The bundle layer holds the rest: `_validate_physics`, `make_oracle`, `NUMERICS`, the identity hashes, and the preparation and control recipes.
- **Recommendation (revised).**
  - Make the stepper seam a declared contract (option 3, Stage 0). Every option needs this.
  - Then widen Blobkit, keeping its scheme, into a term list (option 2). Make that the default language for field worlds.
  - Use raw-Python plugins only for the particle, labelling and event worlds (c14, c31, flow-lenia).
  - Pilot phase_membrane both as a raw plugin and as a translation. That tests whether translation preserves behaviour.
- **Three gaps remain under any option:**
  - **Noise.** Five of the seven grand-challenge holder worlds are deterministic after initialization. PhySim needs a noise policy: dynamics noise, read noise, or deterministic truths with K set by policy.
  - **Time.** Count native steps per window, not tu. phase_membrane and c34 show divisions within a 2500-step window. c40 and c14 do not, at any affordable budget.
  - **Ports.** A port is one index that is both read and driven, with a non-negative amplitude. That meaning breaks for derived flows, tensors, conserved fields, particles and erasure.

## A. What Blobkit is, and in what sense it is general

**Equations** (`BK/genome.py:11-15`; implemented at `BK/soup/sim_cpu.py:196-215`):

- du_i/dt = Du_i ∇²u_i + λ_i u_i − u_i³ + k1_i − Σ_c K[i,c] x_c − Σ β x_c x_c2 + noise
- dx_c/dt = (Σ_a W[c,a] g_c(u_a − u0_a) − x_c)/τ_c + D_c ∇²x_c

Here g is either the identity or tanh(max(z − thr, 0)/sc).

**What that rules out:**
- **Zero or positive cubic terms, and quintic terms.** The cubic is written as −u³ (`BK/genome.py:12`; `BK/soup/sim_cpu.py:199`). Any negative cubic coefficient is only a choice of units: a shift and an amplitude rescale map −r u³ + b u² + a u + c onto −v³ + λv + k1, and K, W, thr and sc absorb the scale. The catch is that PhySim's noise (0.002) and injection amplitude are fixed in field units, so the rescale changes their relative strength.
- **Nonlinear terms in channel equations.** The wiring is bipartite: activators drive channels, and channels feed back into activators. There is no channel–channel drive, and no nonlinear term of any kind in a channel equation.
- **Products of cubic order or higher, clip and `min`.**
  - Quadratic products in activator equations can be emulated. A relay channel with τ = dt, D = 0 and g = id holds the previous step's u − u0 exactly, because explicit Euler with dt/τ = 1 sets x = W·z. Feeding that relay into `bilin` then gives u·x and u·u terms with a one-step lag.
  - Each relay costs one extra public port (`PHYSIM/bundles.py:266`). `bilin` acts only inside activator equations (`PHYSIM/bundles.py:329-338`).
  - The critic ran this check (relay matched the previous step to 3e-7 in f32). I confirmed the mechanism from the step code.
- **What PhySim actually enforces.**
  - PhySim never calls `genome.validate` (no call in `PHYSIM/`, `BK/soup/` or `GEN/`).
  - It requires λ > 0, τ > 0 and sc > 0, and D, Du ≥ 0, with |coefficient| ≤ 1e6 (`PHYSIM/bundles.py:310-326`).
  - It caps the counts at 1–16 activators, 1–48 channels, at most 64 fields and at most 4096 `bilin` terms (`PHYSIM/bundles.py:294-309`).
  - Du = 0 is accepted (`PHYSIM/bundles.py:324`; `schemas/README.md:55-56`). Blobkit's own validator requires Du > 0 (`BK/genome.py:86-87`).
- **Vacuum exactness is a Blobkit convention, not a PhySim requirement.** "Every drive vanishes at the vacuum" (`BK/genome.py:23-25`) holds only for thr ≥ 0. With thr < 0, a tanh channel has g(0) ≠ 0 (`BK/soup/sim_cpu.py:209`). PhySim checks neither that u0 is a root nor that thr ≥ 0 (blobkit verifier, tested).

**State.**
- Real scalar fields on one periodic N×N grid, stacked as [activators | channels] (`BK/genome.py:321-326`).
- Vector or tensor components can be stored as extra real fields. What is missing is terms that mix those components.

**Numerics.**
- Each step is explicit Euler on the reaction terms, then activator noise, then exact diffusion exp(−Dk²dt). This is first-order Lie splitting (`BK/soup/sim_cpu.py:86-90, 195-222`).
- dx = 0.5 and dt = 0.02 are hard-coded on the soup path (`BK/soup/sim_cpu.py:59`; `BK/soup/sim_v1.py:104`).
- PhySim pins L = 128, a 256² grid, float32, periodic boundaries and 1 worker (`PHYSIM/bundles.py:24-33`).

**Noise.**
- Additive iid Gaussian noise on activators only: noise·√dt·N(0,1) per cell per step (`BK/soup/sim_cpu.py:110, 217-220`).
- The amplitude is a bundle field, `noise_coefficient`, in [0, 1] (`PHYSIM/bundles.py:339-341`), passed to `init_soup` (`PHYSIM/bundles.py:469-471`).
- The generator hard-codes 0.002 both in its oracle and in the preparation identity (`GEN/eval_preparation.py:73, 91`; `GEN/build_evaluation_bundle.py:247`).
- Channels are never noised. There are no events during a run.

**The sense in which it is general.**
- Its range comes from the number of species, signed wiring, time scales and length scales.
- **Kernels.** A relaxing, diffusing channel acts as a lagged screened-Poisson filter. At steady state x̂ = W ĝ/(1 + τDk²); this is a derivation, not in the code.
  - Each channel contributes one positive, monotone 2-D Yukawa kernel. With signed K·W, the net kernel is a signed sum of n of them.
  - Two channels already give a centre-surround kernel. My check, with lengths 1 and 3 and weights 1 and −0.6: zero crossing at r ≈ 3.3, minimum at r ≈ 4.7.
  - A narrow positive ring is practically out of reach. The critic's least-squares fit to a Gaussian ring left 30% error with 8 terms. An FFT kernel multiplier would be cheap to add instead (`T/fisim-beyond-laplacian/xgenome.py:67-73, 142-144`).
- **Model family.** The reference worlds are built from the three-component Purwins model (`BK/genome.py:109-123, 161-175`). Calling it the FitzHugh–Nagumo dissipative-soliton family is our characterization; that phrase is not in Blobkit.
- **Positivity.** The exact spectral step does not preserve positivity. On the PhySim grid, a delta diffused for one step has negative lobes of 1.1% of peak at D = 0.3 and 2.4% at D = 1 (my check). Bounded densities therefore need finite-volume fluxes and clipping. Advective terms also need dealiasing, which Blobkit lacks. This is where the FFT-only scheme really stops.

**A labkit world is a different kind of object.**
- It is one Python file with META, `init(seed, size)`, `step(state)` and `fields(state)`, plus optional `particles`, `matter` and `damage` hooks (`research/alife/labkit/world.py:3-34`).
- "Everything else (numerics, parameters, RNG) lives inside the state. A world must be deterministic given the seed" (`research/alife/labkit/world.py:56-57`).
- META declares a default grid and periodicity (`research/alife/labkit/world.py:10, 17`). Its `dt` is "for reporting" only (`research/alife/labkit/world.py:12`); the real dt lives in the state, or in P, which WORLD_P can override.
- META has no length unit for field worlds. `domain` applies to particle worlds only (`research/alife/labkit/world.py:19`).
- There is no source hook. The only intervention is erasure through `damage` (`research/alife/labkit/world.py:34-46`).
- World parameters are module-level and read from WORLD_P at import (c34 `world.py:60`; c31 `world.py:35`; c53 `world.py:29`). So world files are not reentrant.

**The x-genome thread is the existing bridge, and it was never merged.**
- `T/fisim-beyond-laplacian/xgenome.py` (188 lines) adds these keys: `band`, `ch` (Cahn–Hilliard on channels), `perm`, `kern`, `taxis`, `porous` and `adv` (`XGENOME_SPEC.md:8-16`). None of them adds a general product. Each is built to vanish at the vacuum (`XGENOME_SPEC.md:3-6`).
- `xgenome.py` is called the reference implementation (`XGENOME_SPEC.md:3`). Its parity test covers only plain m4: f64, N = 96, noise-free, against `run_genome` (`T/fisim-beyond-laplacian/parity.py:1-15`). That is not the f32 `sim_cpu` PhySim uses.
- No extension term has a term-level parity test. The extension worlds have only behavioural dt/2 and dx checks (`T/fisim-beyond-laplacian/s_num.py:6-9`; `FINAL.md:44`).
- PhySim rejects `g = "band"` (`PHYSIM/bundles.py:327-328`). It **silently ignores** `perm`, `taxis`, `porous`, `adv`, `kern` and `ch`, because `init_soup` reads only acts, chans, W, K and bilin (`BK/soup/sim_cpu.py:56-115`). Tested on m4 with all six keys: max|ΔF| = 0.0.
- Even the established xcell worlds carry their own stepper and world-level Python. For example, xcell-evo2-S:
  - uses zero continuous noise (`world.py:99, 205`);
  - adds Poisson kicks and disk erasures from a separate RNG, `krng` (`world.py:245-273`);
  - runs at L = 64 (`world.py:27, 202`).

## B. The PhySim contract, layer by layer

| Layer | Today | Blobkit-specific by implementation | Intrinsic to the evaluation |
|---|---|---|---|
| Simulator | `Bundle.make_oracle` imports `sim_cpu.init_soup` and runs `devices.step_chunk` (`PHYSIM/bundles.py:452-487`). The step is Blobkit's kernel copied verbatim, with an RNG-free Gaussian source in front (`PHYSIM/devices.py:172-223`). `devices.py` imports `blobkit.genome` and injects through `G.poke` (`:8, 190-193`). | The binding. `OracleRunner` already takes any stepper through the private keyword `_stepper` (`PHYSIM/blobround6.py:237-265, 290`). Two verifiers drove it end to end with a non-Blobkit stepper. The runner itself pins `SIM_DT = 0.02` (`:20`), and the grammar and budget count in those ticks (`:60-70`; `blobround6_explore.py:40, 65`). | One pinned simulator serves both agent experiments and frozen truths (`PHYSIM/taskset.py:324-335`; `GEN/eval_preparation.py:87-124`). |
| World description | `world.json` is a genome, checked by `_validate_physics` (`PHYSIM/bundles.py:285-341`). | All of it. Unknown keys are not rejected. | A hashed world identity, either declarative or code. For lab worlds it must include the WORLD_P overrides (C). |
| State / preparation | One float32 array of shape (n_ports, 256, 256) (`PHYSIM/bundles.py:458-468`). `preparation.npz` must hold exactly one `fields` array (`:459-460`). Dtype kinds are limited to i, u and f (`:224`). Members copy only `F` and `rng` (`PHYSIM/blobround6.py:207-213`). Template arrays are read-only (`:258-261`). Fields must be square (`:240`). The runner accepts float64 (`:241`). | The shape, float32, the single array, F-only cloning, and the square grid. Complex state and extra state arrays are rejected today. | An exact, serializable, resettable t=0 state that holds the entire dynamical state (`public_time=0`, `PHYSIM/bundles.py:290`). |
| Numerics | `NUMERICS` must match exactly, including `workers: 1` (`PHYSIM/bundles.py:24-33, 288`). The template must have dt == 0.02 (`PHYSIM/blobround6.py:244-245`). | The values, and the tick constant. | A declared, fixed tick grid. The world's internal dt and its steps per tick are free; only the public grid is part of the agent contract. |
| Apparatus / ports | n_ports = na + nc, with exactly two devices of 13 and 19 slots (`PHYSIM/bundles.py:265-267`). Device L is 128 (`:385`). Probe spacing is 3 and 6 (`GEN/eval_preparation.py:36`), dilation 0.5–3 (`PHYSIM/devices.py:13`). The runner passes `dict(field, y, x, amp)` to the stepper, using the same index it reads (`PHYSIM/blobround6.py:269, 343-345`). amp ∈ [0, 3] (`:24, 137`). The Gaussian, σ 2, is `step_chunk`'s choice (`PHYSIM/devices.py:12, 189-193`). Slot counts also appear in `PHYSIM/container_worker.py:38` and `PHYSIM/data/agent_spec.txt:68-70`. | "Port = field identity" for reading and driving, the non-negative amplitude, and the 13/19 layout. `PublicRoster` allows 16 devices and 128 ports (`PHYSIM/blobround6_eval.py:41-46`), but the bundle path caps a world at 64 fields and 2 devices. | Anonymous, schedulable, bounded local actuation; spatial reads at continuous positions; a global summary. |
| Noise / realizations | Policy `independent-experiment-v1`. Member RNG = sha256(policy\|truth_seed\|member) (`PHYSIM/blobround6.py:196-204, 329-330`). Injections and sensors draw nothing from the RNG (`PHYSIM/devices.py:190`; `PHYSIM/blobround6.py:267-276`). | The noise form (additive, activators only). The amplitude is already a bundle field (`PHYSIM/bundles.py:339-341`), but the generator ignores it and uses 0.002 (`GEN/eval_preparation.py:91`). A different declared value would split truths from experiments. | All stochasticity flows from one injectable RNG. Actions are RNG-neutral, which paired-noise controls rely on. |
| Suite / truth / scoring | Horizon 50 tu (`PHYSIM/bundles.py:268`). Queries are bounded at `PHYSIM/blobround6_eval.py:130`, actions at `:140`. 1–128 cases per suite (`PHYSIM/bundles.py:417`); BF has 15 cases, XV 15, p4g2_044 19 (`docs_source/data/reward-calibration.json`). 2 truth members (`GEN/build_evaluation_bundle.py:78`) and 64 forecast members (`PHYSIM/bundles.py:419-424`). Controls use 4 members (`GEN/build_evaluation_bundle.py:109`) and include `initial_persistence` (`:111-115`). Energy score (`PHYSIM/blobround6_eval.py:267-278, 308-317`). K is one global precision, default 2 (`PHYSIM/rewards.py:7`), calibrated with 64 members per case (`reward-calibration.json:3, 6`). | The ablations edit the runner's template arrays (`bilin`, `Wf`, `Wid`), switched on port count, plus a 12-port `disable_shared_feedback` (`GEN/build_evaluation_bundle.py:96-105`). Also: the `na` guess and the 13/19 slot ranges in `score_groups` (`:21-37`), L = 128 in `wrong_probe_geometry` (`:107-108`), probe centring on the field-0 argmax (`GEN/eval_preparation.py:31-32`), permutations fixed by world name (`:34`), and the `--world {bf,xv}` switch (`:239`). | The suite is frozen before truths (`GEN/build_evaluation_bundle.py:194`). Scales are fixed in native units. Native-ensemble scores are clearly separated from naive controls. Each world has its own privileged ablations. |
| Identity / pins | `implementation_identity` hashes BK `genome.py`, `sim_cpu.py` and `sim_v1.py`, PHYSIM `devices.py`, and the runner, and pins numpy 2.5.2 and scipy 1.18.0 (`PHYSIM/bundles.py:34, 57-74`). `check_runtime` enforces it (`:443-450`) for experiments and at grading (`PHYSIM/taskset.py:123-124, 326`). The 1e-10 reference check (`GEN/build_evaluation_bundle.py:221`; enforced at `GEN/validate_evaluation.py:44-50`) scores a persistence control built from t=0 readouts; it does not re-simulate the dynamics (`PHYSIM/evaluation.py:372-410`). Cross-platform bitwise identity is not claimed (`schemas/README.md:60-62`). | Which files are hashed. Editing `blobround6.py` or `devices.py` invalidates every existing bundle, even when the numerics are bitwise equal. There is a precedent for keeping old bundles working: the frozen `legacy_v1` runner (`PHYSIM/bundles.py:61-65`). | The simulator is bound to its truths. Bit drift matters most in deterministic chaotic worlds. |

## C. Mapping the collective's world classes onto Blobkit

The 8 met grand challenges are listed at `research/alife/collective/STATE.md:109-116`.

**Classes used below.**
- **(ii)** The world fits Blobkit's scheme: real fields on one square or rectangular periodic grid. Each step is explicit local terms, plus explicit conservative flux terms, plus linear maps applied per Fourier mode (diffusion, k⁴, Stokes projection, streamfunction, dealiasing).
  - It needs new vocabulary only, graded s (small), m (moderate) or l (large) by its distance from today's genome.
- **(iii)** The world needs something outside that scheme: particles, connected-component labelling, discrete state, Lagrangian scatter, or argmax transport.

| Class (worlds; grand challenges held) | Defining operators | Maps to Blobkit as | Stochastic during the run? | Scale and time where the behaviour shows |
|---|---|---|---|---|
| active nematic (c34 marangoni: SIBMD, SIBMD(BD), SIBWMD, IBWD. c34 cargo: IBWD, IBD(BD)) | CH φ with implicit k⁴ and relaxation kr(φ_b − φ); Q as two real fields with corotation, flow alignment and a \|Q\|²Q bulk term; Brinkman–Stokes v̂ = (I − kk/k²)f̂/(ξ + ηk²) from μ∇φ − ζ∇·Q plus Marangoni stress; 2/3 dealiasing; advection; surfactant adsorption drift; Heaviside sources ks·[φ>0] and kc·[φ>0]; Slotboom finite-volume cargo flux (marangoni `world.py:76, 86-158`) | (ii-l). Every operator is explicit or a per-mode Fourier map. | No; RNG used in `init` only (`:66-71`) | 128², dx 1, dt 0.05, T = 1000 (20,000 steps), 411 s/seed (~20.5 ms/step); 22/28/26 persistent splits (`contribution.json:3`) |
| phase field with kernel drive (c29; SIBMD) | Allen–Cahn tilt by L; φ²-gated mobility; drift up ∇4φ(1−φ); S·K(1−K)·φ with a 1/dt cap; normalized Gaussian-kernel velocity, clipped, with MUSCL advection (`world.py:124-131, 180-208`). The claim uses WORLD_P `{"drive":"kernel","mu":1.0,"kd":0.08,"chi":5}`; the file default is `drive = "label"` (`world.py:66-69`; `README.md:3-5`). | (ii-l) with the kernel drive; (iii) with the default label drive | No | 256², dx 1, dt 1, T = 10,000, 276–321 s/seed. Transient: "by t~5000 the cells fill the torus and jam" (`README.md`, Limit) |
| phase-field membrane (phase_membrane; IBD(BD)) | Products φL in the tilt; S·K(1−K)·φ; φ²-gated mobility of K and L; drift of L up ∇w; substrate cap that depends on dt; clips. Fully explicit at dt 1 (`world.py:92-118`). | (ii-l) | No | 128², dt 1, t = 8000 (8000 steps), 11–13 s/seed (~1.5 ms/step); persistent splits 12/10/9 and maximum generation 3/2/2 on seeds 0–2 (`T/autopoiesis/packs/phase_membrane/seed*/FACTS.md:16`) |
| hybrid particle–field (c14 pcell-mwall and -b42; SIBDH) | Particles carrying uid, kind, lineage and heritable yield y; Bernoulli birth and death; mutation; Brownian moves with a Metropolis wall gate; K = smoothed particle count; phase_membrane-type fields plus a wall-material field M, bm = 0.005 (`world.py:38, 104-229`). Rates are per step with no dt (`:140-143, 195-197, 223, 229`). b42 differs only by b = 0.042 (`:35`). | (iii). The field half alone is (ii-l) plus M. | Yes, every step. The draw count depends on the particle count (`:141, 176-207`). | 128², dt 1, 10^5 steps, 1115–1145 s/seed (~11.4 ms/step); splits at t ≈ 63.5k–84.5k; mean yield 1.00 → 1.16–1.18 (`contribution.json:3, 9`) |
| CIPS (c40; IBED) | Enzyme with volume-filling MUSCL drift up ∇p and turnover d(e0 − e); catalysis kc·F·e²(1−p); fuel consumed and regrown; amphiphile drift up ∇4e(1−e); every diffusion implicit and spectral (`world.py:75-93, 124-160`) | (ii-l), on the same kinds of term as c29: mass action, zero cubic, flux drift, clip | No | 192², dt 0.1, ~200,000 steps, 1187–1191 s/seed (~5.9 ms/step); first split at t = 3900, generation 3 at t = 16,600 (`contribution.json:11`) |
| crawler phase field (c31; IBRM) | Front term (ρ−ρ*)\|∇φ\|; conserved q = φρ; bistable kinetics; a pool for each body, rebuilt every step by periodic labelling (`PER_BODY=1` by default, `world.py:34, 107-159`); Langmuir layer; Scharfetter–Gummel cargo (`:221-313`). An optional front cut is off by default (`cut_t = -1`, `:34, 288-289`) and enabled by WORLD_P in the repair runs (`contribution.json`, claim command). | (iii) as claimed. The claim has one planted cell and no division (`contribution.json`). The `PER_BODY=0` global-pool branch (`:136-139`; the cut also updates the budget, `:208`) might reproduce it, but it was not run, and the two branches treat noise-added protein differently. | Yes: additive η√dt·N on ρ inside φ > 0.5, with a fixed draw count (`:312-313`), which is Blobkit's form. The cut is scheduled, not random. | Native 256², L = 5 (dx 0.0195), dt 1e-3, T = 20 (20,000 steps), 514–539 s/seed (~26 ms/step) |
| fed vortex (c53 base; c53 selection, c58 and c63 variants) | Vorticity–streamfunction (ψ̂ = ω̂/k²); 2/3-dealiased advection; implicit νk² + H k⁴; rational gain kYω³/(ω²+wi²) − μω; eating capped at Y/dt; clip (`world.py:44-78`) | Base: (ii-l). c53 selection: a mutation picks a random eating pixel in raster order (selection `world.py:86-88`), which is a field-level event. c58: (iii), because it labels vortices (`C/20261027T1230-c58-vortex-trait-climb/world.py:63-72, 104`). | Base: no. Selection: mutation is off by default (`mut_dt = -1`) and enabled by WORLD_P. Its RNG is `default_rng(mut_seed = 1)`, independent of the world seed (selection `world.py:31, 53`). | 128², dx 1, dt 0.02, T = 3000 (150,150 steps), 1.85–1.92 ms/step; variants 3.6–4.1 ms/step (packs) |
| flow-lenia, c62 S-claim | 10 kernels with Gaussian growth; velocity from Sobel gradients; reintegration-tracking mass scatter | (iii) | No random draws in `step`. Scheduled predator insertion at t_pred = 100 (`C/20261028T0344-c62-flow-lenia-ecology-s-claim/world.py:40`). | 160², dt 0.2, T = 3000 (15,000 steps), 610–614 s/seed (`pack/seed*/FACTS.md`) |
| flow-lenia, c64 (interim) | As c62, plus argmax trait transport (`world.py:55-214`) | (iii) | Yes: mutation every 20 t from `mrng` (`:41, 155, 205-214`) | 160², t = 3000, no labkit pack, untimed |
| reactive convection (c49 heredity world; c49 selection claim) | ω with Boussinesq g∂xT; burning A·Y·T²/(T²+Ti²)·[T > Tc], capped; dealiased advection (`world.py:75-107`). Labels a and b are reset by half-plane at `lab_t = 200` by default (`:33, 93-95`). | (ii-l) for the dynamics (flow, derivative coupling, general reaction; anisotropic). The label reset is a scheduled field event. The selection mutation picks a random burning pixel (selection `:100-102`). | Heredity world: no. Selection: mutation is off by default and enabled by WORLD_P, with `mrng = default_rng(mut_seed = 1)` (selection `:34, 57, 99`). | 128², dt 0.04, T = 800–1200, 4.3–4.5 ms/step (packs) |
| active emulsion (c52, c36; frontier SIXD) | CH M∇²(φ³ − rφ − βp − κ∇²φ) with an A-stabilised implicit κk⁴ solve; cross chemical potentials; reaction sources on the prey; mass action k2·ca²·cb² capped at 0.5·ca/dt; volume-filling taxis (c52 `world.py:101-142`; c36 `:71-87`) | (ii-l) | No. c52 seeds predators at t = 2000 by default (`:53, 110-111`). | 256², dt 0.2 / 0.5, t = 12,000 / 10,000; 1706 s / ~700 s per seed |
| near-Blobkit fields | c37 Swift–Hohenberg: SH symbol plus the products gRu and cr·u²R; its v is already a native channel (`world.py:58-62`). c20 neural field: DoG kernel plus sigmoid. c09 gel: velocity from a stress rational in two fields, then conservative advection (`world.py:50-63`). c32 Lenia: ring kernels, bell growth, clip. c08 NRCH: cross-diffusion with negative D (2×2 per mode). c55 Barkley: activator×activator products, ∂x drift, anisotropic diffusion, multiplicative noise, non-square grid (`world.py:16, 40-52`). | c37 (ii-s); c20 (ii-m); c09 (ii-l); Barkley (ii-l); c32 and NRCH (ii-m) by my grading | Barkley, and NRCH when D > 0 (NRCH's default is D = 0) | c20: dx 0.5, t = 1000, 9 s/seed. c09: dx 0.5, T = 200, 44 s/seed. c32: T = 100, 9 s/seed. Barkley: 32×512 or 16×4096 |
| particle and discrete worlds (16, including coevbits, phoretic, PPS, evoloop, BFF, lattice-chem) | Individuals with state, event chemistry, lookup tables, programs | (iii) all | Checked: evoloop and closed particle-lenia are deterministic; BFF is stochastic. The "14 of 16 stochastic" count was only partly checked. | e.g. coevbits 700k steps (unconfirmed) |

**World-file key** (all paths are `world.py` under the directory):
- c34 marangoni: `C/20261026T0505-c34-nematic-marangoni/`
- c34 cargo: `C/20261026T0405-c34-nematic-cargo/`
- c29: `C/20261026T0227-c29-kernel-ring-screen/`
- phase_membrane: `T/autopoiesis/worlds/phase_membrane/`
- c14: `C/20261025T1345-c14-pcell-mwall-claim/` and `C/20261025T1430-c14-pcell-mwall-b42-claim/`
- c40: `C/20261026T1100-c40-cips-layered-divide-claim/`
- c31: `C/20261026T0243-c31-crawler-layer-repair-claim/`
- c53: `C/20261027T0712-c53-fed-vortex-claim/`; selection variant `C/20261027T0845-c53-fed-vortex-selection-claim/`
- c62: `C/20261028T0344-c62-flow-lenia-ecology-s-claim/`
- c64: `C/20261028T0953-c64-fl-sampled-trait-interim/`
- c49: `C/20261027T0209-c49-thermals-flow-heredity/`; selection claim `C/20261027T0222-c49-thermals-selection-claim/`
- c52: `C/20261027T0325-c52-digestion-ecology-claim/`
- c36: `C/20261026T0413-c36-food-chain-predation-claim/`
- c37: `C/20261026T0847-c37-sh-fission-correction/`
- c20: `C/20261025T1721-c20-neural-comets-depression-claim/`
- c09: `C/20261025T1016-c09-active-gel-comets-claim/`
- c08: `C/20261025T1017-c08-nrch-no-persistent-division/`
- c55 Barkley: `C/20261027T1259-c55-barkley-puffs-split-sighting/`

**Coverage of the 8 grand challenges.**
- **Held by (ii) worlds: 6 of 8.**
  - SIBMD: c29, c34.
  - SIBMD(BD) and SIBWMD: c34.
  - IBWD: both c34 worlds.
  - IBD(BD): phase_membrane, c34 cargo.
  - IBED: c40.
- **Held only by (iii) worlds:** SIBDH (c14) and IBRM (c31, unless `PER_BODY=0` turns out to be enough).
- **Five of the seven holder worlds are deterministic after initialization:** c34 ×2, c29, phase_membrane and c40.
- **phase_membrane's beyond-diffusion credit rests on the membrane.** Its uniform-diffusion twin keeps division but loses the L ring (`C/20261025T0731-c01-phase-membrane-bd-twin/contribution.json:7`).
- **World identity must include the WORLD_P overrides.** The claimed behaviour of c29, c31 and the c53/c49 selection worlds depends on them, not on the file defaults.

## D. The gap, by kind

**1. Operator vocabulary.** These are the term types missing from Blobkit, with the worlds that need each.
- **Products of fields beyond Blobkit's channel×channel `bilin` in activator equations:** products inside channel equations, products of cubic order or higher (φ²L, S·K(1−K)·φ, ca²·cb²), and products without a lag.
  - Worlds: c29, phase_membrane, the c14 fields, c40, c36, c52, c53, c49, flow-lenia, c37, c20, c09, Barkley, evopursuit.
  - Quadratic products in activator equations can be emulated with relay channels (section A).
- **Free local reactions:**
  - no cubic: c40, the KS densities, fuel fields;
  - a positive cubic plus a quintic: CGLE;
  - rational or saturating terms: c53 gain, c49 burning, Hill growth in evopursuit;
  - Heaviside thresholds: c49, c34 (`marangoni world.py:97, 155`);
  - bell or sigmoid growth: c32, c20.
  - λ > 0 is required by PhySim (`PHYSIM/bundles.py:310-326`).
  - A negative cubic coefficient other than −1, and Du = 0, are not gaps (section A).
- **Cahn–Hilliard transport M∇²μ with a nonlinear μ, plus reaction or relaxation sources:**
  - c34 (relaxation, `marangoni :135-136`), c36 and c52 (prey sources);
  - only c52's predator is strictly conserved (`:125-128`);
  - NRCH; FCH (sixth order), AMB+ and AMH were not re-checked.
  - c40 condenses by drift and has enzyme turnover (`:50, 141`).
- **Linear symbols other than −Dk²:**
  - k⁴: CH, hyperviscosity in c53 and c49;
  - (q0² + ∇²)²: c37;
  - k⁶: FCH;
  - negative D with a 2×2 cross-diffusion matrix: NRCH;
  - complex dispersion: CGLE, c55 Schrödinger–Poisson;
  - drift and anisotropy: Barkley.
  - All of these are per-mode factors and cheap to add to the exact Fourier step. x-genome already puts k∇⁴ there (`XGENOME_SPEC.md:11`).
- **Conservative flux transport up another field's gradient,** with upwind, MUSCL or Scharfetter–Gummel faces:
  - volume-filling taxis: c40, c52, evopursuit;
  - adsorption drift: c34, c40, phase_membrane, the FCH solute;
  - gated mobility G(field): G = φ² in c29, phase_membrane and c14; exp(−βq) in FCH-metabolic.
  - x-genome covers only linear mobility into activators (`taxis`) and an exp(−βx_c) gate (`perm`) (`xgenome.py:20-27, 150-157`).
- **Advection by a velocity obtained from a solve, with dealiasing:**
  - Stokes projection: c34, AMH;
  - compressible active-stress flow: c09;
  - streamfunction: c53, c49;
  - normalized-kernel velocity: c29;
  - Lagrangian mass scatter: flow-lenia, which is (iii).
- **Kernels:** narrow ring kernels (c32, flow-lenia). DoG (c20) can be approximated by two signed channels.
- **Non-field operators:**
  - connected-component labelling inside the step: c31's pool, c28's default drive, c58's vortex-mode mutation, evopursuit;
  - argmax trait transport: flow-lenia.
- **Non-smooth operators:** clip, `min` caps and flux limiters, in almost every lab world.
  - Several caps scale with 1/dt, so the equations themselves change with the step: phase_membrane `world.py:102`, c29 `:188`, c36 `:74-75`, c52 `:119`, c53 `:74`, c49 `:80`.

**2. State types.** PhySim's dynamical state is `F` (C, N, N) plus `rng` (`PHYSIM/blobround6.py:207-213, 239-243`).
- **Tensor and vector fields fit as real components.** Q in c34 is two real grids (`marangoni world.py:78`). What is missing is cross-component terms such as \|Q\|²Q and corotation, and actuation and observation that do not depend on the frame. Blobkit's per-component −u³ is not rotation-invariant, so it cannot stand in for −\|p\|²p (c51, c24).
- **Derived velocities are recomputed every step, not evolved** (`marangoni :117-121`). They are observables, not state.
- **What does not fit today:**
  - complex fields (c43, c55): storable as two real fields, but the bundle rejects complex dtypes (`PHYSIM/bundles.py:224`);
  - scalars for each body (c31) and global budgets;
  - particles with identity and internal state (c14 and all particle worlds);
  - discrete state: evoloop (uint8), lattice-chem (counts), BFF (bytes), flow-lenia (argmax trait);
  - secondary generators (`mrng`, `krng`).
  - The bundle allows exactly one `fields` array (`PHYSIM/bundles.py:459-460`), so none of these has a place.
- **A note on cloning, from my reading of `_clone_sim`.**
  - The member dict is a shallow copy, and template ndarrays are read-only.
  - A stepper that rebinds extra keys works per member. One that mutates extra arrays in place fails (tested: "output array is read-only").
  - Mutable objects that are not arrays would be shared across members.
  - Sensors read only `F` (`PHYSIM/blobround6.py:269`).

**3. Numerics.**
- **Lengths and times can be relabelled.**
  - dx and dt are labels. The intrinsic quantities are: grid points, squareness, native steps per public tick, dtype, the scheme, and the size of the apparatus relative to the bodies.
  - The runner already lets a stepper take any number of internal steps per tick. It only checks the public dt (`PHYSIM/blobround6.py:244-245`).
  - The runner accepts float64; float32 is required only at bundle level (`PHYSIM/blobround6.py:241`; `PHYSIM/bundles.py:465`).
- **Worked example, c31.**
  - c31 is natively 256², the same grid count as PhySim. Relabelled to L = 128, its cell radius is about 44 px (≈ 22 world units), and σ = 2 is small against it.
  - The alternative fails: keeping c31's length unit and coarsening to dx 0.5 would make the cell about 3.4 px across, with an interface (ε = 0.1, `world.py:33`) 0.2 px wide.
- **Grids differ.** c34, c53, c49 and c14 are 128² at dx 1, so their side equals PhySim's L. Fitting PhySim's 256² grid means either a 2× refinement, which changes the numerics, or a grid declared per bundle. Barkley is not square.
- **Schemes.**
  - Implicit per-mode solves: c34, c52, c53, c40, c31.
  - Fully explicit at dt 1: phase_membrane, c29, c14 (`T/autopoiesis/worlds/phase_membrane/world.py:92-117`).
  - Others: finite-volume upwind, MUSCL and Scharfetter–Gummel fluxes; integrating factor plus Heun (CGLE); Strang split-step (c55).
  - c14 has no dt at all. Its probabilities are per step (`C/20261025T1345-c14-pcell-mwall-claim/world.py:140-143, 195-197`), so it cannot be put on a finer tick without rewriting its rates.
- **Some behaviour is tied to the scheme.**
  - Halving dt is not a convergence test for reintegration tracking (`T/flow-lenia/FINAL.md:58`; `research/alife/RUBRIC.md:131`).
  - Phoretic persistent splits fell under dt/2 in fresh-seed re-runs, 17 → 12 and 18 → 13 (`C/20261026T0430-c29-review-phoretic-dthalf/contribution.json`; `C/20261026T0445-c32-review-phor-dthalf/contribution.json`).
  - So a translated world is a new world that needs revalidation.
- **Stiffness.** x-genome's explicit CH part requires dt·M·h·8/dx² < 1 (`XGENOME_SPEC.md:18-21`). The term library would need implicit per-mode treatment for k⁴ and k⁶, as c34 and c52 use.

**4. Stochasticity.**
- **PhySim:** realizations differ only through activator noise. Sensors are noiseless.
- **Deterministic after initialization:**
  - c34 (both), c29, phase_membrane, c40, c36, c52 (scheduled predator insertion at t = 2000), c53 base, c49 heredity world (scheduled label reset at t = 200), c62 (scheduled insertion at t = 100);
  - c32, c09, c37, c20, CGLE, evoloop, closed particle-lenia;
  - NRCH at its default D = 0.
- **What that does to scoring.**
  - All members are identical, so the native-ensemble energy is 0 when the simulator reproduces exactly.
  - That does not change today's global K, which is a maximum over all suites (`docs_source/data/reward-calibration.json:6`). But the rule gives no finite K for such a world on its own.
  - An exact reproducer scores S = 0, which maps to reward 1 (`PHYSIM/rewards.py:28-30`). The score would then measure exact reproduction of a deterministic, possibly chaotic, system rather than calibrated uncertainty.
- **Options for deterministic worlds:**
  - add dynamics noise, which changes the world and must be revalidated;
  - add read noise, since sensors draw nothing from the RNG (`PHYSIM/blobround6.py:267-276`);
  - keep deterministic truths and set K by policy, since the energy score stays proper against a point-mass truth.
- **No headline deterministic world has been run with noise during the run.** NRCH (conserved noise, a negative result; `C/20261025T1017-c08-nrch-no-persistent-division/world.py:74-76`), c31 and Barkley do run with noise.
- **Rare-event noise** (c64, and the c53/c49 selection worlds when enabled): within one window, members differ by at most a few discrete events.
  - The c53/c49 selection RNG is seeded by a fixed `mut_seed = 1`. Members cloned from one prepared state would make identical draws and have zero spread unless the harness replaces `mrng`.
- **Intrinsic noise that drives the behaviour: c14 and the particle worlds.**
  - It cannot be scaled to 0.002.
  - c14's draw count depends on the state (one draw per particle, `:141`). So an injection that adds matter would desynchronize member noise streams, breaking the paired-noise counterfactuals behind `GEN/bf_feedback_check.py:19-41`. This is my inference.
  - A counter-based RNG keyed on (particle uid, tick) would restore pairing (critic's suggestion, untested).
- **c31 is different.** Its noise is additive Gaussian in Blobkit's form with a fixed draw count. Whether its behaviour depends on η is untested.
- **RNG injection is not new.** Blobkit also keeps `rng` in its state (`BK/soup/sim_cpu.py:62, 105`), and PhySim already replaces it per member (`PHYSIM/blobround6.py:330`). c14 and c31 each use one generator under the key `rng`, so the same mechanism applies. The real problems are secondary generators and draw counts that depend on the state.

**5. World-level events.**
- **Blobkit has none during a run.** `KICKS` only sets the initial offset of the dressing shadow, and the gt_mv3 entry is a no-op (`BK/worlds.py:34`).
- **Lab worlds have several kinds:**
  - scheduled resets (c53 `lab_t = 300`; c49 `lab_t = 200`);
  - insertions (c62 at t = 100; c52 at t = 2000);
  - switch-ons (evopursuit at t = 150);
  - mutations whose target is chosen from the state;
  - Poisson kicks and erasures (xcell-evo2-S);
  - an optional scheduled cut (c31, off by default).
- **Absolute time.** PhySim restarts the clock at `public_time = 0` from a prepared state (`PHYSIM/bundles.py:290`). The preparation identity already records `original_time` (`GEN/build_evaluation_bundle.py:248`), so it could be passed to the stepper. Otherwise, absolute-time schedules must fall inside the preparation.

**6. Scale and time.**
- **PhySim's window and budget.**
  - The window is 50 tu, or 2500 ticks, starting from a preserved preparation state. That state is recorded at 2500 tu for BF and XV and 1700 tu for p4g2_044. The script loads it; it does not run it (`GEN/eval_preparation.py:28-30, 68`; `GEN/prepare_centered_reference.py:31`).
  - The horizon is set in the bundle layer (`PHYSIM/bundles.py:268`).
  - The agent budget defaults to 1000 experiments and 50,000 tu (`PHYSIM/taskset.py:76-77`), which is 2.5M ticks.
- **Count native steps per window, not tu.** The figures below are my arithmetic from the timings in section C.

| World | 1 tick = 1 native step: share of claim run in one window | Events per window | Agent budget at full use |
|---|---|---|---|
| phase_membrane | 31% | ≈ 2.8–3.75 persistent splits | ≈ 1 h |
| c34 | 12.5% | ≈ 2.75–3.5 splits, if evenly spread (not confirmed) | ≈ 14 h; ≈ 5.7 h if c34 keeps its own tu (1000 steps per window) |
| c29 | 25% | must be prepared before jamming (t < ~5000) | ≈ 21 h |
| c40 | 1.25% | ≈ 0.11–0.14 splits; one split per window needs ~8 native steps per tick | ≈ 4 h at 1 step per tick; ≈ 33 h at 8 |
| c14 | 2.5% | mean-yield change ≈ 0.004 if linear; selection invisible | ≈ 8 h |
| c31 | 12.5% | repair takes ~1 tu = 1000 steps after a cut, so it fits if the preparation ends just after a cut | ≈ 18 h (≈ 65 s per member window) |
| BF (reference) | — | — | ≈ 2.6 h at 3.78 ms/step |

  - If each world instead keeps its own tu, phase_membrane gets 50 steps per window (0.06–0.08 splits), c40 gets 500 steps (0.02–0.03 splits), and c31 gets 50,000 steps (about 22 min per member).
- **One-off costs per world.** Reward calibration runs 64 native members per case (`reward-calibration.json:3`). On top of that, each case needs 3-member science runs (`GEN/eval_preparation.py:254`), 2-member truths and 4-member controls.
  - At 2500 steps per window, the 64-member runs cost about 55 min per case for c34 (≈ 14–17 h for 15–19 cases), about 30 min per case for c14, and about 4 min per case for phase_membrane.
  - The earlier 20 CPU-hour figure for c14 assumed the claim's full horizon.

**7. Apparatus.**
- **What a port means now.** The runner hands the stepper `dict(field, y, x, amp)` on the same index it reads (`PHYSIM/blobround6.py:269, 343-345`). The Gaussian source shape belongs to the stepper (`PHYSIM/devices.py:189-193`).
  - So new actuator kinds per port (add particles, add food, a uniform source) need no change to the runner. The critic ran a non-Blobkit stepper with a uniform source.
  - The runner fixes two things: reading and driving share one index, and amp ≥ 0 (`PHYSIM/blobround6.py:24, 137`).
- **Where that meaning breaks:**
  - **Derived fields** (v, ψ, c14's K) can be read but should not be driven. That needs separate maps for observed and actuated ports.
  - **Tensor components:** driving q1 alone depends on the frame. BF and XV use identity rotation and reflection (`GEN/eval_preparation.py:37, 45-48, 57`), so no hidden orientation exists to leak today. Leakage would arise only with non-identity values, in anisotropic worlds such as c49 (inference).
  - **Conserved fields:** a source adds mass, which bypasses the mechanism that forms the bodies.
  - **Erasure** (labkit's `damage`; c31's IBRM) is blocked by the non-negative amplitude range.
  - **Particle worlds:**
    - The natural actuator is "add or remove particles or food here".
    - Rasterized densities carry shot noise; about 400 prey on 64² bins is about 0.1 per bin.
    - Heredity is identity-based, so field sensors cannot see it.
  - **Evoloop:** an injection acts as a wound that kills loops.
  - **BFF:** it has no space to attach a source to.
- **Scale.** The apparatus is fixed in PhySim world units: device L 128 (`PHYSIM/bundles.py:385`), probe spacing 3 and 6, so reach is about 6 and 12 units (`GEN/eval_preparation.py:36`), dilation up to 3× (`PHYSIM/devices.py:13`), and σ = 2 (`PHYSIM/devices.py:12`). What matters is whether a division happens under a probe within one window.
- **Observed fields.** Labkit's `fields()` is a chosen subset (e.g. xcell RENDER, `world.py:36, 230-233`), whereas PhySim exposes the full state.

## E. Options for generalizing

**(1) Extend the genome with keys (the x-genome route).**
- **Covers:** as scoped today, none of the 8 holder worlds. x-genome adds no general products, and the near-Blobkit worlds each need at least one product or symbol it lacks.
- **The line between (1) and (2) is not principled.** A genome that holds phase_membrane, c29 or c40 needs products in any equation, products of cubic order, flux terms and clip. At that point it is a term list.
- **Cost:**
  - strict key validation, to replace the silent ignore;
  - a stability rule and a term-level reference test for each key;
  - a new implementation identity and rebuilt bundles (`PHYSIM/bundles.py:57-74, 446-448`).
  - Vacuum-safety is a Blobkit convention; PhySim does not require it.
- **Risks:**
  - x-genome's own screens found that ring kernels, porous diffusion, advection and taxis on m4 tile space or collapse (`T/fisim-beyond-laplacian/FINAL.md:53`).
  - Heredity of arisen markers was contradicted (`FINAL.md:17`), and m4 cells "essentially never die on their own" (`FINAL.md:55`).
  - Adding operators does not bring the behaviour with them.

**(2) Widen Blobkit into a term-list PDE spec on its own scheme.**
- **What it is:** declared real fields, with complex or tensor fields stored as real components. Each equation is a sum of library terms. The library would hold:
  - local expressions over any fields, including clip and caps;
  - conservative flux terms ∇·(M(f)∇μ) and ∇·(m(f) v[g]) with upwind, MUSCL or Scharfetter–Gummel faces;
  - per-mode linear symbols, polynomial in k², with cross-field blocks, solved implicitly;
  - FFT kernels;
  - streamfunction and Stokes maps with dealiased advection.
- **Covers:** 6 of the 8 grand challenges (c34 ×2, c29, phase_membrane, c40), plus c36, c52, the c53 base, the c49 dynamics, the near-Blobkit worlds, CGLE and FCH (FCH not re-checked).
- **Misses:** c14 (particles), c31 as claimed (labelling), flow-lenia, the discrete worlds, and events whose targets are chosen from the state.
- **Cost:** smaller than a new simulator. The scheme is Blobkit's, and x-genome already mixes finite-volume flux terms into it (`T/fisim-beyond-laplacian/xgenome.py:47-64, 150-157`). The main costs are the term library, its stability rules and references, and revalidating each translated world.
- **Risks:**
  - Behaviour depends on the scheme (MUSCL versus spectral, explicit versus implicit), so each translation is a new world.
  - The spec may creep toward a programming language.
- **Benefit:** privileged ablations become generic "drop term" edits. That replaces the template-array edits in `remove_feedback` (`GEN/build_evaluation_bundle.py:96-105`).

**(3) A world-plugin interface.** A bundle carries its own reference stepper, hashed into its identity, plus a declared apparatus.
- **The contract:**
  - `prepare` loads named state arrays;
  - `step(sim, n, injections)` draws all randomness from a harness-supplied RNG;
  - `observe` returns (C, N, N) rasters;
  - declared numerics: tick, grid, L, native steps per tick;
  - separate maps for observed and actuated ports, with a declared actuator kind per port, signed or erasing where needed;
  - a full-state clone hook;
  - declared ablation hooks.
- **Covers:** all 8 holder worlds can run. But c14's defining behaviour (selection over 10^5 steps) is not observable in one window. c31's repair is observable only if the preparation ends just after a scripted cut, or if an erasure actuator is added. In grand-challenge terms, (3) adds at most IBRM over (2).
- **Cost:**
  - Generalize `SIM_DT` and the tick grammar, `_validate_physics`, `make_oracle`, `NUMERICS`, the preparation format, the cloning, the roster, and the recipe hard-codes (`GEN/build_evaluation_bundle.py:21-37, 96-108`; `GEN/eval_preparation.py:31-36, 239`).
  - Remove the 13/19 hard-codes in `container_worker.py` and `agent_spec.txt`.
  - Settle K per world.
  - Update the agent spec wherever the tick grid changes.
- **Risks:**
  - Worlds are opaque. This is weakened by the fact that claims already ship their named ablations as P overrides. But WORLD_P is read at import, so control runs need separate module instances.
  - **Reproducibility.** Numba is not in `.venv`. Cross-platform bitwise identity is not claimed (`schemas/README.md:60-62`). The 1e-10 check does not exercise the dynamics. Drift between agent experiments and frozen truths matters most in deterministic chaotic worlds (c53, active nematics).
  - Whether only trusted registry code may run in the grader is unconfirmed.

**(4) Per-world translation.**
- **Covers:** only the worlds chosen. It is cheap only for c37; c20 is moderate; phase_membrane, c09 and Barkley are large.
- **Risks:** each port is a new, unvalidated world; it does not scale; and it causes repeated identity churn.

**Recommendation (revised): a declared contract first, then a widened Blobkit for field worlds, and raw plugins only where fields cannot do the job.**

- **Stage 0: contract only. Every option needs this.**
  - Turn the private `_stepper` seam into a declared interface.
  - Make the tick grid, numerics, roster and noise policy per-bundle. Separate observed ports from actuated ones and allow declared actuator kinds. Add full-state cloning. Move the ablations into world hooks. Reject unknown genome keys.
  - Keep the current runner frozen as a legacy path, as `legacy_v1` was. Otherwise every world, preparation, suite and bundle ID, and the pinned catalog revision (`PHYSIM/taskset.py:35-38`), must be re-issued.
  - Acceptance: re-wrapped Blobkit reproduces the existing BF, XV and p4 truths and reference scores bit for bit, and old bundles still load.
- **Stage 1: widen Blobkit into a term list (option 2) and settle the noise policy.**
  - Add terms with a term-level reference test for each.
  - Pilots:
    - **phase_membrane** (holds IBD(BD); about 1.5 ms/step; about 3 persistent splits per 2500-step window). Run it both as a raw labkit plugin and as a term-list translation, and compare. That directly tests whether translation preserves behaviour.
    - **c53 base**, which already uses dt 0.02, but at dx 1 on a 128² grid.
    - **c37**, as the near-Blobkit control.
  - Acceptance:
    - the behaviour survives the declared noise or read-noise policy;
    - native scores separate from the controls;
    - the reference reproduces.
- **Stage 2: headline field worlds.**
  - Pilots:
    - **c34 marangoni** (4 of the 8; with c34 cargo, 5).
    - **c29**, prepared before it jams.
    - **c40**, only if about 8 native steps per tick (about 33 h of agent budget at full use) is acceptable.
  - Decide what a port means for Q, for the derived v, and for sources on conserved fields.
- **Stage 3: raw-Python plugins for c14, c31, c64 flow-lenia and the c53/c49 selection worlds.**
  - Requirements: a harness-injected RNG (including replacing `mrng`), full-state cloning, RNG-neutral actuation, and rasterized particle observables.
  - c31 also needs either a preparation that ends just after a cut, or an erasure actuator.
  - Treat c14 as a world for its field-level laws; its selection will not show in a window.
- **Deferred:**
  - BFF (no space) and evoloop (wounded by injections);
  - the negative-result worlds: c51 Toner–Tu and flames, c55 Schrödinger–Poisson, c43 CGLE.

## Reader disagreements and unconfirmed points

- **Where c40 belongs.** The draft called c40 "(iii) for the genome" but c29 "(ii)". I applied the criterion stated in C, which puts both in (ii-l). The lab-worlds verifier and the critic agree.
- **Vocabulary versus architecture.** The critic is right that c34, c40, c52 and c53 use Blobkit's explicit-plus-Fourier scheme (confirmed at c34 `:76, 117, 136`, c40 `:141-160`, c52 `:101-130`, c53 `:44, 62-78`). Translation and revalidation remain real costs, so I kept those as the main cost of option (2).
- **Time accounting.** The draft counted in tu; the critic counted in steps. Both mappings are shown in D.6. Steps per window decide what is visible.
- **Horizon:** the labfields reader found no horizon limit. It exists: 50 tu (`PHYSIM/bundles.py:268`), with queries bounded at `PHYSIM/blobround6_eval.py:130`.
- **The "pluggable `make_oracle`" claim.** `GEN/eval_preparation.py:125` is the generator's own `make_oracle` (`:87`). The bundle's `make_oracle` is hard-wired (`PHYSIM/bundles.py:452-487`).
- **Blobkit's per-step cost.** Re-timed: BF 3.78 ms/step and XV 6.36 ms/step at 256², f32, 1 worker. The ~11–13 ms figures for m4 come from other code paths.
- **c29's mapping:** (ii-l) with the claim's kernel drive; (iii) with the default label drive.
- **Unconfirmed:**
  - whether any behaviour survives added noise, float32, relabelling, or a term-list translation;
  - whether c31 behaves the same with `PER_BODY=0`;
  - split rates spread evenly over time;
  - RNG desynchronization under injection (inference);
  - Barkley's affine rescaling;
  - the numba worlds (not run);
  - c20's "jitter" finding;
  - FCH, AMB+ and AMH operators (not re-checked);
  - "14 of 16 particle and discrete worlds are stochastic" (3 checked);
  - coevbits at 700k steps;
  - the grader's trusted-code policy;
  - the critic's ring-kernel fit figures (not re-run; the two-channel DoG shape was re-run).

## Corrections applied

- Summary, "most of PhySim does not depend on Blobkit": added `SIM_DT`, `ADJUST_TICKS`, the budget in ticks, `genome.poke` in `devices.py`, and the `container_worker`/`agent_spec` hard-codes (blobkit #1).
- "Du > 0 is required" and the gap "Du = 0": dropped. PhySim accepts Du = 0 and never calls `genome.validate` (blobkit #2, lab-worlds #3, critic #7).
- Added PhySim's real constraints (λ > 0, τ and sc > 0, count caps) and the thr < 0 vacuum failure (blobkit #3, lab-worlds #3).
- "Cubic coefficient fixed at −1" as a restriction: replaced. A negative cubic coefficient is a choice of units, with a caveat about the noise and injection amplitudes (lab-worlds #2, critic #7).
- "No activator–activator coupling, no u×x": quadratic products in activator equations can be emulated by relay channels with a one-step lag (critic #6; mechanism checked in `sim_cpu.py`).
- Kernels "none can be a ring" and "DoG missing": the net kernel is a signed sum of Yukawas, and two channels give a DoG-like kernel. I re-checked this. Narrow rings still need a kernel multiplier (blobkit #4, critic #8).
- Added the positivity and dealiasing limits of the spectral step, with my own numbers (critic #10).
- "FitzHugh–Nagumo/Purwins family" attribution: changed to "Purwins model; FHN is our label" (blobkit #15).
- META "declares dt": META dt is for reporting only, and META has no length unit (blobkit #18, lab-worlds #20, critic #22).
- "None of the extension terms has a reference": changed to "no term-level parity test; only behavioural checks" (blobkit #12).
- Noise row and D.4: the amplitude is per bundle but the generator hard-codes 0.002. The K calibration does not "break"; it has no finite per-world K, and the noise options are listed (blobkit #5, critic #15).
- `PublicRoster` "16 devices / 128 ports": added the bundle caps (64 fields, 2 devices, one real `fields` array) (blobkit #13).
- Added suite sizes and `initial_persistence` (blobkit #14).
- Ablations: they edit template arrays, not `world.json`. Added the missing hard-codes (blobkit #17).
- 1e-10 reference: corrected the citation, and stated that it checks a persistence control and that cross-platform parity is not claimed (blobkit #16, critic #19).
- Stage 0: added identity churn and the `legacy_v1` frozen-path option (blobkit #11, critic #18).
- "Preparation runs 2500 tu": changed to "loads a preserved state recorded at 2500 tu (BF, XV) or 1700 tu (p4)" (blobkit #7).
- Orientation leakage: removed as a current risk, because BF and XV use identity values (blobkit #8, critic #13).
- c31 "under 2 px": corrected to about 3.4 px across, and reframed around relabelling, under which c31's cell is about 44 px in radius (blobkit #9, lab-worlds #8, critic #5).
- c34 marangoni "5 of 8": changed to 4; c34 cargo adds IBD(BD) (blobkit #10, lab-worlds #6, critic #17).
- Moved c40 from (iii) to (ii-l), with an explicit class criterion. Moved c34, c36 and c52 to (ii-l) under the same criterion (lab-worlds #1, critic #1; checked in code).
- The "6 of 8 held only by worlds no genome extension reaches" headline: replaced by "6 of 8 fit Blobkit's scheme but need new vocabulary; x-genome as scoped reaches none" (critic #1, lab-worlds #1).
- "Selected for leaving Blobkit's vocabulary": softened. The beyond-diffusion twin is not a Blobkit comparison and only 2 of 8 grand challenges require it; x-genome's negative results are cited instead (critic #16).
- Option (4), "cheap" near-Blobkit worlds: only c37 is cheap; c20 is moderate; phase_membrane, c09 and Barkley are large (lab-worlds #4).
- Added the caps that scale with 1/dt and c14's per-step rates (lab-worlds #5).
- c31: the cut is optional and enabled by WORLD_P, not stochastic. The noise is in Blobkit's form with a fixed draw count. The run starts from one planted cell. The `PER_BODY=0` reduction is marked unconfirmed (lab-worlds #7, #9; critic #2).
- "No collective world tested under noise": changed to "no headline deterministic world"; NRCH, c31 and Barkley run with noise (lab-worlds #10).
- Split flow-lenia into c62 (deterministic apart from the t = 100 insertion; 610–614 s) and c64 (mutation; untimed) (lab-worlds #11).
- Added the fixed-seed `mrng` in the c53/c49 selection worlds, and that mutation is off by default (lab-worlds #12; checked).
- Labelling list: c53 and c49 mutate by raster-order pixel choice; only c58 labels (lab-worlds #13).
- The "conserved" list: CH transport with relaxation or reaction sources; only c52's predator is strictly conserved (lab-worlds #14).
- Added c49's `lab_t = 200` reset to D.5 (lab-worlds #15; checked).
- Corrected timings: c53 1.85–1.92 ms/step, variants 3.6–4.1, c49 4.3–4.5, phase_membrane 11–13 s with splits 12/10/9 (lab-worlds #16; phase_membrane checked).
- phase_membrane splits per window: recomputed in steps (lab-worlds #17, critic #4).
- Added c29's transient jamming by t ≈ 5000 (lab-worlds #18).
- Added that world identity must include WORLD_P (lab-worlds #19).
- c14's field half: changed to (ii-l) plus the M wall field (lab-worlds #21).
- Added c34 to the Heaviside list (lab-worlds #22).
- Option (3) "covers all 8": changed to runnable all 8, with c14 and c31 behaviours mostly not observable in one window (critic #3).
- D.6 rewritten in native steps per window, with both time mappings (critic #4).
- Tensors and derived velocities: they fit as (C, N, N) fields; what is missing is cross-component terms and frame-covariant ports (critic #9).
- RNG injection: Blobkit also keeps `rng` in its state; the real issues are secondary generators and draw counts that depend on the state. Added the counter-based RNG suggestion (critic #11).
- Port meaning: the actuator form belongs to the stepper; added the non-negative amplitude blocking erasure (critic #12).
- "Most lab worlds deterministic": changed to "5 of the 7 holder worlds" (critic #14).
- 64-member estimate: calibration does use 64 members, so costs were recomputed per case (blobkit #6, critic #20).
- Added module-level WORLD_P and non-reentrant world files (critic #21).
- Phoretic dt/2 figures: replaced 23 → 10 (single seed, uncited) with the fresh-seed 17 → 12 and 18 → 13 (critic #24).
- "Implicit solves at dt 0.1–1": phase_membrane, c29 and c14 are fully explicit at dt 1 (critic #25; phase_membrane checked).
- Recommendation: kept the Stage 0 contract, made the widened Blobkit term list the default for field worlds, and restricted raw plugins to the particle, labelling and event worlds. This follows the evidence above (critic #3, #23).