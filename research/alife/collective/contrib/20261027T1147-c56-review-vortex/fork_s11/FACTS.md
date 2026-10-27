# Evidence pack: fed-vortices (seed 11)

- world: `../../../collective/contrib/20261027T0712-c53-fed-vortex-claim/world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 751 frames x 150 steps x dt 0.02 = time 2250; grid [128, 128]; wall 247s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0712-c53-fed-vortex-claim/world.py --out c56work/vx/fork_s11 --seeds 11 --frames 750 --spf 150 --no-movie`
- segmentation: matter > 0.29 of robust range [0.0, 0.2056], min area 6 px

## Measurements
- components: final 0, mean 27.7, max 39; occupancy final 0.00
- tracks: 243; persistent (alive >= 50% of run): 11; longest 679 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 20.12 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 8, 2], H1 [0, 0, 0]
- motion: 130 long-lived tracks moved >= 1 body length; max speed 0.444/time; max body lengths 30.0
- replication (lineage window K = 20 frames = time 60, default): splits 73, persistent splits 27 (0 more failed only because the siblings re-merged within K), max generation 6, merges 58, merge/split ratio 0.795, nucleations 0
- channel total drift (end/start - 1): [-1.0, -0.0235, 1.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 43 at frame 347: holes 0, rim-vs-core 0.54, rim-vs-outside 0.53, heterogeneity 0.20; core [0.828, 0.125, 0.05, 0.741] rim [0.543, 0.246, 0.19, 0.326]
  - track 59 at frame 347: holes 0, rim-vs-core 0.73, rim-vs-outside 0.32, heterogeneity 0.19; core [0.828, 0.103, 0.045, 0.698] rim [0.427, 0.318, 0.246, 0.161]
  - track 26 at frame 328: holes 0, rim-vs-core 0.73, rim-vs-outside 0.34, heterogeneity 0.20; core [0.825, 0.109, 0.049, 0.719] rim [0.43, 0.299, 0.245, 0.173]
  - track 183 at frame 580: holes 0, rim-vs-core 0.69, rim-vs-outside 0.33, heterogeneity 0.19; core [0.823, 0.095, 0.921, 0.681] rim [0.443, 0.286, 0.718, 0.18]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 153 components >= 12 px at frames [126, 252, 378, 498, 624]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.747, rim/outside 15.8 (aggregate of 153 individuals; 1/153 membrane-like individually; rim level 0.669)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 11.4, rim/outside 0.776 (aggregate of 153 individuals; 0/153 membrane-like individually; rim level 0.466)
  - radial vorticity (signed): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.946, rim/outside 1.11 (aggregate of 153 individuals; 0/153 membrane-like individually; rim level 0.537)
  - radial eating: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.677, rim/outside 26.5 (aggregate of 153 individuals; 2/153 membrane-like individually; rim level 0.507)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #43 (t=1041, R_eq 4.15): none; #59 (t=1041, R_eq 4.85): none; #26 (t=984, R_eq 4.41): none; #183 (t=1740, R_eq 4.44): none

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 153 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
