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

## Running
- r6-dialsa2-001 (GPU job). Waiting with scratch/wait_job.sh r6-dialsa2-001 (log wait_r6-dialsa2-001.log).

## Next step
- Read origin/gpu-jobs:jobs/r6-dialsa2-001/review.md as soon as it appears and act on it (cancel = push
  requests/r6-dialsa2-001.cancel and verify with git ls-tree).
- After the job: copy outputs (not nets.npz) to results/job/, run make_summary.py --job-id r6-dialsa2-001, write
  README.md and the final report.
