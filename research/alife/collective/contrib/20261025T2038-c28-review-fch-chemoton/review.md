# Review of 20261025T0848-c02-fch-chemoton-claim c1 (SIBE, fch-bilayer)

Written before reading any other review of this claim.

Runs: the claimed world.py and world_starve.py (feed cut at t=300, identical to the fed run until then),
fresh seeds 7 and 8, the claim's settings (192^2, 200 frames x 300 steps, t=600). Plus a new control,
`kcut/kcut.py`: run to t=300, then branch into a fed twin and a twin in which the catalyst K is erased
inside the vesicle carrying the most K (filled body dilated by 4 px); amphiphile in that region is followed to t=600.

What I saw
- S, I: noise at t=0 (sheet), bilayer rods, rings and vesicles by t~50-100, 5 persistent bodies per seed
  that live to t=600 (rerun/fed/seed7, seed8).
- B: K is autocatalytic (a K^2 P) and its mobility is min-gated by exp(-4(u+1)), so it lives only where it
  is immobilised on the bilayer: beads of K along the bilayer of 1-2 bodies per seed. seed 7 track #9 (the
  K vesicle, a figure-8 double ring) has K membrane-like at t=318; seed 8 track #3 (ring) the same. The
  aggregate K profile is not membrane-like in my seeds (rim/core 0.84 and 0.41) because most bodies are
  K-free rings or open strips; on seed 8 most K sits on open bilayer strips, not vesicles.
  K is made where it sits (autocatalysis on the bilayer), so this is a self-made, independently transported
  layer, not a drift written against the body field. The layer does work (below).
- E, fork (rubric L4c): starve twins on both seeds lose all K by t~360; vesicles and strips shrink to
  micelle dots and small rings (amphiphile -91%, -92%) while the fed twins keep theirs (+0.2%, +42%).
  The bodies do not vanish within 300 t: they lose their vesicle body plan and become micelles.
- E, local ablation (new): seed 7, the K vesicle whose K is erased shrinks from a figure-8 to one small ring,
  amphiphile 1336 -> 519 (39%) by t=600, while in the fed twin it grows to 1427; K-free rings elsewhere
  persist in both branches. Seed 8: K re-enters the target within ~50 t from a K-carrying strip that touches
  it, the region dips to 1248 (83%) and recovers to 1285 as K regrows; fed twin 1494.
  So the individual's own catalyst sustains its size, but K is not bound to one body: it spreads along
  touching bilayers.

Limits
- E is by construction: amphiphile is made only by r K P and decays at kap everywhere (RUBRIC L4c: counts
  for the rung, scored under mechanism).
- K-free rings persist for the whole run in the fed world (seed 7: 3 of 5 bodies), on amphiphile shared
  through the bath; only the K carriers keep large vesicles. Starved bodies become micelles rather than
  disappearing.
- No division; no resolution test; I did not run a Laplacian-only twin.
