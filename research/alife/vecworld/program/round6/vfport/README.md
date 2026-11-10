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
results/                proof_ring.json, probe_ring.json, summary.json
RUNBOOK_MAC.md          install, scripted smoke test, one cheap model rollout
```

Round 5's code is reused BY IMPORT from `../../round5/agentenv` (set `PHYSIM2_AGENTENV` to point elsewhere), so the
package is installed from a checkout, not from a wheel. Of agentenv's 3,670 lines outside `results/`:
LINES_PLACEHOLDER

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

PROOF_PLACEHOLDER

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
   What this does NOT cover: a harness that dies (a model can kill its own harness process). verifiers then
   skips finalize and scoring, and that rollout has no reward. The operator rule stays: no retries, no resume,
   an ungraded rollout counts as K (`tools/vfrun.py: rollout`).
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

## 6. Not done

- No model rollout: the stock harnesses (`bash`, `claude_code`, `codex`) were not run. The stop hook
  `Physim2Task.frozen` (end the rollout at the next model call after a submit) has therefore never fired.
- Nothing on macOS: the network cut there uses a different path (memo unknown 4). RUNBOOK_MAC.md, step 2.
- No sealer, no private Hugging Face store, no hash check of downloaded data (memo holes 5 and 6 only as far as a
  local store goes). No compute-budget metering (the cgroup CPU counter of each box is read and reported, nothing
  is enforced). Gliders: GLIDERS_PLACEHOLDER
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
