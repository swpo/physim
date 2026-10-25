# Evidence pack: neural-field-dep-fork (seed 6)

- world: `../../20261025T1733-c20-neural-comets-metabolic-claim/world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 5s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1733-c20-neural-comets-metabolic-claim/world.py --out collective/contrib/20261025T1943-c19-review-comets-jitter/g2.25 --seeds 6 --spf 50 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 40, mean 40.9, max 69; occupancy final 0.10
- tracks: 869; persistent (alive >= 50% of run): 0; longest 83 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [40, 40, 40], H1 [0, 0, 0]
- motion: 113 long-lived tracks moved >= 1 body length; max speed 0.579/time; max body lengths 27.1
- replication (lineage window K = 20 frames = time 100, default): splits 345, persistent splits 20 (0 more failed only because the siblings re-merged within K), max generation 4, merges 106, merge/split ratio 0.307, nucleations 9
- channel total drift (end/start - 1): [1.0, None, -0.5034, -0.1897]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 600 at frame 150: holes 0, rim-vs-core 0.21, rim-vs-outside 0.93, heterogeneity 0.15; core [0.899, 0.498, 1.0, 0.421] rim [0.701, 0.457, 0.958, 0.463]
  - track 214 at frame 47: holes 0, rim-vs-core 0.24, rim-vs-outside 0.88, heterogeneity 0.15; core [0.929, 0.576, 1.0, 0.362] rim [0.711, 0.49, 0.96, 0.412]
  - track 611 at frame 145: holes 0, rim-vs-core 0.22, rim-vs-outside 0.85, heterogeneity 0.14; core [0.883, 0.519, 1.0, 0.317] rim [0.681, 0.471, 0.946, 0.361]
  - track 795 at frame 180: holes 0, rim-vs-core 0.32, rim-vs-outside 0.83, heterogeneity 0.16; core [0.867, 0.606, 1.0, 0.193] rim [0.639, 0.48, 0.861, 0.312]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 222 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.785, rim/outside 3.05 (aggregate of 222 individuals; 0/222 membrane-like individually; rim level 0.702)
  - radial adaptation a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.867, rim/outside 1.91 (aggregate of 222 individuals; 7/222 membrane-like individually; rim level 0.54)
  - radial firing f(u): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.831, rim/outside 29.5 (aggregate of 222 individuals; 0/222 membrane-like individually; rim level 0.801)
  - radial synaptic resource r: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.44, rim/outside 0.861 (aggregate of 222 individuals; 8/222 membrane-like individually; rim level 0.411)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #600 (t=750, R_eq 5.35): none; #214 (t=235, R_eq 2.71): none; #611 (t=725, R_eq 3.91): none; #795 (t=900, R_eq 2.99): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 222 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
