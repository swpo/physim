# Evidence pack: phoretic-colloids (seed 1)

- world: `../../world.py`, family `phoretic-colloids`
- parent: None; mutation: -
- run: 801 frames x 1 steps x dt 0.5 = time 400; grid [128, 128]; wall 118s; status ok
- command: `python -m labkit.run collective/contrib/wip-c33/world.py --out collective/contrib/wip-c33/tpack --seeds 0 1 --frames 800 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5951], min area 6 px

## Measurements
- components: final 18, mean 17.6, max 30; occupancy final 0.06
- tracks: 364; persistent (alive >= 50% of run): 3; longest 602 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.83 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [22, 20, 11], H1 [0, 0, 0]
- motion: 73 long-lived tracks moved >= 1 body length; max speed 0.414/time; max body lengths 9.8
- replication (lineage window K = 20 frames = time 10, default): splits 40, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 4, merges 49, merge/split ratio 1.23, nucleations 235
- channel total drift (end/start - 1): [0.5271, 0.185, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 111 at frame 444: holes 0, rim-vs-core 0.27, rim-vs-outside 0.28, heterogeneity 0.15; core [0.83, 0.161, 0.499] rim [0.567, 0.154, 0.417]
  - track 64 at frame 329: holes 0, rim-vs-core 0.22, rim-vs-outside 0.34, heterogeneity 0.06; core [0.877, 0.0, 0.454] rim [0.663, 0.0, 0.387]
  - track 126 at frame 383: holes 0, rim-vs-core 0.24, rim-vs-outside 0.25, heterogeneity 0.19; core [0.618, 0.59, 0.385] rim [0.484, 0.394, 0.341]
  - track 287 at frame 706: holes 0, rim-vs-core 0.21, rim-vs-outside 0.26, heterogeneity 0.22; core [0.69, 0.342, 0.608] rim [0.515, 0.288, 0.508]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 103 components >= 12 px at frames [134, 269, 403, 531, 666, 800]):
  - radial A density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.837, rim/outside 13.5 (aggregate of 103 individuals; 5/103 membrane-like individually; rim level 0.659)
  - radial B density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.844, rim/outside 10.7 (aggregate of 103 individuals; 39/103 membrane-like individually; rim level 0.332)
  - radial chemicals (sum): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.842, rim/outside 2.42 (aggregate of 103 individuals; 0/103 membrane-like individually; rim level 0.568)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #111 (t=222, R_eq 3.14): ['B density']; #64 (t=164.5, R_eq 2.82): none; #126 (t=191.5, R_eq 2.33): none; #287 (t=353, R_eq 3.78): ['B density']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
