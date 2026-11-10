# PROGRESS (study foundry, round 5) -- kept for restarts

Updated 2026-11-10 05:13 UTC (instance 1; the study started at 03:40 UTC).

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

## Job 1 DONE
- r5-foundry-001: done, exit 0, H100 80GB (datacrunch), 05:10:56-05:21:36 UTC, billed $0.9246 (status.json:cost).
  8192 draws screened in 376 s (74,700 member-ticks/s). Outputs fetched to work/r5-foundry-001 (scratch, not in git);
  results/analysis.json, results/per_draw.json.gz, results/fig/ (posters, 6 GIFs, charts), results/jobs/r5-foundry-001/
  committed. Types: uniform 65.2%, frozen 19.7%, active 15.1% (movers 3.2%); candidates (all four gates) 88 = 1.07%.
  All 24 certified worlds pass every gate again. Gliders by the same estimator: mover, ceilings 0.99/0.96/0.83/0.47/0.20/0.02.

## Running
- GPU request r5-foundry-002 (cap $10.20, max 1.25 h, ref ee9648d4e): PUSHED 05:34 UTC. Arms: enrich (prospective
  test of the weights-only predictor: 3072 selected + 1024 control draws of prior seed 2027; predictions in sel_r2.json),
  late (2000 draws with a 2000-tick burn-in), cert (the 88 candidates at certification size), sigma010, sigma100.
  Watcher: `bash watch.sh r5-foundry-002`.

## Next step
1. CPU follow-ups on top candidates of job 1 (each a minute or two): `python -B wind_probe.py --draws 1672,4470,262,60`,
   `python -B longrun.py --draws 1672,4470,262,60`, `python -B recheck_cpu.py --draws 1672,4470,262,60`.
2. When job 2 is done: `bash fetch.sh r5-foundry-002`; `python -B analyze2.py work/r5-foundry-002/out`.
   If it failed: logs under work/r5-foundry-002/logs; fix, CPU test (FOUNDRY_SIZE=tiny bash job2.sh from a git archive),
   resubmit as r5-foundry-003 (caps in total <= $25; billed so far $0.92).
3. `python -B make_summary.py` (needs results/interpretation.json, to write by hand from the analyses), README.md
   (replace the DRAFT status with the results), report; remove the worktree and scratch.

Budget: $25 total; billed $0.92 (job 1); job 2 cap $10.20.
