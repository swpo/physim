# DEVIATIONS (dialsB)

Nearest things done where the plan, the assignment or DECLARED.md could not be followed, recorded at the time.

1. **11 Nov, 16:20 UTC, the job id.** The assignment names the job ids `r6-dialsB-001, 002, ...` and DECLARED.md 2.7
   names `r6-dialsB-001`. The request with that id was pushed at 16:07 UTC (commit 6e9b9d464) and the runner had
   not acknowledged it 13 minutes later (no `jobs/r6-dialsB-001/` on `gpu-jobs`, no ledger entry; an earlier
   request of the same day was acknowledged 25 seconds after its commit, and study A's `r6-dialsA-001` was not
   acknowledged either). `PROTOCOL.md` on `gpu-jobs` gives the id pattern `[a-z0-9][a-z0-9-]{2,47}`: an upper-case
   letter does not match it. Nearest thing: `r6-dialsB-001.cancel` was pushed first, so that the request cannot
   start later, and the same request was pushed as **`r6-dialsb-001`** (lower case), pinned by `ref` to the
   tested commit 52ae6e403631. Nothing else changed: same paths, machine, hours, cap, script and sizes. Further
   jobs, if any, would be `r6-dialsb-002, ...`.
2. **The ranges are hashed inside the job, committed after it.** The plan asks for the scans' output "committed
   with a hash", and the assignment for ONE job. The container cannot reach the machine while the job runs, so
   the hash is computed and printed by the job before its first gate run (`ranges.sha256`, stdout, every gate
   process checks it), and the file and its hash are committed here from the job's output. The rule that turns
   the scans into ranges was committed before the job (DECLARED.md 2.6).
