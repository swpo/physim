I've built the JAX library at `/home/user/evalwork/vecworld/vw1/vw/` (importable as `vw`). All 81 tests pass in 3.4 minutes on 2 cores. I created the shared venv at `/home/user/evalwork/vecworld/vw1/.venv`; it did not exist yet. The package is 0.8 MB, and nothing was written outside it except the venv.

**API**
- **Level** (`core.py`): `init(params, key)` and `step(params, x, noise, u)`. The state is any pytree, `u` is a flat vector of length `input_dim`, and `params` are the parameters Fisher differentiates against. A level can instead declare `step_xi` (explicit standard-normal noise), which correlated products need. It can also declare `conserved` quantities.
- **Noise** (`core.py`): randomness is a function of a key and a clock. `noise.stream(i)` gives an independent stream; `noise.substep(n, i)` sets the clock to t·n + i.
- **CoarseGrain** (`core.py`): `phi(x, m)` with optional `init_memory` and `update_memory`, plus `start` and `transduce`. Helpers: `identity`, `compose`, `compose_all`, `product_cg`, `unit_level`.
- **InputPort** (`ports.py`): an `Admissible` set (k, lo/hi, total, zero_sum, min_interval, value step, episode budget), the actuable indices, actuation noise and a hidden `in_map`. Violations raise `InputViolation` with nothing run or charged. Whole programs are validated first.
- **ObservePort** (`ports.py`): hidden permutation, optional sign flips, noise, clip, quantisation, max_queries.
- **WorldSpec / World** (`world.py`): `WorldSpec(base, chain, inport, outport, observe_at, …)` is the declaration. `World(spec, world_seed, params)` draws the permutations and gives the agent API: `card()`, `reset`, `step`, `run(program, query_times)`.
- **Designer** (`world.py`): `world.designer` gives privileged `state()`, `branch(rep, fresh)` with identical noise, `ensemble(B)` by vmap, `from_states`, and `rollout(ens, P, T, rec=…)`, a jitted scan with per-member programs.
- **Certificates** (`certificates.py`): closure (ceiling and gap over pasts and horizons, block gaps, Atay split), leak, input and observation capacity, invariant drift, `fisher`, `certify`. The exam harness is in `exam.py`, batched.

**How the operators are implemented**
- **stack**: appends a coarse-graining after the observed level and re-draws the observation permutation.
- **product**: states are tuples and inputs are concatenated. Noise can be `'independent'` (stream i per factor), `'shared'` (common random numbers) or `('correlated', rho)` for two explicit-noise levels. Chains are aligned with identity padding, and the product is anonymised jointly.
- **couple**: before the laws run, the source's observed level is read through a declared sensor (noise, value step) and mapped by `wire` into the destination's actuators. On the destination's actuable coordinates it is clipped into the per-tick admissible set and given its actuation noise. The source's tracking memory moves into the coupled level-0 state, which keeps level 0 Markov.
- **stride**: a `lax.scan` over n sub-steps, with the input before the first.
- **refine**: the fine level becomes level 0 and psi is prepended to the chain. The input port must enter at level −1: lifted actuation (via `lifted`) keeps the old port, otherwise a new port is declared. `check=`/`tol=` runs `commutation_error`.
- **commutation_error**: measures the defect two ways. The pathwise version drives both levels with the same noise. The distributional version compares means and removes the Monte Carlo bias.
- **Opaque blocks** (`opaque.py`): `host_level` and `host_coarse_grain` wrap `jax.pure_callback`, with declared shapes and the key passed to the host. They still run under jit, scan and vmap, so everything composes. They give up autodiff (`fisher` raises `NotDifferentiable`), XLA fusion, a host round trip every tick, vectorised batching (unless `batched=True` with vectorised host code), and they must be pure.

**Changes to the agreed definitions, and why**
1. **Counter-based noise.** With plain key splitting, stride n then m equals stride nm only in distribution. With the clock rule above, stride(stride(L,n),m) equals stride(L,nm) step by step, and stride commutes with product.
2. **Exactness that composes is pathwise.** Phi∘F = F'∘Phi as kernels does not tell you how defects add. The triangle bound rms(ψ₂ψ₁) ≤ Lip(ψ₂)·rms(ψ₁) + rms(ψ₂) holds for pathwise defects under shared noise. For mean defects it holds only for linear ψ.
3. **Zero-sum fix.** Accepted commands are made exactly zero-sum (or snapped to the value step with an integer sum of zero) before they reach the world.
4. **Replica leak closed.** Episode keys include the world seed. In VW-0, two replicas reset to the same seed shared the hidden trajectory, which hands the agent the relative permutation.
5. **Zero-sum input-capacity probes.** The input-capacity certificate probes along an orthonormal basis of the zero-sum directions. The VW-0 single-coordinate probes create mass, so a conserving kick gives no response to them.
6. **Fisher bound.** The certificate returns J^T S⁻¹ J, which is a lower bound for any observation law, plus the Gaussian covariance term, which makes it exact for Gaussian observations.
7. **Card.** No level or coarse-graining names, K, stride or n0; only `public_notes`, which the designer writes on purpose.

**Test results** (`vw/tests/`)
- **Contract (22):** card has no names, permutations, all constraint families, nothing charged on rejection, budgets, `run` equals repeated `step`, replay modes, shared-noise branches give the exact linear response.
- **Ports (9):** the review case (sum 9e-10, total |a| 0.9) is accepted, and after 25 ticks mass drifts by less than 1e-12 relative, in both an additive and a pooling world. A sum of 2e-9 is rejected. Clipping into the admissible set always yields an admissible command.
- **Category laws (16):**
  - The identity coarse-graining is a unit, bit for bit.
  - Stacking is associative to 1e-12.
  - The product equals the pair exactly.
  - Correlated noise with rho = 0 equals independent noise; the measured correlation at rho = 0.6 is within 0.02.
  - stride 2∘3 = 3∘2 = 6.
  - Exact refinement has pathwise defect about 1e-31. Started from matching states with the same keys, the refined world's observations equal the base world's at every tick.
  - Leaky refinement: defect 0.228 measured vs 0.230 closed form.
  - Triangle bound: 2.26 ≤ 3.59.
  - Coupling: deterministic cascade exact, one-step covariance within 5%, destination mass conserved.
- **Calibration (18):** the port of `spec/lingauss.py` (closed-form self-consistency, estimator z-tests, leak, capacity, observation rate, exam vs Kalman, commutation, certify). It also runs on product, stack and leaky-refine worlds.
- **Purity (6):** jit equals eager, vmap equals a loop, results do not depend on the host episode state, one ensemble member equals a single run.
- **Opaque (5)** and **Fisher (5):** the Fisher estimate matches the closed form to within 1–2% (gamma 36206 vs 36525); with beta = 0 the gamma information comes only from the covariance term.

**Speed:** about 0.68M member-ticks/s for the ring and 0.52M for the mass ring on 2 cores; about 2.3 ms per agent step; a default-size closure takes about 10 s.

**Limits**
- Certificates are estimated through linear, Gaussian approximations, so on nonlinear worlds they are bounds rather than exact values (as in VW-0).
- Fisher is computed on the unquantised channel, needs differentiable blocks, and its cost grows with members × observation dimension × parameters (chunked).
- The coupling clip covers only per-tick constraints, not min_interval or the episode budget.
- The product is associative only up to re-bracketing and only in distribution, not pathwise.
- Stack and product drop levels above the observed one.
- The noise clock is folded as 32 bits and wraps after about 4.3e9 sub-steps.
- Only open-loop programs; no closed-loop exams.
- I did not port the Flow-Lenia world.