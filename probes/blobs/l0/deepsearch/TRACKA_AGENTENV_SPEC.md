
=============================================================================
TRACK A SPEC v0.1 — agent environment on evolved worlds (DISCUSSION DRAFT)
=============================================================================

CORE WORRY (user, valid): old instruments were point-level; evolved worlds are
PARTICULATE — localized objects that must be TRACKED to be understood. An agent
with sparse point taps may never even recognize a stationary blob. And the
action space is unclear (pokes vs background fluctuations vs blob insertion).

DESIGN ANSWERS

A. MEASUREMENT: instrument LADDER, all generic DSP, none of our ontology.
   I1 point taps (cheap, continuous): time series of chosen port at chosen
      location. [old default — provably inadequate alone, see A0]
   I2 windowed cameras (the new tier): WxW patch of a chosen port, chosen
      RESOLUTION (downsample allowed), snapshot or low frame-rate. Priced in
      PIXEL-SAMPLES from a per-episode measurement budget: coarse-wide vs
      fine-narrow vs occasional-dense are real experimental tradeoffs.
   I3 global aggregates (cheap): spatial mean/variance per port, mass above
      agent-chosen threshold, radially-averaged spectrum. Generic physics-lab
      gear only.
   NEVER PROVIDED: blob lists, tracks, species labels, bond graphs. Building
   a tracker from camera frames IS the agent's science (they must discover
   the world is particulate — that's finding #1 available to them).

B. BARRIER MECHANISMS (strict, enumerable):
   b1 ports = anonymized field channels (shuffled ids; no genome/params ever)
   b2 instruments = generic signal processing (above), no assay internals
   b3 contracts defined on GENERIC observables the harness computes from raw
      fields: threshold-mass in window, CONNECTED-COMPONENT COUNT in window
      (generic DSP that happens to be a blob census — no construction leak),
      point/window future statistics
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

D. CONTRACT LADDER (evolved-world edition of the classic suite):
   P1 forecast point/window statistics (CRPS), short horizon
   P2 forecast component-count trajectory in window (the census contract,
      defined generically per b3) — REQUIRES agent-built tracking
   P3 perturbation-response: harness announces a specified injection; agent
      predicts response distribution (causal understanding)
   P4 preparation: reach/hold target census or threshold-mass in region
      under injection budget
   P5 executable theory: compact predictor of census dynamics + response
      laws, scored out-of-seed (rich-vs-big: god-probe baseline vs compact
      oracle vs budgeted agents — frontier gap on EVOLVED physics)

E. WORLD LADDER (all from v2 archive, same family = controlled difficulty):
   E1 p4g2_044 (21 stable sparse blobs, seed-stable, no minted vertices) —
      the 'can you even see a blob' world; entry level
   E2 p6g8_033 champion (labyrinth + rotor cores + frozen census over
      reorganizing structure — the film insight = hard mode)
   E3 p3g9_022 (151-organism swarm, still-growing) — stress test

F. PHASE A0 (BEFORE any agent trials): MEASUREMENT ADEQUACY STUDY.
   Scripted reference pipelines (threshold + components + nearest-neighbor
   tracker — ~50 lines, no learning) run P1/P2 contracts at a GRID of
   instrument budgets on E1-E3. Deliverable: adequacy curves (contract score
   vs budget). Choose episode budgets where curves are STEEP (hard but
   possible); publish as the env calibration doc. This converts 'can agents
   even measure this?' from a worry into a measured design input.

OPEN DECISIONS (user input wanted):
 Q1 Round 1 ports: expose ALL field channels (anonymized) or hide the slow/
    w-type channels (agents infer hidden environmental fields from behavior
    — harder, more realistic, but maybe round 2)?
 Q2 Budget currency: single pixel-sample budget covering all instruments, or
    separate budgets (taps cheap/unlimited, camera pixels scarce)?
 Q3 Round 1 contract set: prediction-only (P1-P3) with preparation (P4) and
    theory (P5) in round 2 — or all five from the start?
=============================================================================
