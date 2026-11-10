# PROGRESS (study bias2, round 5) -- kept for restarts

Updated 2026-11-10 01:16 UTC (instance 4, after the restart at about 01:12).

## Done
- Code written and CPU-tested (c5.py, csim.py, ctrain.py, ccert.py, ccombine.py, job.sh, analysis tools).
- GPU jobs r5-bias2-004 (membrane + gliders) and r5-bias2-005 (vortex): both done, exit 0. Billed $4.6802 + $3.6269
  = $8.3071 (status.json:cost.billed_usd). 001 rejected, 002/003 cancelled, $0.
- Nothing is running; no watcher is needed.

## Next (in order)
1. bash cfetch.sh r5-bias2-004 membrane gliders; bash cfetch.sh r5-bias2-005 vortex   (copies small outputs into results/)
2. canalyze.py -> results/analysis.json; cpair.py on out/<world>/items (fetched to scratch, not committed)
3. add final states and billed costs to results/job_history.json; csummary.py -> results/summary.json
4. README.md; commit; push; remove the worktree; report.
