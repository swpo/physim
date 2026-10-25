# Evidence pack: rdtrail_slow5 (seed 21)

- world: `../../../20261025T0755-c07-kstrail-rd-twin/world_slow5.py`, family `reaction-diffusion`
- parent: kstrail; mutation: kstrail with both taxis terms replaced by local threshold kinetics (Laplacian-only twin)
- run: 201 frames x 60 steps x dt 0.05 = time 600; grid [192, 192]; wall 27s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0755-c07-kstrail-rd-twin/world_slow5.py --out collective/contrib/20261025T0935-c10-review-kstrail-twin/twin_kh01 --seeds 21 22 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9934], min area 6 px

## Measurements
- components: final 10, mean 7.4, max 14; occupancy final 0.13
- tracks: 50; persistent (alive >= 50% of run): 1; longest 131 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.60 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 11, 10], H1 [0, 0, 0]
- motion: 12 long-lived tracks moved >= 1 body length; max speed 0.219/time; max body lengths 2.8
- replication (lineage window K = 20 frames = time 60, default): splits 21, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 3, merges 3, merge/split ratio 0.143, nucleations 0
- channel total drift (end/start - 1): [2.6345, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 23 at frame 136: holes 0, rim-vs-core 0.32, rim-vs-outside 0.20, heterogeneity 0.14; core [0.727, 0.533, 0.676] rim [0.45, 0.438, 0.542]
  - track 31 at frame 158: holes 0, rim-vs-core 0.40, rim-vs-outside 0.32, heterogeneity 0.18; core [0.843, 0.597, 0.625] rim [0.502, 0.435, 0.483]
  - track 33 at frame 161: holes 0, rim-vs-core 0.41, rim-vs-outside 0.32, heterogeneity 0.19; core [0.847, 0.647, 0.652] rim [0.505, 0.479, 0.51]
  - track 38 at frame 163: holes 0, rim-vs-core 0.46, rim-vs-outside 0.42, heterogeneity 0.20; core [0.908, 0.722, 0.673] rim [0.557, 0.499, 0.474]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 48 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial u: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.778, rim/outside 9.49 (aggregate of 48 individuals; 4/48 membrane-like individually; rim level 0.629)
  - radial a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.808, rim/outside 3.64 (aggregate of 48 individuals; 0/48 membrane-like individually; rim level 0.548)
  - radial h: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.814, rim/outside 2.71 (aggregate of 48 individuals; 0/48 membrane-like individually; rim level 0.652)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #23 (t=408, R_eq 8.56): none; #31 (t=474, R_eq 12.13): none; #33 (t=483, R_eq 12.88): none; #38 (t=489, R_eq 15.21): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 48 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
