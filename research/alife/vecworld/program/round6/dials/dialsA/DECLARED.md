# Study A, gliders calibration: what is declared before any run

11 Nov 2026, 15:35 UTC. Written and committed before any job request and before any decisive run. Part 1 is
copied from `../PLAN.md` (section 2, "A. Gliders calibration", and the rows of its later tables that name A);
nothing in it is mine and nothing in it may change. Part 2 fixes, also before any result, what the plan leaves
open. If something proves impossible, the nearest thing is done and written in `DEVIATIONS.md` at the time;
this file is not edited after its first commit.

PILOT ONLY: the truths are round 5's public pilot truths; every hidden value here is public and none may ever
be reused as an exam.

## Part 1. From the plan (binding)

**Status.** A has no pass bar. Whatever it finds, it cannot record an exam as passing. Its criteria say whether
"generic repair wins" holds on nets (confirmed, refuted or undecided), whether the defect reaches a net (s), and
whether the zero point holds.

**Exam.** Round 5's ladder exam, the cell with four hidden parameters (`../../../round5/ladder`): an item is 16
input-free ticks of the level-1 block view plus a held-out program from the public mix (none, blind, aimed 200
nats, regional 300 nats), and the answer is the block view 1 to 16 ticks ahead. The hidden world also turns
channel 0 into channel 1 wherever the wind exceeds a threshold, at up to eta x 0.09 per unit time
(`../defect_gliders/dlaw.py`, term XW; threshold 0.12 and ramp 0.05, the pilot's values, in every truth). The
agent is told: "the simulator may lack mechanisms of the world; which, where and how strong is not said; there
may be none."

**Dial and zero point.** eta = 0 and 4. At eta = 0 the hidden tick equals `gworld.tick` bit for bit.

| policy | what it is |
|---|---|
| K | climatology |
| O | the true law run from the hidden state |
| P0 | a net trained on simulations of the public prior |
| D(N) | a net trained on N Lab episodes alone |
| C | the true-form net at the truth, or that net fine-tuned on the Lab episodes: the better, picked on the half of the items that is not scored |
| S(N) | round 5's scripted inference of the four parameters with the public law |
| FT(N) | P0's net fine-tuned on N Lab mix episodes; N = 8 is primary for every policy, 2 and 32 are reported |
| RES(N) | the adversary's policy: P0 plus a per-block residual fitted on N Lab mix episodes |

L is a policy's pooled energy score; lower is better.

| criterion | number |
|---|---|
| zero point, at eta = 0 | round 5's sigma (0.018 +- 0.004) reproduced within 2 SE; and, paired per truth, the true-form C against the public-form C, and FT(8), RES(8) against P0, each within 0.02 of L(K) - L(C) |
| the defect reaches a net: s = (L(P0) - L(C)) / (L(K) - L(C)) on the aimed and regional classes, eta = 4 | the stand-in forecasts 0.20; it "holds" if 0.10 <= s <= 0.30 |
| generic repair: g = (L(P0) - L(G)) / (L(P0) - L(C)), G the better of FT(8) and RES(8), picked on the unscored half | **confirmed** if the one-sided 90% lower bound of g is >= 0.7; **refuted** if the upper bound is < 0.7; otherwise one extension to 16 truths. Tested as a per-truth contrast, and read only if L(P0) - L(C) exceeds 2 SE |
| the study itself fails | the zero point misses, or s < 0.05 (nothing to repair); nothing else is then read |
| standard errors | truths as clusters, plus the training-seed term (seed SD squared over 3); the median and the leave-one-truth-out range beside every mean |
| training rule | a net counts as trained only if its best validation step falls in the first 80% of its schedule; otherwise the schedule doubles; all nets get equal steps |

| size | value |
|---|---|
| truths | the ladder's 8 pilot truths, each at eta 0 and 4. Threshold and ramp are fixed |
| per truth and eta | Lab of 32 mix and 32 input-free episodes; 96 items (24 per class) x 12 replicates |
| training | public and true-form families, 768 parameter points x 8 episodes each; 3 seeds per scored net |
| compute budgets told | research: 8,192 full episodes of 82 ticks (28-31 core-hours; P0 uses 6,144 to simulate and 476 to train). Prediction: 0.05 of simulating a question of 32 members x 16 ticks, which is 3.8 CPU-seconds per item |
| GPU job | one: 1.80 million member-ticks, A100 40 GB, 0.9-1.5 h, about $2-3 (estimate), cap $5 |
| extension | only if the rule for g comes out undecided: one, to 16 truths, about $1, cap $3. Study total cap $8 |
| build first | the law switch around `ladder_lib`; the true-form family; FT and RES on nets; a full-shape validation pass as the job's first step |

What each outcome would mean (plan, section 3):

| outcome | what it decides |
|---|---|
| confirmed, stand-in holds | Every later null includes fine-tuning and a residual. Three CPU screens go on the world card as the gate for any incomplete-law candidate. A defect that is a function of a public field under the exam's own programs is closed as an exam design. |
| confirmed, stand-in misses | The null changes as above, but CPU stand-ins are not a gate: B's stage 0 uses its state-given rules only. |
| refuted | With s >= 0.15, stress conversion is reopened: 16 truths and a recipe told the form before any pass is claimed. With s below 0.15 it stays closed, for lack of effect. |
| zero point misses | A fault in the harness; nothing is read until it is found. |

## Part 2. Fixed here, before any result, where the plan is silent

**R1. Score.** Horizons 1, 2, 4, 8, 16 ticks (round 5's cells). L = mean over items of the fair energy score
summed over the five horizons (`round5/agentenv/evaluator/acceptance.py`), scored by the exam's own scorer.

**R2. Items and halves.** Per truth and eta two exams of round 5's shape, each 48 items (12 per class), 12
replicates, a climatology pool of 48: `sel`, the half that is not scored (every pick is made on it and on
nothing else), and `score` (every L and every criterion). Together 96 items, 24 per class, 96 climatology runs.

**R3. Seeds.** Three complete sets of nets, seeds 0, 1, 2: the public-form net, the true-form net and every net
derived from them (fine-tunes, D). L of a truth is the mean over the three seeds. Picks are made per truth and
seed.

**R4. Standard errors and bounds.** For a per-truth contrast c_t (seed-averaged): SE^2 = SD_t(c)^2 / n_truths
+ SD_s(c_bar_s)^2 / 3, where c_bar_s is the mean over truths of the contrast of seed s. One-sided 90% bounds
are mean -+ t(0.90, n_truths - 1) x SE (1.415 at 8 truths, 1.341 at 16). A ratio is the ratio of the means over
truths; its SE comes from the linearised contrast a_t - r b_t divided by the mean of b. Beside every mean: the
median over truths and the leave-one-truth-out range.

**R5. Families.** Public family: 768 points theta from the public box (the round-3 prior of the four
parameters), 8 mix episodes each (2 per class), simulated with round 5's code unchanged. True-form family: 768
points (theta, eta), theta from the same box with other seeds, eta = 0 at 384 points and 4 at 384 (a fixed
random assignment), 8 mix episodes each, simulated with `dlaw.tick`; threshold and ramp are the constants of
`dlaw.py`. One net family (round 5's block-view net). The true-form net is conditioned on (theta, eta / 4), the
public-form net on theta. The 8 truths and the fitted viability prior are read from round 5's files
(`round5/ladder/results/job/n4/truths.json`, `prior.json`); nothing is redrawn or refitted.

**R6. P0, public-form C, true-form C.** P0 is the public-form net with theta drawn per sample from the public
prior, and the public-form C is that net at the true theta (both as in round 5). The true-form C at eta = 0 is
the true-form net at (true theta, 0).

**R7. C at eta = 4.** Per truth and seed, the better on `sel` of (a) the true-form net at (true theta, 1) and
(b) that net fine-tuned on the same first N Lab mix episodes by FT's recipe, its conditioning held at the
truth. s and the primary g use N = 8; g at N = 2 and 32 is reported with the C of the same N.

**R8. FT(N).** Start from the public-form net of the same seed. Data: the first N Lab mix episodes, all anchors
and horizons as in base training. Conditioning: theta drawn from the public prior per example (as P0
predicts). AdamW as in base training with a fresh state, constant learning rate 1e-4 (the final rate of the
base schedule), batch 64 with 4 noise draws, schedule 400 steps. Steps are chosen by cross-validation over
episodes, min(4, N) folds, on a grid of 40 steps that includes 0 (no change); then the net is fine-tuned on all
N episodes for the chosen number of steps.

**R9. RES(N).** The designer's residual (`../defect_gliders/surrogate.py`, `res_scores`) on nets. For each of
the first N Lab mix episodes, P0's predictive mean (32 samples) at the exam's anchor (after the 16 input-free
ticks) for each horizon. Per program class (none, blind, aimed, regional; recognised from the program's
structure, which the public mix fixes), per horizon and per region class (blocks under an input at any tick,
their 8 neighbours, the rest): a ridge (0.05 x rows) from a block's three scaled numbers at the anchor and 1
to the residual of its three numbers. On an item the fitted correction of its program class is added to every
P0 sample; the spread is P0's. A class with no Lab episode among the N gets no correction.

**R10. G.** Per truth and seed the better of FT(8) and RES(8) on `sel`; scored on `score`.

**R11. S(N), D(N).** S(N): round 5's inference for the block view and the mix arm (projection and emulator
from the public family's episodes, importance sampling under round 5's viability prior), then the public-form
net at posterior draws. D(N): round 5's unconditioned net on the first N Lab mix episodes (3 seeds, 1,200
steps) or round 5's block ridge on them, the better on `sel` per truth and seed.

**R12. Lab.** Per truth and eta 32 mix episodes (consecutive blocks of four hold one episode of each class in
random order, so the first 8 and the first 32 have equal class counts) and 32 input-free episodes; 33 charged
ticks each; nats caps 100 per tick and 400 per episode.

**R13. Zero point, at eta = 0, on `score`, all four classes.** (i) sigma_0 = (L(null) - L(C)) / (L(K) - L(C))
with C the public-form C and null the better of P0 and D(32) (acceptance.py's rule; 32 is round 5's column):
|sigma_0 - 0.018| <= 2 x sqrt(0.004^2 + SE_0^2). The stricter |sigma_0 - 0.018| <= 0.008 is reported beside it.
(ii) |mean_t (L(X) - L(Y))| / mean_t (L(K) - L(public-form C)) <= 0.02 for (X, Y) = (true-form C, public-form C),
(FT(8), P0), (RES(8), P0); point estimates, SE reported. The zero point holds if (i) and the three of (ii) hold;
otherwise it misses.

**R14. s.** eta = 4, `score`, the aimed and regional items, C of R7 at N = 8, ratio of means over truths; point
estimate against 0.10, 0.30 and 0.05; SE and bounds reported. Also reported, not criteria: s on all four
classes, and s with the true-form net alone.

**R15. g.** eta = 4, `score`. Primary: all four classes, the exam as it is sat (the plan restricts s to
classes, not g; the roadmap's shares are defined on the whole exam). d_t = [L_t(P0) - L_t(G)] - 0.7 [L_t(P0)
- L_t(C)]: confirmed if mean - t x SE >= 0, refuted if mean + t x SE < 0, otherwise undecided. g is read only
if mean_t [L_t(P0) - L_t(C)] > 2 SE; not read counts as undecided. Reported beside it as secondary, same rule:
g on the aimed and regional items. The verdict of the study is the primary's.

**R16. Training rule, as built.** Base nets: round 5's trainer and cosine schedule, first 6,000 steps (round
5's length); the rule is checked on all six base nets; if any misses, all six are retrained from scratch at
twice the length; at most two doublings (24,000 steps): P0 then costs 6,144 episodes of simulation plus 1,904
episode equivalents of training (476 per 6,000 steps, `../crit_cost`), 8,048 of the 8,192 the exam tells the
agent, and a 48,000-step net would not fit that budget. Every rung's nets are scored for P0, the public-form C
and the true-form C, so that the curve is shown. D nets: round 5's 1,200 steps, doubled (at most twice) if any
net's best step is past 80%. Fine-tunes: the rule is applied to the mean cross-validation curve of a group (N,
base family, eta); if a group's minimum is past 80% of the schedule the schedule doubles for every fine-tune of
that N (at most twice, and only if the job's clock allows). A rule still unmet at its cap is reported as "not
converged by the rule", with the curves.

**R17. Order under the job's clock.** N = 8 first, then N = 32, then N = 2 (the cost critic's order of cuts),
controls last. Whatever the clock cuts is listed in `DEVIATIONS.md`.

**R18. Reported, never criteria.** Skill of every policy relative to K and O; the state-given plug-in (the
public law at the true theta from the hidden state, 8 members); FT and RES fitted on 8 input-free Lab episodes
(a control at eta = 4); g at N = 2 and 32; per class and per horizon; S(N); the simulation and training cost of
each reference policy in episode equivalents.

**R19. Extension.** Requested only if g is undecided by R15 at 8 truths: 8 more truths, the first 8 viable of
48 box draws (numpy seed [6601, 4]; viability by round 5's rule under the public law), the first job's base
nets reused. The rule is then read once on 16 truths.
