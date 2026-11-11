# PROGRESS: round 6, dials, designer "defect_gliders"

Design study (b) on the gliders wind world: an incomplete public law with a hidden extra term of strength eta.
Design phase only: no GPU, no model calls, small CPU checks.

- 11 Nov 02:40 UTC. Worktree made; program README, DECISIONS, ROADMAP 1 and 3, round-5 ladder README and its
  checker block read. CPU speed measured: 9.1 gliders ticks/s on one thread of the shared container
  (scratch `probe0.py`, 4 members x 50 ticks in 22.1 s).
- Plan: `dlaw.py` (gliders wind tick with five optional hidden terms, all off = the public law), `screen.py`
  (the round-5 screen at tiny size: oracle against the public-law simulator from the hidden state, per input
  program, passive against designed), `results/*.json`, then `DESIGN.md`.
- Candidates: G gust (flow gain above a wind threshold), XW stress conversion (c0 -> c1 above a wind threshold),
  M scar (slow field charged by strong wind that weakens growth), X dense conversion (c0 -> c1 above a density
  threshold), T terrain (static smooth field shifting the growth centres).
