# Evidence pack: fed-vortices (seed 46)

- world: `../../../20261027T0712-c53-fed-vortex-claim/world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 1001 frames x 150 steps x dt 0.02 = time 3000; grid [128, 128]; wall 284s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0712-c53-fed-vortex-claim/world.py --out collective/contrib/c57-w18/rerun/seed46 --seeds 46 --frames 1000 --spf 150 --no-movie`
- segmentation: matter > 0.30 of robust range [0.0, 0.2032], min area 6 px

## Measurements
- components: final 25, mean 27.5, max 44; occupancy final 0.14
- tracks: 260; persistent (alive >= 50% of run): 10; longest 1001 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 3.74 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [26, 26, 26], H1 [0, 0, 0]
- motion: 140 long-lived tracks moved >= 1 body length; max speed 0.472/time; max body lengths 35.7
- replication (lineage window K = 20 frames = time 60, default): splits 74, persistent splits 38 (0 more failed only because the siblings re-merged within K), max generation 7, merges 68, merge/split ratio 0.919, nucleations 0
- channel total drift (end/start - 1): [-0.5574, 0.1801, -177.3631, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 504: holes 0, rim-vs-core 0.63, rim-vs-outside 0.39, heterogeneity 0.18; core [0.816, 0.094, 0.924, 0.644] rim [0.457, 0.313, 0.734, 0.212]
  - track 32 at frame 487: holes 0, rim-vs-core 0.77, rim-vs-outside 0.32, heterogeneity 0.20; core [0.837, 0.111, 0.931, 0.723] rim [0.419, 0.31, 0.713, 0.151]
  - track 91 at frame 471: holes 0, rim-vs-core 0.74, rim-vs-outside 0.33, heterogeneity 0.19; core [0.841, 0.098, 0.935, 0.706] rim [0.438, 0.303, 0.724, 0.166]
  - track 229 at frame 950: holes 0, rim-vs-core 0.69, rim-vs-outside 0.31, heterogeneity 0.19; core [0.798, 0.107, 0.914, 0.642] rim [0.412, 0.315, 0.71, 0.147]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 161 components >= 12 px at frames [168, 336, 504, 664, 832, 1000]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.77, rim/outside 18.7 (aggregate of 161 individuals; 1/161 membrane-like individually; rim level 0.683)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 11.9, rim/outside 0.767 (aggregate of 161 individuals; 0/161 membrane-like individually; rim level 0.475)
  - radial vorticity (signed): peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.05, rim/outside 0.991 (aggregate of 161 individuals; 0/161 membrane-like individually; rim level 0.481)
  - radial eating: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.728, rim/outside 30.9 (aggregate of 161 individuals; 3/161 membrane-like individually; rim level 0.525)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #10 (t=1512, R_eq 5.41): none; #32 (t=1461, R_eq 4.48): none; #91 (t=1413, R_eq 4.69): none; #229 (t=2850, R_eq 5.38): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 161 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
