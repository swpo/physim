# Review of r5-slots-008 (study `slots`, main job; resubmission of r5-slots-007)

Reviewed by the runner Mac. The code is the same as r5-slots-004/005/006/007 (ref 7099a0ded),
which was reviewed in full; see `jobs/r5-slots-004/review.md`.

What changed from 007:
- env: `XLA_PYTHON_CLIENT_ALLOCATOR=platform`
- `S5_STEPS` 2000 -> 3000
- cap $20.80

**Verdict: fine to run. The change addresses the failure of r5-slots-007, with the residual
risk noted below.**

## What r5-slots-007 showed

- On an A100 40GB the references and `sam_sup` ran: 9.4 s per 100 steps, peak 5.7 GB.
- The training chunks of the set and rec families also ran.
- Each of the 13 other configs then failed at its first validation (`jit_val`) with
  RESOURCE_EXHAUSTED for a single 16-19 GiB block. Only about 17% of the 36 GiB BFC pool
  was in use at the time: small arrays that outlive a call sat inside the pool's one large
  region, so it could not supply a second contiguous block, and it could not grow.
- The runner's earlier estimate for validation (about 4 GiB temp from a CPU compile) was
  wrong for the GPU, which asks for about 18 GiB. CPU `memory_analysis` is not a reliable
  proxy for this code's validation on GPU.

## Why the change should work

- **Platform allocator:** `XLA_PYTHON_CLIENT_ALLOCATOR=platform` sends every device
  allocation straight to CUDA and returns it when freed, so there is no pool to fragment.
- **Budget:** resident data (5.2 GiB) plus one call's temporaries (validation 17-19 GiB,
  training chunk about 22-25 GiB; they do not overlap) is about 27-30 GiB of the card's 40.
  With this allocator `XLA_PYTHON_CLIENT_MEM_FRACTION` no longer caps the process.
- **Cost:** the workload makes few, large allocations (100 training steps per call), so the
  per-allocation cost is negligible.

## Time and cost

At the measured 9.4 s per 100 steps, a config takes about 450 s at 3000 steps. All 14
configs and the references take about 1.9 h on an A100 40GB, inside the limits (training
stops at 10400 s, workers killed at 11900 s; kill at 12600 s). Expected spend is about $4
on an A100 40GB, about $9 on the H100. The cap covers an H100 up to about $5.5/h.

## Residual risk

The platform allocator still needs about 18-25 GiB of free device memory per call. The
failure mode does not depend on contiguity in the driver's virtual address space, but it is
not measured on this card. If it fails again, each config fails at its first validation
(about a minute each) and the job ends with the references and `sam_sup` again, for about
$1. 80 GB cards (A100 80GB, H100) remain the safer choice for this code.

## After the run (added by the runner Mac)

- **The allocator change worked.** The job ran on an A100 40GB (backend gpu). There was no
  RESOURCE_EXHAUSTED. 13 of 14 configs trained all 3000 steps, and certification finished
  with 116 halves certified and none unclaimed. `combined.json` was written in full.
- **The time estimate above was wrong.** It took `sam_sup`'s 9.4 s per 100-step chunk for
  every config. `sam_sup` did run at 9.44 s with this allocator, so the allocator cost
  nothing. But the set and self configs take about 20-21.6 s per chunk (660-740 s per
  config), and the rec configs about 12-14 s (410-490 s). Training took 9417 s, and
  `sam_set_sg` was skipped by the training deadline (`train_done.json`).
- **Exit 1 is a reporting bug in `scombine.py`, line 233.** It runs after `combined.json` is
  written, so only `table.txt` is missing. The objval table calls `np.mean` on lists that
  hold None: `objval/sac_set.json` has None for every set and self value, and
  `objval/sac_rec.json` has None for replicas A0 and A1. A None-safe mean there (or
  skipping None) fixes it.
- **For the analysis:** `sac_set` reached val_best 0.001-0.003 and `sgm_set` about 0.02,
  against 0.2-0.28 for the other set configs. The frozen-readout heads for `sac_set`
  (all four replicas) and `sac_rec` A0/A1 sit at a constant rec value of about 0.942,
  with val_h all zero. This looks like a collapsed representation, but the study should
  judge that, not the runner.
- **Cost:** $5.36 billed (lambdalabs A100 40GB at $1.99/h, about 2.7 h).
