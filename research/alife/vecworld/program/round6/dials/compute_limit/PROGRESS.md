# PROGRESS (designer compute_limit, round 6 dials, study c)

- 11 Nov: worktree made, reading done (README, DECISIONS, ROADMAP 1+3, round5 vortexexam/ladder/agentenv checkers).
- Plan: (1) read vxlib / gliders / membrane sizes and CPU rates; (2) tiny CPU screens of where a scale-up binds
  (box area, horizon, rare events); (3) budget curve for P0 / small-box transfer / effective law / control; (4) DESIGN.md.
- Scratch: /tmp/claude-0/-home-user/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/dials_compute_limit/ (delete when done).
- CPU rate of vxlib.Runner (bench, 4 members): 0.0325 / 0.062 / 0.124 s per member-tick at 32 / 48 / 64 px.
- run_boxes.py written; pilot 64 px x 4 members x 260 ticks (eps 0.4, mut128 25): s_b 0 -> 0.92, N about 7-8 (137 CPU-s).
- Next: 32 px pool (same parameters), then transfer analysis (analog, tile-pooled, law, controls) and the budget curve.
