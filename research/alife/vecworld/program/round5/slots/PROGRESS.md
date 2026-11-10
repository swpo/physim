# PROGRESS (study slots, round 5) -- kept for restarts

Updated 01:33 UTC 10 Nov (instance 4, after the third container restart).

## Done
- r5-slots-001 cancelled, r5-slots-002 infra_error ($0), r5-slots-003 pilot done ($3.13, H200, ref e5d146ef3; outputs in results/r5-slots-003/).
- Review fixes on origin as e139c34f3 (results/review.json).
- Changes after the pilot (S5_FIXED, S5_CERT_O=refs, S5_CFG_MIN_S / S5_CFG_MAX_S, tracker recall/purity diagnostic at
  validation, ssummary/scombine for agreement-only Phis) and the pilot's outputs: pushed as 7099a0ded.
  Checked before the commit: syntax of every module, ssummary.py on the pilot's outputs (22 Phis, 2 configs).

## Running
- 01:31 UTC: tiny end-to-end run of job.sh on CPU from a git archive of 7099a0ded (six request paths), env of the
  draft request with S5_SIZE=tiny S5_ALLOW_CPU=1 S5_WORKERS=2; script scratchpad/slots/run_tiny.sh, output
  scratchpad/slots/t3/ (job.stdout ends with "EXIT <code>"). About 16 minutes. If the container restarts: rerun it.
- nothing on the GPU. No request for the full job is on the branch yet (requests on the branch: 001-003).

## Next step (exact)
1. tiny run passes (EXIT 0, FAIL=0, 14 configs trained, table.txt written): set "ref" in the untracked draft
   gpu/requests/r5-slots-004.json to the tested commit (the code must not change between test and request),
   commit + push the request only, start the watcher (scratchpad/slots/watch.sh r5-slots-004).
2. when the job ends: sfetch.sh r5-slots-004 <scratch>, write results/interpretation.json, run
   ssummary.py results r5-slots-004 r5-slots-003, sfigs.py, README.md, report.
Budget: $25 cap, $3.13 spent; r5-slots-004 cap $21.80 (H200 bills $6.69/h; 2.9 h + 0.25 h = $21.07).
