# Evidence pack: active-nematic-marangoni-sinkdiscs (seed 90)

- world: `../../../world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: c34 Marangoni rods (CARGO=0) in growing sink discs that lower the local chemostat target (arm S) or remove the bodies they open on (arm I)
- run: 321 frames x 100 steps x dt 0.05 = time 1600; grid [128, 128]; wall 559s; status ok
- command: `python -m labkit.run /tmp/claude-0/se/world.py --out /tmp/claude-0/se/runs/I/seed90 --seeds 90 --size 128 128 --frames 320 --no-movie`
- segmentation: matter > 0.62 of robust range [-0.9141, 0.5704], min area 6 px

## Measurements
- components: final 15, mean 21.0, max 30; occupancy final 0.05
- tracks: 122; persistent (alive >= 50% of run): 11; longest 265 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.18 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 15, 15], H1 [3, 0, 0]
- motion: 69 long-lived tracks moved >= 1 body length; max speed 0.295/time; max body lengths 10.7
- replication (lineage window K = 20 frames = time 100, default): splits 50, persistent splits 33 (0 more failed only because the siblings re-merged within K), max generation 5, merges 15, merge/split ratio 0.3, nucleations 7
- channel total drift (end/start - 1): [-0.6882, -0.6653, None, -0.2168]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 27 at frame 188: holes 0, rim-vs-core 0.57, rim-vs-outside 0.38, heterogeneity 0.17; core [0.961, 0.726, 0.405, 1.0] rim [0.777, 0.502, 0.898, 1.0]
  - track 44 at frame 199: holes 0, rim-vs-core 0.40, rim-vs-outside 0.43, heterogeneity 0.15; core [0.955, 0.632, 0.457, 1.0] rim [0.82, 0.475, 0.804, 1.0]
  - track 36 at frame 175: holes 0, rim-vs-core 0.55, rim-vs-outside 0.34, heterogeneity 0.13; core [0.938, 0.842, 0.403, 1.0] rim [0.747, 0.527, 0.805, 1.0]
  - track 98 at frame 261: holes 0, rim-vs-core 0.56, rim-vs-outside 0.34, heterogeneity 0.14; core [0.943, 0.923, 0.408, 1.0] rim [0.757, 0.584, 0.818, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 132 components >= 12 px at frames [54, 108, 161, 212, 266, 320]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.807, rim/outside 3.5 (aggregate of 132 individuals; 1/132 membrane-like individually; rim level 0.711)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.793, rim/outside 8.28 (aggregate of 132 individuals; 13/132 membrane-like individually; rim level 0.518)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.23, rim/outside 3.23 (aggregate of 132 individuals; 56/132 membrane-like individually; rim level 0.6)
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1 (aggregate of 132 individuals; 0/132 membrane-like individually; rim level 1)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #27 (t=940, R_eq 4.95): none; #44 (t=995, R_eq 4.18): none; #36 (t=875, R_eq 3.95): none; #98 (t=1305, R_eq 3.83): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 7 of 132 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
