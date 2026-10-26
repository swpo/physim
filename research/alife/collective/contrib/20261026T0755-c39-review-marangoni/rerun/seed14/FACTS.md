# Evidence pack: active-nematic-marangoni (seed 14)

- world: `../../../20261026T0505-c34-nematic-marangoni/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 424s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0505-c34-nematic-marangoni/world.py --out collective/contrib/20261026T0830-c39-review-marangoni/rerun/seed14 --seeds 14 --no-movie`
- segmentation: matter > 0.60 of robust range [-0.8407, 0.5709], min area 6 px

## Measurements
- components: final 30, mean 25.1, max 33; occupancy final 0.09
- tracks: 92; persistent (alive >= 50% of run): 19; longest 174 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.56 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 30, 29], H1 [0, 0, 0]
- motion: 54 long-lived tracks moved >= 1 body length; max speed 0.27/time; max body lengths 10.0
- replication (lineage window K = 20 frames = time 100, default): splits 35, persistent splits 25 (0 more failed only because the siblings re-merged within K), max generation 3, merges 12, merge/split ratio 0.343, nucleations 10
- channel total drift (end/start - 1): [-0.5086, -0.4333, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 21 at frame 114: holes 0, rim-vs-core 0.75, rim-vs-outside 0.35, heterogeneity 0.24; core [0.96, 0.714, 0.401, 0.398] rim [0.754, 0.458, 0.948, 0.012]
  - track 30 at frame 124: holes 0, rim-vs-core 0.72, rim-vs-outside 0.33, heterogeneity 0.24; core [0.943, 0.678, 0.433, 0.406] rim [0.724, 0.402, 0.921, 0.008]
  - track 34 at frame 129: holes 0, rim-vs-core 0.73, rim-vs-outside 0.32, heterogeneity 0.23; core [0.954, 0.681, 0.401, 0.468] rim [0.753, 0.431, 0.874, 0.018]
  - track 60 at frame 139: holes 0, rim-vs-core 0.70, rim-vs-outside 0.34, heterogeneity 0.21; core [0.951, 0.695, 0.363, 0.438] rim [0.752, 0.436, 0.816, 0.012]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 168 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.805, rim/outside 4.79 (aggregate of 168 individuals; 0/168 membrane-like individually; rim level 0.728)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.805, rim/outside 9.66 (aggregate of 168 individuals; 12/168 membrane-like individually; rim level 0.559)
  - radial surfactant s: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.29, rim/outside 3.25 (aggregate of 168 individuals; 85/168 membrane-like individually; rim level 0.593)
  - radial cargo c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.467, rim/outside 2.29 (aggregate of 168 individuals; 20/168 membrane-like individually; rim level 0.138)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #21 (t=570, R_eq 4.98): none; #30 (t=620, R_eq 4.18): none; #34 (t=645, R_eq 4.07): none; #60 (t=695, R_eq 4.03): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 168 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
