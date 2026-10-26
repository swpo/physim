# Evidence pack: active-nematic-rodsource (seed 3)

- world: `../../../20261026T0300-c34-swimdivide/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 418s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0300-c34-swimdivide/world.py --out collective/contrib/20261026T0331-c30-review-swimdivide/rerun_zeta1 --seeds 3 4 --frames 200 --no-movie`
- segmentation: matter > 0.60 of robust range [-0.8049, 0.5415], min area 6 px

## Measurements
- components: final 31, mean 19.3, max 33; occupancy final 0.06
- tracks: 121; persistent (alive >= 50% of run): 3; longest 116 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.08 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [32, 31, 31], H1 [1, 0, 0]
- motion: 55 long-lived tracks moved >= 1 body length; max speed 0.108/time; max body lengths 3.7
- replication (lineage window K = 20 frames = time 100, default): splits 50, persistent splits 28 (0 more failed only because the siblings re-merged within K), max generation 4, merges 17, merge/split ratio 0.34, nucleations 6
- channel total drift (end/start - 1): [-0.5034, -0.5199, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 13 at frame 86: holes 0, rim-vs-core 0.38, rim-vs-outside 0.29, heterogeneity 0.13; core [0.921, 0.708, 0.498] rim [0.751, 0.494, 0.764]
  - track 52 at frame 143: holes 0, rim-vs-core 0.40, rim-vs-outside 0.31, heterogeneity 0.14; core [0.934, 0.862, 0.404] rim [0.759, 0.597, 0.653]
  - track 43 at frame 126: holes 0, rim-vs-core 0.45, rim-vs-outside 0.37, heterogeneity 0.14; core [0.974, 0.955, 0.346] rim [0.792, 0.687, 0.651]
  - track 81 at frame 163: holes 0, rim-vs-core 0.47, rim-vs-outside 0.37, heterogeneity 0.16; core [0.953, 0.905, 0.435] rim [0.765, 0.634, 0.774]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 130 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.83, rim/outside 4.26 (aggregate of 130 individuals; 0/130 membrane-like individually; rim level 0.782)
  - radial order |Q|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.764, rim/outside 7.25 (aggregate of 130 individuals; 0/130 membrane-like individually; rim level 0.654)
  - radial surfactant s: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.54, rim/outside 2.8 (aggregate of 130 individuals; 92/130 membrane-like individually; rim level 0.63)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant s
- membrane-like channels per top track at mid-life: #13 (t=430, R_eq 3.14): none; #52 (t=715, R_eq 3.09): ['surfactant s']; #43 (t=630, R_eq 2.88): ['surfactant s']; #81 (t=815, R_eq 2.82): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 130 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
