# Evidence pack: active-nematic-marangoni (seed 71)

- world: `../../../../../../home/user/physim/research/alife/collective/contrib/20261026T0505-c34-nematic-marangoni/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 353s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out /tmp/claude-0/ms/runs/base/seed71 --seeds 71 --size 128 128 --frames 200 --no-movie`
- segmentation: matter > 0.60 of robust range [-0.8374, 0.5625], min area 6 px

## Measurements
- components: final 31, mean 20.1, max 32; occupancy final 0.09
- tracks: 112; persistent (alive >= 50% of run): 8; longest 148 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.55 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [33, 31, 30], H1 [0, 0, 0]
- motion: 50 long-lived tracks moved >= 1 body length; max speed 0.304/time; max body lengths 8.8
- replication (lineage window K = 20 frames = time 100, default): splits 46, persistent splits 27 (0 more failed only because the siblings re-merged within K), max generation 5, merges 16, merge/split ratio 0.348, nucleations 4
- channel total drift (end/start - 1): [-0.4969, -0.4069, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 18 at frame 128: holes 0, rim-vs-core 0.58, rim-vs-outside 0.32, heterogeneity 0.15; core [0.941, 0.636, 0.468, 0.0] rim [0.715, 0.373, 0.93, 0.0]
  - track 28 at frame 131: holes 0, rim-vs-core 0.67, rim-vs-outside 0.36, heterogeneity 0.17; core [0.963, 0.715, 0.403, 0.0] rim [0.739, 0.444, 0.969, 0.0]
  - track 34 at frame 138: holes 0, rim-vs-core 0.59, rim-vs-outside 0.33, heterogeneity 0.15; core [0.938, 0.711, 0.435, 0.0] rim [0.726, 0.417, 0.899, 0.0]
  - track 69 at frame 156: holes 0, rim-vs-core 0.61, rim-vs-outside 0.36, heterogeneity 0.15; core [0.958, 0.855, 0.315, 0.0] rim [0.75, 0.488, 0.752, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 140 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.798, rim/outside 4.78 (aggregate of 140 individuals; 0/140 membrane-like individually; rim level 0.727)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.786, rim/outside 9.51 (aggregate of 140 individuals; 8/140 membrane-like individually; rim level 0.576)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.34, rim/outside 3.3 (aggregate of 140 individuals; 75/140 membrane-like individually; rim level 0.601)
  - radial cargo c: flat profile (no radial structure; level 0; aggregate of 140 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #18 (t=640, R_eq 4.22): none; #28 (t=655, R_eq 4.72): none; #34 (t=690, R_eq 4.48): none; #69 (t=780, R_eq 2.99): ['surfactant s']

## Warnings
- radial: 3 of 140 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
