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
- 19:00: test 3 with the ONE-TICK loss (results/w_fit1tick_seed2027-46.json; 40 Adam steps, 4 episodes x 2 members x
  24-tick windows): the loss falls to the truth's level (0.236 -> -0.009 from the 30% start; truth -0.007 with the same
  keys) but the weights do not approach the truth (net distance 0.31 -> 0.37) and W's skill at the fit is poor
  (0.52 / 0.24 / -0.02 at 8 / 16 / 32 ticks; from another world 0.45 / 0.06 / -0.27). The one-tick loss is too weak a
  signal for long horizons. Next: the k-tick forecast loss (fl_w.episode_loss_k: assimilate to an anchor, forecast k
  ticks, score; gradient through the k ticks), k = 16, running on CPU (w_cpu.py --fit-k 16).
- 19:02: job 001 screen done (22 min, 38k member-ticks/s on the A100); gate: 818 of 1,490 new candidates pass, so P0
  reaches 1,000 worlds.
- 19:15: k = 16 fit (old score): loss 0.607 -> -0.031 (truth -0.041), skill at the fit 0.34 / 0.14 / -0.03. Then found
  a BUG in fl_w.fair_es: the spread term was divided by M(M-1), not 2M(M-1) (vw.scoring.energy_fair), so the fit loss
  was improper (it rewarded spread). Every fit-loss number above (test 2 ranking, both fit tests) used it; W's skills
  (scored by vw.scoring) are right. Fixed (checked against energy_fair to 1e-7).
- 19:29: k = 16 fit, fixed score (results/w_fitk16_seed2027-46.json; 40 steps, 8 Lab episodes, 4 x 2 members, 2 random
  anchors per episode): loss 0.769 -> 0.249 (truth 0.196, same keys), still falling; W's skill at the fit 0.79 / 0.68 /
  0.53 (truth 0.85 / 0.78 / 0.70). The forecast loss works from a 30% start. Running: the same from another screened
  world's weights (60 steps).

- 20:37: stage-2 code written ahead of the stage-1 verdict (early job log: skill at 16 ticks C 0.59, FT(32) 0.467,
  P0(1,000) 0.431, so sigma near 0.2 and stage 2 likely): fl_w.py (designed programs, paired designed Lab, batched fit,
  prediction), run_fl2.py, job_s2.sh. The whole run_fl2.py at smoke size on CPU: exit 0 (8.7 min). NOT requested.

- 21:02: job 001 DONE (exit 0, 2.35 h, billed $4.92; only items.npz stayed on the Mac, not needed). make_summary.py ->
  results/analysis_stage1.json: S1 SURVIVES, sigma(16, 32) = 0.218 [p10 0.187, min LOO 0.178, p90 0.253], null FT(32);
  S1a "at this compute" (the step 210 -> 1,000 prior worlds gained 0.114 of sigma; doubling P0's steps 0.003);
  S3 still falling at every horizon (s0(16) 0.53 / 0.39 / 0.28 at 64 / 210 / 1,000 worlds); S4 C not converged in data
  (+0.048 of skill at 16 ticks for 4,096 -> 16,384); S5 undecided (0.115, p05 0.077); S2: P0 and C mostly NOT trained
  by the 80% rule (late gains 1-5%), FT's CV chose the lowest rate in 122 of 144 cases. Stage 2 runs.
- 21:10: addendum 3 (stage-2 details, W's loss deviation, FT grid); inputs/stage1/ (31 MB of stage-1 parameters).
- 21:15: job_s2.sh at FL_SIZE=smoke from a git archive of the four request paths: exit 0 (9.6 min); make_summary2.py
  runs on its outputs. Request r6-foundrylong-002 validated (purpose 252 chars, notes 2,610, cap $8.10 >= $7.99).

## Running
- Review of r6-foundrylong-001 read 18:50: fine to run, 2 minor (outputs ~53 MB: check manifest in_git before the analysis;
  completeness marks added to make_summary.py; DEVIATIONS addendum 2).
- GPU job r6-foundrylong-002 (stage 2), requested ~21:20 UTC, cap $8.10. Follow: cd /home/user/physim && git fetch -q origin
  gpu-jobs && git show origin/gpu-jobs:jobs/r6-foundrylong-002/status.json. READ jobs/r6-foundrylong-002/review.md BEFORE
  the results. To cancel: push an empty gpu/requests/r6-foundrylong-002.cancel, verify with git ls-tree on origin.

- 21:35: make_final.py (results/summary.json from the analyses; the exam-profile numbers) drafted and run on stage 1.

## Next step, exactly (stage 2)
1. When 002 is done: read its review.md; check manifest in_git; git archive origin/gpu-jobs jobs/r6-foundrylong-002/out/full
   to scratch; python -B make_summary2.py <dir> --job r6-foundrylong-002 -> results/analysis_stage2.json; read T1-T6.
2. results/summary.json (every number with its source; make_final.py), README.md, final report; remove the worktree.

## Next step as it was before stage 1 (done)
1. When the job is done: copy jobs/r6-foundrylong-001/out/full to scratch (git archive origin/gpu-jobs jobs/r6-foundrylong-001/out/full | tar -x),
   run `python -B make_summary.py <dir> --job r6-foundrylong-001` -> results/analysis_stage1.json; read S1 (verdict), S1a, S2-S5.
2. If S1.stage2_runs: write the stage-2 addendum in DEVIATIONS.md (sizes, assimilation details, designed-program rule), the
   W code (fl_w.py), CPU tests on public worlds, job script, request r6-foundrylong-002. Otherwise stop and report.
3. CPU part (any time): cpu_part.py -> results/cpu_part.json: speed on 2 cores (float64, float32), bundle size, reference rows.
4. results/summary.json (every number with its source), README.md, final report.

## Jobs
| job | state | cap | billed |
|---|---|---|---|
| r6-foundrylong-001 | done 21:01 UTC (exit 0, 2.35 h of run) | $8.10 | $4.92 |
| r6-foundrylong-002 | requested ~21:20 UTC | $8.10 | - |
