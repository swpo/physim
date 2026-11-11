# PROGRESS (dialsB: stage 0 of the membrane carrier, round 6 dials)

Deliverable: the verdict GO / NO-GO / CLOSE CALL of the plan's stage-0 rule for study B, `results/summary.json`,
README.md, DECLARED.md, DEVIATIONS.md.

- 11 Nov 15:17 UTC, start (not a restart): worktree /home/user/wt/dialsB made. Read PLAN.md in full,
  sublevel_second (DESIGN.md, sublevel.py, gvh.py, screen.py), crit_adversary (CRITIQUE.md, adv_fit.py,
  adv_act.py, adv_sim.py, summary.json), crit_stats and crit_cost CRITIQUE.md, defect_gliders/surrogate.py,
  membrane_world, the gpu-jobs PROTOCOL.md.
- 15:35: DECLARED.md written (the plan's row and rule copied; sizes, policies, scan rules and the three-way
  verdict fixed before any run). Nothing has run yet. No job requested.

- 15:45: `s0.py` (scans V and C, ranges with hash, gate per seed and arm, analysis, presmoke, alignment check on
  the designer's pilot seed 5), `job.sh` (presmoke, speed guard, phases with a deadline), `make_summary.py`.
  Presmoke at tiny size ran here (2 min; 424 member-ticks/s per process once compiled). The whole job script at
  tiny size from a git archive of the five requested paths is running here (scratch `dialsB/out_tiny`, smoke
  seeds 91, 92, never gate seeds). Nothing decisive has run; no job requested.

- 16:07: the whole job script at tiny size from a git archive of the five requested paths at 52ae6e403631:
  exit 0, 753 s (smoke seeds 91, 92; numbers meaningless). `s0.py align` at full size on the designer's pilot
  seed 5 reproduces his L(pub), L(pub0), L(O) exactly (max difference 0.0), G2 at 4, 8, 16 ticks to three
  decimals (the 32-tick gain differs: fitted here with the Lab's scale, as declared), and picks the adversary's
  filter (0.25, 1, 3, 2).
- 16:08: job **r6-dialsB-001** requested (CPU_NODE 16 vCPU / 64 GB, max_hours 3.5, cap $2.50).
- 16:21: the runner did not acknowledge r6-dialsB-001 in 13 minutes (upper-case id; DEVIATIONS.md 1): cancel file
  pushed and verified, the same request pushed as **r6-dialsb-001**.
- 16:31: r6-dialsb-001 ran on a nebius CPU node (16 vCPU, $0.54/h) and stopped at its speed guard (exit 3): the
  script took `nproc` = 1 (DEVIATIONS.md 3). r6-dialsb-002 requested: same commit, S0_NPROC=16.

## Next step (exact)

1. Wait: one background loop fetching `origin/gpu-jobs` every 60 s until `jobs/r6-dialsb-002/status.json` has a
   final state (done | failed | timeout | cancelled | rejected | infra_error). "queued, waiting for an offer" is
   not stuck; a stock-out is requeued by the runner.
2. Read `git show origin/gpu-jobs:jobs/r6-dialsb-002/review.md` BEFORE any result and act on it.
3. `git archive origin/gpu-jobs jobs/r6-dialsb-002 | tar -x -C <scratch>`; `python -B make_summary.py
   <scratch>/jobs/r6-dialsb-002`; commit `results/` (summary.json and results/job/*.json, ranges.sha256).
4. README.md (per-seed and per-horizon table, each condition with its number and verdict, what a build needs),
   DEVIATIONS.md, final report; remove the worktree and the scratch folder.

## Jobs

| job | state | note |
|---|---|---|
| r6-dialsB-001 | cancelled 16:21 UTC (cancel file pushed), never acknowledged by the runner | its id has an upper-case letter, which PROTOCOL.md's pattern does not allow; $0 |
| r6-dialsb-001 | failed 16:28 UTC, exit 3 (its own speed guard), $0.0432 billed | `nproc` answered 1 because OMP_NUM_THREADS=1 was exported first; presmoke passed (672 member-ticks/s per process); DEVIATIONS.md 3 |
| r6-dialsb-002 | requested 16:32 UTC | the same tested commit by `ref`, env S0_NPROC=16; cap $2.50 |
