# Evidence pack: active-nematic-marangoni-sinkdiscs (seed 90)

- world: `../../../world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: c34 Marangoni rods (CARGO=0) in growing sink discs that lower the local chemostat target (arm S) or remove the bodies they open on (arm I)
- run: 321 frames x 100 steps x dt 0.05 = time 1600; grid [128, 128]; wall 583s; status ok
- command: `python -m labkit.run /tmp/claude-0/se/world.py --out /tmp/claude-0/se/runs2/S/seed90 --seeds 90 --size 128 128 --frames 320 --no-movie`
- segmentation: matter > 0.65 of robust range [-1.0237, 0.5512], min area 6 px

## Measurements
- components: final 13, mean 12.5, max 23; occupancy final 0.04
- tracks: 100; persistent (alive >= 50% of run): 4; longest 196 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 13, 12], H1 [0, 0, 0]
- motion: 60 long-lived tracks moved >= 1 body length; max speed 0.307/time; max body lengths 9.0
- replication (lineage window K = 20 frames = time 100, default): splits 39, persistent splits 22 (0 more failed only because the siblings re-merged within K), max generation 4, merges 16, merge/split ratio 0.41, nucleations 7
- channel total drift (end/start - 1): [-0.6666, -0.7145, None, -0.0307]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 54 at frame 223: holes 0, rim-vs-core 0.61, rim-vs-outside 0.30, heterogeneity 0.17; core [0.971, 0.687, 0.462, 1.0] rim [0.798, 0.411, 0.98, 1.0]
  - track 30 at frame 151: holes 0, rim-vs-core 0.55, rim-vs-outside 0.38, heterogeneity 0.13; core [0.977, 0.935, 0.27, 1.0] rim [0.797, 0.578, 0.641, 1.0]
  - track 22 at frame 143: holes 0, rim-vs-core 0.65, rim-vs-outside 0.36, heterogeneity 0.14; core [0.983, 0.893, 0.281, 1.0] rim [0.824, 0.522, 0.79, 1.0]
  - track 76 at frame 258: holes 0, rim-vs-core 0.64, rim-vs-outside 0.35, heterogeneity 0.15; core [0.973, 0.896, 0.4, 1.0] rim [0.789, 0.526, 0.885, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 80 components >= 12 px at frames [54, 108, 161, 212, 266, 320]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.825, rim/outside 2.8 (aggregate of 80 individuals; 1/80 membrane-like individually; rim level 0.743)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.814, rim/outside 7.89 (aggregate of 80 individuals; 5/80 membrane-like individually; rim level 0.567)
  - radial surfactant s: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.2, rim/outside 3.16 (aggregate of 80 individuals; 31/80 membrane-like individually; rim level 0.6)
  - radial chemostat target phi_b(x,t): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1.02 (aggregate of 80 individuals; 0/80 membrane-like individually; rim level 0.993)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #54 (t=1115, R_eq 4.3): none; #30 (t=755, R_eq 3.14): ['surfactant s']; #22 (t=715, R_eq 2.59): ['surfactant s']; #76 (t=1290, R_eq 3.83): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 80 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
