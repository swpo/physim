# Evidence pack: active-nematic-marangoni-sinkdiscs (seed 90)

- world: `../../../world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: c34 Marangoni rods (CARGO=0) in growing sink discs that lower the local chemostat target (arm S) or remove the bodies they open on (arm I)
- run: 321 frames x 100 steps x dt 0.05 = time 1600; grid [128, 128]; wall 592s; status ok
- command: `python -m labkit.run /tmp/claude-0/se/world.py --out /tmp/claude-0/se/runs2/I/seed90 --seeds 90 --size 128 128 --frames 320 --no-movie`
- segmentation: matter > 0.66 of robust range [-1.0189, 0.5331], min area 6 px

## Measurements
- components: final 3, mean 6.5, max 18; occupancy final 0.01
- tracks: 78; persistent (alive >= 50% of run): 0; longest 127 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [1, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [3, 3, 3], H1 [0, 0, 0]
- motion: 36 long-lived tracks moved >= 1 body length; max speed 0.375/time; max body lengths 9.0
- replication (lineage window K = 20 frames = time 100, default): splits 34, persistent splits 19 (0 more failed only because the siblings re-merged within K), max generation 7, merges 3, merge/split ratio 0.088, nucleations 7
- channel total drift (end/start - 1): [-0.7337, -0.9199, None, -0.0307]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 17 at frame 108: holes 0, rim-vs-core 0.64, rim-vs-outside 0.39, heterogeneity 0.16; core [0.987, 0.953, 0.446, 1.0] rim [0.825, 0.642, 0.976, 1.0]
  - track 56 at frame 247: holes 0, rim-vs-core 0.57, rim-vs-outside 0.34, heterogeneity 0.15; core [0.987, 0.754, 0.458, 1.0] rim [0.822, 0.51, 0.946, 1.0]
  - track 60 at frame 285: holes 0, rim-vs-core 0.61, rim-vs-outside 0.44, heterogeneity 0.14; core [0.989, 0.947, 0.366, 1.0] rim [0.843, 0.703, 0.906, 1.0]
  - track 65 at frame 293: holes 0, rim-vs-core 0.51, rim-vs-outside 0.44, heterogeneity 0.13; core [0.988, 0.97, 0.396, 1.0] rim [0.835, 0.773, 0.845, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 40 components >= 12 px at frames [54, 108, 161, 212, 266, 320]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.845, rim/outside 2.7 (aggregate of 40 individuals; 0/40 membrane-like individually; rim level 0.756)
  - radial order |Q|: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.874, rim/outside 7.37 (aggregate of 40 individuals; 5/40 membrane-like individually; rim level 0.626)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.15, rim/outside 3.23 (aggregate of 40 individuals; 18/40 membrane-like individually; rim level 0.65)
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1.01 (aggregate of 40 individuals; 0/40 membrane-like individually; rim level 1)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #17 (t=540, R_eq 4.69): ['surfactant s']; #56 (t=1235, R_eq 4.48): ['order |Q|']; #60 (t=1425, R_eq 3.39): ['surfactant s']; #65 (t=1465, R_eq 4.03): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 40 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
