# Study (b) on a second world: a hidden carrier level under the phase-membrane cells

Round 6, dials, designer `sublevel_second`, 11 Nov 2026. A design: no GPU job, no model call. Every number in
sections 0 to 3 was run here on CPU at tiny size and names its file (`R/` = this folder's `results/`; tables by
`make_table.py` into `R/table.json`). Sizes, costs and thresholds in sections 5 to 7 are declarations or estimates
and say so. Hidden values printed anywhere in this folder are pilot values, **never to be reused as an exam**.

## 0. The world: phase-membrane cells

| world | cost | do inputs move the observed level | a level below the public law | verdict |
|---|---|---|---|---|
| fed vortices | 169-444 member-ticks/s, $3.3-4.5 per million (`round5/vortexexam` README 1; checker 10) | yes | below the level-2 law lies level 0 itself: a dial with no zero point; with 6-10 truths sigma carried errors of 0.05-0.16 (README 4, 5) | loses: the dial cannot be resolved at this price |
| foundry automaton | 74,700 member-ticks/s (`round5/foundry` README) | no: an aimed 200-nat command moves the block view by 0.0002-0.023 of its variance; "whether actions matter is not established" (checker) | the weights are the law: there is no form to tell H | loses: an experimenter has nothing to do |
| membrane cells | 0.0123 CPU-s per member-tick, 13 times cheaper than gliders' 0.164 (`track1/membrane_world` summary `timing`; `round5/agentenv` summary `cost`); level 0 alone 2,717 member-ticks/s on an A100 40GB (`round5/bias2/results/membrane_w/sim_A.json`) | yes, locally: an oracle that ignores an aimed 300-nat program loses 0.69-0.74 of the range in the focus view of section 1, 0.08-0.14 in the population view (`R/screen_public_128.json`) | chemistry: an intermediate species the public law has eliminated | chosen |

## 1. The exam

**World.** Membrane cells, 128 x 128 px, tick = 10 time units, 150 ticks of formation inside the reset (one label
gives one formed state, with fresh noise each time). **Observed:** level 1, the cell list. **Scored** at 8, 16 and
32 ticks after a 16-tick history, under a held-out program: the population pair (N, mean size) of level 2, and a
local level-1 view, the *focus view* (cell mass and catalyst mass within 16 px of the item's public focus point,
the largest cell of the last history frame). Program mix: none 1/4, blind 1/4, aimed pulse 1/2 (sign, 2-20 ticks,
onset 0-8, centre 0-16 px off the focus, 100-300 nats).

**Public:** the membrane law (`membrane_jax.py`), coarse-grainings, channel, priors, mix, scales. **Hidden:**
(i) parameters of the public law, as in round 5 (the set is fixed by a viability and headroom scan before the
job); (ii) a level under the substrate field. Of each realised channel coefficient c = u + eta the share
lam c^2 / (c^2 + a0^2) arrives as a *carrier* X that is inert in the medium: it diffuses (D_X), is neither eaten
nor washed out, and becomes substrate only where cell catalyst is (rate rho K / 0.25). The rest arrives at once,
as in the public law, which is the limit of instant conversion. rho, D_X and a0 are hidden per world. Everything
still enters through u + eta, so the nats charge stays exact (`sublevel.py`, candidate `pro`).

**Told:** "Your simulator is approximate: the real world holds state the public law lacks. Where, how, or whether
at all is not stated." The same words at every dial setting.

**Dial:** lam in {0, 0.25, 0.5, 1}; its measured size is the screen gap of section 3. **Zero point:** at lam = 0
nothing is carried and X stays 0. Checked three ways. (1) `check_zero.py`: fields, level 1 and level 2 equal the
public world's bit for bit (`R/check_zero.json`, `candidates.pro.bit_for_bit`). (2) In the job, two truths at
lam = 0 also run through `membrane_world.build` unchanged and must score the same on every item. (3) The lam = 0
arm *is* round 5's design: correct law, hidden parameters, the same harness, policies and `acceptance.py`. No
round-5 exam exists on this world, so "reproduces the baseline" is a prediction here: sigma(0) < 0.15 and
public-law inference within 0.02 of C.

## 2. Why the correct-simulator policy should fail, and what an experimenter must do

P0 learns from public simulations, in which an injection acts at once, where it was put, and is washed out. In
the hidden world the carried share does nothing until it meets a cell, travels meanwhile, outlives the washout
and feeds whichever cells it reaches. Given the state, the public law is right without input and under blind
pushes and wrong under an aimed pulse (table 3a, last block). No public parameter delays or reroutes an
injection (reference S_wide tests that).

A defect on the response side is **not** enough by itself. For a carrier that converts everywhere, a
one-number-per-horizon gain on the public response, fitted to 16 Lab episodes, closes 0.83-0.84 of the
state-given gap (table 3b). With conversion at cells only, the correction depends on the configuration of cells
around the injection; the same recipes close about nothing and a fit that is told the form closes all of it.
That is the mechanism: three or four numbers in mechanism space, no small formula in observable space.

Passive episodes carry nothing (gap at the floor): without a strong injection X is about 0. Blind pushes land
where no cell is. An experimenter must:
1. *Detect.* One aimed pulse on a cell against a same-start episode without input: the focus cell's mass leaves
   the public prediction by 4-5 oracle SDs within 8 ticks.
2. *Dose.* The same nats in 2 ticks and in 20: the prompt share differs, which gives lam and a0.
3. *Place.* The pulse 0, 8, 16 px beside the cell, and into empty medium between two cells at unequal distances:
   what arrives, when, and at which cell gives D_X and the form (converted at cells, not washed out).
4. *Time.* The response after the pulse ends gives rho. With a rate wrong by a factor 4 a known form keeps half
   of the gap (0.19 of 0.37, linear carrier, `R/screen_pro_lam1_wrongrho_m12.json`).

Twelve 48-tick episodes at 300 nats and four controls fit the Lab budget of section 6.

## 3. Candidates and the screen

Screen (round 5's): from each hidden state, replicate futures of the hidden law (the oracle, leave one out)
against the public law run from the same state with the hidden field dropped; gap = (L(public) - L(O)) /
(L(K) - L(O)), fair energy score summed over 4, 8, 16, 32 ticks, by program class at equal nats (300): none
(passive), blind, aimed feed, aimed starve. `screen.py`, 64 px, 12 members, 6 futures; +- is the bootstrap SE over
members.

**Table 3a.** Focus view unless said. File: `R/screen_<run>.json`, key `screen.focus.<class>.screen_gap`.

TABLE3A

**Table 3b.** State-given check of generic repair (`gvh.py`): 16 Lab episodes (one future each) and 32 test items
with pulses from a broad family, focus view; share of the public-to-oracle gap closed. G1 = ridge on Lab residuals
with program features; G2, G3 = gains on the public response (per horizon; with duration, onset, offset); G4 = G3
plus G1; H = told the form, least squares on a 27-point grid of (lam, rho, D_X).

TABLE3B

**Chosen: the carrier converted at cells, with the saturating prompt route.** It is the only candidate that
leaves formation as it is at full dial, is silent without input and under blind input, is large under aimed
input, and is not repaired by the generic recipes of table 3b. The others: any hidden stock in the metabolism
decides whether cells form at all, and what survives (catalyst pool at 0.3) is wrong without any input;
dormancy is never reached (an aimed starve takes the cell's minimum substrate only from 0.11 to 0.02-0.04,
`R/probe_S.json`); the carrier that converts everywhere is repaired by a gain.
Limits: tiny size, one draw of hidden values per row, the state is given, four generic recipes of my own, and
H's truth lies on its grid.

## 4. Reference policies

| policy | script |
|---|---|
| K | climatology pool of the hidden world's no-input runs |
| O | the hidden law from the hidden state, leave one out over the replicate truths |
| C | the truth: the net family trained on the extended law (carrier form switch, lam, rho, D_X, a0 and the public parameters as conditioning), evaluated at the true values |
| P0 | no hypothesis, no experiment: the public-law net with parameters drawn from the prior; also unconditioned, trained equally long |
| D(N) | data only: the better of a net and a ridge on N exam-mix Lab episodes |
| S_pub(N), S_wide(N) | generic: round 5's scripted inference with the public law (4 hidden parameters; all 17 in a doubled box), then the public net at posterior draws |
| R(N) | generic: P0 plus a residual model on N Lab episodes (the gain and ridge forms of table 3b, strength by leave-one-episode-out) |
| F(N) | generic: P0's net fine-tuned on N Lab episodes, early stopping by leave-one-episode-out |
| H(N) | told the form, not the values: the 12 designed episodes of section 2 plus 4 controls, synthetic likelihood on focus-response curves with the extended simulator, then C's net at posterior draws; H_mix(N) = the same on exam-mix episodes |

One net family per view as in `round5/ladder`, two training seeds for every scored net.

## 5. Acceptance, declared now

G* is the best of the generic recipes {P0, D, S_pub, S_wide, R, F} at the Lab budget, chosen on half of the items
and scored on the other half. sigma_G = (L(G*) - L(C)) / (L(K) - L(C)); rho_G = (L(P0) - L(G*)) / (L(P0) - L(C));
rho_H likewise with H. The roadmap's sigma (null = the better of P0 and D) is reported beside them. L is pooled
over both views and the three horizons; intervals by cluster bootstrap over truths.

Gates at lam = 1 and a Lab budget of 16 episodes:
1. sigma_G >= 0.15, with the 90% interval above 0.05.
2. rho_G <= 0.7.
3. rho_H >= 0.7, and L(G*) - L(H) > 0 at z >= 3 over truths: a recipe that was given only the form solves it.
4. Actions still matter: C made blind to the program loses at least 0.10 of L(K) - L(C).

Gates at lam = 0: the three zero-point checks, and H within 0.02 of S_pub.

Reported, not gated: everything at lam 0.25 and 0.5, per view and class, at Lab budgets 4 and 64; H_mix (what the
designed experiments add); the generic recipes on H's designed episodes; a control arm, the carrier that converts
everywhere at lam = 1, where table 3b predicts rho_G > 0.7; the rank correlation of per-world screen gap with
per-world sigma_G, a prospective test of round 5's screen.

**Failure:** at lam = 1 a generic recipe recovers more than 0.7 of C's gain over P0, or sigma_G < 0.15. Then an
incomplete law of this kind does not make the exam test science at this Lab budget.

**Not concluded, whatever the outcome:** that agents do science here (H is told the form; finding it is what
only rollouts show); that no generic method beats my six; that C is a ceiling; anything about hidden levels in
the metabolism, about defects that passive data show, or about other worlds; that the thresholds carry over.

## 6. Sizes and cost (estimates)

| item | size |
|---|---|
| arms | lam = 0, 0.25, 0.5, 1 and the control arm: 5 |
| truths | 12 per arm, nested (the same hidden draws and keys in every arm; only the dial or the form differs): 60 hidden worlds |
| items | 64 per world (16 none, 16 blind, 32 aimed), 12 replicate truths; 768 per arm |
| Lab, per world | 96 episodes of 48 ticks: 16 exam-mix (the budget), 48 more for D(64), 16 designed, 16 passive; 300 nats per episode, 4,800 in all for an agent; 768 ticks |
| training sets | public prior 2,048 episodes; extended prior 4,096; inference designs 1,536 + 1,536 + 2,048 |
| seeds | two training seeds per net; a fresh 256-bit secret per job; pilot marker on every output |
| member-ticks | 91,456 per world (Lab 19,008; exam 35,200; climatology 12,672; state-given screen 24,576), 5.5 million; shared 2.2 million; 7.7 million in all (one full episode = 198 ticks) |
| GPU | 1,500-2,700 member-ticks/s assumed with the tracker on an A100 40GB (measured: 2,717 level 0 alone, 598 with field recording, `r5-bias2-007`), so $0.20-0.92 per million and $1.6-7.1 for simulation; nets about 1.5-2 h, $3-4; in all $5-11, cap $20; the job's first step measures the rate and sizes down by a declared rule; largest array 6e7 elements |
| research budget (decision 2) | 8,192 full level-0 episode equivalents (5.5 core-hours at 0.0123 CPU-s per member-tick); P0 uses 2,048, public-law inference 3,584, H 6,144 |
| prediction budget (decision 2) | 0.1 of fully simulating the question: no simulation at prediction time, at every dial setting |

## 7. Risks, cheapest tests, and what would change the program

| risk | cheapest test |
|---|---|
| a history-only predictor keeps little of a state-given gap (round 5: 4-14%), so sigma_G < 0.15 even at lam = 1 | stage 1 of the job: lam = 1 only, 4 truths, about $1; go on only if (L(P0) - L(C)) / (L(K) - L(C)) >= 0.10 |
| a fine-tuned net repairs what my four recipes could not | the same stage: F(16) and R(16) against H(16) |
| H fails without the state (chaotic futures, summary statistics; truth off the grid) | CPU, 64 px: synthetic likelihood on focus-response curves of 12 designed episodes |
| the population view dilutes a one-cell response at 128 px (gap 0.06 +- 0.03 against 0.33 +- 0.07 in the focus view, linear carrier, `R/screen_pro_lam1_128.json`) | decide before the job, from the 128-px screen, whether the population view is scored or only reported |
| the saturating route halves the defect (focus 0.17 against 0.30 without it) | CPU: a0 between 0.02 and 0.03 |
| the viable box of public parameters is narrow (hidden stocks at dial 0.2-0.3 already empty boxes) | CPU viability and headroom scan before the hidden set is fixed |
| too easy for an agent: one aimed pulse shows the lateness and the told sentence points to it | rollouts only; dial 0.25-0.5 and the hidden a0 make it subtler |
| tracker throughput on the GPU is not measured | the job's first step |

**What would change the program.** A pass at lam = 1 with the control arm failing gives the first exam design
that passes both bars on scripted policies, and a rule for building defects (the correction must depend on
configuration); it goes to rollouts. Generic repair winning in both arms says that measured defects of a
correct law do not make science pay at these budgets, and the weight moves to designs (c) and (d). sigma(0) >=
0.15 would say that this world's plain type-(a) exam already passes, which round 5 saw on neither of its worlds.
