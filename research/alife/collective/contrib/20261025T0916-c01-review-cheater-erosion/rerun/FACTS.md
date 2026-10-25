# Evidence pack: pcell (seed 3)

- world: `../world_real.py`, family `hybrid-particle-field`
- parent: threads/autopoiesis/worlds/phase_membrane; mutation: catalyst field K -> Brownian catalyst particles with kind/lineage, reflected by a phi^2 acceptance gate
- run: 61 frames x 500 steps x dt 1.0 = time 30000; grid [128, 128]; wall 79s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0916-c01-review-cheater-erosion/world_real.py --out collective/contrib/20261025T0916-c01-review-cheater-erosion/rerun --seeds 3 --frames 60 --spf 500 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.827], min area 6 px

## Measurements
- components: final 7, mean 18.1, max 23; occupancy final 0.03
- tracks: 53; persistent (alive >= 50% of run): 21; longest 61 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 14.06 (1 = constant size)
- enclosures: components with a hole mean 2.52, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 7, 7], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.000796/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 10000, default): splits 10, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 1, merges 2, merge/split ratio 0.2, nucleations 0
- channel total drift (end/start - 1): [-0.0543, -0.9634, -0.8915, -0.9125]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 19 at frame 30: holes 0, rim-vs-core 0.60, rim-vs-outside 0.62, heterogeneity 0.21; core [0.291, 0.656, 0.927, 0.782] rim [0.474, 0.195, 0.594, 0.69]
  - track 34 at frame 31: holes 0, rim-vs-core 0.65, rim-vs-outside 0.56, heterogeneity 0.22; core [0.187, 0.686, 0.784, 0.737] rim [0.424, 0.145, 0.518, 0.642]
  - track 31 at frame 31: holes 0, rim-vs-core 0.56, rim-vs-outside 0.56, heterogeneity 0.19; core [0.233, 0.618, 0.801, 0.794] rim [0.431, 0.177, 0.556, 0.664]
  - track 45 at frame 36: holes 0, rim-vs-core 0.63, rim-vs-outside 0.59, heterogeneity 0.21; core [0.186, 0.693, 0.835, 0.728] rim [0.421, 0.192, 0.551, 0.666]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 105 components >= 12 px at frames [10, 20, 30, 40, 50, 60]):
  - radial S: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 5.25, rim/outside 0.794 (aggregate of 105 individuals; 0/105 membrane-like individually; rim level 0.606)
  - radial K particles: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.641, rim/outside 51.1 (aggregate of 105 individuals; 0/105 membrane-like individually; rim level 0.539)
  - radial L link: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.39, rim/outside 69.9 (aggregate of 105 individuals; 47/105 membrane-like individually; rim level 0.866)
  - radial membrane (wall): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.29, rim/outside 60.3 (aggregate of 105 individuals; 91/105 membrane-like individually; rim level 0.887)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): membrane (wall)
- membrane-like channels per top track at mid-life: #19 (t=15000, R_eq 4.48): ['membrane (wall)']; #34 (t=15500, R_eq 5.73): ['L link', 'membrane (wall)']; #31 (t=15500, R_eq 5.08): ['membrane (wall)']; #45 (t=18000, R_eq 5.53): ['L link', 'membrane (wall)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 12 of 105 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
