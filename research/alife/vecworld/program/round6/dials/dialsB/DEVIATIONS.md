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
3. **11 Nov, 16:31 UTC, a second job.** `r6-dialsb-001` was stopped by its own speed guard after 5 minutes (exit 3;
   $0.0432 billed, `jobs/r6-dialsb-001/status.json` [cost.billed_usd]): `job.sh` exports `OMP_NUM_THREADS=1`
   before it calls `nproc`, and GNU `nproc` then answers 1, so the job planned one process at a time on a
   16-vCPU machine (projected 20,762 s against the guard's 9,000). The local tests had set `S0_NPROC` by hand
   and could not see it. The presmoke passed on the machine. This is a failure "for a reason that is not a
   result" (DECLARED.md 2.7): `r6-dialsb-002` is the same tested commit, pinned by `ref`, with the one
   environment variable `S0_NPROC=16`. No line of code and no declared size or rule changed.
   What the failed job showed before it stopped, stated here so that nobody can say it was used silently: its
   presmoke ran scan C's centre point at full size and printed gaps of 0.130 (no input), 0.142 (blind) and
   0.364 (aimed) (`jobs/r6-dialsb-001/out/presmoke.json` [scanC_point]). By the rule of DECLARED.md 2.6 the
   centre is then not "silent" (thresholds 0.03 and 0.05), so scan C will be recorded as failed and the gate
   will run every seed at the pilot centre. The rule stands as declared; nothing was changed in response.
