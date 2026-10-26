# Evidence pack: active-nematic-marangoni-two-kinds (seed 2)

- world: `../../world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 453s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0630-c34-marangoni-two-kinds/world.py --out collective/contrib/20261026T0630-c34-marangoni-two-kinds/sel_s12 --seeds 1 2 --no-movie`
- segmentation: matter > 0.56 of robust range [-0.8346, 0.6448], min area 6 px

## Measurements
- components: final 31, mean 20.8, max 33; occupancy final 0.08
- tracks: 102; persistent (alive >= 50% of run): 7; longest 161 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.22 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [34, 32, 29], H1 [0, 0, 0]
- motion: 51 long-lived tracks moved >= 1 body length; max speed 0.471/time; max body lengths 7.0
- replication (lineage window K = 20 frames = time 100, default): splits 42, persistent splits 26 (0 more failed only because the siblings re-merged within K), max generation 6, merges 10, merge/split ratio 0.238, nucleations 8
- channel total drift (end/start - 1): [-0.5106, -0.3474, 7.1019, 9.1529]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 17 at frame 116: holes 0, rim-vs-core 0.55, rim-vs-outside 0.35, heterogeneity 0.14; core [0.937, 0.914, 0.008, 0.345] rim [0.735, 0.628, 0.02, 0.765]
  - track 26 at frame 129: holes 0, rim-vs-core 0.42, rim-vs-outside 0.33, heterogeneity 0.11; core [0.91, 0.772, 0.006, 0.366] rim [0.733, 0.536, 0.016, 0.659]
  - track 33 at frame 134: holes 0, rim-vs-core 0.59, rim-vs-outside 0.39, heterogeneity 0.14; core [0.967, 0.964, 0.013, 0.263] rim [0.758, 0.67, 0.04, 0.726]
  - track 89 at frame 185: holes 0, rim-vs-core 0.58, rim-vs-outside 0.37, heterogeneity 0.15; core [0.941, 0.835, 0.373, 0.016] rim [0.737, 0.519, 0.815, 0.043]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 137 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.809, rim/outside 4.61 (aggregate of 137 individuals; 1/137 membrane-like individually; rim level 0.726)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.778, rim/outside 7.97 (aggregate of 137 individuals; 3/137 membrane-like individually; rim level 0.594)
  - radial surfactant A: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.995, rim/outside 2.85 (aggregate of 137 individuals; 67/137 membrane-like individually; rim level 0.187)
  - radial surfactant B: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.82, rim/outside 2.95 (aggregate of 137 individuals; 88/137 membrane-like individually; rim level 0.425)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant B
- membrane-like channels per top track at mid-life: #17 (t=580, R_eq 3.24): ['surfactant B']; #26 (t=645, R_eq 3.43): ['surfactant B']; #33 (t=670, R_eq 3.19): ['surfactant A', 'surfactant B']; #89 (t=925, R_eq 3.66): ['surfactant A', 'surfactant B']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 137 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
