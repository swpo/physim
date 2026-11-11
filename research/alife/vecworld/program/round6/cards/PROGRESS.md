# Study cards (round 6): progress

Worktree /home/user/wt/cards (branch wt-cards), study folder `research/alife/vecworld/program/round6/cards`.
Scratch: /tmp/claude-0/-home-user/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/cards (delete when done).
Coordinator channel: scratchpad/cards_COORD.txt (read at start and after waits).

## State (updated 11 Nov 2026, 12:00 UTC)

Done
- Code: `cardlib.py`, `adapters.py` (+ `strided`: the same world on a slower clock), `gates.py`, `job.py`, `job.sh`,
  `make_worlds.py` -> `worlds.json` (70 worlds, 125 runs), `make_worlds2.py` -> `worlds2.json` (second job: membrane,
  vortices, gliders on a clock of 4 world ticks), `make_cards.py`, `check_cardlib.py` (passes), `fetch.sh`, `watch.sh`.
- HYPOTHESES.md and gates.py committed before the GPU request (3e48ce881; paired plug-in loss f81aba84e).
- CPU test of job.sh at tiny size from a git archive of the eleven requested paths at f81aba84e: 16 runs, exit 0.
- CPU full-size run of foundry draw 4470 (run A) for the platform check: results/cpu_check/.
- CPU small-size runs of membrane and vortex64 at their real parameters: both sane; both "dull: the hidden part has
  no weight" at 1-32 world ticks, which is why the second job repeats them on a slower clock.

Running
- **r6-cards-001**: running on an A100 40GB (lambdalabs, $1.99/h) since 11:47 UTC; run deadline 13:47 UTC.

Exact next step
1. `bash watch.sh r6-cards-001` (one loop, ends on a final state); read `origin/gpu-jobs:jobs/r6-cards-001/review.md`.
2. `bash fetch.sh r6-cards-001` -> `work/r6-cards-001/out`; then
   `python -B make_cards.py work/r6-cards-001/out --job r6-cards-001 --rate 1.99`.
3. Read results/table.md and the control verdicts first (the card's own test).
4. Second job r6-cards-002 (A100 only, cap about $4.6): `CARDS_WORLDS=worlds2.json`; needs its own tiny archive test
   (job.py, adapters.py, gates.py changed after the first archive test) and a request file.
5. results/summary.json (every number with job id, file, key), README.md, final report. Remove the worktree when done.
