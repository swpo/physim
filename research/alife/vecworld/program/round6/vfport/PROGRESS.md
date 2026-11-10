# vfport: PROGRESS

## FIXER (role after the builder, the specification review and the red team) -- 10 Nov 2026

Worktree `/home/user/wt/vfportfix` (branch wt-vfportfix, pushes to `claude/fisim-agent-world-research-hepmlz`).
Scratch `/tmp/claude-0/-home-user/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/vfport/fix/`. Venv: the builder's
`/home/user/evalwork/vfport/.venv`. Docker daemon was found running (classic image store), images kept.

### Plan (finding -> fix), status in brackets
- S1 duplicate / colliding / over-long tar members end a rollout ungraded -> freeze refuses them, finalize runs
  verifiers' own restore check inside its try, new hostile agents [todo]
- S2 = R2 state between items (timestamps, PID counter; also kernel counters of the shared box) -> a FRESH verifier
  box per item through verifiers' `provision_runtime` (default), the shared box stays as a pilot mode [todo]
- S3 the trusted side no longer validates -> the three public example calls run in the verifier box before item 1,
  round 5's rule (invalid = K); the tool ops validate/submit run the in-box validator through the controller [todo]
- R1 float64 reply overflows the score -> strict reply reader (float32, exact members), non-finite score = failed [todo]
- R3 FIFO as stderr.txt hangs grading -> non-blocking regular-file reads through a directory fd, per-item timeout [todo]
- R4 harness exit leaves no grade -> single_use on by default (keyed by agent), tools/settle.py records K [todo]
- R5 many-member reply -> members capped at the levels, bounded bytes [todo]
- R6 shared uid 1000 -> random uid per verifier box [todo]
- R7 no PID / disk limit -> operator setting, recorded per box, Open holes [todo]
- R8 crash returns K -> lead's decision, measured, Open holes [todo]
- R9, S4-S9 minors [todo]

### Next step (exact)
- implement in physim2_env/public/_rules.py, _item.py, grading.py, taskset.py, lab_tools.py, access.py; then
  tools/check_units.py (offline), tools/check_probe.py and tools/prove.py on Docker.

---

# (builder's record, kept)


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

- tools/check_probe.py RUN (02:47-02:52 UTC): results/probe_ring.json. Round 5's 34 checks: 32 reproduced, 0 failed,
  2 changed by design (agent is root in its own container). 33 of 33 new checks pass (probes a-d, with controls).
  Fixed on the way: zombies of killed predictor processes (driver is now subreaper and reaps), System V shared
  memory (removed as the predictor's user), umask 0 under docker exec.
- Written: README.md (two placeholders left: line counts and the proof numbers), RUNBOOK_MAC.md, configs/, uv.lock,
  tools/make_summary.py.

- tools/prove.py RUN (02:52-03:16 UTC): results/proof_ring.json. 24 rollouts, all graded, 0 failed items; table within
  noise of round 5's; the same C submission through round 5's grader gives identical per-item scores (4 worlds).
- tools/check_probe.py RUN again on the final code (03:16-03:22): results/probe_ring.json, 32 of 34 + 37 of 37.
- Gliders smoke: one instance and one D rollout through the route, graded (results/gliders_smoke_D.json).
- tools/make_summary.py -> results/summary.json (hidden-value scan: 6 instances, 192 files, 0 hits).
- README.md, RUNBOOK_MAC.md, uv.lock complete. Scratch stores and run outputs deleted (hidden instances).

## Running
- nothing. The Docker daemon is up (classic image store); images kept for the next role: physim2-ring:1 (562 MB
  with its 119 MB base), localhost/verifiers-network:1 (+12 MB). `docker system df`: 573 MB.

## Next step (exact)
- For another role: `S=<scratch>; V=/home/user/evalwork/vfport/.venv/bin/python; cd` to this folder, then
  `$V -B tools/prove.py --store $S/store --scratch $S/proof --worlds 1 --prefix check-ring --policies D,P0,C --out $S/check.json`
  (about 4 minutes, $0) and `$V -B tools/check_probe.py --store $S/store --scratch $S/probe --out $S/probe.json`
  (about 6 minutes). Delete $S/store afterwards.
- Not done: any model rollout, anything on macOS, the sealer and private store, compute metering (README section 6).

## If the container restarted
- `S=/tmp/claude-0/-home-user/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/vfport; mkdir -p $S;
  pgrep -x dockerd >/dev/null || (nohup dockerd --feature containerd-snapshotter=false > $S/dockerd.log 2>&1 &)`
- images survive in /var/lib/docker only if the disk survives; rebuild with docker/Dockerfile.ring (see its header).
- the instance store under $S/store does NOT survive a scratch wipe: re-run tools/make_instances.py.
