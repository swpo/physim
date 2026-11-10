# Round 5, study `slots` (track 1): an object-centric bias on raw Flow-Lenia gliders

STATUS (10 Nov 2026, 03:05 UTC): PRELIMINARY. Only the pilot (`r5-slots-003`) has run; the full job `r5-slots-004`
is waiting for GPU stock. `PROGRESS.md` says what is done and what is next. Numbers below are the pilot's.

Round 4 (`../../round4/bias`) found that no block-wise bias with at most 4 numbers per block yields the object view
of the gliders world. Here the encoder is object-centric: K = 12 slots with a few numbers each, a deterministic
causal function of the level-0 history (fixed start, memory carried from tick to tick). Question: do objects emerge
from an objective plus an object-centric architecture, or does the tracker's hand-written logic
(`../../../vw1/vw/objects.py`) carry something the objective does not supply?

## What is compared

One transducer for every encoder (`snets.py`): 4 x 4 px tokens, 12 slots with content, position and memory, two
attention iterations per tick. With its learned terms at zero it IS soft k-means with carried centres.

| name | what |
|---|---|
| `trk` | the tracker's object view (reference; 12 numbers per slot) |
| `km_s3`, `km_s6`, `km_s6w` | no learning: soft k-means on matter, bandwidth 3 or 6 px, `w` = mass-weighted mixing |
| `grid` | no learning: 12 fixed regions (Eulerian control) |
| `sam_<obj>` | learned masks, moment readout (each slot reports the moments of the matter under its mask) |
| `sac_<obj>`, `sgc_<obj>`, `sgm_<obj>` | code readout (6 learned numbers per slot) / plain slot attention without the k-means distance term |

Objectives: `set` (closure: the slots predict their own future at h = 1, 4, 16 with a permutation-equivariant head,
error in the metric of the joint covariance of the 72 slot numbers, which is the collapse guard; `_dg` adds a
dead-direction term), `self` (local law: one shared rule per slot, own past only), `rec` (reconstruction control),
`sup` (supervised imitation of the tracker's segmentation: a capacity control, not a candidate), `_ws` (warm start
from `sam_sup`, then the objective alone).

Judging (`scert.py`, `scombine.py`; a learned encoder is certified on the half it was not fitted on):
closure ceilings in the encoder's own coordinates with one fixed predictor family for slot sets (family S: shared
linear rule and a shared attention network over slots, on 6 numbers per slot; h = 1, 2, 4, 8, 16), predictable
content (nats, diagonal Gaussian measure), agreement with the tracker (slots matched to tracked objects per frame by
assignment on shared matter: recall, precision, matter-weighted ARI, slots per object, mass / position / velocity
R^2 of the matched slot, recall by ticks since the object's last fusion or fission), seed stability (two seeds per
half), and the value of each objective on each frozen view (heads trained from scratch).

## Files

`s5.py` (layout, grid), `ssim.py` (GPU simulation, tracker tables and label maps), `snets.py`, `strain.py`
(training, encoding, objective values), `scert.py` (CPU certification workers), `scombine.py` (pooling), `job.sh`,
`sfetch.sh`, `ssummary.py`, `sfigs.py`. Requests: `../../gpu/requests/r5-slots-*.json`.
`results/summary.json`: every number with its source (job id, file, key); `results/interpretation.json`: the claims
and their key paths; `results/review.json`: the Mac's code review of the pilot and the fixes;
`results/<job>/`: copies of the job outputs the summary cites.

## Pilot (r5-slots-003; H200, 48 trajectories per half, 600 steps; $3.13)

Only `sam_set` trained (the reference stage used most of the short training window).
- Closure-trained slots stay k-means parts: ARI against the tracker 0.64 (k-means 0.64-0.73), 2.1 slots per tracked
  object, precision 0.99, recall 0.78; matched-slot mass R^2 -0.21, position R^2 0.98, velocity R^2 0.50.
- Seed-stable (seed-pair ARI 0.94) and close to the baseline (ARI against `km_s6` 0.80).
- In their own coordinates the k-means parts are MORE closed than the tracker's objects (family S ceilings at
  h = 1 / 4 / 16: tracker 0.94 / 0.73 / 0.19, `km_s3` 0.98 / 0.88 / 0.56, `sam_set` 0.97 / 0.86 / 0.56), and the
  closure objective prefers them (0.33 against 0.58 for the tracker's view; lower is better).
- The pilot's `sam_set_dg` rows are initial weights (cut by the deadline), not a result.
