# First model rollouts of round 6: progress

PILOT_NEVER_REUSE_AS_EXAM: every instance named here is public pilot material and is never to be used as an exam.

The exam is the verifiers port of round 6 (`../vfport`, pinned by `PIN.sha256` at commit
08bd5a669867623a476e7446a74612be47001b3b; nothing under it is changed by this work). Configs, wrappers and
results of the rollouts are in this folder. Spend: `LEDGER.md`.

## qwen_ring_001 (the mechanics rollout; runner session of 11 Nov 2026, in the cloud container)

Purpose: prove that a real model can take the exam end to end here (key, model route, harness, laboratory,
submission, grading) and see what a weak agent does. One rollout; at most one more, on a new instance, if the
first dies on mechanics.

State (newest last; times UTC as this container's clock shows them):

- 10:30 Runner started after a container restart (the earlier runner's work did not survive; nothing was
  committed). Own worktree; the port's tree equals the pin (109 of 109 hashes; sha256 of PIN.sha256 cd67eb4b...).
- 10:35 Docker daemon started (29.9.2). Images on disk: physim2-ring:1, localhost/verifiers-network:1,
  python:3.12-slim. No container of anybody was running.
- 10:40 Model: `qwen/qwen3.5-35b-a3b` (the pinned config's id) is not in Prime's model list (132 models);
  `qwen/qwen3.6-35b-a3b` is, with tools, at $0.11 in / $1.01 out / $0.099 cache read per million tokens (the
  list's own `pricing` field). It is the cheapest Qwen chat model by input price. Bound by the caps: $0.23 plus
  one request.
- 10:42 MECHANICS, found before any rollout, both from this machine's TLS-intercepting proxy (neither applies to
  the lead's Mac):
  1. vf-eval cannot reach the model from the environment `tools/vfrun.py` gives it. The allow-list (ENV_PASS,
     tools/vfrun.py line 62) drops SSL_CERT_FILE; verifiers' model client (httpx) then checks against certifi:
     measured `CERTIFICATE_VERIFY_FAILED` for `GET /api/v1/models` from an environment of PATH, HOME, LANG, and
     200 with the session's environment. Worked around outside the pinned tree: `tools/here.py` adds the one
     name SSL_CERT_FILE to vfrun.ENV_PASS in memory for the model command only.
  2. The stock `bash` harness installs itself INSIDE the agent's box before the network is cut (`pip install
     uv`, `uv sync --script`: verifiers runtimes/base.py:41-46, 274-279). In `physim2-ring:1` that fails here
     (measured in a throwaway container: curl exit 60, `uv: not found`, status 127 after 16 s), because the box
     does not trust the proxy's CA. Worked around outside the pinned tree: image `physim2-ring-ca:1` =
     `physim2-ring:1` + the machine's CA bundle + four variables (`docker/Dockerfile.ring-ca`); the same
     bootstrap then ends with status 0 in 4 s and the chat program starts (`--help`).
  The session's environment also holds two names the tools refuse (UV_NATIVE_TLS, DOCKER_HTTPS_PROXY):
  `tools/here.py` starts every tool from PATH, HOME, USER, LANG and VF_RUN_ID only, as the cloud rehearsals did.
- 10:44 Instance `pilot-qwen-ring-001-r2-w0` made (ring, smoke_ring: 64 items, R = 16, 400 laboratory ticks),
  commitment a125f5016080ec142c86391721dd52bfccad569b6332e88e3c53a9db1b685852. Store (hidden side, never
  committed): the runner's scratch folder `rollq/store`. Reference table started: `tools/prove.py`, policies
  S, D, P0, PM, C, null, C once more with one box per item; disk floor 1.5 GiB (3.0 GiB free on this machine).

- 10:58 Reference table done (`tools/prove.py`, EXIT 0, 896 s for 7 scripted rollouts with 4 shared cores under
  load 6): all graded, 0 failed items; laboratory ticks S 392, D 392, others 0. On this instance, skill on the
  K-to-O scale (and K-to-C): O 1.000 (1.073), C 0.932 (1.000), S 0.927 (0.994), P0 0.817 (0.876), PM 0.796
  (0.854), D 0.466 (0.500), K 0, null -0.040 (-0.042). C graded once more with one fresh box per item: identical
  per-item scores, 64 item boxes, 4.76 s per item box (so the model's grading takes about 5 minutes). Saved:
  `qwen_ring_001/reference/`. The scripted boxes ran with the tools' own settings (2 CPUs; memory: the task
  row's 8 GiB, `tools/prove.py` has no option for it); the model's boxes are capped at 2 CPUs and 4 GB by config.
- 10:59 Dry run of step 3 in its Linux form (free, no model, no credential): `DRY-RUN-OK`; vf-eval resolved the
  config (`qwen_ring_001/dry_run_resolved_eval.json`: bash harness, tool timeout 600 s, docker, cpu 2,
  memory 4, 40 turns, 1.5 M / 60 k tokens, rollout 3600 s, no retries, push false).
- 10:59 One paid ping of the model from vf-eval's environment (`tools/ping_model.py`; the model list answers 200
  without a credential, so it proves nothing about the key): HTTP 200 in 2.5 s, usage 258 tokens in, 2 out
  (`qwen_ring_001/preflight_ping.json`). The key, the team header and the CA route work.
- SPEND BOUND corrected before the start: the runbook's bound (1.5 M x p_in + 60 k x p_out = $0.23) is not a
  bound on the bill, because verifiers' token caps count each fed-in token once while the provider bills the
  context at every turn. The bound that holds is 40 turns x 262,144 tokens of context: $1.22 (`LEDGER.md`).
- 11:01 ROLLOUT qwen_ring_001 STARTED (committed before the start). Run label physim2-rollq-20261111, run name
  qwen-ring-001, instance pilot-qwen-ring-001-r2-w0, model qwen/qwen3.6-35b-a3b, image physim2-ring-ca:1.
  The command, from the runner's scratch folder S, with R = this folder (the key is inherited through the
  environment; its value is on no command line):

      nice -n 10 /home/user/evalwork/vfport/.venv/bin/python -B R/tools/here.py --run-id physim2-rollq-20261111 \
        vfrun.py --config R/configs/qwen_ring_001.toml --run-name qwen-ring-001 --out-dir S/run --store S/store \
        --disk-floor-gib 1.5 --model-credentials prime > S/run.log 2>&1 < /dev/null ; echo "EXIT $?" >> S/run.log

  Watched by `tools/watch.py` (docker ps by the run label, the laboratory's counters, a copy of submission/
  from the agent's box and the verifier's box; no exec in a box, no signal, no reading of the model's text).

- 11:12 ROLLOUT qwen_ring_001 ENDED: `EXIT 0` after 11 min 32 s. Complete, graded, not cut. 40 model calls, stop
  condition `max_turns`; `submission/` empty (the model wrote its predictor to /workspace/predict.py at turn 39
  and was cut at turn 40 while asking for a validation); final collection: no predict.py; all 64 items scored
  as K; reward 0.000. Laboratory: 18 episodes, 306 of 400 ticks, 0 nats, 39 requests, 1 rejected, 1 validation,
  0 submissions, 0 infrastructure errors. Billed: 758,132 input tokens (656,608 of them cache reads) and 18,888
  output tokens: $0.1025 (`LEDGER.md`). No credential and no hidden value in the run folder.
- 11:25 Extracted into `qwen_ring_001/` (start with `RESULT.md`): result, per-item scores next to the reference
  policies, the laboratory's log, the transcript (Markdown and raw record with the team header removed), the
  watcher's timeline, the port's own report. `tools/scan_key.py` on the whole folder: 0 credentials, 0 account
  identifiers.
- DECISION: no second rollout. Nothing that was reached failed; the model did badly inside the caps, which is a
  result. What a model has NOT yet exercised: an accepted submit and its freeze, the stop hook `frozen`, a
  model-written predictor in the verifier box and in the 64 item boxes. Whoever runs the next rollout should
  read `qwen_ring_001/RESULT.md`, "Mechanics problems found": the 40-turn cap is not told to the agent (it was
  cut at 18 % of its hour), and the token caps do not bound the bill (only turns x context does).

DONE for this role. Left on the machine: the Docker daemon (running, not to be stopped), the images
physim2-ring:1, localhost/verifiers-network:1, python:3.12-slim and the new physim2-ring-ca:1 (needed by any
model rollout on this machine; rebuild with `docker/Dockerfile.ring-ca` after a restart that loses it), no
container, no process. The runner's scratch folder `rollq/` (store with the hidden side of the pilot instance,
the unredacted run folder, the watcher's copies) stays until the container restarts; nothing in it is needed.

For the next runner on this machine (the same wrappers work for any model):
1. `tools/here.py --run-id LABEL prove.py ...` for the reference table of a NEW instance (15 minutes for six
   policies and the box check), then `... vfrun.py --config CONFIG --dry-run`, then `tools/ping_model.py MODEL OUT`.
2. The rollout: `tools/here.py --run-id LABEL vfrun.py --config CONFIG --run-name NAME --out-dir DIR --store STORE
   --disk-floor-gib 1.5 --model-credentials prime`, detached, with `tools/watch.py` beside it.
3. Afterwards `tools/here.py ... run_report.py`, `tools/extract.py`, `tools/scan_key.py` (and
   `tools/redact_values.py` if it reports account identifiers), then the ledger and the commit.
