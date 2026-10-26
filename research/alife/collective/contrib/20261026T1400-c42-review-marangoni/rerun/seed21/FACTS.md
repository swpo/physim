# Evidence pack: active-nematic-marangoni (seed 21)

- world: `../../../20261026T0505-c34-nematic-marangoni/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 512s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out collective/contrib/20261026T1400-c42-review-marangoni/rerun/seed21 --seeds 21 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.8408, 0.5738], min area 6 px

## Measurements
- components: final 33, mean 24.9, max 34; occupancy final 0.09
- tracks: 122; persistent (alive >= 50% of run): 15; longest 171 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 11.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [33, 33, 33], H1 [0, 0, 0]
- motion: 60 long-lived tracks moved >= 1 body length; max speed 0.327/time; max body lengths 8.5
- replication (lineage window K = 20 frames = time 100, default): splits 46, persistent splits 29 (0 more failed only because the siblings re-merged within K), max generation 4, merges 19, merge/split ratio 0.413, nucleations 11
- channel total drift (end/start - 1): [-0.5032, -0.3876, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 18 at frame 116: holes 0, rim-vs-core 0.70, rim-vs-outside 0.28, heterogeneity 0.21; core [0.916, 0.602, 0.495, 0.488] rim [0.733, 0.403, 0.934, 0.017]
  - track 21 at frame 118: holes 0, rim-vs-core 0.77, rim-vs-outside 0.38, heterogeneity 0.24; core [0.948, 0.857, 0.374, 0.527] rim [0.754, 0.538, 0.818, 0.015]
  - track 6 at frame 96: holes 0, rim-vs-core 0.69, rim-vs-outside 0.34, heterogeneity 0.22; core [0.949, 0.682, 0.384, 0.408] rim [0.74, 0.434, 0.841, 0.009]
  - track 81 at frame 166: holes 0, rim-vs-core 0.71, rim-vs-outside 0.38, heterogeneity 0.22; core [0.953, 0.904, 0.345, 0.434] rim [0.761, 0.586, 0.773, 0.014]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 170 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.798, rim/outside 4.74 (aggregate of 170 individuals; 0/170 membrane-like individually; rim level 0.729)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.763, rim/outside 9.53 (aggregate of 170 individuals; 10/170 membrane-like individually; rim level 0.557)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.39, rim/outside 3.36 (aggregate of 170 individuals; 98/170 membrane-like individually; rim level 0.603)
  - radial cargo c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.376, rim/outside 1.95 (aggregate of 170 individuals; 12/170 membrane-like individually; rim level 0.122)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #18 (t=580, R_eq 4.11): none; #21 (t=590, R_eq 3.52): ['surfactant s']; #6 (t=480, R_eq 4.41): none; #81 (t=830, R_eq 3.66): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 170 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
