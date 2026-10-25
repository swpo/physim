# kstrail vs matched Laplacian-only twins (Q:bd-kstrail-laplacian-twin)

kstrail (threads/chemotaxis-motility/worlds/kstrail) moves body matter by taxis up a fast
attractant a and down a slow repellent h. `twin.py` keeps every field, diffusivity, decay,
secretion and the volume-filling factor rho(1-rho), and replaces the taxis flux by a local
reaction rho(1-rho)(c_a a - c_h h - ref). The reference `ref` redistributes the converted
mass: `Lm>0` uses a screened-Poisson average of range Lm (the quasi-static field of a fast
inhibitor, (1 - Lm^2 lap)^-1), plus one uniform correction so int rho is exact; `Lm=0` uses the
global mean. No advection anywhere: the twin is reaction plus linear diffusion.
c_a = fa chi_a, c_h = fh chi_h (taxis gives chi k^2 where the reaction gives c; k ~ 0.5 at the
body scale, so f ~ 0.25 is the matched order).

All runs 192^2, dt 0.05, t = 600, labkit metrics; `readout.jsonl` is produced by `readout.py`.

| run | bodies t=150/300/450/600 | top-10 tracks >= 5 BL | median BL | max speed | median size |
|---|---|---|---|---|---|
| kstrail s0 / s1 / s2 (lab 1 pack) | 14-15 / 10-13 / 9-12 / 9-11 | 10, 10, 10 | 8.0-10.2 | 0.46-0.61 | 9.8-11.2 |
| kstrail chi_h=0 (lab 1) | 54 / 44 / 35 / 29 | 0 | 2.1 | 0.08 | 4.8 |
| **twin** (fa 0.1, fh 0.25, Lm 5) s0 / s1 / s2 | 0 / 6-17 / 12-16 / 8-10 | 10, 10, 10 | 7.0-7.5 | 0.80-0.84 | 9.7-11.0 |
| twin at dt/2, s0 | 0 / 7 / 12 / 11 | 9 | 6.7 | 0.85 | 10.1 |
| twin, fh = 0 (no inhibitor) s0 / s1 | 20-22 / 3-5 / 2-4 / 1-2 | 0, 0 | 0.4 | 0.07-0.32 | 6.7-8.1 |
| twin, global mean (Lm 0, f 0.25) s0 / s1 | 1 / 1 / 1 / 1 | 1 of 1 body | (one body) | 0.47-0.49 | 17-21 (domain-scale) |

Screens (seed 0, not packed): fh in {0, 0.1} static and fh >= 0.25 swimming for the global
twin; Lm 5 with f = 0.25 gives ~20-40 comet swimmers by t=50 that coarsen to 2-3 by t=300;
Lm 10 the same with fewer; Lm 20-30 one or two bodies; "h only" twin (chi_a taxis kept, h
repulsion replaced by reaction, fh 0.01-0.25) gives flickering static spots, 0 tracks >= 5 BL;
non-conserving local kinetics fill the domain (no individuals); a weak Ohta-Kawasaki turnover
(eps <= 0.03) does not stop the global twin's winner-take-all.

What it shows. The twin forms, from the same noise, a population of ~8-17 discrete,
unsaturated (max rho 0.72-0.77, occupancy 0.06 vs kstrail 0.054) bodies of kstrail's size
that each travel >= 5 body lengths, with a bright crescent front and a dim tail of h behind.
Removing the slow inhibitor (fh = 0) leaves static, Ostwald-coarsening spots, exactly as
chi_h = 0 does in kstrail. So spontaneous self-propelled individuals {S, I, M} at this level
are reachable by reaction-diffusion (the Krischer-Mikhailov drift bifurcation); the
taxis operator is not necessary for them.

Differences that remain. The twin needs a mass-redistribution range (Lm ~ body radius); with
a global constraint it collapses to one domain-scale swimmer. Twin bodies are faster (0.8 vs
0.5), their formation is slower (none before t~150), they sit closer together (crowded
fields with long h tails; see pack/seed1/sheet.png), and they did not show kstrail's
spot-ring-rupture-crescent route. Parameters were tuned (about 25 screens); this is "a
Laplacian-only twin can", not "every matched twin does".

Limits. One grid (192^2) and one dt pair; no 1.5x resolution run. Body counts and speeds are
labkit tracker numbers (threshold 0.35 of the matter range), and motion_top lists only the 10
most persistent tracks per run. The screened-Poisson reference is the quasi-static limit of a
fast-diffusing inhibitor field, not a simulated third field.
