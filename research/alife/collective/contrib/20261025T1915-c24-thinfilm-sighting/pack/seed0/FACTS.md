# Evidence pack: thinfilm-active (seed 0)

- world: `../../world.py`, family `thin-film`
- parent: None; mutation: new class: active polar thin-film drops (lubrication + wetting + polarization)
- run: 81 frames x 200 steps x dt 0.25 = time 4000; grid [128, 128]; wall 205s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1915-c24-thinfilm-sighting/world.py --out collective/contrib/20261025T1915-c24-thinfilm-sighting/pack --seeds 0 1 --frames 80 --no-movie`
- segmentation: matter > 0.10 of robust range [0.0447, 4.3956], min area 6 px

## Measurements
- components: final 5, mean 9.6, max 18; occupancy final 0.25
- tracks: 56; persistent (alive >= 50% of run): 7; longest 75 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.76 (1 = constant size)
- enclosures: components with a hole mean 0.04, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [5, 5, 5], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.00804/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 1000, default): splits 11, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 18, merge/split ratio 1.64, nucleations 0
- channel total drift (end/start - 1): [-0.0, 3.822, 1141.7017, -29.4458]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 43: holes 0, rim-vs-core 0.43, rim-vs-outside 0.31, heterogeneity 0.13; core [0.643, 0.959, 0.608, 0.035] rim [0.227, 0.871, 0.593, 0.096]
  - track 36 at frame 43: holes 0, rim-vs-core 0.25, rim-vs-outside 0.21, heterogeneity 0.09; core [0.408, 0.923, 0.919, 0.715] rim [0.182, 0.827, 0.861, 0.698]
  - track 23 at frame 35: holes 0, rim-vs-core 0.35, rim-vs-outside 0.29, heterogeneity 0.11; core [0.561, 0.955, 0.682, 0.053] rim [0.223, 0.866, 0.656, 0.104]
  - track 26 at frame 35: holes 0, rim-vs-core 0.36, rim-vs-outside 0.30, heterogeneity 0.11; core [0.566, 0.953, 0.433, 0.019] rim [0.225, 0.864, 0.445, 0.075]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 58 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial height above precursor h - ha: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.615, rim/outside 6.44 (aggregate of 58 individuals; 0/58 membrane-like individually; rim level 0.389)
  - radial |p| polar order: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.963, rim/outside 2.33 (aggregate of 58 individuals; 0/58 membrane-like individually; rim level 0.898)
  - radial p_x: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.984, rim/outside 1.05 (aggregate of 58 individuals; 0/58 membrane-like individually; rim level 0.532)
  - radial p_y: peak at rho=1.65 (OUTSIDE the peak band 0.5-1.5), rim/core 1.08, rim/outside 0.978 (aggregate of 58 individuals; 0/58 membrane-like individually; rim level 0.435)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #7 (t=2150, R_eq 13.12): none; #36 (t=2150, R_eq 9.08): none; #23 (t=1750, R_eq 11.24): none; #26 (t=1750, R_eq 11.67): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 58 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
