# PROGRESS (study bias2, round 5) -- kept for restarts

Updated 2026-11-10 01:16 UTC (instance 4, after the restart at about 01:12).

## Done
- Code written and CPU-tested (c5.py, csim.py, ctrain.py, ccert.py, ccombine.py, job.sh, analysis tools).
- GPU jobs r5-bias2-004 (membrane + gliders) and r5-bias2-005 (vortex): both done, exit 0. Billed $4.6802 + $3.6269
  = $8.3071 (status.json:cost.billed_usd). 001 rejected, 002/003 cancelled, $0.
- Nothing is running; no watcher is needed.

## Done since (instance 4, 10 Nov 01:13-01:25 UTC)
- cfetch.sh for both jobs -> results/<world>/ (combined.json committed as combined.json.gz), status/progress files.
- canalyze.py -> results/analysis.json, table_<world>.txt.
- cextra.py (new, local) -> results/extra.json: the global part of each latent and the shapes of the linear windows
  (needs latsub/ and windows/ of the jobs unpacked into a scratch folder: git archive origin/gpu-jobs jobs/<id>/out/<world>/{items,latsub,windows}).
- cpair.py -> results/pairs_<world>.json (paired trajectory bootstraps; needs items/ in the same scratch folder).

## Next (in order)
1. cclaims.py (the claims, as calls of claim() read by cinterp.py) -> results/interpretation.json
2. final states and billed costs into results/job_history.json; csummary.py -> results/summary.json
3. README.md; commit; push; remove the worktree; report. No further GPU job is planned.
