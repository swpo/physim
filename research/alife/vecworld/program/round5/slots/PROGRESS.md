# PROGRESS (study slots, round 5) -- kept for restarts

Updated 02:13 UTC 10 Nov (instance 4, after the third container restart at about 01:12).

## Done
- r5-slots-001 cancelled, r5-slots-002 infra_error ($0), r5-slots-003 pilot done ($3.13, H200, ref e5d146ef3; outputs in results/r5-slots-003/).
- Review fixes on origin as e139c34f3 (results/review.json).
- Changes after the pilot (S5_FIXED, S5_CERT_O=refs, S5_CFG_MIN_S / S5_CFG_MAX_S, tracker recall/purity diagnostic at
  validation, ssummary/scombine for agreement-only Phis) and the pilot's outputs: pushed as 7099a0ded.
- Tiny end-to-end run of job.sh on CPU from a git archive of 7099a0ded (six request paths, the request's env with
  S5_SIZE=tiny S5_ALLOW_CPU=1 S5_WORKERS=2), 01:17-01:39 UTC: EXIT 0, FAIL=0, 14 configs trained, 124 halves
  certified, 0 unclaimed, no errors; ssummary.py and sfigs.py run on its outputs.
- Request gpu/requests/r5-slots-004.json (the full job, ref 7099a0ded, cap $21.80, max 2.9 h) committed with this file.

## Running
- GPU job r5-slots-004 (requested about 01:43 UTC). Status: git fetch origin gpu-jobs; git show
  origin/gpu-jobs:jobs/r5-slots-004/status.json. Read jobs/r5-slots-004/review.md when it appears.
  Watcher (cheap to restart): scratchpad/slots/watch.sh r5-slots-004 (in /tmp/claude-0/-home-user/<session>/scratchpad).
  NEVER resubmit while it is queued or running. Budget left after it: about $0 (cap $25, $3.13 + up to $21.07).

- 02:05 UTC: the Mac's review of r5-slots-004 is published and clean (gpu-jobs:jobs/r5-slots-004/review.md; read).
  For the analysis: (a) the config still training at S5_TRAIN_S has NULL objective values; (b) a _ws config cut
  before about step 375 still carries sam_sup's encoder: do not report it as a result; (c) expect 8-11 configs.
  At 02:11 the job was still 'received' (two other pods hold the two slots: r5-vortexexam-003, r5-bias2-007).

## Next step (exact)
1. when the job ends (done / failed / timeout): bash sfetch.sh r5-slots-004 <scratch dir>; look at progress.txt,
   table.txt, train_done.json (skipped configs), train/*.json (checkpoints, cut_by_deadline).
2. write results/interpretation.json (claims with key paths into combined.json), run
   python -B ssummary.py results r5-slots-004 r5-slots-003; python -B sfigs.py <scratch>/r5-slots-004/out results/figs
3. README.md (short), report; commit + push own paths; remove the worktree and the scratch.
If the job fails early at $ small cost: read logs, fix, test on CPU, resubmit as r5-slots-005 only within the $25 cap.
