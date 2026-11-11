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

Decisions (9-10 Nov 2026): the lead's answers to the roadmap's decisions are in `roadmap/DECISIONS.md` (hidden parameters
of a correct public law stay the default, with an incomplete public law and a law too expensive to simulate as subjects
of study; the agent's compute is a budget relative to the cost of full simulation; rollouts with real agents are cleared;
sealed answers go to a private Hugging Face dataset repo and the grader builds on the verifiers library; the collective
pilot and the large foundry pass wait).

Round 5 (9-10 Nov 2026; six studies, GPU jobs through the Mac runner, $32.51 billed for the round, $46.27 in total;
each independently checked, and the checkers' corrections, listed in each `round5/<study>/results/summary.json` under
`checker`, are folded in below):
- `round5/agentenv`: the exam as an agent-facing environment (task statement, public `physim2` package, Lab service with
  tick and nats budgets, per-item grader, reference policies K, D, P0, prior mean, S, C, O), proven with scripted agents
  only. On gliders at full size the science share sigma is 0.03-0.065 and fails its bar in every family. The checker
  showed three limits of its local sandbox can be evaded (CPU limit by forking, wall-clock stop by detaching, item
  isolation through shared temporary folders); the sandbox is replaced by the verifiers port (round 6).
- `round5/ladder`: on the gliders wind world, nine cells (block, object or population view x 1, 4 or 8 hidden
  parameters): sigma is below 0.15 in all nine at the point estimate (largest 0.113, 95% interval 0.03-0.19), and
  simulating the public prior is within 0.047 of training at the true parameters. Two Lab episodes of scripted inference
  match the true-parameter predictor within 0.004 (0.018 in the population view). What predicts sigma is how much the
  parameters change the level's response given the state (rank correlation +0.77 over cells). Checker: "the number of
  hidden parameters is not a dial" is not established (the sets are different worlds; block view 1 against 4 differs),
  the statements about experiments describe the scripted inference, and the data-only budgets are upper bounds.
- `round5/vortexexam`: an exam pilot on the fed-vortex world (two pilots, 6 and 10 truths). Level 2 has an effective law
  for the kind share, b1 s(1-s) + b2 (1-2s), real where selection is strong (eps >= 0.2). The prior-mean plug-in loses
  0.13-0.19 of oracle skill at the median truth (gliders: 0.03). With full-history items the no-experiment policy or a
  data-only fit still takes nearly all the skill (sigma about 0 and 0.06 in the net family; 0.136 +- 0.054 against the
  best C of any family). Checker: "without a simulator the law pays" fails a control (a constant in place of the
  selection term scores the same), each item view fails one acceptance bar and none is shown to fail both, and the gain
  from showing only the last three ticks is 0.10 +- 0.11 on a like-for-like basis.
- `round5/bias2`: the inductive-bias grid on two more level-0 theories. Membrane world: nonlinear closure beats the best
  hand design at 16 ticks (+0.12 to +0.25 depending on the predictor family) and, with spatially whitened latents, is
  the same variable across fit halves. Fed-vortex world: with the standard loss the closure latents take the run's common
  transient (a function of the tick alone carries 88% of the linear latent's box mean), not a world variable; with
  spatially whitened latents linear closure matches block vorticity (R^2 0.77). Gliders: block mass again. No bias gives
  an object variable. Checker: the "replication" reused the same simulations in two of three worlds; "closure finds the
  transported density" rests on one new case; replica means hide split outcomes.
- `round5/slots`: slot encoders with memory on raw gliders states. Closure, local-law and reconstruction objectives all
  settle on soft parts (about 2.1 slots per tracked body, ARI 0.63 against the tracker), although the architecture can
  express the tracker's view (supervised ARI 0.85) and all four objectives move a tracker-like start back to parts while
  their loss falls. By the closure ceiling the parts score above the tracker (+0.389 +- 0.018 at 16 ticks), so closure
  does not single out objects. Checker: one architecture, two starts, one level-0 theory; no parsimony term was tried.
- `round5/foundry`: world foundry v0, a two-kind transport neural automaton whose hidden weights are the law. 8,192 prior
  draws screen in 376 s on one H100 (about $6 per 100,000 draws); 1.07% pass four gates early, 0.35% at screen,
  certification and late time; a weights-only pre-screen enriches candidates 7.4 times (95% interval 5.6-9.8). Checker:
  the shortlist of seven "in the gliders band" uses a rule written after the first job and a linear predictor's
  ceilings; whether actions matter in these worlds is not established.
What round 5 decides: on two worlds, with a correct public simulator, a policy with no hypothesis and no experiment takes
nearly all the reachable skill, whatever the observed level or the number of hidden parameters tried; the exam designs
that remain are those of decision 1. Learned coarse-grainings depend on the level-0 theory and on the loss normalisation,
and none produces objects. Random weights-as-law worlds are cheap to generate and screen.

Round 6 (10-11 Nov 2026, in progress; the lead's direction for it is in `roadmap/DECISIONS.md`, section "Direction"):
- `roadmap/GRADER_VS_VERIFIERS.md` and `round6/vfport`: the exam as a verifiers environment on the library's isolated
  grader, proven with scripted agents on Docker, reviewed, red-teamed and audited for host safety in three rounds. The
  fourth round (two passes) carried the exam faults found by the first rollouts, a dollar cap enforced while a run is
  under way (with an allow-list of request keys), box caps, a bearer on the laboratory and rollouts driven by request
  files for the lead's Mac; its verdict at 0697487eb is GO for the scripted steps 0 to 2 on the Mac and NO-GO for model
  rollouts, on two findings: a box could make vf-eval on the Mac hold about 64 GiB through verifiers' own interception
  server, and one shell command can hold the agent longer than its run without the statement saying so (a rehearsal
  rollout lost 735 of its 900 s that way). A fifth round (in progress) closes both classes: every channel from a box
  into a host process bounded and tested, everything the agent is told checked against what happens.
- `round6/rollouts`: the first two model rollouts, on the ring smoke-test exam, $2.59. A strong model scored 0.964 of
  the oracle in six minutes with a closed-form filter (an estimated 0.05-0.08 of it from choosing its 32 samples
  jointly, which the fair energy score rewards); a cheap model was cut by a reply limit it had not been told and
  scored 0 by rule. The ring is trivially easy for a strong agent and tests bookkeeping in a weak one. Both rollouts
  exposed faults of the exam (failure paid with climatology, a one-tick reset, token limits that do not bound the bill).
- `round6/cards`: one card per world and level, computed by one tool on 77 worlds (140 runs, $2.68): predictability by
  horizon, bodies and whether a single-body law gives their motion, stationarity, the weight of the hidden part given
  the state, actions, cost. Block-level screen for the science share at 8 ticks: gliders 0.09-0.11, fed vortices
  0.07-0.09, membrane 0.01, the seven shortlisted foundry worlds 0.28-0.51. Checker: the numbers reproduce; the card
  does not single out the foundry shortlist independently (in that family the screen is the linear predictor's
  closure gap, the quantity round 5 selected on); the dial is the horizon, not the clock (at equal world time the
  cards agree, and a prior-sized error in the hidden part weighs 2-6% of the predictable variance at 8 ticks but
  32-55% at 32); the rank agreement with round 5's measured shares (0.83 over six cells) is fragile and untested on a
  positive; seven of twelve controls can hardly fail.
- `round6/foundryexam`: an exam pilot on the foundry automaton with all 250 weights hidden ($11.70; three arms: the
  screened prior, and 30% and 10% weight neighbourhoods of three centres). The no-experiment policy's share of the
  true-weights reference is 0.83-0.87 on the screened prior and at 30%, against 0.958 at 10%. At the declared null
  (512 Lab episodes) sigma fails the bar in every arm (0.02-0.07): fine-tuning on Lab data closes the gap without a
  hypothesis. Horizon is the strongest dial: at 16 ticks with 8 Lab episodes sigma is 0.15 or more in all 16 worlds of
  the screened prior. Checker: every number reproduces; neither the reference nor the no-experiment policy is
  saturated in compute, so the shares are values at this compute, not bounds; whether the long-horizon gap needs a
  hypothesis or only more prior simulations is open; no scripted policy chooses its Lab programs, so the study cannot
  say whether experimenting pays.
- `round6/dials`: three exam designs under decision 1 (a public law with a hidden term, on gliders; a hidden carrier
  level under the membrane cells; a compute limit on fed vortices), three adversarial critiques and `PLAN.md`. The
  compute limit does not bite on fed vortices (summed small boxes score as exam-size runs do) and is deferred.
  Study A (`dials/dialsA`, $2.08, checked): with real nets on round 5's ladder harness, a generic repair fitted on 8 Lab
  episodes (fine-tuning, or a per-block residual, which always won) closes 0.47 of the gap between P0 and the
  true-form net (one-sided 90% bounds 0.43 and 0.52; bar 0.7): "generic repair wins" is refuted, where the CPU stand-in
  had forecast 0.70 to 1.46. Checker: the base nets stopped at the declared step cap, not converged by the plan's rule
  (longer training widened the gap at each doubling); on the whole exam the P0-to-C share is 0.146 and 0.077 after the
  repair, so a reopened design can reach the 0.15 bar only on the triggered item classes at 8 to 16 ticks (0.25 and
  0.41 there). Study B stage 0 (`dials/dialsB`, $0.26, checked): the membrane carrier's CPU gate is a close call by the
  declared rule and a no-go at the point; B is not built. Checker: the gate did not test the carrier, because the
  hidden law is numerically unstable at the pilot centre (an explicit diffusion step at D_X = 0.5 grows a checkerboard
  mode in both arms) and every seed shared one hidden value; the question is undecided, not closed.
- `round6/foundrylong` ($8.93, checked): the foundry exam at 16 and 32 ticks with 32 Lab episodes. Stage 1: with five
  times the pilot's prior worlds (1,000), the no-experiment recipe still leaves a gap: sigma 0.218 at 16 ticks
  (one-sided lower bound 0.187; 0.178 with any one world left out), but only at this compute: the step from 210 to
  1,000 prior worlds took 0.114 of sigma and the recipe is still improving (S1a). Stage 2: the best generic recipe
  (fine-tune on Lab data) keeps a gap (T1 0.208, lower bound 0.178), and the obvious scientific move does not close it:
  fitting the 250 weights through the differentiable simulator and simulating scores 0.404 against the fine-tune's
  0.470 and the reference's 0.593 (T3 fails); designed Lab programs do not pay (T4 fails); verdict UNDECIDED by the
  declared rule. Even at the true weights that predictor reaches only 0.527 at 16 ticks: at 8 and 16 ticks the state
  filter on the block view is a limit by itself, at 32 ticks the predictor at the true weights ties the reference and
  the weight inference is the limit (checker's correction). Checker: every number reproduces; the fits ran 143 of 200
  declared steps and many had not converged; the designed Lab spent about twice the nats of the mix Lab.
- `round6/profile2`: the design of the first exam profile beyond the ring, for the foundry world (F) and gliders with
  triggered items (G), with measured costs on 2 CPU cores, a two-tier reference table (GPU ceiling after the rollout,
  box-compute scripts), a decision rule over the two studies' verdicts, the pin changes, and four questions for the lead
  (how the research budget is counted; which scripted share is the bar; whether the package may carry costly
  science-free material; a gliders pilot with an 8-CPU box). By its rule F does not qualify after foundrylong's
  undecided verdict.
What round 6 says so far: the toy exam is trivially easy for a strong agent. On every other world tried, generic
recipes (simulate the prior, then fine-tune or fit a residual on Lab data) take most of the skill at short horizons and
generous Lab budgets. Where they fall short is at long horizons with few Lab episodes, and there the compute given to
the recipe is a dial of its own. In the foundry world at 16 to 32 ticks, neither the generic recipe nor the obvious
scientific move takes the skill at this compute: the first setting that is not trivially easy for a script either way.
Rollouts in such a setting need exam profiles beyond the ring in the environment.
