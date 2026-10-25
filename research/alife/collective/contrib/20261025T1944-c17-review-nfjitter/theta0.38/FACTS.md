# Evidence pack: neural-field-dep (seed 7)

- world: `../world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 30 steps x dt 0.1 = time 600; grid [128, 128]; wall 3s; status ok
- command: `python -m labkit.run world.py --out theta0.38 --seeds 7 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 48, mean 55.0, max 82; occupancy final 0.13
- tracks: 1022; persistent (alive >= 50% of run): 0; longest 77 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [49, 49, 48], H1 [0, 0, 0]
- motion: 158 long-lived tracks moved >= 1 body length; max speed 0.609/time; max body lengths 22.1
- replication (lineage window K = 20 frames = time 60, default): splits 412, persistent splits 31 (1 more failed only because the siblings re-merged within K), max generation 4, merges 137, merge/split ratio 0.333, nucleations 8
- channel total drift (end/start - 1): [1.0, None, -0.3648, -0.2266]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 427 at frame 87: holes 0, rim-vs-core 0.26, rim-vs-outside 0.84, heterogeneity 0.16; core [0.911, 0.466, 1.0, 0.226] rim [0.685, 0.425, 0.903, 0.299]
  - track 511 at frame 108: holes 0, rim-vs-core 0.25, rim-vs-outside 0.86, heterogeneity 0.16; core [0.912, 0.51, 1.0, 0.297] rim [0.692, 0.42, 0.934, 0.359]
  - track 410 at frame 79: holes 0, rim-vs-core 0.27, rim-vs-outside 0.86, heterogeneity 0.16; core [0.898, 0.49, 1.0, 0.335] rim [0.659, 0.447, 0.897, 0.391]
  - track 892 at frame 182: holes 0, rim-vs-core 0.26, rim-vs-outside 0.85, heterogeneity 0.18; core [0.898, 0.489, 1.0, 0.352] rim [0.668, 0.441, 0.893, 0.383]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 320 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.798, rim/outside 2.94 (aggregate of 320 individuals; 1/320 membrane-like individually; rim level 0.702)
  - radial adaptation a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.862, rim/outside 1.91 (aggregate of 320 individuals; 13/320 membrane-like individually; rim level 0.542)
  - radial firing f(u): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.862, rim/outside 31.9 (aggregate of 320 individuals; 2/320 membrane-like individually; rim level 0.823)
  - radial synaptic resource r: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.52, rim/outside 0.876 (aggregate of 320 individuals; 18/320 membrane-like individually; rim level 0.36)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #427 (t=261, R_eq 3.39): none; #511 (t=324, R_eq 3.43): none; #410 (t=237, R_eq 3.87): none; #892 (t=546, R_eq 3.52): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 8 of 320 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
