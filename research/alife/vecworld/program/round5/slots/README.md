# Round 5, study `slots` (track 1): an object-centric bias on raw Flow-Lenia gliders

Round 4 (`../../round4/bias`) found that no block-wise bias with at most 4 numbers per block yields the object view
of the gliders world. Here the encoder is object-centric: K = 12 slots with a few numbers each, a deterministic
causal function of the level-0 history (fixed start, memory carried from tick to tick). Question: do objects emerge
from an objective plus an object-centric architecture, or does the tracker's hand-written logic
(`../../../vw1/vw/objects.py`) carry something the objective does not supply?

**Answer (10 Nov 2026).** They do not emerge. The architecture can express a tracker-like view (supervised: ARI 0.85
against the tracker), but closure, local law and reconstruction all end at soft k-means *parts* (ARI 0.63, 2.1 slots
per tracked object, all 12 slots in use), and when started from the tracker-like encoder they walk back to the parts
within about 600 steps. Closure itself ranks the parts above the tracker's objects (ceiling at h = 16: 0.56 against
0.17). What the tracker adds is individuation (how many objects, one per connected blob) and the bookkeeping of
fusions and fissions; the objectives count exactly those jumps as unpredictable.

Every number: `results/summary.json` (claims with values and sources; one row per view and per config).
Main job: `r5-slots-008` (A100 40GB, 48 trajectories per half, designer seeds 9801 / 9802, float64 simulation,
float32 encoders, 3000 steps, 4 replicas per config = 2 halves x 2 seeds; 13 configs). Public gliders parameters,
no hidden parameters; these data are not an exam and must not be reused as one.

## What is compared

One transducer for every encoder (`snets.py`): 4 x 4 px tokens, 12 slots with content, position and memory, two
attention iterations per tick. With its learned terms at zero it IS soft k-means with carried centres.
`trk` the tracker's view; `km_*` soft k-means (no learning); `grid` 12 fixed regions; `sam_<obj>` learned masks with
a moment readout (each slot reports the moments of the matter under its mask); `sac_` / `sgc_` a learned 6-number
code; `sg` plain slot attention without the k-means distance term. Objectives: `set` closure (slots predict their own
future at h = 1, 4, 16 with a permutation-equivariant head; error in the metric of the joint covariance of the 72 slot
numbers, the collapse guard; `_dg` adds a dead-direction term), `self` local law (one shared rule per slot), `rec`
reconstruction, `sup` supervised imitation of the tracker (capacity control), `_ws` warm start from `sam_sup`.
Judging (`scert.py`, `scombine.py`; a learned encoder is certified on the half it was not fitted on): closure
ceilings in the view's own coordinates with one predictor family for slot sets (S, on 6 numbers per slot),
predictable nats, agreement with the tracker (slots matched to tracked objects per frame by assignment on shared
matter), seed pairs, and the value of each objective on each frozen view.

## Results (r5-slots-008; `python -B stable.py results` prints this table)

| view | objective | ARI | slots per object | slots present | mass R2 (mask / probe) | ceiling S h=1/4/16 | seed ARI | closure value |
|---|---|---|---|---|---|---|---|---|
| trk | (tracker) | 1 | 1 | 7.4 objects | 1 | 0.92 / 0.70 / 0.17 | - | 0.45 |
| sam_sup | supervised | 0.85 | 1.24 | 8.0 | 0.66 / 0.79 | 0.95 / 0.82 / 0.41 | 0.86 | 0.42 |
| km_s3 | none | 0.63 | 2.14 | 11.9 | -0.19 / 0.50 | 0.97 / 0.87 / 0.56 | - | 0.32 |
| grid | none | 0.65 | 1.66 | 9.3 | 0.41 / 0.60 | 0.95 / 0.63 / 0.06 | - | 0.68 |
| sam_set | closure | 0.63 | 2.14 | 12.0 | -0.20 / 0.51 | 0.97 / 0.87 / 0.56 | 0.91 | 0.29 |
| sam_set_dg | closure + dead term | 0.63 | 2.14 | 12.0 | -0.19 / 0.51 | 0.97 / 0.86 / 0.55 | 0.94 | 0.30 |
| sam_self | local law | 0.63 | 2.15 | 12.0 | -0.20 / 0.51 | 0.97 / 0.87 / 0.56 | 0.94 | 0.30 |
| sam_rec | reconstruction | 0.63 | 2.15 | 12.0 | -0.21 / 0.54 | 0.98 / 0.87 / 0.55 | 0.94 | 0.31 |
| sam_set_ws | closure, warm start | 0.63 | 2.14 | 12.0 | -0.19 / 0.50 | 0.98 / 0.88 / 0.57 | 0.92 | 0.29 |
| sam_self_ws, sam_rec_ws, sam_set_ws_dg | warm start | 0.63 | 2.13-2.15 | 11.9-12.0 | -0.2 / 0.5 | 0.97-0.98 / 0.87-0.89 / 0.57-0.58 | 0.90-0.93 | 0.28-0.31 |
| sgm_set | closure, plain attention | 0.00 | 12.0 | 12.0 | -0.42 / 0.00 | 1.00 / 0.94 / 0.43 | 0.84 | 0.02 (collapsed) |
| sgc_rec | classic slot autoencoder | 0.28 | 6.5 | 11.8 | -0.20 / 0.05 | 0.95 / 0.72 / 0.28 | 0.16 | 0.44 |
| sac_set | closure, learned code | 0.64 | 2.16 | 12.0 | -0.22 / 0.00 | 0.97 / 0.94 / 0.90 | 0.90 | not finite (frozen code) |
| sac_rec | reconstruction, learned code | 0.64 | 2.15 | 12.0 | -0.21 / 0.06 | 0.99 / 0.93 / 0.53 | 0.89 | 0.34 (2 of 4 finite) |

Warm start, tracker recall + purity on held-out trajectories (2 = the tracker's segmentation): 1.87 at step 0
(encoder frozen until step 375), 1.71 at step 500, 1.65 from step 1000 on; cold starts sit at 1.65, `sam_sup` at 1.82.
Predictable nats per frame in the same 72 numbers (diagonal measure, h = 1 / 4 / 16): k-means 200 / 102 / 29, tracker
111 / 43 / 5; log-det at h = 1: 192 against 81. The diagonal measure over-counts redundant slots (the collapsed
`sgm_set` scores highest), the log-det does not (`sgm_set` negative).
Events: 67-69 fusions and 131-138 fissions per 300-tick trajectory. After a fusion the parts' best slot holds 0.42 of
the fused object (0.72 after 16 ticks); the supervised encoder recovers to 0.93 within 8-15 ticks.
Figures: `results/figs/` (segmentations, agreement, ceilings, objective values).

## What failed, and limits

- The full size (96 trajectories per half) was dropped: no 80 GB card could be rented for hours (`r5-slots-004`,
  cancelled at $0), so the main job ran at 48 per half on a 40 GB card. Ceiling SEs at this size are 0.01-0.02.
- `r5-slots-007` (A100 40GB, $1.04) lost 13 of 14 configs to GPU memory: the 36 GiB BFC pool could not supply a second
  17-19 GiB block at 17% use. Fixed in `r5-slots-008` with `XLA_PYTHON_CLIENT_ALLOCATOR=platform` (no slowdown).
- `r5-slots-008` exits 1 although every stage ran: the table printer met null objective values (the collapsed
  code readouts). `combined.json` was complete; `table.txt` was rendered locally (`scombine.py --table`, fixed).
- `sam_set_sg` (no gradient through the memory) did not run (training deadline). The set family ran at 21.6 s per
  100 steps on the A100 against 9.6 s on the H200.
- The pilot's `sam_set_dg` rows (`r5-slots-003`) are initial weights, not a result.
- One level-0 theory, one architecture, K = 12 fixed, 3000 steps; a different guard or a parsimony term was not tried.
- Billed: $9.52 of the $25 cap (`results/summary.json: totals, jobs`).

## Files

`s5.py` (layout, grid), `ssim.py` (GPU simulation, tracker tables and label maps), `snets.py`, `strain.py`,
`scert.py` (CPU certification workers), `scombine.py`, `job.sh`, `sfetch.sh`, `ssummary.py`, `stable.py`, `sfigs.py`.
Requests: `../../gpu/requests/r5-slots-*.json`. `results/interpretation.json`: the claims and their key paths;
`results/review.json`: the Mac's review of the pilot and the fixes; `results/<job>/`: copies of what the summary cites.
`PROGRESS.md`: the log kept for restarts.
