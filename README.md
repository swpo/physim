# gpu-jobs

Results branch for Prime GPU jobs. Cloud sessions request jobs by pushing a request file to
their own `claude/*` branch (see PROTOCOL.md); the PhySim macbook session runs them and publishes
`jobs/<job_id>/`, `ledger.json` and `LEDGER.md` here.
Model rollouts, which run on the Mac itself, are requested the same way (see ROLLOUTS.md) and
published under `rollouts/<job_id>/`, with `rollouts/ledger.json` and a "Model rollouts" table
in `LEDGER.md`. GPU jobs and rollouts share one job id namespace.
Only the runner writes this branch, and it builds each commit from its own records, dropping
anything else. Never push to it.
