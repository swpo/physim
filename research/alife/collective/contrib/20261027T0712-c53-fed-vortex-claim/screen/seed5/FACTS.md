# Evidence pack: fed-vortices (seed 5)

- world: `../../world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 151 frames x 150 steps x dt 0.02 = time 450; grid [128, 128]; wall 43s; status ok
- command: `python -m labkit.run collective/contrib/c53-fvc/world.py --out collective/contrib/c53-fvc/screen --seeds 3 4 5 6 7 8 9 10 --frames 150 --spf 150 --no-movie`
- segmentation: matter > 0.29 of robust range [0.0, 0.207], min area 6 px

## Measurements
- components: final 30, mean 31.1, max 37; occupancy final 0.13
- tracks: 114; persistent (alive >= 50% of run): 29; longest 151 frames; alive start-to-end: 5
- size of persistent tracks: max/min area ratio 35.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [32, 31, 31], H1 [0, 0, 0]
- motion: 44 long-lived tracks moved >= 1 body length; max speed 0.308/time; max body lengths 11.2
- replication (lineage window K = 20 frames = time 60, default): splits 29, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 3, merges 18, merge/split ratio 0.621, nucleations 0
- channel total drift (end/start - 1): [-0.5942, 0.1941, 344.9534, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 9 at frame 76: holes 0, rim-vs-core 0.51, rim-vs-outside 0.56, heterogeneity 0.20; core [0.827, 0.116, 0.924, 0.712] rim [0.554, 0.228, 0.782, 0.318]
  - track 19 at frame 76: holes 0, rim-vs-core 0.79, rim-vs-outside 0.31, heterogeneity 0.21; core [0.831, 0.122, 0.926, 0.746] rim [0.41, 0.312, 0.705, 0.148]
  - track 29 at frame 76: holes 0, rim-vs-core 0.74, rim-vs-outside 0.29, heterogeneity 0.19; core [0.812, 0.107, 0.054, 0.662] rim [0.4, 0.315, 0.265, 0.128]
  - track 98 at frame 127: holes 0, rim-vs-core 0.68, rim-vs-outside 0.28, heterogeneity 0.18; core [0.765, 0.157, 0.072, 0.641] rim [0.397, 0.312, 0.266, 0.127]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 184 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.748, rim/outside 13.2 (aggregate of 184 individuals; 2/184 membrane-like individually; rim level 0.662)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 8.06, rim/outside 0.787 (aggregate of 184 individuals; 0/184 membrane-like individually; rim level 0.464)
  - radial vorticity (signed): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.978, rim/outside 1.04 (aggregate of 184 individuals; 0/184 membrane-like individually; rim level 0.501)
  - radial eating: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.66, rim/outside 23.1 (aggregate of 184 individuals; 5/184 membrane-like individually; rim level 0.498)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #9 (t=228, R_eq 4.51): none; #19 (t=228, R_eq 4.11): none; #29 (t=228, R_eq 4.62): none; #98 (t=381, R_eq 4.95): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 184 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
