# Evidence pack: active-nematic-marangoni-sinkdiscs (seed 90)

- world: `../../../world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: c34 Marangoni rods (CARGO=0) in growing sink discs that lower the local chemostat target (arm S) or remove the bodies they open on (arm I)
- run: 321 frames x 100 steps x dt 0.05 = time 1600; grid [128, 128]; wall 560s; status ok
- command: `python -m labkit.run /tmp/claude-0/se/world.py --out /tmp/claude-0/se/runs/S/seed90 --seeds 90 --size 128 128 --frames 320 --no-movie`
- segmentation: matter > 0.62 of robust range [-0.9194, 0.5705], min area 6 px

## Measurements
- components: final 26, mean 23.0, max 32; occupancy final 0.07
- tracks: 131; persistent (alive >= 50% of run): 14; longest 255 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.43 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [28, 27, 26], H1 [0, 0, 0]
- motion: 74 long-lived tracks moved >= 1 body length; max speed 0.286/time; max body lengths 14.7
- replication (lineage window K = 20 frames = time 100, default): splits 51, persistent splits 32 (0 more failed only because the siblings re-merged within K), max generation 6, merges 22, merge/split ratio 0.431, nucleations 7
- channel total drift (end/start - 1): [-0.6575, -0.5529, None, -0.2168]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 35 at frame 194: holes 0, rim-vs-core 0.56, rim-vs-outside 0.30, heterogeneity 0.14; core [0.949, 0.618, 0.441, 1.0] rim [0.76, 0.401, 0.925, 1.0]
  - track 37 at frame 199: holes 0, rim-vs-core 0.55, rim-vs-outside 0.33, heterogeneity 0.13; core [0.953, 0.711, 0.357, 1.0] rim [0.764, 0.445, 0.807, 1.0]
  - track 38 at frame 199: holes 0, rim-vs-core 0.55, rim-vs-outside 0.35, heterogeneity 0.14; core [0.94, 0.836, 0.401, 1.0] rim [0.742, 0.513, 0.794, 1.0]
  - track 117 at frame 296: holes 0, rim-vs-core 0.57, rim-vs-outside 0.36, heterogeneity 0.14; core [0.949, 0.875, 0.354, 1.0] rim [0.753, 0.531, 0.767, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 146 components >= 12 px at frames [54, 108, 161, 212, 266, 320]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.806, rim/outside 3.53 (aggregate of 146 individuals; 0/146 membrane-like individually; rim level 0.715)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.812, rim/outside 8.6 (aggregate of 146 individuals; 15/146 membrane-like individually; rim level 0.532)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.19, rim/outside 3.21 (aggregate of 146 individuals; 57/146 membrane-like individually; rim level 0.595)
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.998, rim/outside 1.01 (aggregate of 146 individuals; 0/146 membrane-like individually; rim level 0.998)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #35 (t=970, R_eq 4.48): ['surfactant s']; #37 (t=995, R_eq 4.07): none; #38 (t=995, R_eq 3.87): none; #117 (t=1480, R_eq 3.39): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 146 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
