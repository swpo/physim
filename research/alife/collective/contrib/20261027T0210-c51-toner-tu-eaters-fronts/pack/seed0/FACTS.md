# Evidence pack: eating-flocks (seed 0)

- world: `../../world.py`, family `polar-active-fluid`
- parent: None; mutation: -
- run: 151 frames x 80 steps x dt 0.25 = time 3000; grid [128, 128]; wall 21s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0210-c51-toner-tu-eaters-fronts/world.py --out collective/contrib/20261027T0210-c51-toner-tu-eaters-fronts/pack --seeds 0 1 --frames 150 --spf 80 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0001, 0.8678], min area 6 px

## Measurements
- components: final 4, mean 6.7, max 29; occupancy final 0.25
- tracks: 522; persistent (alive >= 50% of run): 0; longest 9 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.06, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 6, 4], H1 [1, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 2.9
- replication (lineage window K = 20 frames = time 400, default): splits 13, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 2, merge/split ratio 0.154, nucleations 445
- channel total drift (end/start - 1): [0.716, -0.5204, -0.3041, -7.1281]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 322 at frame 73: holes 0, rim-vs-core 0.25, rim-vs-outside 0.83, heterogeneity 0.14; core [0.824, 0.017, 0.919, 0.038] rim [0.648, 0.152, 0.836, 0.12]
  - track 143 at frame 24: holes 0, rim-vs-core 0.38, rim-vs-outside 0.85, heterogeneity 0.17; core [0.999, 0.003, 0.94, 0.233] rim [0.661, 0.133, 0.826, 0.248]
  - track 487 at frame 132: holes 0, rim-vs-core 0.26, rim-vs-outside 0.54, heterogeneity 0.11; core [0.742, 0.032, 0.903, 0.109] rim [0.565, 0.177, 0.804, 0.18]
  - track 195 at frame 38: holes 0, rim-vs-core 0.31, rim-vs-outside 0.41, heterogeneity 0.15; core [0.765, 0.024, 0.908, 0.19] rim [0.519, 0.157, 0.78, 0.252]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 31 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial density rho: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.728, rim/outside 1.37 (aggregate of 31 individuals; 5/31 membrane-like individually; rim level 0.283)
  - radial food c: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.35, rim/outside 0.965 (aggregate of 31 individuals; 0/31 membrane-like individually; rim level 0.423)
  - radial |p|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.765, rim/outside 1.4 (aggregate of 31 individuals; 5/31 membrane-like individually; rim level 0.397)
  - radial p_x: peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.23, rim/outside 1 (aggregate of 31 individuals; 0/31 membrane-like individually; rim level 0.463)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #322 (t=1460, R_eq 10.91): none; #143 (t=480, R_eq 14.1): none; #487 (t=2640, R_eq 7.11): none; #195 (t=760, R_eq 9.15): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 17 of 31 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
