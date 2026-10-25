# Evidence pack: neural-field-dep (seed 3)

- world: `../../c20nfd/world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 8s; status ok
- command: `python -m labkit.run /tmp/c20nfd/world.py --out /tmp/c20jit/tr55 --seeds 3 --spf 50 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 28, mean 35.4, max 73; occupancy final 0.08
- tracks: 642; persistent (alive >= 50% of run): 1; longest 106 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.20 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [28, 28, 28], H1 [0, 0, 0]
- motion: 114 long-lived tracks moved >= 1 body length; max speed 0.593/time; max body lengths 34.0
- replication (lineage window K = 20 frames = time 100, default): splits 251, persistent splits 20 (0 more failed only because the siblings re-merged within K), max generation 3, merges 64, merge/split ratio 0.255, nucleations 8
- channel total drift (end/start - 1): [-1.0, None, -0.6634, -0.174]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 286 at frame 89: holes 0, rim-vs-core 0.27, rim-vs-outside 0.89, heterogeneity 0.16; core [0.927, 0.546, 1.0, 0.304] rim [0.686, 0.473, 0.928, 0.354]
  - track 425 at frame 138: holes 0, rim-vs-core 0.32, rim-vs-outside 0.77, heterogeneity 0.18; core [0.867, 0.545, 1.0, 0.19] rim [0.635, 0.494, 0.806, 0.286]
  - track 204 at frame 47: holes 0, rim-vs-core 0.26, rim-vs-outside 0.87, heterogeneity 0.17; core [0.896, 0.474, 1.0, 0.363] rim [0.662, 0.438, 0.897, 0.405]
  - track 570 at frame 187: holes 0, rim-vs-core 0.31, rim-vs-outside 0.88, heterogeneity 0.17; core [0.947, 0.465, 1.0, 0.404] rim [0.68, 0.372, 0.911, 0.49]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 182 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.78, rim/outside 2.87 (aggregate of 182 individuals; 0/182 membrane-like individually; rim level 0.69)
  - radial adaptation a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.867, rim/outside 2 (aggregate of 182 individuals; 6/182 membrane-like individually; rim level 0.553)
  - radial firing f(u): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.816, rim/outside 23.7 (aggregate of 182 individuals; 1/182 membrane-like individually; rim level 0.773)
  - radial synaptic resource r: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.5, rim/outside 0.894 (aggregate of 182 individuals; 6/182 membrane-like individually; rim level 0.449)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #286 (t=445, R_eq 2.93): none; #425 (t=690, R_eq 3.61): none; #204 (t=235, R_eq 4.26): ['adaptation a']; #570 (t=935, R_eq 3.43): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 182 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
