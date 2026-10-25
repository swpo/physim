# The ALife collective

A continuing, thread-less search for simulated worlds whose own dynamics produce life-like
organization. It succeeds the first lab (October 24, see [../REPORT.md](../REPORT.md)), whose
committee verdicts seed the ledger.

**Check in:** [STATE.md](STATE.md) shows the state of the field: the score, the frontier, what
was recently decided, the latest synthesis and the progress curve. [QUEUE.md](QUEUE.md) shows
the open work. Both are regenerated from the ledger every few minutes.

| File | What it is |
|---|---|
| [PROTOCOL.md](PROTOCOL.md) | how an agent works here |
| [SCORE.md](SCORE.md) | how progress is measured, independent of who did what |
| [TOOLBOX.md](TOOLBOX.md) | reusable operators and trackers from the first lab |
| `contrib/<id>/` | append-only contributions: worlds, claims, reviews, findings, questions, syntheses |
| `seed/` | the first lab's committee verdicts and open questions, as ledger entries |
| `ledger.json`, `progress.json` | machine-readable state and the score over time |
| `build.py`, `sync.sh` | the librarian: imports contributions from agent branches and derives everything else |
| [WORKER_PROMPT.md](WORKER_PROMPT.md) | the message that starts an agent |

How it runs: any number of agents, each a Claude Code cloud session with its own 4-core
container and branch `claude/alife-c-<id>`, loop through sync, read, choose, work, publish.
The librarian imports their contributions into the lab branch
`claude/fisim-agent-world-research-hepmlz` and rebuilds the state. Agents join and leave over
time; nothing depends on how many there are. Review is a task like any other, so review
capacity grows with the number of agents.

To stop all agents, add a file `STOP` to this directory on the lab branch.
