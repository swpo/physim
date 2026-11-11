# Study cards (round 6): progress

Worktree /home/user/wt/cards (branch wt-cards), study folder `research/alife/vecworld/program/round6/cards`.
Scratch: /tmp/claude-0/-home-user/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/cards (delete when done).
Coordinator channel: scratchpad/cards_COORD.txt (read at start and after waits).

## State (final, 11 Nov 2026, 13:30 UTC)

Done
- Tool: `cardlib.py`, `adapters.py`, `gates.py`; `check_cardlib.py` passes.
- HYPOTHESES.md committed before the first request (d27c3c6ba) and not edited since; DEVIATIONS.md beside it.
- **r6-cards-001**: done, exit 0, 125 of 125 runs, A100 40GB, billed $1.2495. **r6-cards-002**: done, exit 0, 15 of 15
  runs, A100 40GB, billed $1.4331. Total $2.68 of $25. Both reviews read before the results and acted on.
- Results: `results/cards/<world>/` (77 worlds: card.md, card.png, card.json), `results/table.md`, `table.csv`,
  `derived.json`, `robustness.json`, `summary.json` (43 claims with sources), `claims.md`, `results/jobs/`,
  `results/cpu_check/`. README.md written; its numbers were checked against the results files by script.

Running: nothing. No pod is alive (both status.json say pods terminated).

Next (not started; for the coordinator)
- An independent check of this study.
- A non-overlapping late window for the slow-clock membrane and vortex cards (about $0.5 on an A100).
- Exams on foundry 4186 and 4470 with the reference policies, then rollouts (see README, "Which worlds first").
