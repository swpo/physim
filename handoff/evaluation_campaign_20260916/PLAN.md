# Results campaign: model coverage, cost, and limit auditing

Updated September 16, 2026. The user authorized starting this campaign after
the documentation review. Fresh centered-apparatus science, truth, baseline
generation, native validation, and registry reconstruction are complete for all
three worlds. The first paid GLM Flash rollout is active on BF. See
`outputs/evaluation-campaign-20260916`
for resolved configurations, source snapshots, checks, and the spending ledger.

The first model is GLM 5.3 Flash, beginning with BF. XV and p4g2_044 follow after
reviewing the completed BF trace for provider errors and binding limits. Each
rollout is admitted separately; paid inference remains sequential.

The campaign uses each model's highest catalog-supported reasoning effort
(`max`, then `xhigh`, then `high`); models without an effort selector use
reasoning enabled. Each response may use the provider's advertised maximum
output. Record these settings with results; do not tune them against scores.

## Scientific objective

Measure what agents accomplish when they can investigate until they choose to
submit. Cost is an observed outcome on the Pareto plot, not a small, equal
per-model allowance. Artificial turn, token, experiment, and execution limits
must not silently turn this into an efficiency-constrained benchmark.

The campaign's spending target is $50; its authorized hard pause ceiling is
$150, including failed requests, retries, and any rented compute. Crossing $50
must not interrupt an ongoing rollout: let it finish, then discuss the actual
spend with the user before starting another rollout. For example, finishing at
$65 because the latest rollout cost $17 is acceptable. The $150 ceiling is
headroom for completion, not a new spending target or permission to launch more
rollouts after the $50 review point. Keep concurrency at one for paid rollouts
so this boundary is unambiguous.

Before each paid request account for in-flight liability and token/context
pricing. Pause before the next request would risk exceeding $150, even if a
rollout is still in progress. Preserve its state and report the interruption;
it is incomplete evidence, not a natural model stop. Earlier cost checkpoints
are diagnostic reviews and must not terminate a rollout merely for crossing
the checkpoint amount. This supersedes the earlier $50 hard-cap/$10-reserve plan.

## Candidate stages

Model IDs and prices below were checked against Prime's authenticated Models API
on September 16. Prices are USD per million output tokens, not total rollout
cost; input, reasoning, caching, and repeated context also affect billed spend.

Start with the inexpensive models; each initial model should cover all three
worlds before expanding coverage. Review spending and cap interference after
each batch, with an initial $5 checkpoint. The list is a candidate pool, not a
commitment to complete every model or spend the whole allowance.

| Stage | Model ID | Output $/million |
| --- | --- | ---: |
| First, inexpensive | `qwen/qwen3.5-35b-a3b` | 1.30 |
| First, inexpensive | `deepseek/deepseek-v4.1-flash` | 1.20 |
| First, inexpensive | `z-ai/glm-5.3-flash` | 0.50 |
| First, inexpensive | `openai/gpt-5.6-luna` | 1.20 |
| First, inexpensive | `google/gemini-3.8-flash` | 3.75 |
| First, inexpensive | `anthropic/claude-haiku-4.5` | 5.00 |
| Expand open-model coverage | `qwen/qwen3.5-397b-a17b` | 3.60 |
| Expand open-model coverage | `deepseek/deepseek-v4-pro` | 3.83 |
| Expand open-model coverage | `z-ai/glm-5.3` | 4.40 |
| Expand open-model coverage | `moonshotai/kimi-k2.6` | 4.00 |
| Decide after actual costs | `anthropic/claude-sonnet-5` | 10.00 |
| Decide after actual costs | `openai/gpt-5.6-terra` or `openai/gpt-5.6-terra-pro` | 15.00 |
| Decide after actual costs | `moonshotai/kimi-k3` | 17.25 |
| Deferred high tier | `anthropic/claude-opus-5` | 25.00 |
| Deferred high tier | `openai/gpt-5.6-sol` | 30.00 |
| Deferred high tier | `anthropic/claude-fable-5.1` | 50.00 |
| Deferred high tier | `openai/gpt-6-astra` | 50.00 |

Terra Pro is a compute-mode choice, not a larger underlying Terra model. OpenAI
documents pro mode as additional model work at the same token rates, independent
of reasoning effort. Prime lists Terra and Terra Pro at the same rates; verify
the provider routing before choosing the endpoint. Record mode and effort
explicitly. Do not mix those configurations under an unlabeled model point.
Freeze model-specific sampling/reasoning settings before observing rewards;
avoid tuning them against the grading suite.

Begin with one rollout per model/world to establish cost and variability. Aim
for balanced repetitions (ideally three) when the budget supports them. Decide
between repetitions and more expensive models using costs and uncertainty,
without selectively repeating only failures or retaining best-of-N outcomes.

## Preflight findings and required limit review

The table below records the starting settings and their required treatment.
The campaign profile now has unlimited total turns/input/output/total tokens,
experiments, simulated time, validation attempts, and submission attempts.
Predictors receive 4 CPUs, 8 GiB, 3,600 CPU and wall seconds per request,
512 MiB of artifacts, 256 MiB per file and 1 GiB of temporary storage. Agent
rollouts allow seven days; tool/finalization calls allow eight hours and grading
allows 24 hours. These operational safeguards remain audited limits, not a
claim of literally unbounded execution. The 50-tu experimental horizon and
instrument geometry remain part of the common task.

The real Docker/Verifiers workflow passed an offline scripted-model test:
experiment, write predictor, validate, submit, freeze, and grade, with exactly
the frozen persistence reference score and zero API spend. This also passed on
the new BF bundle before paid inference. Unit/integration tests, the package
build, the portable wheel install, campaign accounting/aggregation tests and
the new rectangular-coupling control test pass. Seven existing optional tests
were skipped. The isolated install reproduced BF using the new environment
wheel and the declared public Blobkit dependency.

| Layer | Current setting | Required treatment |
| --- | --- | --- |
| Total model work | 1,024 turns; 1,048,576 output tokens | Campaign config should omit these caps: installed Verifiers supports `None` for unlimited totals. Input/total-token caps already default to `None`. Verify the resolved config. |
| Each model response | Sampling `max_tokens` defaults to `None` | Provider defaults may still truncate. Resolve model-supported output/context limits, leave enough reasoning space, record every response finish reason and context error. |
| Investigation | 1,000 experiments; 50,000 simulated tu | Remove or make nonbinding for the campaign and report actual usage. Laboratory code currently requires positive finite caps; changes need implementation and verification. |
| Interface checks | 128 validations; 128 submissions | Make nonbinding; preserve attempted-check counts and rejected calls. |
| Agent runtime | 24 hours; 4 CPUs; 8 GiB RAM | Track duration, memory failures, and resource use. Extend if these interfere. An omitted agent timeout currently falls back to the task's 24-hour timeout. |
| Tools | 600 seconds per MCP call; Bash subprocess timeout 3,600 seconds | Check actual call durations and errors; raise limits together if necessary. |
| Frozen predictor | 20 CPU seconds; 30 wall seconds per call; 1 CPU; 1 GiB RAM | A substantive potential bottleneck. Make configurable and substantially more permissive before the campaign; keep validation and grading consistent. Record runtime and timeout/OOM outcomes. |
| Finalization and grading | 180 seconds; 900 seconds respectively | Must accommodate the relaxed predictor profile across the complete suite, including validation during finalization. |
| Data/artifact transfer | 64 MiB artifact; 20 MiB individual prediction file; other request/output byte bounds | Audit actual utilization and distinguish execution limits from malformed output. Relax binding operational limits coherently. |

The 50-tu horizon of one experiment, available instruments, allowed action
programs, and prediction array shapes define the task. Do not silently change
them while relaxing total investigation budgets. Review any evidence that
request-size restrictions obstruct useful experiments separately from runtime
limits, then apply protocol changes consistently before collecting comparisons.

The frozen predictor cannot call model APIs. Inference cost describes the
investigating agent; retain local experiment/predictor compute measurements and
declare the runtime resources separately. Include any rented compute in the
campaign's total budget.

## Evidence to retain for every rollout, including unsuccessful ones

- Exact code, package/image, suite, world, provider/model, reasoning, sampling,
  and resolved resource configuration; common task and harness across models.
- Verifiers stop condition and `is_truncated`; inspect all call finish reasons,
  not only the final response. Reuse native lifecycle/error handling.
- Experiment/time usage, rejected experiments, validation/submission counts,
  context usage, token totals including reasoning, billed costs and retries.
- Tool/predictor duration and resource failures. Flag approaching limits before
  they bind, as well as attempts that were actually rejected or interrupted.
- Whether the agent chose to submit/end or the framework stopped it. The current
  finalization hook can collect a predictor after a cap stop; a finite score alone
  is therefore not proof of an unconstrained completion.
- Inspect traces for agents rationing experiments or submitting early because
  of advertised limits, even if the counters never reach the cap.

Fix binding artificial limits and obtain replacement evidence using a common
revised profile. Preserve interrupted attempts and their costs. Do not describe
an incomplete model/world aggregate as a completed comparison, or silently drop
a difficult world. Resume only with faithful state restoration; the existing
submission-recovery helper closes exploration and is not a full continuation.
Never select the better score from an interrupted attempt and its replacement.

Provider/infrastructure failures get bounded retries and no error rows in the
headline figure. An otherwise completed attempt that delivers no valid predictor
still receives zero reward, as already agreed. Classify resource interruptions
before interpreting them as ordinary model failures.

## Results page

One headline cost-versus-reward plot using only the new common, generous profile.
For each rollout use the environment reward `R = 1 / (1 + S)`; then average
repetitions within each world and average the three world means equally. Never
pool cases across worlds or average energy scores before transforming to reward.

Use mean actual inference cost per rollout on log x, mean reward on linear y to
start, and connect members of a model family. Identify the actual Pareto frontier
separately from family segments. Record provider-failure overhead separately
from plotted eligible-rollout costs while including all spend in the ledger.

Refresh baselines on all three new suites. Show a few relevant horizontal lines
with information access explained in the caption; retain the full control data
below or in linked artifacts. Adjust visible range transparently, never remove
model outcomes to improve appearance. Below the plot, show per-world rewards,
repetition counts/variation, and a short account of general versus world-specific
performance. Avoid unsupported precision from one or very few rollouts.

Sources: [Prime Models API](https://docs.primeintellect.ai/api-reference/inference-models),
[OpenAI reasoning modes](https://developers.openai.com/api/docs/guides/reasoning#reasoning-mode).
