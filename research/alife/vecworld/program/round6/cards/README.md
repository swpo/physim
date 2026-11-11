# World cards (round 6, 11 Nov 2026)

The program's working statement of "what interesting might look like from a more abstract perspective"
(the lead's direction, `../../roadmap/DECISIONS.md`): one tool that takes any world through a thin adapter and
computes the same card for it, so that worlds can be compared and the card can later be tested against what agents
do in rollouts. Every number below is in `results/summary.json` with its source (job, file, key). Not yet checked
by an independent reader.

**Pilots only.** Every hidden part here is a public function of public seeds (foundry prior seed 2026, public
default parameters). Never reuse these worlds as exam instances.

## The card

One tool (`cardlib.py`), one adapter per world (`adapters.py`), declared thresholds and verdicts (`gates.py`).
Three readings of a world: the block view, the tracker's slot list read as per-body steps, and a population
vector of the slot list (count, tracked mass, mean speed, sd and largest body mass, kind share).

| part | entries | how |
|---|---|---|
| 1 predictability | predictable fraction PF(h), closure ceiling c(h), h = 1 to 32 ticks, per level | oracle: 6 fresh-noise replicas from 32 held-out states; cheap family: climatology, persistence, closed-form ridge |
| 2 structure | bodies, half-life, speed, events; single-body law on quiet steps, alone and with the surrounding block view | the vw blob tracker on every member |
| 3 stationarity | tick share per channel, member share, a late window | two member halves; a second window `late_gap` ticks later |
| 4 effective laws | linear local law and where it breaks, population law, the fed-vortex kind-share law in every world | closed form |
| 5 levels | what the slot list adds to the block view's predictor and the reverse | the same ridges with added features |
| 6 learned variable | slow features of the 2 x 2 sub-blocks against the hand block view, learned on the other half | closed form |
| 7 actions | aimed 50 / 200 / 800-nat and blind 200-nat inputs against the twin floor | common noise |
| 8 hidden part | plug-in loss of a neighbour at 3%, 10%, 100% of the declared prior; response difference; noise twins | paired, common noise |
| 9 cost | ms per member-tick, compile excluded | timed runs |

Derived screen: **sigma_hat = min(w_theta, 1 - c)** averaged over 4, 8, 16 ticks, where w_theta is the share of
the predictable variance that a prior-sized error in the hidden part costs given the state. It is an upper screen
for the science share: simulating the public prior cannot lose more than w_theta, a data-only fit cannot lose more
than 1 - c. Verdicts: dull (nothing predictable; predictable by the cheap family; the hidden part has no weight)
or exam-worthy, plus reading-worthy (persistent bodies whose motion a single-body law does not give) and actions.

`HYPOTHESES.md` (committed before the first GPU request) says which patterns should go with exams that are not
trivially easy and with rollouts worth reading, and how rollouts can refute them. `DEVIATIONS.md` lists everything
done differently afterwards, with what had been seen by then. `check_cardlib.py` runs the estimators on a world
with closed-form answers (passes; `results/check_cardlib.json`).

## What ran

| job | GPU | billed | what |
|---|---|---|---|
| r6-cards-001 | A100 40GB (lambdalabs, $1.99/h) | $1.25 (0.63 h) | 70 worlds, 125 runs, all done, exit 0, 2,208 s |
| r6-cards-002 | JOB2_GPU | JOB2_BILLED | JOB2_WHAT |

Per run: 16 members x (burn-in + 400 ticks), tracker on every member; from 32 held-out states, 32 ticks of 30 arms
(6 oracle replicas, 12 hidden-part neighbours, 8 input arms, 4 response-difference arms); the card is built on the
pod in numpy. Runs: A and B (two run seeds), late (seed A, `late_gap` ticks later). Float64, JAX 0.12.0.1.
Worlds (`worlds.json`, `worlds2.json`): gliders wind world; fed vortices at 64 px (and 128 px); membrane cells;
round 5's seven shortlisted foundry worlds (also at 128 px); 16 of the other 81 screen candidates at random;
24 unselected prior draws; controls. CPU: a full-size run of foundry draw 4470 for the platform check.
The runner reviewed the job code while it ran (`results/jobs/*/review.md`); its findings are acted on in
`DEVIATIONS.md` (the tick share and one estimator were corrected before any result was read).

## Results

### The card passes its own test

CONTROLS_SENTENCE Two of these are dull almost by construction (noise, diffusion); the ones
that could have failed are the frozen draws and the free bodies. The margin is narrow in one place: a frozen draw
reaches sigma_hat 0.14 at the population level in its late window (bar 0.15). The free bodies look like the
gliders world on the block view (PF(8) 0.95, c(8) 0.74) and are dull because their hidden part has no weight
(sigma_hat 0.04 to 0.06) and a single-body law gives their motion (ceiling 0.96 to 0.98).

### The named worlds (run A; B and late in each `results/cards/<world>/card.md`)

| world | verdict | sigma_hat block | sigma_hat pop | PF(8) | c(8) | bodies | half-life | body law c(8) | action / cheap error | late = early |
|---|---|---|---|---|---|---|---|---|---|---|
NAMED_TABLE

Full table of all worlds: `results/table.md`. One page per world: `results/cards/<world>/card.md` with a figure.

### What the card says, part by part

1. **Predictability.** No named world is noise and none is closed: the block view is predictable at 8 ticks
   (PF 0.93 to 1.00) and the cheap family gets about half of it in gliders, vortices and four foundry worlds
   (c(8) 0.45 to 0.52) and three quarters in the other three (0.74 to 0.76). The membrane block view is closed at 8
   ticks (c 1.00) and still at 16 (0.97): on its native clock nothing a cell does falls inside the card's horizons.
   CLOCK_SENTENCE
2. **Structure.** Bodies persist for 11 to 51 ticks (membrane cells 215). The single-body law on quiet steps
   separates the worlds: gliders 0.97 and foundry 1672 0.95 move like the free-bodies control (0.98), that is by
   inertia; vortices 0.88, foundry 4186, 262 and 3078 0.86 to 0.89 sit at the gate (0.9) and flip with the seed;
   membrane 0.66, foundry 7567 0.67, 6845 0.46 and 4470 0.41 are clearly not single-body. Adding the surrounding
   block view to the body law gives nothing anywhere (at most +0.04). In the gliders world the interest is in the
   events (47 fusions and fissions per 100 ticks), not in the quiet motion.
3. **Stationarity.** The fed vortices' population level is a clock: 22% to 26% of its variance is a function of the
   tick alone in both seeds, 55% to 58% for the kind share (80% at 128 px), 4% in the late window. Foundry 4186 and
   3078 have a population transient in the early window (largest component 0.36 to 0.71) that is gone late.
   Foundry 4470 has a second regime: in run B three of 16 members grow a runaway body (largest body 770 to 1,250
   against 190); foundry 262 splits the same way at late time (5 of 16 members). The gliders world fails the
   declared stationarity gate for another reason: each episode keeps its own conserved masses (member share 1.0
   for the two mass channels, 0.43 for the third), which an agent reads off the history at once.
4. **Effective laws.** The linear local law holds at one tick everywhere (c(1) 0.98 to 1.00) and breaks between 8
   and 16 ticks; half of its excess error at 8 ticks sits in a tenth of the (state, block) cells. The kind-share
   law of round 5 is not better than a line in the share in any world; only the vortices have a constant drift of
   the share (ceiling 0.14 at 8 ticks, 0.28 at 32), which is the selection signal.
5. **Levels.** The slot list improves the block view's predictor by 0.034 of the variance in the gliders world and
   by 0.023 in foundry 262; elsewhere by 0.02 or less. The population level beats persistence by up to 0.75 in
   foundry worlds, but its closure is the card's least robust entry (below).
6. **Learned variable.** Slow features are less closed than the hand block view in most worlds (gliders -0.14 at
   16 ticks, five foundry worlds -0.12 to -0.30) and more closed in two: foundry 4470 (+0.09 at 16 ticks, +0.13 at
   32, both orders of the halves) and 7567 (+0.05, +0.09). The declared gate (at 8 ticks) passes nowhere.
   Slower is not more closed, as round 5's `bias2` found for the fed vortices (claim V8). Round 5 already answers
   the rest: every objective finds block mass in gliders (R^2 0.97 to 0.99) and no objective finds objects
   (`slots`: parts score 0.39 above the tracker at 16 ticks); nonlinear closure beats the hand view in the membrane
   world by 0.14 at 320 and 0.25 at 640 time units (`bias2` M3), horizons this card reaches only on the slow clock.
7. **Actions.** The declared gate (predictable shift of an aimed 200-nat input of at least 0.1 oracle variances)
   passes in 69 of 70 worlds, uniform controls included: it does not discriminate, and my expectation that most
   foundry worlds would fail it was wrong. In units of the cheap family's error the same shift is 1.8 to 2.2 in
   vortices and membrane, 0.27 to 0.47 in foundry 4186, 1672 and 3078, 0.13 to 0.20 in gliders and 7567, 0.09 in
   6845 and below 0.02 in 4470 and 262. Aiming matters: aimed over blind 2.6 to 9 except in the vortices (0.85:
   16 bumps, one aimed).
8. **Hidden part.** A 3% / 10% weight neighbour costs 6 / 82 oracle variances at 8 ticks (median of the seven; round 5:
   5 / 45 over 24 worlds). In the designed worlds a 10%-of-prior move costs 0.01 to 0.15 oracle variances, and a
   prior-sized error 6% (gliders), 6% (vortices) and 2% (membrane) of the block view's predictable variance.
   WATCH_SENTENCE
9. **Cost** on an A100 with the tracker on every member: foundry 0.047 ms per member-tick (21,400 per second;
   $0.03 per million), membrane 0.14 ms, gliders 1.5 ms ($0.83 per million), vortices 4.8 ms at 64 px ($2.64).

### Which entries are robust

Seed (runs A and B, 20 worlds; agreement within 0.05 or 25%): the block-view entries, the structure entries and the
plug-in losses agree in 90% to 100% of the worlds (PF(8), c(8), sigma_hat, w_theta, bodies, half-life, events,
tick share, the action shift). Not robust: the population level's ceiling (60%) and action shift (55%), the
aimed/blind ratio (70%), the learned variable at 16 ticks (75%), the member share (80%). Size (64 px against 128 px,
7 foundry worlds and vortices): the same split; the population ceiling agrees in 25%. Estimator size (even against
odd test states): c(8) agrees in 70 of 70 worlds. Platform: 11 of 11 entries of foundry 4470 agree between this
container's CPU and the A100. Late window: equal to early in 19 of 35 worlds with a late run (6 of 7 shortlisted,
7 of 16 other candidates, the three designed worlds). Gates that flip with the seed: membrane (exam-worthy),
foundry 4470 (stationary), foundry 262 (interaction, stationary). RERUN_SENTENCE

Consequence: **read sigma_hat at the block level.** The declared verdict takes the larger of the two levels, and
BLOCK_SENTENCE

### The hypotheses so far (only rollouts can decide them)

- **H1** (sigma_hat caps the science share). Consistent with everything round 5 measured: gliders block view 0.10
  against a measured share of 0.02, gliders population 0.20 to 0.26 against 0.11, vortices population 0.32 to 0.35
  against 0.14 at most. As an upper screen it is loose by a factor of 2 to 6. H1_SENTENCE
- **H2** (experiments pay only where watching does not identify). WATCH2_SENTENCE
- **H6** (a clock takes the level where the tick share is high): confirmed on the card for the fed vortices'
  population level in both seeds. The first version of the estimator would have hidden it (`DEVIATIONS.md` A1).
- **H7**: the gate as declared is useless (above).
- **H8**: the gate passes nowhere; the two worlds where the learned variable gains at 16 ticks are foundry worlds,
  not the membrane world I guessed.
- H3, H4, H5 need rollouts.

### Which worlds first, on the card's evidence alone

By the declared rule (exam-worthy, stationary in the window, the same at late time; reading-worthy first, then
actions, then sigma_hat; one per family): **foundry 4470** (reading-worthy, block sigma_hat 0.44, the hardest
single-body law, 0.41) and then **foundry 4186** (block sigma_hat 0.44 in all three runs, stationary in all three,
the largest action reach of the reading-worthy foundry worlds). I would put 4186 in front of agents first and 4470
second, because 4470's runaway regime in one seed makes its scores depend on which episodes are drawn. They are
weights-as-law exams: the data-only reference against the true-law reference. The fed vortices and the gliders
world fail the rule on stationarity (a clock at level 2; per-episode masses); the gliders world stays the
calibration point whose science share is known. MEMBRANE_SENTENCE Of the other screen candidates of round 5 only
two of 16 are exam-worthy at the block level (4289, 4495): at 8 ticks most of them are closed for the cheap family.

## What failed, and limits

- The population level's closure is not robust to seed or size; verdicts that rest on it alone are provisional.
- The actions gate does not discriminate; neither unit (oracle variance, cheap error) separates controls from
  interesting worlds on its own.
- The first job's response-difference estimator was biased low (corrected for the second job) and its tick share
  pooled channels (corrected offline); its two "diffusion" controls kept the mobility gain (true ones in job 2).
- The cheap family is linear: 1 - c overstates what a learned predictor leaves, so sigma_hat is loose where the
  data-only fit is strong. sigma_hat ignores identification from history.
- The card depends on the clock (membrane), on the box given to the hidden part where no exam prior exists
  (membrane, free bodies), and on the tracker (blind to dense phases; quiet steps are checked at both ends only).
- One architecture of card, two run seeds, 16 members: rare regimes (4470) are seen or missed by chance.

## Files

| file | what |
|---|---|
| `cardlib.py`, `adapters.py`, `gates.py` | the tool: simulation and analysis; one adapter per world; derived numbers, thresholds, verdicts |
| `HYPOTHESES.md`, `DEVIATIONS.md` | declared before the first request; what changed after, and when |
| `check_cardlib.py` | the estimators against a closed-form world |
| `make_worlds.py`, `worlds.json`, `make_worlds2.py`, `worlds2.json` | the declared lists of worlds and runs |
| `job.py`, `job.sh`, `fetch.sh`, `watch.sh` | the GPU job (also the CPU test at tiny size), fetching and waiting |
| `make_cards.py`, `make_summary.py` | job outputs to `results/` |
| `results/cards/<world>/` | `card.md`, `card.png`, `card.json` (derived numbers and gates of every run) |
| `results/table.md`, `table.csv`, `derived.json`, `robustness.json`, `summary.json`, `claims.md` | comparison table, every run's numbers, robustness, claims with sources |
| `results/jobs/`, `results/cpu_check/` | status, review, job state of each job; the CPU run of foundry 4470 |

Reproduce: `python -B check_cardlib.py`; `bash fetch.sh r6-cards-001; bash fetch.sh r6-cards-002`;
`python -B make_cards.py r6-cards-001=work/r6-cards-001/out r6-cards-002=work/r6-cards-002/out --rate 1.99`;
`python -B make_summary.py`. Raw job outputs stay on `origin/gpu-jobs`. A new world needs one function in
`adapters.py` (init, tick with the hidden part as an argument, two views, a tracker, a neighbour rule, an aim rule).
