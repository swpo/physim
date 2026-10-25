# Evidence pack: neural-field-dep-fork (seed 6)

- world: `../../20261025T1733-c20-neural-comets-metabolic-claim/world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 5s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1733-c20-neural-comets-metabolic-claim/world.py --out collective/contrib/20261025T1943-c19-review-comets-jitter/tr55 --seeds 6 --spf 50 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 37, mean 37.2, max 63; occupancy final 0.10
- tracks: 654; persistent (alive >= 50% of run): 2; longest 117 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.75 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [37, 37, 37], H1 [0, 0, 0]
- motion: 117 long-lived tracks moved >= 1 body length; max speed 0.601/time; max body lengths 55.1
- replication (lineage window K = 20 frames = time 100, default): splits 254, persistent splits 28 (0 more failed only because the siblings re-merged within K), max generation 5, merges 65, merge/split ratio 0.256, nucleations 13
- channel total drift (end/start - 1): [1.0, None, -0.5322, -0.203]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 402 at frame 143: holes 0, rim-vs-core 0.21, rim-vs-outside 0.76, heterogeneity 0.12; core [0.808, 0.572, 1.0, 0.063] rim [0.66, 0.492, 0.909, 0.142]
  - track 363 at frame 121: holes 0, rim-vs-core 0.27, rim-vs-outside 0.92, heterogeneity 0.18; core [0.953, 0.486, 1.0, 0.479] rim [0.692, 0.476, 0.945, 0.484]
  - track 470 at frame 155: holes 0, rim-vs-core 0.19, rim-vs-outside 0.95, heterogeneity 0.14; core [0.935, 0.478, 1.0, 0.454] rim [0.751, 0.454, 0.978, 0.481]
  - track 606 at frame 190: holes 0, rim-vs-core 0.24, rim-vs-outside 0.88, heterogeneity 0.16; core [0.932, 0.577, 1.0, 0.44] rim [0.707, 0.521, 0.95, 0.488]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 217 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.798, rim/outside 2.99 (aggregate of 217 individuals; 0/217 membrane-like individually; rim level 0.718)
  - radial adaptation a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.868, rim/outside 1.91 (aggregate of 217 individuals; 8/217 membrane-like individually; rim level 0.534)
  - radial firing f(u): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.877, rim/outside 29.7 (aggregate of 217 individuals; 1/217 membrane-like individually; rim level 0.834)
  - radial synaptic resource r: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.43, rim/outside 0.881 (aggregate of 217 individuals; 7/217 membrane-like individually; rim level 0.406)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #402 (t=715, R_eq 2.11): ['adaptation a']; #363 (t=605, R_eq 3.95): ['adaptation a', 'synaptic resource r']; #470 (t=775, R_eq 4.62): none; #606 (t=950, R_eq 3.91): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 7 of 217 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
