# Evidence pack: neural-field-dep-fork (seed 0)

- world: `../../world_fork.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 9s; status ok
- command: `python -m labkit.run /tmp/c20nfe/world_fork.py --out /tmp/c20nfe/cut_half --seeds 0 1 --spf 50 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 9, mean 28.4, max 69; occupancy final 0.03
- tracks: 576; persistent (alive >= 50% of run): 0; longest 86 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 9, 9], H1 [0, 0, 0]
- motion: 89 long-lived tracks moved >= 1 body length; max speed 0.587/time; max body lengths 28.9
- replication (lineage window K = 20 frames = time 100, default): splits 225, persistent splits 15 (0 more failed only because the siblings re-merged within K), max generation 4, merges 55, merge/split ratio 0.244, nucleations 10
- channel total drift (end/start - 1): [-1.0, None, -0.8684, -0.2477]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 253 at frame 59: holes 0, rim-vs-core 0.28, rim-vs-outside 0.88, heterogeneity 0.17; core [0.926, 0.5, 1.0, 0.488] rim [0.673, 0.448, 0.894, 0.517]
  - track 149 at frame 40: holes 0, rim-vs-core 0.30, rim-vs-outside 0.83, heterogeneity 0.15; core [0.891, 0.676, 1.0, 0.441] rim [0.665, 0.516, 0.881, 0.476]
  - track 263 at frame 50: holes 0, rim-vs-core 0.27, rim-vs-outside 0.85, heterogeneity 0.17; core [0.914, 0.561, 1.0, 0.448] rim [0.684, 0.508, 0.887, 0.506]
  - track 484 at frame 131: holes 0, rim-vs-core 0.26, rim-vs-outside 0.90, heterogeneity 0.18; core [0.958, 0.54, 1.0, 0.572] rim [0.716, 0.485, 0.923, 0.616]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 145 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.811, rim/outside 2.98 (aggregate of 145 individuals; 0/145 membrane-like individually; rim level 0.71)
  - radial adaptation a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.896, rim/outside 2.02 (aggregate of 145 individuals; 4/145 membrane-like individually; rim level 0.561)
  - radial firing f(u): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.878, rim/outside 24.9 (aggregate of 145 individuals; 3/145 membrane-like individually; rim level 0.809)
  - radial synaptic resource r: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.24, rim/outside 0.916 (aggregate of 145 individuals; 4/145 membrane-like individually; rim level 0.521)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #253 (t=295, R_eq 4.07): none; #149 (t=200, R_eq 3.39): none; #263 (t=250, R_eq 3.14): none; #484 (t=655, R_eq 3.48): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 145 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
