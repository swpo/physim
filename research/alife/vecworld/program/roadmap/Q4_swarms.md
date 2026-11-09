# Q4. How can teams or swarms of agents research this project?

For the lead, 9 Nov 2026. Path prefixes: `P/` = `/home/user/physim/research/alife/vecworld/program/`, `V/` = `/home/user/physim/research/alife/vecworld/vw1/`, `A/` = `/home/user/physim/research/alife/`, `R/` = `/home/user/evalwork/vecworld/program/roadmap/`. One check was made for this memo: `R/checks/q4_collective_sizing.py` (and `.json`), cited as "`q4` check". Thresholds, seats and budgets are proposals.

## Answer in brief

1. We have tried three organisations. The third, this program's rounds, has the best record: 11 studies in two days for $14 of GPU, each recomputed from its saved outputs by an independent checker. Its token cost was not recorded.
2. The ALife collective failed on its contract, not its size: acceptance was a judged rubric, the score paid for large claims, the rules changed 24 times under running sessions, and every fall in its headline score followed an audit by the operator, not a review by a peer.
3. The supervenience program has what ALife lacked: typed artefacts whose acceptance is a program. Accept three types (world family, coarse-graining, exam) through frozen gate programs run on seeds the author has not seen, and keep judgment for reading code and for breaking things.
4. The reason to go beyond rounds is separation of knowledge, not throughput. Today one coordinator session designs worlds, draws truths and would launch contestants. An exam with real secrets needs builders, a sealer and contestants that cannot read each other.
5. Do not launch a swarm. Pilot 10 agent seats for 5 days with $150 of GPU and about $2,000 of tokens, and keep the collective only if it beats the rounds.

## 1. What was tried

| organisation | scale | what worked |
|---|---|---|
| Lab 1, 24 Oct: 7 threads and a committee (`A/CHARTER.md`, `A/REPORT.md`) | 8 hours, about 130 worlds, $605 | judges who re-ran worlds caught a channel bug, a time-step artefact and three sign flips |
| Lab 2, 25-28 Oct: ledger collective (`A/collective/PROTOCOL.md`, `SCORE.md`, gates in `A/RUBRIC.md`) | 64 sessions of about 5.5 hours, 2,389 contributions, 921 CPU-hours | a librarian importing append-only directories (no conflict, two retried pushes: `/home/user/librarian.log`); reviews that must re-run; audits with a deciding control |
| Rounds, 7-9 Nov: memos, a cross-reading (`P/CRITIQUE.md`), then studies each with an independent checker (`P/README.md`) | 11 checked studies, $13.71 of GPU (`P/gpu/LEDGER.md`) | every checker recomputed the results from saved outputs in 2-15 CPU-minutes, and every one corrected the report; at least three changed a result, for example `learned_phi2` (headline gain 0.275 became 0.135 after whitening) and `harness` (a factor-10 slip, one contradicted claim); see the `checker` blocks |

**Where lab 1 failed.** The coordinator that ran the reviews took 64% of spend, and reviews arrived 60-105 minutes into the next sprint. Shared tools were pointed to 9 times and reused 0 times (`A/collective/RETRO_lab1.md`).

**Where lab 2 failed** (`A/evals/labworlds/reports/summary_final.md` §1, §6-7).
- **Lenient review.** 79.9% of verdicts were Supported and 0.8% Contradicted. All 4 falls in reach, the headline score, followed the operator's audits. The check with planted false claims was never switched on.
- **A score that paid for size.** A 5-capability claim added up to 31, five 1-capability worlds 5 (`SCORE.md`). 21 of 52 new established claims carry a capability the code imposes.
- **Moving rules.** The operator changed the rules or the librarian 24 times after launch.
- **Effort without progress.** The last 609 contributions and 343 CPU-hours added no reach. Exploration ended at 0% against a 33% target. The review backlog grew from 13 to 83 as agents left.

**Where the rounds failed.**
- **Two records.** Checker edits live in `summary.json`; three studies note that regenerating the summary would undo them (`P/track2/harness`, `P/track2/wind_recert`, `P/round4/wind`, each `checker` block).
- **Criteria after the fact.** `round4/wind` ran without a declaration, and σ_w was chosen after the band rule could not decide (`P/README.md`, round 3).
- **A shared branch.** Commit 794b516f0, made on a stale index, undid c3328da0f, which carried out a decision of yours on the rollout kit, and deleted another study's scripts. Its author restored them 32 seconds later (11f0953d0); no mechanism caught it.
- **GPU submissions.** 4 of 7 round-4 requests returned nothing: a price cap, a stock-out, slow gradients, out of memory (`P/gpu/LEDGER.md`). Only $1.93 was lost; the cost was time: the benchmark waited 28 minutes for a 4-minute run (`P/gpu/bench/README.md`).
- **State and messages.** The task description for this memo records a container restart mid-round. On disk the running round's files are untracked in two worktrees created at 21:43 on 9 Nov (`/home/user/wt/`), and the lab branch has no commit after 8 Nov. Messages are reliable one way; results return through git (`P/gpu/ack-macbook.txt`).

**Reading.** Agents overstate their own results in every organisation. Checking that recomputes numbers from saved outputs is cheap and reliable. Checking that asks a language model for a verdict is lenient: four of six reviewers supported the ringed rods before the outside audit (`summary_final.md` §4).

## 2. The shared contract

| artefact | type | gate (frozen program, fresh seed) | judged step |
|---|---|---|---|
| world family | `vw.WorldSpec`, a prior, a declared input channel | contract tests (pure, keyed noise, publicly decidable admissibility: `V/note/CATEGORY.md` §9); `invariant_drift`; `nats.kl_check`; envelope and viability at the largest admissible input; a numerics control (half time step, or another platform for a discrete map) | an auditor reads the code for structure the code imposes |
| coarse-graining | `vw.CoarseGrain` on an accepted family | closure ceiling inside a two-sided band under the exam's program mix, with one fixed predictor family; content above a random-window baseline; seed stability (`R/Q1_worlds.md` §3); if learned, trained on prior-predictive data only (`P/track2/EXAM.md` §2) | leak audit |
| exam | `vw.harness.HistoryExam` and a bundle | the six acceptance checks of `EXAM.md` §6.2, with standard errors clustered by hidden world ("truth") | red team |

Theory enters the same way: a proposition with a closed-form check, as in `V/note/checks/`.

**Rules of the contract.**
- **Unseen seeds.** Gate seeds are derived from the merge commit hash (`A/open/DESIGN_draft2.md` §6). The best of 80 equally good configurations scores 2.4 standard errors above its true value (`q4` check), so a fit on one seed is certified on another, as `round4/bias` cross-fitted, and by another agent.
- **Recomputable.** Every headline number recomputes from saved per-item outputs in CPU-minutes, or it is not accepted.
- **One record.** The auditor edits the file every summary is generated from.
- **Frozen per cycle.** Thresholds change only between cycles, by you; the catalogue is then recomputed.

**Caveat.** The gates are unvalidated. The gliders pilot, the only exam run end to end, does not pass the exam checks: identification is finished after two episodes, so the budget does not bind (`P/round4/sbi/results/summary.json`), and actions matter for level-1 nets only at h = 1 (`P/README.md`). Ceilings move 0.12 with predictor quality (`P/CRITIQUE.md` §1b). Expect a second gate version after the pilot.

## 3. Roles, and what each may know

Each seat is its own cloud session and container, not a subagent of the coordinator. That separates compute (lab 1's committee shared 4 cores: `A/REPORT.md` §6.3) and knowledge. A seat is a fixed position, refilled when its session ends. The vault is the private store of sealed weights, secrets and truths.

| role | seats | produces | never sees |
|---|---|---|---|
| world builder | 2 | families: generator, prior, channel | any sealed instance |
| coarse-grainer | 2 | maps for accepted families | hidden-instance data |
| exam builder | 2 | program mix, items, the reference solvers R1-R4 of `R/Q1_worlds.md`, calibrated on pilot instances that are published and never reused | the sealed instance |
| auditor | 2 | `checker` blocks, never on its own lineage | which submissions are planted |
| red team | 1 | leak and shortcut attacks, with a contestant's access | the vault |
| librarian | script | imports, gate runs, catalogue, state page | the vault |
| sealer and grader | script on your Mac, beside the GPU runner | instances, truths, scores | (it holds the vault) |
| contestant | 2 models | predictors | the repository beyond the public bundle |
| operator | your coordinator session | funding within delegated limits, the queue | the vault; it is never a contestant |

**Keeping secrets.** The hidden set is the level-0 weights, a secret of at least 128 bits behind all noise, and the exam instances (`P/README.md`). `V/vw/secret.py` already provides keyed derivation and a publishable commitment.
1. No language-model session holds the weights, secret or truths of a live exam. Builders deliver families; the sealer draws the instance after acceptance (`EXAM.md` §2).
2. Acceptance uses those published pilot instances. The sealed instance gets only pass or fail bits from mechanical checks, each worth at most log(1/p) nats (`R/Q1_worlds.md` §5).
3. The vault is not in git. Job outputs now go to the `gpu-jobs` branch of a public repository, with an unsalted hash of every collected file in the manifest (`origin/gpu-jobs:PROTOCOL.md`; `DESIGN_draft2.md` §11). Sealing needs a private store, salted hashes, and a scanner that rejects any 64-hex string that is not a registered commitment; round-4 checkers did that by hand.
4. One graded submission per contestant per instance, with scores released after the cycle. On a 64-item instance, keeping the best of 10 graded tries can manufacture 0.008-0.027 of apparent skill (0 for climatology, 1 for the oracle); the whole gain from identifying the hidden parameters of gliders is 0.021 (`q4` check). Blum and Hardt ("The Ladder", ICML 2015, PMLR 37:1006-1014; VERIFIED from the abstract) treat the general problem.
5. Seal, contest, reveal against the commitment, retire. Truths are stored, never regenerated: GPU float64 runs are not bit-deterministic (`P/gpu/bench/README.md`).

## 4. Propose, claim, check, merge

1. **Proposal.** A declaration: the artefact, the gate it will face, the deciding control, the result that would kill it, the budget asked.
2. **Lease.** The librarian grants one task per seat; it lapses 2 hours after the last push. Intents are not contributions (they were 41% of lab 2's).
3. **Build** on the seat's own branch and directory, pushing every 30 minutes. Only the librarian writes to the lab branch, and no step waits for a message.
4. **Gate**, run by the librarian.
5. **Audit** by a seat outside the lineage: read the code, recompute with its own code.
6. **Red team** for anything entering an exam.
7. **Catalogue**, and for exams, **seal**.

Leases, merge-hash seeds and planted false claims come from the open-collective draft (`A/open/DESIGN_draft2.md`), which was never run. Its GitHub machinery can wait until a pilot shows the contract works.

**GPU requests** gain two gates: a CPU dry run of two configurations with time and memory recorded (the failures of `r4-bias-001` and `-002` are of the kind it catches), then a GPU smoke run under $1. Requests carry a cap that covers the dearest acceptable GPU type and a fallback list of types. The runner's rules stay: 2 pods at once, and your approval above $25 (`origin/gpu-jobs:PROTOCOL.md`).

## 5. Scoring

All headline numbers describe the catalogue, none an agent.
- **Accepted artefacts**, by family, deduplicated by behaviour.
- **Separation**: gaps between the reference solvers on accepted exams and, after a contest, differences between contestants. Builders cannot move it except by building better exams.
- **Breaks**: confirmed leaks and shortcuts, counted only on artefacts that had passed gate and audit, so each is also an auditor miss.
- **Catch rate** on planted defects, with its interval, and the false-reject rate on clean controls.
- **Cost** per accepted artefact in tokens, GPU dollars and your minutes.

Not scored: contributions, memos, or agreement between reviewers, which rewards herding. Exploration is a quota, not a score: one builder seat in three works on a family with no catalogue entry, and a screened-out family with its pass rate is an entry.

Planted defects come from our own record: the self-pair bias of the v1 energy score, item-level z reported as if clustered by hidden world, a criterion chosen after the run, a map fitted on the hidden instance, a secret left in a results file.

## 6. Budgets, and what you decide

- **Tokens:** a daily cap per seat. At least 40% of the total goes to auditors, red team and contest: review was the main cost of both labs.
- **GPU:** each proposal carries its cap, and the cycle stops at its total.
- **You see** one generated page: catalogue, solver gaps, contest table, open breaks, catch rate, spend against caps, decisions waiting.
- **You decide** gate thresholds and rule versions, seat allocation per cycle, promotion of a family to a sealed exam, disputes between author and auditor, and whether a promoted world looks right on video. Target: 30 minutes a day.

## 7. Pilot

- **Size and time.** 10 seats, 5 days. Day 0: gates as code, vault, state page, 16 planted defects. Two 2-day cycles. Day 5: contest and retrospective.
- **Budget.** GPU $150 of the $986 left. Tokens capped at about $2,000: 10 seats for 5 days at lab 1's $21-42 per researcher session (`A/REPORT.md` §6.2) is $1,050-2,100, plus 12 contestant rollouts (2 models, 3 sealed instances, twice each) at $8-23 (`A/evals/labworlds/rollout_kit/README.md`).
- **First tasks**, starting from whatever the running round has merged.
  - Worlds: a lattice-Boltzmann port as calibration world, and particle life (`P/inventory/WORLDS.md` §4.2, §4.4).
  - Maps: designed maps for vortices and membrane under the exam mix; one composite testing Props. 6 and 12 of `CATEGORY.md`.
  - Exams: the reference solvers and six checks on vortices at level 2; gliders with weight on the level-2 cells that hold 55-89% of its headroom (`R/Q2_difficulty.md` §3).
  - Red team: a reference attacker, and a regression of the weights on public artefacts.
- **It worked if:**
  1. at least 2 families, 4 certified maps and 1 exam passing all six checks are accepted and survive audit and red team (no exam passes today);
  2. at least 14 of 16 planted defects are caught (95% lower bound 0.64) and at most 1 of 6 clean controls is rejected;
  3. no vault material appears in any repository or transcript, and the reference attacker stays within noise of the prior-predictive baseline;
  4. no rule changes inside a cycle;
  5. cost per accepted artefact and your minutes are no worse than the rounds' (measure the running round's token cost for this). Otherwise return to rounds and keep only the sealer and the separated contestants.

## 8. Why this would be different, and what could still fail

Different: gates computed on unseen seeds replace a judged rubric; the false-support rate is measured from day 0; rules are frozen per cycle; seats are fixed and verification is budgeted first; and the terminal score, separation of contestants on sealed instances, is one the builders cannot raise directly.

What could still fail:
- **Shared blind spots.** Auditors and builders are the same model. The catch rate measures this; below two thirds, audit with another model family and keep your outside audits.
- **Insensitive exams.** One 64-item instance has a skill standard error of 0.017-0.027 at item level, and clustering by hidden world widens it 1.2-2 times (`q4` check). Differences of a few hundredths, the size of the inference gaps measured on gliders, need several instances pooled.
- **One Mac.** Runner, vault and grader depend on it being awake.

**Where the running round changes this.** Without a working agent environment, the contest uses reference agents only. A foundry pass rate under 1% moves builder seats from search to ports. If identifying the hidden parameters of vortices is worth nothing at level 2, exam seats go to world building. Slot encoders that survive fusions add object-level maps to the queue.
