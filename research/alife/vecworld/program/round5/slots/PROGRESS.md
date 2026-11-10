# PROGRESS (study slots, round 5) -- kept for restarts

Updated 07:03 UTC 10 Nov (instance 4, after the third container restart at about 01:12).

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
- r5-slots-005 (cancelled before start, $0: the Mac asked for XLA_PYTHON_CLIENT_MEM_FRACTION=0.9) and r5-slots-006
  (cancelled before start, $0: cap 7 cents under the rentable H100 offer) never had a pod.
- r5-slots-007 (same ref 7099a0ded, S5_SIZE=pilot, 2000 steps) ran 05:29-06:00 UTC on an A100_40GB (lambdalabs,
  $1.99/h) and FAILED, $1.04 billed: references and sam_sup fine (9.4 s per 100 steps, as on the H200; sam_sup
  ARI 0.85 against the tracker), then all 13 other configs hit RESOURCE_EXHAUSTED in jit_val (17-19 GiB) with 17% of
  the BFC pool in use: the 36 GiB pool could not supply a second contiguous block. Outputs kept in
  results/r5-slots-007/ (32 certified halves: references and sam_sup; train_errors.txt).
- GPU job r5-slots-008 (requested about 06:17 UTC): same ref 7099a0ded, same env plus
  XLA_PYTHON_CLIENT_ALLOCATOR=platform (no pool, so no contiguity problem; valid value in jaxlib 0.12.0.1) and
  S5_STEPS=3000; types A100_40GB / A100_80GB / H100_80GB, max 3.5 h, cap $20.80 (= what is left of $25: billed so
  far $3.13 + $1.04). Expected: all 14 configs in about 1.9 h, about $4 on the A100_40GB. Status:
  git fetch origin gpu-jobs; git show origin/gpu-jobs:jobs/r5-slots-008/status.json (and review.md).
  Watcher: bash <scratchpad>/slots/watch.sh r5-slots-008; heartbeat: <scratchpad>/slots/hb.sh r5-slots-008.
  NEVER resubmit while it is queued or running. If it fails again there is no budget for another long job on an
  H100; an A100_40GB job of 2 h costs about $4.

- 06:30 UTC: r5-slots-008 STARTED on an A100_40GB (lambdalabs, $1.99/h; the Mac's review: fine to run). Coordinator's
  conditions (COORD.txt 06:07): watch the first validation of the SECOND config (sam_set, about 20 minutes in); if
  it is RESOURCE_EXHAUSTED again, push gpu/requests/r5-slots-008.cancel at once; if 008 fails on memory, the next
  request is 80 GB cards only (no third try of this code on a 40 GB card); report what the platform allocator cost
  in step time (reference: 9.4 s per 100 steps).

- 07:00 UTC heartbeat: the platform allocator WORKS (no slowdown: reference stage 502 s against 492 s; sam_sup 3000
  steps in 364 s at 9.4 s per 100 steps); sam_set (second config) is training past step 2000, 21.6 s per 100 steps
  on this card (2.25 times the H200's 9.6 s). At about 830 s per config expect 10-12 of the 14 configs before the
  training deadline (10400 s from 06:30:28 = 09:23:48 UTC); job.sh ends by 09:49 UTC at the latest; about $7.

## Next step (exact)
1. when the job ends (done / failed / timeout): bash sfetch.sh r5-slots-008 <scratch dir>; look at progress.txt,
   table.txt, train_done.json (skipped configs), train/*.json (checkpoints, cut_by_deadline), train_errors.txt.
   Remember: the config still training at the training deadline has NULL objective values; a _ws config cut before
   step 250 still carries sam_sup's encoder (not a result).
2. rewrite results/interpretation.json for r5-slots-008 (claims with key paths into combined.json), run
   python -B ssummary.py results r5-slots-008 r5-slots-003 r5-slots-007; python -B sfigs.py <scratch>/r5-slots-008/out results/figs
   (the cancelled requests 004, 005 and 006 never had a pod; the report lists them at $0; 007 failed at $1.04).
3. README.md (short; say that the doubled data was dropped and why), report; commit + push own paths; remove the
   worktree (git worktree remove --force /home/user/wt/slots; git branch -D wt-slots) and the scratch.
