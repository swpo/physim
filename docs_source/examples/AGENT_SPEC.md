# Executable prediction contract — centered-pulse-v2

You investigate an unfamiliar dynamical system using repeatable experiments,
two instruments, each with a source at the center of its sensor array. Your deliverable is Python code implementing:

```python
def predict(actions, queries, n_samples=64, seed=0):
    return {"samples": [array_for_each_query]}
```

Use observations collected during exploration to build the predictor. You may
package learned data and model parameters with it. Prediction runs use that
artifact without access to the experimental service. The evaluator supplies new
action/query programs, calls your predictor, then compares its outputs with one
or more fresh physical realizations. The prediction programs are fixed in advance
within each call; adaptive actions based on future readings are outside this API.

## Experiments and time

Each experiment starts from the same prepared physical state and apparatus poses
at time0. Waiting is implicit in timestamps. Starting a new experiment restores
that physical starting point. Ongoing random disturbances differ between
experiments. Your task is to predict observable behavior, including meaningful
uncertainty; reproducing those disturbances is not required or possible through
the API. `seed` only controls your predictor's sampling.

The local experimental service accepts the same `actions` and `queries` grammar
as prediction, and returns one realization in the same `samples` structure. Both
exploration and evaluation allow the ranges below. All times are absolute time
units from the prepared start, nonnegative multiples of0.02 (representation
tolerance1e-9). This example uses a maximum time of50. Each action's entire
occupied interval must end by that maximum, even if all queries are earlier.

The trusted host exposes `experiment(actions, queries)` and `usage()`. The
development exploration budget is1000 experiments and50000 integrated time units.
Each admitted request consumes one experiment and its largest query timestamp
in time units. Empty requests consume a call but no simulated time. Invalid
requests consume neither; an admitted execution that fails retains its charge.
`usage()` reports calls and time consumed and their configured limits. A pilot
may set different budgets, which must be announced before exploration begins.

## Actions

Each instrument has a source at the center of its sensor array. You can use
readings around a source to learn its spatial response. An injection selects
an instrument and an anonymous port:

```json
{"t": 1.0, "kind": "inject", "device": 0, "port": 2, "amp": 0.7, "dur": 4.0}
```

`device` is 0 or 1; `port` is an integer0..11. Amplitude is in [0,3]
and duration in (0,50]. Launch is instantaneous: the pulse captures that
instrument's current center. Forcing continues at that captured position on
[t,t+dur), even if the instrument moves later. This is a finite-duration pulse,
not an instantaneous addition of all its material. Port identities are
consistent across both sources and all sensors. Zero amplitude is permitted.

An adjustment repositions one entire instrument immediately:

```json
{"t": 2.0, "kind": "adjust", "device": 0, "u": [0.2, -0.4, 0.1]}
```

Each of the three controls is a finite number in [-1,1]. Their mapping to
translation and array dilation is initially unknown. Dilation clips at the
apparatus bounds; a valid command at a bound is accepted. Movement changes
where the sensors read and where subsequent pulses start. Previously launched
pulses and the fields they produced remain in the world. Dilation changes
sensor spacing around the center, not the source width.

Each instrument has separate movement and injection lanes. An adjustment
occupies only that instrument's movement lane for 5 time units; a pulse
occupies only its injection lane for `dur`. Movement and injection may overlap,
and the two instruments operate independently. Intervals on the same lane must
not overlap; adjacent endpoints are allowed. Zero-effect actions still occupy
their lanes. Movement is instantaneous repositioning, not continuous travel.

List actions in nondecreasing start-time order. At equal times, list order
matters: inject then adjust starts a pulse at the old center; adjust then inject
starts it at the new center. At each event time, ending pulses are removed,
all starting actions execute in list order, then readings are taken. A newly
launched pulse affects fields during subsequent simulation steps, not at the
launch-time reading. Intervals after the last query are validated but need not
be simulated.

## Queries and output

```json
[
  {"sensor": "device0", "t": [0, 8, 12]},
  {"sensor": "device1", "t": [12, 20]},
  {"sensor": "global", "t": [20]}
]
```

Every query returns all12 ports. `device0` has13 slots, `device1` has19, and
`global` has2 (spatial mean, then spatial population variance). Device geometry,
spatial coordinates, field meanings and governing equations are not supplied.

For each query, return a numeric array with shape:

```text
(n_samples, number_of_requested_times, 12, number_of_sensor_slots)
```

Times within each query must be strictly increasing, with no duplicates.
The same timestamp may appear in queries for different sensors. Each query's
time list is independent; there is no ordering requirement between query objects.
Preserve the input query order and each query's chronological time order.
All values must be finite. No broadcasting, missing ports, extra keys, NaNs or
infinities are accepted. A member index denotes one coherent predicted
trajectory across every time, sensor and query in that call. Permuting whole
members does not affect grading. Independently shuffling values at different
times or devices changes the predicted joint behavior.

A deterministic predictor may repeat its estimate in every member. A stochastic
predictor may return an empirical distribution; it need not be Gaussian.
Repeated calls with the same inputs and predictor seed must reproduce output.
Predicted earlier behavior should not depend on adding later actions or queries.

The protocol supports empty query/time lists with correspondingly empty outputs;
graded examples always contain at least one observation. Exact object keys and
JSON number types are required; booleans are not numbers or integer IDs.

## Grading and operational limits

The evaluator compares your empirical predictive distribution with independently
simulated observations. It never pairs your member0 with physical member0.
Marginal CRPS measures predicted scalar distributions; joint energy scores measure
selected observable groups across times and sensor positions. Lower scores are
better. Group definitions and scales are fixed before grading. There is no
universal0–1 accuracy conversion or requirement to predict a microscopic noise
path. The private phenomenon names and physical explanations are not inputs.

The default request asks for64 predictive members; at most256 are accepted.
The local evaluator caps128 actions,32 queries,256 times per query,1024 total
query times,2,000,000 combined prediction/truth scalar outputs and100,000,000
pairwise score operations. A request must satisfy every cap. Each pilot declares
its model-response, experiment and submitted-artifact execution budgets before
exploration. Submitted code runs in an isolated runtime with its frozen artifact
and own observations; the physical service is unavailable during prediction.
