# Evidence pack: fed-vortices (seed 0)

- world: `../../world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 1001 frames x 150 steps x dt 0.02 = time 3000; grid [128, 128]; wall 277s; status ok
- command: `python -m labkit.run collective/contrib/c53-fvc/world.py --out collective/contrib/c53-fvc/pack_noadv --seeds 0 1 --frames 1000 --spf 150 --no-movie`
- segmentation: matter > 0.29 of robust range [0.0, 0.21], min area 6 px

## Measurements
- components: final 54, mean 53.2, max 54; occupancy final 0.16
- tracks: 77; persistent (alive >= 50% of run): 54; longest 1001 frames; alive start-to-end: 31
- size of persistent tracks: max/min area ratio 3.47 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [54, 54, 54], H1 [0, 0, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.00415/time; max body lengths 1.7
- replication (lineage window K = 20 frames = time 60, default): splits 14, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [-0.4521, 0.0127, -363.1193, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 504: holes 0, rim-vs-core 0.65, rim-vs-outside 0.50, heterogeneity 0.20; core [0.852, 0.126, 0.054, 0.811] rim [0.513, 0.309, 0.221, 0.309]
  - track 1 at frame 504: holes 0, rim-vs-core 0.78, rim-vs-outside 0.30, heterogeneity 0.20; core [0.798, 0.167, 0.907, 0.733] rim [0.392, 0.368, 0.697, 0.134]
  - track 2 at frame 504: holes 0, rim-vs-core 0.71, rim-vs-outside 0.36, heterogeneity 0.19; core [0.804, 0.115, 0.071, 0.689] rim [0.426, 0.362, 0.266, 0.182]
  - track 67 at frame 521: holes 0, rim-vs-core 0.77, rim-vs-outside 0.31, heterogeneity 0.20; core [0.806, 0.143, 0.911, 0.734] rim [0.406, 0.364, 0.705, 0.15]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 322 components >= 12 px at frames [168, 336, 504, 664, 832, 1000]):
  - radial |vorticity|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.706, rim/outside 39.3 (aggregate of 322 individuals; 0/322 membrane-like individually; rim level 0.687)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 23.5, rim/outside 0.789 (aggregate of 322 individuals; 0/322 membrane-like individually; rim level 0.553)
  - radial vorticity (signed): peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.02, rim/outside 0.998 (aggregate of 322 individuals; 0/322 membrane-like individually; rim level 0.489)
  - radial eating: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.575, rim/outside 55.2 (aggregate of 322 individuals; 0/322 membrane-like individually; rim level 0.542)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=1512, R_eq 3.61): none; #1 (t=1512, R_eq 3.57): none; #2 (t=1512, R_eq 4.37): none; #67 (t=1563, R_eq 3.78): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
