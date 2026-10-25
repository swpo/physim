# Evidence pack: rdtrail (seed 8)

- world: `../../../20261025T0755-c07-kstrail-rd-twin/world.py`, family `reaction-diffusion`
- parent: kstrail; mutation: kstrail with both taxis terms replaced by local threshold kinetics (Laplacian-only twin)
- run: 201 frames x 60 steps x dt 0.05 = time 600; grid [192, 192]; wall 24s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0755-c07-kstrail-rd-twin/world.py --out collective/contrib/20261025T0728-c01-review-c07-rdtrail/rerun_kh05 --seeds 7 8 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9927], min area 6 px

## Measurements
- components: final 23, mean 11.4, max 23; occupancy final 0.25
- tracks: 64; persistent (alive >= 50% of run): 1; longest 115 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.42 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [23, 23, 23], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.117/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 60, default): splits 27, persistent splits 20 (0 more failed only because the siblings re-merged within K), max generation 5, merges 4, merge/split ratio 0.148, nucleations 0
- channel total drift (end/start - 1): [5.8374, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 29 at frame 143: holes 0, rim-vs-core 0.36, rim-vs-outside 0.61, heterogeneity 0.18; core [0.89, 0.657, 0.769] rim [0.64, 0.535, 0.533]
  - track 14 at frame 77: holes 0, rim-vs-core 0.46, rim-vs-outside 0.52, heterogeneity 0.18; core [0.88, 0.85, 0.919] rim [0.553, 0.611, 0.691]
  - track 36 at frame 160: holes 0, rim-vs-core 0.48, rim-vs-outside 0.34, heterogeneity 0.17; core [0.834, 0.671, 0.827] rim [0.489, 0.479, 0.557]
  - track 52 at frame 180: holes 0, rim-vs-core 0.53, rim-vs-outside 0.34, heterogeneity 0.17; core [0.861, 0.605, 0.7] rim [0.5, 0.425, 0.352]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 80 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial u: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.783, rim/outside 9.05 (aggregate of 80 individuals; 0/80 membrane-like individually; rim level 0.706)
  - radial a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.801, rim/outside 3.17 (aggregate of 80 individuals; 0/80 membrane-like individually; rim level 0.577)
  - radial h: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.77, rim/outside 5.89 (aggregate of 80 individuals; 0/80 membrane-like individually; rim level 0.692)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #29 (t=429, R_eq 15.74): none; #14 (t=231, R_eq 18.55): none; #36 (t=480, R_eq 13.54): none; #52 (t=540, R_eq 12.75): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 80 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
