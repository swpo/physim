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

- 02:01 UTC: job 2 (`r5-vortexexam-003`) done, exit 0, $1.31 billed, A100 40GB at 169 member-ticks/s, so it
  took preset `small` (6 truths, 192 design points, no dedicated models). Fetched (`results/job2`, scratch
  `vx/job2`) and analysed (`results/analysis2.json`). Reading: net P0 0.559 = C 0.557 of oracle skill (sigma
  -0.003 +- 0.03), prior-mean plug-in 0.35; the law fitted to 1-8 Lab episodes (T) 0.38-0.50 against the
  data-only net -0.38 to 0.21.
- 02:10 UTC: follow-up requested as `r5-vortexexam-004` (pilot B: `--prior prior_B.json` = eps, mu, e; new
  policies Cft / Sft@4 and the short-history families net~3 / ridge~3; sizing fixed). Cap $19.40, max 2.65 h.

## Running
- `r5-vortexexam-004`: requested 02:10 UTC 10 Nov. DO NOT RESUBMIT while it runs. Watcher: a background loop
  that fetches `origin gpu-jobs` every 60 s until `jobs/r5-vortexexam-004/status.json` is terminal. Read
  `jobs/r5-vortexexam-004/review.md` when it appears.
- Budget: $25 - 2.29 - 1.31 = $21.40 before job 004; its cap reserves $19.40.

## Next steps (in order)
1. While job 004 runs: README.md and the report from job 1 and job 2 (results/summary.json).
2. When job 004 is terminal (SP = the scratch folder below):
   `python -B fetch_job.py r5-vortexexam-004 job3 $SP`; check `results/job3/info.json` (no `fatal`, `failed`)
   and `prediction.json` (`final: true`); then `VX_TAG=B python -B analyse2.py $SP/job3` (-> results/analysis2_B.json)
   and `python -B make_summary.py` (reads results/job3 and analysis2_B.json; sections end in `_B`). Commit.
   If it failed: read `jobs/r5-vortexexam-004/logs`, fix, test on CPU from a git archive, resubmit as
   `r5-vortexexam-005` within the cap that is left.
3. README.md, results/summary.json, report (under 1,200 words); delete scratch `vx`; remove the worktree.

Scratch: `/tmp/claude-0/-home-user/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/vx` (job1/, job2/ = job outputs;
commit.sh = the commit helper: pull --rebase --autostash, add only this folder and the request files, push).
Channel file: `/tmp/claude-0/-home-user/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/vortexexam_COORD.txt`.
