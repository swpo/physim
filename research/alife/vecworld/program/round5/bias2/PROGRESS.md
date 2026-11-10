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

## Done since (instance 4, 01:25-01:32 UTC)
- cclaims.py + cinterp.py -> results/interpretation.json (21 claims); csummary.py -> results/summary.json; README.md.
  All pushed. The study is reportable as it stands from this point.

## Follow-up GPU job (decided 01:30 UTC; details in results/job_history.json)
- r5-bias2-006: infra_error before a pod existed ($0). r5-bias2-007 (same ref affd4ecb2): done, exit 0, A100 40GB,
  $2.3364 billed, 02:25-03:36 UTC; all configs trained, 132 / 114 / 92 halves certified.
- Fetched into results/<world>_w (cfetch.sh with B5_SUFFIX=_w), analysed (canalyze, cextra, cpairs_run.sh), claims
  W1-W5 and X3 added to cclaims.py, summary.json and README rebuilt (27 claims). Billed in total $10.6435 of $35.

## State: FINISHED (10 Nov 2026 03:45 UTC)
Everything is pushed. Nothing is running or queued. Remaining for a restarted instance: nothing but the report
(from results/summary.json `claims` and README.md) and removing the worktree /home/user/wt/bias2.
