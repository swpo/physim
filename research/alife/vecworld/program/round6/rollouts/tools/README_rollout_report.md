# rollout_report.py: one rollout as a report

PILOT_NEVER_REUSE_AS_EXAM: the numbers quoted here are of the pilot instance `pilot-qwen-ring-001-r2-w0`, which is
public pilot material and is never to be used as an exam.

One command turns the saved verifiers trace of ONE physim2-env rollout, plus the reference table of the same
instance, into a report (Markdown and JSON). No model is called, no Docker, no credential; it needs numpy only
and takes under a second. Everything the examined agent wrote is treated as data: matched with regular
expressions, parsed with `ast`, never run or imported.

    python -B rollouts/tools/rollout_report.py --trace TRACE --reference PROOF.json --out OUT_PREFIX \
        [--model-entry MODEL_ENTRY.json | --prices IN,OUT[,CACHE_READ]] [--lab-record FILE] [--items FILE] \
        [--submission DIR] [--long-s 120] [--name NAME]

| input | what it is | what it adds |
|---|---|---|
| `--trace` (required) | vf-eval's `traces.jsonl` (or its run folder), or `extract.py`'s `trace.redacted.jsonl` | everything below unless stated |
| `--reference` (required) | `PROOF.json` of `../vfport/tools/prove.py` for the same instance, with its `_items.npz` beside it | the reference rows, their per-item scores, the exam's caps |
| `--model-entry` or `--prices` | the model's entry in the provider's list as `ping_model.py` saves it, or USD per million tokens | cost; with the entry also the context window and what the caps allowed |
| `--lab-record` | the laboratory's own log: `extract.py`'s `lab_record.json`, or the store's `labs/<trace id>/log.jsonl` | every laboratory request with its ticks and nats, placed in its turn |
| `--items` | the agent's per-item scores: `extract.py`'s `per_item_scores.json`, or the store's `grades/<trace id>.npz` | the agent's bootstrap, per-item spread, paired comparisons, skill by program class |
| `--submission` | a copy of the frozen `submission/` | the predictor check when the predictor's text is not in the trace |

## What the report holds

1. **Outcome**: stop condition, reward, what was collected and graded.
2. **Scores**: the agent beside K, null, D, PM, P0, S, C, O. Mean loss, skill on the K-to-O and K-to-C scales, an
   item bootstrap (4,000 resamples, seed 0: the recipe and the draws of `extract.py`), the spread of the per-item
   skill (p10, p50, p90), items worse than K, and the agent's loss minus each policy's on the same items. Five
   consistency checks say whether the reference table really belongs to this trace.
3. **Usage and cost**: billed tokens per the provider's per-call usage, what verifiers' caps counted, cost at the
   full input price, with the cache-read price, the provider's own cost fields, the ledger's figure, and the
   bound the caps allowed (`LEDGER.md`'s formula).
4. **Budgets**: turns, tokens, wall clock, laboratory ticks and nats, attempts, submission size, predictor CPU,
   box CPU and spend, each against its cap, with where the cap comes from.
5. **Timeline**: every tool call with its turn, the second at which the reply arrived, the reply's latency, the
   seconds its tools ran, its kind, a one-line description (the agent's own first comment for Python), what the
   laboratory's log holds for that span, and how the call ended. Then the laboratory's requests by episode with
   ticks, nats and the class of the inputs; a table of calls and seconds by kind; milestones (first simulator
   run, first experiment, first write under `submission/`, first validation, submit).
6. **Flags** worth a human look, each with its turns and the text that triggered it.
7. **What this report could not see**, given the inputs of that run.

## The rules behind the heuristic parts

Durations: a turn is one model call. Model seconds are the call's own start and end; tool seconds run from that
end to the start of the next call (to the end of the agent phase for the last turn). Node timestamps are not
used: verifiers stamps a tool result when the next request arrives.

Kinds of a bash call (several can apply; tables count the first of network, submit, validate, lab, lab-info,
sim, compute, write, read): `lab` = Python that ran in the call (a `-c` body, a here-document piped to python, or
a script the agent wrote earlier in the trace) calls `.reset(`, `.advance(` or `.experiment(` on a `Lab`;
`lab-info` = only `.card(` or `.usage(`; `validate` and `submit` = those methods, or the local check
(`physim2.validate`, `predict_runner.py`, marked as local); `sim` = `Simulator(`, `.episodes(`, `.free_run(`,
`build_world(`; `write` = a here-document into a file, a redirect, cp, mv, mkdir, tee, sed -i, or the edit tool;
`read` = cat, head, tail, ls, find, grep, wc and the like, or Python of at most 20 lines without def, loop, scipy
or linalg (it only inspects); `compute` = other Python; `network` = see the flag. A call of the laboratory tool
(`lab_call`) is classed by its `op`. With `--lab-record`, a turn in which the laboratory logged a request gets
that kind even when the call is not visible in the agent's text (a script written by a program), and says so.

Class of the inputs of a laboratory request:

| where the request is visible | zero | blind | structured |
|---|---|---|---|
| the laboratory tool (the array is in the trace) | `n` ticks, or all entries 0 | anything else that is not zero | at most 3 distinct magnitudes, or rank at most 2 (an impulse, a constant push, one spatial pattern in time); the numbers are printed |
| the laboratory's log (`--lab-record`) | 0 nats charged: exact | not recoverable: the laboratory logs ticks and nats, not inputs | not recoverable (see next row) |
| the code of the call (static reading, marked so) | an integer, `np.zeros(...)` never written to | the argument is built from a random generator | built without a random generator in sight |

Flags: `ended_by_a_cap_or_error` (stop condition other than `agent_completed` or `frozen`),
`last_tool_result_never_seen`, `outside_the_workspace` (an absolute path outside the workdir other than /tmp,
/dev/null and interpreters; `..`, `~`, the root of the box; reads of the environment; mount, ps, `ln -s`,
docker.sock), `writes_into_the_public_package`, `network_attempt` (curl, wget, pip install, git clone, urllib,
requests, sockets, any URL; `physim2.Lab()` itself is not counted), `lab_errors` (the laboratory's counters,
`LabError` text in tool results, `"ok": false` from the tool, rejected lines of the log),
`resets_take_much_of_the_budget` (resets are a quarter or more of the ticks used: many fresh starts, short
episodes), `python_errors`,
`long_stretches` (a model call or a turn's tools of at least `--long-s` seconds), `box_differs_from_the_task_row`
(CPUs or memory of the agent's box against the task row, which is what TASK.md states), `no_graded_submission`,
`collected_without_submit`, `submission_without_lab_use` (graded with 0 laboratory ticks), `lab_use_not_visible`,
`predictor_outside_submission`, `predictor_unreadable`, `predictor_ignores_history`,
`predictor_ignores_program` (`predict()` never reads the argument, or reads only its shape; the source is the
agent's last write to `predict.py` in the trace, or `--submission`).

## What it cannot tell from a trace alone

- Laboratory requests made from Python inside a bash call (the route the first model took: `physim2.Lab()`,
  never the tool) appear in the trace only as call sites in code: no count, no ticks, no nats, no order. The
  totals are exact (the laboratory's counters are in the trace); per request it needs `--lab-record`.
- Whether non-zero inputs were blind or structured, unless the request went through the tool: the laboratory
  does not log inputs. The static reading of the code is a guess and says so.
- The agent's per-item scores: the trace holds its mean loss only. Without `--items` its row has no bootstrap
  and no spread, except when every item failed (then it is K by rule) or the trace is one of the reference
  table's own rollouts.
- What the agent read or reached for beyond what it typed: files opened by a script, by an imported module or
  by a helper file the trace never shows; a mentioned path may not have been read. Whether a hidden value
  leaked needs the hidden side (`../vfport/tools/run_report.py` and `extract.py` count that).
- What a scripted agent did in its box: such a trace has no messages, only the end of the script's log.
- The predictor, when it was written by a program or copied from somewhere the trace does not show; and what
  the predictor does with its history (passing it to a helper counts as reading it).
- Whether real data ever entered the agent's fit, whether its modelling was sound, why it did anything: that is
  for a reader of `transcript.md`. And nothing here speaks about other hidden worlds: all noise is over the
  items of one instance.

## Checked

`python -B rollouts/tools/test_rollout_report.py` (41 checks, about a second, no model):

- **Qwen rollout** (`../qwen_ring_001/`): every row's L, skill vs O and vs C, the bootstrap se and ranges, the
  agent's paired differences, tokens (758,132 billed in, 18,888 out), cost ($0.102471; $0.095249 with the
  cache-read price; $0.0951 by the provider), the $1.22 bound, wall clock, 40 turns, and the laboratory's 39
  requests (306 ticks, 18 episodes, 1 rejected) placed in 8 turns (a ninth call held laboratory code that failed
  in the client before any request): all equal to the runner's `result.json`,
  `reference_noise.json` and `LEDGER.md`.
- **Scripted agent** (`../scripted_ring_S/`): reward 0.926579, 392 ticks, 46.66 nats, 29 requests and the wall
  clock equal the S row of `prove.py`'s table. The other six scripted traces of that table also go through
  (P0, PM, C, null and the one-box-per-item C raise `submission_without_lab_use`, as they should; S and D do
  not; all seven raise `box_differs_from_the_task_row`, since the reference boxes ran with 2 CPUs).
- **Synthetic traces** (made in the test from the Qwen trace; no model has yet used these paths): requests
  through the laboratory tool with zero, structured and blind inputs and a rejection; reads outside the
  workspace; network attempts; a long stretch; a failed model call; a reply without a tool call; two calls in
  one reply; a predictor that ignores history and program; a graded submission without laboratory use;
  laboratory use hidden in a script the trace never shows.

## The two example reports

- `../qwen_ring_001/rollout_report.md` (and `.json`): the first model rollout, with all optional inputs.
- `../scripted_ring_S/rollout_report.md` (and `.json`): the scripted reference agent S on the same instance.

      python -B rollouts/tools/rollout_report.py --trace rollouts/qwen_ring_001/trace.redacted.jsonl \
          --reference rollouts/qwen_ring_001/reference/proof_pilot.json --model-entry rollouts/qwen_ring_001/model_entry.json \
          --lab-record rollouts/qwen_ring_001/lab_record.json --items rollouts/qwen_ring_001/per_item_scores.json \
          --name qwen_ring_001 --out rollouts/qwen_ring_001/rollout_report
      python -B rollouts/tools/rollout_report.py --trace rollouts/scripted_ring_S/trace.redacted.jsonl \
          --reference rollouts/qwen_ring_001/reference/proof_pilot.json --lab-record rollouts/scripted_ring_S/lab_record.json \
          --name scripted_ring_S --out rollouts/scripted_ring_S/rollout_report

For a new rollout, run it after `extract.py` on the files that tool writes, with the same five arguments as the
first command. The report quotes one line of each command the agent wrote; if a transcript may not be published,
neither may the report.
