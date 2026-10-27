# Evidence pack: active-nematic-marangoni-sinkdiscs (seed 90)

- world: `../../../world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: c34 Marangoni rods (CARGO=0) in growing sink discs that lower the local chemostat target (arm S) or remove the bodies they open on (arm I)
- run: 321 frames x 100 steps x dt 0.05 = time 1600; grid [128, 128]; wall 527s; status ok
- command: `python -m labkit.run /tmp/claude-0/se/world.py --out /tmp/claude-0/se/runs/S_mar0/seed90 --seeds 90 --size 128 128 --frames 320 --no-movie`
- segmentation: matter > 0.60 of robust range [-0.9034, 0.594], min area 6 px

## Measurements
- components: final 20, mean 20.1, max 30; occupancy final 0.04
- tracks: 112; persistent (alive >= 50% of run): 10; longest 243 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.86 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [24, 20, 20], H1 [2, 0, 0]
- motion: 66 long-lived tracks moved >= 1 body length; max speed 0.085/time; max body lengths 7.3
- replication (lineage window K = 20 frames = time 100, default): splits 48, persistent splits 38 (0 more failed only because the siblings re-merged within K), max generation 5, merges 9, merge/split ratio 0.188, nucleations 7
- channel total drift (end/start - 1): [-0.6575, -0.6353, None, -0.2168]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 30 at frame 199: holes 0, rim-vs-core 0.28, rim-vs-outside 0.39, heterogeneity 0.11; core [0.902, 0.72, 0.439, 1.0] rim [0.784, 0.591, 0.655, 1.0]
  - track 40 at frame 215: holes 0, rim-vs-core 0.35, rim-vs-outside 0.25, heterogeneity 0.09; core [0.903, 0.684, 0.392, 1.0] rim [0.753, 0.486, 0.645, 1.0]
  - track 14 at frame 137: holes 0, rim-vs-core 0.42, rim-vs-outside 0.32, heterogeneity 0.10; core [0.929, 0.785, 0.406, 1.0] rim [0.771, 0.555, 0.718, 1.0]
  - track 76 at frame 285: holes 0, rim-vs-core 0.37, rim-vs-outside 0.25, heterogeneity 0.09; core [0.897, 0.653, 0.466, 1.0] rim [0.745, 0.462, 0.745, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 127 components >= 12 px at frames [54, 108, 161, 212, 266, 320]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.832, rim/outside 3.7 (aggregate of 127 individuals; 0/127 membrane-like individually; rim level 0.779)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.767, rim/outside 8.03 (aggregate of 127 individuals; 0/127 membrane-like individually; rim level 0.659)
  - radial surfactant s: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.66, rim/outside 2.85 (aggregate of 127 individuals; 92/127 membrane-like individually; rim level 0.592)  MEMBRANE-LIKE
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.993, rim/outside 1.01 (aggregate of 127 individuals; 2/127 membrane-like individually; rim level 0.985)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant s
- membrane-like channels per top track at mid-life: #30 (t=995, R_eq 3.29): ['surfactant s']; #40 (t=1075, R_eq 2.93): ['surfactant s']; #14 (t=685, R_eq 3.48): ['surfactant s']; #76 (t=1425, R_eq 3.91): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 127 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
