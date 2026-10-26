# Outside audit of c34's Marangoni rods, third version: M supported as a minority trait

On 26 October (~14:25 UTC) the operator's principal ruled that a capability shown by only a minority of individuals is acceptable,
provided it replicates; the question it opens is how the minority persists and whether an environment can make it spread
(20261026T1530-c00-marangoni-minority-lineages and the questions Q:marangoni-*). This replaces the earlier audits' M position.

Fresh seeds 61-64 (labkit runs of the unchanged world.py, rerun/seed61-64) each contain a rod that swims 3 or more of its own
lengths (median 4 sqrt(lambda_max) over the track) between its own birth by fission and its own fission into two daughters that
live 20 frames or more: seed 61 #20 (3.23), seed 62 #30 (4.67) and #19 (3.16), seed 63 #11 (4.18), seed 64 #15 (4.45).
Prevalence: 5 of 61 split-born dividing tracks on seeds 61-64, 0 of 41 on seeds 51, 52 and the 1.5x grid (Fisher p 0.08 between
the two sets; 5 of 102 pooled, on 4 of 7 runs). With the earlier finds (claim seed 0, c37 seed 13, c38 seed 17, c42 seed 21) the
minority appears on 8 of 18 runs at 128^2. mar=0 removes it (0 swim-then-divide tracks on every seed tested). B and W were measured
by this audit on seeds 51 and 52 (20261026T1130-c00-audit-marangoni: ring on 100% of body-frames, cargo 9.0-9.3x, wall-off 0.17x).
The reviews in support_rejected stay set aside: their own seeds show no rod passing 3 of its own lengths before dividing.
