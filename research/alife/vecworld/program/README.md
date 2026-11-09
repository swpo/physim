# PhySim v2: supervenient worlds research program (started 7 Nov 2026)

A world is a level-0 evolution network F0 (hidden weights, explicit noise) plus a coarse-graining Φ to level 1 (and
possibly further levels). The agent observes level k > 0 and acts on level 0 through a constrained input port.
Library: `../vw1/vw`; worked example: the Flow-Lenia gliders world (`../vw1/port`, results in `../vw1/fresh`).

| track | question | memo |
|---|---|---|
| 1, more worlds | how to get more worlds: design from motivating examples, search over level-0 families, and learned coarse-grainings whose inductive biases define Φ | `track1/DESIGN.md` (with the closed-form pooling pilot P0) |
| 2, the exam | what the agent predicts, what is hidden, how interaction is limited, how predictions are scored, how it runs as an environment | `track2/EXAM.md` (with the KL check on the ring toy) |
| inventory | which existing worlds can become level 0, with measured costs, invariants and input costs | `inventory/WORLDS.md` |
| review | cross-reading of the three memos against each other and the gliders results | `CRITIQUE.md` |

Track 1 framing (the lead, 7 Nov 2026, speculative and open-ended): choosing an inductive bias (model structure,
objective) and training autoencoders on level-0 dynamics yields emergent coarse variables, such as local conservation
laws, that depend on the bias; which bias is right almost certainly depends on the level-0 theory. World research may
then look like: hand-design level 0, then iterate on the autoencoder's biases to obtain the higher levels instead of
designing those by hand too. The working plan is to map (level-0 theory x inductive bias) to what emerges, judged by
closure, non-triviality, seed stability, agreement with hand designs and closure under the agent's inputs. The first
cell of that map is the learned level-2 prototype on the gliders block view (`track1/learned_phi2`).

`lit/` holds the earlier literature reviews these build on. `cover/` holds the "PhySim v2 / supervenience" cover
(stack concept; liberties listed in `make_cover.py`).

Headline positions so far:
- Hidden set: the level-0 weights, a secret (at least 128 bits) behind all real-world noise, and the exam instances
  until grading. Nothing fitted to the hidden world leaves the evaluator (for example a Φ trained on its data).
  Permutations can be dropped once the semantics are public.
- Interaction: for inputs that enter as a shift before Gaussian noise, the information cost in nats is half the
  noise-whitened squared norm, so the information budget picks the norm. Inputs must enter where the noise is.
- Scoring: oracle-normalised fair energy skill over declared (level, horizon) cells; variogram score secondary.
  The designer's level-1 ceiling is a lower bound, so rewards must not be clipped at it.
- Pooling: a reconstruction autoencoder picks the wrong feature in a mass-conserving world; a long-horizon closure
  objective with a local, translation-equivariant encoder recovers block sums.

Prototypes (7 Nov 2026; each independently checked, corrections in each `results/summary.json` under `checker`):
- `track2/actuation`: a "wind" input channel (8 x 8 force field with Gaussian noise, exact nats) makes actions matter on the
  gliders world; the matter kick does not. Recommended background noise 0.05, budgets of about 150-700 nats per episode.
- `track2/harness` with new library modules `vw/secret.py`, `vw/nats.py`, `vw/scoring.py`, `vw/harness.py` (105 tests):
  on a closed-form toy, climatology < level-1 ARX < simulation-based inference ~ true parameters < oracle, separated;
  the PhySim v1 energy-score estimator is biased (+6.7% at 15 members, +33% at 3).
- `track1/learned_phi2`: closure with a local, translation-equivariant encoder learns a tapered pooling window equal to a
  designed tent and better than the 2 x 2 box; the encoder's receptive field sets the window; reconstruction is worse.
- `track1/vortex_world`: the fed-vortex world with heredity as a JAX Level (matches numpy to round-off), an exact-nats
  stirring channel, a vortex-list level 1 and a kind-share level 2 with a selection signal at 128^2.
Raw arrays are not committed; the scripts regenerate them.

Round 3 (7-8 Nov 2026; each independently checked, corrections in each `results/summary.json` under `checker`):
- `track2/wind_recert`: background wind sigma_w = 0.05 kept (0.1 rejected; the declared band rule could not decide
  at 9 members, so the choice is after the fact); the block-view closure ceiling survives the wind, the object view
  may lose up to 0.09 (unresolved); under the exam's program mix the inputs move the true dynamics by about
  0.1 V_best per item, of which a linear level-1 predictor recovers at least about a seventh.
- `track2/gliders_exam`: four hidden parameters (kernel radius scale, one growth centre, one growth width, growth
  height) with a viability-conditioned prior; given the true state, the prior-mean control loses clearly (OES
  0.73 vs 0.99; z about 3 with truths resampled), but a history-only ridge predictor cannot exploit the true
  parameters; the harness runs end to end on the gliders wind world.
- `track1/vortex128`: the fed-vortex level-2 selection signal holds at 128^2 in 6 of 6 seeds and all windows
  (paired t-test p 0.0006-0.013); with mutation per unit area the 64^2 box recovers the signal. The oracle shows 51-56%
  of the kind-share change is predictable, but a linear level-2 predictor reaches at most 0.10 of it even given the
  true selection coefficient (checker's correction: an earlier wording here said the coefficient "carries" it).
- `track1/membrane_world`: phase_membrane as a JAX Level (matches numpy to round-off, 11-13x cheaper per tick than
  gliders), a substrate input channel with exact nats, a cell-list level 1 and a population level 2; cells grow and
  divide (median cycle 1,850 time units); dt 0.5 is adequate.

Round 4 (8 Nov 2026; GPU jobs through the Mac runner, about $12 billed in total; each independently checked,
corrections in each `round4/<study>/results/summary.json` under `checker`):
- `round4/wind`: at full size (36 trajectories, H100) the wind world keeps its closure ceilings in both views (block
  view F - M |z| <= 1.9 at h = 1-32; object-view loss bounded below 0.04, so round 3's open "up to 0.09" is excluded);
  the wind's own oracle cost is 0.01-0.04 V_best. Under the exam's program mix the inputs move the true dynamics by
  about 0.2 V_best (block view, h <= 4); learned level-1 predictors recover little of it (input-aware slotnet 44% at
  h = 1 in the object view, nothing in the block view), so "actions matter" passes for level-1 nets only at h = 1
  and needs a simulation-trained predictor otherwise. GPU float64 runs are not bit-deterministic.
- `round4/sbi`: simulate-to-train on the gliders exam pilot (4 hidden parameters, 8 truths, never to be reused as an
  exam). Synthetic-likelihood inference with the public simulator contracts all 4 parameters from 2 real episodes,
  with near-nominal marginal coverage (one clear miss at 512 episodes). A net trained on simulated data at posterior
  draws matches the true-parameter net at every budget; trained on the real data alone it needs about 512 episodes
  (a ridge catches up by about 128). The prior-mean plug-in loses 0.03-0.09 OES: the parameters matter, modestly.
- `round4/bias`: the inductive-bias grid on raw Flow-Lenia gliders states (78 configs + 2 random baselines, 2 seeds,
  cross-fitted). Local closure and local-law encoders learn a mass-like block variable unprompted (cleanest: linear
  local law, R^2 0.995 with block mass); nonlinear reconstruction at width 1 does not; the receptive field sets the
  smoothing; nothing learned beats the hand-designed block mass or block channel means in predictable content per
  number; no bias at <= 4 numbers per block yields the object view. One level-0 theory so far.

Roadmap (9 Nov 2026): `roadmap/ROADMAP.md`, built from four memos on the lead's open questions (`roadmap/Q1_worlds.md`,
`Q2_difficulty.md`, `Q3_science.md`, `Q4_swarms.md`) and a second reading (`roadmap/CRITIQUE.md`). Its verdict: the
framework is sound and cheap, but on the gliders pilot a policy with no hypothesis and no experiment (training on
simulations from the public prior) takes 95% or more of the best reference skill, so the exam does not yet test
science; a level structure tests science only where the agent cannot buy its way down to level 0. It proposes two
acceptance quantities (science share sigma, scripted share rho), agents on exams before more worlds, and seven
decisions for the lead. Thresholds and dates in it are proposals.
