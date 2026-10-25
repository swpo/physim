# Evidence pack: neural-field-dep (seed 11)

- world: `../../world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 5s; status ok
- command: `python -m labkit.run scratch/c14/rev_nc/world.py --out scratch/c14/rev_nc/pack --seeds 11 12 --spf 50 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 39, mean 38.3, max 70; occupancy final 0.08
- tracks: 827; persistent (alive >= 50% of run): 0; longest 88 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [39, 39, 39], H1 [0, 0, 0]
- motion: 116 long-lived tracks moved >= 1 body length; max speed 0.584/time; max body lengths 26.9
- replication (lineage window K = 20 frames = time 100, default): splits 327, persistent splits 20 (0 more failed only because the siblings re-merged within K), max generation 4, merges 98, merge/split ratio 0.3, nucleations 14
- channel total drift (end/start - 1): [-1.0, None, -0.6316, -0.1827]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 343 at frame 82: holes 0, rim-vs-core 0.24, rim-vs-outside 0.88, heterogeneity 0.18; core [0.925, 0.484, 1.0, 0.508] rim [0.704, 0.479, 0.91, 0.515]
  - track 505 at frame 126: holes 0, rim-vs-core 0.25, rim-vs-outside 0.90, heterogeneity 0.13; core [0.866, 0.555, 1.0, 0.13] rim [0.674, 0.447, 0.943, 0.242]
  - track 116 at frame 37: holes 0, rim-vs-core 0.25, rim-vs-outside 0.85, heterogeneity 0.16; core [0.898, 0.562, 1.0, 0.398] rim [0.685, 0.507, 0.906, 0.456]
  - track 728 at frame 182: holes 0, rim-vs-core 0.26, rim-vs-outside 0.83, heterogeneity 0.14; core [0.877, 0.58, 1.0, 0.113] rim [0.686, 0.502, 0.921, 0.241]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 209 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.787, rim/outside 2.95 (aggregate of 209 individuals; 0/209 membrane-like individually; rim level 0.706)
  - radial adaptation a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.9, rim/outside 2 (aggregate of 209 individuals; 6/209 membrane-like individually; rim level 0.567)
  - radial firing f(u): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.849, rim/outside 27.5 (aggregate of 209 individuals; 0/209 membrane-like individually; rim level 0.811)
  - radial synaptic resource r: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.49, rim/outside 0.878 (aggregate of 209 individuals; 6/209 membrane-like individually; rim level 0.416)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #343 (t=410, R_eq 5.23): none; #505 (t=630, R_eq 2.52): none; #116 (t=185, R_eq 4.03): none; #728 (t=910, R_eq 2.19): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 209 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
