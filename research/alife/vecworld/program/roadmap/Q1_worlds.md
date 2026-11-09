# Q1. How can we generate new interesting worlds?

For the lead, 9 Nov 2026. Path prefixes: `P/` = `/home/user/physim/research/alife/vecworld/program/`, `V/` = `/home/user/physim/research/alife/vecworld/vw1/`, `A/` = `/home/user/physim/research/alife/`, `R/` = `/home/user/evalwork/vecworld/program/roadmap/`. Thresholds are proposals.

## Answer in brief

1. The framework holds three worlds (gliders, fed vortices, phase membrane), all hand-designed or ported (`P/README.md`). No generated world has passed a gate yet; the running foundry study is the first attempt.
2. "Interesting" should be defined by what an exam can separate, not by how the world looks. A world is interesting when a fixed ladder of reference solvers separates on it and each step up is a distinct scientific act: using the theory, inferring hidden parameters, experimenting. Closure is a gate, not an objective.
3. By that definition gliders is weak. Having the public simulator is worth 0.54 of the oracle's skill; identifying the hidden parameters adds 0.02 and is finished after two episodes (`P/round4/sbi/results/summary.json`).
4. Recommendation: search over families and sample instances. Draw exam worlds by rejection sampling from a declared prior and score families by ladder gaps. Take mechanisms from the hand-designed worlds and depth from the composition operators. One pass over a family costs $70-150 of GPU.

## 1. What "interesting" should mean

**The ladder.** Skill is OES, the oracle-normalised energy skill of `P/track2/EXAM.md`: 0 for the long-run average, 1 for the oracle, the simulator run from the hidden state. What separates R4 from the oracle is hidden state, which no agent can reach.

| rung | reference solver | the step up measures |
|---|---|---|
| R1 | level-k predictor trained on the agent's own budgeted data | regularities learnable without theory |
| R2 | the same predictor trained on simulations of the public family at the prior | using the theory |
| R3 | trained at the posterior after identifying the hidden parameters | inference |
| R4 | as R3, with inputs chosen to be informative | experiment |

**Proposed definition.** A world is interesting at level k and data budget n if it passes the gates of section 3 and:
- R3 − R2 ≥ 0.1 OES with z ≥ 3 across hidden worlds, and identification is neither complete at 2 episodes nor absent at 512;
- designed inputs reach a given posterior contraction in at most half the episodes that blind inputs need;
- at a higher level the hidden parameters act through fewer effective parameters than they have, so there is a transferable reduction to discover.

**Gliders on the ladder** (history-only net, `P/round4/sbi/results/summary.json`). R1 is −0.48, 0.35 and about 0.54 at 2, 32 and 512 real episodes. R2 is 0.544. R3 equals the true-parameter net (0.565) from 2 episodes on. So inference is worth 0.021 (0.042 for a ridge), and theory matters only while data are scarce. The experiment step has never been measured: the lab episodes used input programs drawn from the exam's public mix, not designed ones (`P/round4/sbi/run_sbi.py`).

The vortex world has the structure we want: the predictable part of the level-2 kind-share change is carried by one hidden selection coefficient (`P/README.md`, round 3). A micro parameter appears as a macro coefficient. The running vortex exam pilot tests whether that is worth 0.1.

**What the rounds showed about each certificate.**

| certificate | finding | use |
|---|---|---|
| closure ceiling c(h) | a lower bound that moves 0.12 at h = 8 with predictor quality (`P/CRITIQUE.md` §1b). When the map is free it rewards smoothing: across level-2 maps of the block view, c(8) rises 0.31 to 0.84 as retained level-1 content falls from R² 0.82 to 0.33 (`P/track1/learned_phi2/results/summary.json`, `pareto_closure_vs_content`); on raw level 0 the h = 16 ceiling rises 0.16 to 0.55 with the encoder's halo while effective dimension falls 44 to 13 (`P/round4/bias/results/summary.json`, claim 2) | two-sided band gate, one fixed predictor family |
| predictable content (nats) | hand designs lead per number: block mass 275 nats against at most 266 learned (claim 3). Smoothing need not cost content: the designed tent has 282 nats and a higher h = 16 ceiling (checker) | rank within the band |
| agreement with a hand design (R²); seed stability | R² cannot separate block mass from its smoothed version at 0.93-0.96 (checker, claim 0). Closure-type maps are seed-stable to 0.014 in ceiling at one number per block (claim 9) | drop the first; keep the second as a gate |
| input effect | the wind moves the truth by about 0.2 V_best (the best level-1 predictor's error), but learned level-1 predictors recover 44% of it at h = 1 in the object view and nothing in the block view (`P/README.md`, round 4) | measure what a predictor can exploit |
| hidden parameters | given the true state, the prior-mean control loses 0.26 OES (z about 3 across the 4 hidden worlds; `P/track2/gliders_exam/results/summary.json`, checker); history-only predictors lose 0.02-0.09 (sbi) | gate on the history-only gap |

The last row has a structural cause. The gliders prior was shrunk from ±15% to ±9% because 6 of 16 corners failed viability, and 4 of 16 still fail (same file, `viab_joint_*`). Around a hand-tuned point, viability caps how much the hidden parameters can matter.

**New check** (closed form; `R/checks/q1_ceiling_selection*.py`, `.json`). In 4,000 random linear-Gaussian worlds under a fixed random coarse-graining, ranking worlds by c(4) does not pick empty ones: 2% of the top 5% have nothing to predict at 4 ticks, against 68% of all draws. It picks slow ones: median spectral radius 0.97 against 0.60. Taking the best of 200 random maps per world does not lose predictive information either. So here smoothing is a hazard of optimising a free local map, as in rounds 2-4, not of ranking worlds under a fixed map. The foundry should search parameters under a fixed library of designed maps, with a two-sided band.

## 2. Sources of worlds: yield and cost

| source | evidence on yield | verdict |
|---|---|---|
| Hand design by agent collectives | first lab: 7 agents, 8 hours, about 130 world directories, about $605 (`A/REPORT.md`). Collective: 2,389 contributions, 921 CPU-hours, 281 of 400 claims established (`A/collective/STATE.md`, `ledger.json`); suites for four worlds (`A/evals/labworlds/rollout_kit`) | the most expensive source, and the only one so far of division, heredity and selection. Each world is one published, deterministic parameter point (`P/inventory/WORLDS.md` §1) |
| Ports of known systems | vortex and membrane: one CPU study each, round-off agreement with numpy, exact-nats input channels, three levels (`P/README.md`). Gray-Scott, lattice Boltzmann, Potts and particle life are rated trivial to easy (`WORLDS.md` §4) | about one study per world: the best near-term supply, and the calibration worlds |
| Parametrised families with search | ours: only the gliders box above. Lenia: random search found 30 movers in 117,000 trials, goal exploration with gradients 486 in 1,600 (Hamon et al., verified in `P/lit/embodiment_litreview.md`) | the scalable source, at cents per candidate; pass rates unknown until the foundry study reports |
| Training by gradient toward targets | no result of ours; cost unmeasured. Pathwise gradients match finite differences for about one tick in gliders and disagree from four (`V/note/CATEGORY.md` §9) | a repair tool for short-horizon differentiable properties (viability, input response), not a generator of closure bands or level-2 laws |
| Learned coarse-grainings | local closure objectives recover a mass-like variable; nothing learned beats hand designs per number; no bias finds objects; one level-0 theory (`P/round4/bias/results/summary.json`). Cost $0.04 per trained and certified map (166 for $6.01) | auditor, and default proposer for field levels; not yet a source of new kinds of level |
| Composition (stack, product, stride, refine, couple) | closure defects add per time step under independent products and compose by the chain rule; coupling through coarse wires preserves exactness, through micro wires it does not (`CATEGORY.md` Props. 6 and 12). Demonstrated pathwise on gliders (`V/port/compose_demo.py`); no composite has been certified | near-zero cost: the cheapest source of controlled depth, untested where it matters |
| Co-evolution against agents | POET (Wang et al., arXiv:1901.01753) keeps environments neither too easy nor too hard for a paired agent; PAIRED (Dennis et al., NeurIPS 2020, arXiv:2012.02096) maximises regret between two agents. Both VERIFIED (abstract; POET's criterion via secondary sources). Cost: LLM rollouts | adopt the objective, not the loop: ladder gaps are regret between reference solvers and need no LLM. Real agents in the loop would leak instances |

## 3. A world foundry

Measured unit costs: $0.41 per million member-ticks (one ensemble member advanced one tick) at 1,600 per second on an A100 at $2.35 per hour (`P/gpu/bench/README.md`); $3.64 for a simulate-to-train pilot of 5.6M member-ticks (sbi). Before any draw, the family, prior, noise, input channel with exact nats, map library and thresholds are committed. Rates below are the gliders world's; no GPU job has yet run the vortex or membrane worlds (`P/gpu/LEDGER.md`).

| stage | size (member-ticks) | gate | cost |
|---|---|---|---|
| 1 Screen | 10⁴ draws × 2 members × 200 ticks = 4M | finite, alive, not frozen, declared invariants exact, spatial structure | $1.6 |
| 2 Lite certificate | ≤ 10³ worlds × 11k (16 trajectories, 64 branch states); designed maps, ridge-family predictors | c(1) ≥ 0.8; c(h) first below 0.5 between 4 and 64 ticks; content above a random-window baseline; oracle strictly better than level 1 | $4.4 |
| 3 Full certificate | ≤ 50 worlds × 65k, about 10 maps each, including learned ones trained on sibling instances | a seed-stable map in band, ranked by content; input effect ≥ 0.1 V_best within budget at h ≤ 8 for a simulation-trained predictor; unchanged at half the time step | $21 |
| 4 Ladder | ≤ 8 worlds: parameter headroom, identification, simulate-to-train, blind against designed inputs | the definition of section 1 | $37 |
| 5 Freeze | ≤ 2 worlds, 16 truths each, 1.3-3.2M (`gliders_exam` cost model); independent checker; a person watches the videos | checker verdict | $1-3 |

Nominal total: about $70. Round 4 studies simulated at 540-2,700 member-ticks per second, and 24% of the bias study's spend went to two cancelled jobs (`P/round4/bias/results/summary.json`, `P/round4/wind/results/summary.json`). Plan $100-150 per pass: six to ten passes within the remaining $986. GPU money is not the constraint: the runner is serial and every stage needs a checker, so a pass takes five jobs and one to two days.

Search uses cheap predictors on one designer seed; certification uses the full predictor family on another, by another agent. One platform produces everything frozen, because GPU float64 runs are not bit-deterministic (`P/README.md`).

## 4. When a generated world beats a hand-designed one

1. **Exchangeable instances.** A declared prior gives unlimited instances nobody has seen, and held-out families for generalisation claims.
2. **Parameters that matter, by selection.** Stage 4 keeps only families with an inference step of 0.1; gliders has 0.02.
3. **Measured knobs and exact answers.** Horizon, noise, budget and number of levels get a dose-response, and for composites the theory predicts the certificates, so the exam can ask about level-k laws with exact reference values.

Generated worlds will not soon beat hand designs at level 2. Heredity with selection defeated all seven threads of the first lab (`A/REPORT.md` §1.2); the collective's fed vortices later reached it (`WORLDS.md` §2.1). The best hybrid keeps a hand-designed mechanism as skeleton and generates its parametrisation: fed vortices with a neural gain term, or Gray-Scott with a neural reaction term (`WORLDS.md` §4.1).

## 5. Risks

- **Degenerate worlds.** Constant and near-independent levels are closed (`P/track1/DESIGN.md` §5); CIPS is "good but empty" once the box fills (`WORLDS.md` §2.3); a transport NCA without crowding is expected to collapse to point masses (`CRITIQUE.md` §5). Stages 1-2 gate on content and on the oracle gap.
- **Goodhart.** Ceiling alone selects smoothing or slowness. Content alone selects no coarse-graining at all (`DESIGN.md` §5). I expect a ridge-against-net gap to select static nonlinearity, and parameter headroom alone a dial readable from one mean. Mitigations: require every ladder step, not one; never search on the certifying predictor; keep the rubric's rule that a person looks.
- **Leakage through selection.** For a hard gate with pass rate p, KL(prior given acceptance ‖ prior) = log(1/p): 4.6 nats at 1%, and at most log N for the best of N. That is small, and it lies in directions the public gates already state. A search with a public seed leaks the instance entirely. So search seeds belong in the secret, archives are never published, and exam instances are drawn uniformly from the accepted set.
- **Leakage through fitted objects.** A map, predictor or certificate fitted on the hidden instance is a statistic of it (`P/README.md`, hidden set). Publish these at family level only; pilot truths are never reused (sbi, `PILOT_NEVER_REUSE_AS_EXAM`).
- **Training toward what the exam scores.** A trained world satisfies its public loss. Never train toward an examined property unless the target is itself drawn from a hidden prior.

## 6. Five experiments, ranked by value per cost

1. **The ladder on the worlds we have** ($5-20). Rungs R1-R4 and the oracle at levels 1 and 2 for gliders, vortices at 64² and the membrane, including the first comparison of blind against designed inputs. This fixes the fitness function and its noise. If vortices show an inference step ≥ 0.1 at level 2, "hidden parameters must reach a macro coefficient" becomes a foundry rule.
2. **A foundry pass on two families** ($150-300): the running neural-CA family and one skeleton family (vortices with a neural gain term). With a stage-2 pass rate ≥ 1%, use rejection sampling and no search. Below 1%, change the architecture (conservation, crowding) before resorting to search. If no world in either family reaches stage 5, the limit is the exam's observation design, not world supply.
3. **Composition as a generator** (under $10). Six to eight composites of certified parts: coarse-wire against micro-wire coupling, a stacked level, strides 2 and 4. Test whether defects add as Props. 6 and 12 predict, and whether ladder gaps grow with depth.
4. **Validate the fitness against real agents** (API cost; needs the running agent environment). Two or three worlds spanning the range of ladder gaps, and as many agents of different strength. If ladder gaps do not predict agent separation, the definition of section 1 is wrong and must change before scaling.
5. **Gradient repair against selection** ($10-20). Train gliders-family parameters to raise the one-tick wind response per nat under a viability penalty, then rerun stages 2-3. Adopt only if it beats selection on the same statistic at equal cost by a factor of 2 and stays in band.

**Where the running round changes this.**
- A neural-CA pass rate below 1% puts skeleton families first in experiment 2.
- Slot encoders that match the tracker (c(4) = 0.63, `DESIGN.md` E5) and survive fusions remove the main obstacle to object levels. Otherwise the foundry is limited to field levels plus one hand-written tracker per family.
- A learned map that beats hand designs on the two new worlds promotes learned maps from auditor to proposer in stage 3.
