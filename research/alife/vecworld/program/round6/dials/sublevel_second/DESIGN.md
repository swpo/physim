# Study (b) on a second world: a hidden carrier level under the phase-membrane cells

Round 6, dials, designer `sublevel_second`, 11 Nov 2026. Design only: no GPU job, no model call. Numbers in
sections 0-3 were run here on CPU at tiny size and name their file (`R/` = `results/`); sections 5-7 are
declarations and estimates. Hidden values in this folder are pilot values, **never to be reused as an exam**.

## 0. The world: phase-membrane cells

| world | cost | do inputs move the observed level | a level below the public law | verdict |
|---|---|---|---|---|
| fed vortices | 169-444 member-ticks/s, $3.3-4.5 per million (`round5/vortexexam` README 1; checker 10) | yes | below the level-2 law lies level 0 itself: a dial without a zero point; with 6-10 truths sigma carried errors of 0.05-0.16 (README 4, 5) | loses: the dial cannot be resolved at this price |
| foundry automaton | 74,700 member-ticks/s (`round5/foundry` README) | no: an aimed 200-nat command moves the block view by 0.0002-0.023 of its variance; "whether actions matter is not established" (checker) | the weights are the law: no form to tell H | loses: an experimenter has nothing to do |
| membrane cells | 0.0123 CPU-s per member-tick, 13 times cheaper than gliders' 0.164 (`track1/membrane_world` summary `timing`; `round5/agentenv` summary `cost`); level 0 alone 2,717 member-ticks/s on an A100 40GB (`round5/bias2/results/membrane_w/sim_A.json`) | locally yes: at 128 px an oracle blind to an aimed 300-nat program loses 0.69-0.74 of the range in the focus view of section 1, 0.08-0.14 in the population view (`R/screen_public_128.json`) | chemistry: an intermediate species the public law has eliminated | chosen |

## 1. The exam

**World.** Membrane cells, 128 x 128 px, tick = 10 time units, 150 ticks of formation inside the reset (one label
gives one formed state, fresh noise each time). **Observed:** level 1, the cell list. **Scored** at 8, 16 and 32
ticks after a 16-tick history, under a held-out program: the *focus view* of level 1 (cell mass and catalyst mass
within 16 px of the item's public focus point, the largest cell of the last history frame). The population pair
of level 2 is reported, not pooled. Mix: none 1/8, blind 1/8, aimed pulse 3/4 (sign, 2-20 ticks, onset 0-8,
centre 0-16 px off the focus, 100-300 nats).

**Public:** the law (`membrane_jax.py`), coarse-grainings, channel, priors, mix, scales. **Hidden:** (i) parameters
of the public law, as in round 5 (set fixed by a pre-job viability scan); (ii) a level under the substrate
field. Of each realised channel coefficient c = u + eta the share lam c^2 / (c^2 + a0^2) arrives as a *carrier*
X, inert in the medium: it diffuses (D_X), is neither eaten nor washed out, and becomes substrate only where cell
catalyst is (rate rho K / 0.25). The rest arrives at once; the public law is the limit of instant conversion.
rho, D_X, a0 are hidden per world (pilot centre 0.02, 0.5, 0.03). Everything still enters through u + eta, so the
nats charge stays exact (`sublevel.py`, candidate `pro`).

**Told:** "Your simulator is approximate: the real world holds state the public law lacks. Where, how, or whether
at all is not stated." The same words at every dial setting.

**Dial:** lam in {0, 0.5, 0.75, 1}, measured by the screen of section 3. **Zero point:** at lam = 0 nothing is
carried. Three checks. (1) `check_zero.py`: fields, level 1 and level 2 equal the public world's bit for bit
(`R/check_zero.json`, `candidates.pro`). (2) In the job, two lam = 0 truths also run through
`membrane_world.build` unchanged and must score alike on every item. (3) The lam = 0 arm is round 5's design
(correct law, hidden parameters, same harness, policies, `acceptance.py`). No round-5 exam exists on this world,
so the baseline is a prediction: sigma(0) < 0.15, public-law inference within 0.02 of C.

## 2. Why the correct-simulator policy should fail, and what an experimenter must do

P0 learns from public simulations, in which an injection acts at once, where it was put, and is washed out. In
the hidden world the carried share does nothing until it meets a cell, travels meanwhile, outlives the washout
and feeds whichever cells it reaches. Given the state, the public law is right without input and under blind
pushes, and wrong under an aimed pulse (table 3a, bold rows). No public parameter delays or reroutes an
injection (S_wide tests it).

A defect on the response side is **not** enough. For a carrier that converts everywhere, one gain per horizon on
the public response, fitted to 16 Lab episodes, closes 0.77-0.84 of the state-given gap (table 3b). With
conversion at cells only, the correction depends on the configuration of cells around the injection: the same
recipes close 0.10-0.34, a fit told the form 0.77-1.02. Four numbers in mechanism space, no small formula in
observable space: that is the mechanism.

Passive episodes carry nothing: without a strong injection X is about 0. Blind pushes land where no cell is. An
experimenter must:
1. *Detect.* One aimed pulse on a cell against a same-start episode without input: at 8 ticks the focus cell's
   mass is 4.7-5.4 oracle SDs off the public prediction (`R/screen_pro_cat_sat_lam1_m12.json`,
   `shift_truth_minus_public`).
2. *Dose.* The same nats in 2 ticks and in 20: the prompt share differs, which gives lam and a0.
3. *Place.* The pulse 0, 8, 16 px beside the cell, and into empty medium between two cells at unequal distances:
   what arrives, when, and at which cell gives D_X and the form.
4. *Time.* The response after the pulse ends gives rho. Values matter: with the rate wrong by a factor 4 the
   known form keeps 0.12 of the 0.17 gap (`R/screen_pro_cat_sat_lam1_wrongrho_m12.json`).

Twelve such episodes and four controls fit the Lab budget (section 6).

## 3. Candidates and the screen

Screen (round 5's): from each hidden state, replicate futures of the hidden law (the oracle, leave one out)
against the public law run from the same state with the hidden field dropped; gap = (L(public) - L(O)) /
(L(K) - L(O)), fair energy score summed over 4, 8, 16, 32 ticks, by program class at equal nats (300). Classes
(the passive-against-designed comparison): none, blind, aimed feed, aimed starve. `screen.py`; 64 px, 12 members,
6 futures unless said; ± = bootstrap SE over members.

**Table 3a.** Focus view; last column population view. `R/screen_<run>.json`, `screen.<view>.<class>.screen_gap`.

| candidate (run) | dial | boxes without cells | none | blind | aimed feed | aimed starve | population, input items |
|---|---|---|---|---|---|---|---|
| the public law itself: noise floor (`public_m12`) | 0 | 1 of 12 | -0.001 ± 0.004 | -0.001 ± 0.003 | -0.001 ± 0.002 | 0.004 ± 0.006 | -0.000 ± 0.002 |
| dormant catalyst, dormancy below substrate 0.09 (`dorm_sc0.09_m12`) | 1 | 1 of 12 | -0.001 ± 0.004 | -0.001 ± 0.003 | -0.000 ± 0.002 | 0.014 ± 0.007 | 0.001 ± 0.002 |
| catalyst precursor pool (`kpool_lam0.3_m12`) | 0.3 | 0 of 12 | 0.183 ± 0.051 | 0.132 ± 0.041 | 0.249 ± 0.062 | 0.036 ± 0.011 | 0.087 ± 0.023 |
| lipid precursor pool (`lpool_lam0.3_m12`) | 0.3 | 7 of 12 | 0.107 ± 0.024 | 0.102 ± 0.023 | 0.100 ± 0.021 | 0.100 ± 0.026 | 0.104 ± 0.023 |
| substrate bound to the medium (`bound_lam0.2_m12`) | 0.2 | 10 of 12 | 0.036 ± 0.017 | 0.029 ± 0.010 | 0.035 ± 0.012 | 0.064 ± 0.023 | 0.037 ± 0.012 |
| carrier, converts everywhere (`pro_lam0.5_m12`) | 0.5 | 2 of 12 | -0.001 ± 0.003 | 0.008 ± 0.004 | 0.140 ± 0.051 | 0.246 ± 0.089 | 0.039 ± 0.013 |
| the same (`pro_lam1_m12`) | 1 | 2 of 12 | 0.022 ± 0.020 | 0.029 ± 0.015 | 0.371 ± 0.145 | 0.716 ± 0.274 | 0.108 ± 0.040 |
| carrier, converted at cells, no saturation (`pro_cat_lam1_m12`) | 1 | 2 of 12 | 0.085 ± 0.040 | 0.108 ± 0.044 | 0.416 ± 0.119 | 0.363 ± 0.117 | 0.125 ± 0.041 |
| **carrier, converted at cells, saturating route, a0 = 0.03** (`pro_cat_sat_lam0.25_m12`) | 0.25 | 1 of 12 | -0.003 ± 0.003 | -0.001 ± 0.003 | 0.013 ± 0.007 | 0.020 ± 0.014 | 0.002 ± 0.003 |
| **the same** (`pro_cat_sat_lam0.5_m12`) | 0.5 | 1 of 12 | -0.003 ± 0.003 | -0.001 ± 0.004 | 0.059 ± 0.024 | 0.068 ± 0.029 | 0.008 ± 0.004 |
| **the same** (`pro_cat_sat_lam0.75_m12`) | 0.75 | 1 of 12 | -0.001 ± 0.003 | 0.002 ± 0.004 | 0.170 ± 0.080 | 0.129 ± 0.050 | 0.019 ± 0.009 |
| **the same** (`pro_cat_sat_lam1_m12`) | 1 | 1 of 12 | 0.005 ± 0.006 | 0.010 ± 0.008 | 0.266 ± 0.108 | 0.197 ± 0.074 | 0.032 ± 0.015 |
| the same with a0 = 0.02 (`pro_cat_sat0.02_lam1_m12`) | 1 | 1 of 12 | 0.079 ± 0.071 | 0.090 ± 0.073 | 0.367 ± 0.139 | 0.260 ± 0.089 | 0.067 ± 0.035 |
| floor at 128 px, 6 members (`public_128`) | 0 | 0 of 6 | 0.003 ± 0.006 | 0.005 ± 0.005 | -0.002 ± 0.004 | -0.002 ± 0.004 | -0.008 ± 0.006 |
| **the chosen carrier** at 128 px, 6 members (`pro_cat_sat_lam1_128`) | 1 | 0 of 6 | 0.013 ± 0.011 | 0.050 ± 0.037 | 0.445 ± 0.095 | 0.208 ± 0.075 | 0.015 ± 0.011 |

At dial 1 the catalyst pool forms no cells (8 of 8 boxes); lipid pool and bound substrate fill the box with
inside phase (`R/screen_{kpool,lpool,bound}_lam1.json`, `state_at_T0`).

**Table 3b.** Generic repair, state given (`gvh.py`): 16 Lab episodes (one future each), 32 test items, focus
view, 64 px, lam = 1; share of the public-to-oracle gap closed.

| carrier (pilot rho, D_X; seed) | file `R/gvh_...` | ignores the program | G1: ridge on Lab residuals with program features | better of G2, G3: gains on the public response (per horizon; with duration, onset, offset) | G4 = G3 + G1 | H: told the form, least squares on a 27-point grid | H's fit (lam, rho, D_X) |
|---|---|---|---|---|---|---|---|
| converts everywhere (0.005, 0.2; 5) | `lam1_n16_s5.json` | 0.64 ± 0.03 | 0.37 ± 0.07 | 0.84 ± 0.02 | 0.84 ± 0.02 | 1.00 ± 0.00 | 1, 0.005, 0.2 |
| converts everywhere (0.02, 0.5; 5) | `lam1_n16_s5_rho0.02_DX0.5.json` | -0.42 ± 0.22 | 0.35 ± 0.11 | 0.77 ± 0.02 | 0.71 ± 0.02 | 1.00 ± 0.01 | 1, 0.02, 0.5 |
| converted at cells, no saturation (0.02, 0.5; 5) | `lam1_n16_s5_cat1_rho0.02_DX0.5.json` | -0.11 ± 0.08 | -0.97 ± 0.82 | 0.02 ± 0.08 | -1.13 ± 0.98 | 1.00 ± 0.01 | 1, 0.02, 0.5 |
| **chosen** (0.02, 0.5; 5) | `lam1_n16_s5_cat1_rho0.02_DX0.5_a00.03.json` | -0.82 ± 0.54 | -0.27 ± 0.49 | 0.10 ± 0.16 | -1.01 ± 1.25 | 1.02 ± 0.02 | 1, 0.02, 0.5 |
| **chosen** (0.02, 0.5; 6) | `lam1_n16_s6_cat1_rho0.02_DX0.5_a00.03.json` | -1.45 ± 0.28 | 0.11 ± 0.08 | 0.34 ± 0.10 | -0.15 ± 0.15 | 0.77 ± 0.08 | 0.5, 0.02, 0.5 |

**Chosen: the carrier converted at cells, with the saturating prompt route.** It alone leaves formation as it
is at full dial, is silent without input and under blind input, large under aimed input, and not repaired by the
generic recipes. The others: a hidden stock in the metabolism decides whether cells form at all, and the catalyst
pool at 0.3 is wrong without any input; dormancy is hardly reached (an aimed starve takes the cell's minimum
substrate only from 0.11 to 0.02-0.04, `R/probe_S.json`); without saturation the carried channel noise lifts the
passive gap off the floor; the carrier that converts everywhere is repaired by a gain.
Limits: tiny size, one draw of hidden values, state given, my own four generic recipes, H's truth on its grid
with a0 known; in seed 6 H settles on lam = 0.5 for a truth of 1.

## 4. Reference policies

| policy | script |
|---|---|
| K | climatology pool of the hidden world's no-input runs |
| O | the hidden law from the hidden state, leave one out over the replicate truths |
| C | the truth: the net family trained on the extended law (form switch, lam, rho, D_X, a0 and the public parameters as conditioning), evaluated at the true values |
| P0 | no hypothesis, no experiment: the public-law net with parameters drawn from the prior; also unconditioned, trained equally long |
| D(N) | data only: the better of a net and a ridge on N exam-mix Lab episodes |
| S_pub(N), S_wide(N) | generic: round 5's scripted inference with the public law (the hidden parameters; all 17 in a doubled box), then the public net at posterior draws |
| R(N) | generic: P0 plus a residual model on N Lab episodes (the gain and ridge forms of table 3b, strength by leave-one-episode-out) |
| F(N) | generic: P0's net fine-tuned on N Lab episodes, early stopping by leave-one-episode-out |
| H(N) | told the form, not the values: the 12 designed episodes of section 2 and 4 controls, synthetic likelihood on focus-response curves with the extended simulator, then C's net at posterior draws; H_mix(N) = the same on exam-mix episodes |
| nets | one family as in `round5/ladder`; two training seeds for every scored net |

## 5. Acceptance, declared now

G* is the best generic recipe of {P0, D, S_pub, S_wide, R, F} at the Lab budget, chosen on half of the items and
scored on the other half. sigma_G = (L(G*) - L(C)) / (L(K) - L(C)); rho_G = (L(P0) - L(G*)) / (L(P0) - L(C));
rho_H likewise with H. L is pooled over the focus view's three horizons; intervals by cluster bootstrap over
truths.

Gates at lam = 1 and a Lab budget of 16 episodes:
1. sigma_G >= 0.15, with the 90% interval above 0.05.
2. rho_G <= 0.7.
3. rho_H >= 0.7, and L(G*) - L(H) > 0 at z >= 3 over truths: a recipe given only the form solves it.
4. Actions still matter: C made blind to the program loses at least 0.10 of L(K) - L(C).

Gates at lam = 0: the three zero-point checks, and H within 0.02 of S_pub.

Reported, not gated: the roadmap's sigma (null = better of P0 and D); lam 0.5 and 0.75; program classes; the
population view; Lab budgets 4 and 64; H_mix (what the designed experiments add); the generic recipes on H's
episodes; a control arm (the carrier that converts everywhere, lam = 1), where table 3b predicts rho_G > 0.7;
per-world screen gap against sigma_G, a prospective test of round 5's screen.

**Failure:** at lam = 1 a generic recipe recovers more than 0.7 of C's gain over P0, or sigma_G < 0.15: an
incomplete law of this kind does not then make the exam test science at this Lab budget.

**Not concluded, whatever the outcome:** that agents do science here (H is told the form; finding it is what
only rollouts show); that no generic method beats my six; that C is a ceiling; anything about hidden levels in
the metabolism, defects passive data show, or other worlds.

## 6. Sizes and cost (estimates)

| item | size |
|---|---|
| arms | lam = 0, 0.5, 0.75, 1 and the control arm: 5 |
| truths | 12 per arm, nested (the same hidden draws and keys in every arm; only the dial or the form differs): 60 hidden worlds |
| items | 64 per world (8 none, 8 blind, 48 aimed), 12 replicate truths; 768 per arm |
| Lab, per world | 96 episodes of 48 ticks: 16 exam-mix (the budget), 48 more for D(64), 16 designed, 16 passive. For an agent: 16 episodes, 768 ticks, 300 nats per episode, 4,800 in all |
| training sets | public prior 2,048 episodes; extended prior 4,096; inference designs 1,536 + 1,536 + 2,048 |
| seeds | two training seeds per net; a fresh 256-bit secret per job; the pilot marker on every output |
| member-ticks | one full episode = 198 ticks. Per world 91,456 (Lab 19,008; exam 35,200; climatology 12,672; state-given screen 24,576): 5.5 million; shared 2.2 million; 7.7 million in all |
| GPU | A100 40GB at $1.99/h. Measured: 2,717 member-ticks/s for level 0 alone, 598 with field recording (`r5-bias2-007`); the tracker's GPU cost is not measured. Between those rates $0.20-0.92 per million, $1.6-7.1 for simulation; nets about 1.5-2 h, $3-4; in all $5-11, cap $20. The job's first step measures the rate and sizes down by a declared rule. Largest array 6e7 elements |
| research budget (decision 2) | 8,192 full level-0 episode equivalents (5.5 core-hours at 0.0123 CPU-s per member-tick); P0 uses 2,048, public-law inference 3,584, H 6,144 |
| prediction budget (decision 2) | 0.1 of fully simulating the question: no simulation at prediction time, at every dial setting |

## 7. Risks, cheapest tests, and what would change the program

| risk | cheapest test |
|---|---|
| a history-only predictor keeps little of a state-given gap (round 5: 0.5-14% of the parameters' worth). Here the state-given gap on aimed items is 0.21-0.45 at 128 px and 0.28 over the declared mix (classes weighted 1 : 1 : 3 : 3 in `R/screen_pro_cat_sat_lam1_128.json`, keys `L_public`, `L_O`, `L_K`), so gate 1 needs C to keep more than half of it | stage 1 of the job: lam = 1 only, 4 truths, about $1; go on only if (L(P0) - L(C)) / (L(K) - L(C)) >= 0.10 |
| a fine-tuned net repairs what my four recipes could not | the same stage: F(16) and R(16) against H(16) |
| H fails without the state (chaotic futures, summary statistics, lam against a0) | CPU, 64 px: synthetic likelihood on focus-response curves of the 12 designed episodes, truth off the grid |
| the defect is steep in the dial (aimed gap 0.06, 0.15, 0.23 at 0.5, 0.75, 1) and capped by the saturation scale: a0 = 0.02 gives 0.31 but the passive gap leaves the floor (0.08 ± 0.07) | CPU: a0 between 0.02 and 0.03 with more members, before the ranges of rho, D_X, a0 are fixed |
| the viable box of public parameters is narrow (hidden stocks at dial 0.2-0.3 already empty 7 and 10 of 12 boxes) | CPU viability and headroom scan before the hidden set is fixed |
| too easy for an agent: one aimed pulse shows the lateness, and the told sentence points to it | rollouts only; the dose and placement steps are what the form needs |
| tracker throughput on the GPU is not measured | the job's first step |

**What would change the program.** A pass at lam = 1 with the control arm failing: the first design to pass both
bars on scripted policies, and a rule for defects (the correction must depend on configuration); it goes to
rollouts. Generic repair winning in both arms: measured defects do not make science pay at these budgets; the
weight moves to (c) and (d). sigma(0) >= 0.15: this world's plain type-(a) exam already passes, which round 5 saw
on neither world.
