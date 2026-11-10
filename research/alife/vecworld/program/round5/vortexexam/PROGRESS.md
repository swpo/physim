# vortexexam: progress file (for a restarted self)

PILOT: never to be reused as an exam. Budget $25: job 1 billed $2.29; job 2 holds a cap of $19.80.

## Done
- Library `vxlib.py` (batched fed-vortex runner with 4 hidden parameters, programs, level-1/2 summaries),
  `vxnet.py` (predictor families net / ridge / law / lin2), `vxsbi.py` (identification, from round4/sbi).
- CPU checks: `check_lib.py`, `check_predictors.py`, `check_replay.py` (results/check_*.json).
- GPU job 1 = `r5-vortexexam-002` (done, exit 0, $2.29, H200): throughput, law runs (5 eps x 64 members), scan
  main runs (27 settings x 12 members). Its `scan_branch.npz` (40.2 MB) stayed on the Mac.
  Analysis: `analyse1.py` -> `results/analysis1.json`; small job files in `results/job1/`.
- Prior for the exam pilot: `select_prior.py` -> `prior.json` (eps, mut128, nu, e; viability rule).
- GPU job 2 = `r5-vortexexam-003` requested at 84550bc04 (job2.py, then job1.py --scan-only).
  Review: `origin/gpu-jobs:jobs/r5-vortexexam-003/review.md` (gate met; 1 major: the scan-only run shrinks to
  J = 3, one anchor, because of the rate table; 5 info points).

## Running
- `r5-vortexexam-003`: received 00:53 UTC 10 Nov, reviewed 01:11. DO NOT RESUBMIT. Watcher: a background loop
  that fetches `origin gpu-jobs` every 60 s until `jobs/r5-vortexexam-003/status.json` is terminal.

## Next steps (in order)
1. After the review: sizer fix in `job1.py` (scan-only takes `--J`, `--anchors` or job 1's bench rows), pilot
   marker in every output of `job2.py`, `fetch_job.py` (copies the small job files into `results/jobN/` with
   the marker). Test with `--smoke` on CPU.
2. When job 2 is terminal: `python -B fetch_job.py r5-vortexexam-003 job2` (git show from origin/gpu-jobs into
   scratch `vx/job2`), check `prediction.json` has `final: true` and `info.json` has no `fatal` (job2 exits 0
   even if the report stage fails), then `python -B analyse1.py <scratch>/vx/job1 <scratch>/vx/job2/scan`,
   `python -B analyse2.py <scratch>/vx/job2`, `python -B make_summary.py`.
3. If the cap allows (25 - 2.29 - billed(job 2) >= 6.69 x (max_hours + 0.25)): request
   `r5-vortexexam-004` = `job1.py --scan-only --J 12 --anchors 200,320` (about 15 min), unless the Mac has
   pushed `jobs/r5-vortexexam-002/out/scan_branch_small.npz` (asked for again in the channel file).
4. README.md, results/summary.json, report; remove the worktree.

Scratch: `/tmp/claude-0/-home-user/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/vx` (job1/ = job 1 outputs).
Channel file: `/tmp/claude-0/-home-user/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/vortexexam_COORD.txt`.
