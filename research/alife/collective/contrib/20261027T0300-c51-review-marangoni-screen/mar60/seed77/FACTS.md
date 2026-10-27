# Evidence pack: active-nematic-marangoni (seed 77)

- world: `../../../20261026T0505-c34-nematic-marangoni/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 271s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out collective/contrib/20261027T0300-c51-review-marangoni-screen/mar60/seed77 --seeds 77 --size 128 128 --frames 200 --no-movie`
- segmentation: matter > 0.61 of robust range [-0.831, 0.5298], min area 6 px

## Measurements
- components: final 30, mean 23.3, max 31; occupancy final 0.09
- tracks: 109; persistent (alive >= 50% of run): 15; longest 168 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.45 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 30, 30], H1 [0, 0, 0]
- motion: 60 long-lived tracks moved >= 1 body length; max speed 0.445/time; max body lengths 12.6
- replication (lineage window K = 20 frames = time 100, default): splits 42, persistent splits 22 (0 more failed only because the siblings re-merged within K), max generation 3, merges 14, merge/split ratio 0.333, nucleations 11
- channel total drift (end/start - 1): [-0.4974, -0.5442, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 19 at frame 118: holes 0, rim-vs-core 0.52, rim-vs-outside 0.30, heterogeneity 0.14; core [0.953, 0.541, 0.471, 0.0] rim [0.76, 0.335, 0.904, 0.0]
  - track 26 at frame 119: holes 0, rim-vs-core 0.52, rim-vs-outside 0.29, heterogeneity 0.13; core [0.948, 0.473, 0.499, 0.0] rim [0.746, 0.28, 0.94, 0.0]
  - track 18 at frame 106: holes 0, rim-vs-core 0.34, rim-vs-outside 0.35, heterogeneity 0.11; core [0.907, 0.684, 0.527, 0.0] rim [0.773, 0.526, 0.795, 0.0]
  - track 67 at frame 150: holes 0, rim-vs-core 0.62, rim-vs-outside 0.38, heterogeneity 0.13; core [0.994, 0.873, 0.237, 0.0] rim [0.813, 0.501, 0.701, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 158 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.818, rim/outside 4.48 (aggregate of 158 individuals; 1/158 membrane-like individually; rim level 0.726)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.824, rim/outside 9.19 (aggregate of 158 individuals; 25/158 membrane-like individually; rim level 0.523)
  - radial surfactant s: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.16, rim/outside 3.23 (aggregate of 158 individuals; 54/158 membrane-like individually; rim level 0.616)
  - radial cargo c: flat profile (no radial structure; level 0; aggregate of 158 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #19 (t=590, R_eq 3.87): none; #26 (t=595, R_eq 3.99): none; #18 (t=530, R_eq 4.85): none; #67 (t=750, R_eq 2.46): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 7 of 158 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
