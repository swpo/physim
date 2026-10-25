# Evidence pack: neural-field-dep (seed 7)

- world: `../../world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 8s; status ok
- command: `python -m labkit.run /root/rev5/world.py --out /root/rev5/rerun --seeds 7 8 --spf 50 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 36, mean 39.6, max 68; occupancy final 0.09
- tracks: 701; persistent (alive >= 50% of run): 1; longest 152 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.71 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [36, 36, 36], H1 [0, 0, 0]
- motion: 126 long-lived tracks moved >= 1 body length; max speed 0.607/time; max body lengths 52.1
- replication (lineage window K = 20 frames = time 100, default): splits 282, persistent splits 27 (0 more failed only because the siblings re-merged within K), max generation 8, merges 76, merge/split ratio 0.27, nucleations 8
- channel total drift (end/start - 1): [1.0, None, -0.5573, -0.1747]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 385 at frame 124: holes 0, rim-vs-core 0.17, rim-vs-outside 0.90, heterogeneity 0.15; core [0.88, 0.578, 1.0, 0.23] rim [0.746, 0.514, 0.955, 0.308]
  - track 521 at frame 151: holes 0, rim-vs-core 0.21, rim-vs-outside 0.95, heterogeneity 0.14; core [0.912, 0.532, 1.0, 0.348] rim [0.708, 0.49, 0.97, 0.384]
  - track 515 at frame 148: holes 0, rim-vs-core 0.29, rim-vs-outside 0.89, heterogeneity 0.16; core [0.883, 0.565, 1.0, 0.173] rim [0.649, 0.466, 0.897, 0.271]
  - track 633 at frame 182: holes 0, rim-vs-core 0.29, rim-vs-outside 0.89, heterogeneity 0.17; core [0.937, 0.52, 1.0, 0.437] rim [0.677, 0.449, 0.926, 0.496]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 213 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.789, rim/outside 2.93 (aggregate of 213 individuals; 0/213 membrane-like individually; rim level 0.7)
  - radial adaptation a: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.901, rim/outside 1.96 (aggregate of 213 individuals; 6/213 membrane-like individually; rim level 0.552)
  - radial firing f(u): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.819, rim/outside 26.7 (aggregate of 213 individuals; 1/213 membrane-like individually; rim level 0.787)
  - radial synaptic resource r: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.42, rim/outside 0.876 (aggregate of 213 individuals; 11/213 membrane-like individually; rim level 0.409)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #385 (t=620, R_eq 3.34): ['synaptic resource r']; #521 (t=755, R_eq 3.95): none; #515 (t=740, R_eq 3.09): none; #633 (t=910, R_eq 3.87): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 213 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
