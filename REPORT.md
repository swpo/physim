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
