# foundryexam: design, criteria and thresholds (declared before any GPU run)

Round 6, 11 Nov 2026. An exam pilot where the hidden law is a network's weights: the foundry's two-kind transport
neural automaton (`../../round5/foundry/tnca.py`). Everything here was written before the first GPU request of the
study; later changes are marked "changed after results" in README.md.

**PILOT ONLY.** Every world, weight, Lab episode and item of this study is a public function of public seeds or is
written to public outputs. Nothing here may ever be reused as an exam.

## 1. What is public, what is hidden, what the agent is told

Public: the family (law, noise levels, wind channel, initial distribution: `tnca.py`), the prior over the 250 hidden
numbers, the screen (code and thresholds), the block view, the item format, the program mix, the nats caps, the scoring
rule. Hidden: the weights of the hidden world (and in arm P its 10 scalars), the noise secret, the exam items' futures.

Two exam priors, as two arms on one harness (the "width of the prior" is the dial):

| arm | the exam's prior (public) | hidden | the agent is told |
|---|---|---|---|
| P, screened prior | theta ~ prior, given the public screen (section 2) | all 250 numbers | "one draw of the screened prior" |
| N30, neighbourhood | W = sqrt(1 - eps^2) W_c + eps W_fresh around a public centre world theta_c, eps = 0.3, given the exam-time gate; scalars = the centre's (public) | 240 weights | the centre, eps |
| N10, neighbourhood | the same with eps = 0.1 (run last, dropped first if time runs out) | 240 weights | the centre, eps |

Why both: "the weights are the only thing we hide" in its pure form is arm P, where the public simulator is the family
and not the world. A neighbourhood is the reading "one world, several hidden draws" and is the bridge to round 5's
few-parameter exams. The decision between them for a real exam is an output of this study.

In every arm the agent has the simulator of the family, a Lab on the hidden world (exam-shaped episodes in the block
view, N of them, nats caps 100 per tick and 400 per episode) and held-out items to predict.

## 2. Worlds

Pool (arm P): the early candidates of round 5 (all four gates at ticks 50-290): 88 of prior seed 2026
(r5-foundry-001) and the 323 + 5 of prior seed 2027 (r5-foundry-002, the enriched and control arms), listed in
`results/pool.json` by `make_pool.py`. Exam-time gate, applied in the job to every pool world and every neighbour
(8 members, burn-in 300 ticks, then 32 ticks): cell contrast cv_cell >= 0.25 and persistence error vp(1) <= 1.0
(the thresholds of `criteria.py`) and vp(16) >= 0.2, in units of the window's own variance.
*Changed before any GPU run:* the first version of this file had vp(16) >= 0.02, `criteria.py`'s frozen threshold. A
CPU check of 28 worlds at the exam's burn-in (`results/gatecheck_cpu.txt`, 2 members each) showed worlds at
vp(16) = 0.025-0.04 passing: at tick 300 they are nearly frozen, persistence is nearly the oracle there and the exam
would be trivially easy by construction (round 5 found that most early activity is a transient). The threshold 0.2
(16-tick autocorrelation of the block view at most 0.9) was chosen after that check and before any score existed.
Every hidden world's vp(16) is written to the outputs so that the shares can be read against it.
Hidden worlds of arm P: 16 drawn without replacement from the seed-2027 enriched candidates that pass the gate, by
numpy's default_rng(20261111) (the enriched arm is the larger sample of one well-defined screen: weights-only
pre-screen, then the four gates). Training worlds of the no-experiment policy: every other gate-passing pool world.

Centres (arms N30, N10): 3 of round 5's 7 shortlisted worlds (draws 4470, 4186, 262, 7567, 6845, 1672, 3078 of prior
seed 2026). Rule, written when the CPU probe had returned 6 of the 7 values (round 5 had already published 1672, 4470
and 262): rank the 7 by the wind probe's "aimed 200 nats, effect over noise at 4 ticks"
(`../../round5/foundry/wind_probe.py`, 8 states; 1 means the command displaces the block view as much as fresh noise
does) and take the top 3. Neighbours: `tnca.perturb_theta(theta_c, 606000 + draw, j, eps, hyper=False)`; j = 0..63
are public training candidates (the first 32 that pass the gate are used), j = 1000..1015 are hidden candidates, the
first 4 that pass the gate are the hidden worlds.

## 3. The exam (round-5 harness)

`vw.World` (tnca level, block-view coarse-graining, burn-in 300) behind `vw.harness.HistoryExam` with a
`ProgramMix`; Lab episodes through round 4's `BatchLab`. Observed level: the block view (192 numbers: block means of
the two kinds and of S^2 on the 8 x 8 grid). Item: 17 observed frames (ticks 0..16 after the burn-in, no input), a
public 16-tick test program, queries at 1, 2, 4, 8, 16 ticks; 32 items per hidden world, 12 replicate futures,
96 climatology runs. Program mix, equal shares: a none; b blind (200 nats, random direction in coefficient space,
4 ticks); c aimed (200 nats on the densest block of the last frame, random direction, 4 ticks); d regional (400
nats, one direction on the 3 x 3 blocks around the densest block, 4 ticks). Scores: fair energy score per item and
cell with the RMS norm, coordinates divided by the hidden world's own climatological SD per channel (evaluator side);
oracle-normalised skill from `vw.scoring.skill_report`; sigma and rho from
`../../round5/agentenv/evaluator/acceptance.py`, pooled over the hidden worlds of an arm.
The object view is not examined: this pilot is block view only (the tracker is checked on the centres on CPU and
reported; an object-view exam needs a second predictor family and is left to a follow-up).

## 4. Reference policies (all scripted; one predictor family)

One generative net family (periodic conv net on the block grid, noise inputs, trained with the fair energy score,
inputs normalised per item by the item's own 17-frame mean and SD per channel; a "code" input of 33 summary statistics
of a set of 17-frame windows).

| policy | what it is | needs |
|---|---|---|
| K | climatology pool of the hidden world | - |
| Kp | persistence (the last frame, no spread) | - |
| O | the simulator from the hidden state (leave one out over the 12 futures) | the hidden state and weights |
| C | trained on 1,536 simulated episodes at the true weights; 2 training seeds. Two candidates, both reported: the net trained from scratch, and P0 fine-tuned on the same simulations; C is the one with the lower pooled score over the arm (so that the ceiling of the family is not set by a data-starved net) | the hidden weights |
| P0s | net with lags (0, 1) and no code, trained on simulations of the public prior | no hypothesis, no experiment |
| P0 | net with lags (0, 1, 2, 4, 8) and the code of the item's own history, trained on simulations of the public prior (arm P: 64 episodes of every training world; arms N: of up to 32 training neighbours); 2 seeds. Reads the world off each item's history | no hypothesis, no experiment |
| P0[16], P0[64] | P0 trained on 16 or 64 training worlds (arm P): the cost of the prior in worlds | as P0 |
| S(N) | amortised inference: a net trained like P0 whose code is averaged over the item's history and 2N windows of N Lab episodes (trained with random context sizes); S(0) uses no Lab; 2 seeds | N Lab episodes |
| FT(N) | P0 fine-tuned on N Lab episodes | N Lab episodes |
| D(N) | the same net trained on N Lab episodes alone | N Lab episodes |
| Dr(N) | local ridge on N Lab episodes (3 x 3 blocks x 3 channels x 2 lags + wind), Gaussian residuals | N Lab episodes |
| plug-ins | the simulator from the hidden state with wrong weights: another screened world (arm P) or the centre (arms N), neighbours of the truth at eps 0.03, 0.1, 0.3; and with the true weights but no test program (input-blind oracle) | the hidden state |

Lab budgets N: 2 (S only), 8, 32, 128, 512 (nested prefixes of one Lab of 512 episodes per hidden world).
sigma = (L(null) - L(C)) / (L(K) - L(C)) with null = the better of D(512), FT(512), Dr(512), P0, S(0);
rho = (L(P0) - L(S(N))) / (L(P0) - L(C)).

## 5. Criteria and thresholds (declared)

1. Acceptance (roadmap bars): sigma >= 0.15 and rho <= 0.7 per arm. Verdict from the 90% interval (hidden worlds
   resampled as clusters, one training seed drawn per policy in each resample): pass if the interval lies above the
   bar, fail if below, undecided otherwise. Reported per world as well, with the median.
2. "Trivially easy for the recipe": the share of C's skill taken with no hypothesis and no experiment,
   (L(K) - L(best of P0, S(0), P0s)) / (L(K) - L(C)). At least 0.95: trivially easy (round 5's finding repeats). At most
   0.85: not trivially easy. In between: undecided.
3. State-given gap (round 5's screen): 1 - OES of the plug-in simulator with a prior draw of the weights (arm P:
   another screened world; arms N: the centre), and the same for the eps neighbours.
4. Actions matter (observation-only otherwise): on the items with a program (classes b, c, d), the loss of the
   input-blind oracle, (L(blind oracle) - L(O)) / (L(K) - L(O)), is at least 0.10. Reported per class and per world.
   For the centres on CPU: the probe's effect over noise at 4 ticks is at least 1.
5. Data-only budgets: N90 = Lab episodes at which the best data-only learner (D, Dr) reaches 90% of C's skill, and
   N_P0 = episodes at which it matches P0, by linear interpolation in log2 N; "more than 512" if not reached.
6. Convergence of a trained net: the held-out loss improved by less than 2% of (first - best) over the last fifth
   of its schedule. Groups that do not meet it are flagged and their numbers quoted as lower bounds.
7. Stationarity: the share of the block view's variance (per-world standardised) carried by the tick alone over the
   33 ticks of an episode (variance over ticks of the mean over Lab episodes and blocks). At most 0.01: stationary.
8. Training-seed variance: C, P0 and S have 2 seeds everywhere; D and FT have 2 seeds at N = 32 and 512. Every
   interval of a quantity that involves a trained net draws the seed with the worlds (as in criterion 1), and the
   seed-to-seed difference is reported next to the world-clustered SE.

## 5b. Changes after job r6-foundryexam-002 (declared before request 003; criteria and thresholds unchanged)

Job 002 trained its nets several times slower than the round-5 basis (70 ms per step of the two shared P0 nets where
about 20 were expected: one dispatch per training step under the platform allocator). It was cancelled during arm P;
what had been seen of it by then: the gate's pass counts, the validation curve of the two P0 nets, and the presmoke's
printout on 3 worlds with 60-step nets. No score of the full pass existed when the following was fixed:

- 50 training steps per dispatch (a scan inside the jitted step); the presmoke measures ms per step at the full
  shapes and stops the job if the projected net time exceeds 1.25 times what the full pass has.
- Net: the global inputs (horizon, codes, global noise) enter as a learned per-channel shift at the input and in each
  block instead of being convolved as 81 constant channels. Same information, less compute. This is a different net
  from job 002's, so nothing of 002 enters the results.
- Batch 64 for the per-world nets (C, D, FT) and 128 for the shared nets of the neighbourhood arms (256 in arm P);
  C: 4,000 steps, fine-tuned C: 1,500; P0s and P0[16], P0[64]: 6,000 steps (P0 and S: 12,000).
- Order within an arm (a deadline cuts from the end): P0, S, P0s; C; D(512), FT(512); fine-tuned C; D and FT at 128,
  32, 8; second seeds; P0[16], P0[64]. In the summary the null's budget stays 512 and is flagged if incomplete.
- The public code standardisation is computed from pool worlds that are not hidden worlds of arm P; the amortised
  net's random context never contains the example's own episode.

## 5c. Follow-up job r6-foundryexam-004, declared AFTER the results of job 003 were seen

Job 003 ran everything of sections 1-5 (results/analysis_job003.json). Two things in it fall short of the standards,
and job 004 exists to fix them. It was designed with every number of 003 in view; criteria, thresholds, worlds, hidden
picks and the null are unchanged, and 003's numbers are reported next to 004's.

1. C was not trained to convergence by criterion 6: 4 of 32 nets (arm P), 9 of 24 (N30), 7 of 24 (N10); the best step
   was the last one. In 004, C is trained on 4,096 simulated episodes at the true weights (003: 1,536) for 8,000 steps
   at batch 128 (003: 4,000 at batch 64), the fine-tuned candidate for 3,000 steps at batch 128, and a third net "Csm"
   on the first 1,024 of those episodes shows whether C is converged in data. FT(128) and FT(512) get 1.5 and 2 times
   the steps.
2. The neighbourhood arms were not like for like with arm P: their no-experiment nets saw 24 to 32 prior worlds, arm
   P's 210, and arm P's own curve (P0[16], P0[64], P0) shows that this number matters. In 004 a neighbourhood has 256
   public training candidates and uses up to the first 128 that pass the gate; its shared nets train 8,000 steps
   (P0s 4,000).

Also: all net seeds are offset by 1000, and the job draws a new noise secret, so 004 is an independent repeat of
003 on the same hidden worlds with new Labs, new items and new training seeds. Where the two jobs measure the same
thing (arm P: P0, S, D, FT, the ridge, the plug-ins), their difference is reported as a between-job check.
The final table is 004's if it completes; otherwise 003's, with C marked as a lower bound.

## 5d. Job r6-foundryexam-005, declared after job 004's arm P was seen

Seen when this was written: 003 in full, and of 004 the log line of arm P (per-cell-mean skill C 0.760 on 4,096
true-weight episodes, Csm 0.725 on 1,024, fine-tuned C 0.746, P0 0.654). C still gains 0.035 from four times the data,
so it is not converged in data and every share normalised by C is a bound: P0's share an upper bound, sigma a lower
bound. Job 005 adds one more point to C's learning curve, in arm P only: 16,384 true-weight episodes per hidden world
and a net "Cbig" trained on them (24,000 steps at batch 128, one seed; seed-to-seed differences of C were 0.0003 in
003). Rule, fixed now: the ceiling C of a job is the candidate with the lowest pooled score over the arm among the
scratch nets and the fine-tuned net (sections 4 and 5c); in 005 Cbig is a candidate. The summary reports the curve
C(1,024), C(4,096), C(16,384) from 005 and says whether the last step is still above 0.01 of pooled skill; if it
is, C stays a lower bound in every table and the text says so. Everything else in 005 is 004's arm P unchanged
(same hidden and training worlds, seeds + 2000, a new noise secret), so arm P has three independent repeats (003,
004, 005) of every policy other than C; their spread is reported.

## 6. Sizes and budget

Hidden worlds: 16 (arm P) + 12 (N30) + 12 (N10). One GPU job (A100, $1.99-2.35/h), expected about 2 h, cap $8.40
(job 002; request 003 after the changes of section 5b: cap $7.80; request 004, section 5c: cap $8.40; request 005, section 5d: cap $7.20);
a second job only for a declared follow-up. Study cap $25.
