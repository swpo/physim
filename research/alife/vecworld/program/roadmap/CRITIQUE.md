# Second reading of the roadmap memos (Q1-Q4)

For the lead, 9 Nov 2026. `P/` = `/home/user/physim/research/alife/vecworld/program/`, `V/` = `/home/user/physim/research/alife/vecworld/vw1/`, `A/` = `/home/user/physim/research/alife/`. New check: `checks/crit_power.py` (CPU-seconds, on `P/round4/sbi/results/summary.json`, cited below as sbi).

## Verdict

The memos are accurate on nearly every number I recomputed, and Q2 with Q3 answers your second and third questions. They are not yet one programme: three definitions of an acceptable exam, three lists of next worlds and over twenty experiments, all judged by gaps between predictors we wrote. No agent has taken a v2 exam, and no memo owns that risk (section 4).

## 1. Claims the record does not support

- **Vortex level 2** (Q1 §1, Q2 §8, Q4 §7). Q1 calls it "the structure we want", citing `P/README.md`: the predictable kind-share change "is carried by" the hidden selection coefficient. The checked study disagrees. With the true coefficient as a regressor, a linear level-2 predictor explains at most 0.10 of the change, where the oracle shows 0.51-0.56 is predictable (`P/track1/vortex128/results/summary.json`, `decisions.closure_128`). Q3 §2 cites this correctly; Q1, Q2 and Q4 plan around the stale README sentence.
- **"Without using the inputs"** (Q2 §1). The two identifying episodes carried input programs, 214 nats charged (`P/round4/sbi/run_sbi.py`); only the summary statistics ignore them. No passive run exists.
- **"(\*) fits"** (Q2 §3). The model predicts a residual of 0.003-0.005 after two episodes. The measured 0.002-0.003 has a standard error of 0.003 (sbi, `truth_clustered_gaps`), which rejects neither zero nor twice the prediction. Q2's ladder tests (\*) and does not yet rest on it.
- **Thresholds in OES across worlds** (Q1 §1 and §3, Q2 §7). `V/note/CATEGORY.md` Prop. 9(d): oracle-normalised skill "is not comparable across worlds with different base levels". Q1 ranks families by OES gaps; Q2's sub-level rung varies the base level itself. Use a behaviour-level unit, as Q3's theory ratio does.

Recomputed and correct: the gliders numbers, bias claims 0, 2, 3 and 9, the GPU ledger, the lab figures.

## 2. Contradictions between the memos

| issue | positions | reading |
|---|---|---|
| What to generate | Q1: a foundry pass on a neural-CA family, $150-300. Q2: a neural law is "sequence prediction with a useless simulator" unless structured. Q3: composites of textbook parts | defer the neural-CA pass |
| What passes | Q1 §1: the scripted inference step is at least 0.1. Q2 §7: scripted inference captures under 70% of the headroom. Q4: the six checks of `P/track2/EXAM.md` §6.2. Q1's rungs R1-R4 are Q2's D, P0 and S; Q2's R0-R8 are dials | one definition, one notation, before any gate is frozen |
| When inputs matter | Q2 §4: only where they reach states that fluctuations do not. Q3 §3: a push inside one block has 27% of a block push's response where passive correlations predict none | Q3 is right; test with sub-block pushes |
| Is level 0 public? | Q2's option G hides a sub-level, so the public law is wrong. Q1's rung R2, Q3 §5 and Q4's contract assume it is right | G changes the hidden set of `P/README.md`: your decision |

## 3. Missing options

- **The cost of depth** (my estimate). A further field level with block factor b costs b² in area and b² in time (Q3 §3: s = Dτ/b²): 256 times at b = 4. At 128² the block view is 8 × 8, leaving room for one more level of a few numbers. "How many levels" is now a compute question that no memo prices.
- **A priced choice of view.** Let the agent choose, at a charge, which coarse-graining it observes through. Views complement each other: 3.2 and 1.7 nats per episode alone, 4.0 together (Q2 §3).
- **The same agents on v1 and v2 of one world.** Fed vortices and the membrane exist as v1 bundles (`A/evals/labworlds/rollout_kit`) and as v2 levels: the one direct test of what the generalisation bought.

## 4. Do the four add up, and the risk none addresses

Not yet to a test of science. "Interesting", "hard" and "accepted" are all defined on our reference solvers. Agents appear as experiment 4 of 5 (Q1), a falsifier (Q2), a control arm (Q3) and day 5 (Q4).

The deliverable is a frozen predictor, and the hidden world is a draw from a public prior with a public simulator. Training a predictor on simulations from the prior, with no hypothesis and no experiment, then scores 0.545 on gliders, against 0.575 with the true parameters (sbi). Q2 sees this, but its options C and F stay within reach of that policy: a grammar is a public prior over a discrete unknown, and the agent can simulate a shifted regime. Three devices defeat it: a public law that is wrong (G), no simulator (v1), or a simulator too dear to run at exam scale (Q3's compute cap). The third is also why levels matter in natural science; with a cheap micro-simulator, Q2's finding that depth is no dial is expected.

So the agent's compute envelope decides what the exam measures, and no memo sets or prices it. EXAM §5 proposes one GPU for 8 hours: 46M member-ticks, 8 times the whole SBI pilot, at $16-19 per rollout. Q4's 12 contestant rollouts would cost $190-230 of GPU against a pilot budget of $150. Four CPU cores for 24 hours simulate 2.5M member-ticks, half the pilot.

Exam noise is not the obstacle: across the 8 pilot truths, the difference between two solvers varies by 0.009-0.017 per hidden world (0.08 when one ignores the parameters), so three hidden worlds resolve 0.03. The unknown is an agent's run-to-run variance.

## 5. What I would do, in order

1. **Rollouts first.** Two models of different strength on the gliders pilot, three fresh hidden worlds each, in three arms: simulator with GPU, simulator on CPU, no simulator. 18 rollouts, $250-550; log episodes, nats and simulated ticks. If the simulator arms do not order the models, G or a compute cap comes before any new world.
2. **One acceptance definition,** in behaviour-level units, with the compute envelope declared as part of the exam.
3. **Q1's experiment 1** ($5-20), with Q3's sub-block push.
4. **Worlds.** Build Q3's world 1 and clean vortices only; make the first exam-grade world a composite of certified parts under a compute cap (Q1 experiment 3, Q3 §7).
5. **Organisation.** Keep rounds, adding Q4's sealer, single record and criteria declared before the run. Use extra agents as contestants, whose scores are computed, before builders. Defer the 10-seat pilot until one exam has separated two agents.

**Where the running round changes this.** On disk here I find two of its six studies (`/home/user/wt/bias2`, `slots`), not the four the memos lean on. A working agent environment lets item 1 start at once; without one, building it outranks the foundry. A vortex inference step of 0.1 at level 2 withdraws my first objection. If depth proves a primary dial (Q2's falsifier 1), my reading of levels in section 4 is wrong.

## Citation spot-check

Five VERIFIED citations checked by web search; all correct: Mossel-Roch 2006 (with the noisy-parity claim), Brunet-Derrida 1997, Blum-Hardt 2015, Sagawa-Ueda 2010, POET.
