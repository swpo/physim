# Evidence pack: neural-field-dep (seed 1)

- world: `../../world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 9s; status ok
- command: `python -m labkit.run /tmp/c20nfd/world.py --out /tmp/c20nfd/pack --seeds 0 1 2 --spf 50 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 30, mean 40.5, max 70; occupancy final 0.09
- tracks: 792; persistent (alive >= 50% of run): 2; longest 113 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.38 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 30, 30], H1 [0, 0, 0]
- motion: 116 long-lived tracks moved >= 1 body length; max speed 0.615/time; max body lengths 47.2
- replication (lineage window K = 20 frames = time 100, default): splits 318, persistent splits 27 (0 more failed only because the siblings re-merged within K), max generation 6, merges 85, merge/split ratio 0.267, nucleations 7
- channel total drift (end/start - 1): [1.0, None, -0.5666, -0.1663]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 365 at frame 106: holes 0, rim-vs-core 0.25, rim-vs-outside 0.86, heterogeneity 0.17; core [0.902, 0.468, 1.0, 0.296] rim [0.684, 0.419, 0.924, 0.373]
  - track 527 at frame 146: holes 0, rim-vs-core 0.26, rim-vs-outside 0.91, heterogeneity 0.16; core [0.898, 0.522, 1.0, 0.251] rim [0.651, 0.471, 0.929, 0.281]
  - track 536 at frame 143: holes 0, rim-vs-core 0.21, rim-vs-outside 0.87, heterogeneity 0.15; core [0.887, 0.544, 1.0, 0.307] rim [0.694, 0.499, 0.935, 0.354]
  - track 703 at frame 178: holes 0, rim-vs-core 0.26, rim-vs-outside 0.84, heterogeneity 0.17; core [0.901, 0.544, 1.0, 0.346] rim [0.679, 0.472, 0.891, 0.401]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 215 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.783, rim/outside 2.93 (aggregate of 215 individuals; 0/215 membrane-like individually; rim level 0.701)
  - radial adaptation a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.866, rim/outside 1.93 (aggregate of 215 individuals; 2/215 membrane-like individually; rim level 0.543)
  - radial firing f(u): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.842, rim/outside 29.2 (aggregate of 215 individuals; 1/215 membrane-like individually; rim level 0.809)
  - radial synaptic resource r: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.47, rim/outside 0.864 (aggregate of 215 individuals; 5/215 membrane-like individually; rim level 0.419)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #365 (t=530, R_eq 3.61): none; #527 (t=730, R_eq 3.43): none; #536 (t=715, R_eq 4.18): none; #703 (t=890, R_eq 3.78): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 215 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
