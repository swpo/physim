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
