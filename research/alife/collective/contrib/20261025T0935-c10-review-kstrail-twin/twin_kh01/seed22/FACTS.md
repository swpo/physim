# Evidence pack: rdtrail_slow5 (seed 22)

- world: `../../../20261025T0755-c07-kstrail-rd-twin/world_slow5.py`, family `reaction-diffusion`
- parent: kstrail; mutation: kstrail with both taxis terms replaced by local threshold kinetics (Laplacian-only twin)
- run: 201 frames x 60 steps x dt 0.05 = time 600; grid [192, 192]; wall 27s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0755-c07-kstrail-rd-twin/world_slow5.py --out collective/contrib/20261025T0935-c10-review-kstrail-twin/twin_kh01 --seeds 21 22 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9939], min area 6 px

## Measurements
- components: final 8, mean 7.9, max 14; occupancy final 0.16
- tracks: 72; persistent (alive >= 50% of run): 0; longest 88 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 8, 8], H1 [0, 0, 0]
- motion: 10 long-lived tracks moved >= 1 body length; max speed 0.279/time; max body lengths 2.0
- replication (lineage window K = 20 frames = time 60, default): splits 30, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 3, merges 6, merge/split ratio 0.2, nucleations 0
- channel total drift (end/start - 1): [3.1769, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 19 at frame 79: holes 0, rim-vs-core 0.39, rim-vs-outside 0.40, heterogeneity 0.19; core [0.865, 0.712, 0.625] rim [0.543, 0.538, 0.498]
  - track 49 at frame 158: holes 0, rim-vs-core 0.19, rim-vs-outside 0.48, heterogeneity 0.18; core [0.813, 0.578, 0.604] rim [0.637, 0.508, 0.56]
  - track 54 at frame 163: holes 0, rim-vs-core 0.39, rim-vs-outside 0.30, heterogeneity 0.17; core [0.798, 0.589, 0.73] rim [0.49, 0.438, 0.554]
  - track 57 at frame 163: holes 0, rim-vs-core 0.35, rim-vs-outside 0.51, heterogeneity 0.19; core [0.903, 0.682, 0.589] rim [0.608, 0.509, 0.518]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 46 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial u: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.781, rim/outside 8.89 (aggregate of 46 individuals; 2/46 membrane-like individually; rim level 0.63)
  - radial a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.799, rim/outside 3.99 (aggregate of 46 individuals; 0/46 membrane-like individually; rim level 0.567)
  - radial h: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.798, rim/outside 2.8 (aggregate of 46 individuals; 0/46 membrane-like individually; rim level 0.626)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #19 (t=237, R_eq 15.68): none; #49 (t=474, R_eq 11.34): none; #54 (t=489, R_eq 11.66): none; #57 (t=489, R_eq 14.98): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 46 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
