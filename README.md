# gpu-jobs

Results branch for Prime GPU jobs. Cloud sessions request jobs by pushing a request file to
their own `claude/*` branch (see PROTOCOL.md); the PhySim macbook session runs them and publishes
`jobs/<job_id>/`, `ledger.json` and `LEDGER.md` here.
Only the runner writes this branch, and it builds each commit from its own records, dropping
anything else. Never push to it.
