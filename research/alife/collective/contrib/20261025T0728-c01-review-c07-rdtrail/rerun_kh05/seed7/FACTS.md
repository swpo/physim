# Evidence pack: rdtrail (seed 7)

- world: `../../../20261025T0755-c07-kstrail-rd-twin/world.py`, family `reaction-diffusion`
- parent: kstrail; mutation: kstrail with both taxis terms replaced by local threshold kinetics (Laplacian-only twin)
- run: 201 frames x 60 steps x dt 0.05 = time 600; grid [192, 192]; wall 24s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0755-c07-kstrail-rd-twin/world.py --out collective/contrib/20261025T0728-c01-review-c07-rdtrail/rerun_kh05 --seeds 7 8 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9929], min area 6 px

## Measurements
- components: final 19, mean 11.2, max 19; occupancy final 0.24
- tracks: 52; persistent (alive >= 50% of run): 5; longest 135 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.74 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [23, 19, 19], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.117/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 60, default): splits 21, persistent splits 14 (0 more failed only because the siblings re-merged within K), max generation 4, merges 4, merge/split ratio 0.19, nucleations 0
- channel total drift (end/start - 1): [5.5726, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 23 at frame 133: holes 0, rim-vs-core 0.24, rim-vs-outside 0.68, heterogeneity 0.19; core [0.881, 0.672, 0.715] rim [0.694, 0.571, 0.594]
  - track 26 at frame 141: holes 0, rim-vs-core 0.40, rim-vs-outside 0.62, heterogeneity 0.19; core [0.912, 0.774, 0.819] rim [0.638, 0.579, 0.593]
  - track 27 at frame 146: holes 0, rim-vs-core 0.52, rim-vs-outside 0.45, heterogeneity 0.18; core [0.894, 0.755, 0.848] rim [0.544, 0.527, 0.535]
  - track 48 at frame 182: holes 0, rim-vs-core 0.53, rim-vs-outside 0.45, heterogeneity 0.18; core [0.896, 0.761, 0.834] rim [0.539, 0.557, 0.497]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 74 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial u: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.789, rim/outside 8.62 (aggregate of 74 individuals; 0/74 membrane-like individually; rim level 0.715)
  - radial a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.794, rim/outside 3.32 (aggregate of 74 individuals; 0/74 membrane-like individually; rim level 0.606)
  - radial h: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.763, rim/outside 6.36 (aggregate of 74 individuals; 0/74 membrane-like individually; rim level 0.697)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #23 (t=399, R_eq 15.35): none; #26 (t=423, R_eq 16.64): none; #27 (t=438, R_eq 14.95): none; #48 (t=546, R_eq 14.32): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
