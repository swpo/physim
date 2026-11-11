# foundrylong: progress log (for a restart: read this, then `git log -- .`)

Worktree /home/user/wt/foundrylong (branch wt-foundrylong, pushes to claude/fisim-agent-world-research-hepmlz).
Scratch: /tmp/claude-0/-home-user/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/foundrylong/ (delete when done).

## Done
- 11 Nov 17:55 UTC: DECLARED.md (both stages, criteria, outcomes; commit 2ab6e7bb), DEVIATIONS.md, inputs/pilot_worlds.json and
  inputs/code_norm.json (copied from job r6-foundryexam-005), make_sel.py (reproduces the seed-2027 selection: 384 of 384).
- 18:02: inputs/sel_2028.json: 15,040 of 160,000 draws of prior seed 2028 pass the weights-only pre-screen (9.40%).
- 18:21: fl_lib.py (driver), run_fl.py + job.sh (stage-1 job), make_summary.py; DEVIATIONS.md addendum 1; the whole job.sh
  at FL_SIZE=smoke from a git archive of the four request paths: exit 0 (5.7 min on CPU); make_summary.py runs on its outputs.
- 18:25: request gpu/requests/r6-foundrylong-001.json pushed (cap $8.10, max_hours 3.15, expected 2.65 h, about $5.3).

## Running
- GPU job r6-foundrylong-001 (stage 1). Follow: cd /home/user/physim && git fetch -q origin gpu-jobs &&
  git show origin/gpu-jobs:jobs/r6-foundrylong-001/status.json. READ jobs/r6-foundrylong-001/review.md BEFORE the results.
  To cancel: push an empty gpu/requests/r6-foundrylong-001.cancel, verify with git ls-tree on origin.

## Next step, exactly
1. When the job is done: copy jobs/r6-foundrylong-001/out/full to scratch (git archive origin/gpu-jobs jobs/r6-foundrylong-001/out/full | tar -x),
   run `python -B make_summary.py <dir> --job r6-foundrylong-001` -> results/analysis_stage1.json; read S1 (verdict), S1a, S2-S5.
2. If S1.stage2_runs: write the stage-2 addendum in DEVIATIONS.md (sizes, assimilation details, designed-program rule), the
   W code (fl_w.py), CPU tests on public worlds, job script, request r6-foundrylong-002. Otherwise stop and report.
3. CPU part (any time): cpu_part.py -> results/cpu_part.json: speed on 2 cores (float64, float32), bundle size, reference rows.
4. results/summary.json (every number with its source), README.md, final report.

## Jobs
| job | state | cap | billed |
|---|---|---|---|
| r6-foundrylong-001 | requested 18:25 UTC | $8.10 | - |
