<!-- Provenance: produced on 10 Nov 2026 by a workflow of eight agents (four readers: verifiers scoring, verifiers
runtimes, the PhySim v1 environment, the v2 agent environment; one synthesis; two independent reviews, one refuting
the claims about verifiers and one attacking the recommended architecture; one editor who re-read every cited line).
Verifiers version read: 0.3.2.dev163, commit a24f5e21, the one the PhySim v1 environment pins. Asked for by the lead
under decision 5 (DECISIONS.md). Nothing in it has been run; section 6 lists the tests. -->

# Grader: what verifiers already provides

10 Nov 2026. Prefixes: V/ = pinned `verifiers/v1/`; iv.py = `V/envs/isolated_verifier/env.py`; docs/ = `docs/v1/`; E/ = PhySim v1, `environments/physim/`; A/ = `round5/agentenv/`; R/ = `roadmap/`. The editor read every cited line; "(inferred)" marks a conclusion nobody ran.

## 1. Answer

Yes for the machinery, no for secrecy, and the stock grader is safe for us only with the fixes in section 8.

- Verifiers ships an isolated grader (`--env.id isolated-verifier`, docs/env.md:25): the agent finishes, the declared paths and `/logs/artifacts` are copied out, the agent's box is destroyed, and the task's scoring code runs against a fresh container (iv.py:63-70, 105-122, 148-178; V/utils/artifacts.py:63-79; V/rollout.py:558-560).
- Tool servers run outside the agent's box by default, where the Lab belongs (V/mcp/toolset.py:16-19).
- It has no Hugging Face or sealing code; a task row is saved and, by default, uploaded (table).

Shipping agentenv unchanged would reinvent about 760 of its 3,667 lines and keep the answers on the agent's machine behind process isolation, with open network (A/evaluator/sandbox.py:83-100; A/mac/RUNBOOK.md:104-105). PhySim v1 hand-built its grader from verifiers primitives instead (E/physim/runtime_sandbox.py:59-71; E/physim/taskset.py:616-627; grep of E for `isolated`: no hit). Adopt the stock environment and port v1's per-item worker into it.

## 2. Table

| Part of our hidden side | What verifiers provides (file:line) | Left to us |
|---|---|---|
| Sealed answer store | Not provided. grep for HF_TOKEN, hugging, hf_hub, load_dataset, push_to_hub over the verifiers package: no hit. grep for commitment, sealed, sealer, salted over V/, docs, skills: only comments about a "sealed" trace (V/interception/server.py:384; V/session.py:167). Convention only: host code loads private data (docs/env.md:43-48; the checkout's environments/gsm8k/gsm8k/taskset.py:64-67), and the row carries a pointer because the row is saved in every trace (V/task.py:3-4; V/rollout.py:87-93). | Sealer, loader, hash check. Existing pieces: secret commitment (A/evaluator/instance.py:80), per-file hashes (E/physim/hub.py:79-84), v1's pointer row (E/physim/taskset.py:419-425). v1's downloader passes no token (E/physim/hub.py:37-46), so a private repo fails as written (inferred). |
| Read token | Not a feature. Containers receive only passed variables (V/runtimes/subprocess.py:26-29; V/runtimes/docker/__init__.py:226-230); nothing is forwarded by default (V/configs/harness.py:30-33). Host child processes inherit the worker's environment, except names containing API_KEY (subprocess.py:104, 151). `harness.env` is saved on every trace (V/trace.py:107-109; rollout.py:97); `Task.runtime_env()` enters both boxes (V/task.py:177-179; rollout.py:214-216; iv.py:162-166). | Token in the worker's environment only (holes 4, 5). The standing rule keeps tokens on the Mac (R/DECISIONS.md:80-81), so any other worker takes a token off it. |
| Lab service | Placement and transport. A Toolset runs outside the agent's box by default, one host process per rollout (V/mcp/toolset.py:16-19; V/mcp/launch.py:420-423; rollout.py:270-279). It receives the task row over a private channel (V/mcp/server.py:202-219; V/interception/server.py:1000-1013). It stops before finalize and is absent during grading (rollout.py:484-500; iv.py:111-122). It can instead be an already-running `url` (toolset.py:19; launch.py:615-618), which v1 forbids (E/physim/taskset.py:453-454). v1 precedent: E/physim/taskset.py:299-345. | Wrap LabService as one tool (hole 2). |
| Lab budgets (ticks, nats, attempts) | Not provided. Tool state is synced whole, last writer wins (V/mcp/server.py:221-247). Stop hooks run before each model call (V/session.py:587-589), so `submit` ends a model harness at its next call (inferred). | Ours: A/evaluator/lab_service.py:128-137, 143-153, 163-170. |
| Agent's sandbox | Docker or Prime container with no host mounts (docker/__init__.py:196-244). A row with `network_allow=[]` gets framework routes only, applied after setup, and is refused where it cannot be enforced (V/task.py:106-109; V/utils/compile.py:45-56; V/configs/runtime.py:57-81; rollout.py:280-282). Without it the network is open (runtime.py:60-62). `NEEDS_CONTAINER`, a row image and artifact collection each refuse the subprocess runtime (V/task.py:145-146; compile.py:31-36, 107-109; V/agent.py:440-445). | Declare all three on the task (hole 4); select Docker. |
| Collection of the submission | Declared paths plus `/logs/artifacts` (V/task.py:115-121; V/utils/artifacts.py:63-79), collected after finalize (rollout.py:501-506), 32 MiB default cap (artifacts.py:23), validated on the host as untrusted before restore (artifacts.py:139-157). A timed-out agent is still collected and scored (rollout.py:177-181, 490). | Declare `submission/`, not required (hole 3); raise the cap to our 64 MiB (A/evaluator/instance.py:34). `validate` becomes a public script (its examples are public, A/evaluator/instance.py:122-126), or the Lab reads the agent's box as v1 does (E/physim/runtime_access.py:1-6). agentenv's own snapshot checks for symlinks in one pass and opens files in a later one (A/evaluator/submission.py:36, 50), a race this path avoids (inferred). |
| Execution of the predictor | One fresh container per grading attempt (iv.py:148-178). Its network is cut before scoring only under a restricted policy, and is open during setup, restore and staging (iv.py:169-173; docker/__init__.py:309-317, 415-416). A scoring exception reruns the whole verifier, three attempts in all (iv.py:36-38, 134-182). Not provided: separation between items, an unprivileged user, process limits (docker/__init__.py:527-535; grep for RLIMIT, ulimit, cgroup, getrusage, pids-limit, cpu_seconds over V/: no hit). | v1's worker and launcher (E/physim/container_worker.py:14-19; E/physim/runtime_sandbox.py:156-179) plus per-item cleanup (hole 1). submission/ root-owned and read-only. No submitted code runs in setup or staging. |
| Scoring arithmetic | Hook only: `@vf.reward` functions run in the worker process with a handle on the fresh box (V/task.py:223-225, 253-269; iv.py:121-122). Model-backed judges are refused (iv.py:64-68). | Ours: A/evaluator/instance.py:153-160; A/evaluator/grader.py:45-56. |
| Reference table (K, D, P0, PM, S, C, O, sigma, rho) | Not provided; verifiers records per-rollout rewards and metrics (V/trace.py:407-411). | Ours: grader.py:77-103; A/evaluator/acceptance.py:34. |
| Trace recording | Every episode is appended to traces.jsonl (V/utils/trace_store.py:22-29). `trace.info` and error tracebacks are saved; only `state` is excluded (V/trace.py:412-417, 765-779). No redaction hook (grep for redact, scrub, sanitiz over V/: unrelated hits in dialects/anthropic.py and harnesses/openclaw/harness.py). Upload is on by default, and each whole episode record is sent as it finishes (V/configs/cli/eval.py:116-119; V/cli/eval/runner.py:135-145; site-packages/prime_runs/projection.py:101-116). agentenv leaves transcripts and token counts to the harness (A/mac/RUNBOOK.md:93-95). | `--no-push` on sealed runs (hole 6); the Lab's request log stays on the worker. |
| Time and compute limits | Per-stage timeouts (rollout.py:41-52), turn and token caps (V/session.py:83-115), cores and memory (V/runtimes/container.py:29-32; docker/__init__.py:197-200). Prime defaults: 1 core, 1-hour idle timeout (V/runtimes/prime.py:90-99). No CPU-seconds meter (same grep as above). | Calibration benchmark; a cgroup meter if readable. |
| Scripted agent for the end-to-end proof | Not provided. The 13 stock harnesses are model agents (`ls V/harnesses`; by name, inferred; `null` read, V/harnesses/null/harness.py:39-53). `vf-validate` and `vf-debug` run no model but serve no tools (V/cli/validate.py:241-300; V/cli/debug.py:197-244). | A scripted harness, about 60 lines (estimate). |

## 3. Recommended architecture

- **Private Hugging Face repo, at rest:** hidden parameters, noise secret, exam items, truths, reference runs. Salted hashes stay public (R/DECISIONS.md:74-76).
- **Trusted worker:** the machine running `vf-eval`, sole holder of the read token. Rollouts and rewards run in its process (V/cli/eval/runner.py:3-6); the Lab is a Toolset, one host process per rollout (V/mcp/launch.py:420-423).
- **Agent box:** a container with TASK.md, public physim2 and an empty submission/; its only ways out are the model route and the Lab's URL (V/rollout.py:280-282). Changed: network and container rules are declared on the task row, because verifiers enforces declared rules on both boxes, while the grader's cut (iv.py:173) does nothing under the open default (section 8, hole 4).
- **Verifier box:** fresh, network cut before scoring. It gets the restored submission/ and, via `stage_verifier` (V/task.py:187-189), the public runner; truths never enter it (unlike docs/env.md:43-53). Replies are scored on the worker; a failed item scores K (A/evaluator/grader.py:45-56). Changed: the reward sends one item request at a time and cleans up in between, because one box serves every item and a staged set could be read whole (hole 1).
- **Sealed runs.** Changed: `--no-push`, no `--resume`, no retries, because upload sends whole episode records and a rerun gives the agent a fresh Lab budget (holes 3, 6).

Runtime first: Docker on the Mac, selected explicitly (the default is Prime, V/configs/agent.py:34); this cloud container has no Docker daemon (A/mac/compose.yaml:1). Prime second (hole 7).

You decide:
- **Whether the worker is the Mac.** The standing rule keeps tokens on the Mac and lets exam data pass through but not stay (R/DECISIONS.md:80-81, 85-86), so the worker's cache would be wiped after each run.
- **Whether pilot runs upload to Prime's platform.**

## 4. Keep, wrap, drop

Of 3,667 lines:
- **Drop, about 760:** sandbox.py (139), run_rollout.py (230), socket server (A/evaluator/lab_service.py:230-295), physim2/wire.py and labclient.py (169), mac/ compose and Dockerfiles (49), tests_tcp.py (45), snapshot and launch (A/evaluator/submission.py:27-91).
- **Wrap, about 530:** LabService (lab_service.py:43-227) as a Toolset; build_workspace.py (112) from Task.setup; the grading loop (A/evaluator/grader.py:34-64) as the reward; prove.py and check_probe.py (205) re-driven through `vf-eval`.
- **Keep, the rest, about 2,370:** instance.py, acceptance.py, the table (grader.py:77-103), validation checks (submission.py:94-125), world modules, predict_runner.py, TASK.md.tmpl, agents, configs, study scripts, documents.
- **New, about 750 (estimate):** taskset, sealer and loader, predictor launcher with per-item cleanup, scripted harness.

## 5. Not provided; we build

Five things, with the evidence in the table: a sealer and private-store loader; record hygiene (pointers on the row, nothing truth-derived in `trace.info` or exception text); per-item isolation and process limits for the predictor; a compute budget in simulation units (R/DECISIONS.md:45-47); a scripted, model-free agent.

## 6. Unknowns and smallest tests

Each costs $0 on the Mac unless noted.
1. **Host-side Lab under isolated-verifier?** Setup reruns in the verifier box (iv.py:115-116, 157-158), where v1's would fail (E/physim/taskset.py:466), and the Lab has stopped (rollout.py:485). Test: ring smoke exam as a taskset, Docker, scripted harness, four worlds. Pass if it reproduces the ring table and the 34 boundary checks (A/README.md:55, 61-63), and a probe predictor finds on item 2 neither the file nor the background process it left on item 1.
2. **Lab callable from the agent's Python (A/mac/RUNBOOK.md:93)?** Probably: its URL is on the agent program's command line and needs no credential (V/harnesses/utils/launch.py:60-71; V/mcp/server.py:301-331; inferred). Test: a script in run 1 calls `usage`; then each stock harness once with Qwen, cents.
3. **Token or answer leak?** Test: throwaway private repo with a canary; a probe dumps environment and files in both boxes; grep traces.jsonl.
4. **Network cut on macOS Docker (V/runtimes/docker/__init__.py:224-225, 431-446)?** The probe's network checks in run 1, both boxes.
5. **CPU metering?** JAX exceeded its thread cap (A/README.md:92). Test: simulator benchmark in the box, reading the cgroup CPU counter.

Unread by anyone: Prime internals and tunnel code, the codex and prime-agent harnesses, upstream changes since our pin (E/README.md:23-30).

## 7. Effort

1. Port and smoke on the Mac (unknowns 1, 2, 4; holes 1 to 4); the checker recomputes the table from saved per-item scores.
2. Sealer and private store (unknown 3; hole 5), in parallel; needs your repo and two tokens (R/DECISIONS.md:77-79, 93-94).
3. Compute budget and predictor limits (unknown 5), after 1.
4. Model rollouts, after 1: Qwen on the ring, the gliders dry run, Astra.
5. Optional: Prime for 8 to 24 hours.

Before the first real-model rollout: study 1, checked (R/DECISIONS.md:55-56); Qwen runs on the verifiers taskset, not the never-run compose route (A/README.md:90). Before any quoted rollout: studies 2 and 3 too (R/DECISIONS.md:88-91).

## 8. Open holes

Most severe first, each with its cheapest fix.

1. **One grading box serves all items.** Staged together, all 64 histories are readable at once: 64 x 17 true-world observations, 2.7 times the ring smoke Lab budget (A/physim2/world_ring.py:44; A/physim2/predict_runner.py:7; A/configs/smoke_ring.json:2-3). A predictor can also leave files or a background process for later items (docker/__init__.py:527-535; inferred). Fix: one request per call; v1's unprivileged user (E/physim/runtime_sandbox.py:156-161); between items, root kills that user's processes and wipes its writable paths.
2. **A naive Lab port.** MCP returns a tool exception's text to the agent (site-packages/mcp/server/mcpserver/tools/base.py:173-181); parallel calls undercount budgets kept in verifiers' shared state, where the last writer wins (V/mcp/server.py:224-225). Fix: one tool calling `LabService.handle`, which locks and hides internal errors (lab_service.py:200, 215-217), inside v1's wrapper (E/physim/taskset.py:308-338).
3. **Self-selected re-roll.** Deleting submission/ fails the rollout, ungraded (artifacts.py:124-130; iv.py:107); `--resume` or retries rerun it with a fresh Lab (V/env.py:172-176; V/configs/retries.py:11-13; rollout.py:270-279). Fix: `Artifact(required=False)` (artifacts.py:34); the reward scores K and never raises; a rollout without scores gets K and its name cannot be reused, as now (A/run_rollout.py:66-67, 103-108); no retries or resume on sealed exams.
4. **Operator settings.** The agent cannot change them, but one wrong value loses everything: an open network, a Lab placed inside the agent's box (`colocated`, launch.py:420-421), or the token passed into a box (iv.py:33-35; table). Fix: `network_allow=[]`, an image and `NEEDS_CONTAINER` on the task, as v1 has (E/physim/taskset.py:435, 701-703), plus v1's two guards (taskset.py:453-454, 461-462).
5. **Token reach.** The Lab parses agent input while inheriting the token (V/runtimes/subprocess.py:151), which opens every instance in the repo. Fix: the Lab deletes it from its environment after loading.
6. **Records leave the worker**, though not toward the agent: tracebacks, tool log tails in error text (launch.py:354, 360), the default upload (table). Fix: `--no-push` or `PRIME_RUNS_MODE=disabled` (V/utils/platform.py:68-75); the Lab logs no hidden value.
7. **Residual.** Lab reply times are unpadded (lab_service.py:199-227). On Prime the Lab's URL is a public tunnel with no credential (launch.py:381-384; V/mcp/server.py:301-331). Fix: time one step across the prior; keep sealed exams on Docker until the tunnel code is read.

## Changes from review

**From the claims review, each checked in code:**
- Collection also takes `/logs/artifacts`; a scoring exception regrades up to three times (item 1).
- Container-only and no-network are verifiers task declarations, which v1 already uses, not work left to us (item 6).
- "Verifier box has no egress" is conditional on the row policy, and the network is open during setup and staging (item 7).
- Upload sends each whole episode record as it finishes; no longer an unknown (item 8).
- Added to the table: `runtime_env` and `harness.env` as token hazards, the Lab's absence during grading, the `url` Toolset, stop-hook timing, `vf-debug`, Prime as default runtime (items 3, 5, 10, 11).

**From the red team:** all seven open paths form section 8; the three recommendation changes are marked "Changed" in section 3; a per-item cleanup check joins unknown 1.

**Rejected or narrowed:**
- Claims review, item 6, "a subprocess agent with a Docker verifier passes": rejected. isolated-verifier always collects artifacts (iv.py:70), and collection refuses a subprocess agent (V/agent.py:440-445), as the red team said.
- Claims review, item 7, "the verifier inherits the agent's policy unless `--env.verifier.runtime` is set": narrowed. The row's policy is applied to either base (iv.py:73-74; V/utils/compile.py:45-56).
- Red team, vw/harness.py:50-51 as support for fresh noise on a replayed label: those lines check replay mode, so the claim is left out.

**Editor's own:** R/DECISIONS.md line numbers in sections 3 and 7 were stale; the worker question is reframed around the tokens-stay-on-the-Mac rule; "keep" corrected from 2,100 to 2,370 lines; evidence for sections 5 and 6 moved into the table; two citations re-sourced (RUNBOOK.md:93-95; compose.yaml:1).
