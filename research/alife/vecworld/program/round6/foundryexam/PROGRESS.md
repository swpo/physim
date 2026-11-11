# foundryexam: progress

Study: an exam pilot where the hidden law is a network's weights (the foundry's two-kind transport neural automaton).
Worktree: /home/user/wt/foundryexam (branch wt-foundryexam). Scratch: scratchpad/foundryexam/ (delete when done).

## Log (container clock, 11 Nov 2026)
- 10:31 session started (a restart; earlier selves left nothing committed). Read the program README, DECISIONS (Direction),
  the foundry (tnca, screen, criteria, checker), the ladder, the harness, acceptance.py and the GPU protocol.
- 10:44 wind probe on the 7 shortlisted worlds (CPU): results/wind_probe7.json. Centres by the declared rule: 3078, 1672, 7567.
- 10:45 DESIGN.md (public/hidden/told, worlds, exam, policies, criteria and thresholds) and results/pool.json committed
  BEFORE any GPU request (commit 11a3f558e).
- 10:53 fx_lib.py, fx_net.py, run_fx.py, job.sh written; CPU smoke (run_fx.py --size smoke --arms P,N30) passed end to end
  in 6.6 min (exit 0, failed [], skipped []).
- 11:00 padding (one compiled shape per kind of net), lock size = number of hidden worlds, arm time shares added.

## Done
- design and criteria declared and committed; pool and centres; code; first CPU smoke.

## Running
- nothing on the GPU yet.

## Exact next step
1. rerun the CPU smoke from a `git archive` of exactly the request's paths (vw1, round5/foundry, round5/agentenv/evaluator,
   round6/foundryexam): `FX_SIZE=smoke OUT=... bash job.sh`.
2. write research/alife/vecworld/program/gpu/requests/r6-foundryexam-001.json (A100_40GB, A100_80GB; max_hours 2.75; cap 7.2),
   commit with the code, push, then wait with one background loop on origin/gpu-jobs:jobs/r6-foundryexam-001/status.json.
3. while waiting: make_summary.py (scores.npz -> results/summary.json), README.md.
