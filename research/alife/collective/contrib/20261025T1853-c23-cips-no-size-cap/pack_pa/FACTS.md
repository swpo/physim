# Evidence pack: cips-fuel (seed 0)

- world: `../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261025T1650-c00-q-cips-fuel-limited-condensates; mutation: Cotton et al. CIPS (enzyme drifts up its own product) with the fuel made a consumed, regrowing field
- run: 401 frames x 100 steps x dt 0.1 = time 4000; grid [256, 256]; wall 335s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1853-c23-cips-no-size-cap/world.py --out collective/contrib/20261025T1853-c23-cips-no-size-cap/pa --seeds 0 --frames 400 --no-movie`
- segmentation: matter > 0.52 of robust range [0.0007, 0.9653], min area 6 px

## Measurements
- components: final 68, mean 80.7, max 159; occupancy final 0.14
- tracks: 292; persistent (alive >= 50% of run): 59; longest 335 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 12.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [70, 69, 68], H1 [0, 0, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.00799/time; max body lengths 1.7
- replication (lineage window K = 20 frames = time 200, default): splits 2, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 109, merge/split ratio 54.5, nucleations 179
- channel total drift (end/start - 1): [-0.0, -0.5497, 0.4574]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 235: holes 0, rim-vs-core 0.25, rim-vs-outside 0.30, heterogeneity 0.07; core [0.912, 0.859, 0.015] rim [0.697, 0.744, 0.082]
  - track 15 at frame 235: holes 0, rim-vs-core 0.22, rim-vs-outside 0.28, heterogeneity 0.07; core [0.872, 0.823, 0.022] rim [0.679, 0.73, 0.086]
  - track 19 at frame 235: holes 0, rim-vs-core 0.22, rim-vs-outside 0.28, heterogeneity 0.07; core [0.866, 0.815, 0.024] rim [0.676, 0.726, 0.087]
  - track 263 at frame 266: holes 0, rim-vs-core 0.23, rim-vs-outside 0.26, heterogeneity 0.07; core [0.871, 0.88, 0.024] rim [0.668, 0.784, 0.089]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 457 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.863, rim/outside 13.4 (aggregate of 457 individuals; 1/457 membrane-like individually; rim level 0.783)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.908, rim/outside 3.12 (aggregate of 457 individuals; 0/457 membrane-like individually; rim level 0.836)
  - radial F: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 15.2, rim/outside 0.53 (aggregate of 457 individuals; 0/457 membrane-like individually; rim level 0.435)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #4 (t=2350, R_eq 4.85): none; #15 (t=2350, R_eq 4.15): none; #19 (t=2350, R_eq 4.03): none; #263 (t=2660, R_eq 5.26): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 457 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
