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
  `make_summary.py`; test at tiny size on CPU from a git archive; request `r6-dialsa-001` (A100 40 GB, cap $5).
- 11 Nov 15:52 UTC. Built: `xlaw.py` (law switch; one tick at xw = 0 is bitwise gworld.tick on CPU), `a_nets.py`
  (cross-validated fine-tuning in lockstep, the residual, program classes), `a_stats.py` (criteria),
  `run_a.py` + `job.sh` (presmoke at full shapes in the same process, speed guard, full pass), `check_a.py`,
  `make_summary.py`. A first tiny CPU pass of run_a.py is running in the scratch folder (debugging; not from
  an archive yet). DEVIATIONS entry 4 (stratified folds, the clock rule for doublings) written before any run.
- Running: local CPU smoke only. Jobs: none requested.
- Next: fix what the smoke finds; run check_a.py; run the whole job at tiny size from a git archive of the
  request's paths; write `gpu/requests/r6-dialsa-001.json` (A100 40 GB only, max_hours 2.2, cap $5); push; wait.
- 11 Nov 16:12 UTC. CPU tests done. `check_a.py` from a git archive: ok (one tick, a family of 8 members x 10
  ticks and a Lab batch bitwise equal to round 5's code at eta = 0; `results/check_a.json`). The whole of
  `job.sh` at tiny shapes from a git archive of the request's paths at 12082fa09: exit 0 in 8.7 min (presmoke,
  speed guard, full pass); `make_summary.py` runs on its outputs. Request `gpu/requests/r6-dialsa-001.json`
  written (A100 40 GB only, max_hours 2.2, cap $5.0, script limit 1.9 h).
- Running: job `r6-dialsa-001` requested (see the line below for its state). Nothing local.
- Next: wait for the job on origin/gpu-jobs (one loop, 60 s); read `jobs/r6-dialsa-001/review.md` BEFORE the
  results; copy `out/` to `results/job/`, `status.json` beside it; `python -B make_summary.py`; if the rule for
  g is undecided, request the extension to 16 truths as `r6-dialsa-002` (cap $3) and say so; write README.md;
  delete the scratch folder; remove the worktree.
- 11 Nov 16:27 UTC. The request was first pushed as `r6-dialsA-001` (16:11 UTC). The protocol's id pattern is lower
  case only, so the runner dropped it without publishing anything (the coordinator's note, 16:22). Renamed to
  `r6-dialsa-001`, pinned to ref f38f88ac0 (the tested job code), pushed. No job named r6-dialsA-001 ever existed.
  Since the first push: an extension mode in `run_a.py` (`--extension`, DECLARED R19; not tested yet, not used by
  this job) and a merge of two jobs in `make_summary.py` (`--job2`).
- Running: job `r6-dialsa-001` (requested; both GPU slots may be busy for a while).
- 11 Nov 16:33 UTC. `r6-dialsa-001` was REJECTED by the runner at 16:26 before any pod ($0): "notes: printable text
  up to 4000 characters" (mine had about 4,300). Resubmitted as `r6-dialsa-002`: the same request with notes of
  3,246 characters, pinned to ref f38f88ac0. A tiny CPU pass of the current head (extension mode present, not
  used) also exits 0.
- Running: job `r6-dialsa-002` (requested). Locally: a tiny CPU test of the extension mode.
- Next: as above (wait; review.md first; results to `results/job/`; make_summary; README).
