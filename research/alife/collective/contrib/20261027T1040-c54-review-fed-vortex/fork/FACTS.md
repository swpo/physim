# Evidence pack: fed-vortices (seed 54)

- world: `../../20261027T0712-c53-fed-vortex-claim/world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 751 frames x 150 steps x dt 0.02 = time 2250; grid [128, 128]; wall 272s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0712-c53-fed-vortex-claim/world.py --out collective/contrib/20261027T1040-c54-review-fed-vortex/fork --seeds 54 --frames 750 --spf 150 --no-movie`
- segmentation: matter > 0.29 of robust range [0.0, 0.2063], min area 6 px

## Measurements
- components: final 0, mean 30.3, max 45; occupancy final 0.00
- tracks: 242; persistent (alive >= 50% of run): 17; longest 683 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 34.17 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 1, 1], H1 [0, 0, 0]
- motion: 125 long-lived tracks moved >= 1 body length; max speed 0.368/time; max body lengths 43.1
- replication (lineage window K = 20 frames = time 60, default): splits 73, persistent splits 34 (0 more failed only because the siblings re-merged within K), max generation 7, merges 58, merge/split ratio 0.795, nucleations 0
- channel total drift (end/start - 1): [-1.0, 0.0007, 1.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 12 at frame 340: holes 0, rim-vs-core 0.77, rim-vs-outside 0.30, heterogeneity 0.21; core [0.818, 0.125, 0.92, 0.724] rim [0.402, 0.321, 0.704, 0.143]
  - track 3 at frame 340: holes 0, rim-vs-core 0.79, rim-vs-outside 0.36, heterogeneity 0.20; core [0.861, 0.136, 0.941, 0.813] rim [0.451, 0.302, 0.731, 0.198]
  - track 4 at frame 340: holes 0, rim-vs-core 0.72, rim-vs-outside 0.31, heterogeneity 0.18; core [0.808, 0.101, 0.056, 0.636] rim [0.4, 0.352, 0.272, 0.141]
  - track 211 at frame 649: holes 0, rim-vs-core 0.65, rim-vs-outside 0.33, heterogeneity 0.17; core [0.797, 0.097, 0.063, 0.632] rim [0.436, 0.306, 0.253, 0.174]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 162 components >= 12 px at frames [126, 252, 378, 498, 624]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.759, rim/outside 18.4 (aggregate of 162 individuals; 0/162 membrane-like individually; rim level 0.684)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 12.3, rim/outside 0.772 (aggregate of 162 individuals; 0/162 membrane-like individually; rim level 0.481)
  - radial vorticity (signed): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.02, rim/outside 0.996 (aggregate of 162 individuals; 0/162 membrane-like individually; rim level 0.485)
  - radial eating: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.692, rim/outside 31.6 (aggregate of 162 individuals; 5/162 membrane-like individually; rim level 0.527)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #12 (t=1020, R_eq 4.15): none; #3 (t=1020, R_eq 3.48): none; #4 (t=1020, R_eq 5.38): none; #211 (t=1947, R_eq 5.23): none

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 162 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
