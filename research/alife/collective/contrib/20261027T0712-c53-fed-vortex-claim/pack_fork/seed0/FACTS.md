# Evidence pack: fed-vortices (seed 0)

- world: `../../world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 751 frames x 150 steps x dt 0.02 = time 2250; grid [128, 128]; wall 208s; status ok
- command: `python -m labkit.run collective/contrib/c53-fvc/world.py --out collective/contrib/c53-fvc/pack_fork --seeds 0 1 --frames 750 --spf 150 --no-movie`
- segmentation: matter > 0.29 of robust range [0.0, 0.2036], min area 6 px

## Measurements
- components: final 0, mean 27.3, max 50; occupancy final 0.00
- tracks: 175; persistent (alive >= 50% of run): 18; longest 690 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 21.50 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 3, 2], H1 [0, 0, 0]
- motion: 96 long-lived tracks moved >= 1 body length; max speed 0.32/time; max body lengths 28.3
- replication (lineage window K = 20 frames = time 60, default): splits 41, persistent splits 15 (0 more failed only because the siblings re-merged within K), max generation 6, merges 44, merge/split ratio 1.07, nucleations 0
- channel total drift (end/start - 1): [-1.0, 0.0305, 1.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 43 at frame 347: holes 0, rim-vs-core 0.77, rim-vs-outside 0.30, heterogeneity 0.19; core [0.822, 0.11, 0.929, 0.676] rim [0.396, 0.348, 0.702, 0.131]
  - track 13 at frame 340: holes 0, rim-vs-core 0.73, rim-vs-outside 0.31, heterogeneity 0.19; core [0.828, 0.103, 0.931, 0.693] rim [0.429, 0.306, 0.72, 0.159]
  - track 21 at frame 340: holes 0, rim-vs-core 0.68, rim-vs-outside 0.30, heterogeneity 0.18; core [0.788, 0.119, 0.91, 0.645] rim [0.416, 0.274, 0.713, 0.139]
  - track 158 at frame 655: holes 0, rim-vs-core 0.81, rim-vs-outside 0.30, heterogeneity 0.21; core [0.831, 0.131, 0.057, 0.756] rim [0.401, 0.323, 0.272, 0.135]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 143 components >= 12 px at frames [126, 252, 378, 498, 624]):
  - radial |vorticity|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.789, rim/outside 21.6 (aggregate of 143 individuals; 1/143 membrane-like individually; rim level 0.704)
  - radial fuel Y: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 14, rim/outside 0.765 (aggregate of 143 individuals; 0/143 membrane-like individually; rim level 0.483)
  - radial vorticity (signed): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.03, rim/outside 0.986 (aggregate of 143 individuals; 0/143 membrane-like individually; rim level 0.481)
  - radial eating: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.767, rim/outside 36.3 (aggregate of 143 individuals; 5/143 membrane-like individually; rim level 0.555)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #43 (t=1041, R_eq 5.11): none; #13 (t=1020, R_eq 4.58): none; #21 (t=1020, R_eq 4.11): none; #158 (t=1965, R_eq 4.11): none

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 143 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
