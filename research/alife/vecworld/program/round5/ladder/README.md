# Round 5, study ladder (track 2): what makes a setting hard

**Question.** On the gliders wind world, does difficulty rise with the depth of the observed level and with
the number of hidden parameters, and which measurable property of a world predicts it?

**Answer.** No cell passes the roadmap's bar. The science share sigma is below 0.15 in all nine cells, and
simulating the public prior (P0) is within 0.000-0.047 of training at the true parameters (C).
- *Depth:* the 5-number population summary is the one view where the hidden parameters matter to a
  history-only predictor (sigma 0.04-0.11, against 0.005-0.018 in the block view and at most 0.007 in the
  object view). It still fails the bar, and no view makes inference or learning cost more episodes.
- *Number of hidden parameters:* 1, 4 or 8 makes no measurable difference to sigma or to any budget.
- *Identifiability* gets clearly worse with depth and with the number of parameters, but this does not carry
  over to prediction: two Lab episodes of scripted inference already match C within 0.004 (0.018 in the
  population view).
- *What predicts sigma:* how much the parameters change the level's response when the state is known
  (oracle minus the prior-mean simulator from the hidden state), rank correlation +0.77 over the nine cells;
  not the number of hidden parameters (-0.05), not posterior contraction (+0.27).

PILOT ONLY. The truths were drawn inside the job and are written in `results/job/n*/truths.json`. These
truths, Lab data and exam items must never be reused as an exam.

## What ran

One GPU job, `r5-ladder-002` (`r5-ladder-001` was rejected by the Mac's review before any pod, $0):
A100-SXM4-40GB, 1.28 h billed, $2.56, jax 0.12.0.1, float64 world and float32 nets, 3.65 million
member-ticks, exit 0 with no failed or skipped part, no net schedule cut.

Nine cells: observed view x number of hidden parameters, 8 hidden worlds per hidden set (24 in all).

| view | what the agent sees, infers from and predicts |
|---|---|
| block | 192 numbers: 3 channels on the 8 x 8 block grid (level 1, field view) |
| object | 144 numbers: 12 tracked bodies x 12 features (level 1, object view) |
| pop | 5 numbers computed from the object view: count, tracked mass, mean speed, SD of body mass, largest body |

| hidden set | parameters (uniform box conditioned on the public viability rule) |
|---|---|
| 1 | lR in 0.91-1.09 (all of the box viable) |
| 4 | lR, dm_00, ls_00, lh: the round-3 prior (93% of the box viable) |
| 8 | the four above + dm_10, ls_01, dm_01, lA: next in the headroom scan, scanned box x 0.6 (91% viable) |

Per truth: a Lab of 512 exam-mix episodes (budgets 2, 8, 32, 128, 512 are nested prefixes) plus 128
blind-twin episodes, 33 ticks each; one history exam of 48 items with 12 replicate futures, horizons
1, 2, 4, 8, 16 ticks, whose three levels are the three views (384 items per cell).

Reference policies, one predictor family per view (a generative net trained with the fair energy score):

| policy | what it is |
|---|---|
| K | climatology pool |
| D(N) | data only: the better of an unconditioned net and a ridge fitted to the first N Lab episodes |
| P0 | no hypothesis, no experiment: the theta-conditioned net with theta drawn from the prior per sample; P0u = an unconditioned net trained on prior-predictive simulations |
| PM | the conditioned net at the prior mean |
| S(N) | scripted inference from N Lab episodes (synthetic likelihood on the view's own summaries), then the conditioned net at posterior draws |
| C | the conditioned net at the true parameters |
| O | the simulator run from the hidden state (oracle, leave one out); plugPM = the same at the prior mean |

Scores: fair energy score per item and cell from the exam's own scorer; oracle-normalised skill (OES) from
`vw.scoring.skill_report`; sigma and rho from `round5/agentenv/evaluator/acceptance.py`.

## Results

OES; z over the 8 hidden worlds in brackets; sigma with its world-cluster SE; contraction = geometric mean
over parameters of posterior SD / prior SD; N90 = Lab episodes to reach 90% of C's skill.

| hidden | view | C | P0 | P0u | S(2) | D(512) | plugPM | C - P0 (z) | sigma at 32 | sigma at 512 | rho at 2 / 512 | contraction at 2 / 512 | N90 S / D |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | block | 0.688 | 0.684 | 0.652 | 0.688 | 0.625 | 0.873 | +0.004 (3.8) | 0.005 ± 0.001 | 0.005 | 0.82 / 0.82 | 0.27 / 0.03 | 0 / 451 |
| 1 | object | 0.436 | 0.434 | 0.421 | 0.437 | 0.410 | 0.837 | +0.003 (3.3) | 0.005 ± 0.002 | 0.005 | not defined | 0.30 / 0.03 | 0 / 215 |
| 1 | pop | 0.389 | 0.352 | 0.362 | 0.377 | 0.357 | 0.745 | +0.037 (5.2) | 0.081 ± 0.018 | 0.076 | 0.69 / 0.83 | 0.39 / 0.09 | 0 / 105 |
| 4 | block | 0.650 | 0.637 | 0.618 | 0.647 | 0.599 | 0.804 | +0.013 (4.9) | 0.018 ± 0.004 | 0.018 | 0.77 / 0.98 | 0.38 / 0.08 | 0 / 362 |
| 4 | object | 0.430 | 0.427 | 0.410 | 0.429 | 0.405 | 0.764 | +0.003 (1.7) | 0.006 ± 0.004 | 0.006 | not defined | 0.59 / 0.19 | 0 / 198 |
| 4 | pop | 0.349 | 0.302 | 0.302 | 0.331 | 0.331 | 0.651 | +0.047 (3.6) | 0.113 ± 0.035 | 0.050 | 0.64 / 0.81 | 0.72 / 0.46 | 2 / 323 |
| 8 | block | 0.681 | 0.671 | 0.647 | 0.677 | 0.630 | 0.867 | +0.010 (4.1) | 0.013 ± 0.003 | 0.013 | 0.61 / 0.92 | 0.69 / 0.51 | 0 / 363 |
| 8 | object | 0.438 | 0.438 | 0.419 | 0.438 | 0.412 | 0.833 | -0.000 (-0.0) | -0.001 ± 0.002 | -0.001 | not defined | 0.78 / 0.62 | 0 / 238 |
| 8 | pop | 0.393 | 0.374 | 0.362 | 0.390 | 0.367 | 0.759 | +0.019 (3.9) | 0.041 ± 0.013 | 0.041 | 0.82 / 0.88 | 0.89 / 0.76 | 0 / 106 |

rho is "not defined" where C - P0 is at most 0.003: its world-cluster SE is 0.3 to several hundred.

1. **Acceptance.** sigma is at most 0.113 ± 0.035 (4 hidden, population view, budgets up to 128); at 512
   episodes the data-only learner overtakes P0 there and sigma is 0.050. With the unconditioned P0u in
   place of P0 the largest sigma is 0.120. rho is 0.61-0.82 after 2 episodes and 0.77-0.98 from 8 on (the six cells where it is defined).
2. **Budgets.** P0 is already at 90% of C in eight cells and S(2) in the ninth. The data-only learner needs
   105-451 episodes and never reaches S(2)'s skill within 512. Value of theory: at least 53-226 times at
   90% of C, more than 256 times at the skill of S(2) (lower bounds: S is not measured below 2 episodes).
   The data-only budget does not rise with depth: relative to the block view it is 0.48-0.65 in the object
   view and 0.23-0.89 in the population view.
3. **Where the parameters pay.** Given the state they are worth 0.13-0.35 OES in every cell. A history-only
   predictor keeps 4-6% of that in the block view, 0.5-2% in the object view and 10-14% in the population
   view. In the population view the gain grows with the horizon (C - P0 from 0.005-0.013 at 1 tick to
   0.047-0.094 at 16 ticks).
4. **Identification by input arm** (128 episodes per arm, aimed and blind at 200 nats per episode on the
   same ticks). With 1 hidden parameter inputs tighten the posterior: aimed 0.45-0.72 of the passive SD in
   all three views, blind 0.41 and 0.50 in block and population and no gain in object. With 4 hidden
   parameters only the aimed push in the block view helps (0.87); with 8, every ratio to passive is within 0.95-1.09.
   Designed against blind at equal nats is mixed: better in 4 cells (0.69-0.94), worse in 2 (1.07, 1.51),
   equal in 3.
5. **Residual of scripted inference.** S(N) - C is within ±0.004 in the block and object views. In the
   population view it stays at -0.010 (4 hidden, z -3.7) and -0.007 (1 hidden, z -1.9) at 512 episodes.

## Limits

- One trained net per policy and cell: no SE includes training-seed variance. 8 hidden worlds per hidden
  set; the hidden sets have different truths, so comparisons across them are between worlds.
- Contraction is relative to this scripted inference (linear-regression summaries, synthetic likelihood with
  a misfit term that does not shrink with N). With 4 hidden parameters its 90% intervals cover 72-91% of
  the truths and the joint 90% region 3 of 8 in the object view at 512 episodes: somewhat overconfident.
- N90 is relative to C in the same cell, and C is far from the oracle (0.35-0.69).
- The mix arm's emulator has 8 design episodes per theta, the single-class arms 2: compare arms with each
  other, not with the mix.
- The secret is fresh per job, so the run is not reproducible bit for bit; float64 GPU runs are not
  bit-deterministic either.

## Files

| file | content |
|---|---|
| `results/summary.json` | every number above with its source (job id, file, key); `headline` holds the quoted ones |
| `results/job/` | the job's outputs (`posterior_draws.npz` stays at `origin/gpu-jobs:jobs/r5-ladder-002/out`), `results/status.json` its record |
| `results/check_lib.json`, `results/check_shapes.json` | CPU checks of the library; largest array of every traced program at full size |
| `ladder_lib.py`, `ladder_net.py` | views, hidden sets, summaries, synthetic likelihood, ridges; the three view nets |
| `run_ladder.py`, `make_summary.py` | the GPU job; the summary from its outputs (CPU, about 2 minutes) |
| `check_lib.py`, `check_shapes.py` | the checks |
| `recheck.py` | plain-numpy recomputation of the table's skills and shares from the saved scores (`results/recheck.json`: agrees to 5e-5) |
| `PROGRESS.md` | log of the study |
