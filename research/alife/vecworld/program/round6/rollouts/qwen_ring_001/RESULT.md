# qwen_ring_001: the first model rollout of a v2 exam (mechanics)

PILOT_NEVER_REUSE_AS_EXAM: instance `pilot-qwen-ring-001-r2-w0` is public pilot material and is never to be used
as an exam. Its hidden parameters are printed below for that reason only.

Run on 11 Nov 2026 in the cloud container (Linux x86_64, 4 shared cores under load 6 to 10, Docker 29.9.2,
verifiers 0.3.2.dev163), from the pinned port `../../vfport` (PIN.sha256 cd67eb4b..., 109 of 109 hashes, checked
before and after), which was not changed. One rollout; no second one (see "Was this a mechanics failure?").

## What ran

| | |
|---|---|
| model | `qwen/qwen3.6-35b-a3b` through Prime inference (the pinned config's `qwen/qwen3.5-35b-a3b` is no longer listed) |
| harness | verifiers' stock `bash` (tools offered: `bash`, `edit`, `lab_call`) |
| exam | ring world, config `smoke_ring`: 64 items, R = 16, 400 laboratory ticks, hidden (D, gamma, c) |
| instance | `pilot-qwen-ring-001-r2-w0`, commitment `a125f501...85852`; hidden D = 0.2311, gamma = 0.0344, c = 0.2173 |
| caps | 40 turns, 1.5 M total tokens, 60 k output tokens, 8,192 tokens per reply, 3,600 s, no retries, `push = false`, `PRIME_RUNS_MODE=disabled` |
| boxes | image `physim2-ring-ca:1` (the pinned image plus this machine's CA bundle), 2 CPUs, 4 GB, network cut after setup |
| config | `../configs/qwen_ring_001.toml` |
| command | in `result.json` (`command`): `tools/here.py --run-id physim2-rollq-20261111 vfrun.py --config ... --run-name qwen-ring-001 ... --disk-floor-gib 1.5 --model-credentials prime`; the key reaches the process through the environment only |

The disk floor of the tools was 1.5 GiB instead of 8 (this machine had 2.8 to 3.0 GiB free for everyone).

## Outcome

The rollout ran to a graded end: `ok`, no error, stop condition **`max_turns`** after 40 model calls and 643 s of
the agent phase (451 s waiting for the model, 192 s in tools), 11 minutes of its hour. `submission/` was empty:
the final collection found no `predict.py`, the verifier box was started (2.5 s), found no predictor, and every
one of the 64 items was scored as K. **Reward (skill on the K-to-O scale): 0.000.**

| policy | what it is | mean energy score L | skill vs O | bootstrap se (64 items) | skill vs C |
|---|---|---|---|---|---|
| O | oracle: the true simulator from the true hidden state | 3.971 | 1.000 | | 1.073 |
| C | ridge trained on simulations at the true parameters | 4.109 | 0.932 | 0.008 | 1.000 |
| S | scripted inference, then training on simulations | 4.120 | 0.927 | 0.008 | 0.994 |
| P0 | trained on simulations at prior draws, no experiment | 4.345 | 0.817 | 0.013 | 0.876 |
| PM | trained on simulations at the prior mean | 4.387 | 0.796 | 0.012 | 0.854 |
| D | fitted to the real episodes only, no simulator | 5.060 | 0.466 | 0.047 | 0.500 |
| **the model** | **no predictor: scored as K on all 64 items** | **6.010** | **0.000** | (exactly K) | **0.000** |
| K | the long-run average of the hidden world | 6.010 | 0.000 | | 0.000 |
| null | prior-predictive long-run law | 6.091 | -0.040 | 0.023 | -0.042 |

Reference policies: `tools/prove.py` on the same instance (all graded, 0 failed items; C graded a second time with
one fresh box per item gave identical per-item scores). Noise: the standard errors are a bootstrap over the 64
items of this ONE instance (`reference_noise.json`); they say how well this instance separates the rungs,
nothing about other hidden worlds. Paired over the same resamples: S above P0 by 0.110 (se 0.010), P0 above PM
by 0.021 (0.006), C above S by 0.006 (0.002), P0 above D by 0.35 (0.04). The model's 0.000 has no
noise: it is K by rule, not a measured skill. Per item: `per_item_scores.json`.

## Usage and cost

| | |
|---|---|
| model calls | 40, all answered, all with usage; replies 32 to 2,340 tokens, 0 reasoning tokens |
| billed input tokens | 758,132 (101,524 at the input price, 656,608 cache reads) |
| output tokens | 18,888 |
| what the token caps saw | 18,759 in + 18,888 out = 37,647 of 1,500,000 (verifiers counts each fed-in token once) |
| price | $0.11 in, $1.01 out, $0.099 cache read per million tokens: the `pricing` field of the model's entry in `GET https://api.pinference.ai/api/v1/models`, read on 11 Nov 2026 (`model_entry.json`) |
| cost | **$0.1025** with all input at the full price (the ledger's figure); $0.0952 with the cache-read price; the provider's own `cost` fields sum to $0.0951 |
| wall time | 643 s agent phase, 20 s setup (the harness installs itself in the box), 2.5 s verifier; 11 min 32 s from start (11:00:57 UTC) to `EXIT 0` |

## What the agent did

1. Turns 1 to 9: read TASK.md and the public package, printed the world's constants and matrices and the
   laboratory's card. It reached the laboratory only from Python in its box (`physim2.Lab()`), never through
   the `lab_call` tool.
2. Laboratory: 18 free-running episodes of 16 ticks (306 of 400 ticks), no input ever (0 nats). The real
   episodes were printed and never used: no parameter was fitted to them.
3. Turns 14 to 35: its own simulator. It worked out that the law is circulant, wrote a Kalman-filter likelihood,
   tried grid search, Nelder-Mead and differential evolution on SIMULATED data at the prior mean, found the
   17-tick likelihood nearly flat, and checked stationary covariances.
4. Turns 38 and 39: generated 2,000 simulated episodes at prior draws and wrote a 237-line predictor: for each
   item it weights 500 of those prior draws by the Kalman likelihood of the item's history, estimates the state
   at tick 16 and simulates forward under the test program. A reasonable design that uses none of the
   laboratory's data. It went to `/workspace/predict.py` with `/workspace/episodes.npz`: outside `submission/`,
   with an absolute path that does not exist in a grading box, and was never run on a request.
5. Turn 40: called `lab.validate("submission")` on the still empty folder. The turn cap ended the rollout
   before it saw the answer; it never called submit.

Full text: `transcript.md` (every message, tool call and tool result); raw record: `trace.redacted.jsonl`.

## Was this a mechanics failure?

No leg that was reached failed, so no second rollout was run. What a real model has now exercised end to end
here: the key and team header, the model route (40 calls relayed from the box through verifiers' interception
to Prime), the stock bash harness installed in the box, the network cut, the laboratory from inside the box (39
requests, 1 format rejection, 0 infrastructure errors), one validation request, the final collection, the
verifier box, the rule "no predictor is K", the trace and the report tool. The laboratory process held no
token (`lab_process` in `result.json`); the run folder holds no hidden value (0 hits) and no key.

NOT exercised by a model, because this one never put a predictor into `submission/`: an accepted submit and its
freeze, the stop hook `frozen`, the validation of a model-written predictor in the verifier box, the 64 item
boxes on a model-written predictor (they ran today on the scripted C submission only), the `lab_call` tool.

One thing about the ending is ours and not the model's: **the agent is not told that it has 40 turns.** TASK.md
gives it one hour; the 40-turn cap comes from the config, where it was written as a spend bound. The rollout
ended at 18 % of the hour and 2.5 % of the token cap. The model was slow and misplaced its files, which is a
result; that it was cut off without warning while pacing itself for an hour is a property of our setup, and a
stronger agent will meet the same wall.

## Mechanics problems found (all of them)

1. **vf-eval cannot verify TLS on this machine.** `tools/vfrun.py` passes an allow-list of variables to vf-eval
   (line 62, `ENV_PASS`) without `SSL_CERT_FILE`; behind this container's TLS-intercepting proxy httpx then
   fails with CERTIFICATE_VERIFY_FAILED. Worked around in `../tools/here.py` (adds the one name in memory).
   Does not arise on the Mac.
2. **The bash harness installs itself inside the agent's box over the network** (`pip install uv`, `uv sync`
   for openai, mcp, httpx, tenacity, certifi) while the box's egress is still open. In `physim2-ring:1` that
   fails here (the box does not trust the proxy's CA): worked around with `physim2-ring-ca:1`
   (`../docker/Dockerfile.ring-ca`). On any machine it means that a model rollout downloads unpinned packages
   into the box at setup; the scripted rehearsals never did, and neither HOST_SAFETY_AUDIT.md nor RUNBOOK_MAC.md mentions it.
3. **The runbook's price bound is not a bound.** `max_total_tokens` counts fed-in tokens once (18,759 here);
   the provider billed 758,132 input tokens, 40 times as many. Only `max_turns` times the context window bounds
   the bill ($1.22 here, not $0.23). `../LEDGER.md` has the arithmetic.
4. **The turn cap is undisclosed** (above).
5. **The stated envelope did not match the box**: TASK.md said 4 CPU cores and 8 GiB (the exam config's
   envelope); the box had 2 CPUs and 4 GB, set in the config for this shared machine.
6. The session's environment holds two names the tools refuse (`UV_NATIVE_TLS`, `DOCKER_HTTPS_PROXY`):
   `../tools/here.py` starts every tool from PATH, HOME, USER, LANG and VF_RUN_ID, as the cloud rehearsals did.
7. `tools/run_report.py` prints the reason "submission has no predict.py" as `(other, 28 characters)`: that
   text is not among its fixed beginnings (`REASON_HEADS`, lines 31 to 33).
8. At the cap, the tool call of the 40th reply still ran (the laboratory counted one validation), and its
   result was never shown to the model.
9. verifiers keeps the frozen submission in memory only and removes the agent's box at the end: what the agent
   wrote outside `submission/` survives only as text inside the transcript's tool calls. `../tools/watch.py`
   copied `submission/` (empty) every 20 s; it should copy `/workspace` as well.
10. The model list answers 200 without a credential, so "the list answers with the key" proved nothing; one
    paid request (`preflight_ping.json`, 258 tokens in, 2 out) proved the key before the instance was opened.

## What would have to change in the port (nothing was changed)

| file and line | change |
|---|---|
| `tools/vfrun.py:62` (`ENV_PASS`) | pass `SSL_CERT_FILE` on (or an option naming a CA bundle) for machines behind a TLS-intercepting proxy |
| `docker/Dockerfile.ring:10-13, 23-27` | keep `extra-ca.crt` in the final image and point `SSL_CERT_FILE`/`PIP_CERT` at it when it is not empty; better, install uv and the bash harness's packages in the image so that a box needs no network at setup |
| `RUNBOOK_MAC.md:701-706` and `configs/qwen_ring_bash.toml:5-6` | the price bound: `max_turns x context window x p_in + (max_output_tokens + max_tokens) x p_out` |
| `configs/qwen_ring_bash.toml:26` (`max_turns = 40`) and `physim2_env/taskset.py:39-40` (`PROMPT`) or round 5's `agentenv/TASK.md.tmpl:67` (the compute envelope) | tell the agent its turn budget, or raise it so that the hour is the binding limit; the turn cap then has to be set with the price in mind (problem 3) |
| `tools/run_report.py:31-33` (`REASON_HEADS`) | add `submission has no predict.py` |
| `RUNBOOK_MAC.md:662-674` (step 3, "Open before this step") | add: the bash harness downloads packages into the box at setup (problem 2) |

## Files

`result.json` (everything above as numbers), `per_item_scores.json`, `reference_noise.json`, `lab_record.json`
(the laboratory's own log: every request), `transcript.md`, `trace.redacted.jsonl` (the team header removed by
field name; `tools/scan_key.py` counts 0 credentials and 0 account identifiers in this folder),
`submission_manifest.json` (the folder was empty: there is no `submission/` to show), `timeline.jsonl` (what the
watcher saw), `run_report.json` (the port's own report tool), `resolved_config/`, `dry_run_resolved_eval.json`,
`model_entry.json`, `preflight_ping.json`, `reference/` (the scripted policies on the same instance),
`MANIFEST.json`.
