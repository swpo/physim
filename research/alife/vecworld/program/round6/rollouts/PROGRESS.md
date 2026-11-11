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

## Report tool (toolsmith session of 11 Nov 2026; no rollout, no model call, no Docker run, $0)

Purpose: one command that turns the saved trace of one rollout plus the instance's reference table into a
report a person can read, with no model in the loop.

- 11:33 Own worktree; read the Qwen rollout's files and the pinned port (nothing under `../vfport` is touched).
  The port's `results/` keep no raw trace; the runner's scratch folder still held the seven scripted rollouts of
  its reference table (`prove.py`), so the scripted test input is one of those (policy S on the same pilot
  instance) and no new instance was opened.
- 11:47 `tools/rollout_report.py` (work in progress, committed): scores beside the reference policies, usage and
  cost, budgets, timeline, flags.
- 11:56 DONE. `tools/rollout_report.py`, `tools/README_rollout_report.md` (inputs, the rules behind the
  heuristics, what a trace alone cannot tell), `tools/test_rollout_report.py` (38 checks, all passing: the
  tool's numbers against the runner's `result.json`, `reference_noise.json`, `LEDGER.md` and `prove.py`'s table;
  synthetic traces for the paths no model has used yet). Example reports: `qwen_ring_001/rollout_report.md`
  and `scripted_ring_S/rollout_report.md` (each with its `.json`). New folder `scripted_ring_S/`: the scripted
  trace and the laboratory's log of that rollout, as test inputs.
  Before the commit: 0 credentials and 0 account identifiers (`tools/scan_key.py`), 0 hidden values of the pilot
  instance in the new files.

For the next runner: after `tools/extract.py`, add one step,

    python -B tools/rollout_report.py --trace NAME/trace.redacted.jsonl --reference NAME/reference/PROOF.json \
        --model-entry NAME/model_entry.json --lab-record NAME/lab_record.json --items NAME/per_item_scores.json \
        --name NAME --out NAME/rollout_report

and read section 6 (flags) and section 5 (timeline) of the result before the transcript. The reference table
must be the one of the rollout's own instance (the tool refuses another instance or commitment).

## astra_ring_001 (the first rollout of a strong model; runner session of 11 Nov 2026, in the cloud container)

Purpose: see what a strong agent does on the same exam and where it lands among the reference policies; look for
leaks and shortcuts. One rollout of `openai/gpt-6-astra`; at most one more, on a new instance, if the first dies
on mechanics. The task statement, the exam and the harness are those of qwen_ring_001.

State (newest last; times UTC as this container's clock shows them):

- 11:33 Runner started. Own worktree; the port's tree equals the pin (109 of 109 hashes; sha256 of PIN.sha256
  cd67eb4b...; no difference to commit 08bd5a66 under `vfport/`). Docker 29.9.2 was running, the four images of
  qwen_ring_001 on disk (`physim2-ring-ca:1` included), no container. Free disk 2.7 to 3.0 GiB: the tools' disk
  floor is set to 1.5 GiB on every command, as for qwen_ring_001.
- 11:36 The Qwen rollout shows that the mechanics work (40 model calls answered, the laboratory reached from the
  box, graded end), so the Astra rollout goes ahead. Its mechanics fixes that need no change in the pinned tree
  are applied as they stand: `tools/here.py` (minimal environment, CA bundle for vf-eval), image
  `physim2-ring-ca:1`, the bill sized by turns times context, one paid ping before the instance is opened,
  `tools/watch.py` copying `/workspace` as well. NOT applied, because they need the task statement or the
  pinned tree: telling the agent its turn and token caps, the envelope in TASK.md (it says 4 cores and 8 GiB;
  the box has 2 and 4), the laboratory's error for `experiment(label, None)`, logging of laboratory replies.
- 11:38 Model and price, from Prime's Models API (`GET https://api.pinference.ai/api/v1/models`, no credential
  sent, 132 models): `openai/gpt-6-astra` is listed; `pricing` says $10 in and $50 out per million tokens and
  gives no cache-read price (so all input is counted at $10); context window 1,050,000 tokens; reasoning is
  mandatory, default effort medium. Saved as `astra_ring_001/model_entry.json` after the rollout.
- 11:40 THE CAP. With the pinned caps (40 turns, 1.5 M total tokens) the bill is bounded only by 40 turns x the
  1.05 M context window x $10 = $420, far over the $20 a rollout may cost by its caps. `max_total_tokens` is
  therefore lowered from 1,500,000 to **42,000**; turns (40), output tokens (60,000) and tokens per reply (8,192)
  stay as they were. Bound: every call but the last has prompt + completion under 42,000, so the bill is at most
  (10 x 40 + 40) x 42,000 / 1e6 = $18.48, plus one last reply ($0.41) and $0.01 per 1,000 tokens of tool output
  that reply returns: **$18.89**, under $20 unless that one reply returns over 111,000 tokens of tool output
  (the arithmetic is in `configs/astra_ring_001.toml` and `LEDGER.md`).
  What this does to the rollout, said before it starts: the token cap, not the turn cap, is now the limit the
  agent will most likely meet, and like the turn cap it is not told to the agent. The Qwen rollout used 37,647
  on that counter in 40 turns (no reasoning tokens, small replies); a model that reasons at every turn and reads
  the public code will use it faster. With $10 per million input tokens a $20 bound allows about 1.66 million
  token-turns whatever the split (40 turns x 42 k, 30 x 55 k, 24 x 66 k, 20 x 77 k); the runner's instruction
  was to keep the turn cap and lower the token cap.
- 11:43 Instance `pilot-astra-ring-001-w0` made (ring, smoke_ring: 64 items, R = 16, 400 laboratory ticks),
  commitment 58488c5f9354675cd595e0ace9b0375c5361a6eafb5454a7f36194ee9028f4bf. Store (hidden side, never
  committed): the runner's scratch folder `rolla/store` (the task text's `KEY/store` is a template slip, as in
  the Qwen role). Reference table started on it: `tools/prove.py` through the new `tools/prove_here.py`, which
  caps the scripted boxes at 4 GB as well (checked on the first box: 4,294,967,296 bytes, 2 CPUs); policies S, D,
  P0, PM, C, null in one box per rollout; no second grading of C with one box per item (done for
  qwen_ring_001 on the same image; the model's own grading uses one box per item); `--no-cross-check` (that
  check runs the item driver on the host).
- 11:47 Paid ping of the model as the bash harness calls it (`tools/ping_stream.py`, new: two streamed requests
  with the harness's own tool definitions and its own stream reader; the second sends the assistant's tool call
  back with a made-up result): both answered (5.7 s and 1.3 s), finish reasons `tool_calls` then `stop`, usage
  arrives in the stream (182 + 214 tokens in, 19 + 5 out, 0 reasoning tokens on this trivial request, 0 cached),
  the provider's own `cost` fields are $0.0028 and $0.0024, exactly the listed $10 / $50 per million. So the
  token caps will see this model's usage, and the second turn of a tool conversation is accepted.
- 11:48 COORDINATOR'S RULINGS read in the channel file (written 11:42 UTC): (1) do not repeat the hidden turn
  cut: bound the bill by turns x context at $20 or less and take the largest turn cap that fits; comparability
  with the Qwen run does not justify the flaw; (2) if a config-level field lets one sentence be added to what
  the agent is told without touching the pinned tree, tell it its turn limit there; change nothing else in the
  task statement or the exam; (3) record the frozen submission and /workspace with the watcher. The plan of the
  11:40 entry (40 turns, 42,000 tokens, nothing told) is DROPPED; nothing had been started with it.
- 11:52 THE CAPS AS RUN. At $10 per million input tokens the turn cap cannot go up: turns and total tokens share
  one budget, (turns + 4) x total tokens <= 1.92 million for a $20 bound (`LEDGER.md`, "Row 3": 150 turns would
  leave 12,400 tokens, 40 turns 43,600). The largest turn cap is taken that still leaves the conversation of a
  complete attempt by a model that reasons at every turn, about 3,000 tokens per turn:
  **max_turns 22, max_total_tokens 70,000**; max_output_tokens 70,000 (so that no third cap can end the run
  first); sampling.max_tokens 16,384 instead of 8,192 (for this model a reply is reasoning and answer together;
  a reply cut inside a tool call or inside its reasoning would be a failure of ours). Bound by these caps:
  **$19.02** (under $20 unless the last reply returns over 98,000 tokens of tool output).
  DISCLOSURE: verifiers has a config field for it (`[env.taskset] system_prompt`, a file whose text becomes the
  task's system prompt; the bash harness appends it to its own system line; the pinned tree is not touched). The
  agent is told BOTH limits that can end its run, in one sentence, because with this bound the token limit is as
  likely to end it as the turn limit. Word for word (`configs/astra_ring_001.system_prompt.txt`):

      Limits of this run, set by the operator: it ends after your 22nd reply (a reply with all the tool calls in
      it counts as one) or once the conversation has used 70,000 tokens in total (the task text, every tool
      result and everything you generate, reasoning included, each counted once), whichever comes first; neither
      counter is shown to you.

  Checked without starting anything: the taskset loads the sentence and the harness composes the system message
  as its own line, a blank line, then that sentence; the first message (TASK.md) is identical to the one of
  qwen_ring_001 (9,169 characters, same sha256). So the agent's hour is NOT the binding limit of this rollout:
  22 replies or 70,000 tokens are, and it knows both.
- 11:52 Reference table done (`tools/prove.py` through `tools/prove_here.py`, EXIT 0, 496 s for 6 scripted
  rollouts, boxes at 2 CPUs and 4 GB): all graded. Skill on the K-to-O scale: O 1.000, C 0.888, S 0.883, P0 0.791,
  PM 0.787, D 0.037, K 0, null -0.043.
- 11:52 Dry run of step 3 in its Linux form (free, no model, no credential): `DRY-RUN-OK`; vf-eval resolved the
  config; against the dry run of qwen_ring_001 it differs in exactly: model, instance, max_turns 40 -> 22,
  max_total_tokens 1,500,000 -> 70,000, max_output_tokens 60,000 -> 70,000, sampling.max_tokens 8,192 -> 16,384,
  taskset system_prompt (new), and the run's own names.
- 11:54 ROLLOUT astra_ring_001 STARTED (this entry is committed before the start). Run label
  physim2-rolla-20261111, run name astra-ring-001, instance pilot-astra-ring-001-w0, model openai/gpt-6-astra,
  image physim2-ring-ca:1, config `configs/astra_ring_001.toml`. The command, from the runner's scratch folder
  S, with R = this folder (the key is inherited through the environment; its value is on no command line):

      nice -n 10 /home/user/evalwork/vfport/.venv/bin/python -B R/tools/here.py --run-id physim2-rolla-20261111 \
        vfrun.py --config R/configs/astra_ring_001.toml --run-name astra-ring-001 --out-dir S/run --store S/store \
        --disk-floor-gib 1.5 --model-credentials prime > S/run.log 2>&1 < /dev/null ; echo "EXIT $?" >> S/run.log

  Watched by `tools/watch.py` (docker ps by the run label, the laboratory's counters, copies of submission/
  from the agent's box and the verifier's box and of /workspace from the agent's box; no exec in a box, no
  signal, no reading of the model's text). If this container restarts before an ENDED entry follows, the
  rollout was cut: record it as cut with what the provider billed, and do not reuse the instance.
