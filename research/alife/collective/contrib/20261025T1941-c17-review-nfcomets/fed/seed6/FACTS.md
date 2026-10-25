# Evidence pack: neural-field-dep-fork (seed 6)

- world: `../../world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 5s; status ok
- command: `python -m labkit.run world.py --out fed --seeds 5 6 --frames 200 --spf 50 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 40, mean 37.8, max 64; occupancy final 0.09
- tracks: 809; persistent (alive >= 50% of run): 0; longest 92 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [40, 40, 40], H1 [0, 0, 0]
- motion: 111 long-lived tracks moved >= 1 body length; max speed 0.597/time; max body lengths 42.1
- replication (lineage window K = 20 frames = time 100, default): splits 319, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 3, merges 93, merge/split ratio 0.292, nucleations 11
- channel total drift (end/start - 1): [1.0, None, -0.5472, -0.1856]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 461 at frame 129: holes 0, rim-vs-core 0.33, rim-vs-outside 0.81, heterogeneity 0.19; core [0.917, 0.536, 1.0, 0.341] rim [0.657, 0.446, 0.843, 0.426]
  - track 471 at frame 126: holes 0, rim-vs-core 0.32, rim-vs-outside 0.91, heterogeneity 0.18; core [0.937, 0.52, 1.0, 0.426] rim [0.691, 0.387, 0.923, 0.551]
  - track 564 at frame 155: holes 0, rim-vs-core 0.31, rim-vs-outside 0.84, heterogeneity 0.17; core [0.898, 0.532, 1.0, 0.213] rim [0.66, 0.41, 0.878, 0.312]
  - track 638 at frame 168: holes 0, rim-vs-core 0.24, rim-vs-outside 0.87, heterogeneity 0.15; core [0.924, 0.607, 1.0, 0.233] rim [0.716, 0.498, 0.956, 0.28]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 212 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.789, rim/outside 2.94 (aggregate of 212 individuals; 0/212 membrane-like individually; rim level 0.706)
  - radial adaptation a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.88, rim/outside 1.95 (aggregate of 212 individuals; 7/212 membrane-like individually; rim level 0.548)
  - radial firing f(u): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.834, rim/outside 27.3 (aggregate of 212 individuals; 1/212 membrane-like individually; rim level 0.803)
  - radial synaptic resource r: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.48, rim/outside 0.881 (aggregate of 212 individuals; 6/212 membrane-like individually; rim level 0.422)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #461 (t=645, R_eq 3.14): none; #471 (t=630, R_eq 3.78): none; #564 (t=775, R_eq 3.48): none; #638 (t=840, R_eq 3.24): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 212 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
