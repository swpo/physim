# PROGRESS (study slots, round 5) -- kept for restarts

Updated 05:24 UTC 10 Nov (instance 4, after the third container restart at about 01:12).

## Done
- r5-slots-001 cancelled, r5-slots-002 infra_error ($0), r5-slots-003 pilot done ($3.13, H200, ref e5d146ef3; outputs in results/r5-slots-003/).
- Review fixes on origin as e139c34f3 (results/review.json).
- Changes after the pilot (S5_FIXED, S5_CERT_O=refs, S5_CFG_MIN_S / S5_CFG_MAX_S, tracker recall/purity diagnostic at
  validation, ssummary/scombine for agreement-only Phis) and the pilot's outputs: pushed as 7099a0ded.
- Tiny end-to-end run of job.sh on CPU from a git archive of 7099a0ded (six request paths, the request's env with
  S5_SIZE=tiny S5_ALLOW_CPU=1 S5_WORKERS=2), 01:17-01:39 UTC: EXIT 0, FAIL=0, 14 configs trained, 124 halves
  certified, 0 unclaimed, no errors; ssummary.py and sfigs.py run on its outputs.
- r5-slots-004 (full size, 80 GB cards only; requested 01:40, reviewed clean by the Mac at 02:05) never got a pod:
  no A100_80GB / H100_80GB / H200_141GB was rentable. CANCELLED before start at 04:01 ($0), with the coordinator's
  agreement (COORD.txt 03:54).
- results/summary.json, results/interpretation.json, README.md: PRELIMINARY (pilot only), to be rebuilt.

## Running
- r5-slots-005 was CANCELLED before start ($0) at 04:06: the Mac's review asked for XLA_PYTHON_CLIENT_MEM_FRACTION=0.9
  on a 40 GB card. r5-slots-006 (= 005 plus that env line) was CANCELLED before start ($0) at 05:22: its cap $18.75
  missed the only rentable offer (H100 via datacrunch at $5.0199/h) by 7 cents. GPU job r5-slots-007 (requested about
  05:24 UTC) = r5-slots-006 with cap $21.80: the SAME code ref 7099a0ded, S5_SIZE=pilot (48 trajectories per
  half, fits a 40 GB card), S5_STEPS=2000, types A100_40GB / A100_80GB / H100_80GB, max 3.5 h, cap $21.80
  (about $7.50 expected on an A100_40GB). Limits: training stops at 10400 s, certification 11200 s, workers killed
  at 11900 s. Expected on an A100: the first 9 configs. Status:
  git fetch origin gpu-jobs; git show origin/gpu-jobs:jobs/r5-slots-007/status.json (and review.md when it appears).
  Watcher (cheap to restart): bash <scratchpad>/slots/watch.sh r5-slots-007. NEVER resubmit while it is queued or
  running. Budget: cap $25, $3.13 billed, r5-slots-007 reserves up to $21.80.

## Next step (exact)
1. when the job ends (done / failed / timeout): bash sfetch.sh r5-slots-007 <scratch dir>; look at progress.txt,
   table.txt, train_done.json (skipped configs), train/*.json (checkpoints, cut_by_deadline), train_errors.txt.
   Remember: the config still training at the training deadline has NULL objective values; a _ws config cut before
   step 250 still carries sam_sup's encoder (not a result).
2. rewrite results/interpretation.json for r5-slots-007 (claims with key paths into combined.json), run
   python -B ssummary.py results r5-slots-007 r5-slots-003; python -B sfigs.py <scratch>/r5-slots-007/out results/figs
   (the cancelled requests 004, 005 and 006 never had a pod; the report lists them at $0).
3. README.md (short; say that the doubled data was dropped and why), report; commit + push own paths; remove the
   worktree (git worktree remove --force /home/user/wt/slots; git branch -D wt-slots) and the scratch.
