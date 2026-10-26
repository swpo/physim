# Evidence pack: phoretic-colloids (seed 1)

- world: `../../world.py`, family `phoretic-colloids`
- parent: None; mutation: -
- run: 401 frames x 1 steps x dt 0.5 = time 200; grid [128, 128]; wall 56s; status ok
- command: `python -m labkit.run collective/contrib/wip-c33/world.py --out collective/contrib/wip-c33/pack --seeds 0 1 --frames 400 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.605], min area 6 px

## Measurements
- components: final 16, mean 23.1, max 39; occupancy final 0.08
- tracks: 223; persistent (alive >= 50% of run): 7; longest 359 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.67 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [23, 19, 13], H1 [0, 0, 0]
- motion: 40 long-lived tracks moved >= 1 body length; max speed 0.431/time; max body lengths 6.2
- replication (lineage window K = 20 frames = time 10, default): splits 8, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 1, merges 39, merge/split ratio 4.88, nucleations 168
- channel total drift (end/start - 1): [0.0, 0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 25 at frame 222: holes 0, rim-vs-core 0.25, rim-vs-outside 0.34, heterogeneity 0.09; core [0.682, 0.571, 0.455] rim [0.581, 0.344, 0.417]
  - track 129 at frame 269: holes 0, rim-vs-core 0.37, rim-vs-outside 0.31, heterogeneity 0.17; core [0.793, 0.421, 0.679] rim [0.465, 0.344, 0.518]
  - track 41 at frame 185: holes 0, rim-vs-core 0.24, rim-vs-outside 0.29, heterogeneity 0.07; core [0.844, 0.059, 0.345] rim [0.619, 0.137, 0.312]
  - track 184 at frame 346: holes 0, rim-vs-core 0.32, rim-vs-outside 0.29, heterogeneity 0.21; core [0.707, 0.556, 0.6] rim [0.483, 0.365, 0.486]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 122 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial A density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.784, rim/outside 15.1 (aggregate of 122 individuals; 2/122 membrane-like individually; rim level 0.644)
  - radial B density: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 0.982, rim/outside 11.5 (aggregate of 122 individuals; 50/122 membrane-like individually; rim level 0.407)
  - radial chemicals (sum): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.809, rim/outside 2.48 (aggregate of 122 individuals; 0/122 membrane-like individually; rim level 0.556)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #25 (t=111, R_eq 2.93): none; #129 (t=134.5, R_eq 4.62): ['B density']; #41 (t=92.5, R_eq 2.03): ['B density']; #184 (t=173, R_eq 4.03): none

## Warnings
- none

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
