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

- 02:37 UTC: `offline_views.py` (CPU) recomputed pilot A on three views of the items (results/offline_views_A.json):
  the pod's scores reproduce; with the last three ticks only, net sigma 0.18 (P0 0.47, C 0.57), rho about 1.
- `make_summary.py` writes a computed `headline` section (the report's numbers with sources).

- 02:58 UTC: `r5-vortexexam-005` ended in infra_error at provisioning (no job time; conservative cost $0.35):
  cap $19.40 was 0.1 cent under 6.69 x 2.90 = 19.401. Lesson: round caps UP with a margin.

- 05:01 UTC: job 3 (`r5-vortexexam-006`) done, exit 0, $3.72 billed, A100 40GB, preset `full` (10 truths, 512
  design points). Fetched (`results/job3`), analysed (`VX_TAG=B analyse2.py` -> results/analysis2_B.json;
  `offline_views.py --families ridge --tag B`), summary rebuilt (sections ending in `_B`, `headline`).
- README.md rewritten with all three jobs. Total billed $7.32 of $25 (at most $0.35 more for the pod of 005).

## Running
Nothing. The study is FINISHED (10 Nov 2026, about 05:20 UTC). No GPU job is pending and none should be sent.

## If you are a restarted self
Check that `git log origin/claude/fisim-agent-world-research-hepmlz -- research/alife/vecworld/program/round5/vortexexam`
shows the commit "round5/vortexexam: final". If it does, only the report to the coordinator is left (README.md
has its content). Then remove the worktree and the scratch folder `vx`.
