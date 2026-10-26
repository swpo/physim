# Evidence pack: phase-trait (seed 4)

- world: `../../world.py`, family `autopoiesis`
- parent: threads/autopoiesis/worlds/phase_kinds; mutation: continuous heritable catalyst trait c (growth rate) with link-output trade-off b(c) and +-delta point mutations
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 15s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0458-c32-review-phase-trait/world.py --out collective/contrib/20261026T0458-c32-review-phase-trait/pack --seeds 3 4 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5053], min area 6 px

## Measurements
- components: final 22, mean 11.9, max 22; occupancy final 0.41
- tracks: 43; persistent (alive >= 50% of run): 6; longest 150 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.62 (1 = constant size)
- enclosures: components with a hole mean 5.54, final 8; holes at thresholds 0.2/0.35/0.5 final [0, 8, 28]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [23, 23, 22], H1 [32, 25, 4]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.00456/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 1000, default): splits 20, persistent splits 15 (0 more failed only because the siblings re-merged within K), max generation 5, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [-0.5238, 13.5568, 34.9012, 10.5034, 9.2079]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 126: holes 0, rim-vs-core 0.49, rim-vs-outside 1.15, heterogeneity 0.19; core [0.099, 0.757, 0.746, 0.841, 0.508] rim [0.294, 0.393, 0.641, 0.705, 0.707]
  - track 12 at frame 136: holes 0, rim-vs-core 0.47, rim-vs-outside 1.33, heterogeneity 0.17; core [0.081, 0.856, 0.856, 0.844, 0.551] rim [0.273, 0.476, 0.834, 0.754, 0.73]
  - track 16 at frame 141: holes 1, rim-vs-core 0.29, rim-vs-outside 1.00, heterogeneity 0.17; core [0.131, 0.718, 0.724, 0.846, 0.651] rim [0.225, 0.49, 0.682, 0.725, 0.571]
  - track 37 at frame 182: holes 1, rim-vs-core 0.46, rim-vs-outside 1.27, heterogeneity 0.17; core [0.061, 0.761, 0.745, 0.787, 0.291] rim [0.188, 0.549, 0.682, 0.743, 0.67]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 80 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial S: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 4.52, rim/outside 0.889 (aggregate of 80 individuals; 0/80 membrane-like individually; rim level 0.461)
  - radial K catalyst: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.891, rim/outside 4.74 (aggregate of 80 individuals; 8/80 membrane-like individually; rim level 0.589)
  - radial trait c (0..0.6): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.911, rim/outside 4.13 (aggregate of 80 individuals; 8/80 membrane-like individually; rim level 0.654)
  - radial L link: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.03, rim/outside 3.82 (aggregate of 80 individuals; 10/80 membrane-like individually; rim level 0.654)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.89, rim/outside 3.53 (aggregate of 80 individuals; 51/80 membrane-like individually; rim level 0.562)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #8 (t=6300, R_eq 8.31): ['membrane (wall)']; #12 (t=6800, R_eq 7.55): ['membrane (wall)']; #16 (t=7050, R_eq 8.7, ring): ['membrane (wall)']; #37 (t=9100, R_eq 14.56): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 23 of 80 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
