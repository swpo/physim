# Evidence pack: active-nematic-marangoni (seed 77)

- world: `../../../20261026T0505-c34-nematic-marangoni/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 273s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out collective/contrib/20261027T0300-c51-review-marangoni-screen/base/seed77 --seeds 77 --size 128 128 --frames 200 --no-movie`
- segmentation: matter > 0.60 of robust range [-0.8432, 0.5696], min area 6 px

## Measurements
- components: final 30, mean 23.0, max 31; occupancy final 0.09
- tracks: 115; persistent (alive >= 50% of run): 17; longest 169 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.96 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [32, 30, 29], H1 [0, 0, 0]
- motion: 49 long-lived tracks moved >= 1 body length; max speed 0.373/time; max body lengths 10.8
- replication (lineage window K = 20 frames = time 100, default): splits 42, persistent splits 21 (0 more failed only because the siblings re-merged within K), max generation 3, merges 20, merge/split ratio 0.476, nucleations 9
- channel total drift (end/start - 1): [-0.4974, -0.4087, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 18 at frame 116: holes 0, rim-vs-core 0.53, rim-vs-outside 0.33, heterogeneity 0.14; core [0.936, 0.739, 0.45, 0.0] rim [0.752, 0.499, 0.883, 0.0]
  - track 27 at frame 128: holes 0, rim-vs-core 0.55, rim-vs-outside 0.34, heterogeneity 0.15; core [0.938, 0.704, 0.42, 0.0] rim [0.729, 0.436, 0.854, 0.0]
  - track 30 at frame 128: holes 0, rim-vs-core 0.60, rim-vs-outside 0.36, heterogeneity 0.14; core [0.958, 0.802, 0.377, 0.0] rim [0.77, 0.512, 0.865, 0.0]
  - track 103 at frame 187: holes 0, rim-vs-core 0.56, rim-vs-outside 0.34, heterogeneity 0.15; core [0.935, 0.837, 0.417, 0.0] rim [0.745, 0.517, 0.829, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 157 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.791, rim/outside 4.51 (aggregate of 157 individuals; 0/157 membrane-like individually; rim level 0.71)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.799, rim/outside 8.78 (aggregate of 157 individuals; 7/157 membrane-like individually; rim level 0.548)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.23, rim/outside 3.16 (aggregate of 157 individuals; 75/157 membrane-like individually; rim level 0.571)
  - radial cargo c: flat profile (no radial structure; level 0; aggregate of 157 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #18 (t=580, R_eq 4.69): none; #27 (t=640, R_eq 4.07): none; #30 (t=640, R_eq 3.78): ['surfactant s']; #103 (t=935, R_eq 3.39): ['surfactant s']

## Warnings
- radial: 3 of 157 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
