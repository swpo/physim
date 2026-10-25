# Evidence pack: neural-field-dep-fork (seed 6)

- world: `../../20261025T1733-c20-neural-comets-metabolic-claim/world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 5s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1733-c20-neural-comets-metabolic-claim/world.py --out collective/contrib/20261025T1943-c19-review-comets-jitter/g2.75 --seeds 6 --spf 50 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 37, mean 38.8, max 71; occupancy final 0.09
- tracks: 761; persistent (alive >= 50% of run): 0; longest 95 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [38, 38, 38], H1 [0, 0, 0]
- motion: 123 long-lived tracks moved >= 1 body length; max speed 0.613/time; max body lengths 48.7
- replication (lineage window K = 20 frames = time 100, default): splits 296, persistent splits 17 (0 more failed only because the siblings re-merged within K), max generation 3, merges 89, merge/split ratio 0.301, nucleations 16
- channel total drift (end/start - 1): [1.0, None, -0.5718, -0.1962]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 541 at frame 150: holes 0, rim-vs-core 0.29, rim-vs-outside 0.84, heterogeneity 0.17; core [0.914, 0.534, 1.0, 0.259] rim [0.68, 0.423, 0.909, 0.358]
  - track 565 at frame 156: holes 0, rim-vs-core 0.27, rim-vs-outside 0.90, heterogeneity 0.16; core [0.903, 0.525, 1.0, 0.281] rim [0.676, 0.435, 0.912, 0.363]
  - track 403 at frame 104: holes 0, rim-vs-core 0.20, rim-vs-outside 0.84, heterogeneity 0.14; core [0.83, 0.416, 1.0, 0.19] rim [0.663, 0.407, 0.899, 0.215]
  - track 667 at frame 180: holes 0, rim-vs-core 0.29, rim-vs-outside 0.85, heterogeneity 0.17; core [0.918, 0.555, 1.0, 0.342] rim [0.67, 0.444, 0.887, 0.341]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 215 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.791, rim/outside 2.9 (aggregate of 215 individuals; 0/215 membrane-like individually; rim level 0.71)
  - radial adaptation a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.886, rim/outside 1.95 (aggregate of 215 individuals; 5/215 membrane-like individually; rim level 0.541)
  - radial firing f(u): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.833, rim/outside 27.5 (aggregate of 215 individuals; 1/215 membrane-like individually; rim level 0.8)
  - radial synaptic resource r: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.42, rim/outside 0.874 (aggregate of 215 individuals; 13/215 membrane-like individually; rim level 0.408)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #541 (t=750, R_eq 3.04): none; #565 (t=780, R_eq 3.19): none; #403 (t=520, R_eq 5.32): none; #667 (t=900, R_eq 3.34): ['synaptic resource r']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 215 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
