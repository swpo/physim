# Track A R6 — executable predictor (draft 0.1)

**Status: first offline prototype and physics dossiers reviewed; draft policy, not a shipped environment.**
Direction approved for specification, bounded native prototype tests, and parallel
privileged reviews of existing worlds. No paid model rollout, new pod, broad
simulation battery, or evolution campaign is authorized by this phase.

## 1. Scientific objective and scope

The investigator gets instruments, interventions, and a reproducible starting
point. It must explore, decide where to look, and build a predictive theory. It
need not reconstruct field equations or use the evaluator's vocabulary. A compact
empirical model can be a successful theory.

These dossiers are developer/oracle material. Publishing them for human review
is not proof that they are private from an evaluated agent. Future exploration
and submission runtimes must exclude oracle rules, geometry, caches, dossiers,
and truth from the agent's context/filesystem/network. The two published worlds
are development cases; contamination and genuinely held-out evaluation require
an explicit policy before any benchmark claim.

The deliverable is executable prediction code, not six answers to revealed
contracts. An evaluator privately examines the world using its rules and full 2D
fields, writes evidence-backed physics hypotheses, and tests consequences of
those hypotheses through the same observation interface available to the agent.
This private coverage map does **not** become a public mentor syllabus.

Physics is not generic. Interesting structure can be concentrated in special
places, times, conditions, or interactions. Generic baseline difficulty or a
large sensitivity/noise ratio is not proof of interesting physics. Nor is every
null response uninteresting: invariance, selectivity and an absence predicted by
a theory can be substantive tests. Uniform dense sampling alone does not solve
coverage. Neither does a finite test battery prove universal understanding.

The first pass uses existing `p6g8_033`/seed942 and `p4g2_044`/seed928 caches.
These are starting candidates for study, not certified examples of any claimed
law. Analysis does not turn the two provisional R5 rollouts into clean benchmarks.

## 2. Agent-visible prediction interface

```python
def predict(actions, queries, n_samples=64, seed=0):
    # -> {"samples": [array_for_query_0, array_for_query_1, ...]}
    ...
```

Example request (illustrative, not a disclosed test case):

```json
{
  "actions": [
    {"t": 830.0, "kind": "inject", "port": 6, "amp": 2.8, "dur": 10.5},
    {"t": 845.0, "kind": "adjust", "device": 0, "u": [0.37, -0.07, -0.10]}
  ],
  "queries": [
    {"sensor": "device1", "t": [840.0, 855.0, 880.0, 1005.0]},
    {"sensor": "global", "t": [1230.0]}
  ],
  "n_samples": 64,
  "seed": 17
}
```

- The world includes its fixed initial fields, initial apparatus configuration,
  and base pseudorandom stream. These are opaque to the agent. Every request
  begins at this starting point at t=0. No `history` or public `anchor_t` is
  needed. Artifacts learned during exploration may be packaged with the code.
- Times are absolute, nonnegative, and use the instrument's time units. The
  internal integrator has dt=0.02. Off-5-tu query times can be represented; the
  prototype must define a public accepted time grid/tolerance and reject
  unsupported times explicitly. It must not promise arbitrary real precision.
- Actions are scheduled adjustments and emissions. Waiting is implicit in
  timestamps; reading is a query. There is no scheduled fork/reset action.
  Starting another request supplies reset-to-origin semantics. Adaptive policies
  that choose actions from future readings are outside the first prototype.
- Queries name device0, device1, or global. For a device, a response has shape
  `(n_samples, n_query_times, n_ports, n_slots)`; global has shape
  `(n_samples, n_query_times, n_ports, 2)` (spatial mean, spatial variance).
  Device0 has 13 slots and device1 has 19 for the existing roster. Port meanings,
  node geometry, field rules and private simulator seeds are not exposed.
- Sample index identifies one **joint trajectory across all queries**. Predictive
  uncertainty may reflect both model uncertainty and stochastic dynamics. Samples
  need not be Gaussian. They must have the documented sample semantics; marginal
  arrays with independently shuffled times are not coherent trajectories.
- The return object is `{"samples": [...]}`, not a bare list. Empty queries
  return an empty list; empty time lists return correctly shaped zero-time
  arrays. Validate the whole request before returning, then avoid simulation
  when no observations were requested. Preserve query order and repeated times.
  Actions must already be chronological. Reject booleans as numbers, malformed
  JSON shapes and nonfinite values. The proposed grid tolerance is 1e-9 tu.
  `n_samples` is a positive integer (fair-CRPS scoring requires at least two).
- `seed` controls predictor sampling only, not the evaluator's hidden realization.
  Every call is closed-book. Repeated calls with the same request and seed must
  reproduce the same output. Prefix and query-set consistency require tests.
- This is a bounded protocol language, not literally every possible experiment.
  Action limits, query horizon/count, simultaneous action order, overlap policy,
  command duration, output precision and artifact/compute budgets must be frozen
  before any episode. Exploration/evaluation domains must be stated honestly.
  In particular, above-apparatus emissions from R5 are **not** silently described
  as experimentally accessible interventions.

## 3. Noise and event semantics

Proposed policy A, as discussed: use the fixed base forcing stream until the
first effective state-changing action, then a private continuation stream per
truth member. Later actions do not reseed. Without actions, replay is fixed.
Queries do not branch, consume random numbers, or change the world. No-op
commands must have an explicit neutral rule, not an accidental reseed effect.

This is an evaluation convention, not a physical law. It is not the only
possible design. The primitive runtime and exploration tools must eventually
implement the same convention. The current tool surface has **not** been
certified to do so.

The simulator adds `2e-3 * sqrt(dt) * N(0,1)` to activator fields each substep,
between reaction and diffusion. Random initial placements are separate draws in
initialization. Existing code establishes this mechanism, not that noise is
necessary for motion, nucleation, or interestingness in these worlds.

The privileged implementation is `OracleRunner.sample_truth(..., truth_seed=...)`;
`truth_seed` is a required private keyword, not the public bundle's `seed`.
The submitted-code `Predictor` protocol only declares `.predict(..., seed=0)`.
A public predictor request must not be forwarded wholesale into the oracle call.
This API distinction is not itself a security boundary; isolation is a later gate.

Private continuation seeds must not depend on future actions, query contents,
query count, or predictor output. Otherwise even adding a passive query changes
finite-sample truth. Matched-protocol tests should use explicitly recorded common
random streams where appropriate. Full precision state plus RNG provenance is
needed for an internal restart; f16 record frames are not exact anchors.

**Open causal-comparison gate:** under A, a no-op sham stays on the fixed base
forcing while an effective treatment changes forcing. Simply subtracting those
outputs is not a common-noise paired intervention contrast. The first physics
reviews instead use archived control/treatment branches with the SAME restored
RNG. Before implementing confirmatory paired experiments or interpreting graded
contrasts, resolve whether to change the convention or use an explicitly separate
private paired-experiment helper. Do not silently equate either with public A.
The scheduler tests validate A's implementation, not its scientific suitability.

Scheduled adjustments change device pose at a documented instant and retain
legacy 5-tu command occupancy if that is kept. Emission source terms are active
on a documented half-open time interval. Same-time action/read ordering and
conflicts must be explicit. The prototype ends previous intervals, starts an action, then samples passive
queries at each tick. It rejects simultaneous starts, overlapping injections,
and overlapping adjustments (one command lane); injection and adjustment may
overlap at different start times. Adjacent endpoints are allowed. The proposed
prototype evaluation domain is amplitude [0,3], duration (0,50] on the accepted
time grid. Zero amplitude and actual no-op pose changes do not trigger a branch.
These bounds and overlap rules are implementation proposals, not proof of an
optimal public experimental interface.

Source review found another legacy mismatch: R5 transport rejects a bound-striking
dilation (and clips input commands), while its truth pose helper clips dilation.
The isolated prototype uses validated u in [-1,1] and core/truth dilation clipping.
Exploration parity remains an explicit integration gate, not an existing property.

### Compatibility with R5 is partial

| R5 case | Required caution for R6 comparison |
|---|---|
| L1 | R5 uses one deterministic base-realization truth after the walk; A may branch noise at the first adjustment. |
| L2 | R5 uses an additional hidden device absent from the proposed query roster. |
| L3F | Short horizons use base replay; long horizons branch at an explicit hidden anchor. No-action A does not do that. |
| L3E / L3S | R5 branches noise at a hidden anchor; no-action A replays the base. |
| L4 / L4D | Can be matched with identical anchor state, stream seeds, injection and observation semantics. |

Therefore 'all six old truths reproduce bit for bit' is not a valid blanket
acceptance gate. Match **both semantics and random streams** before claiming
parity. Reuse old numerical components; keep the historical scorer and traces
unchanged.

## 4. Private physics reviews and test selection

Parallel initial dossiers:

- [p6g8_033](../../agentenv/round6/physics/p6g8_033/STATUS.md)
- [p4g2_044](../../agentenv/round6/physics/p4g2_044/STATUS.md)

Each dossier separates:

1. **Observed phenomenon:** full-field visual sequence, location/time, scale,
   precise observable and data provenance. Sensor-local quietness is not global
   inactivity. A 2D image or a metric alone is not a mechanism.
2. **Candidate explanation:** explicit relation, invariant or mechanism; which
   rules support it; alternative explanations and known uncertainty.
3. **Compact experiment:** interventions, predictions that differ between the
   explanations, useful observations, controls, and replication required.
4. **Accessible test:** can this be found/measured using the actual apparatus?
   Separate information hidden from the agent from information impossible to
   infer through its allowed experiments. Lack of observability is a design
   limitation, not automatically a failure of science by the agent.
5. **Private coverage:** held-out parameter/time combinations and diagnostic
   readouts a predictor should capture if it learned the phenomenon. Include
   meaningful negative outcomes and boundaries, not only large responses.

First pass is existing-cache inspection and plotting only. Additional simulations
are proposed and costed separately. Sensitivity search may later help locate
conditions within a studied phenomenon. It does not replace the dossier or
certify that every high ratio is useful physics. Freeze evaluated regions before
scoring a final predictor; keep adaptive adversarial discovery separate from a
held-out confirmation set and report its selection bias.

## 5. Scoring: proposed, not implemented

Primary metrics are absolute, with explicit units and reductions. For a scalar
observable with IID predictive samples X_1..X_M (M>=2) and independent truth
samples Y_1..Y_K, an unbiased Monte Carlo estimator of expected distributional
CRPS is

```
mean_{m,k} |X_m - Y_k| - sum_{m != n}|X_m - X_n| / (2*M*(M-1)).
```

The usual empirical-distribution CRPS with denominator M^2 scores a finite
empirical distribution instead. Do not confuse those estimands. Test analytic
Gaussian/deterministic cases and sample-size effects before selecting the rule.

Report per phenomenon, protocol, sensor, port/readout, and horizon as useful.
Means and variances have different units; do not silently pool them. Marginal
CRPS does not test temporal or spatial dependence even if the API returns joint
samples. Add physics-specific trajectory readouts (e.g. timed passages or coupled
responses) and appropriate joint-distribution diagnostics. Define time resolution
and no-event/censoring conventions. Neither this map nor one aggregate proves
complete predictive coverage.

The full-state conditional oracle's expected CRPS is a **lower bound**, not an
agent-achievable universal floor. For a genuine stochastic ensemble its pairwise
absolute dispersion estimates that quantity. Deterministic truths have zero
floor. Small finite ensembles and partial observation make ratios unstable or
misleading. The earlier Gaussian leave-one-out number is a predictive estimate,
not proof that 1x means a perfect theory. No automatic 0-1 score is frozen here.

Keep raw CRPS alongside other error/calibration diagnostics. Any variability
normalization must name its source, observable, time span and reduction. The
existing exploratory absolute_scoring/ outputs used full-base spans, not always
pre-anchor history. They are now [archived unchanged with caveats](../../agentenv/round5/resource_revision/absolute_scoring/README.md)
in the migration commit, not adopted as a certified R6 score.
Synthetic oracle/lookup predictors are scorer diagnostics, not world-independent
criteria for deciding what physics is interesting.

## 6. Implementation stages and acceptance

### Completed first pass

- Root: this draft, source/visual review, independent 31/31 toy/native checks,
  and static evidence validation. [Review package](../../agentenv/round6/README.md).
- Runner worker: isolated oracle module/scheduler; 25 toy/API/checkpoint and six
  native tests; maximum six substeps per native trajectory; R5 compatibility matrix.
- Two world workers: existing-data physics dossiers with visuals, measured
  contrasts, candidate explanations and proposed experiments. No new truth battery.
- All three explicit handoffs were received and reviewed. The temporary watchdog
  was removed and workers retired. No automatic next-stage launch.

Required runner tests: request validation; exact event ordering; no query-induced
mutation or reseeding; prefix causality; coherent member trajectories; repeats;
multiple interventions; actuator clipping/duration; source interval boundaries;
matched private-state parity only where the protocol is truly the same.

### Later stages, separately reviewed

1. Review both dossiers. Pick concrete phenomena and minimal confirmatory
   experiments. Bound CPU, memory and storage from measurements, not assertions
   that hundreds or thousands of simulations are cheap.
2. Validate physical claims. Design/freeze a private battery and coverage report.
3. Implement scorer and a **real** isolated runtime for untrusted bundles. A
   normal subprocess, resource limit, or cooperative import restriction is not a
   security sandbox. Verify filesystem/network/process isolation independently.
4. Optional adaptation of old agent artifacts, explicitly labeled as adapters.
   Their missing generator inputs and narrow supported protocols may prevent a
   faithful rerun. Unsupported cases are not silently imputed or called original
   submissions. No benchmark conclusions from these two diagnostic artifacts.
5. Integrate the new deliverable/exploration protocol. Fix and regression-test the
   whole-state GET/PUT concurrency defect before any new rollout. Preserve old
   environments and cohorts as historical versions.
6. Only with explicit approval: a wiring smoke/pilot and any paid scale-up.
7. Feed confirmed, useful physics measurements back to world selection as
   candidate metrics, with false-positive/transfer tests. Do not automatically
   replace all evolutionary metrics with sensitivity counts.

No implementation claims, agent scores, new physics laws or successful security
isolation are implied by this draft.
