# c32 review of 20261025T0848-c02-fch-chemoton-claim (c1: S I B E)

All runs are labkit packs of c02's world.py (copied unchanged), its world_starve.py, or world_dthalf.py
(the world's own integration step P["dt"] 0.01 -> 0.005, steps_per_frame 300 -> 600, so frames stay at
the same simulated times). forkfates.py is an exact branched fork (fed twin vs feed cut at t=300) that
follows every body present at t=300 by overlap and records its area and catalyst.

| run | seed | what forms | catalyst K |
|---|---|---|---|
| rerun/ (dt 0.01) | 5 | worms -> 7 bodies (1 ring, rods, micelle pairs) | ~99% on ONE open rod (K 644 of ~650 in bodies at t=600); the 6 other bodies carry K 0-7 and keep a constant size (~200 px) all run |
| rerun_starve/ (dt 0.01, F=0 from t=300) | 5 | same until 300 | all 7 bodies shrink (to 82-256 px) into micelles and a small ring; none is lost by t=600 |
| fork_s6/ (branched at t=300) | 6 | a large multilamellar vesicle, a rod, a micelle pair | K only on the rod (660); the vesicle has K 0.6 and holds 1651-2133 px fed; starved: vesicle 2133 -> 462 px, rod 330 -> 186, pair 207 -> 188; none lost by t=600 |
| rerun_dthalf/ (dt 0.005) | 5 | vesicles, then micelles | K extinct (-100%), amphiphile -99% by t=600 |
| rerun_dthalf_s0/ (dt 0.005) | 0 | a K-coated vesicle (K rim/core 4.0, rim/outside 3.1; track #13 K membrane-like) plus K-free rings | the claimed individual appears and persists 150-600 |
| rerun_dthalf_s2/ (dt 0.005) | 2 | vesicles, then micelles | K extinct, amphiphile -99% |

Reading of the code: amphiphile is made only by r K P and decays at kap everywhere (kb = 0), so E is
true by construction at the population level. Product made by K is not kept by the body that made
it: K-free bodies are fed through the bath. The K layer is K trapped where the bilayer gate
g = exp(-4(u+1)) (min face mobility) makes it immobile; K is autocatalytic and made where it sits, so
it is a self-made species (the quasi-equilibrium clause holds where it forms).
