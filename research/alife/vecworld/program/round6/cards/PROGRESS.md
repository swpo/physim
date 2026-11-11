# Study cards (round 6): progress

Worktree /home/user/wt/cards (branch wt-cards), study folder `research/alife/vecworld/program/round6/cards`.
Scratch: /tmp/claude-0/-home-user/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/cards (delete when done).
Coordinator channel: scratchpad/cards_COORD.txt (read at start and after waits).

## State (updated 11 Nov 2026, 11:42 UTC)

Done
- Code: `cardlib.py`, `adapters.py`, `gates.py`, `job.py`, `job.sh`, `make_worlds.py` -> `worlds.json` (70 worlds,
  125 runs), `make_cards.py`, `check_cardlib.py` (estimators against a closed-form world: passes), `fetch.sh`, `watch.sh`.
- HYPOTHESES.md and gates.py committed before the GPU request (commit 3e48ce881; paired plug-in loss added in f81aba84e).
- CPU test of job.sh at tiny size from a git archive of the eleven requested paths at f81aba84e: 16 runs, exit 0.

Running
- **r6-cards-001** requested at about 11:42 UTC (A100 40GB first; max 2.0 h; cap $11.40). Nothing else.

Exact next step
1. `bash watch.sh r6-cards-001` (one loop, ends on a final state); read `origin/gpu-jobs:jobs/r6-cards-001/review.md`.
2. `bash fetch.sh r6-cards-001` -> `work/r6-cards-001/out`; then
   `python -B make_cards.py work/r6-cards-001/out --job r6-cards-001 --rate <rate from status.json>`.
3. Read results/table.md and the control verdicts first (the card's own test), then write results/summary.json
   (every number with job id, file, key), README.md, the final report. Remove the worktree when done.
If the job fails in the presmoke: fix, rerun the tiny archive test, request r6-cards-002 (A100 only, cap about $4.6).
