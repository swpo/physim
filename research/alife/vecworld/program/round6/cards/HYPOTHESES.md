# World cards: hypotheses, declared before the GPU run (11 Nov 2026)

Committed before any full-size card existed. What I had seen when writing this: CPU runs at small size (4 to 8
members, 48 to 200 ticks) of foundry draw 4470, of the pure-noise control and of the non-interacting-bodies
control, used to debug the tool. Four rules below were written after those runs or after the closed-form check and are marked so.
The thresholds live in `gates.py` (`TH`); the list of worlds and runs in `worlds.json`.

The card is the program's working statement of "what interesting might look like from a more abstract
perspective" (the lead, DECISIONS.md, Direction). It is a claim, not a result: each hypothesis says which
pattern on the card should go with an exam that is not trivially easy or with rollouts worth reading, and what
observation in exams and rollouts would refute it.

## What the card holds

One tool (`cardlib.py`), one thin adapter per world (`adapters.py`), the same entries for every world.
Levels: the block view (grid), the tracker's slot list read as per-body steps (bodies), a population vector of
the slot list (pop: count, tracked mass, mean speed, sd and largest body mass, kind share).

| part | entry | how |
|---|---|---|
| 1 predictability | predictable fraction PF(h), closure ceiling c(h), closure gap, h = 1 to 32 ticks, per level | oracle = 6 fresh-noise replicas from 32 held-out states; cheap family = climatology, persistence, closed-form ridge |
| 2 structure | bodies, half-life, speed, events per 100 ticks, wavelength, block and time correlation | the vw blob tracker on all members |
| 2 interaction | single-body law on quiet steps: ceiling of a body's displacement; gain from adding the surrounding block view | ridge per body; quiet = same identity, no tracker event, mass within x 1.5 |
| 3 stationarity | tick share (variance that is a function of the tick alone), member share (variance between members' time-means), late window against early | covariance of two member halves; a second window `late_gap` ticks later |
| 4 effective laws | linear local law (c at 1 tick), where it breaks (horizon, share of the excess error in the worst 10% of blocks); linear and quadratic population law; the fed-vortex kind-share law for every world | closed form |
| 5 levels | gain of the block view's predictor from the slot list; of the body law from the block view; of the population law from block moments | the same ridges with added features |
| 6 learned variable | slow features (time-lagged, lag 8) of the 2 x 2 sub-blocks, learned on one half of the fit members, against the hand block view on the other half, both orders | closed form; the family contains the hand view |
| 7 actions | paired displacement of an aimed 50 / 200 / 800-nat input and of a blind 200-nat one against the twin floor; its predictable part MS | common noise, 2 replicas |
| 8 hidden part | plug-in loss of a neighbour at 3%, 10%, 100% of the declared prior, per level; response difference (does the response to an input depend on the hidden part); noise-twin divergence | 2 directions x 2 replicas on the noise of the oracle's first two replicas (paired estimator) |
| 9 cost | seconds per member-tick on the job's GPU, compile excluded | timed runs |

Part 6 also quotes round 5 (`bias2`, `slots`) where those studies already answer the question; nothing of
theirs is retrained.

## Conventions that decide what the numbers mean

- **Typical state (after CPU).** Ratios are built from medians over the 32 test states; mean-based values are
  kept beside them. Reason: in the CPU run of draw 4470 one member of eight grew a runaway body and carried
  every mean. An exam score is a mean over items, so the mean-based value is the exam's; the median says
  whether a few episodes carry it.
- **Cheap family includes persistence (after CPU).** Round 5 used the ridge or climatology. The ridge
  extrapolates badly for a member far from the fit members; persistence does not. Ceilings here can only be
  higher than round 5's.
- **Quiet steps (after CPU).** The body law is scored on steps without a tracker event. Without that rule the
  non-interacting control looked interacting, because overlapping bodies merge in the tracker.
- **Paired plug-in loss (after the closed-form check).** `check_cardlib.py` runs the estimators on a world with
  known answers. Round 5's unpaired estimator could not resolve a plug-in loss below about 0.01 of the variance
  there; with common noise and paired differences it is exact to the fourth decimal. The card uses the paired
  one and keeps the unpaired one beside it (`pl_unpaired`).
- **A move of the hidden part is measured in units of its declared prior**, not of its value: foundry =
  round 5's weight neighbour; gliders and vortices = their exam priors; membrane and the two made controls =
  boxes declared in `adapters.py` (no exam prior exists for them, so their hidden-part entries depend on my box).
- **No iteratively trained model enters the card.** Every predictor is a closed-form fit, so there is no
  training-seed variance; the analogue is the fit sample. It is covered by a second run seed (B) for the named
  worlds and by both orders of the halves for the learned variable. Error bars are bootstraps over test states.
- **Like with like.** Learned and hand variables are scored by the same predictor on the same members. Costs
  exclude compile time for every world.

## Hypotheses

**H1. The science share is capped by sigma_hat = min(w_theta, 1 - c).** w_theta is the share of the predictable
variance that a prior-sized error in the hidden part costs given the state (it caps what simulating the public
prior can lose); 1 - c is what the cheap family leaves (it caps what a data-only fit can lose); the null policy is
the better of the two. Averaged over 4, 8, 16 ticks at the observed level.
*Prediction:* an exam on a (world, level) with sigma_hat < 0.15 fails the science-share bar whatever the items;
over six or more (world, level) cells the rank correlation of the measured science share with sigma_hat is above
0.5. *Refuted if* a cell with sigma_hat < 0.10 passes the bar, or the rank correlation is zero or negative.
*Known in advance:* round 5 measured science shares below 0.12 in nine gliders cells and about 0 to 0.14 on
vortices, so the gliders card should give sigma_hat below about 0.15 at the block level. If it gives much more,
the screen is too loose to be useful (it is an upper screen: history that identifies the hidden part lowers the
real share).

**H2. Experiments pay only where watching does not identify the hidden part and the response to an input
depends on it.** The card's evidence index (nats per tick about a 10%-of-prior move) times the history length
says how fast passive watching identifies the hidden part; the response difference says whether an aimed
200-nat input behaves differently in a neighbouring world.
*Prediction:* Lab use raises the score of an agent only on worlds where ticks_to_3nats(0.1) exceeds the item
history and the response difference at 4 ticks is at least the oracle variance. On the gliders world I expect
watching to identify within a few ticks (round 5: two Lab episodes of scripted inference matched the true
parameters), so experiments will not pay there. *Refuted if* agents gain from experiments where the card says
watching suffices, or do not gain where it says they should.

**H3. Rollouts separate agents only inside a band of closure.** Worlds whose observed level has PF(8) >= 0.3 and
a cheap ceiling between 0.2 and 0.8 at 8 ticks leave room between a recipe and the oracle.
*Prediction:* on such worlds different agents land at clearly different places between the data-only reference
and the true-parameter reference; on worlds with c(8) >= 0.95 every agent lands on the data-only reference, and
with PF(8) < 0.1 every agent lands on climatology. *Refuted if* agents separate on a world the card calls closed
or noise, or do not separate anywhere in the band.

**H4. Rollouts are worth reading where bodies persist and the single-body law fails.** Gate `reading_worthy`:
at least 2 bodies, half-life at least 16 ticks, moving or eventful, displacement on quiet steps predictable
(PF >= 0.3) with a single-body ceiling at most 0.9.
*Prediction:* on such worlds agents write object-level hypotheses (collision, growth, division rules) and those
who do beat block-view fitters at 8 ticks and beyond; on worlds without bodies, or with free bodies, no such
difference appears. *Refuted by* reading rollouts: no object-level reasoning on reading-worthy worlds, or the
same amount on the others.

**H5. A second level is worth showing only where it adds.** Gate `levels_add`.
*Prediction:* agents given both views beat agents given one only where the gate passes.

**H6. Where the tick share is high, a clock takes the skill.** If more than a tenth of a level's variance is a
function of the tick alone, a policy that predicts the tick-mean takes at least that share of the skill, and an
exam on that level needs a clock reference policy. I expect this at the population level of the fed vortices
(kind share after labelling; round 5's `bias2` found a learned latent that was 88% a function of the tick).
*Refuted if* the vortex population level has a tick share below 0.1 in both run seeds.

**H7. Programs in the item mix matter only where act_ms >= 0.1.** act_ms is the loss of an input-blind oracle
under an aimed 200-nat input, in units of the oracle variance (the program's own criterion). Round 5 left the
foundry's wind as "not established". I expect most foundry worlds to fail this gate and the gliders world to
pass it. *Refuted for a world if* agents that ignore inputs lose skill there although the gate fails.

**H8. The obvious variable is not the best one only in some worlds.** Gate `learned_differs` (slow features beat
the hand view by 0.05 in ceiling at 8 ticks in both orders and are not the hand view).
*Prediction from round 5:* membrane passes at 16 ticks or beyond (nonlinear closure beat the best hand design by
0.12 to 0.25 there); gliders does not (every objective found block mass). The card's features are linear, so a
failure here does not contradict round 5's nonlinear result; a pass on gliders would.

## The card's own test

Negative controls must come out dull (`gates.py`, verdict starting with "dull"): the pure-noise field, the four
uniform and four frozen foundry draws, the two diffusion worlds, and the non-interacting bodies. Expected reasons:
noise = nothing predictable; uniform, frozen, diffusion = predictable by the cheap family; free bodies = the
hidden part has no weight (and `interaction` fails). **If a control comes out exam-worthy, the card as defined
here fails**, and I will say so rather than move a threshold.

Honest limits known before the run: the free-bodies verdict depends on the box I gave its hidden part; the
cheap family is linear, so 1 - c overstates what a learned predictor leaves (round 5's checker on the foundry
shortlist); sigma_hat ignores identification from history; the tracker is blind to dense phases.

## Which worlds first (rule declared now, answer after the run)

Among worlds that are exam-worthy, stationary in the window and the same at late time: reading-worthy first,
then those passing the actions gate, then by sigma_hat; at most one world per family before a second of any
family. My guess before the run, so that it can be wrong: a foundry mover (draw 1672 or 4470) as a
weights-as-law exam, the membrane world as a variable-discovery exam, and the gliders world kept as the
calibration point whose science share is already known. I expect the fed vortices to fail stationarity at
level 2 and at least one shortlisted foundry world to fail the late window.

## What counts as robust

An entry is seed-robust if runs A and B agree within 0.05 absolute or 25% (`gates.robust`), size-robust if the
128 x 128 run agrees with the 64 x 64 one in the same sense (foundry shortlist, vortices). A gate is robust if
it gives the same answer in A and B. I will list the entries that fail.
