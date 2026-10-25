# Evidence pack: neural-field-dep (seed 0)

- world: `../../world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 8s; status ok
- command: `python -m labkit.run /tmp/c20nfd/world.py --out /tmp/c20nfd/pack_kd0 --seeds 0 1 --spf 50 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 12, mean 27.8, max 76; occupancy final 0.31
- tracks: 1722; persistent (alive >= 50% of run): 0; longest 40 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 12, 12], H1 [0, 0, 0]
- motion: 14 long-lived tracks moved >= 1 body length; max speed 0.571/time; max body lengths 9.3
- replication (lineage window K = 20 frames = time 100, default): splits 621, persistent splits 0 (2 more failed only because the siblings re-merged within K), max generation 0, merges 513, merge/split ratio 0.826, nucleations 5
- channel total drift (end/start - 1): [-1.0, None, 0.3611, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1020 at frame 103: holes 0, rim-vs-core 0.19, rim-vs-outside 1.05, heterogeneity 0.12; core [0.965, 0.518, 1.0, 0.0] rim [0.777, 0.492, 0.973, 0.0]
  - track 1596 at frame 185: holes 0, rim-vs-core 0.18, rim-vs-outside 1.07, heterogeneity 0.12; core [0.971, 0.506, 1.0, 0.0] rim [0.792, 0.478, 0.964, 0.0]
  - track 947 at frame 87: holes 0, rim-vs-core 0.27, rim-vs-outside 0.88, heterogeneity 0.12; core [0.904, 0.509, 1.0, 0.0] rim [0.659, 0.464, 0.91, 0.0]
  - track 1081 at frame 103: holes 0, rim-vs-core 0.27, rim-vs-outside 0.94, heterogeneity 0.11; core [0.921, 0.551, 1.0, 0.0] rim [0.676, 0.454, 0.965, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 136 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.863, rim/outside 1.55 (aggregate of 136 individuals; 10/136 membrane-like individually; rim level 0.509)
  - radial adaptation a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.835, rim/outside 1.19 (aggregate of 136 individuals; 4/136 membrane-like individually; rim level 0.459)
  - radial firing f(u): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.826, rim/outside 2.28 (aggregate of 136 individuals; 23/136 membrane-like individually; rim level 0.489)
  - radial synaptic resource r: flat profile (no radial structure; level 0; aggregate of 136 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1020 (t=515, R_eq 6.93): none; #1596 (t=925, R_eq 7.2): none; #947 (t=435, R_eq 5.59): none; #1081 (t=515, R_eq 3.52): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 51 of 136 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
