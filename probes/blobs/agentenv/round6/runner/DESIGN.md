# R6 oracle runner — independent experiments v1

The shared scientific contract is documented in
[TRACKA_R6_PREDICTOR.md](../../../l0/deepsearch/TRACKA_R6_PREDICTOR.md). The concrete
agent-facing worked-example contract is
[AGENT_SPEC.md](../worked_example/AGENT_SPEC.md).

`physim.blobround6.OracleRunner` is a private native scheduler.
`Predictor.predict(actions, queries, n_samples=64, seed=0)` is the structural
submitted-code interface; it does not implement a model. The evaluator calls
`sample_truth(actions, queries, n_samples, truth_seed=...)` separately.

## Physical state and noise

An oracle owns a full-precision prepared state, initial devices, anonymous port
permutation, actuator map and fixed emitter. Initialization is private dependency
injection. `_native_oracle` constructs a native initial world;
`worked_example/p4g2_044/origin.py` binds the existing exact prepared snapshot to
public time0 and checks its hash against the demonstrated state.

Each member clones those initial fields and devices, and receives fresh ongoing
forcing **from time0**, including no-action and zero-amplitude experiments.
The evaluator selects a fresh private experiment seed per call; member streams
are derived in the `independent-experiment-v1` namespace. Seeds do not depend on
the predictor's seed, actions, queries or output. Later actions never reseed.
Queries are passive. A debug rerun with the same private experiment seed is
reproducible, but noise matching is not part of the agent task or scoring.

The former policy A (fixed base noise until the first effective action) and its
shared base-continuation cache have been removed. Exact physical preparation
remains; stochastic continuations are never silently reused between experiments.
This intentionally changes no-action and pre-intervention truth semantics.
Historical first-pass validation artifacts describe the former implementation.

## Scheduling

The parser validates the complete request before physics. Time grid0.02,
tolerance1e-9; exact keys; finite JSON numbers; integer IDs; controls[-1,1];
source amplitude[0,3]; source duration(0,50]. Actions have strictly increasing
start times. The shared adjustment lane is occupied for5tu; the injection lane
is occupied for its duration. Same-lane overlap and simultaneous starts are
rejected; distinct lanes may overlap. A no-op still reserves its interval.

Sources occupy[t,t+dur). The scheduler advances to the event, ends any old
source, applies a new action, then samples. Adjustments change pose immediately;
dilation clips to native bounds. The emitter remains fixed. Native port
permutation, sensor interpolation, source operator and stepping are reused.
Returned arrays are float64 with shape(members,times,ports,slots), retaining
joint member identity across query arrays. Public exploration and evaluation
require strictly increasing, unique times within each query through
`blobround6_eval.validate_case`. The private native scheduler retains general
query-order support for historical diagnostics; submitted predictors never need
to implement it. Query objects retain their requested order.
Empty observations cause no stepping. Actions after the final query are checked
but do not extend integration.

## Limits and verification

The scheduler is a trusted library, without independent request budgets.
`physim.blobround6_eval` checks horizon, action, query, member, output and scoring
work caps before invoking it. A data-only JSON prediction-bundle scorer is
available; reviewed in-process predictor adapters are explicitly trusted code,
not a sandbox for arbitrary submissions.

Run the scheduler tests with:

```text
.venv/bin/python environments/physim/tools/test_blob_round6.py --gates toy native
```

The29 updated tests cover grammar, independent sham/pre-action forcing,
no-op neutrality, passive pose and query behavior, source boundaries, native
primitive agreement, owned physical origins and member coherence. The short
native tests span at most0.12tu. The worked-example native validation separately
executes the real50tu requests and complete sensor arrays. Neither replaces
checks of an eventual isolated model runtime or R5 transport state integrity.
