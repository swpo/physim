# Study dialsA2, the gliders stress-conversion exam reopened: what is declared before any run

11 Nov 2026, about 19:50 UTC. Written and committed before any job request and before any decisive run (no code of
this study exists at this commit). Part 1 copies the coordinator's task for this study, which applies the plan
(`../PLAN.md` section 2 A, section 3 row "A: refuted, with s >= 0.15") and the lead's choice "Reopen, triggered bar"
(`../../../roadmap/DECISIONS.md`, section "Round-6 design studies: the lead's two choices"); nothing in it is mine and
nothing in it may change. Part 2 fixes, also before any result, what Part 1 leaves open. If something proves
impossible, the nearest thing is done and written in `DEVIATIONS.md` at the time; this file is not edited after its
first commit.

PILOT ONLY: every truth here is a public pilot value (round 5's 8, and 8 drawn by a public seed); the truths, Lab data,
items and nets of this study must never be reused as an exam.

## Part 1. Binding (from the task, which applies the plan and the lead's choice)

**Question.** In round 5's gliders exam with an incomplete public law (stress conversion, `../defect_gliders/dlaw.py`
term XW), restricted to the items that trigger the hidden term and to horizons 8 to 16 ticks, is the science share
left after the best generic repair at least 0.15, and is the design solvable by a recipe told the form?

**Exam.** Round 5's ladder harness, the cell with four hidden parameters, block view. Items are 16 input-free ticks of
history plus a held-out program of the aimed (200 nats) or regional (300 nats) class; answers at 8, 12 and 16 ticks,
pooled. Threshold 0.12 and ramp 0.05 fixed as in study A. 16 pilot truths (the ladder's 8 plus 8 fresh draws from the
same prior), each at eta 0 (zero point) and eta 4; eta 1 and 2 reported for 4 truths if the budget allows. The
agent-facing sentence is A's: "the simulator may lack mechanisms of the world; which, where and how strong is not
said; there may be none."

**Lab per truth.** 32 mix episodes of the two triggered classes (the budget), 32 input-free, 32 designed (the dose
series and controls of `../defect_gliders/DESIGN.md` section 2, at most 200 nats per episode, 100 per tick).

**Policies.** K (climatology), O (the true law from the hidden state), C (the true-form net at the truth, or that net
fine-tuned on Lab: the better, picked on the unscored half), P0 (a net trained on simulations of the public prior),
D(N) (N Lab episodes alone), S(N) (round 5's scripted inference of the four parameters with the public law), FT(N)
(P0's net fine-tuned on N Lab mix episodes) with its grid widened until the cross-validated pick is interior, RES(N)
(P0 plus a per-block residual) with a cross-validated ridge, G* = the best of P0, D, S, FT, RES picked on the
unscored half; H(N) told the form, not the values (synthetic likelihood for the four parameters and the rate on the
corrected simulator from the designed episodes, then the true-form family at posterior draws); H_mix(N) the same from
the mix episodes only. N = 8 primary, 32 reported.

**Training.** Every scored net trained to the plan's rule (best validation step in the first 80% of the schedule;
doubling allowed up to a declared maximum that the budget covers; many steps per dispatch, 25 to 50), three seeds,
equal steps across the policies compared.

**Criteria**, at eta 4, N = 8, triggered exam, horizons 8 to 16 pooled, truths as clusters plus the seed term,
one-sided 90% bounds. L is a policy's pooled energy score; lower is better.

| criterion | number |
|---|---|
| T1 science share | sigma_G = (L(G*) - L(C)) / (L(K) - L(C)) >= 0.15: the lower bound of the mean of L(G*) - 0.85 L(C) - 0.15 L(K) is at least 0 |
| T2 generic share | rho_G = (L(P0) - L(G*)) / (L(P0) - L(C)) <= 0.7, tested the same way; read only if L(P0) - L(C) exceeds 2 SE |
| T3 solvable | H recovers at least 0.7 of the P0-to-C gap and beats G* at t >= 3 over truths |
| T4 actions matter | C made blind to the program loses at least 0.10 of L(K) - L(C) |
| T5 not one truth, not one horizon | T1 and T2 hold at the point estimate with the heaviest truth left out, and at 8 and at 16 ticks separately |
| zero point, at eta 0 | C true-form against C public-form, and G*, H against P0 and S, each within 0.02 of L(K) - L(C) on the mean over truths |
| **PASS** | T1 to T5 and the zero point |
| **FAIL** | T1's upper bound below 0.15, or T2's lower bound above 0.7 |
| **UNDECIDED** | anything else; reported as undecided, never as a pass |

Also reported: H_mix against H (what designed experiments add), the whole-exam numbers beside the triggered ones, the
nets' convergence curves.

**What each outcome means** (declared now):

| outcome | what it means |
|---|---|
| PASS | The first design of type (b) to pass against scripts in this program, on a stated restriction (triggered items, 8 to 16 ticks). It goes to the environment as an exam profile and to rollouts, which alone say whether an agent finds the form. |
| FAIL with T3 holding | A told-form recipe solves it, but generic repair at 8 episodes is close enough to C that the share is small. |
| FAIL with T3 failing | The design is not solvable by the declared recipe at this Lab budget. |

(For UNDECIDED see Part 2, R21.)

**Budget.** GPU cap $12 for the study in at most two jobs.

## Part 2. Fixed here, before any result, where Part 1 is silent

**R1. Score.** Horizons 8, 12, 16 ticks after the anchor (the end of the 16-tick history; the program starts there).
L = mean over items of the fair energy score summed over the three horizons, by the exam's own scorer
(`ladder_lib.ViewCells`: `vw.harness.HistoryExam._per_cell` + `vw.scoring.energy_fair`), as `acceptance.py`. "At 8
ticks" and "at 16 ticks" (T5) use that horizon's score alone.

**R2. Items and halves.** Per truth and eta two exams of round 5's shape (`pilot.GExam`, prefix 16, 12 replicates,
climatology pool of 48 input-free runs), each of 48 items drawn from the public mix {aimed, regional} in equal shares
(`ProgramMix` of round 5's two class functions): `sel` (every pick is made on it and nothing else) and `score` (every
L and every criterion). 96 items per world.

**R3. Truths.** Truths 0-7: round 5's (`round5/ladder/results/job/n4/truths.json`). Truths 8-15: the first 8 viable of
48 draws from the public box (numpy seed [6601, 4]), viability by round 5's rule under the public law
(`viab_joint.viability`), exactly study A's R19 rule, computed inside the job. Round 5's fitted viability prior is read
from `prior.json`. The eta 1 and 2 arms use truths 0-3. Worlds are nested: the same secret children, starts, noise and
Lab random numbers at every eta of a truth.

**R4. Seeds and statistics.** Three complete sets of nets (seeds 0, 1, 2): public-form, true-form and every net
derived from them. L of a truth is the mean over its three seeds; picks are made per truth and seed. For a per-truth
contrast c_t: SE^2 = SD_t(c)^2 / n_truths + SD_s(c_bar_s)^2 / 3 (c_bar_s the mean over truths of seed s). One-sided
90% bounds: mean -+ t(0.90, n - 1) SE (1.341 at 16 truths). A ratio is the ratio of the means over truths, its SE
from the linearised contrast. Beside every mean: the median over truths and the leave-one-truth-out range.

**R5. Lab.** Per truth and eta: 32 mix episodes (16 consecutive pairs, each one aimed and one regional in random
order), 32 input-free, 32 designed (4 consecutive blocks, each the 8 arms of R6 in random order), in that order; 33
charged ticks each (anchor observation + 16 + 16); caps 100 nats per tick and 400 per episode (round 5's), designed
arms at most 200 by construction. "The first N" mix or designed episodes are taken in that order.

**R6. Designed arms** (`../defect_gliders/DESIGN.md` section 2 and `dlaw.strong_push`). A uniform force in a random
direction on a 2 x 2 group of blocks, from the anchor on, for the given ticks; target the heaviest group
(`gworld.heaviest_group`) unless stated:
1. 12.5 nats per tick x 4 ticks (50 nats; peak field about 0.11, below the threshold);
2. 25 x 4 (100; about 0.16, on the ramp);
3. 37.5 x 4 (150);
4. 50 x 4 (200; about 0.23);
5. 100 x 1 (100; about 0.32);
6. 100 x 2 (200);
7. control, empty: 100 x 2 on the 2 x 2 group with the least block mass (smallest sum of the coarse mass-squared
   numbers);
8. control, channel 1: 100 x 2 on the 2 x 2 group with the largest channel-1 minus channel-0 block mean.

**R7. Families** (all 768 points x 8 episodes, simulated in the job; theta uniform on the public box).
Public: round 5's simulator unchanged (`ladder_lib.sim_episodes`), 4 aimed + 4 regional episodes per point (numpy
seed [6602, 0]). True-form: `dlaw` through study A's law switch (`../dialsA/xlaw.py`), the same classes, eta = 0 at
192 points, 4 at 192, uniform on (0, 4) at 384 (a fixed random assignment; seed [6602, 1]), so that H's posterior
draws and the eta 1 and 2 arms lie inside the trained range. Designed (H's emulator only): `dlaw`, eta uniform on
[0, 4], the 8 arms of R6 once each per point (seed [6602, 2]). Threshold and ramp are dlaw's constants everywhere.

**R8. Nets.** Round 5's block-view net (`ladder_net`, unchanged) with its horizon set Cfg.HS = (8, 12, 16) (the
exam's), lags as round 5's. The public-form net is conditioned on theta, the true-form net on (theta, eta / 4). Trained
with round 5's loss, AdamW, batch (128 x 4 draws), and cosine schedule (rate 1e-3, warm-up 100 steps, floor 0.1),
validation every 250 steps on 10% held-out episodes, the best-validation parameters kept; implemented in this
study's trainer with 50 steps per dispatch (a `lax.scan`), the six base nets in lockstep. P0 = the public-form net
with theta drawn per sample from round 5's viability prior; public-form C = that net at the true theta; true-form C =
the true-form net at (true theta, eta / 4).

**R9. Training rule, base nets.** Schedule 24,000 steps (study A's last rung; A showed 6,000 and 12,000 unconverged),
then doubled, each rung retrained from scratch, while any of the six base nets has its best validation step after 80%
of the schedule; at most to 192,000 steps (three doublings), the most the first job's clock is sized for. All six nets
always get equal steps. Every rung trained is scored (P0, public-form C, true-form C) so the curve is shown; the last
rung trained is the scored one. A doubling is made only if the presmoke's estimates leave time for the required
stages (R18); a doubling cut by the clock, or a rule unmet at 192,000, is reported as "not converged by the rule" with
the curves, and written in `DEVIATIONS.md`.

**R10. C.** At eta > 0, per truth and seed the better on `sel` of (a) the true-form net at (true theta, eta / 4) and
(b) that net fine-tuned on the first N Lab mix episodes by FT's recipe (R11), its conditioning held at the truth. The
criteria use N = 8. At eta 0 the zero point compares the true-form net with the public-form C, and the unit is
L(K) - L(public-form C), as in A.

**R11. FT(N).** Start from the public-form net of the same seed; data: the first N Lab mix episodes, every anchor and
horizon of base training; conditioning drawn from the public prior per example; AdamW with a fresh state at a
constant rate, batch 64 x 4 draws, 40 steps per dispatch, many fine-tunes in lockstep. Cross-validation over episodes,
min(4, N) folds stratified by class. Grid: rates {1e-4, 2e-5}, the held-out score every 10 steps from 0 to 400 steps;
each net takes the (rate, steps) with the least mean held-out score over its folds (0 steps = P0's net unchanged),
then is fine-tuned on all N episodes at that point. Widening, decided on each group's mean curves (group = kind x N x
eta): if the group's best point is past 80% of the steps (the plan's rule), the steps double; if it is at 0 steps or
at the first grid point (10) of the smallest rate, a rate five times smaller is added; each at most twice. The pick
is "interior" when neither holds; the share of nets whose own pick lies at an edge is reported per group. CFT (R10) is
the same recipe on the true-form net.

**R12. RES(N).** The designer's per-block residual on P0's predictive mean (32 samples) at the anchor, per program
class (structural), horizon and region class (blocks under input, their neighbours, the rest), fitted on the first N
Lab mix episodes, with the ridge chosen per class among {0.05, 0.5, 5, infinity (no correction)} by leave-one-episode-
out squared error (`../dialsA/a_nets.res_fit_cv`; a class with one episode keeps 0.05). The fitted correction is
added to every P0 sample. A's fixed ridge (0.05) is reported as RESfix, never picked.

**R13. S(N), D(N).** S: round 5's inference for the block view (projection and emulator from the public family's
episodes, importance sampling under round 5's viability prior, `ladder_lib.posterior`, M = 20,000), from the first N
Lab mix episodes, then the public-form net at posterior draws. D: round 5's unconditioned block net on the first N
Lab mix episodes (3 seeds, 1,200 steps, validation every 50 steps, doubled at most twice under the rule) or round
5's block ridge on them, the better on `sel` per truth and seed.

**R14. H(N) and H_mix(N).** Told: the form of the missing term (dlaw's XW with its threshold 0.12 and ramp 0.05) and
a uniform prior on the rate eta over [0, 4] (the true-form family's range; the truth sits at its top, which favours
H). Not told: theta and eta. Summary per episode: round 5's 13 block-view features, the share of the channel-0 block
sum lost from the anchor to 1, 2, 4, 8 and 16 ticks after it, and the share lost in the blocks under input at 1, 2 and
4 ticks (21 numbers, level 1 only). Projection (`sbi_lib.Projection`): a ridge regression of (theta in box units,
eta / 2 - 1) on the standardised summaries, fitted per designed arm (H, on the designed family) or per program class
(H_mix, on the true-form family). Emulator: `ladder_lib.Emulator` over the 5 parameters on the family's projected
summaries (768 points x 8 episodes). Posterior: `ladder_lib.posterior` on [-1, 1]^5, prior = round 5's viability
prior on theta times uniform eta, M = 20,000, observed = the mean projected summary of the first N designed (H) or
mix (H_mix) Lab episodes. Prediction: the true-form net of the same seed, one posterior draw per sample.

**R15. G\*.** Per truth and seed the best on `sel` of P0, D(8), S(8), FT(8), RES(8); scored on `score`. At N = 32 the
same with the 32-episode members (reported).

**R16. Blind C (T4).** C of R10 with each item's program replaced by no input (the net still sees the history);
per truth and seed the blind copy of the candidate C picked.

**R17. Readings of the criteria.**
- T2 holds if the upper bound of d = [L(P0) - L(G*)] - 0.7 [L(P0) - L(C)] is at most 0; its lower bound above 0 is
  FAIL. "Read" if mean_t [L(P0) - L(C)] > 2 SE; not read: T2 does not hold and cannot fail.
- T3: the point estimate of (L(P0) - L(H)) / (L(P0) - L(C)) is at least 0.7, and mean_t [L(G*) - L(H)] / SE >= 3.
- T4: the point estimate of (L(blind C) - L(C)) / (L(K) - L(C)) is at least 0.10.
- T5: the heaviest truth is the one with the largest L(P0) - L(C) (seed mean); with it left out, sigma_G >= 0.15 and
  rho_G <= 0.7 at the point estimate; and the same two at 8 ticks alone and at 16 ticks alone (all 16 truths). The
  worst single leave-one-out of each share is reported beside it.
- Zero point, at eta 0, N = 8, in units of mean_t [L(K) - L(public-form C)], |mean_t of the pair's difference| <=
  0.02 for: true-form C against public-form C; G* against P0; H against S (read respectively). The cross pairs, G*
  against S and H against P0, are reported with the same tolerance, not part of the rule.
- FAIL is read whatever the zero point; a zero-point miss is reported beside any verdict.

**R18. Order under the job's clock.** Required: truths, families, worlds at eta 0 and 4, the inferences (S, H, H_mix),
base nets at 24,000 steps, then at N = 8: FT, CFT, RES, S, D(8), H, H_mix, blind C. Then, each only if the presmoke's
estimate fits: the base-net doublings (each reserving time for the N = 8 stages), N = 32 (FT, CFT, RES, S, D, H,
H_mix), the eta 1 and 2 arms for truths 0-3 at N = 8. What the clock cuts goes to `DEVIATIONS.md`.

**R19. Reported, never criteria.** Per class (aimed, regional) and per horizon; skill relative to K and O; H_mix
against H (the contrast L(H_mix) - L(H) and both recoveries); N = 32; eta 1 and 2; RESfix; FT's and CFT's picks and
curves; the posterior errors of S, H, H_mix in prior SDs; the base nets' curves at every rung; the cost of each
reference policy in episode equivalents (the research budget of an exam profile is set from these, after this study);
study A's whole-exam numbers (all four classes, horizons 1-16, from `../dialsA/results/summary.json`) quoted beside
this study's, with their source, since this exam has triggered items only (see `DEVIATIONS.md` entry 1).

**R20. Jobs.** At most two, GPU cap $12 in all. The first: one A100 40GB (lambdalabs, $1.99/h), the script's own
limit 3.6 h, max_hours 3.9, cap_usd = 1.99 x 4.15 + 0.10, rounded up: $8.40. A presmoke first (every stage once at
full shapes; exit non-zero within minutes on a failure) and a speed guard (exit 4 if the required stages cannot
finish inside the script's limit). A second job only to finish what the first could not (a failure or the clock),
within the remaining $3.60; never to add truths after seeing a result.

**R21. Undecided.** An undecided verdict is reported as undecided with every number; no extension is declared here
(the plan's "one extension" belonged to A's g), so the next step goes to the lead.
