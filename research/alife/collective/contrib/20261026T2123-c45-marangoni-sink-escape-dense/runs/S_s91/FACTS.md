# Evidence pack: active-nematic-marangoni-sinkdiscs (seed 91)

- world: `../../../world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: c34 Marangoni rods (CARGO=0) in growing sink discs that lower the local chemostat target (arm S) or remove the bodies they open on (arm I)
- run: 321 frames x 100 steps x dt 0.05 = time 1600; grid [128, 128]; wall 556s; status ok
- command: `python -m labkit.run /tmp/claude-0/se/world.py --out /tmp/claude-0/se/runs2/S/seed91 --seeds 91 --size 128 128 --frames 320 --no-movie`
- segmentation: matter > 0.65 of robust range [-0.9979, 0.5488], min area 6 px

## Measurements
- components: final 7, mean 12.5, max 20; occupancy final 0.02
- tracks: 84; persistent (alive >= 50% of run): 3; longest 249 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 13.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 7, 7], H1 [0, 0, 0]
- motion: 52 long-lived tracks moved >= 1 body length; max speed 0.365/time; max body lengths 19.4
- replication (lineage window K = 20 frames = time 100, default): splits 30, persistent splits 23 (0 more failed only because the siblings re-merged within K), max generation 4, merges 14, merge/split ratio 0.467, nucleations 10
- channel total drift (end/start - 1): [-0.8904, -0.8603, None, -0.2358]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 31 at frame 196: holes 0, rim-vs-core 0.58, rim-vs-outside 0.33, heterogeneity 0.14; core [0.969, 0.7, 0.394, 1.0] rim [0.789, 0.433, 0.877, 1.0]
  - track 19 at frame 151: holes 0, rim-vs-core 0.61, rim-vs-outside 0.37, heterogeneity 0.14; core [0.97, 0.943, 0.385, 1.0] rim [0.784, 0.584, 0.839, 1.0]
  - track 8 at frame 102: holes 0, rim-vs-core 0.66, rim-vs-outside 0.34, heterogeneity 0.16; core [0.972, 0.732, 0.404, 1.0] rim [0.769, 0.419, 0.946, 1.0]
  - track 80 at frame 296: holes 0, rim-vs-core 0.48, rim-vs-outside 0.33, heterogeneity 0.14; core [0.958, 0.66, 0.414, 1.0] rim [0.788, 0.448, 0.812, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 78 components >= 12 px at frames [54, 108, 161, 212, 266, 320]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.83, rim/outside 3.02 (aggregate of 78 individuals; 0/78 membrane-like individually; rim level 0.753)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.791, rim/outside 8.31 (aggregate of 78 individuals; 3/78 membrane-like individually; rim level 0.586)
  - radial surfactant s: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.28, rim/outside 3.29 (aggregate of 78 individuals; 43/78 membrane-like individually; rim level 0.611)
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.992, rim/outside 1.04 (aggregate of 78 individuals; 0/78 membrane-like individually; rim level 0.992)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #31 (t=980, R_eq 4.18): none; #19 (t=755, R_eq 3.57): ['surfactant s']; #8 (t=510, R_eq 4.51): ['order |Q|', 'surfactant s']; #80 (t=1480, R_eq 5.05): ['order |Q|']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 78 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
