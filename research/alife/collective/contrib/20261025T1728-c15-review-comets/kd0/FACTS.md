# Evidence pack: neural-field-dep (seed 7)

- world: `../world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 8s; status ok
- command: `python -m labkit.run /root/rev5/world.py --out /root/rev5/kd0 --seeds 7 --spf 50 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 9, mean 17.7, max 75; occupancy final 0.31
- tracks: 1486; persistent (alive >= 50% of run): 0; longest 24 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 9, 9], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.501/time; max body lengths 6.7
- replication (lineage window K = 20 frames = time 100, default): splits 529, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 469, merge/split ratio 0.887, nucleations 10
- channel total drift (end/start - 1): [1.0, None, 0.5566, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 79 at frame 13: holes 0, rim-vs-core 0.27, rim-vs-outside 0.92, heterogeneity 0.12; core [0.932, 0.543, 1.0, 0.0] rim [0.682, 0.451, 0.949, 0.0]
  - track 273 at frame 25: holes 0, rim-vs-core 0.25, rim-vs-outside 0.91, heterogeneity 0.13; core [0.929, 0.511, 1.0, 0.0] rim [0.693, 0.462, 0.936, 0.0]
  - track 417 at frame 35: holes 0, rim-vs-core 0.28, rim-vs-outside 0.92, heterogeneity 0.13; core [0.919, 0.546, 1.0, 0.0] rim [0.675, 0.436, 0.933, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 78 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.861, rim/outside 1.62 (aggregate of 78 individuals; 0/78 membrane-like individually; rim level 0.538)
  - radial adaptation a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.82, rim/outside 1.25 (aggregate of 78 individuals; 1/78 membrane-like individually; rim level 0.469)
  - radial firing f(u): peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.886, rim/outside 2.55 (aggregate of 78 individuals; 7/78 membrane-like individually; rim level 0.546)
  - radial synaptic resource r: flat profile (no radial structure; level 0; aggregate of 78 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #79 (t=65, R_eq 4.92): none; #606 (t=295, R_eq 13.23, ring): none; #273 (t=125, R_eq 4.82): none; #417 (t=175, R_eq 4.69): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 30 of 78 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
