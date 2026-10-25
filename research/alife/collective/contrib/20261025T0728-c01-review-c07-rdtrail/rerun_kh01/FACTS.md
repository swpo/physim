# Evidence pack: rdtrail_slow5 (seed 7)

- world: `../../20261025T0755-c07-kstrail-rd-twin/world_slow5.py`, family `reaction-diffusion`
- parent: kstrail; mutation: kstrail with both taxis terms replaced by local threshold kinetics (Laplacian-only twin)
- run: 201 frames x 60 steps x dt 0.05 = time 600; grid [192, 192]; wall 24s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0755-c07-kstrail-rd-twin/world_slow5.py --out collective/contrib/20261025T0728-c01-review-c07-rdtrail/rerun_kh01 --seeds 7 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9939], min area 6 px

## Measurements
- components: final 9, mean 6.0, max 11; occupancy final 0.12
- tracks: 56; persistent (alive >= 50% of run): 1; longest 102 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.44 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 11, 8], H1 [0, 0, 0]
- motion: 8 long-lived tracks moved >= 1 body length; max speed 0.236/time; max body lengths 1.8
- replication (lineage window K = 20 frames = time 60, default): splits 22, persistent splits 9 (0 more failed only because the siblings re-merged within K), max generation 5, merges 6, merge/split ratio 0.273, nucleations 0
- channel total drift (end/start - 1): [2.3177, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 28 at frame 138: holes 0, rim-vs-core 0.34, rim-vs-outside 0.50, heterogeneity 0.18; core [0.886, 0.684, 0.652] rim [0.608, 0.536, 0.531]
  - track 24 at frame 119: holes 0, rim-vs-core 0.38, rim-vs-outside 0.53, heterogeneity 0.19; core [0.915, 0.733, 0.636] rim [0.626, 0.538, 0.483]
  - track 36 at frame 170: holes 0, rim-vs-core 0.32, rim-vs-outside 0.21, heterogeneity 0.15; core [0.729, 0.489, 0.738] rim [0.452, 0.39, 0.611]
  - track 35 at frame 166: holes 0, rim-vs-core 0.47, rim-vs-outside 0.40, heterogeneity 0.20; core [0.901, 0.719, 0.686] rim [0.55, 0.496, 0.479]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 39 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial u: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.789, rim/outside 5.96 (aggregate of 39 individuals; 3/39 membrane-like individually; rim level 0.552)
  - radial a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.813, rim/outside 3.05 (aggregate of 39 individuals; 0/39 membrane-like individually; rim level 0.532)
  - radial h: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.821, rim/outside 2.54 (aggregate of 39 individuals; 0/39 membrane-like individually; rim level 0.651)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #28 (t=414, R_eq 19.35): none; #24 (t=357, R_eq 19.57): none; #36 (t=510, R_eq 8.27): none; #35 (t=498, R_eq 14.93): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 39 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
