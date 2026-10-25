# Evidence pack: lattice-chem-gate (seed 2)

- world: `../../world.py`, family `lattice-artificial-chemistry`
- parent: None; mutation: new class: stochastic lattice gas of reacting particles with pairwise repulsion (Ono-Ikegami type)
- run: 201 frames x 50 steps x dt 1.0 = time 10000; grid [128, 128]; wall 224s; status ok
- command: `python -m labkit.run collective/contrib/c17-latgate-wip/world.py --out collective/contrib/c17-latgate-wip/slowA/seed2 --seeds 2 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 20.0], min area 6 px

## Measurements
- components: final 98, mean 98.8, max 136; occupancy final 0.07
- tracks: 4550; persistent (alive >= 50% of run): 0; longest 61 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [1, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [154, 96, 19], H1 [68, 11, 0]
- motion: 24 long-lived tracks moved >= 1 body length; max speed 0.00943/time; max body lengths 2.7
- replication (lineage window K = 20 frames = time 1000, default): splits 439, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 475, merge/split ratio 1.08, nucleations 3248
- channel total drift (end/start - 1): [2.69, None, -0.674, 1.4613]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 806 at frame 67: holes 0, rim-vs-core 0.16, rim-vs-outside 0.16, heterogeneity 0.19; core [0.549, 0.175, 0.067, 0.319] rim [0.5, 0.31, 0.122, 0.375]
  - track 1343 at frame 87: holes 0, rim-vs-core 0.44, rim-vs-outside 0.28, heterogeneity 0.18; core [0.873, 0.31, 0.017, 0.375] rim [0.471, 0.486, 0.07, 0.412]
  - track 128 at frame 32: holes 0, rim-vs-core 0.45, rim-vs-outside 0.26, heterogeneity 0.17; core [0.804, 0.048, 0.1, 0.208] rim [0.51, 0.357, 0.058, 0.344]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 245 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A (autocatalyst): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.839, rim/outside 2.54 (aggregate of 245 individuals; 29/245 membrane-like individually; rim level 0.505)
  - radial M (membrane): peak at rho=1.15 (in the peak band 0.5-1.5), rim/core 2.42, rim/outside 1.83 (aggregate of 245 individuals; 215/245 membrane-like individually; rim level 0.352)  MEMBRANE-LIKE
  - radial X (food): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.92, rim/outside 0.736 (aggregate of 245 individuals; 26/245 membrane-like individually; rim level 0.19)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): M (membrane)
- membrane-like channels per top track at mid-life: #806 (t=3350, R_eq 2.93): ['A (autocatalyst)', 'M (membrane)']; #1343 (t=4350, R_eq 2.26): ['M (membrane)']; #128 (t=1600, R_eq 2.19): ['M (membrane)']; #1176 (t=3850, R_eq 1.95): ['M (membrane)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 7 of 245 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
