# vfport: the PhySim v2 exam as a verifiers environment (round 6)

Round 5's `agentenv` proved the exam with its own sandbox and orchestration. The lead then asked that the grader
use the verifiers library instead of an isolated one of our own (`roadmap/GRADER_VS_VERIFIERS.md`). This folder is
that port: a verifiers taskset run under the STOCK isolated grader (`--env.id isolated-verifier`), a host-side
laboratory, a per-item predictor driver, and a scripted harness that proves the route with no model.

Status, 10 Nov 2026: built by one agent, reviewed by two (a specification review and a red team, `redteam/`), then
fixed by a fourth; this file describes the code after the fixes. Everything was RUN end to end on Docker in the
cloud container (Linux x86_64, 4 cores, Docker 29.9.2) with scripted agents only. No model call, no GPU job, no
upload. **Nothing was run on a Mac.** Numbers and their sources: `results/summary.json`. Every pilot instance used
here is deleted and must never be reused as an exam.

Read section 8 before running anything from this folder on a machine you care about.

## 1. Who does what

| Part | verifiers supplies (pinned 0.3.2.dev163, commit a24f5e21) | Ours |
|---|---|---|
| Agent's box | Docker container from the task's image, no host mounts; `network_allow=[]` leaves the model route and the tool URLs as the only ways out (iptables in the box's network namespace plus an HTTP proxy in the worker) | The image (`docker/Dockerfile.ring`); `Physim2Task.setup` writes TASK.md, the public `physim2` package and an empty `submission/`; guards refuse any other placement, an open network, a non-container runtime, and any variable for a box that is not on an allow-list |
| Laboratory | A Toolset runs as a host process of the worker, one per rollout, reached from the box through the proxy; the task row reaches it over a private channel | `lab_tools.LabTools`: one tool, `call`, around round 5's `LabService.handle` (budgets, locking, neutral errors), with malformed requests rejected before anything runs or is charged. It loads the instance the row points to, then removes token-like variables from its own process |
| Lab from the agent's Python | The tool URL is handed to the harness only | The task controller writes the URL into the box (`/etc/physim2/lab.json`); `physim2.Lab()` posts MCP `tools/call` over HTTP with the standard library. Same interface as round 5 |
| Validate and submit | Nothing | The tool operations `validate` and `submit` make the task controller run the public validator in the agent's box (`access.BoxAccess.check`); a submit whose check fails freezes nothing and leaves the laboratory open (round 5's behaviour). That report comes from a box where the agent is root, so it is feedback for the agent only: the grader validates again (below) |
| Collection of the submission | `collect` / `restore` of declared artifacts across boxes, validated on the host | `submission/` declared, not required, cap 64 MiB of file bytes. `Physim2Task.finalize` calls verifiers' `collect` itself inside a try, applies the freeze rules on the worker (`public/_rules.py`: regular files only; an archive with duplicate members, a path that is both file and directory, or over-long paths is refused) and then verifiers' own restore check, so that nothing the agent does to its box can end the rollout ungraded |
| Verifier box | A fresh container from the same image and policy; task `setup` reruns there; artifacts restored; `stage_verifier`; network cut; rewards run in the worker with a handle on the box | `setup` detects the verifier phase and stages public files only. `grading.stage` makes everything root-owned and read-only and writes the box marker. The three public example calls of round 5 run HERE first (`grading.validate`); a predictor that fails one is K on every item. No submitted code runs in setup or staging |
| One box per exam item | `provision_runtime`: a new container with the same resolved config and network policy, removed afterwards | `grading.fresh_box` (default, `item_isolation = "box"`): the reward provisions one box per item, stages it like the verifier box, cuts its network, runs ONE request, destroys it. `"shared"` runs all items in the verifier box with the driver's cleanup in between (pilot mode; section 5, finding S2) |
| Running the predictor | `runtime.run` as root in the box | `public/_item.py`: ONE request per call; the predictor runs as an unprivileged user (a random uid per rollout) under CPU, memory, file-size and process limits; root reads the reply through a directory handle, never follows a link, never blocks; afterwards root kills that user's processes and deletes its files. The cleanup refuses to run anywhere but in a prepared box (section 8) |
| Scoring | The `@vf.reward` hook | Round 5's arithmetic by import (`FrozenExam.request/score/references`, `check_shapes`, failed item = K, `acceptance.skill`). A reply must be what `predict_runner.py` writes (float32, one array per level); an item whose score is not finite is a failed item; the reward is always a finite number. Truths never enter a box. The reward never raises: any failure is scored as K and recorded |
| Reference table, sigma, rho | Per-rollout rewards in `traces.jsonl` | `evaluator.grader.table` (round 5, unchanged) on the per-item scores the reward saves in the worker's store; `tools/prove.py`; `tools/recompute_table.py` (numpy only, from the committed per-item scores) |
| One budget per agent | Nothing (a rerun gets a fresh tool server) | `single_use` (on by default): the same agent, named by `agent_key` (default `<model>|<harness id>`), cannot open an instance twice. `tools/settle.py` records K for a rollout verifiers left without a reward |
| Records | `traces.jsonl` per run; state is not saved; upload is ON by default | The row holds an instance id and the public commitment of the secret, never a hidden value. Tools set `push = false`, `PRIME_RUNS_MODE=disabled` and drop `PRIME_API_KEY` |
| Scripted agent | Not provided | `physim2_script`: runs one script in the agent's box, exactly where a model's shell commands run |
| Sealed store | Not provided | NOT BUILT (out of scope): `store.py` reads a local directory; the sealer replaces `hidden_dir` |

## 2. Files

```
physim2_env/            the taskset package (--env.taskset.id physim2-env)
  taskset.py            Physim2Data (pointers only), Physim2Task (guards, setup, finalize, stage_verifier, reward), Physim2Taskset
  lab_tools.py          the laboratory Toolset: one tool `call`; VfLabService = LabService with _check, advance, experiment wrapped
  access.py             worker-side channel laboratory -> task controller: announce the address, run the validator, freeze
  bundle.py             the workspace from PUBLIC inputs: round 5's build_workspace.build, then the transport swap
  grading.py            validation, the item loop (one box per item, or one box), staging, the container-runtime check
  store.py              instance store on the worker; token-like names; environment scrub
  public/               files copied into every box as part of physim2: labclient.py (HTTP), validate.py,
                        _item.py (the one-request driver and its box guard), _rules.py (freeze rules, reply reader)
physim2_script/         the scripted harness (--env.agent.harness.id physim2-script)
agents/                 install_prebuilt.py (evaluator-only references), probe_grading.py, hostile_submission.py (21 modes)
tools/                  make_instances.py, vfrun.py (drives vf-eval), prove.py, check_probe.py, settle.py, recompute_table.py,
                        make_summary.py, check_driver.py (container only), check_units.py (build container only),
                        docker_shim/docker (only for hosts without IPv6)
redteam/                the red team's attack scripts and results, kept; three attacks run again after the fixes (*-after-fix.json)
docker/                 Dockerfile.ring (the one image of every box), Dockerfile.network (proxy-bound hosts only)
configs/                scripted_ring.toml, qwen_ring_bash.toml
results/                proof_ring.json + proof_ring_items.npz, recomputed_table.json, probe_ring.json, units.json,
                        units_before_fix.json, driver_container.json, gliders_smoke_D.json, summary.json
RUNBOOK_MAC.md          install, scripted smoke test, one cheap model rollout (ON HOLD until the host-safety audit)
```

Round 5's code is reused BY IMPORT from `../../round5/agentenv` (set `PHYSIM2_AGENTENV` to point elsewhere), so the
package is installed from a checkout, not from a wheel. Of agentenv's 3,670 lines outside `results/`: 763 are no
longer on the route, 533 are wrapped, 2,374 are kept by import (32 of them copied verbatim into
`public/validate.py`). New here: 5,230 lines (package 2,495, tools 2,061, agents 516,
build and config 158; `results/summary.json: code`). The memo estimated about 750 including a sealer.

## 3. Run it (cloud container; the Mac: RUNBOOK_MAC.md)

```sh
S=<scratch>; V=/home/user/evalwork/vfport/.venv/bin/python; export PYTHONPATH=$PWD OMP_NUM_THREADS=1
pgrep -x dockerd >/dev/null || (nohup dockerd --feature containerd-snapshotter=false > $S/dockerd.log 2>&1 &)
cp /root/.ccr/ca-bundle.crt docker/extra-ca.crt      # session proxy CA; an empty file elsewhere
docker build --network host --build-arg HTTPS_PROXY=$HTTPS_PROXY -f docker/Dockerfile.ring -t physim2-ring:1 docker/
docker build --network host --build-arg HTTPS_PROXY=$HTTPS_PROXY -f docker/Dockerfile.network -t localhost/verifiers-network:1 docker/
$V -B tools/check_driver.py --out results/driver_container.json                    # the cleanup and its guard, inside a container
PHYSIM2_DEV_MACHINE=cloud-container $V -B tools/check_units.py --store $S/store --instance <any ring instance> --out results/units.json
$V -B tools/check_probe.py --store $S/store --scratch $S/probe --out results/probe_ring.json
$V -B tools/prove.py --store $S/store --scratch $S/proof --worlds 4 --prefix proof-ring --out results/proof_ring.json
$V -B tools/recompute_table.py --out results/recomputed_table.json
$V -B tools/make_summary.py --store $S/store --scratch $S
```

Afterwards delete the store by its full path (it holds the hidden instances). One rollout by hand:
`PHYSIM2_STORE=$S/store vf-eval @ configs/scripted_ring.toml --no-rich -o $S/single`.

## 4. What was proven

Everything in this section was run in the cloud container with the fixed code (`summary.json: code_versions`).
Sources are files of `results/` unless marked.

### 4.1 The ring table (`proof_ring.json`; round 5: `round5/agentenv/results/proof_ring.json`)

4 fresh hidden worlds, 256 items, R 16, a budget of 400 ticks (8 episodes), 512 training episodes: round 5's
sizes. Six policies per world; all 24 rollouts went through `vf-eval physim2-env --env.id isolated-verifier` on
Docker and were graded, with 0 failed items of 1,536 (`all_graded`, `n_failed_items_total`). S, D, P0, the
prior-mean policy and the null agent are round 5's `reference_agent.py`, unmodified, run in the agent's box. C
needs the true parameters: its submission is built on the worker and installed from the agent's box
(`agents/install_prebuilt.py`), so no hidden value is on a command line or in a trace. The table's rollouts are
graded with all items in one verifier box (`grading_mode`): the reference policies are the evaluator's own.

Skill is `(L(K) - L) / (L(K) - L(C))` (`pooled.policies[p].vs_C`; `pooled.acceptance`).

| run | S | P0 | prior mean | D at budget | null agent | O | sigma | rho |
|---|---|---|---|---|---|---|---|---|
| this run (after the fixes) | 0.984 | 0.930 | 0.916 | 0.210 | -0.046 | 1.096 | 0.070 (SE 0.022 over worlds) | 0.776 (SE 0.163 over worlds) |
| round 5 | 0.988 | 0.964 | 0.970 | 0.343 | 0.008 | 1.083 | 0.036 (SE 0.009 over worlds) | 0.671 (SE 0.380 over worlds) |
| z | -0.57 | -0.95 | -0.73 | -1.63 | -2.02 | 0.87 | | |

- **Not the same numbers, and they cannot be:** each run draws its own secrets and hidden parameters at run time,
  and round 5 and the builder deleted their instances. z compares the means over the 4 worlds of this run and of
  round 5 (difference over its standard error, `summary.json: ring_table.policies[p].z`). The largest |z| is
  2.02, for the null agent (-0.046 here, +0.008 in round 5, -0.043 in the builder's run); D at budget follows
  with -1.63. The null agent uses no laboratory tick (`per_world[w].rollouts.null.lab_ticks_used` is 0) and its
  predictor is built from public simulations only, so its difference lies in the hidden worlds drawn. Seven
  comparisons of 4 worlds against 4: this neither shows a difference nor proves sameness; what proves that the
  arithmetic is the same is the next point.
- **The arithmetic is the same to the last bit.** The frozen C submission of each world, graded once more by
  round 5's own grader (`evaluator.grader.grade`, agentenv's local sandbox on the worker), gives per-item scores
  identical to this route's in 4 of 4 worlds, maximum absolute difference 0
  (`per_world[w].same_submission_through_round5_grader`).
- The reward on the trace equals the table's `vs_O` for the same world and policy in all 24 rollouts (maximum
  difference 0.0e+00, `summary.json: ring_table.reward_equals_table`).
- **The table can be recomputed without the store.** `results/proof_ring_items.npz` holds the per-item, per-cell
  scores; `tools/recompute_table.py` (numpy only) reproduces 26 numbers of the table with a maximum
  difference of 0.0e+00 (`recomputed_table.json`).
- **One box per item gives the same scores as one box for all items.** The frozen C and D submissions of the first
  world, graded again in the default mode (same files, by hash): identical per-item scores for both, maximum
  difference 0, 64 item boxes each, 0 infrastructure failures (`one_box_per_item_check_world_0`).

### 4.2 Round 5's boundary checks (`probe_ring.json`; round 5: 34 of 34)

Round 5's `probe_agent.py`, unmodified, in the agent's box: **32 of the 34 checks reproduced, 0
failed, 2 do not carry over by design** (the agent is root inside its own container). The validation checks run in
the agent's box through the tool, as a model would use it; the grader repeats the three example calls itself.

### 4.3 The probes of this port (`probe_ring.json: checks_new`, 63 of 63; each with its evidence)

All probe rollouts use the default grading mode (one box per item) unless said otherwise.

- **(a) Files, processes, shared memory.** A predictor that leaves three files, a System V segment and a background
  process at every item finds none of them at any of the 8 items. Control with the cleanup switched off (one box):
  at item 2 it finds all of them.
- **(a2) The state of a box itself.** The same predictor reads a file of its submission, touches three
  directories, forks 40 to 79 processes and sends 1,200 loopback datagrams at every item, and at every item
  looks for the traces of the item before. With one box per item: no file marked as read, no directory touched,
  loopback counter 0 at every item, process id steps between -3 and 1 (`evidence.a2_channels_one_box_per_item`). With all items
  in one box and the cleanup on: every item after the first sees all four (the read mark, three directories, a
  loopback counter growing by 2,411 per item, a process-id step that follows the number of forks of the item
  before to within 1), which is why that mode is a pilot mode and is marked in the trace
  (`evidence.a2_channels_all_items_in_one_box`).
- **(b) No canary, no hidden value.** With `HF_TOKEN=<canary>` in the worker's environment: the laboratory process
  inherited it and dropped it after loading; a script that read the environment and every readable file found no
  canary in the agent's box or in any item box. No token-like variable name exists in either. The saved runs
  contain neither the canary nor the secret or a hidden parameter (`summary.json: hidden_value_scan`:
  429 files, 0 hits).
- **(c) Network.** Control: a container of the same image without the policy reaches a listener on the host. From
  the agent's box and from every item box that listener, a public address and DNS are unreachable, and the
  listener saw no connection. The agent's box reaches the laboratory and its proxy answers 403 for anything
  else. Caveat: in this cloud container public addresses are unreachable from ANY container.
- **(d) Collection cannot end a rollout ungraded.** Ten hostile agents (delete `submission/`, leave it empty, pad
  beyond the cap, pad beyond the transport budget, remove `tar`, add symbolic links, fill `/logs/artifacts`, and
  three that replace the box's `tar` by a program writing a duplicate member, a file-and-directory collision, a
  5,000-byte path): all graded; K where no usable predictor exists. Control with verifiers' default collection:
  5 of 6 end without a reward.
- **(e) The trusted side validates.** A broken predictor submitted through the raw tool is refused and the
  laboratory stays open. A predictor whose samples change from call to call, submitted from a box whose
  validator was replaced by one that always passes: accepted there, K on every item at grading ("validation
  failed (reproducibility)"). The same predictor never submitted, and one that fails only the third example
  call: K on every item. A valid predictor left behind after all 16 submission attempts were spent on a broken
  one is not collected (round 5 counted the final collection as an attempt): K.
- **(f) What the predictor returns.** On exam items only (it behaves on the public examples): a float64 reply
  whose score overflows, a named pipe left as `stderr.txt`, a reply of 3,000 members: every item failed, K, a
  finite reward, grading time 24/24/25 s for 8 items. The largest float32 values are a valid reply: graded,
  reward -4.08e+38 (section 6, hole 5).
- **(h) A harness that dies.** Exit status 1 and `kill -9 -1`: verifiers records `HarnessError` and runs neither
  finalize nor the reward. `tools/settle.py` then writes the K record, and the same agent's second opening of the
  instance is refused.
- **Operator guards:** the laboratory refuses a colocated, url or sandbox placement; setup refuses an open
  network, a non-container runtime, `HF_TOKEN` and `GITHUB_PAT` in the harness environment (anything not on the
  allow-list), and the same agent twice.

### 4.4 Offline checks and the red team's attacks again

- `units.json`: 67 of 67 offline checks pass on the fixed code; the same script on the builder's code passes
  25 of 46 (`units_before_fix.json`: the failures are the reviews' findings reproduced: freeze, reply
  reader, laboratory requests, the missing guard).
- `driver_container.json`: 19 of 19 checks inside a throwaway container (section 8).
- The red team's own scripts through the route, after the fixes (`redteam/results/*-after-fix.json`, 64 items):
  `overflow`: graded, reward 0.0, 24 s (before: reward null, table +inf); `fifo`: graded, reward 0.0, 23 s (before:
  no reward after 168 s). Both predictors are now refused at submit by the check in the agent's box and fail the
  grader's own validation at example 0, so every item is K; the same attacks on exam items only are probes (f).
  `hostile-exit1`: still no reward on the trace (`HarnessError`), as before: hole 2, settled by `tools/settle.py`
  in probe (h).

### 4.5 Cost per rollout

- One box for all items (`proof_ring.json: rollout_cost`, 24 rollouts, boxes capped at 2 cores): wall mean
  58 s, maximum 63 s; CPU: verifier box 29.2 s, `vf-eval` with its children
  16.3 s per rollout.
- One box per item (`one_box_per_item_check_world_0`): 2.6 s of wall per item box. C, one box at a time: grading
  takes 168 s for 64 items against 40 s in one box; the item boxes use 66 CPU-seconds and `vf-eval` with its
  children (mostly the Docker client) 64 s. D, two boxes at a time: 91 s, 69 and 63 CPU-seconds. So the default
  mode adds about 2 minutes of wall and 2 CPU-minutes per rollout of a 64-item exam on this machine.
- The proof took 1,973 s (round 5's: 512 s), the probes 963 s for 37 rollouts.

### 4.6 The memo's unknowns

1. **Host-side laboratory under isolated-verifier:** settled, it works.
2. **Laboratory from the agent's Python:** settled for scripts. Not settled for a model under a stock harness.
3. **Token or answer leak:** settled for a canary in the worker's environment and a local store. The memo's test
   with a private repository was not run: there is no sealer or private store yet.
4. **Network cut on macOS Docker:** NOT settled; this is Linux. RUNBOOK_MAC.md, step 2.
5. **CPU metering:** not studied. The cgroup CPU counter is readable in every box and is what section 4.5 reports
   for the grading boxes; the agent box's counter is read inside a box where the agent is root and is named
   `agent_box_cpu_s_unverified`.

## 5. The two reviews: every finding, what was found again, what was done

S = specification review, R = red team (`redteam/PROGRESS.md`). "Reproduced" names the run or the file.

| Finding | Severity | Reproduced | Now |
|---|---|---|---|
| S1 an archive with duplicate, colliding or over-long members ends the rollout ungraded | major | yes: `units_before_fix.json` (the builder's freeze emits archives verifiers refuses); `probe_ring.json: stock-tar_duplicate` ungraded | FIXED: freeze refuses them, finalize runs verifiers' restore check; three hostile agents graded as K |
| S2 = R2 state passes between items (access and modification times, process-id counter) | major | yes: `probe_ring.json: evidence.a2_channels_all_items_in_one_box`; also the loopback counter, which neither review listed | FIXED by default: one fresh box per item. The one-box mode keeps the channels and is marked. Residual: section 6, hole 1 |
| S3 the trusted side no longer validates | major | yes, by reading and by `hostile-fake_validator` | FIXED: the three example calls run in the verifier box, invalid = K; a failed submit freezes nothing |
| R1 a float64 reply overflows the score: reward null, table +inf | blocker | yes: `units.json: evidence.score` (448 of 448 scores -inf from the red team's samples) | FIXED: strict reply reader, non-finite score = failed item, reward always finite; `hostile-item_overflow` |
| R3 a named pipe as stderr.txt blocks grading until the timeout | blocker | by the red team's run (`redteam/results/fifo.json`, 168 s); not repeated on the old code | FIXED: `driver_container.json` (returns in under a second), `hostile-item_fifo`, a worker-side timeout per request |
| R4 a harness that dies leaves no grade | major | yes: `probe_ring.json: evidence.h_harness_dies` | MITIGATED, OPEN in verifiers (hole 2): `single_use` on by default, `tools/settle.py` |
| R5 a many-member reply makes the worker hold gigabytes | major | yes: `units_before_fix.json: evidence.reply.many_members` (a reply of 3,000 arrays is accepted and held) | FIXED: at most 16 members named level<l>, bounded numbers |
| R6 one uid for every box: a rollout can starve another's predictor of processes | minor (concurrent rollouts only) | not repeated (the red team's two-container run stands) | FIXED: a random uid per rollout (24 different uids in the proof's 24 rollouts) |
| R7 no process or disk limit in a box | moderate | yes: `probe_ring.json: evidence.verifier_box_staging.box_limits` (`pids_max`: max) | OPEN (hole 3): a setting of the Docker daemon |
| R8 a failed item is K, so failing on purpose is free | minor | yes: `proof_ring.json: failed_item_is_K_counterfactual` | OPEN (hole 4): a rule of round 5; the lead's decision |
| R9 malformed requests answered "infrastructure error"; a rejected experiment costs a reset; attempt caps bind nothing | minor | yes: `units_before_fix.json: evidence.lab` | FIXED (requests, reset, the cap on the final collection); validation is public code, so only tool calls are capped (declared) |
| S4 the table cannot be recomputed from per-item scores | minor | yes | FIXED: `proof_ring_items.npz`, `tools/recompute_table.py` |
| S5 wording | minor | yes | FIXED in this file |
| S6 `single_use` off by default | minor | yes | FIXED: on, keyed by agent |
| S7 the agent box's CPU counter is forgeable | minor | yes, by reading | RENAMED `agent_box_cpu_s_unverified`; no trusted meter (hole 6) |
| S8 the token guard matches names only | minor | by reading (the pattern knows TOKEN, SECRET, KEY and the like, not PAT) | FIXED: allow-list (`guard-other-env` refused) |
| S9 runbook | minor | yes | FIXED: RUNBOOK_MAC.md rewritten |

Nothing was rejected: every finding of both reviews was real. The fixer added one of its own: the incident of
section 8.

## 6. Open holes

Most severe first. Each is confirmed (how is said) and not fixed (why is said).

1. **Host-wide state is visible from every box (major for a sealed exam on a shared kernel; not exploited).** A
   fresh box per item resets everything that belongs to a box. It does not hide what the host's kernel shows every
   container: `/proc/stat` (processes created since boot, context switches), `/proc/loadavg`, `/proc/uptime`,
   the clock. Observed: two fresh containers read `processes` 79 apart. A predictor could, in principle, fork or
   wait at item k so that item k+1 reads a few bits; the channel is noisy, costs wall time and was not built or
   measured here. Docker does not mask these files and verifiers passes no option to do so. Fix: a sandboxed
   runtime for the item boxes (gVisor or a micro-VM) or an upstream option; until then keep sealed exams on a
   machine that does nothing else, which at least removes cover traffic for nothing but the predictor.
2. **A harness that dies ends the rollout without a reward (major; verifiers' behaviour).** No task hook runs after
   a `HarnessError` (verifiers/v1/rollout.py:479, envs/isolated_verifier/env.py:107). Here: `single_use` stops the
   re-roll and `tools/settle.py` records K, but the trace itself stays ungraded, and an operator who forgets to
   settle has no score. Fix: upstream (run finalize and scoring after a harness failure), or an env of our own
   around the stock one, which the lead asked us not to write.
3. **No process limit and no disk quota in any box (moderate; operator setting).** `pids_max` is `max` in every box
   (`probe_ring.json: evidence.verifier_box_staging.box_limits`); verifiers passes cores and memory only. The
   predictor is held to 256 processes and 256 MiB per file by the driver, but may fill the disk with many files
   during one request; the agent, root in its box, has no process limit at all. Not run (shared machine). With
   several rollouts at once on one machine, an agent could also keep 256 processes of uid 1000 alive and make
   the check in ANOTHER agent's box fail (that check runs as uid 1000 in every agent box); grading is not
   affected (a random uid per rollout). Fix: Docker daemon settings on the grading machine (`--default-ulimit`,
   a quota-backed storage driver) or a dedicated VM; one rollout at a time until then.
4. **A failed item is scored as K (minor to moderate; a rule to decide).** Round 5's rule, kept. The upper bound
   of what failing on purpose can gain, had a predictor known exactly the items on which it scores worse than K
   (skill on the K-to-O scale, 256 items): D from 0.192 to 0.360 (93 such items), S from 0.8983 to 0.8985 (1
   item), P0 from 0.8484 to 0.8488 (1 item) (`proof_ring.json: failed_item_is_K_counterfactual`). It matters for
   weak predictors only, and the red team found no rule that picks those items from the request. Alternative for
   the lead: a failed item costs K plus the K-to-O gap of that item.
5. **The reward has no floor (minor; a rule to decide).** The largest float32 values are a valid reply and give a
   reward of -4.08e+38 (`probe_ring.json: hostile-item_extreme`). Only the predictor's own score suffers, but a
   mean over rollouts would be meaningless. Alternative: clip the reward, or bound replies by the level's scale.
6. **No trusted CPU meter for the agent's box, no compute budget (minor; out of scope).** The grading boxes'
   counters are read by our root; the agent box's by a command the agent could replace.
7. **No sealer, no private store, no hash check (out of scope; memo holes 5 and 6).** The store is a plain directory
   readable by the worker's user.
8. **Prime sandboxes: not run.** The laboratory URL would be a public tunnel there (memo hole 7), and the driver's
   container check knows Docker and Podman signs only: on Prime grading would stop at staging with "not
   recognised as a disposable box" until a Prime sign is added.
9. **Laboratory reply times are not padded (memo hole 7).** Not measured.
10. **macOS: nothing run.** The network cut uses another path there; the Mac part of `tools/check_probe.py`
    (listener on 127.0.0.1, `host.docker.internal`) was written without a Mac.
11. **No model rollout.** The stock harnesses were not run; the stop hook `Physim2Task.frozen` has never fired; a
    model's direct use of the tool operations `validate` and `submit` is tested with scripts only.
12. **MCP argument errors show pydantic's wording** (`op` given as a number): public text, no hidden value.

## 7. Rules for a sealed run (operator)

`--env.id isolated-verifier`, a Docker runtime, `push = false` (or `PRIME_RUNS_MODE=disabled`), no `--resume`,
`max_retries = 0` for the agent and the episode, `--env.verifier.retries 0`. Leave at their defaults: `single_use`
(true; every opening is recorded in `<store>/<instance>/hidden/opened/`, and only the operator, by removing that
one file, can let an agent whose rollout died before it started open the instance again), `item_isolation` ("box"), `item_cleanup` and `stock_collection` (a rollout run otherwise is marked
`NOT_AN_EXAM` or `between_item_state` in its trace). Pass no variable into a box that is not on the allow-list
(setup refuses). After the run: `tools/settle.py` on the run directory; a rollout without a reward counts as K
and its instance stays closed for that agent. A dedicated machine with Docker process and disk limits (holes 1
and 3).

## 8. Incident of 10 Nov 2026: the driver's cleanup ran on a host

- **What ran.** While writing `tools/check_units.py`, the fixer started `physim2_env/public/_item.py` as root on
  the cloud container itself, outside any container, 14 times (about 04:31 to 04:34 UTC).
- **What it did.** The driver's cleanup is meant for a disposable box: SIGKILL to every process of the
  predictor's uid and deletion of every file that uid owns on every writable file system. On the host, with the
  default uid 1000, it deleted `/home/ubuntu`, the home directory of the unused default account. It was recreated
  from `/etc/skel`; what it held before is not known. The coordinator found no tracked file missing in the
  checkouts and worktrees; the Python environments import; the Docker images run.
- **Why it could.** The driver decided from `euid == 0` alone. It was written to run in containers and nothing
  told it that it was not in one. The builder's code had the same property (`units_before_fix.json:
  evidence.guard_tripwires`: on that code the functions run).
- **The fix: four conditions, all required** (`_item.require_box`), before any function kills, deletes or changes
  a mode: (1) the marker `/etc/physim2/predictor_uid`, root-owned, which only the environment's setup writes into
  a box; (2) a sign of a container (`/.dockerenv`, `/run/.containerenv`, or the control group of pid 1); (3) the
  variable `PHYSIM2_BOX_CLEANUP=disposable-box`, which only the grading route sets on its own commands; (4) a
  target uid equal to the marker's, at least 1000, not 0 and not the caller's. If the route variable is set and
  the box is not recognised, the driver runs nothing at all. Outside the driver: `grading.require_container`
  refuses to send any command through a non-container runtime (those commands create directories and change
  owners as root); `tools/vfrun.py` replaces a run folder only if it holds nothing but vf-eval's own files;
  `physim2.Lab().submit(path)` replaces `submission/` only inside an exam box.
- **The tests of the fix.** On the host (`units.json`, checks `guard_*`): the guard's decision for each missing
  condition; the guard refuses on this machine; every killing or deleting function, called with the route
  variable set, refuses before touching anything, while `os.kill`, `os.fork`, `os.setuid`, `os.unlink`, `os.chmod`,
  `os.chown` and `shutil.rmtree` are replaced by tripwires, so that a broken guard could still do nothing. Inside
  a throwaway container (`driver_container.json`, 19 of 19): ten ways of missing a condition, each refused with
  canary processes and files of two uids intact; with every condition met the cleanup removes the predictor
  uid's process and files and leaves the other uid's alone.
- **What to take from it.** No tool or test of this folder may run the cleanup on a host; `tools/check_units.py`
  refuses to start outside the build container; RUNBOOK_MAC.md lists every command that removes anything and is
  on hold until an independent audit.

## 9. Where the code contradicted the memo, and what else turned up

1. **"This cloud container has no Docker daemon" (memo section 3).** The binaries are installed and the daemon
   starts; everything above ran here.
2. **Hole 3's fix is not sufficient.** `Artifact(required=False)` grades a deleted submission, but under verifiers'
   default collection padding beyond the transport budget, removing the box's `tar`, a link inside `submission/`,
   junk in `/logs/artifacts` and a hand-made archive still end the rollout without a grade. `finalize` collects
   defensively instead (section 1). A harness that dies is not covered (hole 2).
3. **Hole 1's fix as written leaves channels.** Killing the user's processes leaves zombies visible to later items
   unless they are reaped; root in a container may not remove another user's System V memory; and no cleanup of one
   box resets timestamps, the process-id counter or kernel counters (finding S2). Hence one box per item.
4. **Hole 5's fix as written leaves the value readable** in `/proc/<pid>/environ`; `store.scrub_environment`
   overwrites the block.
5. **Unknown 2.** The laboratory URL exists only after setup and carries a random token; the worker writes it into
   the box.
6. **`--sysctl net.ipv6.conf.all.disable_ipv6=1`** fails on a kernel without IPv6; `tools/docker_shim/docker` drops
   that one option on such hosts only.
7. **`docker exec` ran with umask 0 here**; setup and staging set modes explicitly and the driver's scan removes
   world-writable bits (in a box only).
8. **The image needs jax and scipy**, not numpy alone; it stays under the 600 MB budget.
9. **Two of round 5's 34 checks do not carry over, by design:** the agent is root inside its own container.
10. **A saved trace names the operator** (base URL, the name of the key variable, a team-id header). Scrub it
    before a trace leaves the worker.
11. **The memo's "validate becomes a public script" loses round 5's rule** that only a validated predictor is
    graded, unless the grader repeats the validation (finding S3).

## 10. Not done

- No model rollout, nothing on macOS, no Prime sandbox, no sealer, no compute metering (section 6).
- Gliders: one scripted rollout (policy D) on one fresh gliders world with the smoke config, on the fixed code and
  with one box per item: graded, 0 failed of 8 items (`results/gliders_smoke_D.json`). Nothing else was run on
  gliders.
- The one-box mode's channels are measured, not closed: closing them inside one box would mean resetting kernel
  counters a container cannot reset.
