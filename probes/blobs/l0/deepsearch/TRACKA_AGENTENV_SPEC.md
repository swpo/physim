
=============================================================================
TRACK A SPEC v0.1 — agent environment on evolved worlds (DISCUSSION DRAFT)
=============================================================================

CORE WORRY (user, valid): old instruments were point-level; evolved worlds are
PARTICULATE — localized objects that must be TRACKED to be understood. An agent
with sparse point taps may never even recognize a stationary blob. And the
action space is unclear (pokes vs background fluctuations vs blob insertion).

DESIGN ANSWERS

A. MEASUREMENT v2 (2026-08-31, user constraint: NO DIRECT WORLD VIEW —
   no images, no spatial layout, no dimension, no box size):
   The interface is a SENSOR NETWORK with opaque addressing. Space is not
   given; it is DISCOVERABLE.
   ADDRESSING: agent receives K anchor tokens (opaque ids; harness placed
   them randomly, never discloses coordinates). Operations:
     place_sensor(anchor | existing_sensor, step_direction d, step_size s)
   where d ranges over D anonymous 'direction slots' (harness knows the
   secret mapping; per-episode random rotation/reflection). DIMENSION,
   TOPOLOGY (torus wrap!), and METRIC are all inferable only through
   sensor-motion experiments (how many independent directions? do long
   walks return?). This is the strict form of the barrier: geometry itself
   is science.
   SENSOR TYPES (all return SCALAR TIMESERIES; no arrays/images ever):
     s-tap: port value at sensor
     s-int(r): integrated mass within radius r (three gain settings, priced
       by r — a wide antenna, not a picture)
     s-diff(d): finite difference along anonymous direction d
     s-event(theta): threshold-crossing counter (rate stream)
   Global aggregates (I3) reduced to: per-port global mean + variance ONLY
   (no spectra — spectra leak grid/box structure).
   PRICING: per-episode budget in sensor-seconds, weighted by type (s-int
   costs ~r^2). Sensor moves cost budget too (relocation friction).
   NEVER PROVIDED: images, blob lists, coordinates, dimension, box size,
   boundary conditions. Recognizing particulateness, dimensionality, and
   the torus IS the agent's early science program.

B. BARRIER MECHANISMS (strict, enumerable):
   b1 ports = anonymized field channels (shuffled ids; no genome/params ever)
   b2 instruments = generic signal processing (above), no assay internals
   b3 contracts defined ONLY on SENSOR-OBSERVABLE quantities (future
      statistics of named sensor streams, event rates, responses at named
      sensors) — never on spatial constructs (no window counts: a 'window'
      presumes the geometry we refuse to disclose)
   b4 env code path consumes only the sim state tensor through the port
      layer; blobkit metrics stay evaluator-side (scoring + adequacy only)
   b5 world selection by published rule from the archive; contracts fixed
      per (world, seed); report-only conduct metrics unchanged

C. ACTIONS: ONE unified primitive — BUDGETED SOURCE INJECTION:
      inject(port, location, spatial_profile, amplitude, duration)
   with per-episode integral budget (total |injected mass|) and amplitude cap.
   The user's three candidate input types are REGIMES of this primitive:
   - poke = compact impulsive injection (small sigma, one step)
   - background fluctuation = low-amplitude broad/noisy profile, sustained
   - blob insertion = SUPRA-THRESHOLD shaped compact injection — yes, it is
     exactly 'pushing a source into a blob field'; whether a blob NUCLEATES
     depends on world physics (genesis results: threshold+shape matter; some
     coupling classes refuse noise-nucleation entirely). Agents get to
     DISCOVER nucleation science; we never ship an 'insert blob' macro.
   Intrinsic world noise stays world-side (touching the noise generator =
   construction access). Resets: replay same (world, seed) with different
   interventions = standard experiment design, allowed and budgeted.

D. CONTRACT LADDER v2 (sensor-observable currency only):
   P1 forecast sensor-stream statistics (CRPS) at horizon H for NAMED
      sensors (incl. sensors the harness places adversarially far from the
      agent's own net)
   P2 event-rate forecasting: predict s-event rate trajectories (the
      particulate world's census signature, WITHOUT the harness admitting
      a census exists)
   P3 perturbation-response: announced injection at anchor A; predict
      response distribution at sensors B_1..B_k (causality + propagation +
      geometry, all in one)
   P4 preparation: drive named sensor observables into announced bands and
      HOLD (e.g. 's-int(large)@S3 in [a,b] for 200tu') under injection budget
   P5 executable theory: compact simulator/predictor of the SENSOR
      OBSERVABLES, scored out-of-seed and out-of-anchor-layout (rich-vs-big
      on evolved physics; layout generalization = the new twist)

E. WORLD LADDER (all from v2 archive, same family = controlled difficulty):
   E1 p4g2_044 (21 stable sparse blobs, seed-stable, no minted vertices) —
      the 'can you even see a blob' world; entry level
   E2 p6g8_033 champion (labyrinth + rotor cores + frozen census over
      reorganizing structure — the film insight = hard mode)
   E3 p3g9_022 (151-organism swarm, still-growing) — stress test

F. PHASE A0 (BEFORE any agent trials): MEASUREMENT ADEQUACY STUDY, sensor-net
   edition. Reference pipelines now include the geometry bootstrap: (i) infer
   dimension from independent-direction probing, (ii) detect particulateness
   from s-int/s-event statistics, (iii) TRIANGULATE + track a moving blob from
   >=3 integrating taps (no images!), (iv) run P1-P3 at a grid of sensor-second
   budgets on E1-E3. Adequacy curves decide budgets (steep region). If scripted
   pipelines CANNOT localize blobs through sensor nets at sane budgets, we
   learn it BEFORE burning agent runs — and tune sensor pricing/gains, not the
   barrier.

OPEN DECISIONS (user input wanted):
 Q1 Round 1 ports: expose ALL field channels (anonymized) or hide the slow/
    w-type channels (agents infer hidden environmental fields from behavior
    — harder, more realistic, but maybe round 2)?
 Q2 Budget currency: single pixel-sample budget covering all instruments, or
    separate budgets (taps cheap/unlimited, camera pixels scarce)?
 Q3 Round 1 contract set: prediction-only (P1-P3) with preparation (P4) and
    theory (P5) in round 2 — or all five from the start?
=============================================================================
