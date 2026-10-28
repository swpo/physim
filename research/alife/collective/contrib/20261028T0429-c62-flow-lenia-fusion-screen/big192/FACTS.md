# Evidence pack: flow-lenia-digestion-ecology-thetaB (seed 1)

- world: `../world_th.py`, family `flow-lenia`
- parent: collective/contrib/20261025T1932-c18-fl-drive-bg-sighting; mutation: a second conserved Flow-Lenia matter (predator) whose growth gain is set by a product of digesting prey matter; digested prey matter recycled as dilute prey matter
- run: 601 frames x 25 steps x dt 0.2 = time 3000; grid [192, 192]; wall 904s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/fus/world_th.py --out /tmp/claude-0/-home-user-physim/6de1d515-b157-56c9-97ab-8aa81df695be/scratchpad/fus/big192 --seeds 1 --size 192 192 --frames 600 --no-movie`
- segmentation: matter > 0.07 of robust range [0.0019, 2.17], min area 6 px

## Measurements
- components: final 35, mean 42.4, max 136; occupancy final 0.13
- tracks: 5705; persistent (alive >= 50% of run): 0; longest 56 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.19, final 0; holes at thresholds 0.2/0.35/0.5 final [7, 3, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [66, 46, 31], H1 [15, 0, 0]
- motion: 81 long-lived tracks moved >= 1 body length; max speed 0.924/time; max body lengths 15.9
- replication (lineage window K = 20 frames = time 100, default): splits 1960, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 2, merges 1942, merge/split ratio 0.991, nucleations 261
- channel total drift (end/start - 1): [-0.2734, None, -0.0679, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 886 at frame 121: holes 0, rim-vs-core 0.43, rim-vs-outside 0.07, heterogeneity 0.08; core [0.005, 0.497, 0.892, 0.052] rim [0.007, 0.071, 0.888, 0.031]
  - track 714 at frame 91: holes 0, rim-vs-core 0.48, rim-vs-outside 0.10, heterogeneity 0.09; core [0.006, 0.581, 0.916, 0.084] rim [0.009, 0.103, 0.913, 0.052]
  - track 2583 at frame 313: holes 0, rim-vs-core 0.48, rim-vs-outside 0.03, heterogeneity 0.08; core [0.005, 0.52, 0.911, 0.062] rim [0.007, 0.04, 0.908, 0.036]
  - track 3052 at frame 358: holes 0, rim-vs-core 0.60, rim-vs-outside 0.05, heterogeneity 0.09; core [0.007, 0.651, 0.905, 0.07] rim [0.008, 0.048, 0.903, 0.042]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 233 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial prey A: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.888, rim/outside 7.86 (aggregate of 233 individuals; 29/233 membrane-like individually; rim level 0.183)
  - radial predator B: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.03, rim/outside 13.9 (aggregate of 233 individuals; 61/233 membrane-like individually; rim level 0.291)
  - radial food: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.32, rim/outside 0.942 (aggregate of 233 individuals; 0/233 membrane-like individually; rim level 0.761)
  - radial digestion q: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.774, rim/outside 3.5 (aggregate of 233 individuals; 1/233 membrane-like individually; rim level 0.0985)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #886 (t=605, R_eq 4.55): ['predator B']; #714 (t=455, R_eq 4.69): ['predator B']; #2583 (t=1565, R_eq 5.11): ['predator B']; #3052 (t=1790, R_eq 4.15): none
- species `prey` (channels ['prey A'], own threshold): components final 22, mean 21.2, max 78; tracks 1138, persistent 0; splits 358, persistent splits 8 (K=20), max generation 5, merges 313, merge/split 0.874; moving tracks 205
- species `predator` (channels ['predator B'], own threshold): components final 33, mean 32.2, max 41; tracks 2573, persistent 0; splits 869, persistent splits 13 (K=20), max generation 5, merges 713, merge/split 0.82; moving tracks 251

## Warnings
- radial: 1 of 233 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
