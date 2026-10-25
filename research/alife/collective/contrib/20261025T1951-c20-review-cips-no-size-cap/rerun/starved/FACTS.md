# Evidence pack: cips-fuel (seed 5)

- world: `../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: Cotton et al. CIPS (enzyme drifts up its own product) with the fuel made a consumed, regrowing field
- run: 301 frames x 100 steps x dt 0.1 = time 3000; grid [256, 256]; wall 487s; status ok
- command: `python -m labkit.run /tmp/c20nc/world.py --out /tmp/c20nc/starved --seeds 5 --frames 300 --no-movie`
- segmentation: matter > 0.52 of robust range [0.0009, 0.9516], min area 6 px

## Measurements
- components: final 83, mean 84.5, max 154; occupancy final 0.14
- tracks: 262; persistent (alive >= 50% of run): 77; longest 238 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 16.25 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [87, 82, 82], H1 [0, 0, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.0109/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 200, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 87, merge/split ratio n/a, nucleations 175
- channel total drift (end/start - 1): [0.0, -0.5248, 0.4366]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 182: holes 0, rim-vs-core 0.21, rim-vs-outside 0.27, heterogeneity 0.06; core [0.896, 0.846, 0.017] rim [0.719, 0.758, 0.073]
  - track 2 at frame 182: holes 0, rim-vs-core 0.20, rim-vs-outside 0.27, heterogeneity 0.06; core [0.886, 0.827, 0.019] rim [0.717, 0.745, 0.073]
  - track 4 at frame 184: holes 0, rim-vs-core 0.23, rim-vs-outside 0.28, heterogeneity 0.07; core [0.902, 0.859, 0.016] rim [0.707, 0.762, 0.077]
  - track 5 at frame 184: holes 0, rim-vs-core 0.21, rim-vs-outside 0.26, heterogeneity 0.06; core [0.87, 0.883, 0.023] rim [0.69, 0.797, 0.08]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 545 components >= 12 px at frames [101, 151, 199, 250, 300]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.864, rim/outside 10.6 (aggregate of 545 individuals; 1/545 membrane-like individually; rim level 0.782)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.916, rim/outside 2.69 (aggregate of 545 individuals; 0/545 membrane-like individually; rim level 0.847)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 13.9, rim/outside 0.503 (aggregate of 545 individuals; 0/545 membrane-like individually; rim level 0.387)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=1820, R_eq 3.95): none; #2 (t=1820, R_eq 3.7): none; #4 (t=1840, R_eq 4.18): none; #5 (t=1840, R_eq 4.51): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 545 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
