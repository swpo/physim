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
| r6-cards-002 | A100 40GB (lambdalabs, $1.99/h) | $1.43 (0.72 h) | 10 worlds, 15 runs, all done, exit 0, 2,559 s |

Total billed: $2.68 of the $25 budget (1.35 billed pod-hours).

Per run: 16 members x (burn-in + 400 ticks), tracker on every member; from 32 held-out states, 32 ticks of 30 arms
(6 oracle replicas, 12 hidden-part neighbours, 8 input arms, 4 response-difference arms); the card is built on the
pod in numpy. Runs: A and B (two run seeds), late (seed A, `late_gap` ticks later). Float64, JAX 0.12.0.1.
Worlds (`worlds.json`, `worlds2.json`): gliders wind world (4 hidden parameters; also 1 and 8); fed vortices at
64 px (and 128 px); membrane cells; membrane and vortices on a clock of 4 world ticks; round 5's seven shortlisted
foundry worlds (also at 128 px); 16 of the other 81 screen candidates at random; 24 unselected prior draws;
14 controls. In all 77 worlds, 140 runs. CPU: a full-size run of foundry draw 4470 for the platform check.
The runner reviewed the job code while it ran (`results/jobs/*/review.md`); its findings are acted on in
`DEVIATIONS.md` (the tick share and one estimator were corrected before any result was read).

## Results

### The card passes its own test

All 31 runs of the 12 negative controls come out dull: the pure-noise field (nothing predictable), four uniform and
four frozen foundry draws and two true diffusion worlds (predictable by the cheap family, or no weight of the hidden
part), and the non-interacting bodies (the hidden part has no weight). The two no-affinity worlds of the first job,
which are not true diffusion controls, are dull as well and are not counted. Noise and diffusion are dull almost by
construction; the controls that could have failed are the frozen draws and the free bodies. The margin is narrow in
one place: a frozen draw reaches sigma_hat 0.14 at the population level in its late window (bar 0.15). The free
bodies look like the gliders world on the block view (PF(8) 0.95, c(8) 0.74) and are dull because their hidden part
has no weight (sigma_hat 0.04 to 0.06) and a single-body law gives their motion (ceiling 0.96 to 0.98).

### The named worlds (run A; B and late in each `results/cards/<world>/card.md`)

| world | verdict | sigma_hat block | sigma_hat pop | PF(8) | c(8) | bodies | half-life | body law c(8) | action / cheap error | late = early |
|---|---|---|---|---|---|---|---|---|---|---|
| gliders | exam-worthy + actions | 0.11 | 0.16 | 0.99 | 0.49 | 7.7 | 24.2 | 0.96 | 0.12 | yes |
| vortex64 | exam-worthy + reading-worthy + actions | 0.082 | 0.35 | 0.93 | 0.46 | 8.0 | 51.3 | 0.88 | 1.81 | yes |
| membrane | exam-worthy + reading-worthy + actions | 0.012 | 0.16 | 1.00 | 1.00 | 14.5 | 215 | 0.66 | 2.19 | yes |
| membrane, slow clock | exam-worthy + reading-worthy + actions | 0.24 | 0.35 | 0.97 | 0.84 | 14.9 | 52.0 | 0.46 | 0.43 | n/a (overlap) |
| vortex64, slow clock | exam-worthy + reading-worthy + actions | 0.28 | 0.42 | 0.42 | 0.24 | 8.6 | 18.9 | 0.28 | 1.85 | n/a (overlap) |
| foundry 4470 | exam-worthy + reading-worthy + actions | 0.44 | 0.89 | 1.00 | 0.52 | 18.9 | 22.0 | 0.41 | 0.015 | yes |
| foundry 4186 | exam-worthy + reading-worthy + actions | 0.44 | 0.68 | 0.99 | 0.50 | 10.1 | 20.4 | 0.86 | 0.38 | yes |
| foundry 0262 | exam-worthy + reading-worthy + actions | 0.49 | 0.71 | 1.00 | 0.51 | 12.0 | 20.1 | 0.88 | 0.001 | no |
| foundry 7567 | exam-worthy + actions | 0.48 | 0.77 | 0.99 | 0.50 | 11.1 | 11.2 | 0.67 | 0.16 | yes |
| foundry 6845 | exam-worthy + actions | 0.31 | 0.92 | 1.00 | 0.74 | 12.4 | 14.2 | 0.46 | 0.098 | yes |
| foundry 1672 | exam-worthy + actions | 0.28 | 0.49 | 1.00 | 0.76 | 4.1 | 37.3 | 0.95 | 0.33 | yes |
| foundry 3078 | exam-worthy + reading-worthy + actions | 0.29 | 0.54 | 1.00 | 0.74 | 13.2 | 36.2 | 0.89 | 0.33 | yes |
| free bodies (control) | dull: the hidden part has no weight | 0.007 | 0.063 | 0.95 | 0.74 | 5.4 | 40.4 | 0.98 | 0.66 | yes |

Full table of all worlds: `results/table.md`. One page per world: `results/cards/<world>/card.md` with a figure.

### What the card says, part by part

1. **Predictability.** No named world is noise and none is closed: the block view is predictable at 8 ticks
   (PF 0.93 to 1.00), and the cheap family gets about half of it in gliders, vortices and four foundry worlds
   (c(8) 0.46 to 0.52) and three quarters in the other three (0.74 to 0.76). The membrane block view is closed at
   8 ticks (c 1.00) and still at 16 (0.97): on its native clock nothing a cell does falls inside the card's
   horizons. On a clock of 4 world ticks (40 time units, round 5's choice) the same block view opens (c(8) 0.84)
   and a prior-sized error in the nine rate parameters costs 58% of the predictable variance instead of 2%. The
   fed vortices on the slow clock: PF(8) 0.42, c(8) 0.24. At 128 px with the same 8-px blocks the vortices' block
   view is much less closed than at 64 px (c(8) 0.17 against 0.46); the seven foundry worlds keep their block-view
   entries at 128 px.
2. **Structure.** Bodies persist for 11 to 51 ticks (membrane cells 215). The single-body law on quiet steps
   separates the worlds: gliders (0.96 to 0.98) and foundry 1672 (0.95) move like the free-bodies control, that is
   by inertia; vortices (0.86 to 0.89) and foundry 4186, 262 and 3078 (0.86 to 0.94) sit at the gate (0.9) and flip
   with the seed; membrane (0.66 to 0.74), foundry 7567 (0.49 to 0.78), 6845 (0.09 to 0.46) and 4470 (0.28 to 0.43)
   are not single-body. Adding the surrounding block view to the body law gives little (ceiling +0.09 at most).
   In the gliders world the interest is in the events (47 fusions and fissions per 100 ticks), not in the quiet
   motion.
3. **Stationarity.** The fed vortices' population level is a clock: 22% to 26% of its variance is a function of
   the tick alone in both seeds, 55% to 58% for the kind share (80% at 128 px), 4% in the late window. Foundry
   4186 and 3078 have a population transient in the early window (largest component 0.36 to 0.71) that is gone
   late. Foundry 4470 has a second regime: in run B three of 16 members grow a runaway body (largest body 770 to
   1,250 against 190); foundry 262 splits the same way at late time (4 of 16 members). The gliders world fails the
   declared stationarity gate for another reason: each episode keeps its own conserved masses (member share 1.0
   for the two mass channels, 0.41 for the third), which an agent reads off the history at once.
4. **Effective laws.** The linear local law holds at one tick everywhere (c(1) 0.98 to 1.00) and breaks between
   8 and 16 ticks; 46% to 67% of its excess error at 8 ticks sits in a tenth of the (state, block) cells. Round
   5's kind-share law is not better than a line in the share in any world. Only the vortices have a constant
   drift of the share (ceiling 0.14 at 8 ticks, 0.28 at 32): the selection signal. It belongs to the early
   window: on the slow clock, whose window runs to t = 8,500, it is gone.
5. **Levels.** The slot list improves the block view's predictor by 0.02 of the variance in the gliders world
   (-0.02 to 0.04 over eight runs) and by 0.02 or less in the other named worlds. The population level beats
   persistence by up to 0.75 in foundry worlds, but its closure is the card's least robust entry (below).
6. **Learned variable.** Slow features are less closed than the hand block view in most worlds (gliders -0.09 to
   -0.22 at 16 ticks, five foundry worlds -0.12 to -0.30) and more closed in two: foundry 4470 (+0.09 at 16 ticks,
   +0.13 at 32, both orders of the halves) and 7567 (+0.05, +0.09). The membrane world shows no gain on either
   clock (-0.03, -0.05). The declared gate (at 8 ticks) passes nowhere. Slower is not more closed, as round 5's
   `bias2` found for the fed vortices (claim V8). Round 5 already answers the rest: closure and local-law
   objectives find block mass in gliders (R^2 0.92 to 0.99) and no objective finds objects (`slots`: parts score
   0.39 above the tracker at 16 ticks); nonlinear closure beats a single hand block mean in the membrane world by
   0.14 at 320 and 0.25 at 640 time units (`bias2` M3). That comparison is against one channel and with a
   nonlinear encoder; this card's is linear and against four channels, so the two do not contradict each other.
7. **Actions.** The declared gate (predictable shift of an aimed 200-nat input of at least 0.1 oracle variances)
   passes in 76 of 77 worlds, uniform controls included: it does not discriminate, and my expectation that most
   foundry worlds would fail it was wrong. In units of the cheap family's error the same shift is 1.8 to 2.2 in
   vortices and membrane, 0.27 to 0.47 in foundry 4186, 1672 and 3078, 0.12 to 0.20 in gliders and 7567, 0.09 in
   6845 and below 0.02 in 4470 and 262. Aiming matters (aimed over blind 2.6 to 9) except in the vortices (0.85:
   16 bumps, one aimed).
8. **Hidden part.** A 3% / 10% weight neighbour costs 6 / 82 oracle variances at 8 ticks (median of the seven;
   round 5: 5 / 45 over 24 worlds). In the designed worlds a 10%-of-prior move costs 0.01 to 0.15 oracle
   variances, and a prior-sized error 6% (gliders), 6% (vortices) and 2% (membrane) of the block view's predictable
   variance. Watching identifies the hidden part quickly: the evidence index gives 3 nats about a 10%-of-prior
   move within 1 to 7 ticks of the block view in the gliders world, 1 tick in membrane, 14 to 19 ticks in the
   vortices, at once in foundry worlds. The response to an aimed 200-nat input changes by 0.2 to 0.3 oracle
   variances under a prior-sized move in the gliders world and by 0.02 to 0.03 in vortices and membrane (corrected
   estimator, second job); by 3 to 39 in foundry worlds.
9. **Cost** on an A100 with the tracker on every member: foundry 0.047 ms per member-tick (21,400 per second;
   $0.03 per million), membrane 0.14 ms, gliders 1.5 ms ($0.80 per million), vortices 4.8 ms at 64 px ($2.64).

### Which entries are robust

Seed (runs A and B, 23 worlds; agreement within 0.05 or 25%): the block-view entries, the structure entries and the
plug-in losses agree in 91% to 100% of the worlds (PF(8), c(8), sigma_hat, w_theta, bodies, half-life, speed, events,
tick share, the action shift); the body-law ceiling in 87%. Not robust: the population level's ceiling (57%), action
shift (43%) and sigma_hat (78%), the aimed/blind ratio (70%), the learned variable at 16 ticks (74%), the member
share (83%). Size (64 px against 128 px, 7 foundry worlds and the vortices): the same split; the population ceiling
agrees in 25%, and the vortices' block-view ceiling does not agree. Estimator size (even against odd test states):
c(8) agrees in 76 of 77 worlds. Platform: 11 of 11 entries of foundry 4470 agree between this container's CPU and
the A100. Late window: equal to early in 19 of 35 worlds with a late run (6 of 7 shortlisted, 7 of 16 other
candidates, the three designed worlds, 3 of 9 controls); the two slow-clock late windows overlap run A's and are
not counted. Gates that flip with the seed: membrane and gliders with 8 hidden parameters (exam-worthy), foundry
4470 (stationary), foundry 262 (interaction, stationary). The same seeds run in both jobs give identical cards for
vortices and membrane (29 of 29 entries) and another sample for gliders (24 of 29: GPU runs of that world are not
bit-reproducible).

Consequence: **read sigma_hat at the block level.** The declared verdict takes the larger of the two levels, and
the three designed worlds on their native clocks are exam-worthy through the population level only: their block
sigma_hat is 0.09 to 0.11 (gliders), 0.07 to 0.09 (vortices) and 0.01 (membrane) in every run, below the 0.15 bar.
The same holds for 8 of the 10 exam-worthy screen candidates and for the one exam-worthy prior draw. At the block
level alone the bar is passed by the seven shortlisted worlds (0.28 to 0.51 in all 21 runs), 2 of 16 other
candidates, 0 of 24 unselected draws, 0 of 14 controls, and by membrane (0.24 to 0.25) and vortices (0.28; 0.20
late) on the slow clock.

### The hypotheses so far (only rollouts can decide them)

- **H1** (sigma_hat caps the science share). Consistent with everything round 5 measured: gliders block view 0.10
  against a measured share of 0.02, gliders population 0.16 to 0.26 against 0.11, vortices population 0.32 to 0.35
  against 0.14 at most. As an upper screen it is loose by a factor of 2 to 6. On the six gliders cells whose share
  round 5 measured (block view and population x 1, 4, 8 hidden parameters) the rank correlation of sigma_hat with
  the measured share is 0.83 (for six points the one-sided 5% value is 0.83), and sigma_hat is at or above the
  measured share in all six (by 0.002 in one). This is a retrodiction: the shares were known when the card was
  built.
- **H2** (experiments pay only where watching does not identify). The card predicts that experiments will not pay
  in gliders, vortices or membrane: watching identifies a 10%-of-prior move within 19 ticks at most, and the
  response to an input hardly depends on the hidden part (at most 0.4 oracle variances, slow clock included). In
  foundry worlds the response depends strongly on the weights, but so does everything else.
- **H6** (a clock takes the level where the tick share is high): confirmed on the card for the fed vortices'
  population level in both seeds. The first version of the estimator would have hidden it (`DEVIATIONS.md` A1).
- **H7**: the gate as declared is useless (above).
- **H8**: the gate passes nowhere; the two worlds where the learned variable gains at 16 ticks are foundry worlds,
  not the membrane world I guessed.
- H3, H4, H5 need rollouts.

### Which worlds first, on the card's evidence alone

The declared rule (exam-worthy, stationary in the window, the same at late time; reading-worthy first, then
actions, then sigma_hat; one per family before a second), read on run A, gives: **foundry 4470**, then the
**membrane world** (the only other family that qualifies), then foundry 4186 and 3078. Two of these rest on
entries that are not robust: the membrane world's verdict on its native clock is the population level's (0.16 in
run A, 0.11 and 0.14 in B and late), and 4470 fails stationarity in run B (runaway bodies in 3 of 16 members).

Using the block level and all runs, I would put in front of agents:
1. **foundry 4186**: block sigma_hat 0.44 in all three runs, stationary in all three, late equal to early, the
   largest action reach of the reading-worthy foundry worlds (0.36 to 0.47 of the cheap error), a single-body law
   at the gate (0.86 to 0.89);
2. **foundry 4470**: the same block sigma_hat, the world where the single-body law fails most (0.28 to 0.43) and
   the learned variable gains, with the caveat that its scores will depend on which episodes are drawn;
3. **the membrane world on the slow clock**: block sigma_hat 0.24 to 0.25 in three runs, single-body law 0.46 to
   0.56, stationary in the window; its late window overlaps run A's, so that check is still owed.

The first two are weights-as-law exams: the data-only reference against the true-law reference. The fed vortices
and the gliders world fail the rule on stationarity (a clock at level 2; per-episode masses); the gliders world
stays the calibration point whose science share is known. Of the other screen candidates of round 5 only 2 of 16
are exam-worthy at the block level (4289, 4495): at 8 ticks most of them are closed for the cheap family. Draw
4289 (block sigma_hat 0.23, reading-worthy, late equal to early) is the one to add to the shortlist.

My guess before the run (HYPOTHESES.md) named a foundry mover (1672 or 4470), the membrane world and gliders as
calibration, and expected the vortices to fail stationarity at level 2 and one shortlisted world to fail the late
window. 4470, the vortices and the late window (262) came out as guessed; 1672 did not (its bodies move by
inertia), and the membrane world qualifies for a reason I did not guess (the clock, not a learned variable).

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
