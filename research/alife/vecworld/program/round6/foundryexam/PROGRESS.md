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
- 11:29 r6-foundryexam-001 REJECTED by the runner's validation (notes above 4000 characters), $0, no pod. Resubmitted as
  r6-foundryexam-002 with shorter notes, same code (job.sh's two branches also checked with a stub interpreter).

- 11:44 r6-foundryexam-002 running on an A100-SXM4-40GB (lambdalabs, $1.99/h). Presmoke passed in 6 min (exit 0). Full pass
  started 11:49:45 (pod clock): gate passed pool 52/88 (seed 2026), 171/323 (enriched 2027), 3/5 (control); N30 132/240,
  N10 207/240; arm P has 210 training worlds x 64 episodes and 16 hidden worlds.
- 12:01 Mac review of 002: fine to run, 0 blocker, 0 major, 4 minor (results/job/review once fetched). Acted on in
  make_summary.py: the null's budget stays 512 and is flagged if D/FT(512) were cut; a net cut by a deadline is not
  counted as converged. Left for a next request: D(512)/FT(512) before the small budgets, info.json after every arm,
  try/except per hidden world, code norm without hidden worlds, own window masked out of the amortised context.

- 12:14 job 002 heartbeat: the two shared P0 nets took 838 s for 12,000 steps (70 ms per step; about 20 expected): one
  dispatch per step under the platform allocator. At that speed arm P's deadline falls before C starts. Decision: let 002
  finish arm P for an early look at P0, S, the ridge and the plug-ins (no C), then CANCEL it; rerun as 003.
- 12:35 changes for 003 (DESIGN.md section 5b, committed before the request): 50 steps per dispatch, global inputs as
  shifts, smaller batches, priority order of nets, presmoke speed guard (exit 4 if the projected net time does not fit),
  failure containment per hidden world, info.json after every arm. job.sh smoke from the git archive of the request's
  code: exit 0, all three arms (7.8 min).
- 12:40 request r6-foundryexam-003 pushed (A100, max 3.0 h, cap $7.80).

## Done
- design and criteria declared and committed; pool and centres; code; CPU smokes from the git archive; requests 001 (rejected,
  $0), 002 (to be cancelled after arm P), 003 (pushed).

## Running
- r6-foundryexam-002: cancel when its log shows "P done" (push an empty gpu/requests/r6-foundryexam-002.cancel).
- r6-foundryexam-003: watch with scratchpad/foundryexam/watch.sh r6-foundryexam-003. First thing to read: presmoke/shape_test.json
  (ms per step) in the heartbeat or the outputs.

## Exact next step
1. when 003 is final: `bash fetch.sh r6-foundryexam-003 <scratch>`; `python -B make_summary.py <scratch>/jobs/r6-foundryexam-003/out/full
   --job r6-foundryexam-003`; `python -B make_claims.py --job r6-foundryexam-003`; README.md; final report.
2. also fetch 002 (cancelled) for its record: status, review, partial arm P.
3. when finished: remove the worktree and the scratch folder.
