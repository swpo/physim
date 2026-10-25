# Evidence pack: neural-field-dep-fork (seed 6)

- world: `../../20261025T1733-c20-neural-comets-metabolic-claim/world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 5s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1733-c20-neural-comets-metabolic-claim/world.py --out collective/contrib/20261025T1943-c19-review-comets-jitter/tr45 --seeds 6 --spf 50 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 51, mean 46.2, max 64; occupancy final 0.12
- tracks: 920; persistent (alive >= 50% of run): 1; longest 130 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.58 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [52, 51, 51], H1 [0, 0, 0]
- motion: 132 long-lived tracks moved >= 1 body length; max speed 0.59/time; max body lengths 55.4
- replication (lineage window K = 20 frames = time 100, default): splits 372, persistent splits 25 (0 more failed only because the siblings re-merged within K), max generation 4, merges 102, merge/split ratio 0.274, nucleations 8
- channel total drift (end/start - 1): [1.0, None, -0.4211, -0.2006]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 395 at frame 116: holes 0, rim-vs-core 0.22, rim-vs-outside 0.85, heterogeneity 0.17; core [0.865, 0.467, 1.0, 0.281] rim [0.672, 0.443, 0.896, 0.324]
  - track 704 at frame 165: holes 0, rim-vs-core 0.25, rim-vs-outside 0.92, heterogeneity 0.16; core [0.949, 0.569, 1.0, 0.409] rim [0.706, 0.508, 0.967, 0.405]
  - track 606 at frame 133: holes 0, rim-vs-core 0.31, rim-vs-outside 0.84, heterogeneity 0.18; core [0.924, 0.609, 1.0, 0.373] rim [0.68, 0.467, 0.903, 0.453]
  - track 844 at frame 190: holes 0, rim-vs-core 0.19, rim-vs-outside 0.86, heterogeneity 0.15; core [0.832, 0.536, 1.0, 0.259] rim [0.673, 0.497, 0.906, 0.279]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 270 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.787, rim/outside 3.01 (aggregate of 270 individuals; 0/270 membrane-like individually; rim level 0.704)
  - radial adaptation a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.885, rim/outside 1.99 (aggregate of 270 individuals; 6/270 membrane-like individually; rim level 0.551)
  - radial firing f(u): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.851, rim/outside 28.9 (aggregate of 270 individuals; 0/270 membrane-like individually; rim level 0.813)
  - radial synaptic resource r: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.48, rim/outside 0.883 (aggregate of 270 individuals; 6/270 membrane-like individually; rim level 0.414)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #395 (t=580, R_eq 4.26): none; #704 (t=825, R_eq 3.48): none; #606 (t=665, R_eq 3.34): none; #844 (t=950, R_eq 4.62): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 270 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
