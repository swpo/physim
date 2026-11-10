# vfport: PROGRESS

## FIXER (role after the builder, the specification review and the red team) -- 10 Nov 2026

Worktree `/home/user/wt/vfportfix` (branch wt-vfportfix, pushes to `claude/fisim-agent-world-research-hepmlz`).
Scratch `/tmp/claude-0/-home-user/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/vfport/fix/`. Venv: the builder's
`/home/user/evalwork/vfport/.venv`. Docker daemon was found running (classic image store), images kept.

### INCIDENT (10 Nov 2026, about 04:31-04:34 UTC) -- read this first
- What ran: the first version of my `tools/check_units.py` started `physim2_env/public/_item.py` (the one-request
  driver) as root ON THE HOST of this cloud container, outside any container.
- What it did: the driver's cleanup did there what it does in a box: SIGKILL to every process of uid 1000 and deletion
  of every file owned by uid 1000 on the writable file systems (/ and /var/lib/docker).
- Known loss: `/home/ubuntu` (home of the unused default account; recreated from /etc/skel, earlier content unknown).
  Coordinator's check: no tracked file missing in the checkouts and worktrees, the Python environments import.
- Reported on the coordinator's channel at 04:34:53. Fix (commit 7e034be18): `require_box(uid)` in the driver
  (marker /etc/physim2/predictor_uid + container evidence + PHYSIM2_BOX_CLEANUP=disposable-box + the box's own uid,
  never 0); `require_container(runtime)` before every runtime command; the real cleanup is tested only inside a
  throwaway container (`tools/check_driver.py`); on the host only refusals are tested, under tripwires
  (`tools/check_units.py`, checks `guard_*`). RUNBOOK_MAC.md is on HOLD until the coordinator's independent audit.

### Done (code; package final at commit 743f6b75e)
- S1: `_rules.freeze` refuses duplicate members, file/directory collisions, paths over 1024 bytes, more than 20,000
  members; skips names with control characters or undecodable bytes; `finalize` runs verifiers' `_validate_restore`
  inside its try. Hostile agents tar_duplicate, tar_collision, tar_longpath.
- S2 = R2: `item_isolation = "box"` (default): one fresh container per exam item through verifiers'
  `provision_runtime` with the verifier box's config (`grading.fresh_box`); `"shared"` = one box, pilot mode, marked
  in the trace. Probe (a2) measures four channels in both modes.
- S3: `grading.validate` (round 5's three example calls) in the verifier box before item 1, invalid = K on every
  item; tool ops validate/submit run the public validator in the agent's box through the controller
  (`access.BoxAccess.check`), a failed submit freezes nothing.
- R1, R5: `_rules.read_reply` strict (float32, level<l> members only, at most 16, bounded numbers, no allocation from
  a declared size); a non-finite score is a failed item; the reward is always a finite number.
- R3: the driver reads reply and error text through a directory handle, O_NOFOLLOW | O_NONBLOCK, regular files only;
  worker-side timeout per request.
- R4: `single_use` on by default, keyed by `agent_key` (default "<model>|<harness id>"); `tools/settle.py`.
- R6: random predictor uid per rollout (20000-59999). R9: malformed inputs are format rejections, a rejected
  experiment charges nothing; the final collection respects the submission cap.
- S4: `results/proof_ring_items.npz` + `tools/recompute_table.py`. S6: single_use default. S7: the agent box CPU
  counter is renamed `agent_box_cpu_s_unverified`. S8: allow-list for variables entering a box. S9: runbook.

### Results (all on the package code of commit 743f6b75e; `results/summary.json` names every source)
- `tools/check_units.py`: 67 of 67 (the builder's code: 25 of 46). `tools/check_driver.py` (in a container): 19 of 19.
- `tools/check_probe.py` (05:07-05:22, one more rollout at 06:03): round 5's 34 checks: 32 reproduced, 0 failed, 2
  changed by design; 63 of 63 new checks; 37 rollouts, 963 s.
- `tools/prove.py --worlds 4` (05:22-05:54, aggregation at 06:10): 24 rollouts graded, 0 failed items of 1,536;
  S 0.984, P0 0.930, PM 0.916, D 0.210, null -0.046, O 1.096 (of C); sigma 0.070, rho 0.776; C through round 5's
  grader identical in 4 of 4 worlds; C and D with one box per item identical to one box (2.6 s per item box).
  The tool was started three times: the first run ended in an exception in its aggregation step after every
  rollout was done (a key I had renamed); no rollout was repeated; wall time added from the logs (1,973 s).
- `tools/recompute_table.py`: 26 numbers, maximum difference 0. Gliders smoke (D, one box per item): graded, 0 of 8
  failed. Red team's attacks again: overflow and fifo graded as K in 24 s and 23 s; hostile-exit1 still without a
  reward on the trace (open hole 2; `tools/settle.py`).

### Running
- nothing. Docker daemon up (classic image store), images kept for the host-safety audit: physim2-ring:1,
  localhost/verifiers-network:1, python:3.12-slim (573 MB in all). No container. Scratch stores with the hidden pilot
  instances deleted; only logs are left in `<scratch>/`.

### Next step (exact)
- Coordinator: the independent host-safety audit (task 35) of this folder, then release RUNBOOK_MAC.md to the Mac.
  The audit can repeat the checks with: `V=/home/user/evalwork/vfport/.venv/bin/python; cd` to this folder;
  `PYTHONPATH=$PWD $V -B tools/check_driver.py --out /tmp/claude-0/.../driver.json` (container only) and
  `PYTHONPATH=$PWD PHYSIM2_DEV_MACHINE=cloud-container $V -B tools/check_units.py --out /tmp/claude-0/.../units.json`
  (host: refusals under tripwires; it starts test predictors, never the cleanup).
- Open holes and decisions for the lead: README section 6.

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
