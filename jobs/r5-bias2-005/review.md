# Review of r5-bias2-004 / r5-bias2-005 (study `bias2`)

Reviewed by the runner Mac before the jobs started. The same review covers both jobs:
004 (membrane, then gliders; `B5_PLAN=membrane:900:3600:3900 gliders:600:1400:1650`,
`B5_JOB_HARD_S=6900`) and 005 (vortex; `B5_PLAN=vortex:3000:6250:6550`,
`B5_JOB_HARD_S=7260`).

Reviewed code:
- `round5/bias2` at bc207c293 (full review).
- The 6537dbe92 per-half refactor.
- The e24bc7b04 fixes (`job.sh` hard end and timeouts, `lat/DONE` after ctrain, GPU check,
  85% sim margin, `claim()` race). Between 005's ref (11c116b39) and 004's ref (a3096634c),
  only `csummary.py` and a results file changed.

Method: independent reviewers per dimension, each finding checked by a skeptical second
reviewer. Local CPU runs at `B5_TINY=1` passed for all three worlds, at 6f27a167d and at
11c116b39.

**Verdict: fine to run. Every point raised in earlier reviews is fixed.**

## Timing (checked against the real plans)

- **004:** membrane is unclipped and ends by about JOBSTART+4595 s. Gliders' cert deadline is
  clipped to JOBEND-700. Gliders ends by about JOBSTART+6880 s, before the 6900 s hard end.
- **005:** the cert deadline is clipped by 3 s to JOBSTART+6560. job.sh ends at most at
  JOBEND-12 = JOBSTART+7248 s.
- **Both:** job.sh starts about 40-60 s into the pod (setup), so the margin to the runner's
  kill is about 600 s, not the 660 s the request notes say.
- **Per stage:** csim ≤ SD+131 s, ctrain ≤ CD+11 s, workers ≤ CD+251 s,
  ccombine ≤ CD+681 s.

## Minor

1. **ctrain is killed at the cert deadline.** It checks TD only between configs
   (`ctrain.py:466-469`), and writes `train_done.json` only after the loop. A config
   still running at CD is SIGTERMed. The world is then marked `ctrain FAILED`, the job exits
   1 even though it ran as designed, and `train_done.json` (which `cfetch.sh` fetches) is
   missing. For 005 the TD-to-CD gap is 297 s; round 4's configs took up to 183 s on 2
   channels, and the vortex world has 4. Fix: write `train_done.json` from a SIGTERM
   handler, or treat exit 124 from this timeout as a deadline stop.
2. **The pre-loop probes have no timeout** (`job.sh:31/32/34/36`: versions and devices,
   nvidia-smi, df, the GPU check). A slow probe is absorbed by the clipping. But a real hang
   (CUDA init or nvidia-smi on a faulted GPU) runs to the runner's kill, which costs about
   $14.7 for 005 on the H200 and returns only `progress.txt`. Fix: wrap each probe in
   `timeout 120`.

## Info

- **Gliders' skip floor.** Gliders has `BURN=0`, so the 85% early abort never runs for
  it. A heavily clipped gliders window (about 1300-1390 s left before JOBEND) would start,
  then hit its sim deadline. This cannot happen with 004's plan.
- **The cert-worker allowance dropped from +600 s to +240 s.** Fine for these plans:
  q=256 items are hand designs and are claimed first, and learned configs have q ≤ 128.

## Checked and clean (from the earlier reviews)

- **Element counts:** all below 2^31. The largest is the per-half X, 1.26e9.
- **GPU peak:** about 25 GiB for membrane and vortex, about 16.5 GiB for gliders; csim
  stays under 3 GiB.
- **Round-4 lesson:** data are passed to jitted functions as arguments, and compiled
  functions are released between configs.
- **Safety:** no network access or processes after setup, no credentials read, no exam
  material, and every `np.load` has `allow_pickle=False`. `cfetch.sh` and `cpair.py` are
  local tools that job.sh never runs.
