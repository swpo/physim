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

## Running
- nothing

## Next step (exact)
1. Write physim2_env/ (public/{labclient,validate,_item,_rules}.py, access.py, lab_tools.py, taskset.py,
   grading.py), physim2_script/ (scripted harness), tools/{make_instances,prove,check_probe}.py, pyproject.toml.
2. `uv pip install -e .` into the venv; tools/make_instances.py for 1 ring world; one D rollout through vf-eval.

## If the container restarted
- `S=/tmp/claude-0/-home-user/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/vfport; mkdir -p $S;
  pgrep -x dockerd >/dev/null || (nohup dockerd --feature containerd-snapshotter=false > $S/dockerd.log 2>&1 &)`
- images survive in /var/lib/docker only if the disk survives; rebuild with docker/Dockerfile.ring (see its header).
- the instance store under $S/store does NOT survive a scratch wipe: re-run tools/make_instances.py.
