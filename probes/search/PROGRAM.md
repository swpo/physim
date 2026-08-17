# physim WORLD-SEARCH PROGRAM (2026-02-17)

## Mission
Find the most interesting complex-behavior world we have ever built: a
MULTI-LAYER HIERARCHY of dynamics with a SIMPLE, INTERPRETABLE law at the top.
Interesting = rich-vs-big (compact laws, discovery-hard) + hierarchy quality.
Real-world analogue is a bonus, not a requirement.

## Method: searchable world parameterizations (proven on E2)
Design a PARAMETERIZED family you believe contains interesting physics, then
SWEEP it — sample in THEORY COORDINATES (the quantities your own analysis says
matter: ratios, critical points, timescale separations), not raw constants.
E2 lesson: raw-coordinate search 0/48, theory-coordinate 4/48.

## Hard gates (a candidate PASSES only if all hold)
G1 HIERARCHY: >= 3 distinguishable dynamical layers, adjacent-layer scale
   separation >= 5x (time or length), each layer's variable measurable.
G2 SIMPLE TOP: hier_metrics.compact_top_fit on the top macro series gives
   r2 >= 0.85 with model in {oscillator (n_cycles >= 5), relaxation,
   switch (n_flips >= 6)}. "constant" does not count.
G3 COMPUTED, NOT IMPOSED: the top law's parameter (period/tau/dwell) moves
   SMOOTHLY and MONOTONICALLY over >= 4 values of one micro price/parameter
   (a response curve). If you hard-coded the top clock, you failed.
G4 ROBUST: passes on >= 3/4 seeds and under ±10% jitter of all searched params.
G5 BUDGET-REAL: full behavior cycle visible within <= 60k ticks at L <= 96,
   probe runtime <= ~3 min per candidate on one core (report actual).

## Scoring beyond the gates (for ranking)
+ layers beyond 3; + top-law r2; + scale-separation product across layers;
+ power-law/broadband structure at intermediate layers (powerlaw_tail decades
  >= 1.5 counts; below that DO NOT claim criticality);
+ visual drama (save field strips; a film-able world wins ties);
+ real-world analogue named honestly (or "none").

## Honesty rules (from this project's history — violations wasted whole days)
- NEGATIVE RESULTS ARE DELIVERABLES. Report failed regions and mechanisms
  (cf. anode-break inversion killing B3; blending inheritance killing E0v1).
- No agent-coupling, no scripted macro events: the top law must be computed
  by the micro physics. Storms-as-schedule are allowed ONLY as external
  climate (like E1) and do NOT count as an emergent layer.
- Beware: density compensation kills selection; deep suppression kills
  everything (survivable windows are narrow — sweep for them); NEGATIVE
  drive on excitable media RAISES wave rate (anode break); settle order
  matters (weather before life); medians beat single-span stats for noisy
  certifications.

## Engine families that already exist (do NOT clone them)
tanh magnets (D), gray-scott objects (C0-C3), excitable waves (C4),
2-variant ecology (B0-B1), wave-fed ecology (B2, ecowave), heredity worlds
(E0/E1 evo, E2 enzyme economics with emergent R*). Your world must add a NEW
mechanism or a NEW hierarchy level, not re-skin these.

## Deliverables (write into your working dir probes/search/<NAME>/)
1. probe scripts (standalone numpy/scipy; import shared helpers via:
   import sys; sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search"); from hier_metrics import *)
2. results.json: every candidate tried, params (theory coords), gate
   outcomes, metrics; include failures.
3. strips/*.png: field snapshots proving each layer exists (save_strip).
4. SUMMARY.md: the story — mechanism, hierarchy diagram (layer -> variable ->
   timescale), best candidate params, response curve table, honest caveats,
   engine-integration sketch (what World fields/params it would need).
5. Reply to parent (agent_message, receiver_role='parent') with a <=25-line
   scorecard: PASS/FAIL per gate, best candidate numbers, one-line verdict.

## Environment
Run everything with /Users/spoho/Documents/prime/test/physim/.venv/bin/python (numpy/scipy/matplotlib/PIL
available; ALWAYS set MPLBACKEND=Agg). Work standalone — do NOT edit the
physim engine. Timebox yourself; prefer 40 cheap candidates over 4 slow ones.
