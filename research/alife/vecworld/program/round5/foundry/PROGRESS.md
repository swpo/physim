# PROGRESS (study foundry, round 5) -- kept for restarts

Updated 2026-11-10 04:35 UTC (instance 1; the study started at 03:40 UTC).

## Done
- Worktree /home/user/wt/foundry (branch wt-foundry, sparse research/alife/vecworld).
- Family code `tnca.py` (affinity transport NCA, vw.Level, wind channel, prior, weight statistics),
  `screen.py` (cheap certificates, generic in the world), `criteria.py` (types, gates, score),
  `check_tnca.py` (CPU checks, all pass on CPU; results/checks.json to be written by a final run),
  `job.py` + `job.sh` (the GPU job), `analyze.py` (job outputs -> results/analysis.json),
  `fetch.sh` (unpack a job from origin/gpu-jobs into work/<job_id>), `watch.sh` (poll a job).
- CPU pilots on prior seed 1 (scratch only, 24 draws x 4 members x 170 ticks): 14 uniform, 5 frozen,
  5 active (1 mover). First law (raw cell as a feature) had a checkerboard instability in 7 of 16 draws;
  second law (s1 as a feature) gave 2 px spots; current law: features s2, s3, s4, crowding on s1.
- Thresholds in criteria.py fixed from that pilot before any GPU run (GPU screen uses prior seed 2026).
- job.sh passed end to end on CPU at tiny size from a git archive of the request paths (twice, exit 0).

## Running
- GPU request r5-foundry-001 (cap $13.50, max 1.75 h, ref 22134cfd9 = the rebased copy of the tested
  fa6858c86): PUSHED 04:31 UTC (commit 91273504f). The queue held 2 running jobs and 1 received before it.
  results/checks.json written (CPU checks all ok).

## Next step
1. (done) final tiny CPU test passed (exit 0, 433 s); request pushed.
2. Watch: `bash watch.sh r5-foundry-001` in the background (exits at a final state). Read
   origin/gpu-jobs:jobs/r5-foundry-001/review.md when it appears.
3. When done: `bash fetch.sh r5-foundry-001`; `python -B analyze.py work/r5-foundry-001/out`;
   then `python -B figs.py work/r5-foundry-001/out` (posters, GIFs, charts), results/summary.json
   (make_summary.py, to write), README.md,
   report. If the job failed: read logs under work/r5-foundry-001/logs, fix, CPU test, resubmit as
   r5-foundry-002 (caps in total <= $25).

Budget: $25 total; nothing spent yet.
