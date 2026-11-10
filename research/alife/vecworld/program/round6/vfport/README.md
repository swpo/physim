# vfport: the PhySim v2 exam as a verifiers environment (round 6)

Round 5's `agentenv` proved the exam with its own sandbox and orchestration. The lead then asked that the grader
use the verifiers library instead of an isolated one of our own (`roadmap/GRADER_VS_VERIFIERS.md`). This folder is
that port: a verifiers taskset run under the STOCK isolated grader (`--env.id isolated-verifier`), a host-side
laboratory, a per-item predictor driver, and a scripted harness that proves the route with no model.

Status, 10 Nov 2026: built and RUN end to end on Docker in the cloud container (Linux x86_64, 4 cores,
Docker 29.9.2) with scripted agents only. No model call, no GPU job, no upload. Nothing was run on a Mac.
Numbers and their sources: `results/summary.json`. Every pilot instance used here is deleted and must never be
reused as an exam.

## 1. Who does what

| Part | verifiers supplies (pinned 0.3.2.dev163, commit a24f5e21) | Ours |
|---|---|---|
| Agent's box | Docker container from the task's image, no host mounts; `network_allow=[]` leaves the model route and the tool URLs as the only ways out (iptables in the box's network namespace plus an HTTP proxy in the worker) | The image (`docker/Dockerfile.ring`); `Physim2Task.setup` writes TASK.md, the public `physim2` package and an empty `submission/`; two guards refuse any other placement |
| Laboratory | A Toolset runs as a host process of the worker, one per rollout, reached from the box through the proxy; the task row reaches it over a private channel | `lab_tools.LabTools`: one tool, `call`, around round 5's `LabService.handle` (budgets, locking, neutral errors). It loads the instance the row points to, then removes token-like variables from its own process |
| Lab from the agent's Python | The tool URL is handed to the harness only | The task controller writes the URL into the box (`/etc/physim2/lab.json`); `physim2.Lab()` posts MCP `tools/call` over HTTP with the standard library. Same interface as round 5 |
| Collection of the submission | `collect` / `restore` of declared artifacts across boxes, validated on the host | `submission/` declared, not required, cap 64 MiB of file bytes. `Physim2Task.finalize` calls verifiers' `collect` itself inside a try and applies the freeze rules on the worker, so that nothing the agent does to its box can end the rollout ungraded (section 5) |
| Verifier box | A fresh container from the same image and policy; task `setup` reruns there; artifacts restored; `stage_verifier`; network cut; rewards run in the worker with a handle on the box | `setup` detects the verifier phase and stages public files only. `grading.stage` makes everything root-owned and read-only. No submitted code runs in setup or staging |
| Running the predictor | `runtime.run` as root in the box; nothing between items | `public/_item.py`: ONE request in the box at a time; the predictor runs as uid 1000 under CPU, memory, file-size and process limits; after each item root kills that user's processes (and reaps them), removes its System V objects and deletes every file it owns. Port of v1's worker and launcher plus the cleanup |
| Scoring | The `@vf.reward` hook | Round 5's arithmetic by import (`FrozenExam.request/score/references`, `check_shapes`, failed item = K, `acceptance.skill`). Truths never enter a box. The reward never raises: any failure is scored as K and recorded |
| Reference table, sigma, rho | Per-rollout rewards in `traces.jsonl` | `evaluator.grader.table` (round 5, unchanged) on the per-item scores the reward saves in the worker's store; `tools/prove.py` |
| Records | `traces.jsonl` per run; state is not saved; upload is ON by default | The row holds an instance id and the public commitment of the secret, never a hidden value. Tools set `push = false`, `PRIME_RUNS_MODE=disabled` and drop `PRIME_API_KEY` |
| Scripted agent | Not provided | `physim2_script`: runs one script in the agent's box, exactly where a model's shell commands run |
| Sealed store | Not provided | NOT BUILT (out of scope): `store.py` reads a local directory; the sealer replaces `hidden_dir` |

## 2. Files

```
physim2_env/            the taskset package (--env.taskset.id physim2-env)
  taskset.py            Physim2Data (pointers only), Physim2Task (guards, setup, finalize, stage_verifier, reward), Physim2Taskset
  lab_tools.py          the laboratory Toolset: one tool `call`; VfLabService = LabService with _check replaced
  access.py             worker-side channel laboratory -> task controller: announce the address, freeze the submission
  bundle.py             the workspace from PUBLIC inputs: round 5's build_workspace.build, then the transport swap
  grading.py            the item loop of the reward; staging of the verifier box; box CPU counter
  store.py              instance store on the worker; token-like names; environment scrub
  public/               files copied into both boxes as part of physim2: labclient.py (HTTP), validate.py,
                        _item.py (the one-request driver), _rules.py (freeze rules, reply parsing)
physim2_script/         the scripted harness (--env.agent.harness.id physim2-script)
agents/                 install_prebuilt.py (evaluator-only reference C), probe_grading.py, hostile_submission.py
tools/                  make_instances.py, vfrun.py (drives vf-eval), prove.py, check_probe.py, make_summary.py,
                        docker_shim/docker (only for hosts without IPv6)
docker/                 Dockerfile.ring (the one image of both boxes), Dockerfile.network (proxy-bound hosts only)
configs/                scripted_ring.toml, qwen_ring_bash.toml
results/                proof_ring.json, probe_ring.json, gliders_smoke_D.json, summary.json
RUNBOOK_MAC.md          install, scripted smoke test, one cheap model rollout
```

Round 5's code is reused BY IMPORT from `../../round5/agentenv` (set `PHYSIM2_AGENTENV` to point elsewhere), so the
package is installed from a checkout, not from a wheel. Of agentenv's 3,670 lines outside `results/`:
- **dropped from the route, 763 lines** (memo: about 760): `sandbox.py` 139, `run_rollout.py` 230, the socket server
  66, `wire.py` 55 and the socket `labclient.py` 114, `mac/` 49, `tests_tcp.py` 45, snapshot and `run_request` 65.
  The files stay in round 5 untouched; `sandbox.py` and `run_request` are used once more, as the reference grader
  of the cross-check in section 4.1.
- **wrapped, 533 lines** (memo: about 530): `LabService` 185 (subclassed, `_check` replaced: 20 lines),
  `build_workspace.py` 112 (called by `bundle.py`), the grading loop 31 (redone item by item in `grading.py`),
  `prove.py` 97 and `check_probe.py` 108 (redone through `vf-eval` in `tools/`).
- **kept by import, 2,374 lines** (memo: about 2,370). Copied: 32 lines (`evaluator/submission.py:94-125`, into
  `public/validate.py`, which must exist inside the box). Nothing else is copied.
- **new here, 3,246 lines** (memo's estimate: about 750 including a sealer, of which 60 for the harness): package
  1,854 (783 of them the four public in-box files, 107 the harness), tools 948, agents 291, Dockerfiles, configs
  and pyproject 153. Source: `results/summary.json: code`.

## 3. Run it (cloud container; the Mac: RUNBOOK_MAC.md)

```sh
S=<scratch>; V=/home/user/evalwork/vfport/.venv/bin
pgrep -x dockerd >/dev/null || (nohup dockerd --feature containerd-snapshotter=false > $S/dockerd.log 2>&1 &)
cp /root/.ccr/ca-bundle.crt docker/extra-ca.crt      # session proxy CA; an empty file elsewhere
docker build --network host --build-arg HTTPS_PROXY=$HTTPS_PROXY -f docker/Dockerfile.ring -t physim2-ring:1 docker/
docker build --network host --build-arg HTTPS_PROXY=$HTTPS_PROXY -f docker/Dockerfile.network -t localhost/verifiers-network:1 docker/
$V/python -B tools/prove.py --store $S/store --scratch $S/proof --worlds 4 --prefix proof-ring --out results/proof_ring.json
$V/python -B tools/check_probe.py --store $S/store --scratch $S/probe --out results/probe_ring.json
$V/python -B tools/make_summary.py
rm -rf $S/store $S/proof $S/probe                    # the store holds the hidden instances
```

One rollout by hand: `PHYSIM2_STORE=$S/store vf-eval @ configs/scripted_ring.toml --no-rich`.

## 4. What was proven

Everything in this section was run in the cloud container. Sources are files of `results/` unless marked. The
proof ran on the package code of commit f12158bb0; the probes and the gliders rollout on the final code, which
differs by one branch of the reward that no run took (`summary.json: code_versions`).

### 4.1 The ring table (`proof_ring.json`; round 5: `round5/agentenv/results/proof_ring.json`)

4 fresh hidden worlds, 256 items, R 16, a budget of 400 ticks (8 episodes), 512 training episodes: round 5's
sizes. Six policies per world; all 24 rollouts went through `vf-eval physim2-env --env.id isolated-verifier` on
Docker and were graded, with 0 failed items of 1,536 (`all_graded`, `n_failed_items_total`). S, D, P0, the
prior-mean policy and the null agent are round 5's `reference_agent.py`, unmodified, run in the agent's box. C
needs the true parameters: its submission is built on the worker and installed from the agent's box
(`agents/install_prebuilt.py`), so no hidden value is on a command line or in a trace.

Skill is `(L(K) - L) / (L(K) - L(C))` (`pooled.policies[p].vs_C`; `pooled.acceptance`).

| run | S | P0 | prior mean | D at budget | null agent | O | sigma | rho |
|---|---|---|---|---|---|---|---|---|
| this study | 0.979 | 0.863 | 0.846 | 0.394 | -0.043 | 1.086 | 0.137 (SE 0.064 over worlds) | 0.85 (SE 0.05) |
| round 5 | 0.988 | 0.964 | 0.970 | 0.343 | 0.008 | 1.083 | 0.036 (SE 0.009) | 0.67 (SE 0.38) |
| z | -0.70 | -1.12 | -1.03 | -0.25 | -1.21 | 0.44 | | |

- **Not the same numbers, and they cannot be:** each run draws its own secrets and hidden parameters at run time,
  and round 5 deleted its instances. z compares the means over the 4 worlds of each run (difference over its
  standard error, `summary.json: ring_table.policies[p].z`): no policy differs by more than 1.3 standard errors.
  The gap in P0, the prior-mean policy and sigma comes from one of our four worlds (w1), where the prior-trained
  predictors reach 0.73 and 0.68 of C; in the other three they reach 0.94 to 0.99 (`per_world[w].table`).
- **The arithmetic is the same to the last bit.** The frozen C submission of each world, graded once more by
  round 5's own grader (`evaluator.grader.grade`, agentenv's local sandbox on the worker), gives per-item scores
  identical to this route's: 4 worlds x 64 items x 7 cells, maximum absolute difference 0.0
  (`per_world[w].same_submission_through_round5_grader`).
- The reward on the trace (`rewards.skill`, skill on the K-to-O scale) equals the table's `vs_O` for the same
  world and policy in all 24 rollouts (`summary.json: ring_table.reward_equals_table`).

### 4.2 Round 5's boundary checks (`probe_ring.json`; round 5: 34 of 34)

Round 5's `probe_agent.py`, unmodified, in the agent's box: **32 of the 34 checks reproduced, 0 failed, 2 do not
carry over by design** (section 5, item 10). The four predictor checks (unprivileged, no hidden file, no network,
cannot write the submission) hold twice: during validation in the agent's box and at grading in the verifier box.

### 4.3 The new probes (`probe_ring.json: checks_new`, 37 of 37; each with its evidence)

- **(a) Nothing survives from one item to the next.** A predictor that leaves three files, a System V
  shared-memory segment and a background process at every item found none of them at any of the 8 items; the
  cleanup removed 1 process, 4 files and 1 segment after every item (`evidence.a_cleanup_per_item`). Control,
  same predictor with the cleanup switched off: at item 2 it finds all three files, the segment and the process.
- **(b) No canary, no hidden value.** With `HF_TOKEN=<canary>` in the worker's environment: the laboratory process
  inherited it (with 8 other token-like variables of this machine) and dropped all of them after loading; a
  script that read the environment and every readable file found no canary in the agent's box (8,412 files) or
  in the verifier box (about 5,000 files at each item; uid 1000 can read only its own `/proc/<pid>/environ`).
  No token-like variable name exists in either box. The saved runs (traces, configs, logs, notes: 192 files with
  the proof's) contain neither the canary nor the secret or a hidden parameter of any of the 6 instances
  (`summary.json: hidden_value_scan`).
- **(c) Network.** Control: a container of the same image without the policy reaches a listener on the host.
  From the agent's box and from the verifier box that listener, a public address and DNS are unreachable, and
  the listener saw no connection. The agent's box reaches the laboratory (the declared route) and its HTTP proxy
  answers 403 for anything else; the verifier box cannot reach the laboratory's address either. Caveat: in this
  cloud container public addresses are unreachable from ANY container, so "no public route" is not informative
  here; the host listener and the proxy refusals are.
- **(d) No ungraded rollout.** Seven hostile agents (delete `submission/`, leave it empty, pad beyond the cap, pad
  beyond the transport budget, remove `tar`, add symbolic links, fill `/logs/artifacts`): all graded; K where no
  usable predictor exists, a normal grade where links or junk are simply left out. Control with verifiers'
  default collection: only the deleted submission is graded; four of the others end without a reward.
- **Operator guards:** the laboratory refuses a colocated, url or sandbox placement; setup refuses an open
  network, a non-container runtime, a token-like variable in the harness environment, and (with `single_use`) an
  instance whose laboratory was opened before.

### 4.4 Cost per rollout (`proof_ring.json: rollout_cost`, 24 rollouts, boxes capped at 2 cores)

- Wall: mean 51 s, maximum 57 s: boot 0.6 s, setup 6.4 s, agent 2 to 11 s, finalize 0.1 s, verifier phase 37 s
  (64 items, one request each: 0.58 s per item including the cleanup). Round 5's whole proof took 512 s, this
  one 1,410 s.
- CPU: agent box 7.5 s, verifier box 26.9 s (cgroup counters of the containers; 0.22 s inside the predictor per
  item), `vf-eval` with its children (laboratory, docker CLI) 15.5 s per rollout.

### 4.5 The memo's unknowns

1. **Host-side laboratory under isolated-verifier:** settled, it works. Setup does rerun in the verifier box; ours
   then stages public files only. The pass criteria of the memo are met as far as they can be (table within
   noise and arithmetic identical; 32 of 34 checks plus the per-item cleanup check).
2. **Laboratory from the agent's Python:** settled for scripts (every reference policy used `physim2.Lab()` from
   the box; a stateless JSON-RPC `tools/call` needs no MCP session). Not settled for a model under a stock
   harness: no model was called.
3. **Token or answer leak:** settled for a canary in the worker's environment and a local store. The memo's test
   with a private repository was not run: there is no sealer or private store yet.
4. **Network cut on macOS Docker:** NOT settled; this is Linux. RUNBOOK_MAC.md, step 2.
5. **CPU metering:** not studied. The cgroup CPU counter is readable from both boxes here (cgroup v1) and is
   what section 4.4 reports.

## 5. Where the code contradicted the memo, and what else turned up

1. **"This cloud container has no Docker daemon" (memo section 3).** The binaries are installed and the daemon
   starts; everything above ran here.
2. **Hole 3's fix is not sufficient.** The memo proposes `Artifact(required=False)` so that deleting
   `submission/` cannot fail the rollout. Run with verifiers' default collection (control,
   `results/probe_ring.json: evidence.d_control_default_collection`): a deleted submission is graded (K), but four
   other agent actions still end the rollout WITHOUT a grade: padding beyond the transport budget (`SandboxError`
   from `Runtime.read`, verifiers/v1/runtimes/base.py:327-340), removing the box's `tar` (`TaskError`), an
   absolute symbolic link inside `submission/` (`EnvError`: `restore` refuses it in the verifier stage,
   utils/artifacts.py:269-275), and junk in `/logs/artifacts`, which verifiers sweeps first against the same
   budget (utils/artifacts.py:63-79). The agent is root in its box, so in-box sanitising cannot be trusted
   either. Fix here: `finalize` runs verifiers' own `collect` (no sweep) inside a try, applies the freeze rules on
   the worker and fills `trace.state.artifacts` itself, which makes verifiers skip its collection
   (rollout.py:501). All seven hostile agents are then graded (K where there is no usable predictor).
   What this does NOT cover: a harness that dies (a model can kill its own harness process). By reading
   (rollout.py:417-426 and 490; not run), verifiers then skips finalize and scoring and that rollout has no
   reward. The operator rule stays: no retries, no resume, an ungraded rollout counts as K
   (`tools/vfrun.py: rollout`).
3. **Hole 1's fix as written leaves a channel.** "Root kills that user's processes" is not enough when the box's
   init never waits: a killed process stays a zombie whose pid, uid and 15-character name remain readable by the
   next item. The first probe run showed exactly this (the cleanup reported a process it could not remove). The
   driver now makes itself the subreaper and reaps what it kills. Also, root in a Docker container may not
   remove another user's System V shared memory (no CAP_SYS_ADMIN): the removal is issued as that user.
4. **Hole 5's fix as written leaves the value readable.** Deleting a variable from `os.environ` does not change
   `/proc/<pid>/environ`. `store.scrub_environment` also overwrites the kernel-visible block; the laboratory
   records that no value is left (`evidence.b_lab_process.token_values_left_in_environ: false`).
5. **Unknown 2, how the agent's Python finds the laboratory.** The memo expected the URL on the harness command
   line. On Linux Docker the URL is `http://127.0.0.1:<port>/.vf-host/<32-byte token>/mcp`, known only after the
   tool server is up, which is after task setup; reading it from another program's command line is
   harness-specific. Here the laboratory process announces its port to the task controller, which writes the
   same translated URL into the box. The scripted harness checks it equals the URL verifiers handed to it
   (`address_file_matches_tool_url: true` in every rollout).
6. **`--sysctl net.ipv6.conf.all.disable_ipv6=1`** (verifiers/v1/runtimes/docker/__init__.py:221-222) makes
   `docker run` fail on a kernel without IPv6, as here: "open sysctl net.ipv6.conf.all.disable_ipv6 file:
   unsafe procfs detected ... no such file or directory". `tools/docker_shim/docker` drops that one option on such
   hosts only. The iptables cut itself is verifiers' own and works here.
7. **`docker exec` ran with umask 0 here**, so files written through `Runtime.write` and `mkdir -p` were
   world-writable in the boxes (the predictor's user could have written into `/runtime`). Setup and staging now
   set modes explicitly, the driver's `--scan` removes any world-writable bit left outside sticky temporary
   directories, and the probe checks the predictor cannot write its request, `/runtime`, the workspace or the
   submission.
8. **"python:3.12-slim plus numpy is enough for the ring world" (task brief).** The public ring module imports the
   vw library, which imports jax and scipy (`agentenv/physim2/world_ring.py:25-29`, `vw1/vw/certificates.py:35`).
   The image carries numpy, scipy and jax; with jaxlib stripped of its symbol tables and the classic Docker
   image store it stays under the 600 MB budget.
9. **Validation moved into the agent's box** (the memo's first option): `lab.validate` runs the public driver on
   the two public examples; the laboratory only counts the attempt. `lab.submit` asks the worker to collect and
   freeze `submission/` at that moment, so "only the frozen directory is graded" still holds.
10. **Two of round 5's 34 checks do not carry over, by design:** the agent is root inside its own container (round
    5: uid 65534 on the evaluator's machine) and may write anywhere in it. What it cannot reach is anything
    outside the box.
11. **A saved trace names the operator.** Besides the task row and `harness.env` (memo table), every trace
    records the agent's client settings: base URL, the NAME of the key variable and a team-id header taken from
    the worker's Prime configuration, even when no model is called. No secret, but scrub it before a trace
    leaves the worker. The runs' traces of this study were kept in scratch and deleted; `results/` holds none.

## 6. Not done

- No model rollout: the stock harnesses (`bash`, `claude_code`, `codex`) were not run. The stop hook
  `Physim2Task.frozen` (end the rollout at the next model call after a submit) has therefore never fired.
- Nothing on macOS: the network cut there uses a different path (memo unknown 4). RUNBOOK_MAC.md, step 2.
- No sealer, no private Hugging Face store, no hash check of downloaded data (memo holes 5 and 6 only as far as a
  local store goes). No compute-budget metering (the cgroup CPU counter of each box is read and reported, nothing
  is enforced). Gliders: the smoke config loads, and ONE scripted rollout (policy D) ran
  through the same route and the same image on one fresh gliders world: graded, 0 failed of 8 items, 132 lab
  ticks, 71 s of wall for the rollout after 338 s to build the instance (`results/gliders_smoke_D.json`). Nothing
  else was run on gliders: no S, P0 or C, no dry-run or exam size.
- Prime sandboxes: not run. The guards accept `prime`; the laboratory URL would be a public tunnel there (memo
  hole 7).
- Laboratory reply times are not padded (memo hole 7).
- `single_use` (refuse an instance whose laboratory was opened before) exists and is off; it was not exercised.
- The store is a plain directory readable by the worker's user; per-item scores, laboratory logs and predictor
  error text stay there and never enter a trace.

## 7. Rules for a sealed run (operator)

`--env.id isolated-verifier`, a Docker runtime, `push = false` (or `PRIME_RUNS_MODE=disabled`), no `--resume`,
`max_retries = 0` for the agent and the episode, `single_use = true`, no token-like variable in `harness.env`,
`forward_env` or `--env.verifier.env` (setup refuses them), `item_cleanup` and `stock_collection` left at their
defaults (a rollout run otherwise is marked `NOT_AN_EXAM` in its trace), a rollout without a reward counts as K.
