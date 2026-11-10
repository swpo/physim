# Review of r5-slots-005 (study `slots`, main job at pilot data size)

Reviewed by the runner Mac. The code is the same as r5-slots-004 (ref 7099a0ded), which was
reviewed in full: the 2^31 fix was checked at compile level, and all pilot points were
addressed. See `jobs/r5-slots-004/review.md`. Only the env, the limits and the GPU types differ:
- `S5_SIZE=pilot` (48 trajectories per half), `S5_STEPS=2000`
- `S5_TRAIN_S=10400`, `S5_CERT_S=11200`, `S5_HARD_S=11900`, `max_hours` 3.5
- `S5_CFG_MIN_S=1000`, `S5_CFG_MAX_S=1500`
- GPU types A100_40GB, A100_80GB, H100_80GB

**Verdict: fine to run, but the memory margin on an A100 40GB is thin. The runner recommends
adding `XLA_PYTHON_CLIENT_MEM_FRACTION=0.9` (see below).**

## Time (checked)

Workers are killed at 11900 s from the start of `job.sh`, and `scombine` takes seconds.
`job.sh` starts about 60 s into the pod, so it ends by about 11960 s, about 600 s before
the runner's kill at 12600 s. Configs start only with at least 1000 s left before 10400 s.
A started config is bounded by `S5_CFG_MAX_S` = 1500 s, and the training loop stops at the
train deadline.

## Memory on an A100 40GB (the likely card)

- **XLA's limit:** with `XLA_PYTHON_CLIENT_PREALLOCATE=false`, XLA still caps the
  process at its default memory fraction, 0.75. On a 40 GiB A100 that is about 30 GiB.
- **Estimated peak:**
  - Resident device data at this size: about 5.2 GiB (measured on the GPU in r5-slots-003).
  - Training-step temp for the set and rec families at this code: 24.4-24.7 GiB on CPU.
    The calibration from r5-slots-004's review (CPU temp ran about 10% above the GPU on
    the pilot) suggests about 22 GiB on the GPU.
  - So about 27-28 GiB at the peak, leaving 2-3 GiB below the cap before allocator
    fragmentation.
- **The concern:** the nine-matmul token layer is new since the pilot, so its GPU memory
  is not measured. An out-of-memory error is caught per config (the config goes to
  `train_errors.txt` and the next one runs), but `sam_set`, `sam_rec` and `sam_self` are
  among the configs the study needs.
- **Recommendation:** add `XLA_PYTHON_CLIENT_MEM_FRACTION=0.9` (about 36 GiB usable on a
  40 GiB card; nothing else uses the GPU on the pod), or drop A100_40GB from the types. On
  80 GB cards the margin is large.
