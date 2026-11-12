# dialsA3 progress (the zero-point rerun of the reopened gliders exam)

Worktree /home/user/wt/dialsA3 (branch wt-dialsA3, pushed to claude/fisim-agent-world-research-hepmlz). Job ids
r6-dialsa3-NNN (lower case). Scratch /tmp/claude-0/-home-user/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/dialsA3/.
Coordinator channel: /tmp/claude-0/-home-user/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/dialsA3_COORD.txt

## Done
- 12 Nov 03:01 UTC: DECLARED.md (dialsA2's in full with changes A3-1 to A3-11) committed (3e9026c7b) before any code
  or request.
- 03:07-03:35: code run_a3.py, a3_stats.py, make_summary.py, job.sh (f3c192b0e WIP, 37035b5c8 tested). CPU smoke at
  tiny shapes in the worktree: presmoke, stop rule, guard, full pass, exit 0; make_summary runs on its output.
- 03:38: archive test of 37035b5c8 (exactly the request paths), stop path forced by a test flag: exit 0 before the full
  pass, make_summary's stop branch OK.

- 03:56: archive test of 37035b5c8, full path (rule ignored by the test flag): presmoke, guard, full pass, exit 0;
  make_summary OK.
- ~03:58: request r6-dialsa3-001 committed and pushed (ref 37035b5c8, A100 40GB, max_hours 4.5, cap $9.60, script
  limit 4.2 h).

- 04:18: the runner's review: 0 blocker, 0 major, 0 minor, fine to run (results/job/review.md); notes recorded in
  DEVIATIONS entry 1 (no code change while it runs).

- 04:24 job started on the pod (lambdalabs A100 40GB); 04:32 script start; truths 43/48 viable.
- 04:46 presmoke done (13.9 min): stop rule r = -0.2115 +- 0.0236 at 6,000 steps (+0.063 at 500), threshold
  0.067 -> go (the true-form C at eta 0 BETTER than the public-form C in the presmoke); guard: required 78.5 min,
  everything 198.5, left 238 -> go. Full pass from 04:46, expected end about 08:05 UTC.

- Full pass: families done 05:05 (true-form 1,536 x 8 in 802 s), worlds 05:28; base nets 24,000, 48,000 and 96,000
  unmet by the rule; 192,000 rung from 06:09 (as dialsA2).

## Running
- r6-dialsa3-001 full pass (background watch loop: scratch watch.sh -> watch.log); expected end about 08:05 UTC.

## Next step
- Wait on origin/gpu-jobs:jobs/r6-dialsa3-001/status.json (one background loop, 60 s); read review.md BEFORE results and
  act on it (DEVIATIONS entry, no code change while running). Then copy outputs to results/job (not nets.npz),
  run make_summary.py, write README.md, DEVIATIONS, final report.
