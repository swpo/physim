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
- 16:42: the Mac's review of 001/002 read (`jobs/r6-dialsb-002/review.md`: 0 blocker, 0 major, 3 minor; fine to
  run). Acted on in the repository head (the job runs the pinned commit): scan V files get an index prefix
  (DK / dK and DL / dL differed by case only), the gate's npz is written whole and renamed, the dead XLA token
  is gone, `job.sh` takes the processor count before OMP_NUM_THREADS; `make_summary.py` copies the scan files
  under case-distinct names; `horizons.py` adds the per-horizon medians, leave-one-seed-out ranges and
  bootstraps that DECLARED.md 2.4 lists and the job's analysis.json lacks. `r6-dialsB-001.json` (upper case,
  never acknowledged, cancelled) is removed from the requests folder because it differs from
  `r6-dialsb-001.json` by case only; its `.cancel` stays. A tiny-size regression test of the head code is
  running here (scratch `dialsB/out_tiny`). To write up from the review: the noise keys are the same in every
  seed and arm; C3 also tests whether A_act's grid covers the truth.

- 17:03: **r6-dialsb-002 done** (exit 0, 25 min, $0.2204 billed). Review unchanged since read. Outputs fetched
  from `origin/gpu-jobs`; `make_summary.py`, `horizons.py`, `tables.py` run; `results/` committed.
- 17:10: after the fact, `diag_grid.py`: at the pilot centre the carrier field is a growing checkerboard wherever
  there is catalyst (README section 3). In no verdict.
- 17:25: README.md, DEVIATIONS.md 4-6, summary.json final. **Verdict by the declared rule: CLOSE CALL; the plan's
  rule at the point estimates: NO-GO; the build is not started.** DONE. Worktree and scratch removed after the
  last push.

## Next step (exact)

None for this study. For the coordinator: README section 5 (a gate at stable hidden values: one CPU job, about
$0.25, 1.5-2 agent-hours; not requested).

## Jobs

| job | state | note |
|---|---|---|
| r6-dialsB-001 | never acknowledged by the runner; cancel file pushed 16:21 UTC; request file removed later | upper-case id (DEVIATIONS 1); $0 |
| r6-dialsb-001 | failed 16:28 UTC, exit 3 (its own speed guard), $0.0432 billed | `nproc` answered 1 because OMP_NUM_THREADS=1 was exported first; presmoke passed (DEVIATIONS 3) |
| r6-dialsb-002 | done 17:03 UTC, exit 0, $0.2204 billed, 25 min on a nebius CPU node (16 vCPU, $0.54/h) | the tested commit 52ae6e403631 by `ref`, env S0_NPROC=16 |

Billed in all: $0.2636 of the study's $5.
