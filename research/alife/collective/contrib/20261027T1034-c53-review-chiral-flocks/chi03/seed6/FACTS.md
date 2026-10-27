# Evidence pack: chiral-eating-flocks (seed 6)

- world: `../../../20261027T0216-c51-chiral-flocks-negative/world.py`, family `polar-active-fluid`
- parent: None; mutation: -
- run: 301 frames x 40 steps x dt 0.25 = time 3000; grid [128, 128]; wall 29s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0216-c51-chiral-flocks-negative/world.py --out collective/contrib/c53-rev-ch/chi03 --seeds 5 6 --frames 300 --spf 40 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.763], min area 6 px

## Measurements
- components: final 20, mean 15.1, max 26; occupancy final 0.21
- tracks: 2531; persistent (alive >= 50% of run): 0; longest 11 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.13, final 0; holes at thresholds 0.2/0.35/0.5 final [1, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [25, 19, 12], H1 [4, 1, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 2.7
- replication (lineage window K = 20 frames = time 200, default): splits 904, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 864, merge/split ratio 0.956, nucleations 45
- channel total drift (end/start - 1): [0.6311, -0.4521, -0.3559, -1.5591]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 68 at frame 13: holes 0, rim-vs-core 0.26, rim-vs-outside 0.30, heterogeneity 0.10; core [0.659, 0.338, 0.757, 0.262] rim [0.475, 0.44, 0.619, 0.326]
  - track 163 at frame 30: holes 0, rim-vs-core 0.20, rim-vs-outside 0.24, heterogeneity 0.11; core [0.589, 0.193, 0.817, 0.241] rim [0.456, 0.288, 0.705, 0.289]
  - track 47 at frame 10: holes 0, rim-vs-core 0.25, rim-vs-outside 0.69, heterogeneity 0.17; core [0.742, 0.088, 0.893, 0.29] rim [0.613, 0.23, 0.811, 0.436]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 97 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial density rho: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.864, rim/outside 2.7 (aggregate of 97 individuals; 7/97 membrane-like individually; rim level 0.462)
  - radial food c: peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 2.81, rim/outside 0.848 (aggregate of 97 individuals; 0/97 membrane-like individually; rim level 0.446)
  - radial |p|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.883, rim/outside 2.76 (aggregate of 97 individuals; 4/97 membrane-like individually; rim level 0.66)
  - radial p_x: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.07, rim/outside 0.983 (aggregate of 97 individuals; 0/97 membrane-like individually; rim level 0.457)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #68 (t=130, R_eq 2.88): none; #163 (t=300, R_eq 4.07): none; #47 (t=100, R_eq 6.48): none; #601 (t=860, R_eq 2.26): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 18 of 97 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
