# Evidence pack: fed-vortices (seed 1)

- world: `../../world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 1001 frames x 150 steps x dt 0.02 = time 3000; grid [128, 128]; wall 285s; status ok
- command: `python -m labkit.run collective/contrib/c53-fvc/world.py --out collective/contrib/c53-fvc/pack_noadv --seeds 0 1 --frames 1000 --spf 150 --no-movie`
- segmentation: matter > 0.28 of robust range [0.0, 0.211], min area 6 px

## Measurements
- components: final 54, mean 53.5, max 54; occupancy final 0.16
- tracks: 87; persistent (alive >= 50% of run): 54; longest 1001 frames; alive start-to-end: 24
- size of persistent tracks: max/min area ratio 3.47 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [54, 54, 54], H1 [0, 0, 0]
- motion: 11 long-lived tracks moved >= 1 body length; max speed 0.00308/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 60, default): splits 19, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [-0.4443, 0.0157, 150.2099, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 504: holes 0, rim-vs-core 0.30, rim-vs-outside 0.63, heterogeneity 0.19; core [0.739, 0.156, 0.097, 0.585] rim [0.578, 0.266, 0.182, 0.371]
  - track 1 at frame 504: holes 0, rim-vs-core 0.74, rim-vs-outside 0.31, heterogeneity 0.20; core [0.791, 0.137, 0.901, 0.671] rim [0.393, 0.382, 0.694, 0.138]
  - track 4 at frame 504: holes 0, rim-vs-core 0.74, rim-vs-outside 0.30, heterogeneity 0.20; core [0.792, 0.133, 0.902, 0.666] rim [0.394, 0.385, 0.694, 0.136]
  - track 57 at frame 513: holes 0, rim-vs-core 0.73, rim-vs-outside 0.31, heterogeneity 0.20; core [0.8, 0.137, 0.071, 0.695] rim [0.41, 0.372, 0.269, 0.155]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 323 components >= 12 px at frames [168, 336, 504, 664, 832, 1000]):
  - radial |vorticity|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.709, rim/outside 38.5 (aggregate of 323 individuals; 0/323 membrane-like individually; rim level 0.688)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 21.4, rim/outside 0.789 (aggregate of 323 individuals; 0/323 membrane-like individually; rim level 0.561)
  - radial vorticity (signed): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.962, rim/outside 1.05 (aggregate of 323 individuals; 0/323 membrane-like individually; rim level 0.513)
  - radial eating: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.575, rim/outside 54.2 (aggregate of 323 individuals; 0/323 membrane-like individually; rim level 0.532)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=1512, R_eq 4.48): none; #1 (t=1512, R_eq 4.18): none; #4 (t=1512, R_eq 4.26): none; #57 (t=1539, R_eq 3.99): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
