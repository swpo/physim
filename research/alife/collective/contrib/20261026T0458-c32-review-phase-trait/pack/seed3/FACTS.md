# Evidence pack: phase-trait (seed 3)

- world: `../../world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_kinds; mutation: continuous heritable catalyst trait c (growth rate) with link-output trade-off b(c) and +-delta point mutations
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 14s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0458-c32-review-phase-trait/world.py --out collective/contrib/20261026T0458-c32-review-phase-trait/pack --seeds 3 4 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.4898], min area 6 px

## Measurements
- components: final 30, mean 15.2, max 30; occupancy final 0.41
- tracks: 58; persistent (alive >= 50% of run): 6; longest 128 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.20 (1 = constant size)
- enclosures: components with a hole mean 7.16, final 11; holes at thresholds 0.2/0.35/0.5 final [0, 11, 30]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 30, 30], H1 [34, 30, 4]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00276/time; max body lengths 1.0
- replication (lineage window K = 20 frames = time 1000, default): splits 27, persistent splits 15 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [-0.5294, 13.5076, 33.9378, 10.8669, 9.0667]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 138: holes 1, rim-vs-core 0.26, rim-vs-outside 0.91, heterogeneity 0.18; core [0.173, 0.652, 0.698, 0.855, 0.696] rim [0.233, 0.484, 0.639, 0.731, 0.565]
  - track 15 at frame 139: holes 1, rim-vs-core 0.24, rim-vs-outside 1.05, heterogeneity 0.17; core [0.154, 0.705, 0.697, 0.894, 0.527] rim [0.215, 0.531, 0.667, 0.762, 0.606]
  - track 16 at frame 141: holes 1, rim-vs-core 0.24, rim-vs-outside 0.99, heterogeneity 0.18; core [0.156, 0.697, 0.751, 0.85, 0.687] rim [0.219, 0.527, 0.702, 0.744, 0.578]
  - track 49 at frame 182: holes 1, rim-vs-core 0.33, rim-vs-outside 1.12, heterogeneity 0.19; core [0.126, 0.802, 0.843, 0.869, 0.627] rim [0.231, 0.538, 0.765, 0.734, 0.568]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 106 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 6.25, rim/outside 0.886 (aggregate of 106 individuals; 0/106 membrane-like individually; rim level 0.461)
  - radial K catalyst: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.925, rim/outside 6.83 (aggregate of 106 individuals; 4/106 membrane-like individually; rim level 0.702)
  - radial trait c (0..0.6): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.972, rim/outside 5.59 (aggregate of 106 individuals; 4/106 membrane-like individually; rim level 0.803)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.1, rim/outside 5.31 (aggregate of 106 individuals; 10/106 membrane-like individually; rim level 0.762)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 3.35, rim/outside 4.69 (aggregate of 106 individuals; 89/106 membrane-like individually; rim level 0.664)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #10 (t=6900, R_eq 9.59, ring): ['membrane (wall)']; #15 (t=6950, R_eq 10.23, ring): ['membrane (wall)']; #16 (t=7050, R_eq 8.92, ring): ['membrane (wall)']; #49 (t=9100, R_eq 8.2, ring): ['membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 42 of 106 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
