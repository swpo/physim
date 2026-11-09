# Q2. What makes an exam hard: levels, coarse-grainings and difficulty

For the lead, 9 Nov 2026. Paths are relative to `research/alife/vecworld/program/`. Three checks made for this memo are in `/home/user/evalwork/vecworld/program/roadmap/checks/` (`q2_*.py`, each with a `.json`; CPU-seconds, no new simulation). New citations are marked VERIFIED (web search this session) or MEMORY.

## 1. Answer in brief

- **The number of levels is not the difficulty.** For each direction in the space of hidden things, difficulty is set by how much the exam's score depends on it (H) and how much the allowed interaction reveals about it at the observed level (I_k). Coarse-grainings shape I_k; the exam's items shape H.
- **The gliders pilot is easy by every measure below.** The hidden parameters are worth 0.02-0.04 of the score. Two episodes, 0.7% of the proposed tick budget, recover them, without using the inputs. The public simulator alone, before any experiment, is worth 24-500 real episodes.
- **This is structural.** With a public simulator and d smooth hidden parameters, regret falls as tr(H I_k⁻¹)/2N: O(d) episodes whatever the levels.
- **Recommendation.** Hide structure, not only values; put exam weight where passive observation is nearly blind and admissible experiments are not; add a hidden level below the public law, with a measured defect. Depth, memory and budgets are secondary.

## 2. Measurable definitions

Scores are OES (0 climatology, 1 oracle; `track2/EXAM.md` §4). Four reference learners, all history-only at the observed level k: **C**, trained on unlimited simulation at the true law; **P0**, trained on prior-predictive simulation, no interaction; **S(N)**, simulate-to-train after N lab episodes; **D(N)**, trained on N lab episodes alone. All four exist for gliders (`round4/sbi`).

| quantity | definition | reads as |
|---|---|---|
| closure gap | 1 − OES(C), per cell | a cap on every level-k observer, not a difficulty |
| headroom H_θ | OES(C) − OES(P0) | what the hidden draw is worth |
| input headroom H_u | OES(C) − OES(C without inputs), on items with inputs | what the port is worth for prediction |
| interaction cost N_90 | least N with S(N) within 0.1 H_θ of C, as a share of budget | difficulty in the narrow sense |
| value of theory V | episodes D needs over episodes S needs, at matched score; also the N at which D(N) reaches P0 | whether theory is the only route |
| information rate | Fisher information about θ per episode at level k (I_k, prior-sd units); passive ticks one charged nat is worth | what the coarse-graining passes |
| stiffness | spectra of I_k and of the pencil (H, I_k) | which directions are cheap, costly or unidentifiable |
| horizon ratio | question horizon / doubling time of twin divergence | whether a cell tests filtering or the law |
| experiment cost | evaluator member-ticks; agent-side simulation | which budget binds |

**The two-matrix model.** For smooth θ, predicting with θ + δ loses ½δᵀHδ of score to second order (H: the exam Hessian). After N episodes the posterior covariance is (Σ₀⁻¹ + N I_k)⁻¹, so

R(N) = ½ tr[H (Σ₀⁻¹ + N I_k)⁻¹] → tr(H I_k⁻¹)/2N, with H_θ ≈ R(0). (*)

When the exam asks what the lab shows, tr(H I_k⁻¹) is of order d: the parametric rate (Clarke-Barron, MEMORY); D learns at a slower, nonparametric rate. The pencil sorts directions:

| | lab information large | small passively, large under admissible experiments | small under every admissible experiment |
|---|---|---|---|
| **exam weight large** | parameter fitting | the scientific regime | unfair |
| **exam weight small** | free | free | free (universality) |

Difficulty worth having is exam weight in the middle cell. I_k is free once an SBI design set exists (`q2_view_information`). H can be read off the amortised θ-conditioned net by finite differences (not yet done).

## 3. What our data say

| measure | gliders pilot (4 hidden parameters, both level-1 views observed) | source |
|---|---|---|
| OES(C): level 1 at h = 1, 2, 4, 8, 16; level 2 at h = 8, 16 | 0.92, 0.84, 0.70, 0.46, 0.23; 0.44, 0.44 (not shown saturated) | `round4/sbi/results/summary.json` (`prediction`, `checker`) |
| H_θ against P0 (against the box centre) | 0.021 net, 0.030 amortised net, 0.042 ridge, truth-cluster z 3.4-5.9 (0.032-0.091) | same |
| share of H_θ in the two level-2 cells | 55%, 86%, 89% (same order); no level-1 cell at h ≤ 4 holds more than 0.009 | `q2_sbi_split.json` |
| the same parameters, given the true state | 0.26 against the box centre (truth-cluster z 3.1) | `track2/gliders_exam/results/summary.json` (`checker`) |
| after 2 episodes (66 ticks, 214 nats charged) | posterior sd / prior sd 0.17-0.44; S(2) within 0.003 of C (net) | sbi (`identification`) |
| V at S(2)'s score; N at which D(N) reaches P0 | ridge about 49, net above 256; ridge about 24 episodes, net about 500 | `q2_sbi_split.json` |
| H_u | inputs move the truth by about 0.2 V_best (block view, h ≤ 4), yet the best block-view predictor is input-blind; the object-view net recovers 44%, 18%, 6% at h = 1, 2, 4 | `round4/wind/README.md` |

Readings:

1. **(*) fits.** The mean squared sd ratio after 2 episodes is 0.125, so (*) predicts a residual of 0.003-0.005. Measured: 0.002 (amortised), 0.003 (net), 0.010 (ridge).
2. **The hidden parameters are a climate property, read passively.** Their headroom sits in the statistical cells; the summaries that identified them are phase-insensitive statistics of the observations alone (`round4/sbi/sbi_lib.py`, `episode_features`).
3. **Partial observation eats most of the sensitivity:** 0.26 given the state, 0.03-0.09 given a history.
4. **The simulator, not the experiment, carries the exam:** P0 matches the data-only net at 512 real episodes (0.544 against 0.545); experiments then add 0.02.

Information per 33-tick episode by view (`q2_view_information.json`: a linear summary model on the study's design episodes; it reproduces the study's 2-episode contraction within 0.08 per parameter; hand-chosen summaries, so lower bounds):

| view | eigenvalues of I_k | nats per episode | episodes to the study's 2-episode contraction |
|---|---|---|---|
| both level-1 views | 33, 11, 3.0, 0.85 | 4.0 | 2.4 |
| block view only (memoryless) | 23, 6.7, 1.7, 0.29 | 3.2 | 5.8 |
| object view only (tracker memory) | 7.3, 1.1, 0.65, 0.07 | 1.7 | 22 |
| five level-2 population statistics | 3.9, 0.59, 0.003, 0.000 | 1.0 | 6,400 |

## 4. How each dial should move difficulty

**Depth (observing level 2 instead of 1).** A higher level shows a lower-rank, worse-conditioned I_k. In the ring toy (four hidden transport parameters, closed form; `q2_ring_difficulty.json`) the sloppiest direction needs 19, 1,020, 14,100 episodes to halve its prior variance for observers at levels 0, 1, 2. In gliders, five level-2 statistics see two of the four directions. But regret follows the pencil: the toy's N_90 is only 58, 128, 198 episodes, because a level-k exam does not weight what level k cannot see. *Prediction:* a level-2 observer asked level-2 questions has N_90 about 12 episodes, 5 times the pilot's, and V below 5: a four-number slow process is easy to fit directly. Depth alone makes the exam more empirical, not harder. It becomes the lever when the exam weights what level 2 hides, such as the population's response to pushes; the rung is then scientific or unfair, depending on what experiments can reveal.

**Memory in the coarse-graining.** For S memory is free: Φ is public code. D's predictor must carry the causal state of the observed process. Our evidence is confounded: the tracker view carries 1.7 nats per episode against the block view's 3.2, yet adding it gives 4.0. In the toy an exponential memory before the port noise leaves N_90 unchanged (119 against 128). *Prediction:* memory moves N_90 only through the views' information ratio, and at least doubles V. Not a primary dial.

**Number and kind of hidden degrees of freedom.** By (*), N_90 grows with the number of directions carrying exam weight, d_stiff; what D needs does not depend on how the law is parametrised. So V falls as 1/d_stiff, to 1 when d_stiff matches the effective dimension of the level-k law.
- 4 → 20 → 261 Flow-Lenia parameters (EXAM §6.3): sloppy spectra (`lit/lit2_probing-depth.md` [16-19]) predict d_stiff ≤ 10 and ≤ 30, hence N_90 ≤ 5 and ≤ 15 episodes at the pilot's half-episode per direction, 5% of the budget at most. What grows is agent compute (the pilot's design set: 0.67M member-ticks).
- A neural law: count stiff directions in function space, not weights (`lit/lit2_critique.md` (d)). That number is the one I most want.
- Discrete structure: (*) does not apply. The cost is log M over the Chernoff information between neighbouring structures (MEMORY), plus search; when structures cannot be enumerated, observed regularities must prune them.

**The input channel.** In the toy a 5-nat aimed pulse adds 2-4% to the Fisher information of a 16-tick episode (a nat is worth about 0.1 passive tick); a pulse well inside a fibre of the observed level (level 2) adds 0.008%. This is fluctuation-response (`lit/lit2_probing-depth.md` [3]): a linear response already shows in spontaneous fluctuations. *Prediction:* inputs change difficulty only where they reach states that fluctuations do not: collisions, thresholds, rare regimes. Test: a hidden parameter acting only at densities reached under regional pushes. Passive SBI should leave its sd ratio above 0.8 at 512 episodes; designed experiments should bring it below 0.4.

**Horizon.** Twin variance doubles every 2.3 ticks in the block view (EXAM §1); ceilings cross 0.5 near 8 ticks. Pointwise cells before that test filtering; statistical cells beyond it test the law. Averaging five of the first with two of the second dilutes H_θ two- to threefold. Report a filtering score and a law score; define difficulty on the latter.

## 5. The central design issue

With a public simulator and few smooth parameters the exam is parameter fitting, and a fixed recipe solves it: our scripted baseline did.

| option | what it changes | verdict |
|---|---|---|
| A. more parameters of the same family | N_90 ∝ d_stiff, slowly; compute grows | a calibration rung; still fitting |
| B. expressive hidden law (neural rule from a public prior) | d_stiff in the tens to hundreds; V falls toward 1 | only in a structured family; otherwise sequence prediction with a useless simulator |
| C. hidden structure (which kernels exist, what they couple, what is conserved) | hypothesis search; difficulty in bits | **primary** |
| D. no simulator | PhySim v1 | an ablation arm: what the simulator is worth to an agent |
| E. budgets alone | squeezes sample efficiency | two episodes cannot be squeezed. A 10,000-tick lab is 6 s of A100 (`gpu/bench/README.md`), so budgets are a free choice: set them last, with the reference's N_90 at 30-70% |
| F. lab-exam shift (regimes, horizons, initial laws the lab cannot sample) | what theory is for; D fails by construction | **yes, with C** |
| G. hidden level below the public law (an inexact refinement; `../vw1/note/CATEGORY.md` Prop. 11) | the public simulator is wrong by a measured closure defect; S is biased (`lit/lit2_probing-depth.md` [23]) and the agent must model the discrepancy | **yes** |

**Recommendation: C + F + G.** The hidden world is a draw from a public grammar of local laws: in Flow-Lenia, which of the 20 kernels are active, their channel wiring, their values. The exam weights transfer items. The true law has a sub-level whose defect η is a dial; η = 0 is a built-in null test (Prop. 11(b): invisible to agents). G is my answer to "how many levels": levels above the agent's view cap what it can know; a level below the public theory makes that theory approximately true, the usual condition of science. Two caveats: all of this is still fitting given unbounded compute, so difficulty is relative to the compute envelope; and an exam that is easy for our scripted baseline may still separate agents (§7).

## 6. Theory that applies

- **System identification, POMDP learning.** Identifiability and informative experiments are the classical frame (Ljung 1999, MEMORY). Learning a partially observed system from data alone is exponential in the worst case, polynomial when observations are revealing (Liu et al. 2022, VERIFIED). Our coarse-grainings are many-to-one by design, so D has no guarantee; the public law makes the task tractable. Without nonsingularity, hidden Markov models are as hard as noisy parity (Mossel-Roch 2006, VERIFIED): hard for D, trivial given the law, useless as science.
- **Computational mechanics, predictive state** (`lit/lit2_emergence-closure.md`; Littman-Sutton-Singh 2001, VERIFIED): statistical complexity is the memory D's predictor must hold; our closure defect is what the micro state predicts beyond it.
- **Sloppy models** (`lit/lit2_probing-depth.md` [16-19, 22]): Fisher spectra span decades, coarse-graining compresses irrelevant directions, complementary experiments restore them. Profile likelihood separates structural from practical non-identifiability (Raue et al. 2009, VERIFIED): the certificate of fairness.

## 7. A difficulty ladder, and what would falsify this account

One dial per rung; substrate, scoring and reference learners fixed; N from 0 to 512; at least 8 truths; truth-clustered errors. A gliders rung costs about one `r4-sbi` job ($3.64); ring-toy versions, CPU-minutes.

| rung | change | prediction |
|---|---|---|
| R0 (done) | 4 parameters, level 1 | N_90 about 2; V 49 to above 256 |
| R1 depth | observe and ask level 2 only | N_90 about 12; V below 5 |
| R2 memory | block view; object view; both | N_90 about 6, 22, 2.4; V at least doubles with the tracker |
| R3 dimension | 20, then 261 parameters | d_stiff ≤ 10, ≤ 30; N_90 ≤ 5, ≤ 15 |
| R4 inputs | passive against designed labs; then a collision-only parameter | sd within 1.2× at R0; designed labs needed for the new parameter |
| R5 structure | hidden kernel subset, 2^k with k = 4, 8, 16 | N_90 linear in k; a design set per structure exceeds 8 GPU-hours (46M member-ticks) by k = 8 |
| R6 sub-level | refinement defect η = 0, small, large | η = 0 reproduces R0; S plateaus below C as η grows |
| R7 shift | exam regimes outside the lab's | D falls to P0 or below on shifted cells; S holds |
| R8 neural law | foundry family | V below 3 if d_stiff exceeds 100 |

Proposed bar for an exam-grade rung: law-score H_θ at least 0.15; reference N_90 at 10-50% of budget; V at least 10; no weighted direction structurally unidentifiable; the scripted SBI baseline under 70% of H_θ inside the compute envelope.

**Falsifiers.**
1. R1 needs over 30 times R0's episodes for the same share of headroom: the information bottleneck governs, not the exam's weighting, and depth is a primary dial.
2. N_90 is flat from 4 to 261 parameters, or V at R8 is still above 50: dimension is not a dial.
3. Passive-only contraction at R0 is over 1.5× worse in sd than mixed: the inputs did matter.
4. A frontier agent with the same tools cannot match the scripted baseline at R0: parameter fitting already discriminates, and the ladder should start lower.

## 8. Where round 6 would change this

- **Difficulty ladder:** its numbers replace §7's predictions, written without seeing them.
- **Foundry (neural-CA family):** gives d_stiff for a neural law. Under 10, option B is no harder than four parameters. If viable worlds are rare, the selection prior carries much of the information (EXAM §2).
- **Vortex exam pilot:** there a level-2 quantity is driven by a hidden selection coefficient (`README.md`, round 3). A law-score H_θ under 0.05 would make reading 2 gliders-specific.
- **Slot encoders, bias map:** a learned object view would make R2 a controlled comparison and might give the first reference learner to capture H_u.
- **Agent-facing environment:** decides falsifier 4.

## References (new to the project record)

- Raue et al., "Structural and practical identifiability analysis … profile likelihood", Bioinformatics 25:1923-1929, 2009. VERIFIED (abstract).
- Liu, Chung, Szepesvári, Jin, "When is partially observable reinforcement learning not scary?", COLT 2022. VERIFIED (abstract).
- Mossel, Roch, "Learning nonsingular phylogenies and hidden Markov models", Ann. Appl. Probab. 16:583-614, 2006. VERIFIED (abstract).
- Littman, Sutton, Singh, "Predictive representations of state", NIPS 2001. VERIFIED (abstract).
- Cited from MEMORY only: Ljung, *System Identification*, 1999; Clarke-Barron 1990; Chernoff information.
