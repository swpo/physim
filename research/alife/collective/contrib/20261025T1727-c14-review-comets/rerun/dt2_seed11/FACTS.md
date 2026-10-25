# Evidence pack: neural-field-dep (seed 11)

- world: `../world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 100 steps x dt 0.1 = time 2000; grid [128, 128]; wall 10s; status ok
- command: `python -m labkit.run scratch/c14/rev_nc/world.py --out scratch/c14/rev_nc/pack_dt2 --seeds 11 --spf 100 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 37, mean 40.5, max 70; occupancy final 0.09
- tracks: 835; persistent (alive >= 50% of run): 0; longest 88 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [37, 37, 37], H1 [0, 0, 0]
- motion: 126 long-lived tracks moved >= 1 body length; max speed 0.286/time; max body lengths 27.3
- replication (lineage window K = 20 frames = time 200, default): splits 328, persistent splits 21 (0 more failed only because the siblings re-merged within K), max generation 4, merges 106, merge/split ratio 0.323, nucleations 6
- channel total drift (end/start - 1): [-1.0, None, -0.5987, -0.1732]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 592 at frame 156: holes 0, rim-vs-core 0.22, rim-vs-outside 0.84, heterogeneity 0.15; core [0.884, 0.561, 1.0, 0.214] rim [0.704, 0.471, 0.927, 0.277]
  - track 614 at frame 163: holes 0, rim-vs-core 0.21, rim-vs-outside 0.89, heterogeneity 0.16; core [0.862, 0.483, 1.0, 0.325] rim [0.67, 0.463, 0.91, 0.355]
  - track 298 at frame 59: holes 0, rim-vs-core 0.27, rim-vs-outside 0.86, heterogeneity 0.17; core [0.938, 0.659, 1.0, 0.301] rim [0.722, 0.525, 0.936, 0.368]
  - track 790 at frame 190: holes 0, rim-vs-core 0.26, rim-vs-outside 0.91, heterogeneity 0.16; core [0.925, 0.575, 1.0, 0.441] rim [0.687, 0.507, 0.94, 0.493]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 229 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.796, rim/outside 3.04 (aggregate of 229 individuals; 0/229 membrane-like individually; rim level 0.715)
  - radial adaptation a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.873, rim/outside 1.92 (aggregate of 229 individuals; 14/229 membrane-like individually; rim level 0.539)
  - radial firing f(u): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.864, rim/outside 29.7 (aggregate of 229 individuals; 3/229 membrane-like individually; rim level 0.832)
  - radial synaptic resource r: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.41, rim/outside 0.861 (aggregate of 229 individuals; 8/229 membrane-like individually; rim level 0.406)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #592 (t=1560, R_eq 3.57): none; #614 (t=1630, R_eq 5.23): none; #298 (t=590, R_eq 3.34): none; #790 (t=1900, R_eq 3.7): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 229 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
