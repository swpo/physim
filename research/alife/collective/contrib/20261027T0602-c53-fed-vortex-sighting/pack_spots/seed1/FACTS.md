# Evidence pack: fed-vortices (seed 1)

- world: `../../world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 301 frames x 150 steps x dt 0.02 = time 900; grid [128, 128]; wall 80s; status ok
- command: `python -m labkit.run collective/contrib/c53-fv/world.py --out collective/contrib/c53-fv/pack_spots --seeds 0 1 --frames 300 --spf 150 --no-movie`
- segmentation: matter > 0.33 of robust range [0.0, 0.1821], min area 6 px

## Measurements
- components: final 3, mean 5.0, max 49; occupancy final 0.02
- tracks: 135; persistent (alive >= 50% of run): 3; longest 301 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 5.93 (1 = constant size)
- enclosures: components with a hole mean 0.03, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [3, 3, 3], H1 [0, 0, 0]
- motion: 7 long-lived tracks moved >= 1 body length; max speed 0.505/time; max body lengths 4.4
- replication (lineage window K = 20 frames = time 60, default): splits 28, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 27, merge/split ratio 0.964, nucleations 0
- channel total drift (end/start - 1): [-0.9346, -0.0395, -94.341, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 22 at frame 151: holes 0, rim-vs-core 0.76, rim-vs-outside 0.30, heterogeneity 0.19; core [0.836, 0.12, 0.953, 0.777] rim [0.455, 0.359, 0.743, 0.195]
  - track 74 at frame 154: holes 0, rim-vs-core 0.66, rim-vs-outside 0.56, heterogeneity 0.18; core [0.893, 0.058, 0.001, 0.829] rim [0.549, 0.309, 0.128, 0.343]
  - track 92 at frame 156: holes 0, rim-vs-core 0.76, rim-vs-outside 0.29, heterogeneity 0.19; core [0.833, 0.122, 0.019, 0.77] rim [0.449, 0.363, 0.189, 0.188]
  - track 32 at frame 15: holes 0, rim-vs-core 0.25, rim-vs-outside 0.37, heterogeneity 0.09; core [0.638, 0.064, 0.074, 0.351] rim [0.498, 0.186, 0.159, 0.214]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 18 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial |vorticity|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.832, rim/outside 42.4 (aggregate of 18 individuals; 0/18 membrane-like individually; rim level 0.807)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 47.3, rim/outside 0.743 (aggregate of 18 individuals; 0/18 membrane-like individually; rim level 0.564)
  - radial vorticity (signed): peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.31, rim/outside 0.954 (aggregate of 18 individuals; 0/18 membrane-like individually; rim level 0.441)
  - radial eating: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.908, rim/outside 79.9 (aggregate of 18 individuals; 0/18 membrane-like individually; rim level 0.789)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #22 (t=453, R_eq 5.86): none; #74 (t=462, R_eq 6.23): none; #92 (t=468, R_eq 5.89): none; #32 (t=45, R_eq 6.43): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
