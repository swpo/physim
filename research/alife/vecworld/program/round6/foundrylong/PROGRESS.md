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
- 18:30: CPU part measured (cpu_part.py -> results/cpu_float64.json, cpu_float32.json; 2 pinned cores of a SHARED 4-core
  box, so speeds are lower bounds). fl_w.py (W prototype: nudged-ensemble assimilation, fit loss) and w_cpu.py (CPU
  tests 1 and 2 on a public world) written, not yet run. 18:28 stopped by the usage limit; 18:35 restart, WIP committed.
- 18:45 (before any stage-1 result was seen): w_cpu.py tests 1-2 on seed2027-46 -> results/w_cpu_seed2027-46.json.
  W at the TRUE weights: skill 0.85 / 0.78 / 0.70 at 8 / 16 / 32 ticks (8 items, 8 members; K = 0, O = 1); at another
  screened world's weights -0.49 / -0.75 / -1.13; net weights moved 10%: 0.73 / 0.63 / 0.53; 30%: 0.51 / 0.37 / 0.24.
  Fit loss (8 Lab episodes, 4 members): truth -0.004 and -0.012 (two ensembles), 3% -0.012, 10% +0.029, 30% +0.109,
  other screened worlds +0.29 to +0.66: ranks 10% from the truth, not 3%. W is viable if a fit gets within ~10%.
- 18:50: fl_w.py fit coordinates z (248 numbers; dens set from the observed mean mass), Adam, value_and_grad with
  remat; w_cpu.py test 3 (fit from a 30% neighbour with scalars and from another screened world) running on CPU.

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
| r6-foundrylong-001 | running since 18:32 UTC (A100 40GB, $1.99/h) | $8.10 | - |
