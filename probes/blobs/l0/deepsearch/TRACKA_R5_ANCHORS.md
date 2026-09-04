=============================================================================
TRACK A ROUND-5 RESPEC v2.1: category-anchored contracts, closed-book reveal
("BLOB2-v2" — spec step, 2026-09-04; elaborates R5_BRIEF.md as revised by
 R5_BRIEF2.md: the v2.0 draft's fork-oracle acceptance is SUPERSEDED by
 two-phase closed-book episodes; keeps the round-2 contract FAMILIES of
 TRACKA_CLEANSLATE_EVAL.md; the round-4 numbers freeze as the v1 row and
 are never mixed with v2 rows)
=============================================================================

DECISIONS AT A GLANCE (agreed; this doc elaborates, does not relitigate.
 Numbered decisions 1-3 cite R5_BRIEF2 user decisions; lettered (a)-(c)
 cite R5_BRIEF.)
 v1 (BLOB2-E1/E2, round 4)              v2 (BLOB2v2-E1/E2, round 5)
 ---------------------------------      -----------------------------------
 BUDGETS bind + advertised              SAFETY CAPS only (~25-33x), silent,
   (sensor 40000 / adjust 1200 /          target hit rate exactly 0
    injection 120, steep pricing)
 budget/cost/remaining in status,       TRACK DON'T TELL: zero cost language
   tool returns, refusal coaching         anywhere agent-visible; everything
                                          metered silently -> per-rollout log
                                          -> post-hoc Pareto (skill v spend)
 uniform T0=1700 span + hard stop       ANCHORS: base line fully observable;
   + LOCK_AT_INJECT                       instance anchors drawn CONTINUOUS
                                          from published domains; no locks
 contract menu = concrete instances     KNOWN CATEGORIES, HIDDEN INSTANCES:
   announced at t=0                       the syllabus publishes per tier the
                                          payload schema, the ladder rungs,
                                          and the instance-sampling DOMAIN
                                          (ranges, never values)
 world open until episode end           CLOSED-BOOK REVEAL: agent-triggered
                                          probe_ready() reveals the concrete
                                          instances and closes ALL world
                                          access; answers come from the
                                          agent's own artifacts (notes,
                                          fitted models, its own code)
 replicas: 12 forks from T0 only        exploration forks from ANY anchor,
                                          inject/read/adjust inside, reset
                                          free; never scored; Phase A only
 truth = the one cached realization     truth = fresh replica ENSEMBLE per
   (same historic noise stream)           instance spec, salted noise
                                          streams, built at reveal, frozen
                                          per (world, seed, instance)
 agent-authored contracts: n/a          still OUT (L6 executable-theory
                                          lane; difficulty-normalization
                                          open problem noted, not solved)

PART 1 — MOTIVATION
Round 4 measured the budgets doing what budgets do: binding. Injection
spend fractions 0.74/0.95/0.70 (E1) and 0.58/0.45/0.81 (E2); the replica
cap 12/12 saturated in 4 of 6 rollouts (probes/blobs/agentenv/round4/
ROUND4_FINAL.md rollouts). A binding budget conditions the score: the
headline number confounds "best science" with "thrifty science" at an
exchange rate we never chose or published. We want the score to measure
understanding; economy is real but it is a SEPARATE axis — measured,
logged, and read off a Pareto frontier after the fact, never priced into
reward and never used to coach the agent mid-episode. (Same logic as token
caps on LLM evals: the cap exists so a runaway costs bounded compute, and
any run that touches it is an invalid measurement, not a graded outcome.)

The second flaw is the span itself. T0=1700 is an arbitrary constant that
round 2 baked into every contract ("at the end of the span"), and the
LOCK_AT_INJECT machinery (blobround2.py) exists only because agent replicas
and contract truth shared that single anchor on the same historic noise
stream — an amp=0 control replica literally replayed the P1/L3 truth, so
forecasts had to lock before the first inject. But a conditioning point is
a PARAMETER of a contract, not a property of the world: one can fork from
t=0, from step T, from anywhere. Round 5 makes the anchor explicit per
contract instance, makes truth a fresh-stream ensemble that no agent fork
can replay, and deletes the lock and the preamble constant with it.

The third flaw surfaced only while drafting v2.0: with concrete instances
announced up front and a world that stays open, free forking turns short-
horizon legs into simulation-execution tests (the "fork oracle": fork at
the scored anchor, run the protocol, ensemble the samples). The v2.0
draft accepted that as an owned consequence. The user chose a stronger
design instead — publish the CATEGORY, hide the INSTANCE, close the world
before the questions become concrete. Exploration cannot rehearse answers
(instances unknown behind effectively-continuous domains) and answering
cannot touch the world (closed book). What survives the reveal is exactly
what the benchmark wants to measure: the portable artifact — notes,
fitted models, the agent's own runnable simulator — an explicit bridge
toward the L6 executable-theory lane.

PART 2 — NEW PRIMITIVES AND THE AGENT-FACING SURFACE

2.1 Two-phase episode (the defining v2 mechanic)
 PHASE A — EXPLORATION (t=0 until the agent calls probe_ready).
   Visible from t=0: the SYLLABUS (2.3) — per tier the payload schema,
   the scoring-ladder rungs, and the published INSTANCE-SAMPLING DOMAIN
   (ranges, never values). The concrete instances stay hidden. World
   access is fully open: base-record reads, forks from any anchor,
   adjusts and injections inside forks, free resets — R5_BRIEF decisions
   (a)/(b) unchanged: no announced meters, silent safety caps only.
   Fork-ensembling in Phase A is legitimate and USELESS for rehearsal:
   the instances are unknown, and every tier keeps at least one
   effectively-continuous hidden dimension, so pre-computing answers over
   the domain is hopeless by construction — and visibly so, because the
   syllabus states continuous sampling explicitly (decision 2).
 THE REVEAL — agent-triggered ONLY: probe_ready(). There is NO fixed
   reveal time: a set time is another cap that makes agents worry about
   the clock while they work. The only exploration ceiling is the
   generous silent live-sim safety cap (2.7), never surfaced, target hit
   rate 0. probe_ready is irreversible and returns the concrete instance
   menu (ids, anchors, protocols, observables, payload shapes).
 PHASE B — CLOSED BOOK (reveal until episode end). ALL world access
   closes: probe_read/wait/adjust/fork/reset/inject return a generic
   phase error; probe_status and probe_submit remain. The agent answers
   from its theory artifacts — notes, fitted models, ITS OWN code and
   simulators run in the harness (bash/python stay fully allowed; only
   the world itself is closed, base-record re-reads included). If the
   agent wants the record after the reveal, the record must already live
   in its notes/files. Submissions stay revisable until episode end;
   unsubmitted = -1 unchanged. An episode that never calls probe_ready
   scores every instance -1 (unchanged rule: unsubmitted is unscored).
 WHAT THIS SCORES: the portable artifact built during exploration —
   theory that runs without the instrument (the L6 bridge).

2.2 Anchors, forks, instances (evaluator-side model)
 ANCHOR    (line, t): a state the world can be forked from. Scored-
           instance anchors live on the BASE LINE (the cached (world,
           seed) trajectory, t in [0, T_BASE=2500]) — see PART 7 Q2 for
           fork-state anchors (deferred). Instance anchor times are drawn
           uniform-CONTINUOUS from the published domain and realized at
           sim-step resolution by deterministic replay from the nearest
           cached checkpoint (2.6): the 5tu control grid is a READ grid,
           not a state grid. Agent forks anchor on the read grid, so an
           instance anchor is off-grid with probability 1 — one more
           continuous gap between rehearsal and the graded draw. Anchors
           fix WORLD state only; device poses are agent instrument state
           and travel with the agent, never with the anchor.
 EXPLORATION FORK  (Phase A only) agent-spawned via probe_fork from any
           base-line grid t (or from another fork's current state —
           hash-id). Runs LIVE forward under agent control: read/adjust/
           inject freely. Never scored, discardable (reset = discard,
           free). Fork noise streams are salted per (rollout nonce, fork
           counter): a fork is a fresh realization from the anchor, never
           a replay of the base line's continuation and never equal to
           any truth member. In v2.1 this stream separation is belt-and-
           braces: the primary rehearsal barrier is that the instances
           themselves are hidden behind continuous domains until the
           world is closed.
 SCORED INSTANCE   harness-issued, fixed per (world, seed) for cross-
           agent comparability (hash-drawn from the published domains,
           blobround2 _rng pattern, salt "r5_instances_v1"); HIDDEN from
           the agent until probe_ready. instance = (tier, anchor,
           protocol, observable, horizons); protocol = undisturbed | one
           hidden command sequence | one hidden emission (port, amp,
           dur). Truth = a fresh replica ensemble from exactly that spec
           (2.6). All values EXPLICIT at reveal; ids = family tags
           ("L3F@i1"). Before the reveal the agent sees only category +
           domain (2.3).

2.3 The syllabus (the published Phase-A contract text)
Published in full at t=0 (system prompt; repeated by probe_status). Per
tier: the payload schema, the ladder RUNGS it is scored against (names
only, never numbers — the numbers depend on the hidden anchor), and the
instance-sampling DOMAIN, stating continuous sampling explicitly
(decision 2: the infeasibility of rehearsal must be VISIBLE, so rational
agents do not attempt it). The E1 text below is normative wording,
verbatim; <angle> constants are category facts filled per (world, seed)
— instance-independent by the reveal-leak audit (PART 6 step 3).
 ---- BEGIN SYLLABUS (E1) ----
 SYLLABUS — BLOB2v2-E1 (the only contract text before the reveal)
 This episode has two phases. NOW (exploration): probe_read / probe_wait /
 probe_adjust / probe_fork / probe_reset / probe_inject are open on the
 base record and on your forks. WHEN YOU CALL probe_ready(): the six
 instances below are revealed with concrete values, every world tool
 closes for the rest of the episode, and probe_submit opens. Everything
 outside the world (your notes, files, code) stays available. Submit
 {"mean","sigma"} arrays of the stated shape per instance; resubmission
 allowed, last accepted wins; unsubmitted instances score -1.
 Scoring per instance: skill = 1 - CRPS/CRPS_ref, clipped to [-1, 1],
 where CRPS_ref is the best of the stated reference forecasts ("ladder"),
 fit to pre-anchor base-record data; reward = mean over the six.
 Hidden instance parameters are sampled once per episode from the stated
 domains and revealed all at once at probe_ready(). CONTINUOUS means any
 real value in the range — do not expect grid values. tu = time units of
 the base record, which spans [0, 2500].
  L1  apparatus response. At a hidden anchor a fresh fork is taken and a
      hidden command sequence is applied to device 0 (from its t=0
      configuration); predict device 0's reading right after the final
      command. domain: anchor t_a continuous-uniform in [600, 2300];
      sequence length in {1, 2, 3}; each command u in [-1, 1]^3,
      components continuous, one control step each; only sequences the
      apparatus accepts are drawn. payload: [ports][slots of device 0].
      ladder: climatology | persistence.
  L2  hidden-sensor nowcast. One additional fixed sensor cluster of 13
      slots reports the same ports; predict its reading vector at a
      hidden anchor. domain: t_a continuous-uniform in [600, 2300].
      payload: [ports][13]. ladder: global climatology | global
      persistence.
  L3F forecast. Predict device i's streams (t=0 configuration) at every
      horizon H in {5, 25, 100, 400} tu after a hidden anchor,
      undisturbed. domain: device i uniform over your devices {0, 1};
      t_a continuous-uniform in [600, 2300]. payload:
      [4][ports][slots of device i]. ladder: climatology | persistence
      | AR(2).
  L3E event rate. Predict the crossing count of the announced event
      (port <p2_port>, sign <p2_sign>, threshold <p2_thr>) in each of 16
      consecutive 50tu windows starting at a hidden anchor, undisturbed;
      windows may extend past the base record. domain: t_a continuous-
      uniform in [600, 2300]. payload: [16]. ladder: zero-rate |
      pre-anchor rate.
  L4  emission response, beyond the apparatus range. At a hidden anchor a
      fresh fork is taken and one hidden emission is driven through the
      same emitter probe_inject uses; predict device 1's streams (t=0
      configuration) at lags {10, 25, 50, 100, 175, 250} tu from emission
      start. domain: t_a continuous-uniform in [600, 2300]; port uniform
      over the ports; amp continuous-uniform in [1.5, 3.0] (your
      apparatus stops at 1.0); dur continuous-uniform in [5, 20] tu.
      payload: [6][ports][slots of device 1]. ladder: climatology |
      persistence.
  L4D emission response, inside the apparatus range. Same protocol shape
      as L4. domain: t_a continuous-uniform in [600, 2300]; port uniform
      over the ports; amp continuous-uniform in [0.30, 0.90]; dur
      continuous-uniform in [5, 20] tu; lags {25, 75, 150} tu. payload:
      [3][ports][slots of device 1]. ladder: climatology | persistence.
 ---- END SYLLABUS ----
E2 deltas: L3F horizons {25, 100, 400}, payload [3][...]; L3E replaced by
L3S — predict the per-port global mean and variance (the free aggregate
stream) averaged over the 200tu windows ending at t_a+400 and t_a+800,
undisturbed, payload [2][ports][2] with [.,.,0]=mean [.,.,1]=variance,
ladder: windowed climatology | windowed persistence; all domains
identical to E1's.

2.4 The base line
The v1 hard stop at T0 is DELETED. In Phase A the base line is observable
on the full cached span [0, T_BASE]; the read head stays monotone (replay
honesty); probe_fork gives random access to any grid t. Injection is NOT
allowed on the base line (it is the immutable historical record);
injection happens inside forks. Rationale for full observability: v1 hid
(T0, 2500] because truth WAS the cache continuation; v2 truth is a fresh-
stream ensemble, so the base line's own continuation is just one more
(historic) realization — legitimate conditioning data, not the answer
key. In Phase B the base line closes with everything else (decision 3: NO
world access post-reveal, base-record re-reads included).

2.5 Tools (probe_ prefix; servers/blob.py rewrite)
Phase column: [A] exploration only (in Phase B: generic phase error);
[B] reveal onward (in Phase A: generic phase error); [A+B] always.
 probe_status()   [A+B]  t_base_head, T_BASE, phase (exploration |
                       revealed), contexts (open forks: id, anchor,
                       t_now), interface counts (n_devices, ports,
                       slots_per_device, n_actuator_channels), apparatus
                       caps (amp/dur/u ranges), and the SYLLABUS (2.3).
                       After the reveal: plus the concrete instance menu
                       (id, anchor, protocol, observable statistic,
                       horizons/lags, payload shape) and per-instance
                       submitted flags.
                       REMOVED: budget dict, costs dict, pricing strings,
                       replicas_left, lock state, every "unspent/afford"
                       note — and every pre-reveal instance datum.
 probe_read(ctx, window, devices, ports, stride)   [A]  read streams in
                       context ctx ("base" | fork id). window=0 reads the
                       current state without advancing. Base reads replay
                       the cache; fork reads advance the live sim. Free
                       per-port global mean/var included as in v1.
 probe_wait(ctx, steps)   [A]  advance without reading.
 probe_adjust(ctx, device, u1, u2, u3, steps, read)   [A]  the R3-final
                       opaque actuator, unchanged semantics (fixed
                       undocumented global map, commanded-effort strain,
                       generic "adjust_rejected"); legal in ANY Phase-A
                       context — poses are per-context, forks inherit the
                       spawning context's poses.
 probe_fork(line, t | fork)   [A]  spawn an exploration fork from a base-
                       line grid t or from a fork's current state.
                       Returns fork id (hash).
 probe_reset(fork)   [A]  discard a fork. Free, always allowed in
                       Phase A.
 probe_inject(ctx, port, amp, dur)   [A]  drive the fixed emission
                       channel inside fork ctx starting at its current
                       time. Apparatus constraints KEPT and announced:
                       amp = 0 or in [0.05, 1.0] (AMP_CAP — the
                       calibrated-regime task definition), dur in (0, 50]
                       tu. Refusal text states the apparatus limit only.
                       The v1 lags/read bundling is gone: injection is an
                       action in a fork; reading is probe_read.
 probe_ready()   [A->B]  irreversible; ends exploration, opens the
                       envelope: returns the revealed instance menu (as
                       probe_status thereafter) and closes every world
                       tool. Draws nothing at call time — instances were
                       fixed at build. No fixed reveal time exists and no
                       exploration deadline besides the silent live-sim
                       safety cap (2.7).
 probe_submit(instance, payload)   [B]  unchanged mechanics ({"mean",
                       "sigma"} shape-checked, last accepted wins, scored
                       at episode end). Open from reveal to episode end;
                       NO locks. Before the reveal there is nothing
                       addressable to submit to (phase error).
Message-size guard (60000 numbers per response) stays — it is transport
plumbing, phrased without cost language ("response too large; narrow the
read").

2.6 Truth generation (evaluator-side)
Truth for instance (anchor, protocol, observable, horizon) = an ensemble
of n_truth live replicas forked from the anchor state, each running the
protocol with an independent salted noise stream:
  member stream salt = ("truth", world, seed, instance_id, m)
  agent fork salt    = ("fork", rollout_nonce, fork_counter)
Domain separation is mandatory (2.2). Continuous anchors: the anchor
state is realized by deterministic replay from the nearest cached
checkpoint to the exact sim-step anchor time. Ensembles are BUILT AT
REVEAL: the first reveal for a (world, seed) builds and freezes the truth
tensors (round5/ cache namespace, same pattern as the round-2 L4D dose
cache); every later rollout is scored against the identical frozen
members. Prebuilding at registry-build time is an equivalent optimization
(nothing in the build depends on rollout events); the binding rule is
frozen-once, keyed (world, seed, instance). Build hardware (CPU f32
default; the batched GPU stepper in probes/blobs/gpu is admissible)
matters only at build time. Degenerate cases: the base realization is
well-defined at any sim step via the same deterministic replay and MAY
serve as single-member truth where replay==live holds at A0 tolerance
(4.6e-4): L1 (adjust-only forks do not disturb the world), L2 (horizon
0), and undisturbed legs with horizon <= 25tu. Every longer leg and every
emission protocol uses the fresh ensemble.

2.7 Safety caps (silent) and meters
Caps exist ONLY as runaway protection; they are sized ~25-33x the v1
budgets so that no competent strategy ever meets one (target hit rate:
exactly 0; see PART 6 monitoring). They are NOT announced, NOT returned
by any tool, and a cap refusal is generic ("the apparatus refuses"): no
cost number, no remaining amount, no cheaper-tool coaching (the v1
"budget too low ... use probe_wait" class of message is deleted). Per
decision 1 the live-sim cap doubles as the ONLY exploration ceiling —
there is no reveal deadline to worry about while working.
 meter                unit                v1 bound        v2 safety cap
 sensor               node-tu             40000 (budget)  1,000,000
 adjust               commanded cu        1200  (budget)  30,000
 injection            amp-tu, v1 price    120   (budget)  3,000
                      fn amp*(1+4*max(0,amp-0.5)) — kept as the METER for
                      cross-round log continuity; visibility changes, the
                      logged unit does not
 fork spawns          count               12 (replicas)   400
 open forks           count (memory)      n/a             8 concurrent
 live sim             tu simulated        3000 implicit   100,000
 resets               count               n/a             uncapped (free)
 time-to-ready        sim_tu + turns at   n/a             NONE (meter
                      probe_ready                         only, never a
                                                          cap)
All meters (spend_sensor / spend_adjust / spend_injection, n_forks,
n_resets, sim_tu, per-context read counts, turns, and t_ready — the
time-to-ready Pareto axis, decision 1) are logged per rollout into the
results json and surfaced as trace metrics; the report layer draws the
skill-vs-spend Pareto frontier per meter. No reward term, no partial
credit for thrift or for early readiness: efficiency is analysis, not
conditioning.

PART 3 — SCORING (formula unchanged; inputs re-derived)
Per instance:  skill = clip(1 - CRPS_agent / CRPS_best_rung, -1, +1)
Unsubmitted instances score -1. Rollout reward = MEAN skill over the menu.
This is verbatim the round-2 rule (blobround2.py _skill / score_episode2);
nothing about the formula, the -1 floor, or the mean changes (but see
PART 7 Q5 for a deferred rethink of the normalization itself).
What changes underneath:
 TRUTH   per instance spec (2.6): built at reveal, frozen per (world,
         seed, instance). CRPS_agent = mean over truth members of
         CRPS(agent's gaussian, member) — an unbiased estimate of the
         expected CRPS under the world's own predictive distribution.
         Members are frozen, so every agent is scored against the same
         draws (paired comparisons; estimator noise cancels in rankings).
 LADDER  climatology / persistence / AR(2)-where-applicable, recomputed
         PER INSTANCE from full-rate pre-anchor base-line history
         (backtest sigmas ending at the anchor; estimators pose- and
         instance-ignorant). This is exactly the pre-reveal base record
         any agent could have kept: the rungs are category-generic, use
         no hidden information, and stay classical — the floor is fair on
         both sides of the reveal. The domain lower bound t_a >= 600
         exists to guarantee the AR(2) rung its backtest history (the
         folded Q1). CRPS_best_rung = min over the ladder, per instance.
 FLOORS  all floor tables re-derived (PART 6); v1 floors are meaningless
         for v2 instances.
THE FORK ORACLE IS DEAD BY CONSTRUCTION. Phase A: instances are unknown,
and every tier keeps >=1 effectively-continuous hidden dimension (anchor
t_a, command u-values, emission port/amp/dur), so fork work can calibrate
LAWS but cannot rehearse ANSWERS — gridding a domain is hopeless (PART 6
step 4 documents per-tier cardinality) and visibly so (the syllabus
states continuous sampling), so a rational agent does not attempt it.
Phase B: the lab is closed; nothing can be run against the world at the
revealed parameters. Consequences: the v2.0 flags dissolve. E1's L3F H=5
leg is UN-FLAGGED and meaningful again — it now prices short-horizon
modeling plus record-keeping (in the deterministic regime its ceiling is
near-aleatoric for any agent that kept the base record; that is by
design: Phase B makes "did you keep the record" a scored capability).
L4D stops drifting toward execution+interpolation: Phase-A dose sweeps
remain legitimate law CALIBRATION, but the graded (port, amp, dur, t_a)
cannot be executed. Discriminative margin concentrates where v2 wants it:
spatial modeling (L2), actuator law (L1), dose law inside and beyond the
apparatus range (L4D/L4), and honest long-horizon calibration
(L3F/L3E/L3S).

PART 4 — TIER MAPPING v1 -> v2.1 (families survive; instances hidden)
Per family: what v1 announced at T0, what v2.1 hides per instance, and
the domain the syllabus publishes (2.3 — normative wording there).
Anchors: every family draws its own t_a uniform-continuous in [600, 2300]
(independent draws; the v2.0 shared-anchor-set policy went with Q1).
Payloads are {"mean","sigma"} pairs of the shapes below.
 L1   v1: K=3 ANNOUNCED command sequences from span end; truth = cache at
      the walked pose; locked at inject.
      v2.1 hidden: t_a + ONE sequence (length, per-step u). published
      domain: length in {1,2,3}; u in [-1,1]^3 per step, components
      continuous, one control step each; apparatus-acceptable sequences
      only. payload (ports, kA) — the K axis is gone with the
      announcement. change: the sequence is no longer given in advance,
      so L1 now prices the actuator LAW (learn it in Phase A, execute it
      offline in Phase B); truth stays single-member (2.6: adjust-only
      forks do not disturb the world).
 L2   v1: hidden-sensor nowcast at T0; locked.
      v2.1 hidden: t_a. published domain: t_a only; 13 slots, same ports
      as always. payload (ports, 13). change: anchor only; the hidden
      device stays fixed per (world, seed); single-member truth
      (horizon 0).
 L3F  v1: device 0, horizons 5/25/100/400 (E1) / 25/100/400 (E2) from
      T0; locked.
      v2.1 hidden: t_a + device index i. published domain: i uniform over
      the roster {0, 1}; full horizon set scored. payload (nH, ports,
      k_i). change: device ambiguity added ("what will be measured");
      H=5 un-flagged (PART 3); ensemble truth for H > 25.
 L3E  v1: 16 x 50tu crossing-count windows over (T0, 2500]; locked (E1
      menu).
      v2.1 hidden: t_a. published domain: same statistic, 16 consecutive
      50tu windows from t_a; windows may extend past T_BASE (live
      ensemble truth, not cache-capped). payload (16,).
 L3S  v1: global mean/var over 200tu windows ending T0+400/T0+800; locked
      (E2 menu).
      v2.1 hidden: t_a. published domain: same windows, ending t_a+400
      and t_a+800. payload (2, ports, 2).
 L4   v1: announced amp-3.0/10tu emission at T0 on the announced port; 6
      lags, device-1 streams; open.
      v2.1 hidden: t_a + port + amp + dur. published domain: port uniform
      over the ports; amp uniform-continuous in [1.5, 3.0] — the WHOLE
      domain sits above AMP_CAP=1.0, so the graded protocol is never
      runnable even in Phase A: extrapolation stands as a RANGE, not a
      point; dur uniform-continuous in [5, 20]tu; lags {10, 25, 50, 100,
      175, 250} fixed. payload (6, ports, kB).
 L4D  v1: announced dose grid .30/.45/.60/.75/.90 x 3 lags; secret amp
      U[0.3, 0.9] per (world, seed); agent submits a TABLE over the grid,
      scored by interpolation at the drawn amp; open.
      v2.1 hidden: t_a + port + amp + dur. published domain: amp uniform-
      continuous in [0.30, 0.90] (inside the calibrated range); port and
      dur as L4; lags {25, 75, 150} fixed. payload (3, ports, kB) — a
      DIRECT prediction at the revealed instance; the grid/table/
      interpolation machinery is DELETED. The v1 secret amp is no longer
      special: hidden continuous parameters revealed only at probe_ready
      are the NORMAL case of the general pattern, and L4D is simply the
      inside-range leg of the L4 pair. Law-learning is enforced by the
      closed book instead of by the table trick.
Menus stay world-adaptive and unchanged in family composition
(E1: L1 L2 L3F L3E L4 L4D; E2: L1 L2 L3F L3S L4 L4D). v2 menu = ONE
instance per family — six instances, reward comparable in structure to
v1's six-contract mean; anchors are independent draws per family, so no
two families share "all anchors at one t" by construction.

PART 5 — SCRIPTED ACTOR v2 (tools/smoke_blob2.py successor)
Two-phase play. The v1 policies survive as a PHASE-A calibration program
plus PHASE-B classical answers evaluated at the revealed instances.
Phase A (generic, fixed program — no adaptive timing):
 record    burst-read the FULL base line (duty ~0.45) on both roster
           devices + the free global stats; persist the log to its own
           files (Phase B has no re-reads).
 adjust    a brief per-channel calibration walk inside a throwaway fork
           (exercises the tool + meter; its data is deliberately unused —
           see the L1 policy below).
 inject    one control fork + calibration injections PER PORT (amps
           0.3/0.6/1.0, dur 10) read on a lag grid covering [10, 250];
           fit a per-(port, lag) linear-in-amp template; keep residuals.
 ready     probe_ready() after the fixed program — deliberately early;
           its t_ready is the reference point on the time-to-ready
           Pareto axis.
Phase B (classical statistics on its own pre-reveal record):
 L1        pose- and law-ignorant BY POLICY: nearest logged device-0
           reading at/before t_a + drift-inflated sigma (no actuator
           model — L1 now prices exactly the capability the reference
           refuses to have).
 L2        per-port global mean at t_a + spatial-spread sigma (v1 logic,
           evaluated from the log).
 L3F       AR(2)/climatology blend fit on its logged pre-t_a history of
           the revealed device i.
 L3E/L3S   v1 estimators windowed to logged pre-t_a data.
 L4/L4D    the template at the revealed (port, lags), scaled linearly to
           the revealed amp (extrapolated for L4) and first-order in dur
           (amp-tu); sigma = fit residual inflated by the scale factor.
POLICY LINE: the actor does NOT fork-ensemble and does NOT sweep domains
— it is the classical-statistics reference (recorded data + minimal
calibration forks, early ready). The agent-minus-actor gap then reads as
modeling skill carried through the reveal, not as who found a rehearsal
trick (there is none to find).
Smoke gates (updated for the closed book): all instances submitted, none
at -1, L4/L4D positive (the law template survives the reveal), L1 within
tolerance of the floor (|skill| <= ~0.1 — the v1 "L1 positive" gate is
impossible closed-book for a law-ignorant reference; a positive L1 now
certifies the capability v2.1 prices), zero safety-cap hits.

PART 6 — MIGRATION / VALIDATION PLAN (order of work)
 1. Domain + instance freeze: fix per-world syllabus templates (2.3);
    hash-draw the hidden instances per (world, seed) (blobround2 _rng
    pattern, salt "r5_instances_v1") from the published domains; reserve
    the round5/ cache namespace; truth ensembles build at first reveal
    (2.6), never touching the v1 caches or the round2/ dose cache.
 2. Implementation: blobcore (caps/meters; BUDGETS demoted to CAPS),
    blobround5 (instance registry, syllabus generation, per-instance
    ladders, scoring), servers/blob.py surface rewrite (2.5) + the phase
    machine (probe_ready irreversible; world tools -> generic phase error
    in Phase B), blobstate (contexts, meters, phase, t_ready), taskset
    BLOB2v2-E1/E2 tags + system-prompt rewrite (budget paragraph, lock
    list, and "unspent budget" line deleted; syllabus + two-phase closed-
    book language added). v1 tags and code paths stay untouched until
    step 6.
 3. Text audit: extend the barrier regex over ALL agent-visible strings
    with the economy vocabulary ('budget', 'cost', 'price', 'spend',
    'remaining', 'afford', 'left'); unit tests assert no tool return, no
    refusal, and no prompt line matches (the message-size guard is
    reworded to comply); cap refusals tested generic. PLUS the REVEAL-
    LEAK AUDIT: the whole Phase-A surface (syllabus, status, tool
    returns, refusals) must be instance-independent — test: redraw the
    hidden instances under a different salt and assert the Phase-A
    surface is byte-identical; syllabus text may depend only on (world,
    seed) category facts (device/slot/port counts, the L3E event spec)
    that v1 announced anyway.
 4. Phase gates: (a) POST-REVEAL ISOLATION test — a scripted driver calls
    probe_ready then every world tool; PASS = all return the generic
    phase error, probe_status/probe_submit stay alive, resubmission
    works, world meters stop accruing. (b) BRUTE-FORCE-INFEASIBILITY
    note, published with the floors: per tier, the hidden dimensions,
    their continuity, and effective cardinality (anchor at sim-step
    resolution >= ~3e5 distinguishable values, times continuous u / port
    / amp / dur) — documents that domain-gridding is hopeless, per
    decision 2.
 5. A0-style adequacy re-run: scripted actor v2 on BLOB2v2-E1/E2 x 3
    seeds. PASS = PART-5 smoke gates + the actor still SEPARATES worlds
    (per-family skill profile differs E1 vs E2 in the expected directions
    — the v1 signature was L3E/L3S menu split + L2 gap). Floor tables
    (smoke_blob2 equivalent: smoke_blob2v2_*.json) recomputed and
    published in the results json exactly as round 2 did; confirm E1
    L3F's H=5 leg reads as a fair leg under the new floors (PART 3 —
    the v2.0 flag is retired).
 6. Safety-cap monitoring: per-rollout cap_hits dict logged; the round is
    valid only if EVERY rollout shows zero hits. A hit by a non-
    degenerate rollout means the cap shaped behavior: raise that cap
    (>=4x), rebuild nothing (caps are non-semantic by construction), and
    re-run the affected rollouts. time-to-ready is reviewed as a
    DISTRIBUTION only (silent meter, Pareto axis; no target, no cap —
    decision 1). After v2 smoke passes, gate the v1 tags (BLOB2-E1/E2 ->
    gated "superseded by BLOB2v2, see this file") so rows cannot be
    mixed by accident.
 7. Comparability note (mandatory in every report): v1 rows (round-4
    numbers: fable E1 +0.308 / E2 +0.287, scripted +0.238/+0.233) are
    budget-conditioned, single-realization-truth, T0-anchored, open-book;
    v2 rows are none of those. THE TWO COLUMNS NEVER MIX; no cross-
    version deltas. (No v2.0 rows exist: the open-book v2.0 draft was
    spec-only and never implemented.)
 8. Post 11 (docs/blobs/measuring-evolved-worlds.html) gets a round-5
    update AFTER implementation + first v2 results — future work, not
    part of this change.

PART 7 — OPEN QUESTIONS (kept short; recommendations, not decisions)
 Q1 RESOLVED BY FOLD: anchor selection policy is no longer a separate
    knob — it IS the published sampling domain (2.3). The old Q1
    constraints live on as domain bounds: t_a uniform-continuous in
    [600, 2300] per family, independent draws (spread over t is
    statistical, not scheduled); the lower edge guarantees the AR(2)
    rung >= 600tu of backtest history; the upper edge keeps late anchors
    live (truth may run past T_BASE) while bounding build cost. Revisit
    the bounds only with the floors in hand.
 Q2 Fork-state anchors in scored instances. v2: BASE-LINE ANCHORS ONLY —
    RECOMMENDED because truth must be cached per (world, seed, instance)
    and compared across agents: a fork-state anchor is a function of one
    rollout's private history, so its truth cannot be prebuilt, shared,
    or compared (and the cache key space explodes). Hidden-instance
    sampling makes this stronger still: a fork-state anchor cannot even
    be phrased as a published domain. Fork-state anchors return with
    agent-authored contracts in the L6 executable-theory lane, which owns
    the same difficulty-normalization open problem (two agents anchoring
    different states get incomparably hard tasks — unsolved, explicitly
    out of scope here).
 Q3 Truth ensemble size. n_truth=12 echoes MAX_REPLICAS but has no other
    justification. Estimator noise is shared across agents (frozen
    members), so ranking bias is second-order; per-instance skill noise
    still scales ~1/sqrt(n). RECOMMEND: n_truth=16 default, 24 for the
    long-horizon instances (L3E, L3S, L3F H=400) where member spread is
    largest; confirm with a build-time variance check (CRPS of the ladder
    vs member count) before freezing — raise only if the ladder's skill
    estimate moves > ~0.02 between n and n/2.
 Q4 Does Phase-B code-running advantage coding harnesses over chat
    tiers? In principle yes: the closed book rewards agents that can run
    their own fitted simulator, and a chat-only tier would face the
    reveal with notes and mental math. BLOB2 is already coding-harness-
    native (bash/python have always been part of the surface), so within
    this benchmark the comparison is fair; revisit only if a chat-tier
    lane is ever added — that would need a tier split in the harness,
    not a world change.
 Q5 Scoring philosophy (DEFERRED; v2.1 ships with the unchanged skill
    formula). The user leans toward ABSOLUTE scores over baseline-
    relative skill in a later round — different agent performances then
    become their own measure of relative performance. Noted for that
    revisit:
    (a) raw per-instance CRPS is already logged in the detail dicts and
        MUST remain logged verbatim in v2;
    (b) the only structural reason for normalization is aggregation
        across instances/worlds with different scales and aleatoric
        floors;
    (c) candidate absolute anchor if revisited: truth-ensemble self-CRPS
        (the aleatoric limit) instead of the classical ladder — physics-
        anchored rather than stats-anchored;
    (d) unsubmitted = -1 needs redefinition in any absolute regime.

CONTEXT / LINEAGE (cited paths)
 probes/blobs/l0/deepsearch/R5_BRIEF.md            round-5 decisions
                                                   (a)-(c)
 probes/blobs/l0/deepsearch/R5_BRIEF2.md           v2.1 revision brief:
                                                   category anchoring +
                                                   closed-book reveal
 probes/blobs/l0/deepsearch/TRACKA_CLEANSLATE_EVAL.md   v1 design (round 2)
 probes/blobs/l0/deepsearch/TRACKA_R2_CONTROLS.md  control-surface history
 environments/physim/physim/blobcore.py            BUDGETS, T0/T_EP,
                                                   MAX_REPLICAS, AMP_CAP,
                                                   price fn, replica fork
 environments/physim/physim/blobround2.py          menus, _skill,
                                                   LOCK_AT_INJECT, ladders
 environments/physim/physim/servers/blob.py        v1 surface (budget
                                                   advertisement to remove)
 environments/physim/physim/blobstate.py           rollout state / meters
 environments/physim/physim/taskset.py             BLOB2 prompts (budget +
                                                   lock language to remove)
 environments/physim/tools/smoke_blob2.py          scripted actor v1
 probes/blobs/agentenv/round4/ROUND4_FINAL.md      the frozen v1 row
 docs/blobs/measuring-evolved-worlds.html          post 11 (update later)
=============================================================================
