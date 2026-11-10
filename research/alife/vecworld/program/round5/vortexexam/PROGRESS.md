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

- After the review of job 2 (10 Nov, 01:15-01:30 UTC): `job1.py` sizer fixed (`--J`, `--anchors`, `--bench-json`),
  `job2.py` writes the pilot marker everywhere and exits non-zero on a failed final report (the RUN used
  84550bc04), `fetch_job.py`, `analyse2.py`, `analyse1.py` (scan of a rerun -> "scan2"; integrated-law check),
  `make_summary.py` (reads analysis2.json). All tested on CPU: smoke outputs for job 2's chain, a git archive
  for the scan-only job. Draft request for the scan-only job: `request_r5-vortexexam-004.draft.json`.

- 01:26 UTC: the Mac pushed `jobs/r5-vortexexam-002/out/scan_branch_small.npz` (job 1's branches, 12 members
  x 2 anchors). `analyse1.py $SP/job1` now gives the level-2 and level-1 headroom table (results/analysis1.json
  `scan.table`). So NO scan-only job. Finding: mut128 has no headroom, nu little; the declared rule on the real
  headroom picks (eps, mu, e) -> `prior_B.json` (`select_prior.py $SP/job1 --n-min 8 --out prior_B.json`;
  prior.json is the record of job 2 and must not be overwritten).

## Running
- `r5-vortexexam-003`: RUNNING since 01:21 UTC 10 Nov on an A100 40GB (lambdalabs, $1.99/h); run deadline
  04:03 UTC. DO NOT RESUBMIT. Watcher: a background loop that fetches `origin gpu-jobs` every 60 s until
  `jobs/r5-vortexexam-003/status.json` is terminal. Its cap ($19.80) is reserved until it ends.

## Next steps (in order)
1. When job 2 is terminal (SP = the scratch folder below):
   `python -B fetch_job.py r5-vortexexam-003 job2 $SP`; check `results/job2/info.json` (no `fatal`, `failed`)
   and `prediction.json` (`final: true`); then
   `python -B analyse1.py $SP/job1 $SP/job2/scan` ; `python -B analyse2.py $SP/job2` ; `python -B make_summary.py`.
   Commit.
2. Follow-up exam job `r5-vortexexam-004` (pilot B), only if job 2's outputs are sane and the cap covers it
   (25 - 2.29 - billed(job 2) >= 6.69 x (max_hours + 0.25), or list only A100 types):
   run = `python -B job2.py --prior prior_B.json --out $OUT --max-hours <max_hours - 0.2>`; paths as job 003;
   CPU test from a git archive first (`job2.py --smoke --prior prior_B.json --smoke-names eps,mu,e`, passed in the
   worktree at 01:30). Its analysis: `fetch_job.py r5-vortexexam-004 job3 $SP`, then
   `VX_TAG=B python -B analyse2.py $SP/job3` (-> results/analysis2_B.json); make_summary.py reads results/job3 and it.
3. README.md, results/summary.json (make_summary.py), report; delete scratch `vx`; remove the worktree.

Scratch: `/tmp/claude-0/-home-user/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/vx` (job1/ = job 1 outputs;
commit.sh = the commit helper: pull --rebase --autostash, add only this folder and the request files, push).
Channel file: `/tmp/claude-0/-home-user/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/vortexexam_COORD.txt`.
