# physim M0 report — does difficulty track model performance?

*2026-02-11. Environment: `environments/physim` (verifiers v1 taskset, chat tier /
`null` harness). One task = one hidden world (seeded); the agent explores through
the anonymous-port interface within a tick budget, then answers 12 prediction
contracts (4 per stratum S1/S2/S3) scored `exp(-|err|/scale)` against fresh
truth ensembles, `scale = max(3*ensemble_sd, 10% channel range)`.*

## The environment in one paragraph

Hidden micro-world: modular tanh lattice (locality + modularity + heterogeneity
motifs), collective bistability with hysteresis — the "deep structure" to
discover. Interface: `n_in` anonymous input ports, `n_out` anonymous noisy
sensors (random gain/sign/offset, shuffled, some dead), persistent state, tick
budget. Difficulty presets scale four axes together:

| preset | modules (k*) | ports | dead | sign flips | meas noise | what it adds |
|---|---|---|---|---|---|---|
| D0 | 1 | 6 in / 24 out | 0 | none | 0.02 | clean senses, one collective mode |
| D1 | 1 | 6 / 32 | 4 | 35% | 0.05 | murky senses, same law |
| D2 | 3 | 6 / 36 | 4 | 35% | 0.05 | three semi-independent collective modes |
| D3 | 6 | 8 / 48 | 8 | 40% | 0.07 | six modes + weak global tie, tighter budget |

Contract strata: S1 = weak push + relaxation; S2 = held moderate drives
(uniform/single-port/subset); S3 = strong drive + release, incl. opposite-sign
push-past (hysteresis memory).

## Results

Scripted baselines (3 seeds each; play through the same JSON interface):

| | D0 | D1 | D2 | D3 |
|---|---|---|---|---|
| null (answer 0, no exploration) | 0.04 | 0.03 | 0.06 | 0.04 |
| tail (resting state predicts everything) | 0.42 | 0.50 | 0.43 | 0.34 |
| reference (scripted scientist, ~30 experiments) | 0.72 | 0.72 | 0.65 | 0.67 |
| replication reference (run the protocol once, report it) | ~0.98 | ~0.98 | ~0.98 | ~0.98 |

Models (chat tier, ≤40 turns, 3 seeds per cell; D0 cells include 2 extra
earlier rollouts):

| model | D0 | D1 | D2 | D3 |
|---|---|---|---|---|
| google/gemini-3.5-flash | **0.72** | 0.58 | 0.54 | 0.35 |
| deepseek/deepseek-v4-flash | **0.64** | 0.56 | 0.52 | 0.38 |
| openai/gpt-5-nano | 0.12 | 0.11 | 0.13 | 0.04 |

Difficulty ↔ reward (Spearman, per-rollout): deepseek ρ=−0.49 (p=0.04),
gemini ρ=−0.42 (p=0.13), pooled competent models **ρ=−0.50 (p=0.003)**.

## Reading

1. **The difficulty axis works.** Both competent models degrade monotonically
   D0→D3; pooled correlation is significant at n=32 rollouts. The axis is
   compound (port opacity + number of collective modes + noise + budget), by
   design — it's the D-ladder, not a single knob.
2. **The task discriminates models sharply.** gemini-3.5-flash ≈ scripted
   reference at D0 (0.72 vs 0.72) but falls to 0.35 at D3 vs reference 0.67;
   gpt-5-nano barely beats the null baseline anywhere (it explores 1–3% of
   budget, then guesses; its coverage 0.4–0.7 with near-zero accuracy = badly
   calibrated *and* wrong).
3. **The scripted reference is an honest floor-of-competence**: no model beats
   it at any difficulty yet. Models lose mostly on S2/S3 (per-port structure
   and hysteresis memory), exactly the strata that require deliberate
   experiment design rather than passive observation.
4. **Failure modes observed in traces**: answering from the *current* world
   state instead of fresh-state reasoning (fixed with a prompt clarification);
   exploring only 1 port; never using `reset`; spending <10% of tick budget.
   The environment surfaces experiment-design skill, not just curve fitting.

## Caveats & next

- n=3 seeds per cell is a smoke test, not a paper: variance within cells is
  large (gemini D2 ±0.39 — one rollout aced it, one flopped).
- gpt-5-nano's collapse is partly *protocol* failure (JSON discipline over 40
  turns), worth separating from scientific failure via the coding-harness tier.
- Next steps: (a) sandbox/coding-harness tier (agent writes analysis code;
  DESIGN.md v0.2), (b) policy programs + preparation/control contracts (v0.3),
  (c) simulator-submission scoring (v0.4), (d) certification meter as world
  filter + per-axis difficulty decomposition (v0.5), (e) larger grids, more
  models, r>1 rollouts per seed.

## Repro

```bash
cd /Users/spoho/Documents/prime/test/physim
uv pip install -e environments/physim
# baselines
.venv/bin/python -c "from physim.baselines import run_baseline; print(run_baseline('D0', 0, 'reference')['reward_accuracy'])"
# eval grid (needs PRIME_API_KEY)
./run_grid.sh google/gemini-3.5-flash D0 3
# collect
.venv/bin/python -c "from physim.report import collect_traces, summarize; [print(s) for s in summarize(collect_traces())]"
```
Raw per-rollout rows: `/tmp/physim_results.json`. Traces: `outputs/`.


---

# Addendum (2026-02-11, later): stronger models, longer rollouts, and the D4 frontier tier

## What changed

- **Turn limit is ours, not the harness's**: `--env.taskset.max_turns` (default 40).
  Strong-model runs below used 100.
- **New D4 preset** ("frontier"): adds two motifs to the engine —
  per-module response rates (timescale separation, `lam ∈ [0.04, 1.0]`) and a
  **slow adaptation state** (`a += eps*(x−a)`, feedback `−g·a`, timescale ~200
  ticks). Consequences, verified: duration-dependent memory (same drive held
  60 vs 400 ticks → post-release macro differs by 0.43), slow post-release
  drift over hundreds of ticks, spontaneous relaxation oscillations
  (bistability + fatigue), hysteresis retained. 10 in / 60 out / 10 dead,
  150k tick budget.
- **New S4 contract stratum** (all difficulties): multi-stage push →
  counter-push on a port subset → 300–700-tick settle. Requires long-horizon
  understanding. Contracts stay well-posed: cross-clone sd ≈ 0.02 on S3/S4.
- Solvability floor on D4 is genuinely low: scripted reference 0.27,
  an *upgraded* scripted probe with duration features 0.30, a
  physics-informed kNN oracle (knows to integrate drive at 3 timescales) 0.21.
  Null jumps to ~0.15 (oscillation phase makes some contracts land mid-range).

## Strong-model results (null harness, 100 turns, 2 seeds; 16 contracts incl. S4)

| model | D2 | D4 |
|---|---|---|
| anthropic/claude-opus-4.8 | 0.60 ± 0.21 | 0.18 ± 0.07 |
| openai/gpt-5.2 | 0.46 ± 0.02 | 0.22 ± 0.06 |
| google/gemini-3.1-pro-preview | 0.50 ± 0.28 | 0.19 ± 0.07 |
| *scripted reference* | *0.64* | *0.27* |
| *null* | *0.06* | *0.15* |

## Findings

1. **D4 does what was asked**: the best available models score 0.11–0.28 —
   barely above the null floor, *below* the dumb scripted scientist. There is
   now a tier where frontier models can't do well yet, with large headroom
   (replication reference ≈ 0.93).
2. **Long rollouts are used but not converted**: gpt-5.2 runs 58–98 turns and
   sometimes spends 100% of the tick budget, yet S3/S4 stay near zero. The
   bottleneck is *scientific strategy* (designing duration-controlled
   experiments, discovering adaptation), not interaction quota. opus-4.8
   interestingly stops early on D4 (~30 turns) — it gives up exploring rather
   than running out.
3. **S-strata separate models**: everyone does S2 (steady drives); S3/S4
   (memory, slow modes) is where all models crash on D4 (0.01–0.26).
4. High within-cell variance (seeds differ by 2–4×) — real conclusions need
   n≥5 seeds; these are directional numbers.

## Current difficulty ladder (baseline acc, 3 seeds)

| | D0 | D1 | D2 | D3 | D4 |
|---|---|---|---|---|---|
| null | 0.04 | 0.03 | 0.06 | 0.05 | 0.15 |
| tail | 0.46 | 0.51 | 0.44 | 0.32 | 0.22 |
| reference | 0.70 | 0.71 | 0.64 | 0.65 | 0.27 |

(D0–D3 numbers now include S4 contracts; slightly different from the first table.)

## Next

- n≥5 seeds on D2/D4 for a stable strong-model ranking; add kimi-k3 / glm-5.
- Coding-harness tier so models can build duration-response curves offline
  (separates protocol failure from scientific failure).
- A D5 candidate: adaptation + modular timescales + tighter budget, or
  spatially-structured inputs requiring port-geometry mapping first.
- Consider reporting score vs. *ticks spent* curves (sample efficiency), and
  moving outputs/ to HF datasets once they outgrow the repo.


---

# Addendum 2 (2026-02-11, later still): M1 coding-harness tier, frontier pairings

## What was built

`--env.taskset.tier tools`: the world becomes a **per-rollout MCP tool server**
(`physim_run/reset/status/ready/answer`) launched inside the agent's own
container; world snapshots ride verifiers' per-rollout state channel
(`trace.state`), and scoring happens post-hoc in `PhysimTask.accuracy` from the
recorded answers — engine and truth ensembles never enter the agent's sandbox.
Coding harnesses (codex, claude_code) require `--env.scientist.runtime.type
docker`. Chat tier unchanged and regression-tested.

Harness pairing rule (user guidance + verified empirically): anthropic models
run through the `claude_code` harness (bare chat-completions against
anthropic/* return empty content on Prime Inference); OpenAI-compatible models
pair with `codex`; anything else defaults to `codex`.

## First tools-tier numbers (D4 frontier worlds, 2 seeds, docker)

| model + harness | rewards (seeds) | mean | budget used |
|---|---|---|---|
| gpt-5.2 + codex (D0 smoke) | 0.49 | — | 0.88 |
| gpt-5.6-sol + codex | 0.26, 0.23 | 0.24 | 0.52–0.66 |
| claude-opus-5 + claude_code | 0.41, 0.23 | 0.32 | 0.19–0.28 |
| claude-fable-5 + claude_code | 0.38, 0.36 | **0.37** | 0.16–0.45 |

Chat-tier D4 reference points: opus-4.8/gpt-5.2/gemini-3.1-pro 0.18–0.22,
scripted reference 0.27, null 0.15, replication ~0.93.

## Findings

1. **The harness helps — the frontier moved but did not fall.** Best pairing
   (fable-5 + claude_code, 0.37) roughly doubles the chat-tier frontier and
   clears the scripted reference (0.27), but remains far from replication
   (~0.93). D4 stays a genuinely open tier even for the strongest current
   setup, which is exactly the regime the benchmark wants.
2. **The D0 smoke run shows the mechanism works**: gpt-5.2+codex spent 88% of
   the tick budget building offline fits and hit S4=0.96 (chat tier: S4≈0.2)
   — code + files convert budget into long-horizon accuracy when the world is
   easy enough to model.
3. **On D4 the models still under-spend budget** (fable 0.16–0.45) and S1
   (weak-push relaxation, most sensitive to the adaptation dynamics) stays
   ≤0.35 everywhere: nobody has discovered the slow fatigue variable yet.
4. Long rollouts happen naturally in this tier (66–173 turns, ~10–25 min per
   rollout); tick budget, not turn count, is the binding constraint now.

## Operational notes

- anthropic + claude_code occasionally hits transient `aux call failed: 404`
  warnings (retries succeed); one gpt-5.2+codex rollout errored out entirely
  (`reward=0.000` row) before a retry passed — treat single-seed tools-tier
  numbers with care.
- Rollouts run in `python:3.11-slim` containers; the MCP server is reached at
  `host.docker.internal`.

## Next

- n>=5 seeds per pairing; add gemini-3.1-pro + codex.
- Give the tools tier a persistent scratch summary of experiment history in
  the prompt? (models re-discover basics each rollout)
- HF dataset upload for outputs/ (repo now 30+ MB of traces).


---

# Addendum 3 (2026-02-11): rollout cost accounting (tools tier, D4)

Per-rollout usage from `traces.jsonl` model-call records (prompt tokens are
dominated by cached context re-reads; costs shown as cached + fresh):

| pairing | seed | model calls | fresh prompt | cached prompt | completion | reasoning | wall time | reward |
|---|---|---|---|---|---|---|---|---|
| gpt-5.2+codex (D0) | 0 | 106 | 0.07M | 4.6M | 31k | 21k | 14 min | 0.49 |
| gpt-5.6-sol+codex | 0 | 66 | 0.10M | 4.3M | 12k | 8k | 8 min | 0.26 |
| gpt-5.6-sol+codex | 1 | 98 | 0.10M | 5.4M | 17k | 11k | 12 min | 0.23 |
| opus-5+claude_code | 0 | 67 | 0.24M | 4.1M | 111k | 24k | 25 min | 0.41 |
| opus-5+claude_code | 1 | 93 | 0.27M | 6.5M | 125k | 26k | 36 min | 0.23 |
| fable-5+claude_code | 0 | 173 | 0.60M | 50.9M | 241k | 28k | 63 min | 0.38 |
| fable-5+claude_code | 1 | 113 | 0.70M | 22.1M | 191k | 37k | 52 min | 0.36 |

Observations: (1) 60–170 model calls per rollout; effective context stays
manageable because raw data lives in sandbox files. (2) fable-5 reads 5–10x
more cached context than the others (long-context strategy) and takes ~1h per
rollout; sol is 5x cheaper per rollout at ~35% lower score. (3) Chat-tier
rollouts (null harness) are far lighter: ~25–40 calls, <1M cached, 2–15 min.

# Addendum 4: world isolation audit (MazeBench pattern check)

- Engine + truth ensembles run evaluator-side only. Tools tier: the MCP world
  server is a separate host process outside the agent's docker container
  (reached via host.docker.internal); the agent container has no volume
  mounts, no engine code, no physim package.
- Tool responses expose only: tail_mean/tail_sd/series of chosen channels,
  ticks_run, budget_left, phase, interface card, contract specs
  (protocol + channel + stat), and answer receipts. Scoring internals
  (mu, tau, scale, strata, per-contract detail) are computed post-rollout in
  `Task.score` and never flow through a tool.
- The per-rollout state channel (world snapshots) is HMAC-authenticated
  between server and host; the agent receives only the MCP URL.
- New: `PHYSIM_WORLD_SALT` env var mixes an evaluator-side salt into world
  generation and noise streams, so the public engine code + a guessed seed
  cannot reproduce a live world (unset = reproducible published defaults).
  Residual risk accepted: local subprocess runtime (debug only) offers no
  isolation; use docker/prime for real evals.


---

# Addendum 5 (2026-02-11): n=5 D4 pairing statistics + protocol-robustness fixes

## Final D4 leaderboard (tools tier, 5 seeds each, latest run per seed)

| pairing | reward (mean±sd) | budget used | S1 | S2 | S3 | S4 | coverage |
|---|---|---|---|---|---|---|---|
| claude-fable-5 + claude_code | **0.349 ± 0.04** | 0.32 | 0.21 | 0.42 | 0.48 | 0.29 | 0.66 |
| claude-opus-5 + claude_code | 0.324 ± 0.11 | 0.41 | 0.23 | 0.39 | 0.43 | 0.25 | 0.79 |
| gpt-5.6-sol + codex | 0.244 ± 0.07 | 0.54 | 0.21 | 0.39 | 0.19 | 0.19 | 0.47 |
| gemini-3.1-pro + codex | 0.194 ± 0.12 | 0.01 | 0.22 | 0.27 | 0.13 | 0.16 | 0.96 |
| *scripted reference (5 seeds)* | *0.274 ± 0.04* | *0.11* | | | | | |
| *tail baseline (5 seeds)* | *0.211 ± 0.04* | | | | | | |
| *null baseline (5 seeds)* | *0.133 ± 0.05* | | | | | | |
| *replication reference* | *~0.93* | | | | | | |

Reading: fable-5 is the only pairing clearly above the scripted reference
(0.35 vs 0.27, and the most consistent, sd 0.04). opus-5 matches it on mean but
with 3x the variance. sol spends the most budget for less score. gemini
barely explores (1% budget, ~12 turns) and lands at the null floor + eps; its
0.96 coverage with bottom-rung accuracy = wide honest intervals around
guesses. D4 remains open: best mean 0.35 vs 0.93 achievable.

Budget-use vs reward across all 20 rollouts: Spearman rho=0.14 (p=0.55) —
spending ticks does not by itself buy score; *what* you measure matters more
than how much. (sol: most ticks, mid score; fable: moderate ticks, top score.)

## Environment robustness fixes shipped during these runs (v0.1.2)

Diagnosed from failing gemini+codex traces (reward 0.000, n_answered 0):

1. **Tool-arg normalization**: some MCP clients deliver structured arguments
   as JSON strings (sometimes double-encoded, sometimes per-element).
   `physim_run.segments` and `physim_answer.answers` now decode recursively
   and return instructive errors instead of "segment 0 must be an object"
   loops. (Root cause of gemini's zero-scores: it fumbled the format 3-4x,
   then gave up and answered zeros "due to constraints".)
2. **Premature-ready guard**: `physim_ready` with <5% budget used requires
   `confirm=true` (accidental phase transitions locked agents out of
   exploration).
3. **physim_answer during exploration** now errors instead of silently
   issuing contracts.
4. Version-bump note: the tool server installs the env package by sdist;
   uv caches wheels by name-version, so tool-code changes REQUIRE a version
   bump in pyproject.toml to reach the server runtime.

Even after the fixes, gemini-3.1-pro's conduct is unchanged (satisfices in
~12 turns) — that is a model finding, not an env artifact.


---

# Addendum 6 (2026-02-11): trace gallery + workspace artifact collection

- **Trace gallery** at `docs/rollouts.html` (GitHub Pages): per pairing x
  difficulty, best/median/worst rollouts rendered as lab reports — condensed
  experiment log (every physim tool call + world response), the agent's own
  workspace files, and per-contract truth-vs-answer tables. The standout
  artifact: claude-fable-5's `MODEL.md` on D4 correctly identifies "6 bistable
  relaxation-oscillator units", maps ports to units with polarities, measures
  release schedules and mutual entrainment (period ~390-430), and ships a
  per-contract prediction procedure — readable theory, 0.31 reward (its
  jitter-accumulation limits are visible in the same file).
- **Workspace artifact collection** (v0.1.3): tools-tier tasks now declare the
  agent workspace as a verifiers artifact; `PhysimTask.finalize` collects it
  (tar, capped, junk-excluded) into `trace.state.artifacts`, and scoring
  extracts text files into `trace.info["physim"]["workspace"]` (durable in
  traces.jsonl). Rollouts predating this recover files best-effort from
  Write/Edit tool-call arguments; bash-heredoc writes in old rollouts are lost
  — the motivating gap. Validated end-to-end: gpt-5.2+codex D0 rollout
  scored **0.73** (new codex D0 best) and its collected `model.py` contains a
  two-basin affine model with switching threshold and time constant — theory
  as executable code, now preserved.


---

# Addendum 7 (2026-02-11): M2 + M3 shipped — policies, preparation contracts, executable theories

## What shipped (v0.2.0-0.2.3)

- **Policy jail** (`physim.jail`): agent code runs in a hardened subprocess
  (restricted builtins, no imports — tolerant rewriting of `import math/numpy`
  since models type them reflexively — curated numpy without file IO, rlimits,
  per-tick timeouts). Escape battery passes.
- **Closed-loop experiments**: `physim_run_policy(code, t)` — policy(t, y, mem)
  executed tick-synchronously against the live world.
- **Preparation contracts (M2)**: "steer a fresh draw into sensor band B, hold
  after release" — bands placed on reachable branch values by construction;
  scored as success rate over 5 fresh clones. `physim_answer_prep(id, code)`.
- **Theory submission (M3)**: `physim_submit_theory(code)` — an executable
  init/step simulator of the sensors; scored post-hoc by simulating every
  prediction-contract protocol and comparing tail statistics on the same scale
  as answers (report-only reward weight for now).
- Baselines: `prep_pi` scripted P-controller — prep 1.00 on D0/D2, **0.24 on
  D4** (slow adaptation fights naive holds): the control-depth gradient is real.

## First frontier results (D2, tools tier, n_prep=3, 2 seeds)

| model | prediction acc | preparation | theory acc |
|---|---|---|---|
| claude-fable-5 + claude_code | **0.86, 0.95** | **1.0, 1.0** | 0.0*, **0.90** |
| gpt-5.2 + codex | 0.12, 0.78 | **1.0, 1.0** | not attempted |

*seed-1 theory scored 0 for `import` usage — jail now tolerates preloaded-module
imports (v0.2.3); the same 13KB theory would now score.

Highlights:
- fable-5 seed 0 is the best physim rollout ever recorded: prediction 0.95,
  all three preparations 5/5 clones, and a **0.895 executable theory**
  (per-stratum 0.84-0.93) — it modeled the world well enough to simulate it.
- Preparation contracts are currently EASIER for frontier models than
  prediction (both models 100% on D2 preps) — as designed for D2, where
  branch-steering suffices; D4/D5 preps (adaptation, feedback-required
  worlds) are where the prep_pi certifier already drops to 0.24.
- gpt-5.2 seed 0 shows reward decomposition working: prep 1.0 with
  prediction 0.12 — it learned to steer without learning to predict.

## Bugs found by models, fixed

- Session reconstruction (tool server) lost issued prep contracts ->
  "unknown preparation contract id"; contracts are now rebuilt
  deterministically from the seed on any answer-phase call (v0.2.1).
- prep/theory detail now persisted into trace.info (v0.2.2).
- Jail import tolerance (v0.2.3).


---

# Addendum 8 (2026-02-11): D4 grid with preparation + theory (M2/M3 at the frontier)

Grid: 4 pairings x 3 seeds, D4, n_prep=3, theory enabled. Baselines on the
same seeds: null acc 0.145 / prep 0.0; prep_pi acc 0.34 / prep 0.24.

| pairing | prediction | preparation | theory |
|---|---|---|---|
| claude-fable-5 + claude_code | **0.305** | **0.73** | 0.29 (3/3 submitted) |
| claude-opus-5 + claude_code | 0.269 | 0.67 | 0.31 (2/3) |
| gpt-5.2 + codex | 0.219 | 0.47 | 0/3 submitted |
| gpt-5.6-sol + codex | 0.214 | 0.51 | 0.21 (1/3) |

## Findings

1. **Preparation >> prediction on D4** for frontier models (fable 0.73 vs
   0.305): steering a system you cannot yet predict is easier than predicting
   it — consistent with control theory (feedback forgives model error) and
   with the gpt-5.2 D2 result. The scripted prep_pi manages only 0.24, so
   models now clearly beat the certifier on preparation while remaining
   ~1.5-2x above null on prediction.
2. **Per-contract profile**: of 36 attempted preps, 20 hit 5/5 clones, 3 were
   flaky (0<rate<1 — only 8%: policies mostly either work robustly or fail
   flat), 13 scored 0.
3. **Solvability audit of the failures** (seed-2 sample): every zero-rate
   contract IS solvable — one by doing nothing, one by pin-and-release, and
   one (ch58) ONLY by feedback control with the correct sign, where naive
   P-control latches the wrong branch (+0.99) and inverted-sign P-control
   scores 5/5 (measured feedthrough sign inversion). Models failed exactly
   where control depth crosses from open-loop to feedback-with-
   identification. The task discriminates the intended skill.
4. **Theory tracks prediction** (r=0.72, n=6): the executable-simulator score
   is measuring the same understanding as contract accuracy, on ~1/3 of
   attempts models simply don't submit a theory (gpt-5.2: zero submissions —
   codex agents treat optional tools as skippable; worth a nudge or a weight).
5. Adaptation rebound remains the wall: fable's best D4 prediction is 0.37
   vs its 0.95 on D2; S1 stays <=0.5 everywhere. D4 is unsaturated on all
   three rewards.

## Environment verdict

M2/M3 mechanics behave at the frontier: rewards decompose (prep vs pred vs
theory measure different skills), preparation contracts are solvable-but-
discriminating, theory submission correlates with understanding. Next
design lever: control-depth-graded prep strata (open-loop / feedback /
feedback+identification) as an explicit axis, and possibly weighting theory.


---

# Addendum 9 (2026-02-12): chemistry track — first frontier runs (C0/C1)

Engine v0.3.1 (unified core; snapshot fix for grayscott worlds). Runs: 2 seeds
per pairing, n_prep=2, theory enabled, 100-turn default.

| pairing | diff | prediction | preparation | theory |
|---|---|---|---|---|
| claude-fable-5 + claude_code | C0 | 0.95, 0.91 | 1.0, 1.0 | 0.96, 0.92 |
| gpt-5.2 + codex | C0 | 0.82, 0.54 | 1.0, 0.75 | not submitted |
| claude-opus-5 + claude_code | C1 | 0.96, 0.95 | 1.0, 1.0 | 0.96, 0.95 |
| gpt-5.6-sol + codex | C1 | 0.97, 0.92 | 1.0, 1.0 | 0.82, — |
| *baselines C0 (2 seeds)* | | *null 0.32 / tail 0.75 / ref 0.71* | | |

## Findings

1. **The chemistry track as configured is frontier-easy** (0.91-0.97 acc,
   preparation saturated). Root cause: objects are STATIC between
   perturbations and co-located sensors make tail-means quasi-constant;
   held-out protocols mostly reproduce probed regimes. The physics is
   richer than the contracts currently exercise (no motion, no multi-object
   interaction probed). C-track difficulty needs: mobile objects (feed
   gradients / drift), contracts on object COUNT changes (split/merge
   protocols), apparatus-dependent contracts (bands only measurable by
   moving a sensor), and tighter scales.
2. **The apparatus went entirely undiscovered.** The best rollout (opus-5
   C1 seed 0, 179 turns, 84% budget) explicitly classified ports 2,4,6 as
   "inert" — ports 2 and 4 ARE the apparatus (stage + enable). Short probes
   (~200 ticks) through empty space look like nothing; no agent ran the
   sustained scans needed to see the stage signature. As designed, apparatus
   discovery is HARD; to make it learnable it needs either (a) contracts that
   require it, or (b) sensor starting positions where small moves already
   change readings (edge-of-object placement).
3. **The science was real despite the wrong ontology — best artifact yet.**
   opus-5's notes.md describes "4 independent 4-sensor cells" with
   "positive drive = slow progress along a line attractor" (= object growth),
   "negative = threshold trigger to absorbing state T" (= object death,
   thresholds measured per cell: 0.615/0.685/0.625), "sigma > 850: IMMUNE"
   (= object too large to starve), and validated with held-out protocols
   (mean |err| 0.021). It reconstructed the object inventory as "cells",
   growth curves as "line attractors", kill thresholds, and death as an
   absorbing state — chemistry rediscovered in alien coordinates, without
   any spatial ontology. Its executable theory scored 0.96.
4. gpt-5.2 (C0) lagged (0.54-0.82): its fits treated S3/S4 kill-release
   contracts poorly (S3 0.30-0.53) — it never characterized object death.

## Verdict

Mechanically the track works end-to-end (contracts, preps, theory, artifact
collection, gallery). Scientifically the frontier models validated the
substrate but exposed the contract suite as too shallow for the physics.
C2+ design queue: object motion, count-change contracts, apparatus-forced
measurement, GS-aware scripted scientist, tighter answer scales.


---

# Addendum 10 (2026-02-12): the trivial-preparation gap, closed (v0.3.2-0.3.3)

Audit after the C0/C1 frontier runs found preparation contracts could be
satisfied by DOING NOTHING: all sampled C-track preps and ~half of D-track
preps had bands containing the do-nothing outcome (bistable worlds land
in-band by luck; GS probes barely shifted tails). This inflates every
preparation number reported in addenda 7-9 (models scored some preps for
free; fable's C0/C1 prep 1.0 was partly trivial).

Fixes (v0.3.2): GS prep sampler probes hot ports hard and reads outcomes
after release, requiring reproducibility across draws; tanh sampler uses a
6-draw resting ensemble; both rank candidates by |shift from rest| and pass a
final gate that runs the ACTUAL scorer with a null policy (drop if do-nothing
succeeds >20% of clones). Verified: null-policy success now 0.0-0.2 on all
tracks; scripted single-port actions still reach 1.0 (solvable, non-trivial).
D0 legitimately yields fewer preps (branch preparation is half-free in a
1-module world by construction).

Also fixed (v0.3.3): a C-track wedge — ready() re-sampled contracts on every
retry (72-250s per attempt from GS clone settles + the new verification gate),
exceeding tool-call timeouts. Contracts are now sampled once and cached in
tool state; GS clones reuse the settled initial fields. D-track regression
(incl. clone noise streams) stays bit-identical.

Revalidation (fable-5, C1, n_prep=3): prediction 0.93, preparation 3/3 with
genuine kill actions (bands unreachable by rest, finals well inside), theory
0.88. The chemistry track remains frontier-easy on PREDICTION (static
objects; a persistence THEORY still scores ~0.89 on C0) — that is the C2
mobility work, unchanged in the queue.


---

# Addendum 11 (2026-02-13): C2 — moving chemistry (v0.4.0-0.4.1)

## What shipped

- **Object motion**: differential V-advection (gs_drift) — spots self-propel
  coherently (~1 cell/20 ticks at 0.005) along a hidden per-world direction;
  drift-compensated kill rate keeps counts stable; post-settle cull +
  generation-time certify() (taskset skips unstable seeds, e.g. C2 seed 5's
  replication cascade).
- **Stat-aware contracts**: mean (20-tick tail) or sd (200-tick window).
  On drifting worlds half of S2/S3 + all of S5 are sd-stat on traffic-visited
  channels (resting fluctuation > 3x noise floor).
- **Tight GS scales** (v0.4.1): quasi-deterministic GS ensembles made the
  10%-range scale floor saturating (gpt-5.2 hit 0.91-0.96 on loose scales
  with replication_ref 0.96-0.97). GS scales now 3% (mean) / 1.5% (sd) of
  channel range.
- **Apparatus-forced preparation (C1)**: one prep targets the MOVABLE
  sensor's channel with a band around its on-object reading — solvable only
  by discovering and driving the stage port (scripted scan-until-in-band
  scores 1.0; do-nothing 0.0). On C2, preparations are absent in v1:
  positions are transient by design (tracking preps deferred to C3).

## Floors (C2 seed 0, tight scales)

| baseline | accuracy |
|---|---|
| null | 0.11 |
| tail (rest-means) | 0.49 |
| persistence theory | 0.39 (S5 0.23) |

## First frontier reads

- gpt-5.2 + codex on C2 (tight scales): **0.73, 0.82** — above tail 0.49,
  below the ~0.95+ replication regime; sd contracts and traffic structure
  are doing real work. (On loose v0.4.0 scales the same setup scored
  0.91-0.96 — scale calibration matters as much as world physics.)
- fable-5 C2 (loose scales): 0.97 with a 0.95 executable theory; one rollout
  died to a HarnessError (retry infra noise).
- **C1 apparatus separation works**: fable seed 2 scored 4/4 on standard
  preps and **0/1 on the apparatus prep** (ch23 = the movable sensor; its
  notes classify the stage port as "constants/nothing"). Meanwhile it
  labeled the gain-apparatus channel an "integrator" — apparatus phenomena
  are visible to agents, but the sensor-motion ontology remains undiscovered.
  Instrument discovery is now a measurable, currently-unsolved skill.

## C2 verdict

Medium tier as configured: harder than C0/C1 (motion breaks static
exploits), not yet D4-hard. The remaining slack is the contract grammar
(traffic statistics are learnable from modest sampling). Next hardening
levers if wanted: longer-horizon sd windows, count-change contracts phrased
via multi-channel functionals, faster drift with tracking-grade apparatus
(C3), and multi-species chemistry (M4 proper).


---

# Addendum 12 (2026-02-13): consolidation snapshot (post-calibration numbers)

All numbers below use the HONEST samplers (v0.3.2+ preps) and TIGHT GS scales
(v0.4.1+). Earlier addenda numbers are superseded where marked.

## Cross-track frontier snapshot (fable-5 + claude_code unless noted)

| world | prediction | preparation | theory | notes |
|---|---|---|---|---|
| D4 (seeds 5,6) | 0.27, 0.30 | **0.0** (1 issued) | 0.39, 0.15 | honest preps are HARD (0.73 in add.8 was partly trivial-band inflation) |
| C1 (seeds 2,3) | 0.91, 0.96 | 0.8, 1.0 | 0.93, 0.96 | apparatus prep = the one miss (0/1) |
| C2 (seeds 0,1) | 0.93, 0.75 | n/a | 0.86, 0.71 | tight scales; S3/S5 dips show motion isn't free |
| C2 gpt-5.2+codex | 0.82, 0.73 | n/a | not submitted | |

Difficulty ordering at the frontier (prediction): C0/C1 (~0.95, saturated) >
C2 (0.73-0.93, mid) > D4 (0.27-0.35, open). The two tracks now bracket the
frontier from both sides.

## Premature-closure question (user-raised) -> DESIGN v0.8 pre-note

Frontier agents settle on wrong-but-adequate ontologies (fable: stage port =
"constants", gain-apparatus channel = "integrator"; 0.96 accuracy while
missing the apparatus entirely). Analysis: (1) reward-correct laziness — we
score prediction, not completeness; the miss cost exactly the apparatus
contract; (2) no anomaly pressure within a single rollout; (3) no
falsification oracle. Candidate mechanisms (B) anomaly-completion contracts,
(C) a limited-use self-test tool `check_model`, (D) iterated rollouts on the
same world, (E) longer budgets + conduct prompt. To be decided; the benchmark
currently MEASURES closure behavior rather than correcting it, which is
itself a finding worth reporting.

## Site

Results pages restructured per-track with the consolidated tables; rollout
gallery split into rollouts-bulk.html / rollouts-chemistry.html (old URL
redirects). sd-stat contracts now disclosed in the system prompt (grammar
transparency; v0.4.2).


---

# Addendum 13 (2026-02-13): M4 — multi-species chemistry (C3, v0.5.0)

## World

`grayscott2`: two coupled reaction systems. Species A = standard stable
spots. Species B carries a kill-rate excess (dies alone) offset by A's local
presence — so B objects survive only stacked ON A hosts, and killing a host
via its port cascades to the tenant (~200 ticks later). Ports are
species-tagged (each feeds one species; hidden); sensors read hidden species
mixtures (60% pure / 40% blended). "There are two kinds of stuff" is itself
a discovery. Verified end-to-end through the port interface: bound pairs
persist 8k+ ticks; far-seeded B dies; host-kill removes both.

Documentation principle (DESIGN v0.9): C3's worlds.html panels describe the
world at the SPECIES level (composite species map, binding-distance
histogram clustering at 0, three-frame cascade sequence) — human docs climb
the emergence ladder with the worlds; agents still see only ports.

## Floors and frontier (2 seeds, n_prep=3)

| | prediction | preparation | theory |
|---|---|---|---|
| claude-fable-5 + claude_code | **0.90, 0.89** | 1.0 | 0.78, 0.87 |
| gpt-5.2 + codex | 0.57, 0.57 | 0.83-1.0 | not submitted |
| tail / null / persistence | 0.60 / 0.00 / 0.69 | | |

## The layer-2 closure finding

fable-5 predicts C3 excellently via a LINEAR-LATENTS ontology ("sensors =
linear readout of a few latent states"; port-groups as latents; slow
integrators) — with zero species/host/dependency vocabulary anywhere in its
workspace. The cascade law appears only as "long port0 drive displaced MANY
channels." Same closure behavior as C1's apparatus miss, now one emergence
level up: the agent compresses two-species physics into an adequate
single-layer theory and stops. gpt-5.2's S3/S4 (cascade strata) collapse to
0.25-0.65 — it pays for the missing ontology; fable's latents happen to
capture the cascades functionally (S3/S4 0.80-0.96). Conduct metrics:
port_coverage 1.0 for all four rollouts (everyone probes everything once;
nobody re-opens anomalies).

C3 verdict: mechanically sound, mid-tier at the frontier (fable 0.90 /
gpt-5.2 0.57), and the two-layer ontology question is now measurable:
the gap between predictive adequacy and structural discovery is the
benchmark's sharpest lens yet.


---

# Addendum 14 (2026-02-14): C4 — excitable chemistry: the first rich-not-big frontier-hard world

## The rich-vs-big criterion (DESIGN v0.10, user-set)

A hard world must pass three tests: (1) intended emergent phenomena verified
by god-knowledge probes; (2) a COMPACT theory exists that solves the
contracts (else the world is merely big); (3) frontier models score far
below that compact oracle. C4 is the first world built under and passing
all three.

## The world

FitzHugh-Nagumo excitable medium: a hidden pacemaker emits traveling rings;
sensors read periodic pulse trains. Ports inject current — a sustained drive
CREATES a new pacemaker. Compact laws (each verified by scripted probe):
- wave speed (~0.9 cells/tu; arrival phase = distance/speed)
- entrainment: the faster rhythm source takes over the whole medium
  (collision annihilation ⇒ far-field period = min over sources;
  sustained port drive gives period 39 vs intrinsic 82)
- refractory conduction block: 1:1 at slow drive, 2:1 at period ~110,
  irregular Wenckebach-like zone between
New ontology-neutral statistic for wave worlds: stat="rate" (threshold
upcrossings per 200-tick window; threshold = channel median + 1 sd).
Contract grammar engages the laws: S1 autonomous rhythm, S2 competing
pacemaker, S3 pulse-train conduction, S4 two-port collision.

## Rich-vs-big battery

| reference | accuracy | size |
|---|---|---|
| null / tail / persistence | 0.09 / 0.16 / 0.25 | — |
| entrainment-aware compact oracle | 0.76 (v1, improvable ~0.9) | ~40 lines |
| single replication (true engine) | 0.90 | — |

Deepest floors of any physim world: level-thinking is worthless against
waves.

## Frontier results (2 seeds each, tools tier)

| pairing | prediction | theory |
|---|---|---|
| claude-fable-5 + claude_code | **0.24, 0.18** | 0.52, 0.32 |
| gpt-5.2 + codex | 0.13, 0.12 | not submitted |

The frontier is BROKEN on C4 without any scaling: 96² lattice (same as
C1-C3), 8 ports, 40 sensors, modest noise. fable's notes contain real wave
vocabulary ("wave, pulse, period, phase") and its seed-0 theory scores 0.52 —
it SEES the rhythm but cannot convert to contract-grade timing/rate
predictions. gpt-5.2 never forms the wave ontology (S2 = 0.02-0.03: the
entrainment stratum is invisible to level-based fits).

Gap summary: compact oracle 0.76+ vs best frontier 0.24 on a world whose
laws fit on an index card. This is the project thesis made quantitative:
richness (emergent laws discoverable by better science) rather than bigness
(more parameters/noise) is what separates current AI scientists from the
achievable.


---

# Addendum 15 (2026-02-14): effort diagnostic + calibration A/B — do models try harder on harder worlds?

## Diagnostic (53 tools-tier rollouts)

Question (user): as worlds get harder, do the best models run more
experiments and synthesize more? Hardness := 1 - frontier mean accuracy.

- **fable-5**: synthesis scales with hardness (completion tokens rho=+0.75
  p<0.001; workspace chars +0.54 p=0.015) but EXPERIMENTS do not (+0.07).
  It thinks harder, writes more theory — but does not collect more data.
- **gpt-5.2**: every effort metric flat-to-negative with hardness (wall
  minutes rho=-0.47): works uniformly LESS on harder worlds.
- **sol / opus-5**: fewer experiments on hard worlds (46 vs 78; 80 vs 115).
- Universal: hard-world budget use 26-40% — everyone stops with most fuel
  left. The stopping policy binds, not resources.

Verdict: the ideal property (harder -> try more) FAILS for data collection
across all frontier models tested.

## The basic-compatible lever: pay for honest uncertainty

Intervals were reward-free; narrow-and-wrong cost nothing, so once a point
estimate existed further experiments had no scoreboard value. Added a
Winkler-based interval-calibration reward (fixed function of world+seed;
nothing adapts to the agent): narrow-right 0.91 > medium-right 0.74 >
wide-honest 0.14 > narrow-wrong 0.03. Uncertainty reduction is now the only
path up — and honest reporting beats bluffing.

## A/B on C4 (weight 0 vs 1, 2 seeds/model)

| model | acc | calibration | coverage | experiments | budget |
|---|---|---|---|---|---|
| fable-5 w=0 | 0.21 | 0.00* | 0.12 | 86 | 24% |
| fable-5 w=1 | 0.24 | 0.37 | 0.25 | 80 | 18% |
| gpt-5.2 w=0 | 0.12 | 0.00* | 0.34 | 63 | 34% |
| gpt-5.2 w=1 | 0.17 | 0.38 | 0.38 | 62 | 20% |

*retro-scored as 0 (metric did not exist).

Result: calibration reward improves ANSWER HONESTY (calibration, coverage,
small accuracy gains) but does NOT change experimental effort (experiments
and budget flat/down; n=2 caveats). Models adapt their reporting, not their
science. Conclusion: at current capability, effort-on-hard-worlds is a model
property, not an incentive artifact — the environment can measure it (conduct
metrics, budget use) but not buy it with scoring. This cleanly greenlights
the world-creation program: build past frontier-zero and let the benchmark
wait for models that can climb it.

Default: calibration_weight stays 0 (report-only) for comparability with the
existing leaderboard; recommended 0.5+ for future training runs (honesty
shaping).
