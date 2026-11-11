# PROGRESS (dialsB: stage 0 of the membrane carrier, round 6 dials)

Deliverable: the verdict GO / NO-GO / CLOSE CALL of the plan's stage-0 rule for study B, `results/summary.json`,
README.md, DECLARED.md, DEVIATIONS.md.

- 11 Nov 15:17 UTC, start (not a restart): worktree /home/user/wt/dialsB made. Read PLAN.md in full,
  sublevel_second (DESIGN.md, sublevel.py, gvh.py, screen.py), crit_adversary (CRITIQUE.md, adv_fit.py,
  adv_act.py, adv_sim.py, summary.json), crit_stats and crit_cost CRITIQUE.md, defect_gliders/surrogate.py,
  membrane_world, the gpu-jobs PROTOCOL.md.
- 15:35: DECLARED.md written (the plan's row and rule copied; sizes, policies, scan rules and the three-way
  verdict fixed before any run). Nothing has run yet. No job requested.

## Next step (exact)

1. Write `stage0.py` (scans V and C, gate per seed and arm, analysis) and `job.sh` in this folder, importing
   `sublevel`, `screen`, `gvh` (designer) and `adv_act`, `adv_sim` (adversary) unchanged.
2. Tiny-size CPU test of the whole job script from a git archive of exactly the requested paths.
3. Request `research/alife/vecworld/program/gpu/requests/r6-dialsB-001.json` (CPU_NODE 16 vCPU, cap $2.50).

## Jobs

none yet
