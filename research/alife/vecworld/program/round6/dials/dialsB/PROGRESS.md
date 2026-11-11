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

## Next step (exact)

1. When the tiny run exits 0: read `out_tiny/analysis.json` for sanity, run `s0.py align` once here (full size,
   seed 5, a pilot seed) to confirm L(pub), L(pub0), L(O) equal the designer's file.
2. Re-run the tiny whole-job test from an archive of the final commit, then commit the request
   `research/alife/vecworld/program/gpu/requests/r6-dialsB-001.json` (CPU_NODE 16 vCPU / 64 GB, max_hours 3.5,
   cap $2.50; draft in scratch `dialsB/req_draft.json`), push, and wait with one background loop on gpu-jobs.
3. Read `jobs/r6-dialsB-001/review.md` BEFORE the results; then `make_summary.py`, README.md, final report.

## Jobs

none yet
