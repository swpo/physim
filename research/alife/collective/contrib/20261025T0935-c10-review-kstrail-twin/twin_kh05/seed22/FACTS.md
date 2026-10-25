# Evidence pack: rdtrail (seed 22)

- world: `../../../20261025T0755-c07-kstrail-rd-twin/world.py`, family `reaction-diffusion`
- parent: kstrail; mutation: kstrail with both taxis terms replaced by local threshold kinetics (Laplacian-only twin)
- run: 201 frames x 60 steps x dt 0.05 = time 600; grid [192, 192]; wall 26s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0755-c07-kstrail-rd-twin/world.py --out collective/contrib/20261025T0935-c10-review-kstrail-twin/twin_kh05 --seeds 21 22 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.993], min area 6 px

## Measurements
- components: final 20, mean 12.8, max 20; occupancy final 0.23
- tracks: 60; persistent (alive >= 50% of run): 7; longest 161 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.75 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [21, 19, 19], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 20 frames = time 60, default): splits 24, persistent splits 14 (0 more failed only because the siblings re-merged within K), max generation 4, merges 6, merge/split ratio 0.25, nucleations 0
- channel total drift (end/start - 1): [5.3033, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 14 at frame 121: holes 0, rim-vs-core 0.33, rim-vs-outside 0.65, heterogeneity 0.17; core [0.897, 0.805, 0.896] rim [0.656, 0.646, 0.727]
  - track 16 at frame 121: holes 0, rim-vs-core 0.24, rim-vs-outside 0.75, heterogeneity 0.18; core [0.879, 0.859, 0.909] rim [0.701, 0.744, 0.795]
  - track 29 at frame 134: holes 0, rim-vs-core 0.54, rim-vs-outside 0.46, heterogeneity 0.18; core [0.898, 0.669, 0.778] rim [0.551, 0.457, 0.419]
  - track 46 at frame 176: holes 0, rim-vs-core 0.55, rim-vs-outside 0.44, heterogeneity 0.18; core [0.889, 0.706, 0.805] rim [0.532, 0.489, 0.448]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 85 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial u: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.794, rim/outside 6.68 (aggregate of 85 individuals; 0/85 membrane-like individually; rim level 0.72)
  - radial a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.795, rim/outside 2.95 (aggregate of 85 individuals; 0/85 membrane-like individually; rim level 0.589)
  - radial h: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.763, rim/outside 5.06 (aggregate of 85 individuals; 0/85 membrane-like individually; rim level 0.681)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #14 (t=363, R_eq 15.5): none; #16 (t=363, R_eq 18.3): none; #29 (t=402, R_eq 15.51): none; #46 (t=528, R_eq 14.49): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
