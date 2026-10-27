# Evidence pack: fed-vortices (seed 54)

- world: `../../../20261027T0712-c53-fed-vortex-claim/world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 1001 frames x 150 steps x dt 0.02 = time 3000; grid [128, 128]; wall 353s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0712-c53-fed-vortex-claim/world.py --out collective/contrib/20261027T1040-c54-review-fed-vortex/rerun --seeds 54 55 --frames 1000 --spf 150 --no-movie`
- segmentation: matter > 0.29 of robust range [0.0, 0.2057], min area 6 px

## Measurements
- components: final 30, mean 32.2, max 45; occupancy final 0.14
- tracks: 346; persistent (alive >= 50% of run): 11; longest 851 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.39 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [34, 33, 30], H1 [0, 0, 0]
- motion: 187 long-lived tracks moved >= 1 body length; max speed 0.511/time; max body lengths 47.4
- replication (lineage window K = 20 frames = time 60, default): splits 108, persistent splits 52 (0 more failed only because the siblings re-merged within K), max generation 10, merges 92, merge/split ratio 0.852, nucleations 0
- channel total drift (end/start - 1): [-0.5586, 0.1625, -367.3645, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 429: holes 0, rim-vs-core 0.82, rim-vs-outside 0.29, heterogeneity 0.21; core [0.838, 0.146, 0.93, 0.769] rim [0.406, 0.321, 0.708, 0.136]
  - track 130 at frame 580: holes 0, rim-vs-core 0.73, rim-vs-outside 0.29, heterogeneity 0.19; core [0.81, 0.11, 0.921, 0.656] rim [0.402, 0.323, 0.706, 0.136]
  - track 151 at frame 630: holes 0, rim-vs-core 0.64, rim-vs-outside 0.29, heterogeneity 0.17; core [0.775, 0.109, 0.903, 0.593] rim [0.416, 0.31, 0.713, 0.145]
  - track 315 at frame 933: holes 0, rim-vs-core 0.76, rim-vs-outside 0.30, heterogeneity 0.19; core [0.816, 0.111, 0.058, 0.659] rim [0.393, 0.363, 0.28, 0.131]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 186 components >= 12 px at frames [168, 336, 504, 664, 832, 1000]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.751, rim/outside 16 (aggregate of 186 individuals; 1/186 membrane-like individually; rim level 0.664)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 10.4, rim/outside 0.773 (aggregate of 186 individuals; 0/186 membrane-like individually; rim level 0.483)
  - radial vorticity (signed): peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.08, rim/outside 0.993 (aggregate of 186 individuals; 0/186 membrane-like individually; rim level 0.485)
  - radial eating: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.686, rim/outside 26.4 (aggregate of 186 individuals; 5/186 membrane-like individually; rim level 0.499)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #3 (t=1287, R_eq 3.61): none; #130 (t=1740, R_eq 4.69): none; #151 (t=1890, R_eq 4.95): none; #315 (t=2799, R_eq 5.2): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 186 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
