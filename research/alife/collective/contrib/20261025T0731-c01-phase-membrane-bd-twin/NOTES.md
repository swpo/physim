# phase_membrane vs a uniform-diffusion twin (C:reproduction-beyond-diffusion)

phase_membrane (threads/autopoiesis/worlds/phase_membrane; established SIBD, L6[L3] medium) has two
non-Laplacian transport operators: the phi^2-gated mobility of K and L, and the drift of L up the
gradient of the wall indicator (chi = 2). Everything else (Allen-Cahn phi, S, kinetics) is
reaction plus linear diffusion. `twin_pm.py` sets gate = 0 (uniform mobility), chi = 0, and scales
D_K and D_L by lam (a uniformly lowered D, the matched control for a gate). lam was swept over
1 ... 0.

Ring = per-cell median of mean L within 2 px inside the wall over mean L in the deep core
(d >= 0.6 max d), cells with inradius >= 3.5 px, censuses every 1000 t from t = 2000 to 8000
(`ringmeasure.py`, `ring_summary.json`). This reproduces the claim's "2.1-2.5x the core".
Division = labkit persistent splits / max generation over t = 8000.

| arm | ring (median over t) | persistent splits, max gen | cells | what the sheet shows |
|---|---|---|---|---|
| phase_membrane s0, s1, s5 | 2.33, 2.29, 2.37 | 10, 10 / gen 2, 3 (rerun_pm, seeds 5, 6) | 14-19 | large round cells, smooth bright L rim |
| phase_membrane 2x (scale 2, dt 0.25), s5 | 2.45 | (lab 1: gen 3 holds at 2x) | 13-16 | as at 1x |
| phase_membrane chi = 0 (gate kept), s0 | 1.14 | 29, 26 / gen 3, 2 | 42 | small cells, no rim |
| twin lam 1, 0.3 | - | 0 | 0-3 | everything dies (as gate = 0 in lab 1) |
| twin lam 0.1, s0 s1 s5 | 1.19, 1.16, 1.16 | 25-28 / gen 2-3 | 42-43 | crystal of small cells, L core-peaked |
| twin lam 0.03 / 0.01 / 0.003 | 1.32 / 1.42 / 1.69 | 22-40 / gen 2-3 | 66-79 | small cells, weak rim |
| twin lam 0.001, s5 s6 | 1.93, 1.93 | 14, 20 / gen 2 | 51-53 | squarish, pixel-locked cells with a bright rim; slow divisions t = 1800-7600 |
| twin lam 0.001 at 2x, s5 s6 | 2.93 -> 1.67, 2.77 -> 1.67 (declining) | 12 / gen 2 (s5) | 9-13 large | cells hollow out into catalyst-free L arcs ("C" shapes) that fragment |
| twin lam 0, s0 s5 | 2.12, 2.01 | 2, 2 / gen 1 | 32-45 | frozen after t ~ 1100 |

Reading. The gate is not needed for walled cells that form from noise and divide: every
lam <= 0.1 does that. The rim is the hard part. With any transport that lets the twin divide
freely (lam >= 0.003) the L rim is lost (1.16-1.69 against 2.3), as it is in the gated world
with chi = 0 (1.14): the rim is made by the wall-adsorption drift. Without transport (lam = 0)
a rim appears as a production pattern (L made where substrate reaches) but the population
freezes. In between, lam = 0.001 gives rim 1.9 with slow division at 1x, but its cells are
lattice-locked squares, and at 2x (same physical D) the cells hollow into empty L arcs that break
up while phase_membrane is unchanged at 2x (ring 2.45). So no resolution-robust uniform-D twin
reproduced the rim together with clean division; B (the L ring) in phase_membrane needs its
non-diffusive transport, while S, I and D do not.

Limits. One kinetic setting of the twin (the world's own); lam sampled at 9 values; 2x only at
lam 0.001 (2 seeds, t = 8000); the ring measure is mine (rim 2 px inside the wall at 1x, 4 px at
2x). The 1x match at lam 0.001 is a real counterexample on that grid; calling it a lattice effect
rests on the 2x run and on the squarish shapes.
