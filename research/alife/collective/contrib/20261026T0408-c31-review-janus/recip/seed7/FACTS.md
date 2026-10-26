# Evidence pack: phoretic-colloids (seed 7)

- world: `../../../20261026T0254-c33-phoretic-janus-claim/world.py`, family `phoretic-colloids`
- parent: None; mutation: -
- run: 401 frames x 1 steps x dt 0.5 = time 200; grid [128, 128]; wall 46s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0254-c33-phoretic-janus-claim/world.py --out collective/contrib/wip-c31/janus/recip --seeds 7 --frames 400 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 1.9899], min area 6 px

## Measurements
- components: final 19, mean 22.3, max 37; occupancy final 0.07
- tracks: 197; persistent (alive >= 50% of run): 14; longest 374 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [20, 19, 17], H1 [0, 0, 0]
- motion: 13 long-lived tracks moved >= 1 body length; max speed 0.203/time; max body lengths 2.1
- replication (lineage window K = 20 frames = time 10, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 24, merge/split ratio n/a, nucleations 173
- channel total drift (end/start - 1): [0.0, 0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 215: holes 0, rim-vs-core 0.28, rim-vs-outside 0.34, heterogeneity 0.12; core [0.886, 0.423, 0.605] rim [0.644, 0.327, 0.502]
  - track 27 at frame 222: holes 0, rim-vs-core 0.25, rim-vs-outside 0.27, heterogeneity 0.12; core [0.778, 0.53, 0.524] rim [0.579, 0.402, 0.454]
  - track 30 at frame 225: holes 0, rim-vs-core 0.29, rim-vs-outside 0.36, heterogeneity 0.15; core [0.803, 0.698, 0.651] rim [0.594, 0.522, 0.544]
  - track 31 at frame 225: holes 0, rim-vs-core 0.31, rim-vs-outside 0.34, heterogeneity 0.19; core [0.79, 0.599, 0.666] rim [0.553, 0.455, 0.534]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 126 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial A density: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.86, rim/outside 20 (aggregate of 126 individuals; 0/126 membrane-like individually; rim level 0.736)
  - radial B density: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.915, rim/outside 15 (aggregate of 126 individuals; 18/126 membrane-like individually; rim level 0.564)
  - radial chemicals (sum): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.867, rim/outside 2.74 (aggregate of 126 individuals; 0/126 membrane-like individually; rim level 0.622)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #5 (t=107.5, R_eq 3.48): none; #27 (t=111, R_eq 2.93): none; #30 (t=112.5, R_eq 3.66): none; #31 (t=112.5, R_eq 3.99): none

## Warnings
- none

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
