# foundrylong: progress log (for a restart: read this, then `git log -- .`)

Worktree /home/user/wt/foundrylong (branch wt-foundrylong, pushes to claude/fisim-agent-world-research-hepmlz).
Scratch: /tmp/claude-0/-home-user/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/foundrylong/ (delete when done).

## Done
- 11 Nov 17:55 UTC: DECLARED.md (both stages, criteria, outcomes), DEVIATIONS.md (empty), inputs/pilot_worlds.json and
  inputs/code_norm.json (copied from job r6-foundryexam-005), make_sel.py (pre-screen of a fresh prior pool; reproduces
  the seed-2027 selection on its first 4,096 indices: 384 of 384).

## Running
- make_sel.py on prior seed 2028, pool 160,000 (CPU, background; log in scratch make_sel.log) -> inputs/sel_2028.json.

## Next step, exactly
1. When inputs/sel_2028.json exists: commit it.
2. Write fl_lib.py (constants H = 32, horizons 8/16/32 patched into fx_lib before fx_net is imported; the training
   driver with per-horizon sampling, validation and checkpoints; fine-tune cross-validation), run_fl.py (the job:
   screen, gate, simulations, hidden worlds, nets, scores, parameters of P0(1,000) and C(16,384) seed 0), job.sh.
3. CPU smoke from a git archive of the request's paths; request gpu/requests/r6-foundrylong-001.json; push; wait.
4. make_summary.py -> results/summary.json; verdict S1; stage 2 or stop.
5. CPU part: speed on 2 cores (float64, float32), bundle size, reference rows.

## Jobs
none yet (cap of the study $25, at most three jobs).
