# vfport: PROGRESS (builder)

Study: PhySim v2 exam as a verifiers environment (round 6). Worktree `/home/user/wt/vfport`, branch pushes to
`claude/fisim-agent-world-research-hepmlz`. Scratch: `/tmp/claude-0/-home-user/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/vfport/`.
Venv: `/home/user/evalwork/vfport/.venv` (python 3.12, verifiers 0.3.2.dev163 wheel as v1 pins).

## Done
- Read: the memo (GRADER_VS_VERIFIERS.md), agentenv (all of evaluator/, physim2/, agents/, run_rollout, prove,
  check_probe), v1 (taskset.py, runtime_sandbox.py, container_worker.py, runtime_access.py), verifiers
  (isolated_verifier/env.py, task.py, rollout.py, mcp/*, runtimes/docker/*, utils/artifacts.py, harness.py).
- Docker daemon starts in this container (docker 29.9.2, `docker info` answers): the memo's "this cloud container
  has no Docker daemon" (section 3) no longer holds here.

## Running
- nothing

## Next step (exact)
1. `uv venv /home/user/evalwork/vfport/.venv --python 3.12` and install the verifiers wheel + numpy (+ jax for the Lab).
2. Build the agent/verifier image (python:3.12-slim + numpy/scipy/jax) and `localhost/verifiers-network:1`.
3. Package `physim2_env/` (taskset, lab toolset, reward worker), `physim2_script/` (scripted harness).
