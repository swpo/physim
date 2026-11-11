# dialsA2 progress (the gliders stress-conversion exam, reopened with a triggered bar)

Worktree /home/user/wt/dialsA2 (branch wt-dialsA2, pushed to claude/fisim-agent-world-research-hepmlz). Job ids
r6-dialsa2-NNN (lower case, per the coordinator). Scratch /tmp/claude-0/-home-user/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/dialsA2/.

## Done
- 19:26 UTC: DECLARED.md committed (3fd4076c5) before any code or request; DEVIATIONS.md entries 1 (whole exam quoted
  from A) and 2 (the header's clock time is wrong; the commit time is the record).
- 19:33-20:02: code: a2_lib.py (scan trainers, rate-per-net fine-tunes, designed arms, H/H_mix), a2_stats.py (criteria),
  run_a2.py (job), job.sh, make_summary.py. CPU smoke in place: presmoke, guard, full pass, exit 0 (20:02);
  make_summary runs on its output. Committed 04ddec834 (the ref to pin).
- 20:03: archive test started: job.sh at tiny shapes from a git archive of exactly the request paths at 04ddec834
  (scratch arch/, log arch.log).

- 20:26: archive test of e0df0c079 (per-group widening of the fine-tune grid): job.sh at tiny shapes from a git
  archive of exactly the request paths, presmoke, guard, full pass, exit 0; make_summary runs on its output.
- 20:28: request r6-dialsa2-001 committed and pushed (ref e0df0c079, A100 40GB, max_hours 3.9, cap $8.40,
  script limit 3.6 h).

- 20:35: r6-dialsa2-001 started on an A100 40GB (lambdalabs). 20:47: the runner's review: 0 blocker, 0 major, 3
  minor, fine to run; recorded in DEVIATIONS entry 3 (no code change while it runs).
- Heartbeats: presmoke and guard passed (required 101 min, everything 260, left 208); families done 21:02; worlds
  21:18; base nets 24,000 and 48,000 unconverged by the rule (48,000: best steps 29,000-39,500, one past 80%);
  96,000 unmet; 192,000 rung training from 22:00.

## Running
- r6-dialsa2-001 (GPU job). Waiting with scratch/wait_job.sh r6-dialsa2-001 (log wait_r6-dialsa2-001.log).
  Expected end about 23:45 UTC; N = 32 will probably be cut by the guard's oversized D estimate (review minor 1).

## Next step
- Read origin/gpu-jobs:jobs/r6-dialsa2-001/review.md as soon as it appears and act on it (cancel = push
  requests/r6-dialsa2-001.cancel and verify with git ls-tree).
- After the job: copy outputs (not nets.npz) to results/job/, run make_summary.py --job-id r6-dialsa2-001, write
  README.md and the final report.
