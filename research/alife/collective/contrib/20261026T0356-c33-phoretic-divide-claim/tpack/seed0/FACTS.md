# Evidence pack: phoretic-colloids (seed 0)

- world: `../../world.py`, family `phoretic-colloids`
- parent: None; mutation: -
- run: 801 frames x 1 steps x dt 0.5 = time 400; grid [128, 128]; wall 126s; status ok
- command: `python -m labkit.run collective/contrib/wip-c33/world.py --out collective/contrib/wip-c33/tpack --seeds 0 1 --frames 800 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.5905], min area 6 px

## Measurements
- components: final 16, mean 16.8, max 26; occupancy final 0.05
- tracks: 373; persistent (alive >= 50% of run): 2; longest 541 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.33 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [23, 17, 11], H1 [0, 0, 0]
- motion: 70 long-lived tracks moved >= 1 body length; max speed 0.487/time; max body lengths 7.5
- replication (lineage window K = 20 frames = time 10, default): splits 27, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 4, merges 45, merge/split ratio 1.67, nucleations 274
- channel total drift (end/start - 1): [0.4957, 0.195, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 19 at frame 343: holes 0, rim-vs-core 0.28, rim-vs-outside 0.29, heterogeneity 0.06; core [0.887, 0.0, 0.396] rim [0.609, 0.0, 0.341]
  - track 205 at frame 585: holes 0, rim-vs-core 0.23, rim-vs-outside 0.32, heterogeneity 0.20; core [0.754, 0.295, 0.507] rim [0.541, 0.345, 0.423]
  - track 41 at frame 262: holes 0, rim-vs-core 0.29, rim-vs-outside 0.32, heterogeneity 0.12; core [0.923, 0.13, 0.54] rim [0.647, 0.158, 0.452]
  - track 340 at frame 760: holes 0, rim-vs-core 0.30, rim-vs-outside 0.31, heterogeneity 0.19; core [0.821, 0.292, 0.481] rim [0.534, 0.351, 0.414]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 86 components >= 12 px at frames [134, 269, 403, 531, 666, 800]):
  - radial A density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.8, rim/outside 15.6 (aggregate of 86 individuals; 2/86 membrane-like individually; rim level 0.662)
  - radial B density: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.91, rim/outside 14.1 (aggregate of 86 individuals; 29/86 membrane-like individually; rim level 0.342)
  - radial chemicals (sum): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.821, rim/outside 2.71 (aggregate of 86 individuals; 0/86 membrane-like individually; rim level 0.56)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #19 (t=171.5, R_eq 2.59): none; #205 (t=292.5, R_eq 3.29): ['B density']; #41 (t=131, R_eq 3.24): ['B density']; #340 (t=380, R_eq 2.88): none

## Warnings
- none

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
