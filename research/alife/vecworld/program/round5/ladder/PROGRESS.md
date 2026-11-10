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
- 02:05 UTC. r5-ladder-001 is `received` (the Mac's local smoke of it passed; its review was still running).
  README.md drafted (design only, no results). make_summary.py extended and tested on smoke outputs.
- 02:21 UTC. **r5-ladder-001 was REJECTED by the Mac's review before any pod ($0 billed)**: the block view's
  D(N) validation would have built 3.6e9-element arrays (review: origin/gpu-jobs:jobs/r5-ladder-001/review.md).
- 02:27 UTC. Fixes committed (ac871b3f1 locally): validation one net and one 128-row chunk at a time, at most
  8 nets in lockstep, `check_elems` guard, `check_shapes.py` (full-shape trace: largest array 1.13e8 elements =
  0.053 x 2^31; results/check_shapes.json), failure isolation per view / group / policy, pilot line in
  progress.txt, 128 class-e episodes, sizes back up (48 items, 96 climatology runs, N_theta {1: 384, 4: 768,
  8: 768}) because the burn-in is 50 ticks, not 132: about 3.6 million member-ticks in all.
- NEXT: the 3-set CPU smoke from a git archive of ac871b3f1 is running; when it passes, set `ref` in the
  untracked request `gpu/requests/r5-ladder-002.json` to the pushed commit that holds this code, commit and
  push it, start the watcher. In step 1-4 below read r5-ladder-002 for r5-ladder-001.
- 02:50 UTC. CPU tests passed after the fixes (3-set smoke at 33f6c69a4, 1-set smoke with two lockstep batches
  at 28263eb3e, check_lib, check_shapes, make_summary --smoke). **GPU request r5-ladder-002 committed and
  pushed** (ref 28263eb3e, max_hours 2.9, cap $21.2). In the restart steps below read r5-ladder-002.
- 03:23 UTC. r5-ladder-002: review "fine to run" (origin/gpu-jobs:jobs/r5-ladder-002/review.md; 1 minor:
  run.log lacks the pilot line); state `queued`, accepted for an H200 at $6.69/h (at most $21.07).
- 03:50 UTC. r5-ladder-002 is RUNNING since 03:44:31Z on an A100_40GB at $1.99/h (expected about 1.8-2.1 h,
  so until about 05:45Z; hard limit max_hours 2.9).
