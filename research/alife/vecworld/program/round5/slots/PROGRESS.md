# PROGRESS (study slots, round 5) -- kept for restarts

Updated 01:20 UTC 10 Nov (instance 4, after the third container restart).

## Done
- r5-slots-001 cancelled, r5-slots-002 infra_error ($0), r5-slots-003 pilot done ($3.13, H200, ref e5d146ef3; outputs in results/r5-slots-003/).
- Review fixes on origin as e139c34f3 (results/review.json).
- Changes after the pilot (S5_FIXED, S5_CERT_O=refs, S5_CFG_MIN_S / S5_CFG_MAX_S, tracker recall/purity diagnostic at
  validation, ssummary/scombine for agreement-only Phis): staged by instance 3, index tree 6c43bea1; its tiny
  end-to-end run was cut by the restart at 00:53 after 2 of 14 configs (no error up to there).

## Running
- nothing on the GPU. No request for the full job is on the branch yet (requests on the branch: 001-003).

## Next step (exact)
1. commit + push the staged work (this file included), no request file.
2. tiny end-to-end run of job.sh from a git archive of the pushed commit (the six request paths), env of the
   draft request gpu/requests/r5-slots-004.json (untracked) with S5_SIZE=tiny S5_ALLOW_CPU=1 S5_WORKERS=2.
3. if it passes: pin "ref" in r5-slots-004.json to the pushed commit, commit + push the request, start the watcher
   (scratchpad/slots/watch.sh r5-slots-004), then fetch with sfetch.sh, run ssummary.py, write README + report.
