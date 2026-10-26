# Evidence pack: neural-field-dep (seed 1)

- world: `../../world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 8s; status ok
- command: `python -m labkit.run /tmp/c20nfd/world.py --out /tmp/c20nfd/pack_kd0 --seeds 0 1 --spf 50 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 7, mean 16.3, max 78; occupancy final 0.32
- tracks: 1317; persistent (alive >= 50% of run): 0; longest 22 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 7, 7], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 0.557/time; max body lengths 6.4
- replication (lineage window K = 20 frames = time 100, default): splits 452, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 383, merge/split ratio 0.847, nucleations 5
- channel total drift (end/start - 1): [1.0, None, 0.5981, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 231 at frame 22: holes 0, rim-vs-core 0.21, rim-vs-outside 1.05, heterogeneity 0.13; core [0.978, 0.522, 1.0, 0.0] rim [0.777, 0.5, 0.958, 0.0]
  - track 268 at frame 24: holes 0, rim-vs-core 0.19, rim-vs-outside 1.05, heterogeneity 0.12; core [0.968, 0.557, 1.0, 0.0] rim [0.789, 0.495, 0.966, 0.0]
  - track 552 at frame 50: holes 0, rim-vs-core 0.23, rim-vs-outside 0.91, heterogeneity 0.11; core [0.911, 0.53, 1.0, 0.0] rim [0.693, 0.472, 0.949, 0.0]
  - track 426 at frame 34: holes 0, rim-vs-core 0.19, rim-vs-outside 1.04, heterogeneity 0.12; core [0.969, 0.533, 1.0, 0.0] rim [0.787, 0.479, 0.972, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 60 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.965, rim/outside 1.36 (aggregate of 60 individuals; 1/60 membrane-like individually; rim level 0.49)
  - radial adaptation a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.81, rim/outside 1.12 (aggregate of 60 individuals; 0/60 membrane-like individually; rim level 0.443)
  - radial firing f(u): peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.955, rim/outside 1.77 (aggregate of 60 individuals; 5/60 membrane-like individually; rim level 0.46)
  - radial synaptic resource r: flat profile (no radial structure; level 0; aggregate of 60 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #231 (t=110, R_eq 6.18): none; #268 (t=120, R_eq 9.59, ring): ['activity u', 'adaptation a', 'firing f(u)']; #552 (t=250, R_eq 4.65): none; #426 (t=170, R_eq 7): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 30 of 60 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
