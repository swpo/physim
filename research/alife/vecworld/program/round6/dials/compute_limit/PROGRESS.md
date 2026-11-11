# PROGRESS (designer compute_limit, round 6 dials, study c)

STATE: FINISHED (11 Nov, 13:50 UTC). DESIGN.md is the deliverable; results/summary.json and results/mut100.json hold
every number; the scratch folder and the worktree are removed after the last push.

What was run (CPU, one process at a time, nice 10; 2.0 CPU-hours of simulation, summary.json [cpu]):
1. run_pools.sh: level-2 pools at 32 px (60 members x 380 ticks), 48 px (20 x 320), 64 px (16 x 260); later one more
   64 px pool (4 members) and two 128 px pools (8 members x 260 ticks) by run_after.sh and run_after3.sh.
2. screen_state.py (run_after.sh, run_after2.sh): four 64 px states at tick 140, eight fresh-noise branches each,
   arms none / blind / aimed (200 nats), native step x 1, x 2, x 5, four 32 px tiles per state. The two "x 4" lines
   stop at an assertion (250 / 4 is not an integer); nothing was lost.
3. analyse.py <scratch>: finite-size table, budget curve, horizon transfer, transfer to 128 px, screen. A second
   full run reproduced every number (only a note and the new cpu block differ).
4. run_mut100.sh + check_mut100.py: the transfer from 64 to 128 px at mut128 = 100.

Findings (all at tiny size, public parameters, level 2 from its own state):
- Rescaled small-box predictors lose 0.10 (64 px) to 0.31 (32 px) at 128 px; a regression on POOLED small boxes
  (4 x 64 px or 7 x 48 px) equals the exam-size reference; from 32 px (2.3 vortices per box) nothing does.
- The level-2 law beats brute-force learners only at a budget of one exam-size episode, where a constant-drift
  control is level with it; from 8 episodes a generic regression is better.
- A native step five times longer and 3 members instead of 7 lose nothing at level 2 given the state; a truncated
  horizon and tiles cut from the state are worse than a level-2 model that costs nothing.
- Designed stirring neither exposes a surrogate's defect nor helps to fit the law's constants.
- Overflow counters of the tracker (saved apart since 12:50): 0 overflow ticks on every pool made after the fix
  (64 px peak 13-15 of 24 slots, 128 px peak 46-48 of 56). The older pools carry only the meaningless sum.
- Forecast: design (c) fails on fed vortices; a $5 stop-rule job is proposed; the pooling defect is proposed as a
  world-card quantity.

Three runs exceeded "a few CPU-minutes": the 128 px pools (14, 15 and 18 CPU-minutes).
