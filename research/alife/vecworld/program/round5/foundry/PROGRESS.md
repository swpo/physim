# PROGRESS (study foundry, round 5) -- kept for restarts

Updated 2026-11-10 04:06 UTC (instance 1; the study started at 03:40 UTC).

## Done
- Worktree /home/user/wt/foundry (branch wt-foundry, sparse research/alife/vecworld).
- Family code `tnca.py` (affinity transport NCA, vw.Level, wind channel, prior, weight statistics),
  `screen.py` (cheap certificates, generic in the world), `criteria.py` (types, gates, score),
  `check_tnca.py` (CPU checks), `job.py` + `job.sh` (the GPU job).
- CPU pilots on prior seed 1 (scratch only): the first law (raw cell as a feature) had a checkerboard
  instability in 7 of 16 draws -> features are now the smoothed scales s2, s3, s4 and crowding uses s1.

## Running
- nothing on the GPU yet.

## Next step
1. Finish the CPU pilot (24 draws, prior seed 1) with the current law; fix thresholds in criteria.py.
2. `python -B check_tnca.py` -> results/checks.json.
3. CPU test of job.sh at tiny size from a git archive of the request's paths (FOUNDRY_SIZE=tiny).
4. Commit, write gpu/requests/r5-foundry-001.json (cap about $10.2 for 1.25 h at the H200's 6.69/h), push,
   start a watcher on origin/gpu-jobs:jobs/r5-foundry-001/status.json.
5. After the job: fetch outputs, `analyze.py` (to write) -> results/summary.json, posters, README, report.

Budget: $25 total; nothing spent.
