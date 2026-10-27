# Evidence pack: active-nematic-marangoni-sinkdiscs (seed 97)

- world: `../../20261026T2123-c45-marangoni-sink-escape-dense/world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: c34 Marangoni rods (CARGO=0) in growing sink discs that lower the local chemostat target (arm S) or remove the bodies they open on (arm I)
- run: 321 frames x 100 steps x dt 0.05 = time 1600; grid [128, 128]; wall 452s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2123-c45-marangoni-sink-escape-dense/world.py --out collective/contrib/20261027T0413-c51-review-marangoni-sink-dense/S_s97 --seeds 97 --size 128 128 --frames 320 --no-movie`
- segmentation: matter > 0.65 of robust range [-1.0142, 0.5514], min area 6 px

## Measurements
- components: final 6, mean 11.3, max 21; occupancy final 0.02
- tracks: 72; persistent (alive >= 50% of run): 4; longest 210 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 10.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [1, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [6, 6, 6], H1 [0, 0, 0]
- motion: 42 long-lived tracks moved >= 1 body length; max speed 0.308/time; max body lengths 13.7
- replication (lineage window K = 20 frames = time 100, default): splits 23, persistent splits 16 (0 more failed only because the siblings re-merged within K), max generation 4, merges 13, merge/split ratio 0.565, nucleations 12
- channel total drift (end/start - 1): [-0.8543, -0.8731, None, -0.076]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 121: holes 0, rim-vs-core 0.58, rim-vs-outside 0.33, heterogeneity 0.14; core [0.971, 0.813, 0.39, 1.0] rim [0.801, 0.511, 0.853, 1.0]
  - track 37 at frame 161: holes 0, rim-vs-core 0.68, rim-vs-outside 0.37, heterogeneity 0.16; core [0.971, 0.901, 0.432, 1.0] rim [0.785, 0.501, 0.954, 1.0]
  - track 24 at frame 118: holes 0, rim-vs-core 0.53, rim-vs-outside 0.40, heterogeneity 0.14; core [0.964, 0.93, 0.372, 1.0] rim [0.787, 0.642, 0.774, 1.0]
  - track 60 at frame 288: holes 0, rim-vs-core 0.44, rim-vs-outside 0.32, heterogeneity 0.14; core [0.951, 0.66, 0.557, 1.0] rim [0.807, 0.482, 0.93, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 66 components >= 12 px at frames [54, 108, 161, 212, 266, 320]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.841, rim/outside 3.04 (aggregate of 66 individuals; 0/66 membrane-like individually; rim level 0.767)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.812, rim/outside 9.42 (aggregate of 66 individuals; 4/66 membrane-like individually; rim level 0.603)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.31, rim/outside 3.39 (aggregate of 66 individuals; 35/66 membrane-like individually; rim level 0.611)
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.994, rim/outside 1.02 (aggregate of 66 individuals; 0/66 membrane-like individually; rim level 0.979)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #10 (t=605, R_eq 4.3): none; #37 (t=805, R_eq 3.39): ['surfactant s']; #24 (t=590, R_eq 3.78): none; #60 (t=1440, R_eq 5.7): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 66 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
