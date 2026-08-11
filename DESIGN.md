# physim — a simulated-universe benchmark for doing science
*(working draft — design discussion, v0)*

## 0. One-sentence goal

Build a verifiers taskset where each task drops the agent into a **procedurally
generated universe with hidden laws**, gives it **instruments and an experiment
budget** instead of direct state access, and rewards it for the **predictive
power of the theories it develops** — with worlds deliberately constructed so
that good science requires *choosing a level of description* and *defining the
right observables*, not just fitting curves.

## 1. Contrast with MazeBench (why this is a different kind of task)

| | MazeBench | physim |
|---|---|---|
| What is hidden | the **state** (unvisited rooms) | the **laws** (dynamics, parameters, structure) |
| Dynamics | known, simple, deterministic, learned in a few steps | unknown; the whole point |
| Epistemic act | exploration of a fixed finite structure | inference + experiment design over an infinite hypothesis space |
| An observation | pins down a room forever | never pins down a law; only reweights hypotheses |
| Reward | state achievement (gems, rooms) | predictive accuracy on held-out interventions (epistemic reward) |
| Determinism | every action repeatable | ground truth deterministic given seed, but *observations* are noisy/partial/costly |

Shared DNA with MazeBench that we keep: procedurally generated task instances
from a seeded family (like maze levels), a real engine as ground truth that the
evaluator can replay deterministically, a small fixed tool surface, long-horizon
multi-turn rollouts, deterministic evaluator-side scoring, and
evaluator-only hidden state (the agent never sees the law, like the agent never
sees board hashes).

## 2. The mental model, made precise-ish

Ground truth: a micro state space `X` with dynamics `Φ_θ` (θ = hidden
parameters/structure sampled per task). The agent **never touches X**. It gets:

- **Preparation knobs** `u ∈ U`: boundary conditions, fields, densities,
  stimulation protocols — the levers of experiment design.
- **Instruments**: functions `m_i: X → ℝ^k + noise`, each with a **cost**,
  **resolution**, **field of view**, and **noise floor**. Raw instruments are
  local and expensive (a "microscope patch"); the agent may *define new derived
  instruments* — named programs over raw channels (its candidate observables).

The hierarchy/coarse-graining idea, formalized loosely: a coarse-graining is a
map `π: X → Y`. It is a *good* observable set iff there exists a macro dynamics
`ψ` with

```
π ∘ Φ ≈ ψ ∘ π        (approximate commuting diagram / approximate closure)
```

i.e. the macro level is **approximately autonomous**: knowing `π(x)` is enough
to predict `π(Φ(x))` up to fluctuations (cf. lumpability of Markov chains,
Koopman observables, computational mechanics / "causal states", Hoel-style
causal emergence). The `≈` is exactly the user's precision tradeoff: macro laws
hold statistically, with finite-N fluctuations, and different definitions of
"the same" quantity have different bias/variance/lawfulness.

**Design invariant #1:** every generated world must *possess* at least one good
coarse-graining with a compactly expressible macro law (that's what makes a
"theory of the collective" exist to be found).

**Design invariant #2:** brute-force micro identification must be *economically
infeasible* (budget), not forbidden. The agent that measures the right order
parameter gets clean laws cheap; the agent that tracks particles drowns in cost
and noise. Coarse-graining is then a discovered strategy, not a rule.

**Design invariant #3 (operationalism):** observables are not god-given. The
environment hands over raw channels; "temperature", "polarization", "force–
velocity curve" exist only if the agent defines estimators for them. Whether an
experiment "works" depends on whether the defined observable is one for which a
closed law exists — Bridgman's point, gamified.

## 3. Prior art (and the gap we aim at)

- **BoxingGym** (arXiv:2501.01540): experimental design + model discovery vs
  generative models. Good scoring ideas (expected information gain, prediction
  error). But observables are handed to the agent and simulators are shallow —
  no emergence, no level-choice.
- **DiscoveryWorld** (arXiv:2406.06769), ScienceWorld: game-like discovery
  worlds; breadth over dynamical depth; observables again pre-defined; the
  "science" is often reading the room, not compressing data.
- **DeepMind Alchemy**: latent causal structure per episode, meta-learning of
  structured hypotheses — good precedent for per-task hidden laws, but a small
  discrete latent space.
- Robot-scientist line (Adam/Eve, AI Feynman, SINDy, symbolic regression
  benchmarks): law-finding from data, but no embodied experiment loop, no
  measurement economics, fixed ontology.

**The gap physim targets:** agent-defined observables + hierarchy with genuine
emergence + measurement cost/precision economics, in a procedurally-generated,
exactly-replayable universe with evaluator-side ground truth.

## 4. World families (each a generator: seed → θ → universe)

Alien-ize everything (random constants, warped functional forms, scrambled
names/units) so pretrained physics knowledge helps with *method*, not answers.

1. **Contractile tissue ("muscle")** — flagship, matches the motivating example.
   Micro: a 2D lattice/network of stochastic contractile units (hidden
   attachment/detachment kinetics, nonlinear elasticity, hidden disorder).
   Knobs: clamp length/force, stimulation rate, bath parameter. Micro
   instrument: expensive small-patch imaging. Macro truth: a Hill-like
   force–velocity/force–length law + hysteresis emerges. The agent should
   invent "tension" and "strain" estimators and find the macro law.
2. **Flocking (Vicsek-like)**: hidden interaction kernel + noise; macro:
   polarization order parameter, density waves, a phase transition. Tests
   whether the agent finds the order parameter and maps the phase diagram.
3. **Spin/lattice world (Ising-ish)**: hidden couplings; macro: magnetization,
   susceptibility, critical point, scaling. Cheap to simulate, rich structure.
4. **Reaction–diffusion (Gray–Scott-ish)**: hidden rates; macro: pattern
   wavelength, front speeds, phase regions in knob space.
5. **Coupled oscillators (Kuramoto-ish)**: hidden coupling/graph; macro: sync
   order parameter, critical coupling.
6. **Tier-0 warmups**: single hidden ODE/SDE (alien damped-driven oscillator,
   logistic-ish growth) — no hierarchy, pure design-of-experiments + fitting;
   calibrates the harness and scoring before emergence enters.

Same-universality-class *sibling worlds* (different micro, same macro law form)
enable transfer tests — the strongest evidence an agent found the *theory*
rather than a lookup table.

## 5. Agent interface (verifiers v1 Toolset, MCP)

Small, fixed tool surface (MazeBench discipline):

- `list_knobs() / list_instruments()` — discover the interface, not the laws.
- `run_experiment(prep: dict, protocol: list, measurements: list) -> data`
  — costs budget: sim ticks + per-measurement cost (resolution- and
  FOV-dependent). Returns tabular/array data + remaining budget. Seeded RNG
  per run; *repeating an identical experiment gives a fresh noise draw*
  (irreducible stochasticity — unlike the maze).
- `define_instrument(name, program)` — a derived observable: a program in a
  restricted, sandboxed expression language (start: whitelisted numpy
  expression DSL) over raw channels. Becomes available in `measurements`.
  This is the operationalization move, and we log it — instrument definitions
  are themselves a research artifact worth studying.
- `notebook_write / notebook_read` — cheap persistent scratch state (long
  horizon support; also gives us a window into the agent's theorizing).
- `submit_theory(predictor_program)` — optional/tiered: an executable predictor
  (sandboxed) mapping (prep, question) → prediction + uncertainty. Enables MDL
  scoring (accuracy − λ·description length) and machine-checkable theories.
- `answer_contract(contract_id, prediction, uncertainty)` — the scored act.

## 6. Scoring (the crux — and the main open problem)

**Primary reward: prediction contracts.** The evaluator issues contracts
phrased **in raw, evaluator-defined terms** ("prepare u=…; predict statistic S
of raw output at t=T, with an interval"), sampled across regimes, including
held-out **extrapolation regions** (other side of a phase boundary, knob ranges
the agent could never afford to probe densely). Score = proper scoring rule
(log-loss / CRPS / interval coverage) against ground-truth ensembles replayed
evaluator-side. Tolerances are set by ground-truth ensemble variance, so
irreducible noise is not punished but resolution-limits bite.

Why evaluator-defined S: if the eval scored the agent's own observables, the
agent defines trivial observables with trivial laws ("my constant is constant")
— degenerate. Instead the agent's ontology is **instrumentally** selected: you
invent "polarization" because it is the thing that makes the contracts
predictable. That mirrors why real definitions survive.

**Secondary metrics (report, maybe lightly reward):**
- calibration (uncertainty honesty),
- budget efficiency (score per unit budget — the economics of coarse-graining),
- MDL of submitted theory programs,
- transfer score on sibling worlds,
- structural discoveries via cheap-to-verify claims ("knob k3 is irrelevant",
  "there is a critical point near u* ∈ [a,b]") checked against θ.

**Anti-gaming rules:**
- contracts issued only after the experiment budget is spent/frozen, or
  interleaved with commit-before-run semantics; no post-hoc oracle queries;
- eval prep configs disjoint from the agent's query history by construction;
- the sim engine runs evaluator-side only (like MazeBench's Node bridge);
  tool metadata must leak nothing about θ (audit like MazeBench's
  "board hashes are evaluator-only" discipline);
- per-task alien parameterization defeats memorization.

## 7. Failure modes to design against

1. **Curve-fitting benchmark in a lab coat**: if contracts are all
   interpolations, symbolic regression on raw data wins without any
   level-choice. Fix: extrapolation contracts across phase boundaries, budget
   pressure, transfer worlds, structural-claim contracts.
2. **Ontology leakage**: instrument names, docstrings, or contract phrasing
   that reveal the intended macro variables ("measure_polarization"). Raw
   channels must be bland (fields, positions, counts).
3. **Reward hacking via the sim**: any path where the agent can run the
   ground-truth engine on eval configs. Strict budget accounting + config
   disjointness + evaluator-side replay.
4. **Noise laundering**: agents dodging hard contracts by claiming huge
   uncertainty everywhere. Proper scoring rules + calibration metrics handle
   this if tolerances come from ground-truth ensembles.
5. **Textbook shortcutting**: recognizable physics lets the model skip
   discovery. Alien-ization; also keep some *deliberately recognizable* worlds
   as a control condition to measure the shortcut's size.

## 8. Implementation sketch (Prime verifiers v1)

- Pure-Python/numpy engines (fast enough for lattice/particle worlds at study
  scale; JAX later if needed). Engine deterministic given (seed, θ, protocol).
- `physim` package layout mirroring the addition/mazebench pattern:
  - `worlds/` — generator families (`family.sample(seed) -> World`), each
    exposing `step`, `raw_channels`, `knobs`, and a `macro_truth` module used
    only by the evaluator for contract construction.
  - `instruments.py` — cost model, noise model, derived-instrument sandbox.
  - `contracts.py` — contract sampler + proper-scoring implementation.
  - `taskset.py` — `PhysimTaskData` (seed, family, budgets, tier),
    `PhysimTask` (rewards = contract scores; metrics = calibration,
    efficiency, transfer), `PhysimTaskset` (infinite, generator-based),
    `PhysimToolset` (tools above).
- Everything in-process Python — no Node bridge needed (simpler than MazeBench).

## 9. Milestones

- **M0 (walking skeleton):** one Tier-0 world (alien damped-driven
  oscillator), tools = `run_experiment` + `answer_contract`, log-loss reward,
  end-to-end `prime eval` run with a stock harness.
- **M1 (economics + operationalism):** budgets, noise/resolution cost model,
  `define_instrument` DSL, notebook; contracts with calibration scoring.
- **M2 (emergence):** contractile-tissue or Vicsek family; micro-patch
  instrument expensive, macro contracts incl. extrapolation across a phase
  boundary; measure whether agents invent order parameters (we can literally
  read their instrument definitions).
- **M3 (theories as artifacts):** `submit_theory` predictor programs, MDL
  scoring, sibling-world transfer tasks.

## 10. Open questions (for discussion)

1. Contract language: how expressive can evaluator-side statistics S be while
   staying ontology-neutral? (moments, spatial spectra, hitting times…?)
2. Should instrument *definitions* ever be directly rewarded (e.g., a bonus if
   an agent-defined observable achieves closure), or strictly instrumental?
   Direct reward risks Goodharting; instrumental-only risks weak signal early.
3. Budget calibus: how to set micro-instrument costs so the coarse-graining
   pressure is real but Tier-2 tasks stay solvable within model context limits?
4. One long rollout per universe (MazeBench-style, 100s of turns) vs episodic
   visits with persistent notebook (closer to a research program)?
5. How much stochasticity? Deterministic micro + noisy instruments vs
   stochastic micro. (Probably both, per family.)
6. Theory representation: free-form predictor programs (MDL-scorable, but
   sandbox complexity) vs structured hypothesis DSL (cleaner scoring, less
   open-ended)?


---

# v0.1 addendum — the raw-port interface ("one layer higher")

## The proposal

Drop all named knobs and instruments. The interface to *every* world is identical and semantics-free:

```
run(U) -> Y      U: [T, n_in] floats in [-1,1]   (input ports)
                 Y: [T, n_out] floats            (output ports)
```

The agent is told only `n_in`, `n_out`, and the budget. Ports are anonymized:
inputs couple into the micro substrate as smooth local fields; outputs are noisy
affine reads of local functionals of micro state, with **random gain, random
sign, random offset, shuffled channel order, and some dead channels**. Before an
agent can do experiments it must first do *sensorimotor science*: find the noise
floor, find dead sensors, learn polarities, discover which outputs co-move,
build its own observables — "learn to use its hands."

## Feasibility probe (done, 2026-02; see conversation log)

Built `RawPortWorld`: hidden 28×28 tanh-lattice with neighbor coupling J=1.3
(collective bistability + hysteresis), 8 anonymous input ports (Gaussian bump
fields), 40 output ports (36 live patch-reads with random sign/gain/offset,
shuffled, + 4 dead), measurement noise. A **scripted naive scientist** knowing
only `run(U)->Y`:

- Stage A (babbling: silence + per-port step probes): dead-channel detection
  4/4 correct; responsiveness map recovered.
- Stage B (body schema): sensor polarity 100% correct via global-drive
  co-movement. Geometry partially recoverable from correlation MDS
  (nearest-pair overlap 35% vs 15% chance) — enough for *neighborhoods*,
  which is all we need.
- Stage C (observable): defined its own macro variable m(Y) = sign-corrected
  normalized mean of live channels — i.e. it *invented magnetization* from
  generic operations.
- Stage D (law): swept its own aggregate drive up/down through m(Y): clean
  hysteresis loop (gap 0.79 vs ~0.00 noise), bistable region located
  (up-jump u≈+0.1, down-jump u≈−0.2). Total ≈1.4e5 channel-ticks.

Key empirical insight: the **first thing** blind correlation analysis finds is
the global collective mode — in an emergent world, the order parameter is the
*most discoverable* structure, while the micro law stays invisible. The
interface hides exactly what we want hidden and surfaces exactly what we want
surfaced.

## Why this is architecturally *better*, not just harder

1. **Ontology-neutrality becomes automatic.** Contracts are phrased in port
   terms ("given input program U*, predict statistic S of channels at t")
   — the v0 worry about leaking ontology through tool/knob names vanishes.
2. **One interface, all worlds.** The port-wiring layer (fields in, affine
   noisy reads out, permutation, dead channels) is a world-agnostic adapter:
   write once, wrap any micro engine. World families reduce to swappable
   dynamical cores.
3. **Alien-ization comes free.** Every task looks identical at the surface;
   wiring is resampled per task instance; no tool names to pattern-match.
4. **Two orthogonal difficulty dials.** Interface opacity (dead channels, gain
   spread, sensor lag/filtering, read nonlinearity) vs law depth (hierarchy,
   phase structure). Tiers: T0 clean ports + shallow law → T3 opaque ports +
   deep hierarchy.

## The two real costs, and their mitigations

- **Design burden → certification burden.** We cannot analytically guarantee
  solvability; instead every generated world must pass an automated
  **reference-scientist battery** at generation time (the scripted Stages A–D
  above, generalized): (i) ports responsive above noise floor, (ii) dead/live
  separable, (iii) scripted generic pipeline finds the macro law within budget
  B_ref. Ship only certified worlds; set agent budget as multiple of B_ref.
  The probe script doubles as the certifier. Also gives a floor baseline for
  scoring ("did the agent beat the dumb scientist?").
- **Context bandwidth.** Raw semantics must not mean raw data through the
  context window. The agent submits *protocol programs* (restricted DSL:
  generate U, reduce Y server-side — means, spectra, thresholds crossings,
  its own defined observables) and gets back small summaries. So
  `define_instrument` survives, now as the compression channel:
  `run_experiment(protocol_program, reducers=[...]) -> summary tables`.
  Sensorimotor bootstrap then costs tens of tool calls, not thousands.

## Accepted degeneracy (feature, not bug)

The agent can never distinguish "sensor convention" from "world property"
(gauge freedom: sign flips, offsets, units). Real physics has the same
property. Contracts are in raw channel terms, so gauge-invariance of the
score is automatic.

## Revised M0

One `RawPortWorld`-style task end-to-end in verifiers: tools =
`run_experiment(protocol, reducers)` + `notebook` + `answer_contract`;
certification battery as part of world generation; contracts = interval
predictions of channel statistics under held-out input programs, incl. one
extrapolation contract (drive regime beyond probed range / other hysteresis
branch). Baselines: (a) random, (b) the scripted reference scientist.


---

# v0.2 addendum — drop the DSL: one interface + agent-implemented tooling

Clarifications agreed in discussion (2026-02):

- `U: [T, n_in]` / `Y: [T, n_out]` is array-shape notation: a 2-D table, rows =
  time ticks, columns = ports. One experiment = submit a U table, receive the
  same-height Y table.
- The "scripted scientist" is ~100 lines of deterministic numpy (no LLM): fixed
  probe schedule (silence → per-port steps → global drives → up/down sweep) and
  fixed analysis formulas. Roles: existence proof, world **certifier**, floor
  **baseline**.

## Interface-only environment (replaces the reducer-DSL idea)

Rather than a bespoke restricted protocol/reducer language, expose the world as
a single dumb endpoint inside an agent sandbox that has a general coding
harness (Claude Code / Codex / mini-swe-agent style):

```
world.run(U: float[T, n_in]) -> Y: float[T, n_out]     # costs budget
world.budget() -> {ticks_left, ...}
world.contracts() / world.answer(contract_id, prediction, interval)
```

The agent writes its **own** tools: probe scripts, analysis code, instrument
functions, notebooks — ordinary files + Python in its sandbox. "Build your own
measuring devices" becomes literal. The DSL design burden disappears; the
context-bandwidth problem disappears (raw Y lives in sandbox files; the model
reduces it with code it writes).

Architecture = MazeBench's two-sandbox pattern: harness+agent in sandbox A;
authoritative world engine (with θ, budget ledger, contract oracle) in process/
sandbox B, reachable ONLY through the endpoint above. Ground truth and budget
accounting never enter the agent's reach. Every U submitted is logged server-
side → full deterministic replay of any rollout.

Consequences:
- The verifiers Toolset shrinks to a thin client (or even just an HTTP spec +
  in-sandbox client file the agent can read).
- The agent's code is a first-class research artifact: its instruments and
  theories are readable Python we can diff across models/worlds.
- Scoring unchanged: contracts in raw port terms, proper scoring rules,
  evaluator-side ensembles.
- Optional later: a no-code MCP-tools tier for comparing harness-less models,
  same worlds. (MazeBench keeps game-only tools for hosted training; we can
  mirror that split.)

Open per earlier + new: budget units (ticks × channels read? per-run overhead
to discourage 1-tick spam?), and whether `submit_theory` = "hand us a .py file
path in your sandbox" (probably yes — evaluator copies + sandboxes it).


---

# v0.3 addendum — interactive worlds: (S,A) -> S', state preparation as a control problem

## The model (user proposal, adopted)

The world is a **persistent process**: hidden micro state S(t) evolves
autonomously; the agent's action A(t) enters the evolution map

    S(t+1) = F(S(t), A(t), noise)      A = 0  =>  ordinary autonomous evolution

The agent NEVER sets S directly (no state surgery). Interventions are physical:
they pass through the dynamics. Observation remains through the port layer
Y(t) = ports(S(t)) + noise. `run(U) -> Y` becomes the open-loop special case
(precommit the whole action sequence; ignore observations while it runs).

Consequence: **state preparation is a control problem and a learnable skill.**
"To study S*, first find actions that steer S(0) -> near S*" — exactly the
user's framing.

## Evidence that closed-loop strictly enlarges reachable science (probes, 2026-02)

Probe on two variants of the bistable lattice world, target = hold the agent's
own macro observable m in a band between the two stable branches:

| world | best constant input | best open-loop ramp/anneal | feedback (PI on m) |
|---|---|---|---|
| local coupling (J=1.3, sigma=0.05) | 100% time-in-band | 57% | 100% |
| mean-field coupling (J=1.8, beta=0.7, sigma=0.02), band around unstable m=0 | **0%** (51 protocols) | **0%** (12 anneal timings; lingers ~0 ticks) | **100%** (holds m≈0.00 for 400 ticks) |

So there exist worlds where a whole region of state space (the unstable
manifold) is **unreachable by any open-loop protocol** but fully accessible
with feedback — the inverted-pendulum / voltage-clamp phenomenon. (Hodgkin–
Huxley needed the clamp: membrane voltages that don't self-sustain become
measurable only under feedback.) Also scientifically meaningful: whether
intermediate states are open-loop-preparable *depends on the coupling
structure* (local pinning vs global winner-take-all) — same surface interface,
different experimental accessibility, discoverable by the agent.

## Resolving the tick-latency problem: policy submission

An LLM cannot sit in the loop at world-tick rate (cost, context, latency).
Resolution consistent with v0.2 (agents implement their own tools): the agent
submits **policy programs** — its own code

    policy(t, Y_t, memory) -> A_t

executed tick-synchronously server-side against the live world, seeing ONLY
measured ports Y_t (never S). `advance(policy_or_U, T, channels) -> reduced
observations` is the single world-stepping call; state persists across calls;
`fresh_sample()` (reset to a new draw of initial conditions) is an explicit
costed action (a new mouse, not ctrl-Z). Writing a *working* controller for a
world you don't yet understand itself requires prior system identification
(signs, gains, lags) — instrument-building now literally includes building
clamps/thermostats, and we can read those artifacts.

## New contract types unlocked

1. **Prediction** (as before): statistics of channels under evaluator-chosen
   input programs.
2. **Preparation**: "bring the world into a state where channels satisfy
   predicate P over window W, then release control; we verify." Verifiable in
   raw port terms; ontology-neutral; = synthesis tasks in real science.
3. **Control**: "keep statistic S in band B for duration T while we inject
   disturbances." (Higher tiers.)

## New difficulty axis: control depth

(a) passive observation suffices (astronomy) → (b) open-loop interventions
needed (chemistry-ish) → (c) closed-loop control needed to reach/hold the
states contracts ask about (experimental biophysics). Certification battery
gains a scripted-controller stage (generic PI on the certifier's own macro
observable — shown above to work); tier label = weakest scripted scientist
that passes.

## Budget note

World time advances only inside `advance()` calls (no wall-clock background
evolution) — keeps determinism, replay, and budget accounting exact while
preserving the "world evolves whether or not you act" semantics (a do-nothing
advance still moves S).


---

# v0.4 addendum — scoring: theories as executable observable-process simulators

## Adopted (user proposal)

The primary scored artifact is an **executable transition model of the
observable process**: a program G, submitted from the agent's sandbox, that the
evaluator runs as a simulator of the ports. This *is* "the theory of the world
as seen through the interface," machine-checkable, MDL-measurable, and
diffable across agents/worlds.

## Three refinements (each backed by a probe on RawPortWorld, 2026-02)

1. **G must be allowed internal state.** Signature not (Y_t, A_t) -> Y_{t+1}
   but `G.init(Y_history) -> h; G.step(h, A_t) -> (h', Y_{t+1})`.
   Ports are partial observations; the observable process need not be Markov
   in Y alone (probe: our world happens to be near-Markov at 36 channels —
   residual 0.077 ~ noise floor 0.05 — but this is world-dependent, and with
   6 channels history already helps: 0.079 -> 0.072). The internal state h the
   agent chooses IS its ontology (its macro variables) — readable artifact.

2. **Uniform sampling in Y-space is ill-posed — evaluate along realizable
   trajectories only.** Probe: uniform draws in the Y bounding box sit far off
   the reachable manifold (median NN-distance 4.33 vs 2.50 for held-out real
   states; 28% farther than 99% of real states; dead channels + inconsistent
   patch overlaps mean most Y-box points correspond to NO micro state).
   Deeper: the evaluator *cannot generate ground truth* at an arbitrary Y —
   you cannot set S to realize a given Y, only run S forward. So the
   evaluation measure must be a distribution over **preparation protocols**
   (action programs run on the true world), never over raw Y-points.

3. **One-step comparison is nearly content-free — score K-step rollouts and
   trajectory functionals.** Probe: persistence (Y'=Y, zero physics) achieves
   96% of the best linear theory's one-step accuracy and *wins outright* in
   quiet regimes. 40-step rollouts separate them (MAE 0.277 vs 0.330 and
   growing with horizon). For stochastic/chaotic worlds pointwise rollout
   comparison fails even for the TRUE law -> score **functionals of
   trajectory windows** (means/vars, spectra, crossing counts, transition
   rates), distribution-to-distribution (truth ensemble vs G ensemble),
   normalized by truth-ensemble spread so irreducible noise isn't punished.

## The evaluation measure ("uniform vs physically interesting" resolved)

Sample protocols from a **published protocol grammar** (constants, steps,
ramps, sweeps, random walks, feedback templates — same primitives the agent
uses), stratified:

- S1 autonomous: A=0 relaxation from fresh initial conditions (baseline
  behavior; cheap sanity stratum).
- S2 interpolation: protocol parameters inside the agent's probed ranges.
- S3 extrapolation: amplitudes/frequencies/durations OUTSIDE anything the
  agent tried (drawn wider by construction; the agent knows the grammar, not
  the draws).
- S4 structure-seeking: protocols steering near discovered structure —
  phase boundaries, both hysteresis branches, unstable manifolds (found by
  the certifier's scripted scientist + controller at generation time; this is
  where "physically interesting" lives, without leaking ontology — they are
  just action programs).
- S5 discrimination (later tier): protocols chosen to maximize disagreement
  among a reference set of theories (persistence, linear fit, scripted
  scientist's fit, agent's G) — Bayesian-experimental-design flavored
  evaluation, concentrates scoring power where theories differ.

Headline score = weighted mean over strata (S3/S4 weighted up), each stratum
= mean over protocols of exp(-error/scale) per functional, scale = truth
ensemble spread. Report per-stratum breakdown always.

## Floors and ceilings (every run reports them)

- Floors: persistence G; random G; scripted scientist's fitted linear G.
- Ceiling: the true engine scored through the same pipeline (its own noise
  ensemble) — defines achievable score given irreducible stochasticity.
- Agent skill = position between floor and ceiling, per stratum.

## Anti-gaming

- G runs sandboxed (no network, CPU/memory/time caps, size cap).
- Eval protocols sampled fresh after G is frozen; agent knows the grammar,
  never the draws.
- MDL (program size + runtime) *reported*, only lightly rewarded if at all —
  a giant learned emulator that survives S3/S4 has genuinely captured
  structure; MDL distinguishes "compressed understanding" in analysis.
- Contracts (v0.2/v0.3 point-prediction + preparation + control) remain as
  cheap intermediate reward shaping and as the harness-less tier; the
  simulator submission is the main event.

## Open

- Distributional distance for stochastic G on functional vectors (energy
  distance / MMD) vs simple per-functional proper scores — start simple.
- Whether S5 uses the agent's own G in the reference set (adaptive, powerful,
  but adds evaluator complexity) — defer to M2+.
- Horizon ladder per world family (K short/medium/long) set by certifier
  mixing-time estimates.


---

# v0.5 addendum — generating hierarchy: motif families x random instances x a closure meter

## Question

Design each world's hierarchy by hand, or generate randomly and filter on a
measured "hierarchy property"?

## Answer: both, with a specific division of labor (probe-backed, 2026-02)

**Blind-random mechanisms don't work.** Probe: three N=400 worlds under an
identical slow random-walk drive:
  A: unstructured random dense tanh network (no designed structure)
  B: local lattice (motif: locality) — the RawPortWorld core
  C: 8 modules, strong intra / weak inter coupling + per-module bias
     (motifs: modularity + heterogeneity)

A generic **closure meter** (PCA rank-k coarse-graining -> fit polynomial
macro dynamics z' = f(z, u) -> held-out tests) measured:

| metric | A random | B lattice | C modular |
|---|---|---|---|
| var captured by k=1 | 0.37 | 1.00 | 0.92 |
| 1-step closure R^2 (k=1) | 0.996 | 0.998 | 0.998 |
| micro-ceiling gap (k=1) | +0.002 | -0.003 | -0.002 |
| **drive-only R^2** (z' from input history alone) | **0.96** | 0.76 | 0.71-0.73 |
| 20-step rollout skill vs persistence | 0.86 | 0.65 (k=1) | 0.75 (k=2 > k=1's 0.56) |

Reading:
- All three "close" at one step — closure alone is NOT the discriminator.
- The discriminator is **drive enslavement**: A's collective mode is ~fully
  explained by recent input history (R^2 0.96) — a filtered echo of the drive,
  no autonomous collective memory, nothing to discover. B and C carry state
  the drive cannot explain (R^2 ~0.75 despite near-perfect closure): that
  residual IS the emergent memory (bistability/hysteresis).
- **Micro-ceiling gap ~ 0** (macro fit as good as the best predictor given the
  FULL micro state) = the coarse-graining is genuinely closed: micro details
  add nothing for predicting the macro future. This is the operational
  pi.Phi ~ psi.pi test.
- The meter reads off **k\*** (number of emergent variables): B is a k=1
  world (k>1 adds only fitting instability); C is k=2+ (rollout skill jumps
  0.56 -> 0.75 from k=1 to k=2 — it detects the meso layer). Hierarchy depth
  is measurable, not just designed.

## Generation pipeline (adopted)

1. **Mechanism families with hierarchy-generating motifs** (intentional):
   locality, modularity, timescale separation, conservation laws, symmetries,
   weak coupling between designed layers. Stat mech says these motifs produce
   emergent low-rank structure; we choose motifs, never hand-tune outcomes.
2. **Random instantiation** (per task): parameters, wiring, disorder, port
   layer, gauge scrambling — sampled from the family's distribution.
3. **Certification by meter battery** (filter): keep an instance iff
   (a) sensorimotor battery passes (v0.1); (b) closure meter finds some small
   k* with: closure R^2 high, micro-ceiling gap ~ 0, drive-only R^2 LOW
   (autonomous memory exists), rollout skill > 0 at horizon ladder;
   (c) scripted-scientist (+ controller, v0.3) cracks it within reference
   budget; (d) micro identification infeasible within agent budget (cost
   accounting). Reject the rest; report acceptance rates per family.

The meter output doubles as the **difficulty label**: dim(Y) = verbosity,
k* = macro complexity, closure R^2 / rollout skill = law cleanness,
drive-only gap = how much genuine memory, plus control depth (v0.3 tiers).
Curriculum = sort published worlds along these axes (user: start easy — high-
dim Y, low k*, clean closure — verify agents rediscover baked-in rules; then
push k* up, closure down, control depth up).

Note: the meter is itself a reference theorist (PCA + poly regression). If it
finds the macro law, the task is solvable-in-principle by an agent that
reinvents generic methods — the same certifier-as-floor logic as v0.1.
Numerics: cubic-feature rollouts blow up at overfit k (seen at k=8) —
production meter needs stabilized regression (stronger ridge, saturating
features, clipped rollouts).

## Status

Design pillars all settled: raw-port interface (v0.1-0.2), interactive
persistent worlds + policy programs (v0.3), simulator-submission scoring with
protocol-measure evaluation (v0.4), motif x random x meter generation (v0.5).
Next: implement M0.


---

# M0 status (2026-02-11)

Implemented at `environments/physim` (verifiers v1, chat tier): engine
(modular tanh lattice, D0-D3 presets), session (JSON protocol commands,
budget ledger, stratified contracts, ensemble scoring with channel-range
scale floor), taskset/env (PhysimEnv drives the interaction loop
engine-authoritatively), scripted baselines (null/tail/reference), report
tooling. First grid (3 models x 4 difficulties x 3 seeds): reward decreases
monotonically with difficulty for competent models (pooled Spearman rho=-0.50,
p=0.003); gemini-3.5-flash matches the scripted reference at D0, no model
beats the reference anywhere; gpt-5-nano ~ null baseline. Full numbers:
REPORT.md. Deferred to M1+: coding-harness tier, policy programs,
preparation/control contracts, simulator submission, meter-certified
generation, per-axis difficulty decomposition.


---

# v0.6 pre-note — M4 direction: deeper hierarchy ("emergent chemistry") [DISCUSSION PENDING]

User proposal (2026-02-11, recorded for the M4 design discussion): current
worlds have ~1-2 reasoning layers (grid -> modes/sources/barriers). The bold
target is a THIRD+ layer: modes as "atoms/molecules" that interact with each
other to form larger structures with their own effective theory — an analogue
of chemistry emerging from what is currently more like bulk material
(gas/metal/glass). Known blocker: lattice size (24x24 - 32x32 is too small for
diverse interacting "species"); expect orders-of-magnitude more sites and a
faster engine (vectorization/JAX) plus port layers that only sparsely sample.
Design challenge: motifs whose collective modes are MOBILE and COMPOSABLE
(localized excitations / solitons / domain-wall bound states) rather than
pinned stripes. To discuss after M2/M3 land. Two axes going forward: making
models do better on existing worlds, and making ever more complex worlds.
