# Evidence pack: phoretic-colloids (seed 3)

- world: `../../../../20261026T0254-c33-phoretic-janus-claim/world.py`, family `phoretic-colloids`
- parent: None; mutation: -
- run: 401 frames x 1 steps x dt 0.5 = time 200; grid [128, 128]; wall 95s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0254-c33-phoretic-janus-claim/world.py --out collective/contrib/wip-c37/phatt/rerun_kd05/seed3 --seeds 3 --frames 400 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.781], min area 6 px

## Measurements
- components: final 20, mean 24.1, max 38; occupancy final 0.07
- tracks: 174; persistent (alive >= 50% of run): 15; longest 382 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [20, 20, 17], H1 [0, 0, 0]
- motion: 26 long-lived tracks moved >= 1 body length; max speed 0.224/time; max body lengths 3.2
- replication (lineage window K = 20 frames = time 10, default): splits 2, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 25, merge/split ratio 12.5, nucleations 145
- channel total drift (end/start - 1): [0.0, 0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 212: holes 0, rim-vs-core 0.32, rim-vs-outside 0.31, heterogeneity 0.16; core [0.739, 0.658, 0.571] rim [0.573, 0.401, 0.474]
  - track 25 at frame 218: holes 0, rim-vs-core 0.34, rim-vs-outside 0.36, heterogeneity 0.15; core [0.706, 0.72, 0.635] rim [0.545, 0.449, 0.512]
  - track 35 at frame 222: holes 0, rim-vs-core 0.18, rim-vs-outside 0.31, heterogeneity 0.13; core [0.495, 0.837, 0.394] rim [0.454, 0.663, 0.349]
  - track 39 at frame 225: holes 0, rim-vs-core 0.26, rim-vs-outside 0.31, heterogeneity 0.11; core [0.851, 0.276, 0.516] rim [0.675, 0.11, 0.429]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 136 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial A density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.876, rim/outside 17.2 (aggregate of 136 individuals; 0/136 membrane-like individually; rim level 0.732)
  - radial B density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.756, rim/outside 24.2 (aggregate of 136 individuals; 7/136 membrane-like individually; rim level 0.542)
  - radial chemicals (sum): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.825, rim/outside 2.83 (aggregate of 136 individuals; 0/136 membrane-like individually; rim level 0.601)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #6 (t=106, R_eq 3.43): none; #25 (t=109, R_eq 3.87): none; #35 (t=111, R_eq 2.33): none; #39 (t=112.5, R_eq 3.29): none

## Warnings
- none

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
