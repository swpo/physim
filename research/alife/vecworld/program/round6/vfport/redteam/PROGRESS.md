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

## Status
- written: all scripts (not yet run).
- next: recon, overflow, fifo, plainD, hedge, hostile-*.
