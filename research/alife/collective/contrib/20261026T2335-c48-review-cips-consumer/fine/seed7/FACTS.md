# Evidence pack: cips-consumer (seed 7)

- world: `../../../20261026T1700-c43-cips-consumer/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1302-c42-foodchain-both-divide-claim; mutation: c42's predator condensate replaced by a conserved CIPS enzyme whose catalysis consumes prey material
- run: 401 frames x 40 steps x dt 0.25 = time 4000; grid [128, 128]; wall 86s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1700-c43-cips-consumer/world.py --out collective/contrib/20261026T2335-c48-review-cips-consumer/fine/seed7 --seeds 7 --frames 400 --spf 40 --lineage-k 50 --no-movie`
- segmentation: matter > 0.35 of robust range [0.038, 1.9895], min area 6 px

## Measurements
- components: final 44, mean 41.9, max 86; occupancy final 0.19
- tracks: 529; persistent (alive >= 50% of run): 2; longest 220 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 14.89 (1 = constant size)
- enclosures: components with a hole mean 0.07, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [46, 43, 40], H1 [0, 0, 0]
- motion: 46 long-lived tracks moved >= 1 body length; max speed 0.0207/time; max body lengths 3.7
- replication (lineage window K = 50 frames = time 500, --lineage-k): splits 183, persistent splits 24 (0 more failed only because the siblings re-merged within K), max generation 3, merges 47, merge/split ratio 0.257, nucleations 102
- channel total drift (end/start - 1): [0.0271, 0.0191, None, -0.6018]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 249 at frame 134: holes 0, rim-vs-core 0.31, rim-vs-outside 0.46, heterogeneity 0.28; core [0.682, 0.595, 0.563, 0.15] rim [0.559, 0.435, 0.325, 0.178]
  - track 113 at frame 111: holes 0, rim-vs-core 0.33, rim-vs-outside 0.56, heterogeneity 0.27; core [0.785, 0.464, 0.493, 0.103] rim [0.549, 0.432, 0.281, 0.169]
  - track 394 at frame 306: holes 0, rim-vs-core 0.42, rim-vs-outside 0.34, heterogeneity 0.28; core [0.799, 0.457, 0.49, 0.106] rim [0.544, 0.318, 0.203, 0.183]
  - track 489 at frame 376: holes 0, rim-vs-core 0.22, rim-vs-outside 0.26, heterogeneity 0.22; core [0.814, 0.205, 0.138, 0.08] rim [0.608, 0.2, 0.124, 0.156]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 230 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial prey a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.899, rim/outside 11.3 (aggregate of 230 individuals; 16/230 membrane-like individually; rim level 0.674)
  - radial consumer q: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.788, rim/outside 9.45 (aggregate of 230 individuals; 25/230 membrane-like individually; rim level 0.342)
  - radial product r: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.668, rim/outside 14.7 (aggregate of 230 individuals; 17/230 membrane-like individually; rim level 0.284)
  - radial fuel u: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 2.59, rim/outside 0.763 (aggregate of 230 individuals; 0/230 membrane-like individually; rim level 0.234)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #249 (t=1340, R_eq 5.35): none; #113 (t=1110, R_eq 6.18): none; #394 (t=3060, R_eq 5.7): none; #489 (t=3760, R_eq 5.97): ['consumer q', 'product r']
- species `prey` (channels ['prey a'], own threshold): components final 44, mean 38.7, max 78; tracks 561, persistent 1; splits 215, persistent splits 20 (K=50), max generation 3, merges 37, merge/split 0.172; moving tracks 33
- species `consumer` (channels ['consumer q'], own threshold): components final 32, mean 32.3, max 71; tracks 325, persistent 3; splits 91, persistent splits 10 (K=50), max generation 4, merges 6, merge/split 0.066; moving tracks 82

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 9 of 230 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
