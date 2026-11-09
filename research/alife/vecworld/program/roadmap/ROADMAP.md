# Roadmap: supervenient worlds as tests of scientific ability

For the lead, 9 Nov 2026. Built from four memos (Q1 to Q4) and their second reading (`CRITIQUE.md`), all in `R/` = `/home/user/evalwork/vecworld/program/roadmap/`. Other prefixes: `P/` = `/home/user/physim/research/alife/vecworld/program/`, `V/` = `/home/user/physim/research/alife/vecworld/vw1/`, `A/` = `/home/user/physim/research/alife/`. Thresholds, budgets and dates are proposals. New arithmetic: `R/checks/roadmap_envelope.py`.

**Verdict.** The framework is sound, implemented and cheap to run. The exam built on it does not yet test science. On our only end-to-end pilot, a policy with no hypothesis and no experiment takes 95% or more of the skill our best reference reaches, and no agent has sat a v2 exam. Every proposal in the memos is judged by gaps between predictors we wrote ourselves. So the first money should go to agents taking the exam we have, and the first design work to what decides what an exam measures: what the agent cannot simulate.

## 1. The goal, and what "doing science" means here

The goal is yours: virtual worlds that test an agent's ability to do science, free of physical interfaces. A world is a level-0 law with hidden parameters and explicit noise, a chain of deterministic coarse-grainings above it, and two ports (`V/note/CATEGORY.md`, Def. 9). The agent observes level k ≥ 1, perturbs level 0 through a channel charged in nats, holds the public simulator, and submits a frozen predictor of how level k responds to input programs it has not seen (`P/track2/EXAM.md` §1). PhySim v1 is the case with sensors and devices on a hidden prepared state and no simulator (`EXAM.md` §5).

**Operational definition.** An agent does science on an exam to the extent that it beats two policies that do none:
- **D**, which fits a level-k predictor to the lab data;
- **P0**, which simulates the public prior and trains a predictor on the result.

The margin over the better of the two has three measurable parts: using a theory, inferring what is hidden, and experimenting (designed inputs against blind ones at equal nats).

**One notation** (replacing Q1's rungs and Q2's letters): K, the long-run average; D(N), with N lab episodes; P0; S(N), scripted inference then training on simulations; T, the level-k effective law with fitted constants, never running level 0; C, trained at the true parameters; O, the simulator run from the hidden state.

**One acceptance definition**, replacing the three in the memos. It avoids the oracle, because oracle-normalised skill is not comparable across base levels (`CATEGORY.md`, Prop. 9(d)). L is a policy's pooled energy score, with one predictor family throughout. The agent's compute envelope is part of the exam. C is a lower bound, so shares may exceed 1 and are not clipped.
1. Science share σ = (L(null) − L(C)) / (L(K) − L(C)), where null is the better of D at budget and P0. Bar: σ ≥ 0.15.
2. Scripted share ρ = (L(P0) − L(S)) / (L(P0) − L(C)) at budget. Bar: ρ ≤ 0.7.
3. Checks 3 to 6 of `EXAM.md` §6.2: actions matter, the budget binds, the envelope is safe, the audits pass.
4. Where T exists, the theory ratio (L(D) − L(agent)) / (L(D) − L(T)) on transfer items (Q3 §4).
5. Validity: two models of different strength are ordered at z ≥ 3, clustered by hidden world.

The gliders pilot has σ at most 0.05 and ρ of 0.77 to 0.94 after two episodes (`R/checks/roadmap_envelope.json`, from `P/round4/sbi/results/summary.json`). It fails items 1 and 2, and item 5 is untested.

## 2. What is established

1. **The framework is consistent and implemented.** An exam depends on a world only through its input-output behaviour, so exact refinements are invisible to every score. Closure defects compose by a chain rule. Coupling through coarse signals preserves exactness; through micro signals it does not (`CATEGORY.md`, Props. 6, 9, 11, 12). Gliders, fed vortices and the phase membrane each run with three levels (`P/README.md`).
2. **Interaction has an exact price, and the score is fair.** An input that shifts a Gaussian noise term costs half its noise-whitened squared norm in nats (`EXAM.md` §3.1; checked in `P/CRITIQUE.md` §2). On gliders a wind channel makes inputs matter and the matter kick does not (`P/track2/actuation/results/summary.json`). v1's energy-score estimator is biased by +6.7% at 15 members; v2's is not (`P/track2/harness/results/summary.json`). The designer's ceiling is a lower bound that moves 0.12 with predictor quality (`P/CRITIQUE.md` §1b).
3. **Learned coarse-grainings find field variables, not objects.** Closure and local-law objectives with local encoders learn a mass-like block variable (R² up to 0.995). Nothing learned beats the hand designs in predictable content per number, and no bias yields the object view. When the map is free, closure rewards smoothing (`P/round4/bias/results/summary.json`; `P/track1/learned_phi2/results/summary.json`). All of this is on one level-0 theory.
4. **On gliders the simulator carries the exam.** P0 scores 0.544 of oracle skill, equal to D at 512 episodes. The true parameters add 0.021 to 0.042, and two episodes of scripted inference recover that (`P/round4/sbi/results/summary.json`). Given the true state the same parameters are worth 0.26 (`P/track2/gliders_exam/results/summary.json`), so partial observation removes most of their effect.
5. **Inputs move the truth more than predictors use.** Under the exam's program mix they shift the dynamics by about 0.2 of the best level-1 error; learned predictors recover 44% of that at one tick in the object view and nothing in the block view (`P/round4/wind/results/summary.json`).
6. **Fed vortices show selection at level 2, without a level-2 law.** The signal holds in 6 of 6 seeds at 128². The oracle shows 51-56% of the kind-share change is predictable, and a linear level-2 predictor reaches at most 0.10 of it even given the true selection coefficient (`P/track1/vortex128/results/summary.json`, `decisions.closure_128`). `P/README.md` still says the coefficient "carries" the predictable part; the checker withdrew that.
7. **Compute is cheap and not reproducible bit for bit.** One A100 runs 1,600 member-ticks per second, $0.40 per million; $13.71 is spent (`P/gpu/bench/README.md`, `P/gpu/LEDGER.md`).
8. **Checks that recompute work; checks that judge do not.** Independent checkers recomputed all 11 studies from saved outputs and corrected the reports (each `checker` block). In the ALife collective 79.9% of 877 judged verdicts were Supported, and every fall in the headline score followed the operator's own audits (`A/evals/labworlds/reports/summary_final.md`).

**Only suggestive.**
- Q2's model of difficulty (regret ½ tr[H(Σ₀⁻¹ + N I_k)⁻¹]). Its predicted residual of 0.003-0.005 sits beside a measured 0.002-0.003 with standard error 0.003 (`R/CRITIQUE.md` §1).
- "The inputs were not needed to identify the parameters." The summaries ignore inputs, but both identifying episodes carried input programs, and no passive run exists (`P/round4/sbi/run_sbi.py`).
- "Depth is not a dial", the information rates per view, and the hydrodynamic reading of the ceiling. Each rests on a linear model (`R/checks/q2_ring_difficulty.json`, `q2_view_information.json`, `q3_hydro_scaling.json`).
- Everything about agents. One frontier-model rollout exists on the v1 fed-vortex bundle: reward 0.49, against 0.72 for the true simulator (`P/laptop/scorer-fix-impact-table.md`).

## 3. Open questions

**How can we generate new interesting worlds?** "Interesting" should mean "passes the acceptance definition"; closure is a gate, not an objective (Q1 §1).
- No generated world has passed any gate, and no pass rate is measured for any family (Q1 §2).
- No composite has been certified, although theory predicts its certificates (Props. 6 and 12).
- Can hidden parameters matter in a viable family? The gliders prior shrank from ±15% to ±9%, and 4 of 16 corners still fail viability (`P/track2/gliders_exam/results/summary.json`).
- The memos disagree on what to generate: a neural-CA foundry pass (Q1), structured families only (Q2), composites of textbook parts (Q3). I would defer the neural-CA pass: until agents validate the acceptance definition, a foundry optimises an untested fitness.

**What makes a setting challenging, in levels and maps?** The number of levels is not the difficulty. With a public, correct, cheap simulator and a few smooth hidden parameters, P0 needs no science, and on Q2's model inference costs a few episodes per parameter whatever the levels. My position: *a level structure tests science only where the agent cannot buy its way down to level 0.* Three devices do that: a public law that is wrong by a measured defect (a hidden level below it; Prop. 11(c)), no simulator (v1), or a level 0 too dear to run at exam scale. The third is why levels matter in natural science.
- On gliders nothing is too dear. P0's training set costs 3.2 core-hours and the whole scripted recipe 28.5, against 96 in a 4-core, 24-hour sandbox. The GPU for 8 hours proposed in `EXAM.md` §5 is 61 times the recipe (`R/checks/roadmap_envelope.json`). A cap must come from scale: under diffusive scaling each further field level with block factor b costs b⁴ in level-0 work, 256 at b = 4 (`R/CRITIQUE.md` §3).
- The position is untested on agents, and Q2's first falsifier would refute it.
- Do designed experiments beat passive observation? No passive run exists. Q2 says inputs matter only where fluctuations do not reach; in Q3's check a push inside one block has 27% of a block push's response where passive correlations predict none. I follow Q3.
- A priced choice of view is an untried dial: the two level-1 views are complementary (Q2 §3).

**Which properties of natural science can we exhibit?** Nearly all the classical ones, from conservation laws and hydrodynamic limits to renormalisation, fluctuation relations and the breakdown of effective theories. Quantum mechanics, reversible Hamiltonian mechanics and true limits do not fit (Q3 §2, §5).
- None of our three worlds has a tested reference law, so a low score cannot be attributed to the agent, the certificate or the absence of a law. Finding 6 is the live case. Nor have our certificates been checked on a world with exact answers.
- In the linear ring the ceiling does not improve with block size b under the stationary law; for prepared profiles the deficit falls as 1/b. If that generalises, exams starting from the burnt-in law sit where effective laws are weakest (Q3 §3).
- Agents will recognise textbook systems. Those worlds calibrate; exam-grade worlds couple certified parts.

**How can teams or swarms of agents research this?** Rounds with recomputing checkers are the best organisation we have tried. The reason to go further is separation of knowledge, not throughput (Q4).
- The catch rate of our checkers on planted defects has never been measured in any of the three organisations, nor has a round's token cost (Q4 §1).
- One coordinator session designs worlds, draws truths and would launch contestants. GPU outputs go to a public branch with unsalted hashes (`origin/gpu-jobs:PROTOCOL.md`).
- The best first use of more agents is as contestants, whose scores are computed, not judged.

## 4. The plan

Dates: 23 Nov (2 weeks), 21 Dec (6 weeks), 1 Feb 2027 (12 weeks). A round is a batch of parallel studies with checkers; workstreams share rounds. Token prices are v1's: $7.60 and $23 per rollout for the two pilot models (`A/evals/labworlds/rollout_kit/README.md`).

| workstream | by 23 Nov | by 21 Dec | by 1 Feb |
|---|---|---|---|
| **A. Agents on exams** | The agent environment passes a scripted smoke test. Six graded rollouts: 2 models × 3 fresh hidden gliders worlds, simulator, 4 cores for 24 hours, beside K, D, P0, S and C. *Result:* where each agent sits relative to P0 and S. Tokens $90, GPU under $10, 1 round | Twelve more, in a capped arm (simulation under P0's 3 core-hours) and a no-simulator arm. Four on fed vortices, in v1 and v2 form. *Result:* whether any arm orders the two models at z ≥ 3. Tokens $245, GPU under $20, 2 rounds | Two models sit B's frozen exam on 5 sealed hidden worlds. *Result:* item 5 passes or fails. Tokens $155, GPU under $20, 1 round |
| **B. Exam design** | Acceptance as code, reproducing σ and ρ on gliders. The reference ladder on gliders, vortices at 64² and the membrane, with passive, blind and designed inputs and a sub-block push. *Result:* σ, ρ and the designed-to-blind ratio per world. GPU $5-20, 1 round | Three dial studies at three settings each: a hidden sub-level with defect η (η = 0 must reproduce the baseline), scale-transfer items under a predictor cap, a hidden kernel subset. *Result:* which dial reaches σ ≥ 0.15 with ρ ≤ 0.7. GPU $30-50, 2 rounds | Exam v1 frozen with its envelope and thresholds, passing items 1 to 4. GPU $20-40, 2 rounds |
| **C. Worlds and calibration** | Two CPU ports with checkers: the conserved lattice with a hidden potential, and clean vortices. *Result:* T implemented; certificates match the closed forms within stated error. GPU $0, 1 round | Six to eight composites of certified parts. *Result:* defects add as Props. 6 and 12 predict, or not. A count lattice with Moran selection. *Result:* its level-2 predictable fraction matches theory. GPU under $10, 2 rounds | Two frozen worlds passing items 1 to 4, one a composite with exact reference answers. A foundry pass on a skeleton family only if A has validated acceptance. GPU $0-150, 2 rounds |
| **D. Sealing and record** | The running round committed. A sealer and grader script on your Mac with a private store. *Result:* one pilot instance sealed, graded and revealed with no model session holding its truth. GPU $0 | Sixteen planted defects and six clean controls through the checkers. *Result:* at least 14 caught, at most 1 control rejected. Tokens only, 1 round | Go or no-go on the collective pilot (section 5) |

**Totals.** GPU at most $320 of the $986 left. Rollout tokens about $490. Five shared rounds, whose token cost the first will measure. At the pace of rounds 1 to 4 (11 checked studies in two days) agent time does not set these dates; rollouts of up to 24 hours, the Mac runner and your decisions do.

**Dependencies.**
- A's first rollouts need the agent environment, its vortex rollouts need a v2 vortex exam, and anything sealed needs D.
- B's choice of dial at week 6 needs A's first table. If agents sit at S whatever their strength, the dial studies come before any new world. If they fall below P0, parameter fitting already discriminates and gliders is usable as it stands.
- C's composites need its certified parts and B's acceptance code. The foundry waits for item 5.

**Where the running round changes this.** Only two of its six studies are visible from this container (`/home/user/wt/bias2`, `slots`).
- **Agent environment.** If it works, A starts this week. If not, building it outranks everything in C beyond the two ports.
- **Vortex exam pilot.** σ ≥ 0.15 at level 2 makes fed vortices the first exam candidate and shows a nonlinear predictor reaching what finding 6's linear one could not. Under 0.05, the count lattice moves to week 2.
- **Difficulty ladder.** If depth alone costs over 30 times the episodes, my position in section 3 is too strong and B adds a depth study.
- **Foundry.** A stage-2 pass rate of 1% or more keeps the conditional pass and makes rejection sampling enough. Below that, ports and composites are this quarter's supply.
- **Slot encoders, bias map.** Encoders that match the tracker, or a learned map that beats the hand designs, add generated levels to C's supply.

## 5. How the work is organised

- **Keep the rounds, with four rules.** No model session holds a live truth. Checkers edit the file that summaries are generated from. Criteria are declared before each run. Token cost is recorded per study.
- **Defer the collective pilot** (Q4 §7: 10 seats, 5 days). Its first success criterion needs an exam that passes acceptance, and none does. Triggers: one exam has ordered two agents, and the catch rate is known.
- **GPU.** The runner allows two pods at once (`origin/gpu-jobs:PROTOCOL.md`); Q1's "serial" is wrong. Four of seven round-4 requests returned nothing (`P/gpu/LEDGER.md`), so each request first passes a CPU dry run and a smoke run under $1.
- **What you review.** One page per round: each exam's reference table with σ and ρ, the agent table, spend against caps, decisions waiting, and the video of any world promoted to an exam. You decide thresholds, promotion to a sealed exam, disputes between author and checker, and any GPU job over $25.

## 6. Decisions needed from you

| decision | options | recommendation |
|---|---|---|
| 1. What is hidden | (a) parameters of a correct public law, as now; (b) also a level below the public law, with a measured defect; (c) a correct law too dear to run at exam scale; (d) no simulator | Authorise (b) and (c) as exam dials, which changes the hidden set of `P/README.md`. Keep (a) as baseline and (d) as an arm. Choose between them at week 6 |
| 2. The agent's compute envelope | one GPU for 8 hours ($16-19 per rollout, 61 times the gliders recipe); 4 cores for 24 hours (3.4 times); a cap declared per exam | The envelope is part of each exam's definition. CPU only this quarter |
| 3. The acceptance definition | section 1; or keep the six checks of `EXAM.md` §6.2 alone | Adopt section 1 as provisional, to be recalibrated on A's first table |
| 4. Rollouts before worlds | 18 rollouts on the gliders pilot now (tokens about $275); or wait for a better exam | Now, with the two models of the v1 rollout kit unless you name others |
| 5. Neural-CA foundry pass ($150-300) | now; after validation; never | After validation, and only on a family with structure |
| 6. Collective pilot (about $2,150) | now; on the triggers of section 5; never | On the triggers. Approve the sealer and a private store on your Mac now |
| 7. v1 and v2 on one world | keep them apart; or run the same models on both forms of fed vortices (4 rollouts, about $60) | Run it: the one direct measure of what the generalisation bought |

Decisions 1 to 3 replace items 3 and 8 of `EXAM.md` §6.4. No citation is new here; the literature behind each position is in the memos and `P/lit/`.
