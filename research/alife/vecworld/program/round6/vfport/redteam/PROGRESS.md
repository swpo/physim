# vfport red team: PROGRESS

Role: red team of the verifiers port (round6/vfport, builder's final commit e4a30854d). Worktree
`/home/user/wt/vfportred` (branch wt-vfportred, pushes to claude/fisim-agent-world-research-hepmlz). Only this
folder (`redteam/`) is committed by this role. Scratch: `<scratchpad>/vfport/red/` (store = hidden pilot instance
`rt-ring-w0`, never an exam). Venv: the builder's `/home/user/evalwork/vfport/.venv`.

## Files
- `rt_run.py` (worker side): one attack = one `vf-eval` rollout (isolated-verifier, docker, physim2-script, push=false).
- `agent_rt.py` (agent box): recon, network, laboratory fuzz, budget races, attempt caps, score games, hostile exits.
- `predict_vprobe.py`, `predict_overflow.py`, `predict_fifo.py`, `predict_hedge.py` (verifier box).
- `results/<attack>.json`: what each run observed (no hidden value; pilot marker inside).

## How to run one attack
`S=<scratchpad>/vfport/red; V=/home/user/evalwork/vfport/.venv/bin/python; cd round6/vfport;`
`$V -B tools/make_instances.py --store $S/store --world ring --config smoke_ring --n 1 --prefix rt-ring` (once), then
`OMP_NUM_THREADS=1 $V -B redteam/rt_run.py --store $S/store --scratch $S/rt <attack>` with attack in
recon, overflow, fifo (add `--scoring-timeout 150`), plainD, hedge, null, hostile-exit1, hostile-sigkill,
hostile-killall, hostile-hangtar (add `--finalize-timeout 45`).

## Status: done (10 Nov 2026, about 04:10 UTC)
Every attack below was RUN through the route unless marked otherwise; numbers are in `results/<attack>.json`.

OPEN
1. `overflow`: a float64 reply written past predict_runner's float32 cast (samples at +-1e154/sqrt(sum 1/scale^2))
   passes check_shapes; all 448 per-item scores are -inf with 0 failed items; evaluator.grader.table gives
   vs_O = +inf; the trace reward is null (`worker_side_check`, `rollout.grade`).
2. `recon`, state between items: access times of the root-owned submission files (64 of 64 items read every earlier
   item's 16-bit fingerprint, 1008 bits at the last item); PID counter (pid step minus forks = 16 +-2);
   /dev/shm mtime phase (63 of 63) (`verifier_box_probe.atime_channel`, `.pid_channel`, `.dir_mtime_channel`).
3. `fifo` (--scoring-timeout 150): stderr.txt replaced by a named pipe; the reward blocks in grading.py:127 until
   the scoring stage times out; episode error "IsolatedVerifierEnv.finalize() timed out", no reward.
4. `hostile-exit1`, `-sigkill`, `-killall`: the harness script ends non-zero; HarnessError, no finalize, no reward.
5. `reply_bomb_offline.py` (offline, small): 3000 members, 0.6 MB reply, 91 MiB held by the worker; 64 MiB of reply
   extrapolates to 9.9 GiB (not run at that size).
6. `nproc_cross_box.sh` (by hand, two plain containers, the real driver): 255 sleeping processes of uid 1000 in one
   box make a one-thread predictor in another box fail ("can't start new thread"); `results/nproc_cross_box.txt`.
7. Not run (shared machine), read from `recon.json: boxes`, `agent_report.box`: no PID limit and no disk quota in
   either box (PidsLimit null, pids.max = max, the box sees the host's free disk).
8. `plainD`: a failed item is scored as K; 9 of 64 items of policy D are below K; crashing exactly those would give
   0.536 instead of 0.496 (counterfactual on the saved per-item scores; no class rule gained).
9. Small: three inputs give "infrastructure error; the evaluator must intervene"; a rejected `experiment` with a
   bad `n` still costs a reset; the validation and submission caps bind nothing (local validation, final collection).

CLOSED (observed): network of both boxes, proxy with and without its credential, laboratory budgets under 24
parallel calls, error messages, freeze at submit (a swap after submit is ignored), hard links, message queue,
System V segment handed to uid 0, setuid binaries, /proc of the driver, hanging tar in the agent box (K after the
finalize timeout).

## Left behind
- Docker daemon running, images kept (physim2-ring:1, localhost/verifiers-network:1, python:3.12-slim); no container.
- Scratch `<scratchpad>/vfport/red/` deleted (it held the hidden pilot instance rt-ring-w0).
