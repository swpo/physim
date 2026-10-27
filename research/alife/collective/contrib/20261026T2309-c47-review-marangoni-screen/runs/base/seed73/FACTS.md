# Evidence pack: active-nematic-marangoni (seed 73)

- world: `../../../../20261026T0505-c34-nematic-marangoni/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 439s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out collective/contrib/20261026T2309-c47-review-marangoni-screen/runs/base/seed73 --seeds 73 --size 128 128 --frames 200 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.8408, 0.5725], min area 6 px

## Measurements
- components: final 29, mean 23.4, max 33; occupancy final 0.09
- tracks: 115; persistent (alive >= 50% of run): 11; longest 168 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 10.25 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 30, 29], H1 [0, 0, 0]
- motion: 58 long-lived tracks moved >= 1 body length; max speed 0.245/time; max body lengths 9.5
- replication (lineage window K = 20 frames = time 100, default): splits 43, persistent splits 27 (0 more failed only because the siblings re-merged within K), max generation 4, merges 20, merge/split ratio 0.465, nucleations 9
- channel total drift (end/start - 1): [-0.5094, -0.4135, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 16 at frame 118: holes 0, rim-vs-core 0.58, rim-vs-outside 0.32, heterogeneity 0.15; core [0.948, 0.641, 0.418, 0.0] rim [0.741, 0.389, 0.899, 0.0]
  - track 27 at frame 124: holes 0, rim-vs-core 0.58, rim-vs-outside 0.32, heterogeneity 0.14; core [0.943, 0.674, 0.429, 0.0] rim [0.732, 0.416, 0.903, 0.0]
  - track 30 at frame 124: holes 0, rim-vs-core 0.54, rim-vs-outside 0.32, heterogeneity 0.14; core [0.928, 0.642, 0.501, 0.0] rim [0.732, 0.409, 0.953, 0.0]
  - track 90 at frame 176: holes 0, rim-vs-core 0.59, rim-vs-outside 0.33, heterogeneity 0.14; core [0.951, 0.712, 0.405, 0.0] rim [0.748, 0.435, 0.886, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 152 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.803, rim/outside 4.59 (aggregate of 152 individuals; 1/152 membrane-like individually; rim level 0.706)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.808, rim/outside 8.98 (aggregate of 152 individuals; 10/152 membrane-like individually; rim level 0.549)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.21, rim/outside 3.24 (aggregate of 152 individuals; 64/152 membrane-like individually; rim level 0.584)
  - radial cargo c: flat profile (no radial structure; level 0; aggregate of 152 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #16 (t=590, R_eq 4.22): none; #27 (t=620, R_eq 3.99): ['surfactant s']; #30 (t=620, R_eq 4.37): none; #90 (t=880, R_eq 4.11): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 152 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
