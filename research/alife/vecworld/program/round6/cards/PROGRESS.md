# Study cards (round 6): progress

Worktree /home/user/wt/cards (branch wt-cards), study folder `research/alife/vecworld/program/round6/cards`.
Scratch: /tmp/claude-0/-home-user/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/cards (delete when done).
Coordinator channel: scratchpad/cards_COORD.txt (read at start and after waits).

## State (updated 11 Nov 2026, 12:26 UTC)

Done
- Code complete: `cardlib.py`, `adapters.py`, `gates.py`, `job.py`, `job.sh`, `make_worlds.py` -> `worlds.json`,
  `make_worlds2.py` -> `worlds2.json`, `make_cards.py`, `make_summary.py` (written, not yet run on real data),
  `check_cardlib.py` (passes), `fetch.sh`, `watch.sh`.
- HYPOTHESES.md + gates.py committed before the first request; corrections after the Mac's review of r6-cards-001
  recorded in HYPOTHESES.md (last section) before any card was read.
- CPU: tiny archive tests of both jobs passed; full-size run of foundry draw 4470 on this CPU (results/cpu_check).

Running
- **r6-cards-001** (70 worlds, 125 runs): running on an A100 40GB (lambdalabs, $1.99/h) since 11:47 UTC; run deadline
  13:47 UTC; review: 0 blocker, 0 major, 6 minor (acted on, see HYPOTHESES.md).
- **r6-cards-002** (10 worlds, 15 runs, `CARDS_WORLDS=worlds2.json`): requested 12:24 UTC, A100 only, cap $4.30.

Exact next step
1. `bash watch.sh r6-cards-001` / `bash watch.sh r6-cards-002` (each ends on a final state).
2. `bash fetch.sh r6-cards-001; bash fetch.sh r6-cards-002`; check each `work/<job>/manifest.json` for
   `in_git: false` entries (review item 3: outputs near the 50 MB cap); copy status.json and out/job_state.json to
   `results/jobs/<job>/`.
3. `python -B make_cards.py r6-cards-001=work/r6-cards-001/out r6-cards-002=work/r6-cards-002/out --rate 1.99`
   then `python -B make_summary.py`.
4. Read results/table.md and the control verdicts first; write README.md and the final report; remove the worktree.
