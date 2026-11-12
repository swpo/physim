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

## Running
- nothing.

## Next step
- Archive test of 37035b5c8, full path (--ignore-stop-rule), log in scratch arch_full.log; if exit 0 and make_summary
  OK: commit and push the request research/alife/vecworld/program/gpu/requests/r6-dialsa3-001.json (written, ref
  37035b5c8, cap $9.60), then wait on origin/gpu-jobs:jobs/r6-dialsa3-001/status.json; read review.md first.
