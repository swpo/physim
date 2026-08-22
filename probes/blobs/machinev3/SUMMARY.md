# MACHINE V3 — first machine built entirely from SEARCHED parts

**Status: V3-0 CERTIFIED. V3-1 CERTIFIED (amended delivery mode). V3-2 not attempted.**

This machine's engine and cargo were both found by the equation-space search
(stage-2 uniform sampling + stage-3 census), not designed. The composition
(coupling move, blade tow, release primitive, dock assembly) was searched here.
**It works: a searched engine delivers searched cargo and builds a parked
3-stack at a target site.**

## Parts (verbatim from the search)
- ENGINE `engine_10748` (extract of s2_107_48_jit act1): 1 act + 2 chans,
  c=0.2038 kicked+dressed. In the merged world: c identical to 4 digits.
- CARGO `s2_128_26_uni` act0: plateau-bond blob, bond d*=14.06, 3-stacks park
  under noise (stage-3 verdict). Its act1 is dead weight (never nucleates).

## World: block direct-sum + ONE coupling move
`lib.build_world`: `operators_lib._block_merge(engine, cargo)` -> 3 acts,
5 chans. Coupling grid result (drag px of single cargo, T=800, L=96):

| move                                | eta    | drag px | verdict |
|-------------------------------------|--------|---------|---------|
| xv_sym cross-v (task's suggestion)  | 0.05   | 0.0     | no grip |
| xv_sym cross-v                      | 0.10   | 0.0     | ENGINE SPLITS |
| e2c_c1t (write binder tanh only)    | 0.05-0.6| 0.0    | no grip |
| e2c_c2 (write repeller only)        | +-0.05-0.6| <=2  | no grip |
| e2c_c0 (write spacer only)          | 0.6    | 0.3     | no grip |
| c0+c1t                              | 0.6    | 2.4     | no grip |
| c0+c2                               | 0.6    | 15.4    | cargo DIES |
| c1t+c2                              | 0.6    | 90.3    | grip (minimal pair) |
| **mimic (0.6 x all three W_C cols)**| **0.6**| **131.3**| **LOCK** |
| mimic                               | 0.3    | 4.5     | cargo dies |
| mimic                               | 1.0    | 132.4   | lock (same) |
| kw_c (cargo reads engine w)         | +-0.3-0.8| <=18  | weak plow |

**The move: `mimic eta=0.6` — the engine act writes 0.6-scaled copies of the
cargo's own channel-drive weights into all three cargo channels (c0, c1t, c2).
The engine becomes a 60% phantom cargo.** One-way: no feedback into the engine
(its c is exactly unchanged, gate G_ENGINE rel=1.0000). Vacuum-exact (W drives
are deviation-linear). Grip needs the binder+repeller pair at >=~0.5; partial
imprints die or slip.

## V3-0 gates (all PASS, cert row `V3-0_PASS`)
- G_ENGINE: c_coupled=0.20374 = c_ref (rel 1.0000); no cargo nucleation 600tu.
- G_CARGO: single parked cargo drifts 0.001px/800tu at noise 2e-3; 3-stack 0.0005px.
- G_TOW: **PUSH lock** (blade), not pull: engine sits 4.27+-0.41px BEHIND the
  cargo and pushes at c_lock=0.199 (97.6% of solo speed), drag 131px until the
  run ends. Pull does not exist: an engine ahead runs away (torus-laps, then
  captures from behind). Same blade law as machine-v2's factory.
- RELEASE PRIMITIVE (certified): **coupling cut eta->0 mid-run.** Cargo parks
  instantly (drift 7e-15 px over 400tu); the decoupled engine keeps c=0.2038
  and laps harmlessly (architectural flyby immunity: zero cross terms).
  Negative: engine stall dial (Dv*1.15 mid-run) does NOT release (holds grip,
  oscillates); in-genome frozen-channel dock (rail amp 0.35) nucleates engine
  copies (fold distance ~0.03 << 0.35); amp 0.03 is harmless but does not stop.

## V3-1: stack delivery (PASS under documented amendment)
**Measured no-go: a pre-bonded 3-stack cannot be towed as a unit.**
- Full-speed blade (c=0.2): front bond compresses < merge distance -> chain
  MERGES (3->1) after ~25px.
- Slow blade (dv110+kw0.8, c=0.021): chain TEARS (bond max force < push need);
  per-blob tracks show neighbor handoff, not transport.
- y-laid stack: engine slips between bonds, takes only the on-lane blob
  (49.8px "drag" was a COM artifact - flagged honest, row `y_stack_artifact`).
- Weaker/stronger engines (Du0.9, Dv1.1, Dv1.13, mimic 0.35/0.8/1.0,
  K_tanh*1.5 cargo): all fail by merge, tear, replication, or stall.

**Amended delivery mode (metrics amendment row): sequential single-cargo
delivery + assembly at the dock.** 3 phases: fresh engine + fresh cargo at
x=8, blade tow ~13px/lap-free straight push, coupling cut when the cargo
crosses its slot (positions from the tracker, 2.5tu control resolution),
150tu settle -> next cargo parks 14px short of the previous. Result: a
**parked bonded 3-stack** (spacings 13.55-14.02 = the certified d* well),
built at x~57-84 from pickup at x=8.

3 runs (hold-noise seeds; tow deterministic): displacements per cargo
44.9-76.6px, stack COM 58.6-63.0px, final hold 800tu at noise 2e-3:
drift 0.0006-0.0017px, census 3, engine parked/decoupled. Cert row `V3-1_PASS`.

Caveats (in the cert row): last cargo moves 44.9-49.5px (<60; lane length at
L=96), the chain COM and 2/3 cargoes exceed 60px; release timing is an outer
control loop (in-genome release exists as the eta-cut primitive, but slot
TIMING needs either the controller or a future dock search).

## Deliverables
- `results.json` 75 rows (save-as-you-go, every run appended; smoke row first).
- `metrics.py` locked before certs; one amendment row (V3-1 mode), gates kept.
- `lib.py` (world builder + rail experiment), `runner.py` (5 job kinds),
  `make_strips.py`, `strips/` (v30_tow_lock.png, v30_release_eta0.png,
  asm3_det_a/b_final.png + npz series per run).
- Scorecard: sent to parent.

## Machine-v2 lineage notes
Blade law confirmed in a fully-searched world: capture is push-side, standoff
4.3px (v2: 7.1px with eta-wells). Release-by-decoupling is cleaner than v2's
dock: the cut is exact and instantaneous. Stack no-tow is NEW physics vs v2
(v2 chains were eta-well queues, not plateau bonds): plateau bonds are
parking-grade, not towing-grade - transport plateau cargo one at a time.

## Cost
69 sim rows, ~6.3 core-hours total (per-row wall in results.json).
