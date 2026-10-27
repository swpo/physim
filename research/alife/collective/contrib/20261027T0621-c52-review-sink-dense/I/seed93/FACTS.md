# Evidence pack: active-nematic-marangoni-sinkdiscs (seed 93)

- world: `../../../../collective/contrib/20261026T2123-c45-marangoni-sink-escape-dense/world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: c34 Marangoni rods (CARGO=0) in growing sink discs that lower the local chemostat target (arm S) or remove the bodies they open on (arm I)
- run: 321 frames x 100 steps x dt 0.05 = time 1600; grid [128, 128]; wall 584s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2123-c45-marangoni-sink-escape-dense/world.py --out collective/contrib/20261027T0621-c52-review-sink-dense/I/seed93 --seeds 93 --size 128 128 --frames 320 --no-movie`
- segmentation: matter > 0.65 of robust range [-1.011, 0.5549], min area 6 px

## Measurements
- components: final 3, mean 13.4, max 21; occupancy final 0.01
- tracks: 106; persistent (alive >= 50% of run): 3; longest 255 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.93 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 3, 3], H1 [0, 0, 0]
- motion: 49 long-lived tracks moved >= 1 body length; max speed 0.274/time; max body lengths 15.7
- replication (lineage window K = 20 frames = time 100, default): splits 41, persistent splits 20 (0 more failed only because the siblings re-merged within K), max generation 5, merges 12, merge/split ratio 0.293, nucleations 12
- channel total drift (end/start - 1): [-1.0736, -0.94, None, -0.236]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 33 at frame 194: holes 0, rim-vs-core 0.58, rim-vs-outside 0.38, heterogeneity 0.15; core [0.964, 0.923, 0.402, 1.0] rim [0.792, 0.607, 0.855, 1.0]
  - track 31 at frame 137: holes 0, rim-vs-core 0.64, rim-vs-outside 0.33, heterogeneity 0.16; core [0.97, 0.699, 0.409, 1.0] rim [0.776, 0.42, 0.948, 1.0]
  - track 43 at frame 156: holes 0, rim-vs-core 0.55, rim-vs-outside 0.36, heterogeneity 0.15; core [0.953, 0.832, 0.424, 1.0] rim [0.773, 0.542, 0.856, 1.0]
  - track 70 at frame 229: holes 0, rim-vs-core 0.51, rim-vs-outside 0.34, heterogeneity 0.13; core [0.953, 0.848, 0.404, 1.0] rim [0.784, 0.589, 0.816, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 79 components >= 12 px at frames [54, 108, 161, 212, 266, 320]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.831, rim/outside 2.99 (aggregate of 79 individuals; 0/79 membrane-like individually; rim level 0.761)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.81, rim/outside 9.2 (aggregate of 79 individuals; 3/79 membrane-like individually; rim level 0.611)
  - radial surfactant s: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.25, rim/outside 3.25 (aggregate of 79 individuals; 36/79 membrane-like individually; rim level 0.613)
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1.01 (aggregate of 79 individuals; 0/79 membrane-like individually; rim level 0.995)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #33 (t=970, R_eq 3.74): ['surfactant s']; #31 (t=685, R_eq 4.33): ['surfactant s']; #43 (t=780, R_eq 3.95): ['surfactant s']; #70 (t=1145, R_eq 4.41): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 79 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
