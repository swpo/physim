# Evidence pack: active-nematic-marangoni (seed 72)

- world: `../../../../20261026T0505-c34-nematic-marangoni/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 381s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out collective/contrib/c49rev5/runs/base/seed72 --seeds 72 --size 128 128 --frames 200 --no-movie`
- segmentation: matter > 0.60 of robust range [-0.8374, 0.5639], min area 6 px

## Measurements
- components: final 32, mean 21.1, max 33; occupancy final 0.09
- tracks: 117; persistent (alive >= 50% of run): 11; longest 138 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [34, 33, 32], H1 [0, 0, 0]
- motion: 54 long-lived tracks moved >= 1 body length; max speed 0.379/time; max body lengths 11.7
- replication (lineage window K = 20 frames = time 100, default): splits 47, persistent splits 27 (0 more failed only because the siblings re-merged within K), max generation 5, merges 17, merge/split ratio 0.362, nucleations 5
- channel total drift (end/start - 1): [-0.5073, -0.416, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 13 at frame 113: holes 0, rim-vs-core 0.51, rim-vs-outside 0.30, heterogeneity 0.12; core [0.938, 0.485, 0.463, 0.0] rim [0.75, 0.334, 0.913, 0.0]
  - track 31 at frame 133: holes 0, rim-vs-core 0.53, rim-vs-outside 0.32, heterogeneity 0.14; core [0.95, 0.665, 0.401, 0.0] rim [0.757, 0.442, 0.845, 0.0]
  - track 33 at frame 133: holes 0, rim-vs-core 0.57, rim-vs-outside 0.34, heterogeneity 0.14; core [0.96, 0.699, 0.351, 0.0] rim [0.758, 0.44, 0.814, 0.0]
  - track 96 at frame 171: holes 0, rim-vs-core 0.67, rim-vs-outside 0.36, heterogeneity 0.15; core [0.958, 0.853, 0.385, 0.0] rim [0.743, 0.454, 0.874, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 142 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.778, rim/outside 4.65 (aggregate of 142 individuals; 0/142 membrane-like individually; rim level 0.709)
  - radial order |Q|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.743, rim/outside 9.01 (aggregate of 142 individuals; 7/142 membrane-like individually; rim level 0.546)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.32, rim/outside 3.24 (aggregate of 142 individuals; 70/142 membrane-like individually; rim level 0.6)
  - radial cargo c: flat profile (no radial structure; level 0; aggregate of 142 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #13 (t=565, R_eq 4.22): none; #31 (t=665, R_eq 4.18): none; #33 (t=665, R_eq 4.11): none; #96 (t=855, R_eq 3.19): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 142 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
