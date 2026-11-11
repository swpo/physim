# PROGRESS (crit_stats, round 6 dials: statistician's critique)

- 11 Nov 2026: worktree /home/user/wt/crit_stats created at 9d9439874. Task: read the six round-5 checker blocks,
  critique the three dial designs (defect_gliders, sublevel_second, compute_limit) for statistical adequacy,
  write CRITIQUE.md (< 900 words). No GPU, no model calls.
- Step 1 (in progress): reading program/README.md, roadmap/DECISIONS.md, ROADMAP.md sections 1 and 3.
- Step 1 done: program README, DECISIONS, ROADMAP 1-3 read; all six round-5 checker blocks read.
  Notes kept for the critique (source: round5/<study>/results/summary.json [checker]):
  - ladder: sigma SE over 8 worlds 0.0014-0.004 (block, object), 0.012-0.036 (population); no SE includes training
    seed; C trained once (6,000 steps, best validation at last/second-to-last evaluation in 9 of 9 cells);
    D(512) schedule-limited (47 of 48 nets best at step >= 2,250 of 2,500); P0u 3,000 steps against 6,000;
    rho undefined where C - P0 ~ 0 (SE 0.3 to > 100); n8 truths sat near the prior mean (RMS 0.39 vs 0.58 expected):
    nested truths asked for; screen holds within one view and family only (+0.74 block over 24 worlds).
  - vortexexam: C not a ceiling (same net with less history better by 0.045, z 4.8); sigma A -0.003 pod vs 0.045
    CPU retrain (seed/platform); sigma B 0.061 +- 0.048 (10 truths), 0.136 +- 0.054 against best C; short history
    0.232 +- 0.157, 0.126 without truth 6; per-truth sigmas 0.001 to 2.98; T equals a constant-drift control;
    each sigma used its own view's C; families and hidden set added after pilot A; best-over-families picked on
    the scored items.
  - agentenv: ring replication with 4 worlds: sigma SE 0.009 reported vs 0.020 replicated; rho 0.67 +- 0.38 vs
    0.75 +- 0.36; D at budget 0.343 vs 0.137; gliders full size (8 worlds, 512 items) rho SE 0.09-0.21 (ridge, net),
    sigma SE 0.004-0.008; grader gave every item seed 0 (item bootstrap optimistic).
  - bias2: "replication" reused the same simulations; replica means hide split outcomes; second training moved a
    ceiling 0.547 -> 0.473.
  - slots: best-of-three variant chosen after results; checkpoint selection on the scored held-out set.
  - foundry: band rule written after job 1; wind verdict on 4 worlds x 8 states.
- Step 2 (next): read the three designs' folders (results/summary.json), acceptance.py; small CPU check of the
  expected SE of sigma and rho from round-5 per-world scores.
