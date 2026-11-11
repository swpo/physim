# foundryexam: progress

Study: an exam pilot where the hidden law is a network's weights (the foundry's two-kind transport neural automaton).
Worktree: /home/user/wt/foundryexam (branch wt-foundryexam). Scratch: scratchpad/foundryexam/ (delete when done).

## Log (container clock, 11 Nov 2026)
- 10:31 session started (a restart; earlier selves left nothing committed). Read the program README, DECISIONS (Direction),
  the foundry (tnca, screen, criteria, checker), the ladder, the harness, acceptance.py and the GPU protocol.
- 10:44 wind probe on the 7 shortlisted worlds (CPU): results/wind_probe7.json. Centres by the declared rule: 3078, 1672, 7567.
- 10:45 DESIGN.md (public/hidden/told, worlds, exam, policies, criteria and thresholds) and results/pool.json committed
  BEFORE any GPU request (commit 82b655c98 on the branch).
- 10:53 fx_lib.py, fx_net.py, run_fx.py, job.sh written; CPU smoke (run_fx.py --size smoke --arms P,N30) passed end to end
  in 6.6 min (exit 0, failed [], skipped []).
- 11:00 padding (one compiled shape per kind of net), lock size = number of hidden worlds, arm time shares added.

- 11:07 CPU check of the gate at the real burn-in (results/gatecheck_cpu.txt): nearly frozen worlds passed at vp(16) >= 0.02;
  threshold raised to 0.2 BEFORE any GPU run (DESIGN.md section 2). Ceiling C = better of scratch and fine-tuned P0 (DESIGN.md
  section 4). make_summary.py written and tested on smoke outputs.
- 11:21 job.sh (FX_SIZE=smoke) from a git archive of exactly the request's four paths at commit 787de8679: exit 0 in 8.4 min.
- 11:25 request r6-foundryexam-001 committed and pushed (A100 40/80 GB, max 3.25 h, cap $8.40).

## Done
- design and criteria declared and committed; pool and centres; code; CPU smoke from the git archive; request 001 pushed.

## Running
- r6-foundryexam-001 (GPU job). Watch: scratchpad/foundryexam/watch.sh r6-foundryexam-001 (log watch_r6-foundryexam-001.log);
  status at origin/gpu-jobs:jobs/r6-foundryexam-001/status.json; read review.md when it appears.

## Exact next step
1. when the job is final: copy origin/gpu-jobs:jobs/r6-foundryexam-001/out/full to scratch, run
   `python -B make_summary.py <out>/full --job r6-foundryexam-001 --status <status.json>` -> results/analysis.json.
2. write results/summary.json (claims with job id, file, key), README.md, final report; copy status.json, review.md and the small
   job outputs (meta.json, info.json, gate.json, worlds.json without thetas if large) into results/job/.
3. if the job failed in the presmoke: fix, bump to r6-foundryexam-002 (never reuse an id), rerun the archive smoke first.
4. when finished: remove the worktree and the scratch folder.
