# Evidence pack: neural-field-dep-fork (seed 3)

- world: `../../../20261025T1733-c20-neural-comets-metabolic-claim/world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 6s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1733-c20-neural-comets-metabolic-claim/world.py --out collective/contrib/20261025T1815-c19-review-neural-comets/cut_all/seed3 --seeds 3 --spf 50 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 0, mean 23.2, max 73; occupancy final 0.00
- tracks: 571; persistent (alive >= 50% of run): 0; longest 92 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [48, 24, 4], H1 [40, 10, 0]
- motion: 50 long-lived tracks moved >= 1 body length; max speed 0.594/time; max body lengths 30.9
- replication (lineage window K = 20 frames = time 100, default): splits 217, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 2, merges 62, merge/split ratio 0.286, nucleations 9
- channel total drift (end/start - 1): [-1.0, None, -0.9985, -0.3354]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 314 at frame 79: holes 0, rim-vs-core 0.29, rim-vs-outside 0.84, heterogeneity 0.16; core [0.914, 0.621, 1.0, 0.369] rim [0.673, 0.507, 0.894, 0.431]
  - track 327 at frame 69: holes 0, rim-vs-core 0.27, rim-vs-outside 0.87, heterogeneity 0.17; core [0.926, 0.543, 1.0, 0.47] rim [0.697, 0.456, 0.897, 0.533]
  - track 383 at frame 82: holes 0, rim-vs-core 0.22, rim-vs-outside 0.89, heterogeneity 0.13; core [0.962, 0.589, 1.0, 0.494] rim [0.755, 0.538, 0.988, 0.531]
  - track 428 at frame 82: holes 0, rim-vs-core 0.22, rim-vs-outside 0.85, heterogeneity 0.14; core [0.856, 0.563, 1.0, 0.368] rim [0.678, 0.499, 0.897, 0.425]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 106 components >= 12 px at frames [34, 67, 101]):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.8, rim/outside 3.11 (aggregate of 106 individuals; 0/106 membrane-like individually; rim level 0.72)
  - radial adaptation a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.867, rim/outside 1.99 (aggregate of 106 individuals; 5/106 membrane-like individually; rim level 0.55)
  - radial firing f(u): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.86, rim/outside 28.8 (aggregate of 106 individuals; 2/106 membrane-like individually; rim level 0.818)
  - radial synaptic resource r: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.22, rim/outside 0.898 (aggregate of 106 individuals; 1/106 membrane-like individually; rim level 0.519)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #314 (t=395, R_eq 2.99): none; #327 (t=345, R_eq 2.88): none; #383 (t=410, R_eq 3.04): none; #428 (t=410, R_eq 3.78): none

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 106 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
