# Study A (dialsA), progress log

Worktree `/home/user/wt/dialsA`, branch `wt-dialsA`; scratch
`/tmp/claude-0/-home-user/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/dialsA/`.

- 11 Nov 15:35 UTC. Read PLAN.md, defect_gliders (DESIGN, dlaw.py, surrogate.py, check_zero), the three
  critiques, round5/ladder (lib, net, job, results), the jobs protocol. `DECLARED.md` and `DEVIATIONS.md`
  (three entries, all at declaration) written. No run, no job.
- Done: declaration.
- Running: nothing. Jobs: none requested.
- Next: build `xlaw.py` (law switch: level, world, batched runner, family simulator), `a_nets.py` (fine-tuning
  with cross-validation, the residual, saving nets), `run_a.py` + `job.sh` (presmoke at full shapes, speed
  guard, full run), `check_a.py` (CPU: eta = 0 bitwise against gworld.tick, tiny end-to-end), then
  `make_summary.py`; test at tiny size on CPU from a git archive; request `r6-dialsA-001` (A100 40 GB, cap $5).
- 11 Nov 15:52 UTC. Built: `xlaw.py` (law switch; one tick at xw = 0 is bitwise gworld.tick on CPU), `a_nets.py`
  (cross-validated fine-tuning in lockstep, the residual, program classes), `a_stats.py` (criteria),
  `run_a.py` + `job.sh` (presmoke at full shapes in the same process, speed guard, full pass), `check_a.py`,
  `make_summary.py`. A first tiny CPU pass of run_a.py is running in the scratch folder (debugging; not from
  an archive yet). DEVIATIONS entry 4 (stratified folds, the clock rule for doublings) written before any run.
- Running: local CPU smoke only. Jobs: none requested.
- Next: fix what the smoke finds; run check_a.py; run the whole job at tiny size from a git archive of the
  request's paths; write `gpu/requests/r6-dialsA-001.json` (A100 40 GB only, max_hours 2.2, cap $5); push; wait.
