# vfport: PROGRESS (builder)

Study: PhySim v2 exam as a verifiers environment (round 6). Worktree `/home/user/wt/vfport`, branch pushes to
`claude/fisim-agent-world-research-hepmlz`. Scratch: `/tmp/claude-0/-home-user/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/vfport/`.
Venv: `/home/user/evalwork/vfport/.venv` (python 3.12, verifiers 0.3.2.dev163 wheel as v1 pins).

## Done
- Read: the memo, agentenv (evaluator/, physim2/, agents/, run_rollout, prove, check_probe), v1 (taskset.py,
  runtime_sandbox.py, container_worker.py, runtime_access.py), verifiers (isolated_verifier/env.py, task.py,
  rollout.py, mcp/*, runtimes/docker/*, utils/artifacts.py, harness.py, agent.py).
- Docker works here: `dockerd --feature containerd-snapshotter=false` (classic image store: no compressed copy of
  every layer, needed for the 600 MB budget). Images built: `physim2-ring:1` (513 MB incl. the 119 MB base;
  numpy+scipy+jax, jaxlib stripped), `localhost/verifiers-network:1` (+12 MB). `docker system df`: 524 MB.
- Found: verifiers' restricted Docker runtime passes `--sysctl net.ipv6.conf.all.disable_ipv6=1`
  (runtimes/docker/__init__.py:221-222); this kernel has no IPv6, so `docker run` fails with
  "open sysctl net.ipv6.conf.all.disable_ipv6 file: unsafe procfs detected ... no such file or directory".
  Workaround planned: a `docker` shim on PATH (tools/docker_shim) that drops that one option when
  /proc/sys/net/ipv6 is absent. The iptables cut itself was run by hand in a container here and works.
- Venv /home/user/evalwork/vfport/.venv: verifiers 0.3.2.dev163 wheel + numpy 2.5.4, scipy 1.18.1, jax 0.12.0.1.

- Built and working (commit 25b083f30 and later): physim2_env/ (taskset.py, lab_tools.py, access.py, bundle.py,
  grading.py, store.py, public/{labclient,validate,_item,_rules}.py), physim2_script/ (scripted harness),
  agents/ (install_prebuilt, probe_grading, hostile_submission), tools/ (make_instances, vfrun, prove, docker_shim).
- First rollouts through `vf-eval physim2-env --env.id isolated-verifier` on Docker here: D, C, P0 on one world
  graded with 0 failed items; about 75 s wall per rollout (57 s of it the 64-item verifier phase).
- Found: `docker exec` runs with umask 0000 in this container, so files written by verifiers' Runtime.write were
  world-writable; staging now chmods explicitly and the driver's --scan fixes any leftover.

## Running
- tools/prove.py, 4 worlds x (S, D, P0, PM, C, null), started 02:37 UTC; log $S/prove.log; state
  $S/proof/prove_state.json (resumable per policy); writes results/proof_ring.json.

## Next step (exact)
1. When prove.py ends: check results/proof_ring.json against agentenv's results/proof_ring.json.
2. tools/check_probe.py (boundary checks + probes a-d), then results/summary.json, README.md, RUNBOOK_MAC.md, uv.lock.

## If the container restarted
- `S=/tmp/claude-0/-home-user/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/vfport; mkdir -p $S;
  pgrep -x dockerd >/dev/null || (nohup dockerd --feature containerd-snapshotter=false > $S/dockerd.log 2>&1 &)`
- images survive in /var/lib/docker only if the disk survives; rebuild with docker/Dockerfile.ring (see its header).
- the instance store under $S/store does NOT survive a scratch wipe: re-run tools/make_instances.py.
