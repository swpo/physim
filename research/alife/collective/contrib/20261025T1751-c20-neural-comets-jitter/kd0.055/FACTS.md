# Evidence pack: neural-field-dep (seed 3)

- world: `../../c20nfd/world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 8s; status ok
- command: `python -m labkit.run /tmp/c20nfd/world.py --out /tmp/c20jit/kd0.055 --seeds 3 --spf 50 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 33, mean 35.2, max 74; occupancy final 0.09
- tracks: 700; persistent (alive >= 50% of run): 0; longest 70 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [33, 33, 33], H1 [0, 0, 0]
- motion: 108 long-lived tracks moved >= 1 body length; max speed 0.59/time; max body lengths 28.1
- replication (lineage window K = 20 frames = time 100, default): splits 281, persistent splits 19 (0 more failed only because the siblings re-merged within K), max generation 3, merges 65, merge/split ratio 0.231, nucleations 7
- channel total drift (end/start - 1): [-1.0, None, -0.6194, -0.1746]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 515 at frame 166: holes 0, rim-vs-core 0.22, rim-vs-outside 0.88, heterogeneity 0.16; core [0.908, 0.53, 1.0, 0.438] rim [0.708, 0.493, 0.937, 0.478]
  - track 440 at frame 131: holes 0, rim-vs-core 0.31, rim-vs-outside 0.78, heterogeneity 0.18; core [0.901, 0.611, 1.0, 0.197] rim [0.679, 0.491, 0.87, 0.314]
  - track 453 at frame 141: holes 0, rim-vs-core 0.24, rim-vs-outside 0.85, heterogeneity 0.16; core [0.902, 0.589, 1.0, 0.248] rim [0.697, 0.527, 0.919, 0.31]
  - track 577 at frame 176: holes 0, rim-vs-core 0.30, rim-vs-outside 0.83, heterogeneity 0.14; core [0.916, 0.454, 1.0, 0.176] rim [0.655, 0.417, 0.855, 0.222]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 188 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.791, rim/outside 2.83 (aggregate of 188 individuals; 0/188 membrane-like individually; rim level 0.69)
  - radial adaptation a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.862, rim/outside 1.93 (aggregate of 188 individuals; 4/188 membrane-like individually; rim level 0.537)
  - radial firing f(u): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.834, rim/outside 24.3 (aggregate of 188 individuals; 2/188 membrane-like individually; rim level 0.778)
  - radial synaptic resource r: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.56, rim/outside 0.882 (aggregate of 188 individuals; 5/188 membrane-like individually; rim level 0.43)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #515 (t=830, R_eq 5.2): none; #440 (t=655, R_eq 2.99): none; #453 (t=705, R_eq 2.82): none; #577 (t=880, R_eq 3.09): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 188 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
