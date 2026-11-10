# PROGRESS (study foundry, round 5) -- kept for restarts

Updated 2026-11-10 06:35 UTC (instance 1; started 03:40 UTC).

## State: FINISHED
- Both GPU jobs are done and analysed; nothing is running or queued; no watcher is needed.
  - r5-foundry-001: done, exit 0, H100 80GB (datacrunch), 0.225 pod hours, billed $0.9246.
  - r5-foundry-002: done, exit 0, H200 141GB (nebius), 0.280 pod hours, billed $1.5503.
  - Total billed $2.4749 of $25.
- Deliverables committed and pushed: results/summary.json (35 claims with sources, 14 verdicts), README.md,
  results/interpretation.json, results/analysis.json, results/analysis_r2.json, results/per_draw.json.gz,
  results/fig/ (posters, 6 GIFs, charts), results/jobs/ (status, reviews, progress, ledger rows), CPU results
  (checks.json, wind_probe*.json, longrun.json, recheck_cpu*.json, cpu_vs_gpu.json).
- The Mac's reviews were read (results/jobs/<job>/review.md); the minor points of the first are fixed in job.py /
  analyze.py, the info point of the second (read only recorded chunks) in analyze2.py.

## If a restarted instance finds this
Nothing is left but the report (from results/interpretation.json and README.md) and removing the worktree
(/home/user/wt/foundry, branch wt-foundry) and the scratch folder (scratchpad/foundry). To rebuild the results:
`bash fetch.sh r5-foundry-001 && bash fetch.sh r5-foundry-002`, then the commands at the end of README.md.
