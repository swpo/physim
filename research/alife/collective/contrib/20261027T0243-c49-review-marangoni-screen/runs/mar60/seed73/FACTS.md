# Evidence pack: active-nematic-marangoni (seed 73)

- world: `../../../../20261026T0505-c34-nematic-marangoni/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 389s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out collective/contrib/c49rev5/runs/mar60/seed73 --seeds 73 --size 128 128 --frames 200 --no-movie`
- segmentation: matter > 0.61 of robust range [-0.8307, 0.5263], min area 6 px

## Measurements
- components: final 28, mean 23.6, max 32; occupancy final 0.09
- tracks: 128; persistent (alive >= 50% of run): 14; longest 166 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.96 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [29, 29, 27], H1 [0, 0, 0]
- motion: 55 long-lived tracks moved >= 1 body length; max speed 0.373/time; max body lengths 14.1
- replication (lineage window K = 20 frames = time 100, default): splits 47, persistent splits 23 (0 more failed only because the siblings re-merged within K), max generation 4, merges 24, merge/split ratio 0.511, nucleations 9
- channel total drift (end/start - 1): [-0.5094, -0.5327, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 19 at frame 118: holes 0, rim-vs-core 0.48, rim-vs-outside 0.24, heterogeneity 0.13; core [0.93, 0.542, 0.562, 0.0] rim [0.78, 0.271, 0.932, 0.0]
  - track 28 at frame 121: holes 0, rim-vs-core 0.51, rim-vs-outside 0.39, heterogeneity 0.13; core [0.955, 0.925, 0.41, 0.0] rim [0.77, 0.623, 0.778, 0.0]
  - track 35 at frame 128: holes 0, rim-vs-core 0.48, rim-vs-outside 0.39, heterogeneity 0.13; core [0.943, 0.881, 0.413, 0.0] rim [0.753, 0.588, 0.749, 0.0]
  - track 72 at frame 155: holes 0, rim-vs-core 0.55, rim-vs-outside 0.40, heterogeneity 0.14; core [0.949, 0.912, 0.468, 0.0] rim [0.76, 0.584, 0.861, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 155 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.816, rim/outside 4.45 (aggregate of 155 individuals; 1/155 membrane-like individually; rim level 0.72)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.835, rim/outside 8.89 (aggregate of 155 individuals; 26/155 membrane-like individually; rim level 0.504)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.13, rim/outside 3.27 (aggregate of 155 individuals; 46/155 membrane-like individually; rim level 0.625)
  - radial cargo c: flat profile (no radial structure; level 0; aggregate of 155 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #19 (t=590, R_eq 3.74): none; #28 (t=605, R_eq 3.7): none; #35 (t=640, R_eq 3.7): none; #72 (t=775, R_eq 3.74): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 155 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
