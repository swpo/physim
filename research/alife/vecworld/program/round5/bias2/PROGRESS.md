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

## Follow-up GPU job r5-bias2-006 (decided 01:30 UTC; why: results/job_history.json and the request's notes)
- Question: in the vortex world the closure latents collapsed onto a box-scale mode (effective dimension 2-8) because the
  closure loss normalises pooled variance per channel. New arm Lw / Nw (B5_ARMS=w): closure loss on latents whitened over
  all 64 blocks. Does closure then find vorticity (vortex), cell material (membrane), mass (gliders)?
- Code: commit affd4ecb2 (c5.configs under B5_ARMS=w, cnets.train_glob_white, job.sh review fixes).
- Steps: (1) tiny CPU test of job.sh from a git archive of the requested paths at affd4ecb2 with the request's exact
  env (scratch t6; redo if a restart lost it); (2) commit + push ../../gpu/requests/r5-bias2-006.json (cap $12.4,
  max_hours 1.6; drafted in the worktree); (3) watcher: loop fetching origin/gpu-jobs every 60 s until
  jobs/r5-bias2-006/status.json is done/failed/timeout/cancelled/rejected/infra_error; (4) cfetch.sh r5-bias2-006
  vortex membrane gliders into results/w/ (NOT over results/<world>/: use RESULTS dir results_w, see cfetch.sh), canalyze,
  cpair, add claims W1.. to cclaims.py, csummary, README, job_history.json; (5) commit, push, remove worktree, report.
- STATE (01:40 UTC): step 1 passed (exit 0, 403 s). Step 2 done: request r5-bias2-006 pushed with ref pinned to
  affd4ecb2. Now at step 3 (watching). Never resubmit id 006. If it failed: read logs, fix, CPU-test, resubmit as 007
  only if the remaining cap allows (spent $8.31 + 006's bill; study cap $35).

## Next if the follow-up is abandoned
Report from results/summary.json as it is; say the follow-up was not run and why.
