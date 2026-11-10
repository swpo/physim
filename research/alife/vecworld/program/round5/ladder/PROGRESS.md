# ladder study: progress (kept current; a container restart may kill the agent at any time)

- 2026-11-10 01:14 UTC. Third instance of this study (container restarts at 00:12, 00:53, 01:12).
- 01:40 UTC. CPU tests passed from a git archive of the request's paths: `run_ladder.py --smoke --cpu-ok`
  for the three hidden sets (exit 0; log in results/smoke_progress_cpu.txt), `check_lib.py`,
  `make_summary.py --smoke`; again for `--sets 8` at the pinned commit a92093604 (01:48).
- 01:50 UTC. GPU request **r5-ladder-001** committed and pushed (ref a92093604, max_hours 2.9, cap $21.2,
  types A100_40GB, A100_80GB, H100_80GB, H200_141GB). Sizes: 8 truths per hidden set, 36 items, R 12,
  N_theta {1: 256, 4: 448, 8: 512}, 512 mix + 32 class-e Lab episodes per truth, budgets 2-512.
  The queue held r5-vortexexam-003 (running), r5-slots-004 and r5-bias2-006 at that time.

## If you are a restarted instance
1. `cd /home/user/physim && git fetch -q origin gpu-jobs && git show origin/gpu-jobs:jobs/r5-ladder-001/status.json`
   (also read `jobs/r5-ladder-001/review.md`). Do NOT resubmit while it is received / queued / running.
2. Watcher (background): a loop that fetches gpu-jobs every 60 s and exits on a terminal state.
3. When done: copy `origin/gpu-jobs:jobs/r5-ladder-001/out` to `results/job/` (without presmoke/), save
   status.json to `results/status.json`, run `python -B make_summary.py`, write README.md and the report,
   commit and push, remove the worktree.
4. If it failed: read logs (`jobs/r5-ladder-001/logs/run.log`), fix, test on CPU from a git archive,
   resubmit as r5-ladder-002 with cap <= $25 minus what r5-ladder-001 billed.
