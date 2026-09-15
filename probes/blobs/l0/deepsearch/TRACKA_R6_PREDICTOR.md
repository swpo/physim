# Track A R6 — executable predictor, worked-example specification v0.3

This is the current offline R6 design. The
[p4g2_044 worked example](../../agentenv/round6/worked_example/README.md) combines
confirmed physics, anonymous prediction programs, independent native truth,
and executable scoring. The first smaller-model pilots are recorded in its
rollout report; the next pilot uses64 responses and strictly increasing query
times. Registry design and broader world exploration remain later stages.
The historical first-pass documents and
validation JSON describe earlier code; their policy-A convention is superseded.

## Scientific objective

An investigator gets instruments, interventions and control of a repeatable
physical starting point. It explores, decides where to look, and builds a
predictor. It need not recover equations or adopt the evaluator's terminology.
A useful empirical model can be a successful predictive theory.

The evaluator privately investigates a world and selects observable consequences
of its demonstrated physics. That investigation is not a mentor syllabus for
the agent. Interesting behavior can involve a selective response, delayed effect,
spatial rearrangement or meaningful null. Evolutionary fitness, visual activity,
baseline difficulty and signal-to-noise ratio are useful diagnostics, not proofs
of scientific interest. A finite case suite establishes finite coverage.

The reusable unit is a world package: immutable world definition and simulator
provenance, prepared instances, apparatus/noise settings, reproducible experiments,
causal evidence, and executable prediction cases. The first packages are public
development examples. Future claims about discovery in unfamiliar worlds require
separate held-out worlds. Registry storage and publication are later work.

## Shared prediction interface

```python
def predict(actions, queries, n_samples=64, seed=0):
    return {"samples": [array_for_each_query]}
```

Every request starts from the same opaque prepared physical state and apparatus
at public time0. It contains the complete subsequent action history. There is no
public field-state, physical seed, coordinate map, `history` or `anchor_t` input.
Artifacts learned during exploration may be packaged with the predictor.
Starting another experimental request supplies reset-to-origin semantics;
scheduled fork/reset actions are unnecessary. The first interface covers fixed
programs rather than adaptive actions chosen from future observations.

`actions` contains `inject` or `adjust` objects; `queries` selects `device0`,
`device1` or `global` and lists absolute times. Device output shape is
`(n_samples,n_query_times,n_ports,n_slots)`. The current example has12 ports and
13/19 device slots. Global output has2 slots: spatial mean and population
variance. Ports are anonymous but consistent across source and sensors.

A sample index identifies one joint predicted trajectory across every query.
Samples can represent stochastic and model uncertainty without a Gaussian
assumption. A deterministic model may repeat its prediction. `seed` controls
only the predictor's sampling. Same request and predictor seed should reproduce
its output; adding future actions or passive queries should not change earlier
predictions. Prediction receives no experimental-service access.

The exact agent-facing grammar and bounds are in
[AGENT_SPEC.md](../../agentenv/round6/worked_example/AGENT_SPEC.md). Both
exploration and evaluation use source amplitude[0,3], duration(0,50], controls
[-1,1], dt0.02 with tolerance1e-9, and native dilation clipping. The worked
example's maximum public time is50. It deliberately does not inherit R5's
amplitude1 exploration cap.

## Independent noise and event semantics

Each experiment restores the prepared physical state and evolves with fresh
ongoing noise from time0. The evaluator runs one or more independent realizations
and compares predicted distributions with them. It does not align predictor
members with physical members or expect prediction of random disturbances.
No-action experiments and shams also have fresh ongoing noise. Noise is not reset
by injections, pose changes or queries. The native coefficient remains0.002;
no additional sensor noise is introduced.

The private oracle method is
`sample_truth(actions,queries,n_samples,truth_seed=...)`. Its seed is selected
independently by the evaluator for each experiment. Member streams use the
`independent-experiment-v1` namespace. Reusing a private seed enables debugging;
it is not an agent capability, a grading condition, or a scientific requirement.
A predictor's sampling seed never enters the oracle. There is no cached common
base continuation across experiments.

The earlier policy A held base noise fixed until the first effective action.
It has been replaced. Exact physical state restoration is retained; matching a
future microscopic realization is not. Optional common-forcing causal diagnostics
remain supporting investigator tools and do not define evaluation semantics.

Actions must have strictly increasing starts. Injections occupy[t,t+dur);
adjustments change pose at their start and occupy a shared lane for5tu. Same-lane
overlap and simultaneous starts are rejected. Injection and adjustment may
overlap with different starts. No-ops still occupy their declared intervals.
At an event time, previous injection ends, a new action starts, then readings
are sampled. Queries are passive. Times within each public query must be strictly
increasing without duplicates; different queries may cover overlapping times.
The predictor preserves query order and each query's chronological time order.
The emitter remains at its fixed initial location while devices move.

The parser validates the complete request before physics. Finite JSON numbers,
exact keys and integer IDs are required; booleans are rejected. Empty observations
are valid at the protocol level and cause no stepping. Scoring requires at least
one observation. Actions beyond the last query are validated but do not extend
integration. Prepared snapshots are full-precision fields, never float16 movie
frames. Native dynamics in this example are autonomous, so rebasing original
time1700 to public0 changes timestamps without changing the dynamics.

## From physics to cases

Investigations distinguish observed behavior, candidate explanation, causal test,
apparatus observability, and supported scope. Each accepted phenomenon provides:

1. A reproducible physical preparation and intervention program.
2. Full-field evidence that identifies what happened, including spatial scope.
3. Causal evidence for the claimed explanation, with privileged diagnostics
   explicitly separated from agent-accessible actions.
4. Actual anonymous sensor queries and native readings establishing observability.
5. Independent-noise repetitions at the relevant horizon.
6. A private case/feature definition, evidence links, and limits on interpretation.

The initial worked example includes pulse survival/extinction/rebound, feedback
that changes fate, and spatial observations. Further confirmed discoveries add
versioned cases. Generalization to other amplitudes, timings, preparations or
longer horizons is not admitted solely because a case generator can emit it.
New parameter regions require evidence. Case selection is frozen before a model
is evaluated; exploratory adaptive selection is identified as such.

The agent sees action/query payloads and generic interface documentation. Private
mechanistic names, geometry, source definitions, full fields, case reductions and
causal diagnostic data belong to the evaluator. Local development files are not
an isolation boundary; the eventual agent runtime must enforce this separation.

## Implemented scoring

`physim.blobround6_eval` validates complete output shape and finiteness, then
scores the empirical predictive distribution against independent observations.
Prediction and truth ensembles may have different member counts. Whole-member
permutations leave the score unchanged.

For predictive samples X and truth samples Y, marginal CRPS is:

```text
mean(m,k) |X_m - Y_k| - 0.5 * mean(m,n) |X_m - X_n|
```

The second mean includes self pairs and uses M². This scores the submitted
finite empirical distribution; it is not the unbiased/fair estimator of an
underlying infinite-sample predictive law. One predictive member is supported.
CRPS is reported by query, port and slot in native units. Field means and
variances have different units and are not silently pooled.

For each predeclared salient group, selectors form a vector across time, port,
slot or device. Coordinates are divided by fixed positive scales. The energy
score uses the same cross-minus-half-self formula with the RMS Euclidean distance.
It therefore tests joint temporal/spatial behavior that marginal scores can miss.
Group scores use the declared scales and receive equal weight within a case;
case-level aggregation is stated in the worked-example report. No universal0–1
normalization, exact noise-floor normalization or baseline-relative reward is
adopted. Detailed marginal and group results accompany the aggregate.

The evaluator checks action/horizon, member, query, output and pairwise-work caps
before prediction or truth computation. Malformed prediction output is rejected
before spending native truth work. Data-only JSON bundles allow offline scoring;
reviewed in-process adapters allow integration tests. Neither is a sandbox for
executing arbitrary submitted Python.

## Implementation and next acceptance gate

The native scheduler, local experiment adapter and offline evaluator are separate
from the historical R5 server and its scoring. R6 exploration uses the same
parser, apparatus math, action domain and independent-noise oracle as evaluation.
The local service restores the origin on each complete-history request and
serializes budget admission. It is not yet a production model-facing transport.

Tests cover grammar, event ordering, fresh sham/pre-action noise, no-op neutrality,
owned physical origins, native primitive agreement, member coherence, malformed
outputs, proper score formulas, dependency-sensitive joint scoring, sample-order
invariance, and resource caps. The worked example also runs complete native
trajectories through the actual scheduler and scores historical development
references against fresh truth. Such references check wiring; they are not agent
results or evidence of held-out scientific generalization.

Before smaller-model pilots, provide an isolated exploration/submission runtime,
freeze model-facing budgets and packaging, and test its filesystem/network/process
boundary. Do not route pilots through the known R5 whole-state GET/PUT concurrency
path without fixing it. No paid models, remote pods, registry publication or
broader evolution run is part of this worked-example implementation.
