# R6 executable predictor — Phase 1 runner design

**Status: isolated prototype complete; not a shipped environment.**
The parent confirmed the event, noise, and proposed evaluation-domain rules below.
Final resource budgets and exploration integration remain open.
No production or R5 transport code changed.

## API boundary: submitted predictor versus privileged oracle

The submitted-code contract is:

```python
predict(actions, queries, n_samples=64, seed=0)
# -> {"samples": [numpy_array_for_query_0, ...]}
```

`blobround6.Predictor` is only a structural `Protocol` for this interface.
It is not an implemented agent model, native simulator export, grader, or sandbox.
The submitted predictor's `seed` controls its own samples only.

The implemented privileged engine is separate:

```python
oracle = _native_oracle(world, hidden_seed, workers=1)  # evaluator-only binding
oracle.sample_truth(actions, queries, n_samples=64, truth_seed=grader_owned_seed)
# -> {"samples": [numpy_array_for_query_0, ...]}
```

`OracleRunner.sample_truth` requires keyword-only `truth_seed`; there is no default
and no `seed` alias. The evaluator must choose this seed independently of the
submitted predictor's seed. The truth-only member hash domain is
`physim/blobround6/truth/policy-A/v0`. Its only variable inputs are the grader-owned
truth seed and member index. It excludes the hidden initialization seed, queries,
actions, and submitted predictor output or sampling seed.

Each request starts logically at the same opaque, exact world `t=0`: fields,
initial apparatus, and base RNG state. There is no public history, anchor, hidden
seed, geometry, or simulator-state argument. The private binding is not part of
the submitted predictor API.

Results preserve input query order and each query's time order. Each array has
shape `(members, times, ports, slots)`. Native device0 has 13 slots, device1 has
19, and `global` has exactly two slots: spatial mean and spatial variance. These
are instantaneous observations, not time-window reductions. The same member
index identifies one joint trajectory across every query, device, and time.
Containers are float64 without output rounding. Native global reductions retain
the native float32 calculation before their exact conversion into the container.
No private metadata is returned.

## Exact JSON grammar and support (v0)

- `actions` and `queries` are Python lists of JSON-shaped dictionaries, not JSON strings or tuples.
- Inject object: exactly `t`, `kind="inject"`, `port`, `amp`, `dur`.
- Adjust object: exactly `t`, `kind="adjust"`, `device`, `u` (a list of three numbers).
- Query object: exactly `sensor`, `t` (a list of absolute times).
- Sensors are `device0`, `device1`, and `global` for the native roster.
- No wait, read, fork, reset, history, relative-lag, anchor, pose, coordinate, port-map, or seed action keys.
- Numeric values must be finite Python JSON numbers (`int` or `float`), not booleans, strings, arrays, or coerced values.
- IDs must be integers in the anonymous roster/port range, not floats. `n_samples` must be an integer at least one.
- The private `truth_seed` must be an integer in `[0, 2**64-1]`.
- All times are finite and nonnegative. They must lie on `dt=0.02` within absolute representation tolerance `1e-9` tu. Negative values are rejected even within that tolerance.
- Accepted float representations map to their integer tick. Unsupported off-dt times raise `ProtocolError`; there is no silent rounding to a sensor cadence.
- Off-5tu but on-dt queries and actions are supported.
- Actions must have strictly increasing start ticks. Queries/times may be unsorted or repeated; order and repeats are preserved in results.
- `u` components are in `[-1,1]`, `amp` in `[0,3]`, and `dur` in `(0,50]`. Duration must span at least one dt tick. These are the confirmed **prototype evaluation domain**, not the current exploration apparatus domain.
- Empty queries return `{"samples": []}`. Empty time lists return correctly shaped `(M,0,n_ports,n_slots)` arrays. The whole request is still validated; no physics runs when all output time lists are empty.

Constants are exposed in `blobround6.py`: `SIM_DT`, `TIME_ATOL`, `ADJUST_TU`,
`ADJUST_TICKS`, `AMP_RANGE`, `DURATION_MAX`, `CONTROL_RANGE`, `DEFAULT_SAMPLES`,
`MAX_SEED`, and `MAX_EXACT_TICK`. The parser also enforces integer representation
bounds (`MAX_EXACT_TICK=2**53-1`, including interval ends, and the native `intp`
array-dimension bound). **These are not resource budgets.**

There are no finalized action-count, query-count, horizon, member-count, output,
or CPU budgets. The library can allocate large outputs or run for a long time if
misused. It is only for trusted, explicitly bounded local requests. It is **not
safe for untrusted requests** until such limits and a real isolated runtime exist.

## Events and occupied intervals

At each tick: finish prior half-open intervals; start the action; sample passive
queries; then advance toward the next event.

Injection uses the existing fixed-emitter source on `[t,t+dur)`. There is no
instantaneous field jump at `t`; the source acts on subsequent active substeps.
Moving a device does not move this fixed emitter.

Adjust changes device pose immediately at `t` and occupies `[t,t+5)`.
A query at the start sees the new pose. A query at the end sees five elapsed tu.
An adjust never moves a requested sample to `t+5` or forces physics beyond the
last requested time. Inspection of the legacy command confirmed that it applies
pose before advancing 5tu and returns its optional read after completion.

The scheduler supports one injection lane and one globally occupied adjust lane.
Their intervals may overlap when their start times differ. Thus inject at 830
for 10.5tu and adjust at 835 is supported. Overlapping inject/inject, overlapping
adjust/adjust (even on different devices), and all simultaneous action starts
are rejected. Exact end/start adjacency is allowed. Queries may occur inside
occupied intervals or on any boundary. These conflict rules also apply to no-op
commands; a no-op is not an escape from the validated grammar or occupancy rule.

Out-of-range input controls are rejected, not clipped. Valid controls use the
existing private actuator map. Position wraps periodically. Dilation clips to
native bounds, matching `blobround5._walked_device_l1` and `ProbeDevice` math.
R5 transport `_walk_poses` instead rejects bound-striking commands and clips
out-of-range input controls. That distinction remains an explicit integration
gate; transport parity is not claimed.

## Noise policy A and passive queries

Base noise applies before the first **effective** state change. This includes
apparatus pose changes, not only injection. At that action, each truth member
switches once to a fresh private continuation RNG. Later actions never reseed.
The field value at injection start is still the pre-source value. A pose-start
query uses the changed pose, but no continuation RNG draw has occurred yet.

Zero-amplitude injection, a zero adjustment, and a valid adjustment that leaves
the actual clipped pose unchanged do not switch RNG. Removing or adding a legal
no-op does not change a branch stream. No actions gives repeated samples of the
base realization, independent of truth seed. A future action suffix cannot
change earlier queries. Increasing member count only extends the existing member
prefix. Queries consume no random numbers and change no fields or apparatus.

## Native physics and exact private checkpoints

Physics is reused, not reimplemented: `device.step_chunk`, native source stamping,
`ProbeDevice.sample`, and the existing actuator map. The native factory rebuilds
only the existing selected t=0 state. It does not load the heavy f16 frame cache
or regenerate any records or frozen truths.

The runner owns a full-precision t=0 template. It shares native read-only
parameters, but each live member has its own fields, RNG, and device copies.
Base replay before branching is shared across members. Members run sequentially,
so the runner does not retain an ensemble of native field states.

Private base checkpoints are captured only from this template's own exact base
replay. Each checkpoint keeps owner/provenance identity, absolute tick, original
field dtype, full fields, RNG state, and a field/RNG integrity digest. Restore
checks those values. The cache retains at most t=0 and one additional checkpoint.
A checkpoint is used only at or before the earliest required query or first
effective intervention, whichever comes first. Earlier actions/queries force an
earlier start. Checkpoints do not change request semantics.

There is no arbitrary external checkpoint importer, f16-record reconstruction,
public anchor input, or serialization-based restart API in this phase. Native
fields remain f32; toy fixtures use f64. Field records in f16 are never treated
as exact state. Private ownership/integrity checks are not a security boundary
against hostile code with evaluator-process access.

## R5 compatibility matrix

| Family | R5 semantics | Policy-A comparison and Phase 1 coverage |
| --- | --- | --- |
| L1 | Pose walk, degenerate undisturbed base fields | Pose-helper math parity passed. Nonzero R6 adjustment switches noise, so the old stochastic truth is not generally equal. Full old truth parity UNRUN. |
| L2 | Degenerate base at extra hidden device | That device is not in the R6 public query roster. No public one-to-one parity case. |
| L3F short (`H<=25`) | Degenerate base | Semantically matchable with identical full-precision state/base RNG and absolute query time. Initial native base/substep parity passed; actual old truth horizon parity UNRUN. |
| L3F long | Fresh streams at hidden anchor | R6 no-action repeats base. Not matched. |
| L3E | Fresh anchor continuations, crossing reduction | R6 no-action repeats base; raw queries do not perform this reduction. Not matched. |
| L3S | Fresh anchor continuations, time-averaged globals | R6 no-action repeats base; globals are instantaneous. Not matched. |
| L4/L4D | Fixed-emitter source after anchor, private member stream | Matchable if first R6 effective action is that injection and fields, tick, source, devices, and RNG agree. Identical R5 `_member_state` plus source-primitive/substep parity passed; full `_run_member` or old truth-instance parity UNRUN. |

R5 `AMP_CAP=1` exploration does not cover the prototype's full `[0,3]` domain.
Above-apparatus predictions must not be described as accessible experiments
until exploration is aligned or extrapolation is explicitly disclosed.

There is no all-six-truth parity claim. There is no scorer, universal
“perfect-model floor,” or Gaussian restriction on the submitted samples.
Conditional LOO Gaussian CRPS is not a universal floor.

## Validation completed

Command (repo root, project environment):

```text
.venv/bin/python environments/physim/tools/test_blob_round6.py --gates toy native --json-out probes/blobs/agentenv/round6/runner/validation.json
```

Authoritative result: `validation.json` reports **31/31 passed**, no failures,
errors, or skips. It contains per-test timing and exact environment details.
- 25 toy/validation/checkpoint/API tests.
- 6 native tests using existing `p4g2_044` / seed928 only.
- Native trajectory maximum: six dt substeps (`0.12` tu).
- Suite wall time: `0.5228532501` s. Whole command, including process/import overhead: `1.4957175422` s.
- Peak process RSS: `328,597,504` bytes (about 329 MB / 313.4 MiB).
- Native initialization: `0.0140672503` s; fields `(12,256,256)` f32, `3,145,728` bytes.
- NumPy `2.5.2`; `.venv/bin/python`; `OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, and `MKL_NUM_THREADS` all set to `1`.

Coverage includes deterministic known-state laws; query invariance; causal action
prefixes; member ordering and distinct streams; seed-namespace separation;
reset/repeat determinism; no-op neutrality; multiple actions; source half-open
boundaries; fixed emitter; pose timing, wrapping and clipping; strict
shape/key/type/range/order failures; and exact checkpoint dtype/provenance/RNG
integrity. The API boundary test rejects public `seed` at `sample_truth`, requires
an explicit truth seed, and checks that changing predictor sampling seed leaves
a fixed grader truth request/output unchanged. This is not a scorer or sandbox
test.

No full replay, ensemble battery, old truth regeneration, new world/seed, model,
eval, paid/remote work, production integration, or commit was performed.
`toy_validation.json` records the earlier toy-only revision; `validation.json`
is the final combined result. Tiny native timing does not establish long-horizon
performance or adequacy on evolved late-time physics.
