# Review of r5-slots-003 (study `slots`, pilot)

Reviewed by the runner Mac before the job started. Code: `round5/slots` at f97113d73
(full review), plus the e5d146ef3 delta (dead-direction term, explicit config order).
Method: four independent reviewers (safety, resources, correctness, the delta), each
finding checked by a second, skeptical reviewer. A CPU run of `job.sh` at
`S5_SIZE=tiny` with this request's `S5_KEEP` passed: 68 halves certified, FAIL=0.

**Verdict: fine to run as a pilot. The FULL job must not run until the blocker is fixed.**

## Blocker for the full job (not for this pilot)

1. **Validation tensor past 2^31 elements at full size.** `strain.py:464-476` encodes all
   `N_VAL` validation trajectories x 301 ticks x 4 replicas in one call (`val_v`), and the
   3x3 token concat (`snets.py:187`) makes it `f32[4,8,301,32,32,288]` =
   2,840,592,384 elements at full size (`N_VAL=8`). It runs at the first validation of
   every learned config. At pilot size it is 1.42e9 elements, so a clean pilot shows
   nothing about it. It is also the full job's memory peak: about 37 GiB vs about 28 GiB
   at pilot. Fix: `lax.map` / loop `val` over replicas or trajectories, or use
   `lax.conv_general_dilated` for the 3x3 layer so the 9xC map never exists.

## Minor (pilot)

2. An encoder stopped by the train deadline before step `STEPS//4`, or with NaN validation
   throughout, is still certified under its learned name with its initial weights
   (`strain.py:548/559`). The only trace is `val_best = null` and `best_step = 0` in
   `train/<name>.json`. Check those before reading a config's row in `table.txt`.
3. `job.sh` cert-worker timeout = cert deadline + 900 s, which falls after the runner's kill
   (`max_hours`). An item claimed just before the deadline can then cost `scombine` and
   so `combined.json` / `table.txt`. Per-item files in OUT survive. Keep
   `S5_CERT_S + 900` below `max_hours x 3600 - ~200 s`. On this pod (H200, 16 vCPU,
   13 workers) items take about 190-700 s each.
4. `strain.py` loads data at import time, outside the `try/finally` that writes `lat/DONE`,
   and `job.sh` never touches `DONE`: if strain dies at import, workers idle until the
   cert deadline. (bias2 fixed the same pattern in job.sh by touching DONE after the
   trainer exits.)
5. `scert.py` `claim()` sort key calls `exists()` then `getmtime()`; a concurrent rename can
   raise and kill a worker. (bias2's fix: wrap `getmtime` in `try/except OSError`.)
6. No check that JAX sees a GPU; `ssim` silently switches to the CPU MapWorld. This pod
   reported `CudaDevice(id=0)`.

## Minor (full job)

7. `stopcarry` is a no-op in training (`snets.py:289`: the stop-gradient is applied only in
   `tick()`, which is used for the first frame of a window, whose state is already
   stop-gradient'ed). The measured gradient difference is exactly 0, so `sam_set_sg`
   duplicates `sam_set`.
8. The pilot covers only part of the full job's cost: `N_VAL` 4 -> 8, J 48 -> 96 (encode
   and cert time about 2x), and `nomem` / `self` configs are not piloted
   (`sam_rec_nomem`'s training chunk compiles about 17% larger).

## Checked and clean

Network or processes after setup: none in the import closure. Credentials: none read.
Writes stay in OUT, S5_WORK and existing `results/`. No exam material in the bundle or in
OUT. Every `np.load` has `allow_pickle=False`. Pilot element counts are below 2^31 (largest
1.42e9). Data are passed to jitted functions as arguments, and compiled functions are
released between configs. All `S5_KEEP` names exist, and `S5_KEEP_ORDER=1` now asserts that.
