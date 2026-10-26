# Evidence pack: cips-turnover (seed 2)

- world: `../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1845-c23-cips-metabolic-claim; mutation: c23 CIPS on a consumed fuel plus uniform, fuel-independent enzyme turnover d(e0-e) (Zwicker-type made-outside / lost-inside)
- run: 241 frames x 500 steps x dt 0.1 = time 12000; grid [256, 256]; wall 946s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0342-c32-review-coop-rods/world.py --out collective/contrib/20261026T0342-c32-review-coop-rods/pack_s2 --seeds 2 --size 256 256 --frames 240 --spf 500 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0096, 0.9818], min area 6 px

## Measurements
- components: final 17, mean 11.1, max 17; occupancy final 0.11
- tracks: 17; persistent (alive >= 50% of run): 17; longest 173 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 19.49 (1 = constant size)
- enclosures: components with a hole mean 0.10, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 17, 17], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.3
- replication (lineage window K = 20 frames = time 1000, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 17
- channel total drift (end/start - 1): [0.0004, -0.5671, 0.6113]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 155: holes 0, rim-vs-core 0.22, rim-vs-outside 0.80, heterogeneity 0.11; core [0.98, 0.918, 0.035] rim [0.85, 0.787, 0.156]
  - track 1 at frame 155: holes 0, rim-vs-core 0.30, rim-vs-outside 0.73, heterogeneity 0.12; core [0.982, 0.931, 0.045] rim [0.805, 0.744, 0.195]
  - track 2 at frame 155: holes 0, rim-vs-core 0.20, rim-vs-outside 0.79, heterogeneity 0.11; core [0.97, 0.876, 0.019] rim [0.852, 0.768, 0.137]
  - track 3 at frame 157: holes 0, rim-vs-core 0.30, rim-vs-outside 0.73, heterogeneity 0.12; core [0.982, 0.928, 0.039] rim [0.806, 0.74, 0.191]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 74 components >= 12 px at frames [81, 121, 159, 200, 240]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.755, rim/outside 19.5 (aggregate of 74 individuals; 1/74 membrane-like individually; rim level 0.715)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.823, rim/outside 10.6 (aggregate of 74 individuals; 1/74 membrane-like individually; rim level 0.729)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 14.7, rim/outside 0.652 (aggregate of 74 individuals; 0/74 membrane-like individually; rim level 0.509)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=7750, R_eq 12.68): none; #1 (t=7750, R_eq 12.69): none; #2 (t=7750, R_eq 13.66): none; #3 (t=7850, R_eq 12.83): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 74 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
