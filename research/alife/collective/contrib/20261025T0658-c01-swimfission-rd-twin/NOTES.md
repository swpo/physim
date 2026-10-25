# swimfission vs its Laplacian-only twin (extension of Q:bd-kstrail-laplacian-twin)

swimfission (threads/chemotaxis-motility/worlds/swimfission; established SIMD, L6[L2]+L4b) is
kstrail with Da 4 -> 2 plus growth on a regrowing nutrient and toxin death. `twin_sf.py` keeps
all of it and replaces only the taxis flux by the local mass-conserving reaction of
`../20261025T0632-c01-kstrail-rd-twin/twin.py` (fa 0.25, fh 0.5, Lm 3). One change was needed
for a fair start: growth is switched on at t_on = 400, not 150, because the twin forms bodies
later and growth on the still-uniform state floods the domain (screens: 4/6 settings flooded
at t_on = 150). The control `fission/swimfission_ton400_s0` shows the delay does not hurt
swimfission (11 clean fissions, gen 2, 10.4 bodies).

Readout: the lab's strict fission tracker (threads/chemotaxis-motility/fission.py: lone parent
for >= 40 t, both children survive >= 40 t without re-merging), T = 1200, 160^2.

| run | clean fissions | max strict generation | bodies (late mean) | labkit persistent splits |
|---|---|---|---|---|
| swimfission s0 / s1 / s2 (lab 1) | 10 / 10 / 15 | 3 / 3 / 3 | 10.7 / 12.5 / 11.7 | 3 / 6 / 8 |
| swimfission, t_on 400, s0 | 11 | 2 | 10.4 | - |
| twin s0 / s1 / s2 | 3 / 2 / 1 | 3 / 2 / 1 | 5.4 / 5.5 / 4.8 | 0 / 0 (s0, s1) |

Screens (seed 0, labkit only): fa 0.1 fh 0.25 Lm 5 at t_on 400 gave 1 split, 3 clean
fissions (gen 2), 2-3 bodies late; fh 0.5 Lm 5 gave 0 splits and non-moving bodies;
fa 0.25 fh 1 gave 0 splits.

What the images show. Twin bodies swim as crescents (as in the kstrail twin), but growth makes
them elongate into long worms and bands rather than pinch at a waist. Of the 6 "clean
fissions" in the strips, one is a binary waist split of an elongated body (twin_s0 strip, row
3); the others are lateral buds that nucleate beside a large body and swim off (twin_s1 rows 1-2)
or a tip shed from a long band (twin_s2). In seed 1 (pack/seed1/sheet.png) the population falls
to one body by t~700 and is then refilled by a burst of new bodies nucleating de novo from the
regrown, fed background (t~834-888): in the twin most births are not divisions at all.

Reading. Self-propelled bodies survive the replacement of taxis by reaction-diffusion (previous
contribution); robust binary fission at swimfission's rate does not, in this twin family:
the claim's own readout (strict generation 3 on 3/3 seeds) is met on 1/3 seeds, with 5x fewer
clean fissions and half the bodies. This is one twin family after ~12 screens, not a proof that
no Laplacian-only world divides this way.

Limits. Seeds 0-2 for the tracker, 0-1 for the pack; one grid; no dt/2 for the twin_sf. The
t_on change is a deliberate mismatch, controlled on swimfission for seed 0 only.
