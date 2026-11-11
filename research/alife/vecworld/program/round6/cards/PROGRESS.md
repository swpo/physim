# Study cards (round 6): progress

Worktree /home/user/wt/cards (branch wt-cards), study folder `research/alife/vecworld/program/round6/cards`.
Scratch: /tmp/claude-0/-home-user/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/cards (delete when done).
Coordinator channel: scratchpad/cards_COORD.txt (read at start and after waits).

## State (updated 11 Nov 2026, 11:05 UTC)

Done
- Read the program (see git history of this file for the list).
- Code written (WIP, CPU-tested at tiny and small size on foundry draw 4470, the noise control and the
  free-bodies control): `cardlib.py` (adapter type, simulation, analysis), `adapters.py` (foundry, gliders,
  vortex, membrane, two controls), `gates.py` (derived numbers, declared thresholds, verdicts), `job.py`,
  `make_worlds.py` -> `worlds.json` (70 worlds, 125 runs: declared list).

Not yet tested: gliders, vortex, membrane adapters; job.py end to end.

Running: nothing on the GPU. No request submitted yet (ids will be r6-cards-001, ...).

Exact next step
1. HYPOTHESES.md (write and commit BEFORE the GPU request; gates.py holds the thresholds).
2. CPU: `CARDS_SIZE=tiny OUT=<scratch>/out python -B job.py` (one world per program group), fix what breaks.
3. job.sh; run it at tiny size from a `git archive` of exactly the requested paths; write
   `../../gpu/requests/r6-cards-001.json` (A100 40GB first; cap = rate x (max_hours + 0.25) + 0.10); push.
4. One background loop on origin/gpu-jobs:jobs/r6-cards-001/status.json; read review.md.
5. `fetch.sh` + `make_cards.py`: per-world card.md + figure, comparison table, results/summary.json, README.md.
