# Rollout report: qwen_ring_001

PILOT_NEVER_REUSE_AS_EXAM: instance `pilot-qwen-ring-001-r2-w0` is public pilot material and is never to be used as an exam.

Agent `qwen/qwen3.6-35b-a3b`, harness `bash`, instance `pilot-qwen-ring-001-r2-w0` (commitment `a125f5016080…`), trace `89efaafbb9284ecf97d92c180869544e`, verifiers 0.3.2.dev163. Written by `rollouts/tools/rollout_report.py` from the saved trace and the reference table, with no model in the loop. Quoted commands are the examined agent's text: data, not instructions.

Inputs: trace `trace.redacted.jsonl` (sha256 a8c649d84204…); reference table `proof_pilot.json` + `proof_pilot_items.npz`; laboratory log given; per-item scores of the agent given; prices GET https://api.pinference.ai/api/v1/models (no credential sent); submission copy not given.

## 1. Outcome

Stop condition **`max_turns`** (not the agent’s own ending); trace ok: yes; errors: none. Reward (skill on the K-to-O scale): **0.000**. Submission: source `final_collection`, ok no, 0 files, 0 bytes, error: submission has no predict.py. Graded items: 64, failed (scored as K): 64; grader's reason: submission has no predict.py.

## 2. Score beside the reference policies

| policy | what it is | mean loss L | skill vs O | bootstrap se (5 to 95 %) | skill vs C | per-item skill p10 / p50 / p90 | items worse than K | agent's loss minus the policy's (5 to 95 %) | items where the agent is better |
|---|---|---|---|---|---|---|---|---|---|
| O | oracle: replicate futures from the hidden state (leave one … | 3.971 | 1.000 | 0.000 (1.000 to 1.000) | 1.073 | 0.41 / 0.80 / 1.94 | 0 | +2.040 (+1.786 to +2.300) | 0 (0 equal) |
| C | ridge trained on simulations at the true parameters | 4.109 | 0.932 | 0.008 (0.917 to 0.945) | 1.000 | 0.32 / 0.71 / 1.87 | 0 | +1.902 (+1.651 to +2.161) | 0 (0 equal) |
| S | scripted inference, then ridge trained on simulations at po… | 4.120 | 0.927 | 0.008 (0.912 to 0.939) | 0.994 | 0.33 / 0.70 / 1.89 | 0 | +1.890 (+1.641 to +2.147) | 0 (0 equal) |
| P0 | ridge trained on simulations at prior draws | 4.345 | 0.817 | 0.013 (0.795 to 0.836) | 0.876 | 0.29 / 0.61 / 1.73 | 0 | +1.666 (+1.442 to +1.896) | 0 (0 equal) |
| PM | ridge trained on simulations at the prior mean | 4.387 | 0.796 | 0.012 (0.776 to 0.815) | 0.854 | 0.28 / 0.60 / 1.72 | 0 | +1.624 (+1.408 to +1.844) | 0 (0 equal) |
| D | ridge fitted to the real episodes the budget allows | 5.060 | 0.466 | 0.047 (0.380 to 0.537) | 0.500 | -0.20 / 0.38 / 1.35 | 12 | +0.951 (+0.705 to +1.198) | 12 (0 equal) |
| **the agent** | the examined agent of this trace | 6.010 | **0.000** | 0.000 (0.000 to 0.000) | 0.000 | 0.00 / 0.00 / 0.00 | 0 | – | – |
| K | long-run average of the hidden world (climatology pool) | 6.010 | 0.000 | 0.000 (0.000 to 0.000) | 0.000 | 0.00 / 0.00 / 0.00 | 0 | +0.000 (+0.000 to +0.000) | 0 (64 equal) |
| null | null agent: prior-predictive long-run law, no history, no p… | 6.091 | -0.040 | 0.023 (-0.077 to -0.001) | -0.042 | -0.34 / 0.00 / 0.14 | 32 | -0.081 (-0.161 to -0.002) | 32 (0 equal) |

L is the energy score summed over the valid (level, time) cells, averaged over the 64 items (lower is better); skill vs O = (L_K - L) / (L_K - L_O). The per-item skill is (K_i - L_i) / (L_K - L_O) for one item: its mean over items is the skill, its spread shows where the score comes from. The bootstrap resamples the items of this ONE instance (4,000 resamples, seed 0, the same draws for every row): it says how well this instance separates the rows, and nothing about other hidden worlds. The agent's per-item scores come from: --items (extract.py's per_item_scores.json, rounded to 6 decimals); 64 of its items failed.

Skill vs O by the class of the test program (a none, b blind random, c aimed from the history, d regional):

| class | items | C | S | P0 | PM | D | the agent | null |
|---|---|---|---|---|---|---|---|---|
| a | 16 | 0.928 | 0.928 | 0.837 | 0.813 | 0.659 | 0.000 | -0.022 |
| b | 16 | 0.935 | 0.929 | 0.819 | 0.782 | 0.584 | 0.000 | -0.007 |
| c | 16 | 0.889 | 0.885 | 0.791 | 0.789 | 0.022 | 0.000 | -0.072 |
| d | 16 | 0.954 | 0.945 | 0.818 | 0.798 | 0.519 | 0.000 | -0.051 |

Consistency: reference table recomputed from its per item file: yes; trace L K and L O equal the reference table: yes; agent per item mean equals trace L: yes; agent skill equals trace reward: yes; failed items equal trace n failed: yes.

## 3. Usage and cost

|  |  |
|---|---|
| model calls | 40 (0 failed, 0 without usage) |
| billed input tokens | 758,132 (101,524 at the input price + 656,608 cache reads) |
| output tokens | 18,888 (0 reasoning) |
| what the token caps saw | 18,759 in + 18,888 out = 37,647 (verifiers counts each fed-in token once; the provider bills the context at every turn) |
| largest context / largest reply | 37,567 / 2,340 tokens |
| prices (USD per million tokens) | 0.11 in, 1.01 out, 0.099 cache read; source: GET https://api.pinference.ai/api/v1/models (no credential sent) |
| cost | **$0.1025** for the ledger (the larger of: all input at the full price $0.1025, the provider's own cost fields $0.0951); with the cache-read price $0.0952 |
| what the caps allowed | $1.22 (max_turns x context window x input price + (max_output_tokens + max_tokens) x output price; the other bound gives $7.96) |

Wall clock: boot 1.6 s, setup 19.7 s, agent 643.3 s (model 451.4 s, harness and tools 191.9 s), finalize 1.5 s, verifier 2.5 s.

## 4. Budgets against the caps

| budget | used | cap | share | where the cap comes from | note |
|---|---|---|---|---|---|
| model turns | 40 | 40 | 100.0 % | agent config max_turns | what the agent was shown does not state this cap |
| tokens as verifiers counts them (each fed-in token once) | 37,647 | 1,500,000 | 2.5 % | agent config max_total_tokens | what the agent was shown does not state this cap |
| output tokens | 18,888 | 60,000 | 31.5 % | agent config max_output_tokens |  |
| largest single reply (tokens) | 2,340 | 8,192 | 28.6 % | sampling max_tokens |  |
| largest context sent (tokens) | 37,567 | 262,144 | 14.3 % | the model's context window (--model-entry) |  |
| agent phase, wall seconds | 643.3 | 3,600.00 | 17.9 % | agent config timeout.rollout, else the task row |  |
| laboratory ticks | 306 | 400 | 76.5 % | exam config (reference table) |  |
| nats in total | 0.000 | – | – | exam config (reference table) | no total cap in this config |
| largest nats in one episode | 0.000 | 8.00 | 0.0 % | TASK.md in the trace | from the laboratory's log |
| validation attempts | 1 | 16 | 6.2 % | exam config (reference table) |  |
| submit attempts | 0 | 16 | 0.0 % | exam config (reference table) |  |
| submission size, bytes | 0 | 67,108,864 | 0.0 % | exam config (reference table) |  |
| predictor CPU seconds, worst item | – | 30 | – | exam config (reference table) | not in this trace (no predictor ran, or one box per item) |
| agent box CPU seconds (read inside the box: unverified) | 163.7 | 14,400.00 | 1.1 % | the envelope's cores x the wall-clock cap |  |
| model spend, USD | 0.102 | 1.22 | 8.4 % | the smaller bound of section 3 |  |

## 5. What the agent did

Tool calls by kind (a call with several kinds counts under the first of: network, submit, validate, lab, lab-info, sim, compute, write, read):

| kind | tool calls | turns | model s | tools s |
|---|---|---|---|---|
| validate | 1 | 1 | 2.2 | 1.9 |
| lab | 7 | 7 | 40.8 | 9.8 |
| lab-info | 1 | 1 | 3.5 | 0.6 |
| sim | 23 | 23 | 376.7 | 171.0 |
| read | 8 | 8 | 28.3 | 4.7 |

Laboratory reached through: the `lab_call` tool 0 time(s), `physim2.Lab()` from Python in 9 tool call(s). Milestones: first simulator run: turn 7 (t = 21 s); first laboratory experiment: turn 10 (t = 41 s); first write under submission/: never; first validation: turn 40 (t = 641 s); submit: never.

Longest model call: 37.1 s (turn 39); longest run of one turn's tools: 30.1 s (turn 25).

The laboratory's counters in the trace: 306 ticks, 18 episodes, 0.00 nats, 39 requests (1 rejected, 0 infrastructure errors), 1 validation(s), 0 submit(s), submitted: no.

Every tool call (t = seconds of the agent phase at which the model's reply arrived; model s = that reply's latency; tools s = until the next model call started, shared by the calls of one reply; lab = what the laboratory's own log holds for that span):

| turn | t | model s | tools s | kind | what | lab (its own log) | result |
|---|---|---|---|---|---|---|---|
| 1 | 8 | 4.4 | 0.1 | read | `cat TASK.md ¦ head -100` |  | ok (5,907 chars) |
| 2 | 9 | 0.8 | 0.0 | read | `ls -la` |  | ok (246 chars) |
| 3 | 10 | 0.8 | 0.1 | read | `ls -la physim2/` |  | ok (805 chars) |
| 4 | 12 | 2.0 | 0.0 | read | `cat physim2/world_ring.py` |  | ok (9,175 chars) |
| 5 | 13 | 0.8 | 0.0 | read | `cat physim2/__init__.py` |  | ok (859 chars) |
| 6 | 15 | 2.0 | 1.3 | read | `python -c "import physim2; W = physim2.load_world(); print(dir(…`; runs 1 lines of Python |  | ok (815 chars) |
| 7 | 21 | 4.5 | 9.4 | sim | `python -c: Generate some episodes at prior mean to understand t…`; runs 10 lines of Python; simulator: Simulator, episodes |  | ok (386 chars) |
| 8 | 33 | 2.8 | 1.6 | read | `python -c: Let's understand the observation model better`; runs 8 lines of Python |  | ok (793 chars) |
| 9 | 38 | 3.5 | 0.6 | lab-info+read | `python -c: lab = physim2.Lab()`; runs 7 lines of Python; Lab calls in the code: card, usage | 2 req (card x1, usage x1), 0 ticks, 0.00 nats | ok (999 chars) |
| 10 | 41 | 2.2 | 3.7 | lab | `python -c: Try a simple experiment with no input`; runs 10 lines of Python; Lab calls in the code: reset, advance; inputs zero (static) | 2 req (reset x1, advance x1), 17 ticks, 0.00 nats | ok (353 chars) |
| 11 | 58 | 14.0 | 0.6 | lab | `python -c: Let's try experiment which is reset + advance`; runs 6 lines of Python; Lab calls in the code: experiment; inputs invalid (static) |  | error: ValueError: Out of range float values are not JSON compliant: nan |
| 12 | 62 | 3.5 | 0.6 | lab | `python -c: Try experiment with empty input array (T ticks witho…`; runs 5 lines of Python; Lab calls in the code: experiment; inputs invalid (static) | 1 req (experiment x1), 0 ticks, 0.00 nats, 1 rejected | Lab rejected: format: inputs must be finite numbers with shape (T, 24), 1 <= T <= 4096 |
| 13 | 66 | 3.4 | 0.9 | lab | `python -c: experiment: reset + advance, so we need to provide T…`; runs 7 lines of Python; Lab calls in the code: experiment; inputs zero (static) | 1 req (experiment x1), 17 ticks, 0.00 nats | ok (110 chars) |
| 14 | 73 | 5.9 | 6.5 | sim | `python -c: Let's understand the dynamics better`; runs 9 lines of Python; simulator: Simulator, free_run |  | ok (418 chars) |
| 15 | 87 | 6.8 | 6.8 | sim | `python -c: Generate many episodes at different parameter values…`; runs 12 lines of Python; simulator: Simulator, free_run |  | ok (217 chars) |
| 16 | 108 | 14.7 | 1.6 | read | `python -c: Let me understand the dynamics more carefully`; runs 11 lines of Python |  | ok (139 chars) |
| 17 | 111 | 1.6 | 1.8 | lab | `python -c: Let me try a simpler approach: use real experiments …`; runs 11 lines of Python; Lab calls in the code: reset, advance; inputs zero (static) | 10 req (reset x5, advance x5), 85 ticks, 0.00 nats | ok (890 chars) |
| 18 | 128 | 15.2 | 6.8 | sim | `python -c: Let's understand the observation model more carefully`; runs 13 lines of Python; simulator: Simulator, free_run |  | ok (300 chars) |
| 19 | 158 | 22.3 | 1.8 | sim | `python -c: Let me try a different approach: use the Kalman filt…`; runs 8 lines of Python; simulator: Simulator |  | ok (36 chars) |
| 20 | 170 | 10.3 | 4.3 | sim | `python -c: Let me think about this differently.`; runs 10 lines of Python; simulator: Simulator, free_run |  | ok (290 chars) |
| 21 | 179 | 4.9 | 1.4 | lab | `python -c: Let me try a more practical approach: use the Lab to…`; runs 22 lines of Python; Lab calls in the code: reset, advance; inputs zero (static) | 2 req (reset x1, advance x1), 17 ticks, 0.00 nats | ok (310 chars) |
| 22 | 215 | 34.9 | 6.1 | sim+write | `cat > /workspace/infer_params.py << 'EOF'`; runs 76 lines of Python; writes infer_params.py (124 lines); simulator: Simulator, free_run |  | ok (79 chars) |
| 23 | 242 | 21.1 | 5.3 | sim | `python -c: The issue is that the Kalman filter needs to track t…`; runs 57 lines of Python; simulator: Simulator, free_run |  | ok (139 chars) |
| 24 | 266 | 18.4 | 6.1 | sim | `python -c: Generate test data at known params`; runs 53 lines of Python; simulator: Simulator, free_run |  | ok (89 chars) |
| 25 | 288 | 15.5 | 30.1 | sim | `python -c: Generate test data at known params`; runs 57 lines of Python; simulator: Simulator, free_run |  | ok (85 chars) |
| 26 | 330 | 12.0 | 17.5 | sim | `python -c: Generate test data at known params`; runs 55 lines of Python; simulator: Simulator, free_run |  | ok (138 chars) |
| 27 | 361 | 14.0 | 3.6 | sim | `python -c: Let me check: is the observation model correct?`; runs 27 lines of Python; simulator: Simulator, free_run |  | ok (164 chars) |
| 28 | 372 | 7.3 | 3.6 | sim | `python -c: The theoretical variance is ~1.96 for all blocks, bu…`; runs 29 lines of Python; simulator: Simulator, free_run |  | ok (436 chars) |
| 29 | 386 | 10.3 | 3.8 | sim | `python -c: The theoretical covariance has a specific structure.…`; runs 36 lines of Python; simulator: Simulator, free_run |  | ok (933 chars) |
| 30 | 398 | 7.7 | 3.7 | sim | `python -c: Check: does the Simulator use the correct stationary…`; runs 15 lines of Python; simulator: Simulator, free_run |  | ok (203 chars) |
| 31 | 406 | 5.0 | 3.4 | sim | `python -c: The variance varies a lot across seeds at t=0, which…`; runs 14 lines of Python; simulator: Simulator, free_run |  | ok (207 chars) |
| 32 | 432 | 22.8 | 3.7 | sim | `python -c: Test Kalman filter log-likelihood computation`; runs 46 lines of Python; simulator: Simulator, free_run |  | ok (100 chars) |
| 33 | 450 | 13.7 | 9.7 | sim | `python -c: The LL values are quite different for the same param…`; runs 51 lines of Python; simulator: Simulator, free_run |  | ok (81 chars) |
| 34 | 485 | 25.6 | 8.5 | sim | `python -c: Let me try a much finer grid around the true params`; runs 52 lines of Python; simulator: Simulator, free_run |  | ok (83 chars) |
| 35 | 525 | 31.7 | 5.2 | sim | `python -c: The problem is that the likelihood landscape is very…`; runs 49 lines of Python; simulator: Simulator, free_run |  | ok (235 chars) |
| 36 | 554 | 23.1 | 8.1 | sim | `python -c: The LL differences are very small. This is because:`; runs 49 lines of Python; simulator: Simulator, episodes |  | ok (857 chars) |
| 37 | 573 | 11.2 | 0.8 | lab | `python -c: Let's collect some real data first`; runs 13 lines of Python; Lab calls in the code: reset, advance; inputs zero (static) | 20 req (reset x10, advance x10), 170 ticks, 0.00 nats | ok (1,332 chars) |
| 38 | 585 | 11.5 | 15.3 | sim+write | `cat > /workspace/build_predictor.py << 'PYEOF'`; runs 57 lines of Python; writes build_predictor.py (77 lines); simulator: Simulator, episodes |  | ok (180 chars) |
| 39 | 638 | 37.1 | 1.7 | sim+write | `cat > /workspace/predict.py << 'PYEOF'`; runs 137 lines of Python; writes predict.py (234 lines); simulator: Simulator |  | ok (52 chars) |
| 40 | 641 | 2.2 | 1.9 | validate | `python -c: Test with the example requests`; runs 6 lines of Python; Lab calls in the code: validate | 1 req (validate x1), 0 ticks, 0.00 nats | no result: the rollout ended |

Shape of the experiments: 18 episodes; ticks of advance per episode: least 16, median 16, most 16; 0 episode(s) are a reset alone; 0 with non-zero inputs.

Laboratory requests, one line per episode (from the laboratory's own log; like episodes of one turn share a line; a rejected request has its own):

| episode | turn | t | requests | ticks | nats | inputs | rejected |
|---|---|---|---|---|---|---|---|
| – | 9 | 38 | card | 0 | 0.00 | – |  |
| – | 9 | 38 | usage | 0 | 0.00 | – |  |
| 1 | 10 | 41 | reset, advance | 17 | 0.00 | zero (0 nats charged) |  |
| – | 12 | 63 | experiment | 0 | 0.00 | – | experiment: request: format: inputs must be finite numbers with shape (T, 24), 1 <= T <= 4096 |
| 2 | 13 | 67 | experiment | 17 | 0.00 | zero (0 nats charged) |  |
| 3 to 7 | 17 | 113 | reset, advance (each) | 85 (17 each) | 0.00 each | zero (0 nats charged) |  |
| 8 | 21 | 180 | reset, advance | 17 | 0.00 | zero (0 nats charged) |  |
| 9 to 18 | 37 | 573 | reset, advance (each) | 170 (17 each) | 0.00 each | zero (0 nats charged) |  |
| – | 40 | 642 | validate | 0 | 0.00 | – |  |

## 6. Flags worth a human look

- **ended_by_a_cap_or_error**: the rollout did not end by the agent's own choice: stop condition `max_turns`
- **last_tool_result_never_seen** (turns 40): the last reply (turn 40) called a tool whose result never reached the model: validate; whatever it did (a validation attempt, a laboratory request) still counted
- **lab_errors** (turns 12): the laboratory rejected 1 request(s) and counted 0 infrastructure error(s) (its counters in the trace); 1 rejection(s) are visible in tool results, 1 in the laboratory's own log
  - `turn 12: experiment: request: format: inputs must be finite numbers with shape (T, 24), 1 <= T <= 4096`
- **python_errors** (turns 11, 12): 2 tool call(s) ended in a Python traceback
  - `turn 11: ValueError: Out of range float values are not JSON compliant: nan`
  - `turn 12: physim2.labclient.LabError: format: inputs must be finite numbers with shape (T, 24), 1 <= T <= 4096`
- **no_graded_submission**: nothing gradable was collected (source `final_collection`, error: submission has no predict.py): scored as K
- **box_differs_from_the_task_row**: the agent's box did not have the resources of the task row, which is what TASK.md states as the compute envelope (cpu: task row 4, box 2; memory: task row 8, box 4)
- **predictor_outside_submission**: the agent's predict.py is at `predict.py` (relative to the workspace) and the trace shows no copy under submission/, the only folder that is collected

Predictor source: read from the trace (the agent's last write to `predict.py`); `predict(history, program, queries, n_samples, seed)`, 234 lines; reads of `history`: 3, of `program`: 2.
Checks that did not fire: collected_without_submit, lab_use_not_visible, long_stretches, network_attempt, outside_the_workspace, predictor_ignores_history, predictor_ignores_program, predictor_unreadable, resets_take_much_of_the_budget, submission_without_lab_use, writes_into_the_public_package.

## 7. What this report could not see

- The laboratory does not log the inputs of a request, only ticks and nats: `zero` is exact (0 nats charged), `blind` or `structured` for requests made from Python is a reading of the code that ran in that turn, and is absent when that code is not in the trace.
- The predictor check is a static reading: an argument passed on to a helper counts as read, and what the code does with it is not judged.
- What the agent read is taken from the commands it wrote: files opened inside a Python script, by a module it imported, or by a helper file the trace never shows are not seen; a path that is mentioned may not have been read. Network attempts likewise: names of tools and libraries, not packets.
- Kinds, input classes and flags are heuristics over text (the README lists the rules); the numbers of sections 1 to 4 are not.
- Whether a hidden value of the instance appears anywhere in the run needs the hidden side: this tool does not look (run_report.py and extract.py count that).
- Why the agent did something, whether its modelling was sound, and whether real data ever entered its fit are for a reader of transcript.md.
- The noise shown is over the items of one instance; nothing here says how the agent would do on another hidden world.
