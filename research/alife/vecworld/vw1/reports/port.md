I've ported VW-0's A_gliders world to the VW-1 types and all six items ran; the output is in `/home/user/evalwork/vecworld/vw1/port/` (6.3 MB). Three results differ from what was asked or expected. The 2000-step free-running match is impossible for any implementation, because the rule is chaotic. The Fisher certificate yields only a very wide bracket. The product operator's default input port can create matter. The harness blocked writing a REPORT.md file, so the report is below. The shared venv already existed, so I did not recreate it. Nothing was written outside `port/`.

# VW-0 A_gliders in the VW-1 types

## What worked, with numbers

**Flow-Lenia level.**
- **Equivalence:** one JAX substep from each of the 4000 numpy states along the reference trajectory differs from `flowlenia.py` by at most 7.1e-15 (median 4.1e-15). Kernels, kick and Φ_coarse match to about 1e-16.
- **Free running:** the rule amplifies rounding by about 0.2 per step, so no two implementations can track each other for 2000 steps.
  - JAX vs numpy crosses 1e-6 at step 63; numpy vs itself, started 1 ulp apart, crosses at step 58. Both differences are O(1) by step 130 (`results/level0_divergence.png`).
  - numpy in the venv reproduces the stored `state_t4000` bitwise.
- **Mass:** relative drift 1.3e-14 over 4000 steps (same as numpy), 3e-15 over 1000 noisy substeps, 2e-16 per kick.
- **Speed (CPU, 2 cores, float64):**

| run | time |
|---|---|
| numpy substep | 7.3 ms |
| JAX substep, deterministic | 3.6 ms |
| VW-0 tick (20 substeps + noise + kick), 1 member | 95 ms (numpy about 165 ms) |
| vmap, per member, B = 8 / 32 | 97 / 141 ms |
| lax.map, per member, B = 8 / 32 | 90 / 92 ms |

  - Batching brings no gain on CPU because the state is cache-bound.
  - Two `optimization_barrier`s alone made the step 2.2× faster.

**Coarse-grainings.**
- Φ_coarse is written in JAX and is differentiable.
- Φ_objects wraps the VW-0 tracker unchanged (2.3 ms per call). The memory update runs on the host via `pure_callback`; the readout is a JAX slice.
- Replaying the numpy tracker on the world's recorded states gives identical output and memory. `grad` raises, and `vw.fisher` raises `NotDifferentiable`.

**World, agent API, exam.**
- **Construction and card:** the world is `vw.stride(WorldSpec(L_FL, Φ, VW-0 ports, burn_in=1000), 20)`. The card shows n_in = 16384, n_obs = 192 (coarse) or 144 (objects), the constraints, and no names.
- **Agent API:** the four VW-0 smoke-test violations are rejected with nothing charged. A kick tick conserves mass to 1e-16, and the observation is exactly the quantised, permuted level 1.
- **Exam:** 8 items, prefix 4, horizon 8, 8 replicates.
  - Oracle MSE runs 0.0020 to 0.018; persistence 0.13 to 3.2.
  - A naive extrapolating agent scores skill 0.52, 0.48, 0.22, −0.39 at q = 1, 2, 4, 8.

**Certificates.**
- **Method:** VW-0's own estimator, unchanged, on VW-1 data. Sample: 16 trajectories × 240 ticks, 48 test states × 6 replicates, 11 minutes.

| | τ = 1 | τ = 2 |
|---|---|---|
| Coarse ceiling, VW-1 port | 0.9857 ± 0.0008 | 0.9424 ± 0.0022 |
| VW-0 published (24 × 300) | 0.9880 | 0.9533 |
| VW-0 data, same sample size | 0.9863 ± 0.0005 | 0.9439 ± 0.0018 |

- **Result:** at matched sample size the agreement is z = −0.7 and −0.5. The gap to the published numbers comes from the ridge predictor's training-set size, not from the port.
- **Other numbers:** the oracle variance is 5.9e-4 vs 6.3e-4. The objects ceiling at τ = 1 is 0.867 ± 0.029 (matched VW-0: 0.846 ± 0.025).

**Composition on the real world.**
- **stack:**
  - Level 2 is computed from Φ_objects alone: count, tracked mass, mean speed, and a running average of the fusion rate. It needs 151 memory numbers vs 16593 at level 1.
  - Checked against the tracker's own events, its fusion counts have precision 1.00 and recall 0.98, exact on 99.5% of ticks.
- **product:**
  - Two independent glider worlds equal the pair bitwise.
  - The default joint port (k = 16, one zero-sum over both blocks) accepts commands with sources in one world and sinks in the other.
  - With sources on dense cells, total mass is kept but the channel mix changes. With sources on empty cells, 2.0 units of matter are created.
- **stride:**
  - Stride 10 of stride 20 equals stride 200 bitwise, burn-in included.
  - The tracker fails at stride 200, as the note's Prop. 10(e) predicts. Per 1000 substeps it records 13.9 births and 15.3 deaths (0 and 0 at stride 20) and 2.3 fusions (11.3). Measured speed is 1.8 px/tick instead of about 16.
- **couple:** the gliders' coarse level drives a linear-Gaussian oscillator. The glider path is unchanged bitwise, and the oscillator's response equals its closed form to 1.4e-15.
- **refine (mass-ring toy, each cell split in two):**
  - Exact refinement: pathwise defect 3.5e-32. Observations, exam MSEs and the closure gap (0.3156 nats) all match the coarse world to 1e-14.
  - Leaky in the mean: defect δ² = 0.020, `refine(tol)` rejects it, and the gap rises to 0.377 (SE 0.013).
  - Leaky only in the variance: pathwise defect 0.008, but the distributional δ² is 0 ± 0.002, so `refine(tol = 1e-3)` accepts it.

**Fisher by autodiff.**
- **Setup:** θ = (m₀, R), the growth centre of kernel 0 and the kernel radius. The world starts from one prepared state and runs one tick; the quantum is replaced by noise of std q/√12.
- **Checks:**
  - Autodiff matches central finite differences with common random numbers at h = 1e-8. Median per-path relative error is 3e-8 and 6e-8; the mean derivative agrees to 7e-4.
  - At h = 1e-6 the finite differences are already nonlinear.
  - `vw.fisher` on R matches my code to 7e-11.
- **Bounds (N = 2048):**
  - The complete-data upper bound is diag(6.2e12, 6.1e9), i.e. Cramér–Rao bounds of 4e-7 and 1.3e-5.
  - The moment lower bound is unresolved: the mean derivative's signal-to-noise is about 1, and the debiased value is −1e5 ± 6e6.
  - The certificate is therefore a bracket wider than five orders of magnitude.
- **Growth with horizon:** from tick 1 to tick 2 the per-path derivative grows ×1000 and the pathwise estimator's per-sample RMS ×1.1e4. The likelihood-ratio estimator, usable because the flow noise is additive Gaussian, grows only ×1.25. Its variance at 2 ticks is about 2e8 times smaller.

## What the types could not express, or expressed awkwardly

1. **The kick is fused into `Level.step`.**
   - stride evaluates it at every substep.
   - product cannot express a joint kick, which causes the matter creation above.
   - `lifted` handles only additive lifts.
2. **Programs are dense (T, B, n_in) arrays:** 1.3 MB per member-tick here, and every new T recompiles. I added `chunked_rollout`.
3. **Batching is vmap only.** I added `MapWorld`, which batches with lax.map.
4. **Pathwise equalities hold only within one compiled layout.**
   - lax.map equals unbatched execution bitwise.
   - vmap vs lax.map: equal for 1 tick, 1e-22 apart after 2, O(1) after 10.
   - So `replay="full"` and common-random-number branching are reproducible only with a pinned program, and the library's "vmap equals a loop" test only holds on toys.
5. **The certificates assume cheap, independent trajectories.**
   - `closure` would need about 35 CPU-hours here.
   - `leak` forms a 32768² covariance (8.6 GB).
   - `input_capacity` probes all 16383 zero-sum directions.
   - Only VW-0's stationary time-series plan worked, run through the designer API.
6. **`fisher` has four gaps.**
   - It differentiates whole leaves only, so m₀ needed an embedding.
   - It ignores the quantum, so with zero observation noise the covariance is singular.
   - It does not debias: 4.7e6 raw vs about 0 debiased.
   - Its pathwise estimator collapses under chaos.
7. **`commutation_error` measures a mean defect only,** so it misses variance leaks.
8. **Smaller gaps.**
   - There is no fan-out ⟨Φ₁, Φ₂⟩; I wrote `phi.pair`.
   - Memories cannot be recorded, so I added an audit view of the tracker.
   - There is no `prepare(params)` hook, so speed relies on XLA hoisting the kernel FFTs.
   - `stride` silently keeps a tracker that no longer works.

## Recommended changes

**Library.**
- Split `Level` into a declared kick κ(x, u), flagged conserving or state-dependent, and a law F(x, noise). stride then applies κ once, product takes a joint kick or a per-block port, and refine checks lifting for any κ.
- Make product's port refuse a zero-sum over the union unless the kick is joint.
- Use sparse k-entry programs with fixed-length chunks, and add `World(batching="vmap"|"map")`.
- Give certificates a sampling plan (stationary runs plus branches), sparse random input probes, and PCA for leak.
- `fisher`: accept a θ-embedding, add a resolution-noise floor, debias, report the complete-data bound alongside, and add the likelihood-ratio estimator for additive-noise levels.
- `commutation_error`: add a second-moment (Gaussian W₂) term.
- Add `pair`, memory records `M<j>`, `Level.prepare`, and a warning from `stride` on memory coarse-grainings.

**Note.**
- Prop. 1 and Section 9: say that pathwise couplings and exactness hold only to rounding × e^{λt}. Declare a finite-time Lyapunov rate as a certificate (about 0.2 per substep here).
- Open question 5 is answered for chaotic worlds: the complete-data bound is not enough, by more than 10⁵. Make the likelihood-ratio identity the default estimator for additive-noise presentations.
- Prop. 5's defect must go beyond the mean; the variance-leaky refinement is a counterexample to mean-based acceptance.
- Section 6.2: a joint zero-sum port over conserving, state-dependent kicks creates matter. Require separable constraints or a joint kick.
- Prop. 10(e) is now measured. Prop. 9(c) is confirmed pathwise: exam MSEs are unchanged under exact refinement to 1e-15.

Files are in `/home/user/evalwork/vecworld/vw1/port/` (`results/` holds every JSON output and log; `README.md` maps each script to its item):
- `flowlenia_jax.py`
- `phi.py`
- `aworld.py`
- `check_level0.py`
- `check_phi.py`
- `check_batching.py`
- `check_world.py`
- `repro_closure.py`
- `closure_vw0_subsample.py`
- `compose_demo.py`
- `refine_toy.py`
- `fisher_demo.py`
- `fisher_lr.py`