# Evidence pack: rdtrail (seed 21)

- world: `../../../20261025T0755-c07-kstrail-rd-twin/world.py`, family `reaction-diffusion`
- parent: kstrail; mutation: kstrail with both taxis terms replaced by local threshold kinetics (Laplacian-only twin)
- run: 201 frames x 60 steps x dt 0.05 = time 600; grid [192, 192]; wall 26s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0755-c07-kstrail-rd-twin/world.py --out collective/contrib/20261025T0935-c10-review-kstrail-twin/twin_kh05 --seeds 21 22 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9924], min area 6 px

## Measurements
- components: final 22, mean 12.2, max 22; occupancy final 0.25
- tracks: 52; persistent (alive >= 50% of run): 5; longest 131 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 11.30 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [23, 23, 22], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.177/time; max body lengths 1.0
- replication (lineage window K = 20 frames = time 60, default): splits 22, persistent splits 16 (0 more failed only because the siblings re-merged within K), max generation 4, merges 3, merge/split ratio 0.136, nucleations 0
- channel total drift (end/start - 1): [5.9606, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 17 at frame 136: holes 0, rim-vs-core 0.60, rim-vs-outside 0.44, heterogeneity 0.20; core [0.912, 0.744, 0.785] rim [0.541, 0.488, 0.389]
  - track 19 at frame 138: holes 0, rim-vs-core 0.49, rim-vs-outside 0.56, heterogeneity 0.19; core [0.922, 0.721, 0.798] rim [0.63, 0.519, 0.454]
  - track 21 at frame 141: holes 0, rim-vs-core 0.44, rim-vs-outside 0.75, heterogeneity 0.21; core [0.939, 0.858, 0.871] rim [0.7, 0.645, 0.577]
  - track 37 at frame 166: holes 0, rim-vs-core 0.45, rim-vs-outside 0.36, heterogeneity 0.15; core [0.811, 0.678, 0.883] rim [0.486, 0.509, 0.628]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 84 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial u: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.782, rim/outside 8.26 (aggregate of 84 individuals; 0/84 membrane-like individually; rim level 0.713)
  - radial a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.796, rim/outside 3.02 (aggregate of 84 individuals; 0/84 membrane-like individually; rim level 0.586)
  - radial h: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.76, rim/outside 5.82 (aggregate of 84 individuals; 0/84 membrane-like individually; rim level 0.689)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #17 (t=408, R_eq 16.5): none; #19 (t=414, R_eq 15.43): none; #21 (t=423, R_eq 20.22): none; #37 (t=498, R_eq 12.48): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 84 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
