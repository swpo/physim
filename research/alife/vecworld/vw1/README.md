# VW-1: supervenient worlds as a category, with a JAX module library (7 Nov 2026)

- `note/CATEGORY.md`: the formal note. Levels are open stochastic systems (Markov kernels with inputs and a public
  admissibility automaton); coarse-grainings are deterministic causal transducers; exact morphisms form a symmetric
  monoidal category; approximate ones carry a metric defect (affine composition) or a closure defect (chain rule);
  ports form a lens; stack, product, stride, refine and couple with their laws. Edited by the checker (marked
  "[Checker]").
- `vw/`: the JAX library (`Level`, `CoarseGrain`, `InputPort`, `ObservePort`, `WorldSpec`/`World`, the operators,
  agent and designer APIs, certificates including autodiff Fisher, opaque host blocks). 81 tests pass.
- `port/`: VW-0's A_gliders world re-expressed in the types (Flow-Lenia in JAX, Phi_coarse in JAX, Phi_objects as an
  opaque block), composition demos on the real world, the Fisher demo. Large arrays omitted.
- `check/`: the independent check, including adversarial tests of stacking associativity and stride composition.
- `reports/`: the four agents' reports; `reports/check.md` lists corrections to the others.

Setup used: a separate venv with `jax[cpu]`, numpy, scipy, pytest (never the physim venv, whose numpy and scipy the
lab bundles pin). Scripts use absolute paths under `/home/user/evalwork/vecworld/` from the build session.
