# Evidence pack: neural-field-dep-fork (seed 24)

- world: `../../../20261025T1733-c20-neural-comets-metabolic-claim/world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 8s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1733-c20-neural-comets-metabolic-claim/world.py --out collective/contrib/20261025T1832-c24-review-comets-metabolic/cut_all/seed24 --seeds 24 --spf 50 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 0, mean 24.6, max 70; occupancy final 0.00
- tracks: 502; persistent (alive >= 50% of run): 0; longest 100 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [57, 27, 5], H1 [41, 7, 0]
- motion: 71 long-lived tracks moved >= 1 body length; max speed 0.585/time; max body lengths 28.0
- replication (lineage window K = 20 frames = time 100, default): splits 193, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 2, merges 47, merge/split ratio 0.244, nucleations 12
- channel total drift (end/start - 1): [-1.0, None, -0.9985, -0.3528]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 231 at frame 64: holes 0, rim-vs-core 0.32, rim-vs-outside 0.83, heterogeneity 0.16; core [0.919, 0.66, 1.0, 0.514] rim [0.687, 0.471, 0.89, 0.577]
  - track 290 at frame 64: holes 0, rim-vs-core 0.31, rim-vs-outside 0.86, heterogeneity 0.16; core [0.932, 0.549, 1.0, 0.452] rim [0.674, 0.429, 0.887, 0.52]
  - track 321 at frame 71: holes 0, rim-vs-core 0.17, rim-vs-outside 0.93, heterogeneity 0.15; core [0.942, 0.475, 1.0, 0.457] rim [0.773, 0.476, 0.964, 0.463]
  - track 353 at frame 82: holes 0, rim-vs-core 0.27, rim-vs-outside 0.86, heterogeneity 0.15; core [0.923, 0.607, 1.0, 0.382] rim [0.697, 0.491, 0.921, 0.38]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 128 components >= 12 px at frames [34, 67, 101, 133]):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.802, rim/outside 3.31 (aggregate of 128 individuals; 0/128 membrane-like individually; rim level 0.746)
  - radial adaptation a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.857, rim/outside 2.06 (aggregate of 128 individuals; 3/128 membrane-like individually; rim level 0.542)
  - radial firing f(u): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.868, rim/outside 33.1 (aggregate of 128 individuals; 0/128 membrane-like individually; rim level 0.848)
  - radial synaptic resource r: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.22, rim/outside 0.916 (aggregate of 128 individuals; 1/128 membrane-like individually; rim level 0.525)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #231 (t=320, R_eq 3.7): none; #290 (t=320, R_eq 3.14): none; #321 (t=355, R_eq 2.99): none; #353 (t=410, R_eq 3.04): none

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 128 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
