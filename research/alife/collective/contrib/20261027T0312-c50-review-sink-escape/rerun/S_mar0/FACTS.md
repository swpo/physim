# Evidence pack: active-nematic-marangoni-sinkdiscs (seed 93)

- world: `../../../../../../home/user/physim/research/alife/collective/contrib/20261026T2123-c45-marangoni-sink-escape-dense/world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: c34 Marangoni rods (CARGO=0) in growing sink discs that lower the local chemostat target (arm S) or remove the bodies they open on (arm I)
- run: 321 frames x 100 steps x dt 0.05 = time 1600; grid [128, 128]; wall 661s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2123-c45-marangoni-sink-escape-dense/world.py --out /tmp/claude-0/se2/runs/S_mar0/seed93 --seeds 93 --size 128 128 --frames 320 --no-movie`
- segmentation: matter > 0.63 of robust range [-1.0073, 0.5982], min area 6 px

## Measurements
- components: final 4, mean 14.2, max 21; occupancy final 0.01
- tracks: 105; persistent (alive >= 50% of run): 4; longest 221 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 4, 4], H1 [0, 0, 0]
- motion: 46 long-lived tracks moved >= 1 body length; max speed 0.1/time; max body lengths 10.8
- replication (lineage window K = 20 frames = time 100, default): splits 40, persistent splits 23 (0 more failed only because the siblings re-merged within K), max generation 5, merges 14, merge/split ratio 0.35, nucleations 11
- channel total drift (end/start - 1): [-1.0681, -0.9304, None, -0.236]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 22 at frame 145: holes 0, rim-vs-core 0.53, rim-vs-outside 0.33, heterogeneity 0.13; core [0.962, 0.934, 0.358, 1.0] rim [0.78, 0.624, 0.745, 1.0]
  - track 42 at frame 172: holes 0, rim-vs-core 0.54, rim-vs-outside 0.34, heterogeneity 0.13; core [0.963, 0.923, 0.359, 1.0] rim [0.779, 0.617, 0.771, 1.0]
  - track 23 at frame 121: holes 0, rim-vs-core 0.48, rim-vs-outside 0.35, heterogeneity 0.12; core [0.96, 0.854, 0.389, 1.0] rim [0.786, 0.58, 0.745, 1.0]
  - track 91 at frame 274: holes 0, rim-vs-core 0.22, rim-vs-outside 0.18, heterogeneity 0.05; core [0.863, 0.127, 0.575, 1.0] rim [0.745, 0.098, 0.754, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 80 components >= 12 px at frames [54, 108, 161, 212, 266, 320]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.849, rim/outside 3.1 (aggregate of 80 individuals; 0/80 membrane-like individually; rim level 0.806)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.781, rim/outside 8.21 (aggregate of 80 individuals; 1/80 membrane-like individually; rim level 0.687)
  - radial surfactant s: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.82, rim/outside 3.06 (aggregate of 80 individuals; 61/80 membrane-like individually; rim level 0.625)  MEMBRANE-LIKE
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1.02 (aggregate of 80 individuals; 0/80 membrane-like individually; rim level 1)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): surfactant s
- membrane-like channels per top track at mid-life: #22 (t=725, R_eq 3.29): ['surfactant s']; #42 (t=860, R_eq 3.48): ['surfactant s']; #23 (t=605, R_eq 3.48): ['surfactant s']; #91 (t=1370, R_eq 2.03): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 80 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
