# PROGRESS (designer compute_limit, round 6 dials, study c)

- 11 Nov: worktree made, reading done (README, DECISIONS, ROADMAP 1+3, round5 vortexexam/ladder/agentenv checkers).
- Plan: (1) read vxlib / gliders / membrane sizes and CPU rates; (2) tiny CPU screens of where a scale-up binds
  (box area, horizon, rare events); (3) budget curve for P0 / small-box transfer / effective law / control; (4) DESIGN.md.
- Scratch: /tmp/claude-0/-home-user/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/dials_compute_limit/ (delete when done).
- CPU rate of vxlib.Runner (bench, 4 members): 0.0325 / 0.062 / 0.124 s per member-tick at 32 / 48 / 64 px.
- run_boxes.py written; pilot 64 px x 4 members x 260 ticks (eps 0.4, mut128 25): s_b 0 -> 0.92, N about 7-8 (137 CPU-s).
- Next: 32 px pool (same parameters), then transfer analysis (analog, tile-pooled, law, controls) and the budget curve.
- 12:15: run_pools.sh running in the background (64 px 3 x 4 members, 32 px 2 x 20, 48 px 2 x 10); first sign: the
  32 px box sweeps several times slower than the 64 px box (20 against 4 members; to be confirmed on the pools).
- screen_state.py + run_screen.sh (state-given screen: tiles, coarse step, truncated horizon, input arms) and
  analyse.py written, NOT yet run. Order after the pools: run_screen.sh, then analyse.py <scratch>, then DESIGN.md.
- 12:26: pools nearly done (64 px 16 members, 32 px 60, 48 px 10 of 20); run_after.sh queued (screen stages, one
  128 px run of 4 members, input arms). analyse.py now has: finite-size table, budget curve (analog, ridge, law,
  controls, tiles, residual recipe, finite-size extrapolation), horizon transfer (sources cut at tick 140), screen.
- Partial results (8 truth members, 40 small boxes; results/summary.json is a PARTIAL file until the final run):
  small boxes are biased (b1 0.13 at 32 px against 0.23 at 64 px; density +22%); few-constant models saturate at
  2-4 exam-size episodes and the law ties with its controls (lin, const, ridge); the law fitted on data cut at
  tick 140 extrapolates worse than a constant drift; small-box simulations do nearly as well as the reference there.
  Forecast for the design: a pure compute dial is filled by generic few-constant fits; say so and declare a stop rule.
