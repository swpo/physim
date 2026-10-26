# Evidence pack: active-nematic-marangoni (seed 22)

- world: `../../../20261026T0505-c34-nematic-marangoni/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 505s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out collective/contrib/20261026T1400-c42-review-marangoni/rerun/seed22 --seeds 22 --no-movie`
- segmentation: matter > 0.60 of robust range [-0.8403, 0.5703], min area 6 px

## Measurements
- components: final 33, mean 23.4, max 34; occupancy final 0.09
- tracks: 99; persistent (alive >= 50% of run): 18; longest 157 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.57 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [33, 33, 32], H1 [0, 0, 0]
- motion: 59 long-lived tracks moved >= 1 body length; max speed 0.277/time; max body lengths 9.2
- replication (lineage window K = 20 frames = time 100, default): splits 39, persistent splits 26 (0 more failed only because the siblings re-merged within K), max generation 4, merges 13, merge/split ratio 0.333, nucleations 8
- channel total drift (end/start - 1): [-0.5066, -0.4027, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 22 at frame 123: holes 0, rim-vs-core 0.62, rim-vs-outside 0.45, heterogeneity 0.23; core [0.941, 0.879, 0.408, 0.476] rim [0.781, 0.607, 0.769, 0.088]
  - track 23 at frame 123: holes 0, rim-vs-core 0.67, rim-vs-outside 0.39, heterogeneity 0.23; core [0.946, 0.752, 0.401, 0.54] rim [0.787, 0.517, 0.782, 0.074]
  - track 28 at frame 126: holes 0, rim-vs-core 0.74, rim-vs-outside 0.38, heterogeneity 0.23; core [0.954, 0.902, 0.386, 0.448] rim [0.763, 0.555, 0.848, 0.025]
  - track 79 at frame 176: holes 0, rim-vs-core 0.75, rim-vs-outside 0.32, heterogeneity 0.22; core [0.961, 0.584, 0.368, 0.472] rim [0.764, 0.359, 0.887, 0.015]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 158 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.786, rim/outside 4.67 (aggregate of 158 individuals; 0/158 membrane-like individually; rim level 0.715)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.777, rim/outside 9.39 (aggregate of 158 individuals; 6/158 membrane-like individually; rim level 0.559)
  - radial surfactant s: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.33, rim/outside 3.26 (aggregate of 158 individuals; 74/158 membrane-like individually; rim level 0.596)
  - radial cargo c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.427, rim/outside 2.05 (aggregate of 158 individuals; 16/158 membrane-like individually; rim level 0.13)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #22 (t=615, R_eq 3.66): ['surfactant s']; #23 (t=615, R_eq 4.03): none; #28 (t=630, R_eq 3.48): ['surfactant s']; #79 (t=880, R_eq 3.95): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 158 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
