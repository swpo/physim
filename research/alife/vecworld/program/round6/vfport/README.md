# vfport: the PhySim v2 exam as a verifiers environment (round 6)

Round 5's `agentenv` proved the exam with its own sandbox and orchestration. The lead then asked that the grader
use the verifiers library instead of an isolated one of our own (`roadmap/GRADER_VS_VERIFIERS.md`). This folder is
that port: a verifiers taskset run under the STOCK isolated grader (`--env.id isolated-verifier`), a host-side
laboratory, a per-item predictor driver, and a scripted harness that proves the route with no model.

Status, 10 Nov 2026: built by one agent, reviewed by two (a specification review and a red team, `redteam/`), then
fixed by a fourth. An independent host-safety audit then returned **NO-GO for the Mac** (`HOST_SAFETY_AUDIT.md`); a
fifth agent made the audit's nine required changes (section 8.3). A re-audit passed the code and returned NO-GO
again, narrowly, for the runbook's stop-and-recover text (section 8.5); a sixth agent changed that text and
rehearsed it as a session issues commands (sections 8.6 and 8.7). The re-audit of that round said GO for the
scripted smoke test on the Mac. The Mac session then reviewed the released commit read-only before running
anything and returned three major and eleven minor points; **the GO is suspended and `RUNBOOK_MAC.md` is ON HOLD
again.** A seventh agent changed the code and the runbook to meet those points and a disk requirement of the
coordinator, and rehearsed the result (sections 8.9 and 8.10). This file describes the code and the runbook as
they were after round 3, and section 8.12 describes round 4 (11 Nov 2026: after two model rollouts in the cloud
container exposed faults of the exam, and with the lead's Mac available again, the code and the runbook were
changed for model rollouts driven by request files; `RUNBOOK_MAC.md` is ON HOLD until that round's verdict).
Where section 8.12 and an earlier section differ, 8.12 holds. Everything of rounds 1 to 3 was
RUN on Docker in the cloud container (Linux x86_64, 4 cores, Docker 29.9.2) with scripted agents only. No model
call, no GPU job, no upload.
**Nothing was run on a Mac.** Numbers and their sources: `results/summary.json`, which also says which result file
ran on which code (`code_versions`): the 4-world table of section 4.1 and the costs of 4.5 were NOT run again
after the host-safety changes. Every pilot instance used here is deleted and must never be reused as an exam.

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
| Running the predictor | `runtime.run` as root in the box | `public/_item.py`: ONE request per call; the predictor runs as an unprivileged user (a random uid from 20000-59999 per rollout) under CPU, memory, file-size and process limits; root reads the reply through a directory handle, never follows a link, never blocks; afterwards root kills that user's processes and removes its files (unlink and rmdir of listed paths; no tree is removed by walking it). Outside a prepared box, or with any extra file system mounted, the driver runs nothing (section 8) |
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
  grading.py            validation, the item loop (one box per item, or one box), staging, the gate on the runtime object
                        (container_gate: verifiers' own Docker or Prime runtime, not borrowed)
  store.py              instance store on the worker; token-like names; environment scrub
  public/               files copied into every box as part of physim2: labclient.py (HTTP), validate.py,
                        _item.py (the one-request driver and its box guard), _rules.py (freeze rules, reply reader)
physim2_script/         the scripted harness (--env.agent.harness.id physim2-script)
agents/                 install_prebuilt.py (evaluator-only references), probe_grading.py, hostile_submission.py (21 modes);
                        the last two run inside an exam box only and refuse anywhere else
  _nokey.py             round 3: closes the two readers of ~/.prime/config.json before verifiers is imported
tools/                  make_instances.py, vfrun.py (drives vf-eval: run label, environment allow-list, disk floor, one
                        stop path with SIGTERM before SIGKILL, status 97/98; also the command that steps 2c and 3 of
                        the runbook use), vfeval.py (the only way vf-eval is started: verifiers' entry point behind
                        the credential stand-in), build_reference.py (the reference submission C; theta from a 0600
                        file), prove.py, check_probe.py, settle.py, recompute_table.py, run_report.py (a run as fixed
                        fields and counts, never message text), pin.py (PIN.sha256), make_summary.py,
                        make_safety_summary.py, docker_shim/docker (only for Linux hosts without IPv6)
                        development checks, cloud container only: check_safety.py and check_units.py (host, under
                        tripwires.py), check_driver.py and check_interrupt.py (throwaway containers), check_round3.py
                        (round 3: tripwires, a made-up credential file, real signals in a container),
                        check_runbook.py (the runbook as text), fixtures/mounts/ (stored mount tables)
rehearsal/              cloud container only, not for the Mac: issue.py (round 2) and issue3.py (round 3: issues ONE
                        runbook command as `sh -c '<text>'` and records it), watch_open.py (inotify on the made-up
                        credential file), check_round2.py (the round-1 verdict's tests, with stand-ins), make_record.py,
                        make_round2_index.py, make_round3_index.py, remarks_round2.json, remarks_round3.json;
                        parts.py and make_runbook.py (round 3: every runbook command written once, and the runbook
                        generated from them, so that repeated text is identical); not listed in PIN.sha256 (the
                        pilot executes none of it)
redteam/                the red team's attack scripts and results, kept; three attacks run again after the first fixes
                        (*-after-fix.json); not run again after the host-safety changes
docker/                 Dockerfile.ring (the one image of every box), Dockerfile.network (proxy-bound hosts only)
configs/                scripted_ring.toml (step 2c); a model rollout's config is NOT here: it is a flat file under
                        ../rollouts/configs/, named by a request (section 8.12)
round 4 (section 8.12)  physim2_env/boxcaps.py and runtime.py (the box caps on verifiers' one `docker run` of a box, read
                        back from the engine; the bearer on a box's proxy; credential-free docker clients),
                        bearer.py (the laboratory's per-rollout secret), spend.py (the spend stop and the context cap
                        on verifiers' one route to the provider), profiles.py, rollout_config.py, capture.py,
                        physim2_verifier/ (fixer A: section 8.13);
                        tools/check_config.py (the strict schema of a rollout config), check_request.py (a request,
                        the pin, the lead's standing go, the ledgers, prices and bounds; --fetch; --facts),
                        vfrun.py --request (the stages instance, reference, dry-run, rollout, close),
                        pack_rollout.py (the publication folder with its key scan), settle.py (an ungraded run counts
                        as the null policy); development checks, cloud container only: check_round4.py with
                        check_round4_step3.py (host, under tripwires), check_step3.py (through vf-eval, with
                        standin_model.py as the model endpoint), agents/probe_caps.py (runs in a box only);
                        results/round4_step3.json
results/                proof_ring.json + proof_ring_items.npz, recomputed_table.json, probe_ring.json, units.json,
                        units_before_fix.json, driver_container.json, gliders_smoke_D.json, summary.json;
                        host safety, round 1: host_safety_round1.json (one entry per required change), safety_host.json,
                        safety_interrupt.json, safety_runbook.json, rehearsal_round1.json
                        host safety, round 2: host_safety_round2.json (one entry per remaining change),
                        session_mode_round2.json (stand-in tests), rehearsal_round2.json (every command's literal text
                        and complete output), rehearsal_round2_proof.json and rehearsal_round2_probe.json (what steps 2a
                        and 2b of that rehearsal produced), safety_runbook_round2.json (the pinned text checker)
                        host safety, round 3: host_safety_round3.json (one entry per finding of the Mac review and D1),
                        round3_checks.json (tools/check_round3.py), safety_host_round3.json, safety_interrupt_round3.json
                        and safety_runbook_round3.json (the three older checkers on the new code and text),
                        rehearsal_round3.json (every command's literal text and complete output, the opens of the
                        made-up credential file), rehearsal_round3_proof.json and rehearsal_round3_probe.json
HOST_SAFETY_AUDIT.md    the independent audit of 10 Nov 2026 (NO-GO, nine required changes), its re-audit, round 1
                        (NO-GO, narrowly) and round 2 (GO for steps 0 to 2; SUSPENDED, see the note at its top)
RUNBOOK_MAC.md          verify, install, scripted smoke test, one cheap model rollout (ON HOLD: the round-2 GO is
                        suspended; the round-3 text has not been re-audited)
PIN.sha256              sha256 of every file the Mac pilot executes or imports (tools/pin.py; the runbook carries its hash;
                        round 3: 109 files; 91 of them are byte for byte those of the round-2 pin 7aa9bbfc...f64c19)
```

Round 5's code is reused BY IMPORT from `../../round5/agentenv`, so the package is installed from a checkout,
not from a wheel. (`PHYSIM2_AGENTENV` can point the import elsewhere for development; since round 3 the pilot's
tools refuse to start in an environment that holds it, or any other `PHYSIM2_*` name.) Of agentenv's 3,670 lines outside `results/`: 763 are no
longer on the route, 533 are wrapped, 2,374 are kept by import (32 of them copied verbatim into
`public/validate.py`). New here: 7,310 lines (package 2,735, tools 3,846, agents 570,
build and config 159; `results/summary.json: code`; 5,230 before the host-safety changes, most of the growth
is test tooling). The memo estimated about 750 including a sealer.

## 3. Run it (cloud container; the Mac: RUNBOOK_MAC.md)

```sh
S=<scratch>; V=/home/user/evalwork/vfport/.venv/bin/python
pgrep -x dockerd >/dev/null || (nohup dockerd --feature containerd-snapshotter=false > $S/dockerd.log 2>&1 &)
cp /root/.ccr/ca-bundle.crt docker/extra-ca.crt      # session proxy CA; an empty file elsewhere
docker build --network host --build-arg HTTPS_PROXY=$HTTPS_PROXY -f docker/Dockerfile.ring -t physim2-ring:1 docker/
docker build --network host --build-arg HTTPS_PROXY=$HTTPS_PROXY -f docker/Dockerfile.network -t localhost/verifiers-network:1 docker/
# the development checks refuse to start without PHYSIM2_DEV_MACHINE; none of them runs the cleanup on the host
D="env -i PATH=$PATH HOME=$HOME PHYSIM2_DEV_MACHINE=cloud-container"
$D $V -B tools/check_safety.py --out results/safety_host_round3.json               # host; every destructive primitive a tripwire
$D $V -B tools/check_driver.py --out results/driver_container.json                 # the cleanup and its guard, inside two containers
$D $V -B tools/check_interrupt.py --out results/safety_interrupt_round3.json       # SIGTERM first; containers found by label
$D $V -B tools/check_round3.py --scratch $S --out results/round3_checks.json       # allow-list, credential stand-in, watchdog, stop path
$D PYTHONPATH=$PWD $V -B tools/check_units.py --store $S/store --instance <any ring instance> --out results/units.json
# the pilot's tools start only from a clean environment (round 3): no PHYSIM2_*, UV_*, DOCKER_*, PYTHONPATH, ...
# VF_RUN_ID is required: verifiers labels every container with it (verifiers.run)
P="env -i PATH=$PATH HOME=$HOME VF_RUN_ID=<a label of this run>"
$P $V -B tools/check_probe.py --store $S/store --scratch $S/probe --disk-floor-gib 1 --out results/probe_ring.json
$P $V -B tools/prove.py --store $S/store --scratch $S/proof --worlds 4 --prefix proof-ring --disk-floor-gib 1 --out results/proof_ring.json
$V -B tools/recompute_table.py --out results/recomputed_table.json
$V -B tools/pin.py --write && $V -B tools/check_runbook.py --out results/safety_runbook_round3.json
```

`--disk-floor-gib` is the disk watchdog's floor (default 8 GiB; this machine has about 2 GiB free for everyone, so
a lower floor is given here). `results/summary.json` was last written as a whole by `tools/make_summary.py` before
the host-safety rounds; rounds 2 and 3 added their parts with `rehearsal/make_round2_index.py` and
`rehearsal/make_round3_index.py`.

Round 4 (the block above is round 3's and is kept as it was run then; image 1 and its certificate file are gone):

```sh
# the image: built by fixer A behind the session's proxy with two build arguments that the Mac does not use (section 8.13)
#   docker build --network host --build-arg HTTPS_PROXY=$HTTPS_PROXY --build-arg EXTRA_CA_B64="$(base64 -w0 /root/.ccr/agent-proxy-ca.crt)" \
#       -f docker/Dockerfile.ring -t physim2-ring:2 docker/
V=.venv/bin/python                     # an environment made with the runbook's step 1 inside this checkout
env -i PATH=$PATH HOME=$HOME $V -B tools/check_round4.py --scratch $S/chk --out $S/chk/round4_host.json      # host, under tripwires: 124 checks
P="env -i PATH=$PATH HOME=$HOME VF_RUN_ID=<a label of this run>"
$P nice -n 10 $V -B tools/check_step3.py --scratch $S/e2e --out $S/e2e/round4_step3_e2e.json --dev-machine cloud-container --disk-floor-gib 1.2
#   caps: agents/probe_caps.py in a capped box.  route: fetch, instance, reference, dry run, rollout (stand-in endpoint), close, pack
$V -B tools/check_runbook.py --out $S/chk/runbook_check.json                                                 # the runbook as text
$V -B tools/make_round4_step3.py --host ... --caps ... --route ... --runbook ... --out results/round4_step3.json
$V -B tools/check_request.py --facts                                                                         # the block of facts of the runbook's step 3
```

`tools/check_round3.py` is round 3's record: its part on the command form with model credentials describes a
route that round 4 replaced (a model run now starts from a request only), so it was not run again in round 4.

Afterwards delete the store by its full path (it holds the hidden instances). After an interruption:
`docker ps -a --filter label=verifiers.run=$VF_RUN_ID` lists exactly this run's containers; remove them by name.

## 4. What was proven

Everything in this section was run in the cloud container. Sections 4.2 to 4.4 ran on the code as it is now, after
the host-safety changes; **4.1 and 4.5 ran before them (package code of commit 743f6b75e) and were not repeated**:
since then the driver's guard and wipe, the staging and the gate on the runtime changed, the arithmetic of scoring
did not, and one world of the table was run again with the Mac's arguments in the rehearsal
(`results/rehearsal_round1.json`; `summary.json: code_versions`). Sources are files of `results/` unless marked.

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

### 4.3 The probes of this port (`probe_ring.json: checks_new`, 65 of 65; each with its evidence)

All probe rollouts use the default grading mode (one box per item) unless said otherwise.

- **(a) Files, processes, shared memory.** A predictor that leaves three files, a System V segment and a background
  process at every item finds none of them at any of the 8 items. Control with the cleanup switched off (one box):
  at item 2 it finds all of them.
- **(a2) The state of a box itself.** The same predictor reads a file of its submission, touches three
  directories, forks 40 to 79 processes and sends 1,200 loopback datagrams at every item, and at every item
  looks for the traces of the item before. With one box per item: no file marked as read, no directory touched,
  loopback counter 0 at every item, process id steps between -2 and 3 (`evidence.a2_channels_one_box_per_item`). With all items
  in one box and the cleanup on: every item after the first sees all four (the read mark, three directories, a
  loopback counter growing by 2,411 per item, a process-id step that is the number of forks of the item
  before plus a constant 20), which is why that mode is a pilot mode and is marked in the trace
  (`evidence.a2_channels_all_items_in_one_box`).
- **(b) No canary, no hidden value.** With `HF_TOKEN=<canary>` in the worker's environment: the laboratory process
  inherited it and dropped it after loading; a script that read the environment and every readable file found no
  canary in the agent's box or in any item box. No token-like variable name exists in either. The saved runs
  contain neither the canary nor the secret or a hidden parameter (`evidence.b_trace_scan`: 227 files, 0 hits;
  `summary.json: hidden_value_scan`).
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
  finite reward, grading time 24/23/25 s for 8 items. The largest float32 values are a valid reply: graded,
  reward -1.50e+38 (section 6, hole 5).
- **(h) A harness that dies.** Exit status 1 and `kill -9 -1`: verifiers records `HarnessError` and runs neither
  finalize nor the reward. `tools/settle.py` then writes the K record, and the same agent's second opening of the
  instance is refused. The test agents now carry a gate that refuses outside an exam box (section 8); inside the
  box it lets them work: the harness ends with status 137, killed by the agent's own `kill -9 -1`
  (`h_kill_all_was_issued_inside_the_box`, `box_scripts_passed_their_gate_inside_the_box`).
- **Operator guards:** the laboratory refuses a colocated, url or sandbox placement; setup refuses an open
  network, a non-container runtime, `HF_TOKEN` and `GITHUB_PAT` in the harness environment (anything not on the
  allow-list), and the same agent twice.

### 4.4 Offline checks and the red team's attacks again

- `units.json`: 66 of 66 offline checks pass on the code as it is now. Since the audit this tool no longer starts
  the driver as a program when it runs as root, so its six `driver_*` checks are absent here (the same cases are
  in `driver_container.json`); the first fixer's run had 67 of 67 with them. The same script on the builder's code
  passed 25 of 46 (`units_before_fix.json`, not repeated: the failures are the reviews' findings reproduced).
- `driver_container.json`: 31 of 31 checks inside two throwaway containers (section 8); the 19 of the first fix
  are among them.
- `safety_host.json` 36 of 36, `safety_interrupt.json` 8 of 8, `safety_runbook.json`: the audit's tests (section 8).
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
- The proof took 1,973 s (round 5's: 512 s). The probes, run again on the code as it is now: 1,072 s for 37
  rollouts (963 s before the host-safety changes; the agent box's validation now also checks the mount table, and
  the machine was shared).

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
   during one request; the agent, root in its box, has no process limit at all. Not run (shared machine). The
   check in an agent's box and the grading both run under a uid drawn per box and per rollout from 20000-59999
   (the agent box's was 1000 before the host-safety changes), so one agent can no longer aim at the uid of
   another's check. Fix: Docker daemon settings on the grading machine (`--default-ulimit`,
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
   guard knows Docker only (its signs of a container and, since the host-safety changes, its mount table): on
   Prime grading would stop at staging with "not recognised as a disposable box", naming the sign or the mount,
   until Prime's are added. It fails closed.
9. **Laboratory reply times are not padded (memo hole 7).** Not measured.
10. **macOS: nothing run.** The network cut uses another path there; the Mac part of `tools/check_probe.py`
    (listener on 127.0.0.1, `host.docker.internal`) was written without a Mac.
11. **No model rollout.** The stock harnesses were not run; the stop hook `Physim2Task.frozen` has never fired; a
    model's direct use of the tool operations `validate` and `submit` is tested with scripts only.
12. **MCP argument errors show pydantic's wording** (`op` given as a number): public text, no hidden value.

## 7. Rules for a sealed run (operator)

`--env.id isolated-verifier`, a Docker runtime, `VF_RUN_ID` set to a label of the run (the only safe way to find its
containers after an interruption), `push = false` (or `PRIME_RUNS_MODE=disabled`), no `--resume`,
`max_retries = 0` for the agent and the episode, `--env.verifier.retries 0`. Leave at their defaults: `single_use`
(true; every opening is recorded in `<store>/<instance>/hidden/opened/`, and only the operator, by removing that
one file, can let an agent whose rollout died before it started open the instance again), `item_isolation` ("box"), `item_cleanup` and `stock_collection` (a rollout run otherwise is marked
`NOT_AN_EXAM` or `between_item_state` in its trace). Pass no variable into a box that is not on the allow-list
(setup refuses). After the run: `tools/settle.py` on the run directory; a rollout without a reward counts as K
and its instance stays closed for that agent. A dedicated machine with Docker process and disk limits (holes 1
and 3).

## 8. Host safety: the incident of 10 Nov 2026, the audit, and what was changed

### 8.1 The incident

- **What ran.** While writing `tools/check_units.py`, the first fixer started `physim2_env/public/_item.py` as root
  on the cloud container itself, outside any container, 14 times (about 04:31 to 04:34 UTC).
- **What it did.** The driver's cleanup is meant for a disposable box: SIGKILL to every process of the
  predictor's uid and deletion of every file that uid owns on every writable file system. On the host, with the
  default uid 1000, it deleted `/home/ubuntu`, the home directory of the unused default account. It was recreated
  from `/etc/skel`; what it held before is not known. The coordinator found no tracked file missing in the
  checkouts and worktrees; the Python environments import; the Docker images run.
- **Why it could.** The driver decided from `euid == 0` alone. It was written to run in containers and nothing
  told it that it was not in one.
- **The first fix** (commit 7e034be18): a guard of four conditions in the driver (marker, sign of a container,
  route variable, the box's own uid), a check of the runtime's type string before commands are sent into a box,
  tests under 12 tripwires on the host and in a throwaway container.

### 8.2 The audit: NO-GO

An independent audit (`HOST_SAFETY_AUDIT.md`) found the first fix incomplete and the Mac runbook unsafe to follow:
five major findings (A1: the runbook's first command, `uv sync`, deletes another project's `.venv` when run from
the wrong folder; A2: an interrupted run leaves containers and a laboratory process, and the runbook's only
listing also matched other verifiers runs; A3: two test scripts run `kill -9 -1` with no check of where they
are; A4: in any Docker container three of the four guard conditions come for free, so a hand-started container
with a host folder mounted would be cleaned; A5: the wipe used `rmtree`, which deletes files of any owner below a
directory of the uid), fifteen minor ones, nine required changes, two hardening items.

### 8.3 Round 1 of changes (this code; re-audited in 8.5)

`results/host_safety_round1.json` has one entry per change: what changed, the test the audit named, its result
and the file that records it. Evidence labels: **tripwire** = run on the cloud host with 65 primitives of `os`,
`shutil`, `subprocess` and `pathlib` (kill, unlink, rmdir, rename, chmod, chown, set-id, fork, exec, rmtree, run,
Popen, ...) replaced by recorders that raise, before the package is imported (`tools/tripwires.py`);
**container** = run in a throwaway container started without any host mount; **vf-eval** = scripted rollouts
through the route; **read** = checked as text; **inferred** = everything about macOS.

| change | what the code does now | test and result |
|---|---|---|
| 1 working directory (A1) | every runbook command starts with `cd "<absolute study folder>" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py &&`; `uv` appears in two commands only, both with `--project <absolute path>`, the dry run first and started from `/` so that uv prints the environment's absolute path; no `uv run`; no subagents (round 2: both with `--managed-python`, the real sync detached) | with `echo` in place of the command the guard prints nothing for 8 wrong folders from 2 starting points and prints for the study folder: `safety_runbook.json`, `guard_*`, `uv_*` (run: cd, test, echo only) |
| 2 interruption (A2) | `tools/vfrun.py` requires `VF_RUN_ID` (verifiers writes it on every container as the label `verifiers.run`), checks that Docker answers, and stops vf-eval with ONE SIGTERM, SIGKILL only 120 s later; a stop request to a tool is passed on. Runbook: long commands detached with a log, a status command that lists containers by that label and processes by the checkout's own `.venv` path, a section "If a run was interrupted" (round 2 replaced the process listing and the stop command: 8.6) | a stand-in for vf-eval records SIGTERM and no SIGKILL under `timeout=1`: `safety_host.json` `R2_*` (tripwire, no process) and `safety_interrupt.json` `stop_*` (container, a real process); a foreign `vf-other` is absent from the label listing and present in the old name listing: `label_*` (container). With the real vf-eval: the rehearsal |
| 3 box scripts (A3) | `agents/hostile_submission.py`, `agents/probe_grading.py`, `redteam/agent_rt.py`: the first statement exits unless `/.dockerenv` exists and `/etc/physim2/predictor_uid` is a root-owned regular file; asked again directly before each `kill -9 -1` and before the box's `tar` is replaced | 34 starts through `runpy`, every mode: `SystemExit("refused: ...")`, no tripwire reached, nothing imported; also with one of the two signs simulated: `safety_host.json` `R3_*` (tripwire). The `harness-killall` rollout still ends by the agent's own kill inside the box (status 137): `probe_ring.json` (vf-eval) |
| 4 driver (A4, A5) | `_item.py`: (a) the wipe unlinks and rmdirs exactly the paths the uid owns, deepest first, never a mount point; no `rmtree`, `shutil` is not imported; (b) an unreadable mount table raises, nothing falls back to `/`; (c) a mount condition in the guard: an overlay root, kernel file systems at or below `/proc`, `/sys`, `/dev`, and Docker's three `/etc` files; anything else refuses | the pure function on 13 stored mount tables (3 captured here, 10 written by hand, among them a host folder, a volume, a macOS share): `safety_host.json` `R4_*` (tripwire). In containers: a root-owned file below a directory of the uid survives the cleanup; with `--tmpfs /extra` the guard, every function and the driver refuse and the canaries survive; the 19 earlier checks pass: `driver_container.json`, 31 of 31 |
| 5 worker gate (A4) | `grading.container_gate`: only an object whose class is exactly verifiers' `DockerRuntime` or `PrimeRuntime`, with the matching type, not borrowed (`info.borrowed`: a container somebody else started and attached), not nested, with a container name verifiers generated; used by the taskset and by the scripted harness | recording stand-ins typed `docker`, `subprocess` and `prime` receive zero commands from ten entry points (`stage`, `run_request`, `_public_files`, `setup`, `BoxAccess.check`, ...); a subclass of the real class, a borrowed and a hand-named container are refused: `safety_host.json` `R5_*` (tripwire). 37 rollouts pass the gate with real runtimes (vf-eval) |
| 6 runbook text | an inventory of what is signalled, deleted, written and listening on the Mac; the store path on every command; "stop and report" instead of the Docker shim; a `docker info` gate before each run; step 4 as one `&&` chain that copies the results out first and keeps the shared image; the one expected macOS failure named; the "never" table | `safety_runbook.json` `text_*` (read) |
| 7 pin | `PIN.sha256`: the sha256 of the 105 tracked files the pilot executes or imports (this folder, round 5's `agentenv`, the `vw` library); the runbook's pin block carries the hash of that list (round 2: and no commit; the commit is the one the coordinator's GO message names: 8.6) | `safety_runbook.json` `pin_*`; step 0 of the runbook in the rehearsal (run) |
| 8 rehearsal | steps 0 to 2 and 4 of the rewritten runbook, once in the cloud container from a fresh clone of the pushed commit with its own `.venv`, two interruptions | `results/rehearsal_round1.json`; section 8.4 |
| 9 step 3 | its own hold; the paid command alone between STOP lines with the price formula; output to a file that is never displayed; `tools/run_report.py` prints fixed fields and counts, never message text; no other harness offered; Docker Desktop's disk limit below the free space | `safety_runbook.json` `step3_*` (read). Step 3 was not run; the report tool was run on scripted traces |
| S1 driver hardening | uid range 20000-59999 (1000 is refused even with a marker that says 1000); `--uid` has no default; the guard requires a root caller; the identity is verified after the set-id calls and before `kill(-1)`; outside a box nothing runs unless `--no-box` is given; the agent box's marker comes from the range; the validator runs only where the marker exists | `safety_host.json` `S1_*` (tripwire); `driver_container.json` (container); `probe_ring.json` `predictor_runs_unprivileged` (vf-eval) |
| S2 tools | `check_units.py` never starts the driver as a program when it is root and puts all 65 tripwires in before it imports the driver; `redteam/rt_run.py` and `nproc_cross_box.sh` delete no path and no container name they did not make | `units.json` 66 of 66 (tripwire). The two red-team tools were changed by reading and NOT run |

Run again on this code: `check_units.py`, `check_driver.py`, `check_probe.py` (37 rollouts: 32 of 34 and 65 of 65),
and in the rehearsal one world of `prove.py` with the Mac's arguments and one direct `vf-eval` rollout. NOT run
again: `prove.py --worlds 4`, the gliders rollout, the red team's attacks.

### 8.4 The rehearsal

Steps 0, 1, 2 and 4 of the rewritten runbook were run once in the cloud container (15:12 to 15:50 UTC, 10 Nov
2026) from a fresh clone of the pushed commit cac38e324 with its own `.venv`; every command came from the runbook
through a script, with two textual substitutions (the study folder; `$HOME`, which had to point into this
session's scratch) (`results/rehearsal_round1.json`: every command, its exit status and what it printed).

- **What ran as written.** Step 0 (commit, `PIN.sha256`, Docker and folders). `uv sync`: the dry run named the
  clone's own `.venv` by its absolute path; the sync took 6.7 s and left the working tree clean. Step 2a
  (7.5 minutes): all graded, 0 failed items, ticks 392 / 0 / 0, one box per item with identical scores, 64 boxes,
  2.68 s per box. Step 2b (37 rollouts, 1,291 s): 32 of 34 and 65 of 65, both failure lists empty (Linux). Step 2c
  (3.5 minutes): the report tool printed its fixed fields; 0 hidden-value hits. Step 4: five result files copied
  out, the two pilot folders deleted, no container of the pilot.
- **Two interruptions.** (1) `kill -TERM` of the tool by the runbook's own procedure, with a box up and the
  laboratory running: the tool passed the signal on, the real vf-eval removed its container and stopped its
  laboratory, and 4 seconds later nothing of the pilot was listed. (2) SIGKILL of vf-eval, the case of finding A2:
  one container and the laboratory process stayed; the runbook's status command listed exactly those two
  (containers by the run label, processes by the checkout's `.venv` path); they were removed by exact name and by
  pid, the pilot folders were reset, and the step ran to its end.
- **Four deviations forced by the machine:** a sparse, shallow clone (disk); `$HOME` replaced and by-hand checks
  that differ (root, x86_64, a proxy, `UV_NATIVE_TLS`); the image build NOT run (the shared image exists here, at
  which the runbook says stop; a rebuild needs the proxy's certificate and half of the free disk); the IPv6 shim on
  PATH for the one direct `vf-eval` of step 2c (this kernel has no IPv6).
- **Five places where the text did not match what happened**, all corrected in the runbook afterwards (the pinned
  package and tools are byte for byte the rehearsed ones: same `PIN.sha256`): the end of the log of 2a has two JSON
  lines, not one; after a hard kill two small folders stay that nothing removes (the laboratory's working folder
  under `~/.cache/verifiers/runtimes/subprocess/` and the task controller's socket folder in the temp directory);
  what the tool's log shows after an interruption was not described; the status command shows the last lines of
  the log of 2c, which the text told the reader not to look at; the shape of the status output.
- **Not rehearsed:** the image build in the runbook's form, step 3, anything on macOS.

### 8.5 The re-audit of round 1: NO-GO, narrowly

The re-audit (`HOST_SAFETY_AUDIT.md`, "Re-audit, round 1") closed A1, A3, A4 and A5 and passed the code: the
verdict on the code holds for the files that `PIN.sha256` lists (sha256 7aa9bbfc...f64c19, 105 files). It kept
A2 open, for four reasons that are all in the runbook:

- **The waiting shell.** A session issues every command as `<shell> -c <text>`. A detached command then leaves
  a waiting shell whose command line is that whole text, so the status command's process listing showed it next
  to the tool; a stop signal sent to that line stops nothing, and the log never gets its `EXIT` line. The first
  rehearsal ran the commands from files and could not see this.
- **The interpreter.** On a Mac whose Python 3.12 is a framework build, the process line may not begin with the
  `.venv` path, and the listing would show nothing while the pilot runs (inferred).
- **Step 1 had no branch** for a cut: the real `uv sync` ran in the foreground.
- **The pin handover.** The copy of the runbook inside the pinned commit named no commit.

It also reported two minor gaps of the guard on Linux hosts, off the runbook (a memory file system mounted below
`/dev`, `/proc` or `/sys` passes the mount condition; the guard does not look at the process namespace) and two
minor ones of the tools (the box scripts' gate does not look at mounts; `check_units.py` runs `tar` and `chmod
-R` on a temp folder before its tripwires). These four are NOT fixed here: they need a change of pinned files and
a re-audit of its diff, and they are to be closed before the package runs on any Linux machine other than the
cloud container.

### 8.6 Round 2 of changes (runbook text and one rehearsal; not re-audited)

No file listed in `PIN.sha256` was changed. `results/host_safety_round2.json` has one entry per remaining
change: what changed, the lines, the test the verdict names, its result and the file that records it.

| change | what the runbook does now | test and result |
|---|---|---|
| 1 process listing | both status commands list processes with `ps axww -o pid= -o command= \| grep -E "^ *[0-9]+ <study folder>/\.venv/bin/python"`: the pid, then a command line that BEGINS with the checkout's interpreter. A waiting shell begins with the shell's name and is not listed. The path is now a pattern, so section C checks by hand that it holds only letters, digits and `/ . _ -`. (The verdict wrote `ps axwwo pid=,command=`; two `-o` options mean the same and cannot be misread by a BSD `ps`; on Linux both print the same.) | the 2a command issued as ONE `sh -c '<text>'` and as `bash -c`, with a stand-in tool: the status lists the tool and not the waiting shell, and the round-1 listing, as a control, lists both (`session_mode_round2.json`, `standin_1_*`); the same with the real tool, also through the session's own command tool (`rehearsal_round2.json`) |
| 2 stop command | `... && ps -ww -p <pid> -o command= \| grep -E "^<study folder>/\.venv/bin/python" && kill -TERM <pid>`: it prints the command line of the process it signals; for any other pid it prints nothing and sends nothing | aimed at the waiting shell's pid: no output, no signal (under `sh -x` the shell ran `ps` and `grep` and no `kill`), both processes alive, no `EXIT` line; aimed at a foreign `sleep` and at a pid that is gone: nothing; aimed at the tool: its command line, then `EXIT 143` (`standin_2_*`); in the rehearsal on the real waiting shell, tool, vf-eval and laboratory |
| 3 interpreter | `--managed-python` on both uv commands (uv then uses its own Python, which does not re-execute under another path; if it has none, the DRY RUN already downloads it: found here, and now said in the runbook); a command after the import check prints the interpreter's own process line and `INTERPRETER-OK` or `INTERPRETER-DIFFERS`; after each detached start the text says what `processes:` must show and, if it does not: send no signal, wait for `EXIT`, stop and report | with a stand-in interpreter that re-executes under another path the check prints `INTERPRETER-DIFFERS`, and the status lists nothing while its tool runs (`standin_3_*`); in the rehearsal `Using CPython 3.12.13` without a path and `INTERPRETER-OK` |
| 4 step 1 | the pilot folders are made first; the real `uv sync` runs detached with a log, an `EXIT` line and a status command; a cut or an unexpected output in step 0, 1 or 4 is a stop. "If a run was interrupted" is for step 2 only, is used once (a second interruption: points 1 to 5, then stop), and stops on a Docker error; a reset or a step-4 command that prints nothing is a stop | `text_4_*`; the detached sync in the rehearsal. The "once" rule was not exercised as a rule |
| 5 pin handover | the file names no commit. The commit is the 40-character hash of the coordinator's GO message; the lead gives it to the session and the first line of step 0 must equal it; the code is identified by the sha256 of `PIN.sha256`. The hold notice stands between two markers and is the only text a verdict edits. Step 0 says what a failed comparison prints | on a copy of the three trees: intact, the hash and `PIN-OK`; one file changed, `shasum: WARNING: 1 computed checksum did NOT match` and no `PIN-OK`; one file missing, `shasum: <file>: No such file or directory` and a `WARNING` line (`standin_5_*`) |
| 6 text | what each log shows after a stop (a traceback and `EXIT 130`; `EXIT 143`; `EXIT 130` without a traceback), the end of `single.log`, the numbers that macOS pads, and six places where the second rehearsal differed | `text_6_*`; `rehearsal_round2.json`, `mismatches` |
| 7 rehearsal | section 8.7 | `rehearsal_round2.json` |
| same pass, not gating | the never table forbids any `docker run` by hand, whatever its options; the paid command of step 3 starts nothing without a file `LEAD-GO-STEP3` that the lead creates by hand; a command for the lead's use copies the run folder of step 3 out before step 4, unread, and only when the report tool counts no hidden value (the lead decided that pilot traces may be uploaded where that helps; the upload is the lead's own act) | with stand-ins for vf-eval and the report tool (`standin_same_pass_*`). Step 3 was never run |

All named tests pass: `rehearsal/check_round2.py` 47 of 47. The pinned text checker `tools/check_runbook.py`
passes 32 of 33; the one that fails asks for the round-1 `[p]ython` pattern, which change 1 replaces (the tool is
pinned and was not changed). `tools/pin.py --check`: 105 files, 0 differences.

Run again on the pinned code, from the rehearsal's clone: `check_safety.py` 36 of 36 (host, tripwires),
`check_driver.py` 31 of 31 and `check_interrupt.py` 8 of 8 (throwaway containers), each check equal to the
recorded file; in the rehearsal `check_probe.py` (37 rollouts: 32 of 34 and 65 of 65), one world of `prove.py`
and one direct `vf-eval` rollout. NOT run again: `check_units.py` (no pinned file changed; a part of it runs
outside its tripwires), `prove.py --worlds 4`, the gliders rollout, the red team's attacks.

### 8.7 The second rehearsal, in session mode

Run once in the cloud container (16:47 to 17:27 UTC, 10 Nov 2026) from a fresh clone of the pushed commit
be2c17ae6 with its own `.venv`. Every command was issued as ONE `sh -c '<text of the fenced command>'`, started
in `/`, never from a file, with the same two substitutions as before (the study folder; `$HOME`).
`results/rehearsal_round2.json` holds the literal text and the complete output of each of the 81 commands
(40 of them status commands).

- **What ran as written.** Step 0. Step 1 without the image build: the dry run downloaded uv's Python and
  printed `Using CPython 3.12.13` and the clone's own `.venv` path; the detached sync ended with `EXIT 0`;
  `INTERPRETER-OK`. Step 2a (7.5 minutes): all graded, 0 failed items, ticks 392 / 0 / 0, one box per item with
  identical scores, 64 boxes, 2.65 s per box. Step 2b (37 rollouts, 1,264 s): 32 of 34 and 65 of 65, both failure
  lists empty (Linux). Step 2c (3.5 minutes): the report's fixed fields, 0 hidden-value hits. Step 4: five files
  copied out, the pilot folders deleted, Docker as in the baseline.
- **The session's own tool.** In the clean pass the 2a command and the first status were issued through the
  rehearsing session's own command tool. It left the waiting shell the re-audit described (`/bin/bash -c ...
  eval ...`, parent of the tool); the status listed one line, the tool.
- **Five interruptions**, each cleared by the runbook's own points, with nothing of the pilot listed afterwards.
  (1) The stop command aimed at the waiting shell on purpose: nothing printed, nothing signalled; then at the
  tool inside its first rollout: traceback, `EXIT 130`, nothing listed 3 s later. (2) The tool stopped before
  its first rollout: `EXIT 143`. (3) SIGKILL of vf-eval: one container and the laboratory listed; the container
  removed by name; the laboratory had ended by itself before the stop command, which printed nothing. (4) The
  vf-eval of 2c stopped: `EXIT 130` without a traceback, nothing listed 2 s later. (5) SIGKILL again, and the
  stop command on the laboratory while it was still there: it printed its command line and stopped it.
- **Deviations forced by the machine or chosen:** the four of the first rehearsal (sparse clone; `$HOME` and the
  by-hand checks; no image build; the IPv6 shim for 2c, here on the PATH of that call); uv's Python sent to the
  scratch folder; and the section "If a run was interrupted" used five times, each time as a first interruption.
- **Six places where the text did not match**, all prose, all corrected (the 30 commands are byte for byte the
  rehearsed ones): `Would download 1 package` in the singular; the interpreter line is cut at 160 characters; a
  line `Terminated` from the shell before `EXIT 143`; a laboratory that ends by itself before point 4; a helper
  container with a name chosen by Docker under `containers:` for a moment; vf-eval's own log lines before its
  `EXIT 130`.
- **Not rehearsed:** the image build, step 3 with its file gate and its trace copy, the "once" rule as a rule,
  anything on macOS (zsh, BSD `ps`, uv's Python there).

### 8.8 What remained after round 2 (kept as written; 8.11 is the list of today)

- A re-audit of the round-2 runbook, then a verdict. Until it says GO, nothing runs on the Mac. (Done: 8.9.)
- Nothing ran on macOS or Docker Desktop. Inferred: that containers there carry `/.dockerenv` and Docker's usual
  mount table. If not, staging stops with "not recognised as a disposable box" and names the reason; nothing is
  damaged, and nothing is graded.
- The guard still rests on Docker conventions; in a long-lived container that was prepared by this environment,
  the files of the predictor uid can still be removed. That is its job.
- A vf-eval killed with SIGKILL still leaves its containers and its laboratory process; they are now findable (by
  label, by a command line that begins with the checkout's `.venv` path) without touching anything else, and the
  runbook says how. The session does that recovery itself, once.
- The two minor gaps of the guard and the two of the tools that the re-audit reported (8.5) are open.
- The laboratory runs on the worker as the operator; verifiers signals only process groups it started.
- `uv sync` runs an unpinned build backend (hatchling) on the machine (pinned in round 3), replaces `./.venv` of
  the study folder and, with `--managed-python`, installs uv's own Python if uv has none. The image build of
  step 1 has never run in the runbook's form.
- In step 3 an untrusted model is root in a container for an hour; Docker Desktop's virtual machine is the only
  wall, and it was not tested.
- Not touched (outside this folder): round 5's `agentenv/mac/` runbook and compose file, which mount host folders
  into a container that deletes there as root. The Mac runbook's "never" table names them.
- Rules that stand: no tool or test of this folder may run the cleanup on a host; a host test installs
  `tools/tripwires.py` before it imports the package; a real cleanup or a real signal is tested in a throwaway
  container without a host mount.

### 8.9 The round-2 verdict, the Mac session's own review, and round 3 of changes (not re-audited)

The re-audit of round 2 said **GO for steps 0 to 2** (`HOST_SAFETY_AUDIT.md`, "Re-audit, round 2"; commit af767adbd).
Before running anything, the Mac session reviewed that commit read-only, six lenses with a skeptic on each finding.
It found no blocker, three major and eleven minor points, and facts about the machine (16 GiB free; Docker
Desktop's disk image may grow far beyond that; `~/.prime/config.json` exists; `~/Documents` is synced to iCloud).
The GO was suspended, the runbook put back ON HOLD (commit fb54884bc), and the coordinator added a disk
requirement (D1). Round 3 answers each point. Unlike round 2 it changes pinned files, so `PIN.sha256` is new
(109 files, sha256 `cd67eb4b8d706acf44c23dce72efd087532b422a5b66179c1cdc92561ffd03e4`) and the code needs a re-audit of its diff. `results/host_safety_round3.json` has
one entry per finding: where it was confirmed, what changed (file and lines), the test, its result and the file
that records it. Every finding was confirmed against the code first; none was rejected.

| finding | confirmed where | what changed | test and result |
|---|---|---|---|
| M1 the session's own environment is never checked, and all of it reaches vf-eval, `docker` and the laboratory | `tools/vfrun.py` (old `child_env`: everything but one name); verifiers `runtimes/subprocess.py:104, 134, 151` (the laboratory inherits vf-eval's environment), `runtimes/container.py:44-57` (so does the `docker` client), `mcp/server.py:278-283` (`MCP_HOST`, `MCP_PORT` set the laboratory's address), `physim2_env/_paths.py` (`PHYSIM2_AGENTENV`) | (a) runbook step 0: a command the session runs itself (names only; `docker context show`; the context's address). (b) `child_env` is an allow-list: nine names are copied, the rest is set by the tool. (c) every tool refuses to start when its environment holds a name of the step-0 list. (d) a tool refuses a Docker context that is not a Unix socket of the machine. (e) the laboratory binds 127.0.0.1 whatever `MCP_HOST` says | `round3_checks.json`: `host_env_*` (10, under tripwires), `box_the_child_gets_the_allow_list_...`, `box_a_session_with_docker_host_is_refused_...` (container); rehearsal: step 0 from a clean and from a deliberately dirty session |
| M2 the signal table is incomplete | verifiers `runtimes/container.py:44-65` (SIGKILL of the client's process group whenever a call is cut), `runtimes/subprocess.py:103-129` (the probe and `tail` helpers), `utils/version.py:23-31` (`git rev-parse`, 5 s), `mcp/server.py:112-118` (Linux only: the laboratory dies with its parent); our own `subprocess.run(..., timeout=)` calls | runbook section B rewritten from the source: ten rows, each with who can be the target; the status command names verifiers' probe (`PROBE`) | text: `check_runbook.py` 46 of 46; rehearsal: after a hard kill the status showed exactly that probe for some minutes, as the text says |
| M3 the listener list is incomplete, and the Prime key is loaded although no model is called | verifiers `interception/server.py:346, 444-447`; `configs/cli/eval.py:86` -> `configs/client.py:37-57` (the file is read when verifiers is IMPORTED), `client.py:93-104`, `clients/eval.py:67`; `physim2_env/access.py` (the Unix socket). **Found in addition here, by tracing a rollout:** the prime-runs SDK reads the file and its key for every run, uploads off or not (`utils/platform.py:93` -> `prime_runs/run.py:456` -> `prime_traces/core/config.py:25-32`) | section B lists six listeners with who can connect and what each needs. `physim2_env/_nokey.py` closes both readers before verifiers is imported, in every process of the pilot; vf-eval is started through `tools/vfeval.py` only; every scripted run gets a stand-in client (`http://127.0.0.1:9/v1`, a key variable that is never set); `PRIME_API_KEY` is not passed on. Step 3 is separate: `--model-credentials prime` on its one command | `round3_checks.json`: `nokey_*` (8): with a made-up file in a scratch home, the stock import opens it and loads its key, the SDK does so for a disabled run; through the package neither opens it. Rehearsal: the kernel's record of every open of that file over the whole rehearsal (section 8.10) |
| m1 theta on a command line | `tools/prove.py:56-57` (old) | `tools/build_reference.py`: the parameters come from a file of mode 0600 in the store and reach round 5's script in memory only; process lines are cut at 160 characters, log lines at 200 | `host_theta_*` (2); rehearsal: the record holds no hidden value (counted) |
| m2 the path as a pattern; any process of the environment accepted | runbook round 2, status and stop commands | both use `awk` with `index()`: the command line must be, letter for letter, the interpreter's path followed by one of eight program beginnings; each listed line carries a word (`TOOL`, `VF-EVAL`, `LAB`, `HELPER`, `PROBE`, `OTHER`) | run with mawk on made-up `ps` output (a neighbour path with another character in place of the dot, another checkout, the old console script: not matched); rehearsal: the stop aimed at the waiting shell printed and sent nothing |
| m3 `rm -rf` through a linked pilot folder | runbook round 2 | `test ! -L` on the pilot folder and its two subfolders before both `rm -rf`; step 0 and step 1 refuse links too | `r3_no_rm_rf_follows_a_linked_pilot_folder` |
| m4 no step for an orphaned helper | `tools/prove.py`, `tools/check_probe.py` (`subprocess.run` without a handler) | `vfrun.run_helper`: the helper is stopped with its tool; the status and stop commands know `HELPER`; point 4 of the section | `box_a_helper_is_stopped_with_its_tool` (container) |
| m5 on macOS the laboratory outlives a killed vf-eval; the tool went on after a SIGKILL | verifiers `mcp/server.py:112-118`; `tools/vfrun.py` (old `run_eval` returned) | a vf-eval that was stopped by the tool or died of a signal ends the tool: status 98 (97 for the disk), a line `refused to go on: ...`; section B and point 4 say what macOS does (inferred) | `box_time_limit_...`, `box_sigkill_only_after_...`, `box_a_vf_eval_that_dies_of_sigkill_...` (container); rehearsal: `EXIT 98` after the hard kill |
| m6 `docker rm -f` trusts the copied name | runbook round 2, point 3 | the command first reads the run label that Docker has for that exact name and removes only if it is this pilot's | rehearsal: a name nobody has, and a container of the rehearsal's own with another label: nothing removed; the pilot's leftover box: removed |
| m7 any container can reach the laboratory on Docker Desktop | verifiers `runtimes/docker/__init__.py:224-225, 336`; the laboratory has no secret | the rule now: a command before step 2 that must list no running container; section B says why. **Deferred:** a bearer for the laboratory is not cheap (the address is handed out by verifiers and read by round 5's client, neither of which this folder may change in passing); it is a named condition of step 3 | text only |
| m8 the proxy is never asked for the worker's own loopback names | `agents/probe_grading.py:156-157` (old) | the probe asks the box's proxy, with the box's password, for `127.0.0.1`, `localhost`, `vf.host.internal` and `host.docker.internal` at the listener's port, by GET and by CONNECT; a new check requires `HTTP 403` eight times and no hit on the listener | rehearsal 2b: `HTTP 403` for the four names by GET and by CONNECT, 0 connections on the listener; 66 of 66 new checks |
| m9 the build backend is unpinned | `pyproject.toml:18` (old) | `hatchling==1.33.0` and five packages under it as build constraints; uv 0.11.32 writes them into `uv.lock` (`[manifest] build-constraints`) and `--locked` refuses a `pyproject.toml` that differs. Versions, not hashes: uv has no hashes for build requirements | run in scratch: a changed constraint fails `uv lock --locked`; rehearsal: the detached `uv sync --locked` ended `EXIT 0` |
| m10 the build cache is in no inventory | runbook round 2 | section B and step 4 name it; step 4 prints `docker system df`; removing it is the lead's (`prune` stays on the never list) | text |
| m11 counts hide failures | runbook round 2, step 0 and step 4 (`... \| wc -l`) | no count: each listing is followed by a word that is printed only if the listing command succeeded (`TREE-LISTED`, `CONTAINERS-LISTED`, ...) | `r3_no_count_can_hide_a_failed_command`; rehearsal |
| D1 the disk | the Mac: 16 GiB free | `tools/vfrun.py`: before a run the free space of the home folder's file system must be at least the floor (`--disk-floor-gib`, 8 on the runbook's commands); during a run it is read every 15 s and, below the floor, vf-eval gets the one SIGTERM of the stop path; the reason goes to the log and to `<run>.stopped.json`; status 97; nothing is deleted. The runbook has rule 7, a disk command in step 0 and the same check in front of the three starts of step 1; step 3 names the lead's decision about Docker Desktop's limit | `host_disk_*` (5), `box_watchdog_*` (3), `box_command_form_is_refused_under_the_floor`; rehearsal: a refusal at the runbook's own 8 GiB and a stop during a rollout |

Also changed: steps 2c and 3 start their rollout through `tools/vfrun.py --config ...` (the allow-list, the floor
and the stop path are in that tool; a session can no longer start vf-eval with its whole environment); the three
rules of the round-2 GO notice are in the body; the dry run of step 3 is behind the lead's file; the lead states
the price in the go message; the checkout belongs directly under the home folder; `tools/check_safety.py` and
`tools/check_interrupt.py` follow the new stop semantics; `redteam/rt_run.py` one line.

Tests on the new code, none of which kills or deletes on a host: `tools/check_round3.py` 48 of 48
(`results/round3_checks.json`: 22 pure checks under tripwires, 8 traces of a made-up credential file, 18 with
real signals inside one throwaway container without a mount); `tools/check_safety.py` 36 of 36 under its 65
tripwires (`results/safety_host_round3.json`); `tools/check_interrupt.py` 8 of 8 (containers;
`results/safety_interrupt_round3.json`); `tools/check_runbook.py` 46 of 46 on the new text
(`results/safety_runbook_round3.json`); `tools/pin.py --check` 109 files, 0 differences. NOT run again:
`tools/check_units.py`, `tools/check_driver.py` (the driver and its guard did not change: `physim2_env/public/`,
`grading.py`, `taskset.py`, `access.py` are byte for byte those of the round-2 pin), `prove.py --worlds 4`, the
gliders rollout, the red team's attacks.

### 8.10 The third rehearsal

From a fresh sparse clone of commit 00947b226 (the round-3 code with its new pin), in the cloud container, 10 Nov
2026, 20:01 to 20:37 UTC. `results/rehearsal_round3.json` holds the literal text and the complete output of each of
the 65 commands (79 entries with the operator's notes and the three actions that are not runbook commands), 24
of them status commands. Each command was issued as ONE `sh -c '<text>'` started in `/`, by `rehearsal/issue3.py`.
New in this round: `$HOME` was not replaced in the text. The rehearsal's home folder was given to every command
as the variable `HOME`, in an environment built from `PATH`, `HOME`, `USER` and `LANG` only, so that the commands
ran byte for byte except for the study path, the pid and name placeholders, and the disk floor (this machine has
1.8 GiB free for everyone: `8` became `0.5` where a command had to run).

- **Steps 0 and 1.** The hash, the path and `TREE-LISTED`; the pin hash and `PIN-OK`; `6 names, 0 refused`, the
  context and its socket (here `default` at `/var/run/docker.sock`); the sentinels of the Docker and folder check.
  The same session check with `DOCKER_HOST` and `PYTHONPATH` set on purpose: two `FOUND` lines, `8 names, 2
  refused`. The disk command at the runbook's own floor: `refused: 1 GiB free ...`. The dry run (refused at 8 GiB
  before uv started; then the four expected lines), the pilot folder with mode 0700, the detached `uv sync
  --locked` with the pinned build backend (`EXIT 0`), the import check ending in `stand-in`, the interpreter
  check, the image check, the instance.
- **A stop by the runbook's own command.** With `TOOL`, `VF-EVAL`, `LAB` and a box listed, the stop command was
  aimed at the waiting shell's pid on purpose: nothing printed, nothing signalled. Aimed at the tool: its command
  line, and 6 s later no process and no container; the log ended with the traceback, `KeyboardInterrupt` and
  `EXIT 130`. Reset, new instance.
- **A hard kill.** vf-eval was killed with SIGKILL while its box was up. The tool ended with `refused to go on:
  vf-eval died of signal 9. Its containers and its laboratory process may be left. ...` and `EXIT 98` (round 2:
  it went on and ended with `EXIT 1`). The status listed the box and one `PROBE` line, verifiers' own port probe,
  which stayed for about four minutes and then was gone; no laboratory (Linux). The removal command printed
  `error: no such object` for a name nobody has, nothing for a container of the rehearsal's own that carried
  another run label (it was still there afterwards), and the label and the name for the pilot's box, which it
  removed. Reset, new instance.
- **The disk watchdog, twice.** Before a run: the 2a command exactly as the runbook has it, floor 8 GiB:
  `refused: the disk watchdog did not start the tool: 1.78 GiB free ..., the floor is 8.00 GiB. Nothing was
  started and nothing was deleted.` and `EXIT 97`; no run folder. During a run: 2a with a floor 24 MiB under the
  free space of the moment; when its rollout ran, 48 MiB were written to the scratch. One second later the
  watchdog found 1.73 GiB under a floor of 1.75 GiB: one SIGTERM to vf-eval, which removed its box and stopped
  its laboratory; `refused: stopped by the disk watchdog (...): SIGTERM. ... nothing was deleted.`, `EXIT 97`, and
  `proof-d.stopped.json` with the reason. The run folder was still there.
- **The clean pass.** 2a in 7 minutes: all graded, 0 failed items, ticks D 392, P0 0, C 0, one box per item with
  identical scores (64 boxes, 2.44 s each), table O 1.065, D 0.377, P0 0.951, C 1.0 (`rehearsal_round3_proof.json`);
  C was built from the 0600 file. 2b: 37 rollouts in 1,177 s, round 5's checks 32 of 34 with none failed, the new
  checks 66 of 66, among them the proxy asked for the worker's four loopback names: `HTTP 403` eight times and no
  connection on the listener (`rehearsal_round3_probe.json`). 2c: one rollout through `tools/vfrun.py --config`,
  every expected field of the report. Step 4: five files copied, both folders removed, no container.
- **The credential file.** The rehearsal's home held a made-up `.prime/config.json`. `rehearsal/watch_open.py`
  asked the kernel for every open of it from before step 0 until after step 4: **0 events** in 45 rollouts (42
  finished, 3 cut) and every tool. The control afterwards, the stock import of verifiers with the same home: 3
  events (open, read, close). In step 2b the laboratory scrubbed exactly one token-like variable from its
  environment, the canary the tool gave it; before round 3 every such name of the session reached it.
- **Hidden values:** 0 hits of the 8 needles of the clean pass's store in the record.
- **Mismatches between the text and what happened** (prose corrected afterwards; the 33 commands are byte for byte
  the rehearsed ones): the removal command prints Docker's `error:` line for a name nobody has; a `PROBE` line of
  a killed vf-eval stays for minutes and shows up in the status of the next start; with a very long study path
  the 160 characters of a status line hold the path only, and the word in front is what tells the process.
- **Deviations forced by the machine:** a sparse clone; root on x86_64 behind a proxy; context `default`; the
  shared image exists already, so the image build and its status were not issued; the lowered floor; uv's cache
  and uv's own Python pointed elsewhere for the two uv commands; the rehearsal went on after each interruption
  and after the watchdog stop, where the runbook says stop and report.
- **Not rehearsed:** the image build; all of step 3 (its two start commands are new); point 4 of the interruption
  section (no laboratory or helper was left without its vf-eval here); the "once" rule and the 60-minute bound as
  rules; anything on macOS.
- **Found before the rehearsal, by a pre-test in the fixer's worktree,** and fixed: a helper started by a tool
  refused the tool's own child environment; the prime-runs SDK read the credential file for a disabled run (the
  second reader of 8.9, M3).

### 8.11 What remains

- A re-audit of round 3 (the diff of the pinned files, and the runbook), then a verdict. Until it says GO, nothing
  runs on the Mac. For the re-audit: the rehearsed commit and the sha256 of `PIN.sha256` are in
  `results/host_safety_round3.json`.
- Nothing ran on macOS or Docker Desktop. New inferences of round 3: the system `awk`, `df -Pk` and `docker
  context` there; that a laboratory outlives a killed vf-eval there; that uv 0.12 reads the build constraints of
  this `uv.lock` as uv 0.11.32 does.
- The laboratory still has no bearer (m7): for step 2 the rule "no other container runs" stands in for it; for
  step 3 it is an open condition.
- Step 3 is unrehearsed, and its two start commands are new. The lead decides about Docker Desktop's disk limit
  before it; the watchdog stops a run at the floor but cannot give space back.
- The stand-in for the credential readers rests on two names inside other packages
  (`verifiers.v1.utils.prime.load_prime_config`, `prime_traces.core.config.Config._load_config`); both are pinned
  by `uv.lock`, and `tools/vfeval.py` refuses to start a scripted run if either is not in place. Two more modules
  can read the file (`prime_sandboxes`, `prime_tunnel`); a Docker rollout does not reach them.
- The build constraints pin versions, not hashes.
- Open from the earlier rounds, unchanged: N5 to N8 on Linux hosts (8.5); the guard rests on Docker conventions; a
  vf-eval killed outright leaves its containers (found by label, removed by exact name after the label is read
  back); in step 3 an untrusted model is root in a container for an hour and Docker Desktop's virtual machine is
  the only wall; round 5's `agentenv/mac/` files, which the never table names.
- Rules that stand: no tool or test of this folder may run the cleanup on a host; a host test installs
  `tools/tripwires.py` before it imports the package; a real cleanup or a real signal is tested in a throwaway
  container without a host mount.

### 8.12 Round 4, step 3 and host safety (11 Nov 2026; not audited yet)

Why: the first two model rollouts ran in the cloud container from the round-3 pin (`../rollouts/`). The mechanics
worked; the exam and the runbook's step 3 did not hold up (a turn cap the statement never named, a failed
submission paid better than the honest baseline, a price bound that was wrong by a factor of forty, an open
laboratory port, a harness that installed unpinned packages in the box). The Mac then became available, and its
session set a protocol: rollouts are requested by files (schema `rollout-job/v1`), executed one at a time by
following `RUNBOOK_MAC.md`, step 3, and published as a folder. Two agents changed the code: the exam side is
section 8.13; this section is step 3 and host safety. Evidence labels: READ, TRIPWIRES (run on the host with
every destructive primitive replaced), VF-EVAL (run through vf-eval in containers that verifiers started, in the
cloud container, run label `physim2-port4b`), INFERRED. Results: `results/round4_step3.json`.

| # | what | where | evidence |
|---|---|---|---|
| 1 | **The laboratory's bearer.** 256 random bits per rollout, drawn in vf-eval at set-up, handed to the laboratory over verifiers' state channel and to the box's proxy in memory; in no environment, command line, file or box; the laboratory's record holds its sha256. Without it `401` and an empty body before the laboratory's code is reached; DNS-rebinding protection on again (`421` for another Host, `403` for a foreign Origin); a laboratory without a bearer serves nothing | `physim2_env/bearer.py`, `lab_tools.py` (`_serve`), `runtime.py` (`BearerEgressProxy`), `access.py` | TRIPWIRES B1 to B18; VF-EVAL R16 to R21 (asked from the host while a rollout ran; searched for in the box's processes and files, in the laboratory's command line and environment, and in every output) |
| 2 | **Box caps in code**, no Docker Desktop setting: 2 CPUs, 4 GB without swap (a request may lower it), 512 processes, a read-only root, memory-backed `/workspace` (1 GiB) and `/tmp` (512 MiB) as the only places a box can write, read back from the engine before a box is used. One code path for the agent's box, the grading boxes and the reference policies' boxes. A box cannot write to Docker's disk | `physim2_env/boxcaps.py`, `runtime.py`; the in-box guard allows the four tmpfs mounts (`public/_item.py`, fixer A) | TRIPWIRES A1 to A16; VF-EVAL K1 to K12 (`agents/probe_caps.py` hits each cap from inside a box; the rollout is still graded) |
| 3 | **The spend stop.** Every HTTP attempt to the provider is admitted, counted and priced in vf-eval; a call is sent only while counted + in-flight worst cases < `cap_usd`; anything without complete usage counts as one worst-case call; `max_context_tokens` bounds each prompt before it is sent; a stop ends the run through verifiers' own stop path, so the submission is graded. Bound on the bill: `cap_usd` + one worst-case call | `physim2_env/spend.py`; hooks in `taskset.py`; prices and bounds in `tools/check_request.py` (`prices_of`, `bounds`) | TRIPWIRES C1 to C40 (verifiers' own client against a stand-in endpoint in the same process); VF-EVAL R9 to R15 |
| 4 | **Step 3 is driven by a request** and repeatable: fetch, check, instance, reference, dry run, rollout, (close), publication. The lead's go is one standing file with a ceiling and a date; the ceiling is one total across machines (`--shared-ledger`); a job, an instance name and a config name are used once; one rollout at a time | `tools/vfrun.py` (`request_route`, `close_job`), `tools/check_request.py`, `RUNBOOK_MAC.md`, step 3 | TRIPWIRES D6 to D24, D36 to D39; VF-EVAL F1, F2, R1 to R27 |
| 5 | **The strict config schema**: flat TOML, known keys only, the expansion compared with what the pin fixes (the image's preinstalled `bash` harness, no retries, `push = false`), a list of fields that may appear nowhere. The runner reads its copy of the one file; nothing is written into the checkout | `tools/check_config.py`; the schema itself is fixer A's `physim2_env/rollout_config.py` | TRIPWIRES D1 to D5, D22d |
| 6 | **The publication folder**: status, transcript, redacted trace, laboratory log, grades per item, reference table, usage and cost per call, the frozen submission, a manifest with sha256 and size, the pilot marker, a key scan by value (from the environment) and by shape; a file with a hit is left out and listed | `tools/pack_rollout.py` | TRIPWIRES D25 to D35; VF-EVAL R24 to R26 |
| 7 | **A crash in the middle of a model rollout**: what it leaves, the clean-up, and stage `close`, which writes the job's closing row only when nothing of the job is left | `RUNBOOK_MAC.md`, "If a run was interrupted", point 8; `tools/vfrun.py` (`leftovers`, `close_job`) | TRIPWIRES D36 to D38 (made-up process and container listings); not produced for real |
| 8 | **Section B of the runbook** as the inventory for steps 1 to 3: who holds the key and for how long, every listener, signal, deletion, in-place replacement, file left, network destination | `RUNBOOK_MAC.md`, section B | READ (code and verifiers 0.3.2.dev163); the destinations of a model run were not measured at the socket |
| 9 | The Mac review's minor findings | the table below | |
| 10 | The default model id is `qwen/qwen3.6-35b-a3b` (`physim2_env/rollout_config.py`, the runbook's example); the old `configs/qwen_ring_bash.toml` is no longer used by anything | | READ |

What the Mac's runner asked of the spend stop, and the test of each line: (1) missing or partial usage, a stream
without a usage chunk, an error reply: one worst-case call (C6, C25 to C30); (2) every HTTP attempt counts:
verifiers' client does not retry (`clients/base.py:14-16`), the config allows no retry, a retry of the harness is
a new counted request (C27; D4 "a retry"); (3) cache reads at the full input price unless the saved entry lists
one (C3, C4, D15b); (4) counter and stop on the host only, one counted client, no model call without a meter
(C36 to C39); (5) prices and window from the listing at run start, saved as `model_entry.json` (D13, R9, R24);
(6) `max_turns` is always set and compared with the config (D1, D4); (7) `max_context_tokens` mandatory and
enforced before each call (D2, C17, C34, C35); (8) the acceptance rule and the bound are in the runbook, the
count per call and in total is in the publication folder (D30, R25).

Bounds for the default config (150 turns, 8,192 tokens per reply, a context cap of 200,000, `cap_usd` 1.00;
prices of 11 Nov 2026: $0.11 in, $1.01 out, window 262,144): one worst-case call $0.0303; bound on the bill
$1.0303; crude bound without the spend stop $5.57.

**The Mac session's minor findings on the round-3 pin** (identifiers only; the review itself stays private).
closed = changed in code or text at this pin; accepted = stated in the runbook as a fact of the route; deferred
= not done, with the reason.

| finding | status | what and where |
|---|---|---|
| SIG-2 | closed (text) | runbook B, signal table: the pilot's own deadlines are named as occasions on which a `docker` client is killed |
| SIG-3 | closed (code) | `tools/vfrun.py`, `stop_child`: one SIGTERM per child however often the tool is signalled; the wait goes on to the same deadline, then SIGKILL |
| R3-8 | closed in part | same function: the tool no longer leaves vf-eval behind when it is told to stop twice. The tool's own short `docker` clients can outlive it for up to 60 s (they end by themselves); said in "If a run was interrupted", point 7 |
| INV-7 | closed (text) | runbook B, signal table: the row for Python's asyncio and the laboratory |
| DEL-1 | accepted | runbook B, deletion table: the laboratory's working folder has a random 48-bit name; a collision cannot be arranged from a box |
| DEL-2 | closed (text) | runbook B: the new table "What is replaced in place" |
| DEL-3, INV-6 | closed (text) | runbook B (written and left) and "If a run was interrupted", point 7: the bundle and network temp folders; clients outside the status listing |
| DOCK-4 | mitigated, guard unchanged | the in-box guard is fixer A's file. A box of this pin cannot carry a file mount: `boxcaps.cap_run_argv` refuses a box command with any option the pin does not expect (A9), and the started box is read back |
| DOCK-5 | accepted | runbook B (written and left) and C: an existing helper image is used as it is; the lead looks for it by hand |
| network paragraph | closed (text) | runbook B, Network: Debian's mirror in the build stage, Alpine's mirror for verifiers' helper image |
| CRED-2 | accepted, in part closed | `docker` clients of vf-eval start without credential-like names (`runtime.docker_client_env`); the client's own config file (credential helpers, a `proxies` section) is a by-hand check in C |
| CRED-4, CMD-14 | deferred / accepted | the build backend stays pinned by version (uv.lock has no hash for build requirements; changing the build is outside this round). That the runbook's direct commands run with the session's whole environment is said in B |
| CRED-5 | closed (code) | row 1 above |
| R3-7 | closed in part | `DYLD_*` joins the names no tool starts with (and step 0's list); `PATH` and the direct commands are said in B |
| G1 detail | closed (code) | `PYTHONEXECUTABLE` and `__PYVENV_LAUNCHER__` are refused by the tools and looked for in step 0. `python -E` or `-I` was not adopted (untested here) |
| RB-6 | deferred | needs the Mac: listed in the runbook's last section (a detached command and the end of a session) |
| RB-7 | closed (text) | step 0: a value with a line break can add a line, never hide a name |
| RB-8 | closed (command) | step 0 lists ignored files too (a bytecode cache, an old environment) and no longer writes git's index |
| INV-9 | closed (code, fixer A) | `tools/prove.py`: the cross-check with round 5's grader is off unless asked for; the runbook's command still carries `--no-cross-check` |
| INV-3, R3-9 | accepted, in part closed | runbook C: 11 GiB before step 0; the watchdog measures the home volume, Docker's disk image must be on it. Nothing watches the disk DURING `uv sync`, the image build and the helpers: each start checks the floor, and what they write is bounded (about 3 GiB). A box no longer writes to Docker's disk at all |
| INV-5 | closed (text) | runbook B, the key table: the scrub of the laboratory's environment block is Linux-only; the model key never reaches the laboratory on any system |
| INV-8 | closed (text) | runbook B, listeners: the 104-byte limit of a socket path |
| NEWC-1 | closed (code and command) | the reason of a stop is written before the stop begins (`run_child`, `on_stop`); a second signal during the stop changes nothing; the reset command of point 6 refuses below the disk floor |
| RB-1 | closed (text) | rule A.2: the shapes a pid and a container name must have before they are put into a command |
| RB-9 | closed (text) | runbook C and step 0: 11 GiB |
| CRED-1 | closed (text) | the folder of step 3 is directly under the home folder; C keeps the row about synced folders |
| DOCK-3, INV-4, INV-2 | closed | the rule "nothing else runs in Docker" is repeated before 2b, 2c, the reference table and the paid command; the laboratory needs its bearer; stage `close` refuses while a laboratory of the job's instance is alive |
| DOCK-1, RB-4, R3-1, RB-5 | closed in part | every tool start checks that the Docker context names a local Unix socket (`require_docker`); the builder is not pinned beyond step 1 (deferred: the image is built once, by one command) |
| R3-3 | accepted | runbook B and "If a run was interrupted": status 130 after a stop by signal |
| RB-3, R3-4 | closed (code) | the tools refuse a bad environment before the package is imported (`require_clean_environment` first) |
| CMD-5, RB-2, SIG-1, R3-2, R3-5, INV-1 | deferred | the appendix names them without their text; they wait for the Mac's own re-review of this pin |
| the list "not covered by anyone" | deferred | outside this study's reach from the cloud container; repeated in the runbook's last section |

What remains after this round, for the integrator and the verdict: `PIN.sha256` and the runbook's pin block (not
regenerated here); a rehearsal of the runbook's commands as `sh -c` lines, steps 0 to 2 and the free part of
step 3 (the last section of the runbook lists what was not issued as written); one model call through the new
route to see the provider's usage fields, the explicit `[client]` table and the destinations of vf-eval; a real
interruption of a model rollout; everything about macOS.

### 8.13 Round 4, the exam side (fixer A; summarised from that agent's handoff, not re-derived here)

Rulings E1 to E16 of the coordinator (`../../roadmap/DECISIONS.md`): whatever is in `submission/` when a run ends
is graded, however it ends (`physim2_verifier`, a 49-line env that also grades the last checkpoint of a FAILED
run; `physim2_env/capture.py` is the one writer of box content on the worker); the box starts with the null
baseline in `submission/`; a failed item is scored as the null policy, never as K; the task statement is
rendered per run with the turn, time, reply, context and spend limits and the box as measured; the Lab client
logs every reply to `/workspace/lab_log.jsonl`; `lab.usage()` reports time and turns; the ring profile uses
`ring_r4` (256 samples per item, a reset costs 17 ticks); the image `physim2-ring:2` holds the `bash` harness
preinstalled from hashed pins behind a stand-in for `uv`, so a box fetches nothing at set-up; a rollout config
is a flat file (`physim2_env/rollout_config.py`), a profile fixes world, exam config, image, box and reference
policies (`physim2_env/profiles.py`). Proof: `results/round4_exam.json` and `tests/` of that agent.

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
- No re-audit of the host-safety changes, and no rerun of the 4-world table, the gliders rollout or the red team's
  attacks after them (section 8).
- Gliders: one scripted rollout (policy D) on one fresh gliders world with the smoke config, on the fixed code and
  with one box per item: graded, 0 failed of 8 items (`results/gliders_smoke_D.json`). Nothing else was run on
  gliders.
- The one-box mode's channels are measured, not closed: closing them inside one box would mean resetting kernel
  counters a container cannot reset.
