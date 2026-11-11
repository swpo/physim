# Round 6, dials: the plan

11 Nov 2026, planner. Built from three designs (`defect_gliders`, `sublevel_second`, `compute_limit`) and three
critiques (`crit_adversary`, `crit_stats`, `crit_cost`) in this folder. I checked every number below against the
file named beside it and ran no simulation. "Estimate" marks what nobody measured. Every hidden value in these
folders is a pilot value, never to be reused as an exam.

Terms: K is climatology, O the true law run from the hidden state, C a net trained at the truth, P0 a net trained
on simulations of the public prior, D(N) a net trained on N Lab episodes alone (the no-simulator arm, design (d)).
A *generic recipe* repairs P0 from Lab data with no idea of what is wrong. L is a policy's pooled energy score;
lower is better.

## 1. Recommendation

| order | study | verdict | reason |
|---|---|---|---|
| 1 | **A. Gliders calibration**: stage 1 of `defect_gliders`, with a changed question | run now | It is cheap, uses round 5's harness, and measures with real nets what so far rests on a linear stand-in at 6 states: that a residual fitted to a few Lab episodes repairs an incomplete law. |
| 2 | **B. Membrane carrier**: `sublevel_second`, changed | CPU gate now; GPU only if the gate passes | It is the only design the adversary could not break at every horizon, but it holds at 32 ticks only and largely through one start state per seed, so a CPU gate comes before a 10-14 agent-hour build. |
| - | Stress conversion on gliders as an exam (stage 2 of `defect_gliders`) | drop | One Lab episode per program class closes 0.70-0.94 of its gap, so its bars 2 and 3 fail on the designer's own forecast. |
| - | Compute limit on fed vortices (`compute_limit`, both jobs) | defer | Summed small-box runs score as exam-size runs do (0.448 against 0.454), designer and adversary both expect failure, and the one risk the $5 job tests has an untried cheap answer (joining the vortex lists of small boxes). |

What I changed so that no recommended threshold is one the adversary's policy defeats:

- **A has no pass bar.** The adversary's policy is the designer's own residual, and it defeats the design. The job
  is kept as a measurement of that policy: its criteria say whether "generic repair wins" holds on nets. Whatever
  it finds, A cannot record an exam as passing.
- **B is gated where the adversary found it weak.** His policy and the designer's gains join the null. The bars
  must hold at 32 ticks alone and with the heaviest hidden world left out. The recipe told the form is fitted to
  hidden values off its grid. A CPU stage on fresh seeds must confirm this before anything is built.
- `compute_limit` leaves three things at no cost: the two compute numbers on every exam, the pooling defect
  (exam-size reference minus summed small boxes) on the world card, and summed boxes in any later null.

## 2. The studies

### A. Gliders calibration

**Exam.** Round 5's ladder exam, the cell with four hidden parameters (`round5/ladder`): an item is 16 input-free
ticks of the level-1 block view plus a held-out program from the public mix (none, blind, aimed 200 nats, regional
300 nats), and the answer is the block view 1 to 16 ticks ahead. The hidden world also turns channel 0 into
channel 1 wherever the wind exceeds a threshold, at eta x 0.09 per unit time (`defect_gliders/dlaw.py`, term XW;
threshold 0.12 and ramp 0.05, the pilot's values, in every truth). The agent is told: "the simulator may lack
mechanisms of the world; which, where and how strong is not said; there may be none."

**Dial and zero point.** eta = 0 and 4. At eta = 0 the hidden tick equals `gworld.tick` bit for bit
(`defect_gliders/results/check_zero.json` [bitwise_equal_to_gworld.traced_zero]).

| policy | what it is |
|---|---|
| K, O, P0, D(N) | as above |
| C | the true-form net at the truth, or that net fine-tuned on the Lab episodes: the better, picked on the half of the items that is not scored |
| S(N) | round 5's scripted inference of the four parameters with the public law |
| FT(N) | P0's net fine-tuned on N Lab mix episodes |
| RES(N) | **the adversary's policy**: P0 plus a per-block residual fitted on N Lab mix episodes |

N = 8 is primary; 2 and 32 are reported.

| criterion, declared now | number |
|---|---|
| zero point, at eta = 0 | round 5's sigma (0.018 +- 0.004) reproduced within 2 SE; and, paired per truth, the true-form C against the public-form C, and FT(8), RES(8) against P0, each within 0.02 of L(K) - L(C) |
| the defect reaches a net: s = (L(P0) - L(C)) / (L(K) - L(C)) on the aimed and regional classes, eta = 4 | the stand-in forecasts 0.20 (`defect_gliders/results/summary.json` [forecast_block_view_eta4]); it "holds" if 0.10 <= s <= 0.30 |
| generic repair: g = (L(P0) - L(G)) / (L(P0) - L(C)), G the better of FT(8) and RES(8), picked on the unscored half | **confirmed** if the one-sided 90% lower bound of g is >= 0.7; **refuted** if the upper bound is < 0.7; otherwise one extension to 16 truths |
| the study itself fails | the zero point misses, or s < 0.05 (nothing to repair); nothing else is then read |

| size | value |
|---|---|
| truths | the ladder's 8 pilot truths, each at eta 0 and 4 (the statistician's minimum) |
| per truth and eta | Lab of 32 mix and 32 input-free episodes; 96 items (24 per class) x 12 replicates |
| training | public and true-form families, 768 parameter points x 8 episodes each; 3 seeds per scored net |
| compute budgets told | research: 8,192 full episodes of 82 ticks (28-31 core-hours; P0 uses 6,144 to simulate and 476 to train). Prediction: 0.05 of simulating a question of 32 members x 16 ticks, which is 3.8 CPU-seconds per item |
| GPU job | one: 1.80 million member-ticks, A100 40 GB, 0.9-1.5 h, about $2-3 (estimate), cap $5 |
| build first | the law switch around `ladder_lib`; the true-form family; FT and RES on nets; a full-shape validation pass as the job's first step. 4-5 agent-hours (estimate) |
| sources | `crit_cost/results/recompute.json` [defect_gliders], [net_training_inside_the_research_budget]; round 5's sigma from the table of `round5/ladder/README.md`, row 4 hidden, block view |

### B. Membrane carrier

**Exam.** Phase-membrane cells at 128 px (`track1/membrane_world`): the agent observes the level-1 cell list; an
item is a 16-tick history plus a held-out program (none 1/8, blind 1/8, an aimed substrate pulse of 100-300 nats
3/4); the answer is the *focus view*, cell mass and catalyst mass within 16 px of the item's focus cell, at 8, 16
and 32 ticks. Hidden are parameters of the public law and a level under the substrate: a share lam of each strong
injection arrives as an inert carrier that diffuses and becomes substrate only where cell catalyst is
(`sublevel_second/sublevel.py`, candidate `pro`). The agent is told, at every dial setting: "Your simulator is
approximate: the real world holds state the public law lacks. Where, how, or whether at all is not stated."

**Dial and zero point.** lam = 0, 0.5, 0.75, 1. At lam = 0 fields, level 1 and level 2 equal the public world bit
for bit (`sublevel_second/results/check_zero.json` [candidates.pro.bit_for_bit]). The lam = 0 arm is also this
world's first plain exam of type (a).

**What the adversary found** (`crit_adversary/results/summary.json` [rows]; state given, 64 px, 16 Lab episodes).
His policy A_act runs the public law under a delayed, blurred copy of the command, four fitted numbers, knowing
nothing of the carrier. It closes 0.82-0.90 of the public-to-oracle gap at 8 ticks, 0.69-0.84 at 16, and 0.06 at
32, where the recipe told the form closes 0.91. Over the exam's three horizons it closes 0.33 and 0.36: the
pooled bar of 0.7 survives, through the 32-tick horizon alone. His files hold a fact his text does not state:
with the heaviest of the 6 to 8 start states left out, A_act closes 0.72 and 0.58 on its two seeds, and the
designer's gain 0.44-0.72 on three seeds of four (`crit_adversary/results/adv_s*.json`
[closed_without_heaviest_member], pooled over 4-32 ticks). On this evidence stage 0's rule is a close call.

**Forecast (estimate).** Given the state, the public law loses 0.27 of the climatology-to-oracle range over the
declared mix (`sublevel_second/results/screen_pro_cat_sat_lam1_128.json`, keys L_public, L_O, L_K, classes
weighted 1 : 1 : 3 : 3; the designer writes 0.28). If a history-only net keeps the 19-38% that the gliders
stand-in kept (`defect_gliders/results/surrogate.json` [kept_fraction]), P0 trails C by 0.05-0.10, below the 0.15
bar. That carry-over between worlds is weak evidence; stages 0 and 1 test it cheaply.

| stage | what runs | go rule |
|---|---|---|
| 0, CPU, about 5 CPU-hours (estimate) | state given, 64 px, 8 fresh seeds, main and control arm, per horizon, with the cell-resolved list as a second view; the told-form recipe with truths off its grid; a history-only stand-in as in A; the scans that fix the hidden parameter set and the ranges of rho, D_X, a0, committed with a hash | build only if, pooled over seeds and 8-32 ticks: the better of the gains and A_act, picked on the Lab episodes, closes <= 0.7 in the main arm, both with all start states and with each seed's heaviest left out, and >= 0.7 in the control arm; the told-form recipe closes >= 0.7; and, if A found its stand-in to hold, the stand-in's P0-to-C share is >= 0.10 |
| 1, GPU | lam = 1, 4 truths, both training families, 3 seeds; P0, C, F, R, A_act | stop if the one-sided 90% upper bound of (L(P0) - L(C)) / (L(K) - L(C)) is below 0.15 |
| 2, GPU | all arms, all policies | none |

| policy | what it is |
|---|---|
| K, O, P0, D(16), D(64) | as above |
| C | the extended-law net at the true values, or that net fine-tuned on the Lab episodes: the better, picked on the unscored half |
| S_pub, S_wide | round 5's scripted inference with the public law: the hidden parameters; all 17 in a doubled box |
| R | P0 plus a residual on the Lab episodes: gains on the public response, or a ridge on program features |
| A_act | **the adversary's policy** without the state: P0's net fed the filtered command, the four numbers fitted on the Lab episodes |
| F | P0's net fine-tuned on the Lab episodes |
| G* | the best of all the above except C, picked on half of the items and scored on the other half |
| H, H_mix | told the form, not the values: 12 designed episodes and 4 controls, then C's net at posterior draws; H_mix does the same from exam-mix episodes |

Criteria, declared now, at lam = 1 with a Lab of 16 episodes (48 ticks and 300 nats each), focus view, pooled over
8, 16 and 32 ticks:

| criterion | number |
|---|---|
| B1, science share | sigma_G = (L(G*) - L(C)) / (L(K) - L(C)) >= 0.15: the mean over truths of L(G*) - 0.85 L(C) - 0.15 L(K) has a one-sided 90% lower bound >= 0 |
| B2, generic share | rho_G = (L(P0) - L(G*)) / (L(P0) - L(C)) <= 0.7, tested the same way; read only if L(P0) - L(C) exceeds 2 SE |
| B3, solvable | H recovers >= 0.7 of P0-to-C and beats G* at t >= 3 over truths |
| B4, actions matter | C made blind to the program loses >= 0.10 of L(K) - L(C) |
| B5, not one horizon, not one world | B1 and B2 hold at the point estimate at 32 ticks alone, and with the heaviest truth left out; 8 and 16 ticks are reported (forecast: generic repair wins at 8) |
| B6, the recipes are competent | in the control arm, where the carrier converts everywhere, rho_G >= 0.7 at the point estimate |
| zero point, at lam = 0 | two truths run through the unchanged `membrane_world.build` score alike on every item; paired per truth, the extended-family C against the public-family C, and G*, H against P0 and S_pub, each within 0.02 of L(K) - L(C) |
| **pass** | B1 to B6 and the zero point |
| **fail** | the 90% upper bound of B1 or B2 lies on the wrong side of its bar, after at most one doubling of the truths |
| **undecided** | anything else; reported as undecided, never as a pass |
| standard errors, A and B | truths as clusters, plus the training-seed term (seed SD squared over 3) |
| training rule, A and B | a net counts as trained only if its best validation step falls in the first 80% of its schedule; otherwise the schedule doubles; all nets get equal steps |

| size | value |
|---|---|
| truths | 16 at lam 0, at lam 1 and in the control arm; 6 at lam 0.5 and 0.75; nested, the same hidden draws in every arm: 60 hidden worlds (the statistician's minimum) |
| per world | 64 items (8 none, 8 blind, 48 aimed) x 12 replicates; Lab of 96 episodes: 16 exam-mix (the budget), 48 more for D(64), 16 designed, 16 passive |
| training | public prior 2,048 episodes, extended prior 4,096, inference designs 5,120; 3 seeds per scored net; fine-tuning by 4-fold cross-validation over episodes (leave-one-out would be 10,440 trainings) |
| compute budgets told | research: 16,384 full episodes of 198 ticks (2.44 CPU-seconds each, 11 core-hours), training included; the designer's 8,192 covers H's 6,144 of simulation but not its net (about 2,400, estimate). Prediction: 0.25 of simulating a question of 32 members x 32 ticks, 3.1 CPU-seconds per item; the designer's 0.1 leaves 1.3, of which the grading box itself uses 1.0 |
| GPU jobs | stage 1: 1.58 million member-ticks, A100 40 GB, 0.9-1.5 h, $2-3, cap $4. Stage 2: 5.4 million, A100 40 GB, 2-3 h, $4-6, cap $10. Hours and dollars are my estimates from the cost critic's two-seed figures: simulation is under $1.5 at the measured 7,091 member-ticks/s, nets are the bill, and no membrane net exists yet |
| build first | stage 0; then the exam (hidden set, mix, focus view), a net family whose training programs include filtered commands, inference in 17 dimensions, R, F, A_act, H, H_mix, the control arm; a full-shape validation pass first in each job. 3-4 agent-hours for stage 0, then 10-14 (estimates) |
| sources | `crit_cost/results/recompute.json` [sublevel_second]; `crit_stats/results/se_check.json` [design_expectations]; stage sizes recomputed from the designer's per-world counts |

## 3. What each outcome would mean

| outcome | what it decides |
|---|---|
| A: generic repair confirmed, stand-in holds | Every later null includes fine-tuning and a residual. Three CPU screens go on the world card as the gate for any incomplete-law candidate: the state-given gap, the share a history-only family keeps, and the share a generic residual leaves. A defect that is a function of a public field under the exam's own programs is closed as an exam design. |
| A: confirmed, stand-in misses | The null changes as above, but CPU stand-ins are not a gate: B's stage 0 uses its state-given rules only. |
| A: refuted, with s >= 0.15 | Stress conversion is reopened: 16 truths and a recipe told the form (the designer's stage 2, about $4) before any pass is claimed. |
| A: zero point misses | A fault in the harness; nothing is read until it is found. |
| B: stage 0 fails | A filter on the command repairs the carrier except in rare start states. B is not built, at no GPU cost. With A confirmed, "extra term" defects are closed on two worlds; what stays open is a defect whose correction needs hidden state that only the history reveals. |
| B: stage 1 stops, or B1 fails with P0 close to C | The hidden level does not reach a history-only predictor; the state-given screen overstates again, as in round 5. |
| B: B2 fails in both arms | Measured defects do not make the exam test science at a 16-episode Lab; the question of section 5 goes to the lead. |
| B: passes | The first design to pass both bars against scripts, with a rule: the correction must depend on the configuration of cells. A pilot instance goes to rollouts, which alone say whether an agent can find the form. The claim is about 32 ticks. |
| B: main arm and control arm both resist generic repair | The recipes are too weak to serve as a null; no pass is recorded until they are strengthened. |
| B: sigma at lam = 0 is >= 0.15 | This world's plain type-(a) exam already passes, which round 5 saw on neither world; it goes to rollouts as it is. |

## 4. What these studies will not show

- Whether agents do science. Every policy is a script, and H is told the form of the defect; whether an agent
  finds the form, only rollouts show.
- That no generic method beats the listed ones. A pass is relative to P0, D, scripted inference, gains, the
  command filter and fine-tuning.
- That C is a ceiling; shares can exceed 1.
- Anything beyond 32 ticks, the focus view, a 16-episode Lab, or these two worlds; nothing about defects that
  passive data reveal.
- Whether the research budget binds on an agent: the port limits a predictor's CPU per item but does not meter
  the agent's research compute (`round6/vfport/README.md` section 4, item 5, through the cost critic).
- Anything about design (c) beyond level 2 of fed vortices, where the evidence has no hidden worlds.
- A sealed exam. The form of each defect is public in this repo; under design (b) the secret is code, which needs
  the private store of decision 5.

## 5. Cost, order of work, decisions

| item | GPU estimate | cap | agent-hours (estimate) |
|---|---|---|---|
| A | $2-3 | $5 | 4-5 |
| B, stage 0 | none | none | 3-4 |
| B, stage 1 | $2-3 | $4 | 10-14 for the whole build |
| B, stage 2 | $4-6 | $10 | |
| total | $8-12 | $19 | 17-23 |

Billed so far: $46.27 of the approved $1,000 (`../../README.md`, round 5). No model call. If B stops at stage 0,
the round costs about $3 and 8 agent-hours.

Order of work:
1. Now, in parallel: build A; run B's stage 0 on CPU.
2. A's job.
3. Read A and stage 0 together; build B only if stage 0 passes.
4. B's stage 1 job; if it does not stop, B's stage 2 job.
5. A checker recomputes each study before its result is quoted.

**What the lead must decide: nothing before work starts.** Every job is below the $25 that starts without asking.
Two choices of mine the lead may wish to overrule: for designs of type (b) the science share is measured against
the best generic recipe, with the roadmap's sigma reported beside it; and (c) is deferred, not run as a $5
confirmation of a failure its designer and the adversary both expect.

One decision comes later, and only if B fails: the designs disagree on where the weight then goes.
`sublevel_second` says to (c) and (d). `compute_limit` says (c) has no window on fed vortices: it needs a new
world whose card shows a pooling defect of at least 0.15, and a third declared number beside decision 2's two,
the largest box the agent may run.
