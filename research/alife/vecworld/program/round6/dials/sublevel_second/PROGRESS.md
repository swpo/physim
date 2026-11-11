# PROGRESS: round 6, dials, designer "sublevel_second"

Task: design study (b) on a second world with a hidden finer level (design only; CPU checks; no GPU, no model calls).
Deliverable: `DESIGN.md` in this folder.

- 11 Nov 2026, 02:42 UTC, start: worktree `wt-sublevel_second` created; reading round-5 material (ladder, vortexexam,
  foundry, bias2, agentenv, slots), the three candidate worlds' code and the acceptance code.
- 02:50: world chosen (phase-membrane cells); `sublevel.py` (four candidate hidden fields on top of the public
  membrane law: kpool, lpool, dorm, bound) and `check_zero.py` written; `results/check_zero.json`: at dial 0 three
  candidates equal the public world bit for bit, `dorm` to 3e-15 (fields) at 64 x 64, 3 members, 60 ticks.
- 10:31: the container restarted before the first commit; files were intact in the worktree. Re-read the material
  (program README, DECISIONS, ROADMAP 1 and 3, round-5 READMEs and checker blocks). Next: `screen.py` (round-5 screen
  per candidate: oracle against the public-law simulator from the hidden state; passive against designed input),
  then DESIGN.md.
