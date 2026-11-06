# VW-0 vector-world spec: report

I wrote the contract (DESIGN.md, 2,410 words), a generic `VectorWorld` implementation with an agent API and a designer API, and a linear-Gaussian calibration family with exact formulas. On seven calibration worlds the estimators agree with the exact values, and all 37 pytest tests pass in about 8 seconds. I could not save this report as `REPORT.md`, because the harness blocks report files from subagents, so it is returned here instead.

Everything is in `/home/user/evalwork/vecworld/spec/` (496 KB):
- `DESIGN.md`: the contract.
- `vecworld.py`: the generic world, agent API, designer API, exam harness and composition operators.
- `lingauss.py`: the linear-Gaussian family, its exact formulas and the toy worlds.
- `calibrate.py`: the calibration run. Its results are in `calibration/summary.md`, `calibration/results.json` and `calibration/calibration.png`.
- `tests/test_contract.py` and `tests/test_calibration.py`.

## The contract in brief

- **Levels.** Level 0 is a hidden vector h0 evolving under a fixed, noisy law F0 that does not depend on time or on the agent. Level 1 is h1 = Φ(h0, m), where Φ is fixed and many-to-one. The optional tracking memory m depends only on the level-0 history (object identities, for example), so (h0, m) together form a Markov state and level 1 never has independent state.
- **What the agent sees and does.** It observes the level-1 vector through a hidden permutation, with declared noise and rounding. Its inputs are added to h0 through a hidden permutation of the input coordinates.
- **Why permutations only.** Permutations are the only linear maps that preserve sparsity, the per-value bound, the per-tick total, zero-sum and positivity all at once. A rotation would turn a one-coordinate poke into a smear across all of level 0. Sign flips are an option on the observation side only.
- **Input constraints.** The world declares k, [lo, hi], a per-tick total, zero-sum, a minimum interval, a value step, an episode budget and input noise.
  - Whether an input is allowed depends only on public information.
  - A violation raises `InputViolation`: nothing runs, nothing is charged, and a whole program is validated before any of it runs.
  - Limits that depend on the hidden state belong inside the input physics, not in rejections, because a state-dependent rejection would leak hidden information.
- **Scored task.** The agent predicts level-1 vectors under held-out open-loop programs. Each exam item reveals a run of past observations, then a program and query times. Scoring uses many replicate futures branched from the hidden state. The references are a persistence baseline, the designer's best level-1-only predictor (the ceiling), and an oracle that knows h0.
- **Certificates.** All are measured conditional on the program, at several horizons and past lengths:
  - the closure ceiling and gap, including multi-step futures and the one-step split into memory and residual;
  - leak, meaning how much of h0 can be read from level-1 history;
  - input capacity and observation capacity;
  - provisional admission flags.
- **Composition.** Concatenation, coupled product, stacking (level 2 = Φ2(h1)), time striding, and extending downward to a level −1, which comes with a commutation-error check.

## API

```python
w = VectorWorld(spec, world_seed); w.card(); o0 = w.reset(seed)
o = w.step({3: 0.5, 17: -0.5})              # sparse dict or dense vector, agent coordinates
Y = w.run([(0, {...}), (5, {...})], query_times=[1, 4, 8], seed=None)
d = w.designer                               # privileged: d.state(), d.branch(rep, fresh=False), d.ensemble(B, seed)
d.closure(...); d.leak(...); d.input_capacity(...); d.observation_capacity(...); d.certify(...)
Exam(w, n_items, prefix, horizon).score(predictions, references={...})
product(a, b, coupling=...); stack(spec, Phi2, n2); stride(spec, s); refine(spec, F_fine, n, psi, ...); commutation_error(...)
```

Noise is fixed by (stream, seed, member, tick), so branches that share a seed get identical noise regardless of batch size. The reset modes are `initial` (default: the same seed gives the same starting state with fresh noise), `full` and `none`.

## Calibration results

Seven worlds were built through the generic code:

| world | n0 |
|---|---|
| ring: damped diffusion, 6 block sums, zero-sum inputs with k = 2 | 24 |
| mass-conserving ring | 24 |
| random non-normal system, 12 of 16 coordinates actuable | 16 |
| `product` of ring and random | 40 |
| `stack` of ring | 24 |
| exactly lumpable `refine` of ring | 48 |
| leaky `refine` of ring (η = 0.3) | 48 |

Each used 40,000 trajectories per program (3 programs), oracle estimates from 8,000 × 16 fresh-noise branches, and 8-fold standard errors. The full run took 2.5 minutes on one core.

| check | result |
|---|---|
| closure gap, errors, ceiling, multi-step gap (5 horizons × 6 pasts) | max \|z\| 1.4–3.5, rms 0.8–1.6 |
| ring at τ = 1, past 16: gap / ceiling | 0.268 ± 0.005 vs exact 0.271 / 0.980 vs 0.980 |
| ring memory / residual split | 0.029 / 0.268 vs exact 0.029 / 0.271 |
| leak information | ≤ 0.13% relative error; leak dimensions identical |
| input response | exact to 1.4e-15 |
| input singular values / capacity bound | ≤ 1.0% / ≤ 0.44% relative error |
| observation information rate | ≤ 0.02 bits/tick off |
| gaps add under concatenation; lumpable refinement leaves the gap unchanged | both to 1.8e-15 |
| commutation error, leaky refinement | 0.233 vs exact 0.230 |
| exam: Kalman predictor and oracle | within 1–2 SE and within 1.6% of exact |

The gaps do not change with the input program, as the theory predicts for this family.

What the certificates say about the ring: level 1 is nearly closed. The gap falls from 0.27 to 0.01 nats between horizon 1 and 16. Six of the 24 level-0 directions can be read from level-1 history. One direction can be pushed per tick, five input directions are visible at level 1, and the capacity bound is 4.7 bits per tick. The random world's inputs are nearly invisible at its bound of 0.5, and `certify` correctly flags it as `inputs_visible = False`.

## Open design questions

1. **Thresholds.** The admission thresholds are guesses. Which gap and leak values keep a level both universal and probeable needs mapping with real agents.
2. **Nonlinear worlds.** The linear level-1 predictor is exact only for this family. On nonlinear worlds it overstates the closure gap, and the linear leak decoder understates how readable level 0 is. A nonlinear calibration family with a computable optimal filter (for example a lumpable finite-state Markov chain) should come before Lenia-like laws.
3. **Reset default.** `full` gives the agent identical noise across resets, a strong counterfactual tool; `initial` is closer to a lab. Should the exam depend on which one a world uses?
4. **Leak dimension.** It is an integer count with a threshold and can flip when an eigenvalue sits near ½; this happened in one test run. Reports should give the full spectrum.
5. **Capacity bound.** It ignores sparsity, so it is loose when k is much smaller than the number of inputs.
6. **Standard errors.** Eight folds give noisy standard errors (max \|z\| reached 3.5). More folds or a bootstrap are needed before these numbers act as hard gates.
7. **Scoring details.** Identity swaps in tracked object slots make squared error harsh, so slot-matched losses may be needed. Closed-loop exams would need directed information.
8. **Legibility.** The toy worlds are not meant to be legible. The first world graded against the ALife rubric (persistent individuals, motion, interaction) needs a level-0 law with individuals and a Φ made of density blocks plus tracked slots. That is outside this spec.