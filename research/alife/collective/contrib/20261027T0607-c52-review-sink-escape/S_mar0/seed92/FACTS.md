# Evidence pack: active-nematic-marangoni-sinkdiscs (seed 92)

- world: `../../../../collective/contrib/20261026T2053-c45-marangoni-sink-escape/world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: c34 Marangoni rods (CARGO=0) in growing sink discs that lower the local chemostat target (arm S) or remove the bodies they open on (arm I)
- run: 321 frames x 100 steps x dt 0.05 = time 1600; grid [128, 128]; wall 432s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2053-c45-marangoni-sink-escape/world.py --out collective/contrib/20261027T0607-c52-review-sink-escape/S_mar0/seed92 --seeds 92 --size 128 128 --frames 320 --no-movie`
- segmentation: matter > 0.60 of robust range [-0.9309, 0.6084], min area 6 px

## Measurements
- components: final 24, mean 21.3, max 29; occupancy final 0.05
- tracks: 148; persistent (alive >= 50% of run): 8; longest 237 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.14 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [24, 24, 24], H1 [0, 0, 0]
- motion: 67 long-lived tracks moved >= 1 body length; max speed 0.0806/time; max body lengths 5.5
- replication (lineage window K = 20 frames = time 100, default): splits 62, persistent splits 41 (0 more failed only because the siblings re-merged within K), max generation 7, merges 13, merge/split ratio 0.21, nucleations 11
- channel total drift (end/start - 1): [-0.5487, -0.5238, None, -0.0199]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 15 at frame 148: holes 0, rim-vs-core 0.50, rim-vs-outside 0.33, heterogeneity 0.12; core [0.951, 0.872, 0.302, 1.0] rim [0.756, 0.574, 0.65, 1.0]
  - track 45 at frame 180: holes 0, rim-vs-core 0.49, rim-vs-outside 0.35, heterogeneity 0.13; core [0.944, 0.887, 0.329, 1.0] rim [0.759, 0.609, 0.683, 1.0]
  - track 43 at frame 159: holes 0, rim-vs-core 0.51, rim-vs-outside 0.35, heterogeneity 0.13; core [0.946, 0.887, 0.33, 1.0] rim [0.747, 0.585, 0.695, 1.0]
  - track 136 at frame 309: holes 0, rim-vs-core 0.56, rim-vs-outside 0.33, heterogeneity 0.14; core [0.949, 0.842, 0.365, 1.0] rim [0.747, 0.544, 0.795, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 142 components >= 12 px at frames [54, 108, 161, 212, 266, 320]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.826, rim/outside 3.49 (aggregate of 142 individuals; 0/142 membrane-like individually; rim level 0.786)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.745, rim/outside 8.17 (aggregate of 142 individuals; 2/142 membrane-like individually; rim level 0.653)
  - radial surfactant s: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.99, rim/outside 2.96 (aggregate of 142 individuals; 121/142 membrane-like individually; rim level 0.595)  MEMBRANE-LIKE
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1.01 (aggregate of 142 individuals; 1/142 membrane-like individually; rim level 0.993)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant s
- membrane-like channels per top track at mid-life: #15 (t=740, R_eq 2.93): ['surfactant s']; #45 (t=900, R_eq 3.14): ['surfactant s']; #43 (t=795, R_eq 3.14): ['surfactant s']; #136 (t=1545, R_eq 2.82): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 142 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
