# Evidence pack: active-nematic-marangoni-two-kinds (seed 4)

- world: `../../../20261026T0655-c34-two-kinds-swap/world.py`, family `active-nematic`
- parent: 20261025T1141-c11-active-nematic-ringed; mutation: surfactant source restricted to rod pixels (phi>0); chis 3 -> 5; optional ring-gated CH mobility gm; cargo excluded by the ring (kappa); Marangoni stress of the ring (mar)
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 668s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0655-c34-two-kinds-swap/world.py --out collective/contrib/20261026T0915-c38-review-two-kinds/rerun/orig_seed4 --seeds 4 --no-movie`
- segmentation: matter > 0.56 of robust range [-0.8393, 0.654], min area 6 px

## Measurements
- components: final 28, mean 25.6, max 32; occupancy final 0.09
- tracks: 103; persistent (alive >= 50% of run): 18; longest 165 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.57 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 29, 28], H1 [0, 0, 0]
- motion: 57 long-lived tracks moved >= 1 body length; max speed 0.29/time; max body lengths 10.0
- replication (lineage window K = 20 frames = time 100, default): splits 38, persistent splits 25 (0 more failed only because the siblings re-merged within K), max generation 4, merges 17, merge/split ratio 0.447, nucleations 11
- channel total drift (end/start - 1): [-0.5085, -0.3729, 14.7499, 3.7759]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 25 at frame 119: holes 0, rim-vs-core 0.58, rim-vs-outside 0.32, heterogeneity 0.17; core [0.956, 0.632, 0.03, 0.431] rim [0.749, 0.482, 0.083, 0.953]
  - track 35 at frame 124: holes 0, rim-vs-core 0.66, rim-vs-outside 0.39, heterogeneity 0.17; core [0.948, 0.934, 0.03, 0.322] rim [0.712, 0.608, 0.087, 0.844]
  - track 20 at frame 108: holes 0, rim-vs-core 0.56, rim-vs-outside 0.35, heterogeneity 0.15; core [0.935, 0.809, 0.344, 0.016] rim [0.739, 0.495, 0.769, 0.042]
  - track 78 at frame 156: holes 0, rim-vs-core 0.57, rim-vs-outside 0.35, heterogeneity 0.14; core [0.933, 0.844, 0.346, 0.003] rim [0.734, 0.513, 0.759, 0.008]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 170 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.816, rim/outside 5.04 (aggregate of 170 individuals; 2/170 membrane-like individually; rim level 0.744)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.778, rim/outside 9.76 (aggregate of 170 individuals; 5/170 membrane-like individually; rim level 0.579)
  - radial surfactant A: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.35, rim/outside 3.21 (aggregate of 170 individuals; 99/170 membrane-like individually; rim level 0.464)
  - radial surfactant B: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.26, rim/outside 3.05 (aggregate of 170 individuals; 88/170 membrane-like individually; rim level 0.174)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant B
- membrane-like channels per top track at mid-life: #25 (t=595, R_eq 4.3): ['order |Q|', 'surfactant A', 'surfactant B']; #35 (t=620, R_eq 3.43): ['surfactant A', 'surfactant B']; #20 (t=540, R_eq 3.34): ['surfactant A', 'surfactant B']; #78 (t=780, R_eq 3.57): ['surfactant A']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 170 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
