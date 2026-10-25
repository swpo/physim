# Evidence pack: neural-field-dep (seed 3)

- world: `../../c20nfd/world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 8s; status ok
- command: `python -m labkit.run /tmp/c20nfd/world.py --out /tmp/c20jit/g2.75 --seeds 3 --spf 50 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 29, mean 36.9, max 74; occupancy final 0.09
- tracks: 786; persistent (alive >= 50% of run): 0; longest 76 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [29, 29, 29], H1 [0, 0, 0]
- motion: 101 long-lived tracks moved >= 1 body length; max speed 0.604/time; max body lengths 34.3
- replication (lineage window K = 20 frames = time 100, default): splits 313, persistent splits 14 (0 more failed only because the siblings re-merged within K), max generation 4, merges 83, merge/split ratio 0.265, nucleations 12
- channel total drift (end/start - 1): [-1.0, None, -0.6208, -0.1682]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 465 at frame 116: holes 0, rim-vs-core 0.23, rim-vs-outside 0.87, heterogeneity 0.16; core [0.909, 0.493, 1.0, 0.412] rim [0.694, 0.462, 0.924, 0.421]
  - track 445 at frame 108: holes 0, rim-vs-core 0.26, rim-vs-outside 0.92, heterogeneity 0.16; core [0.934, 0.587, 1.0, 0.382] rim [0.699, 0.511, 0.961, 0.442]
  - track 486 at frame 126: holes 0, rim-vs-core 0.25, rim-vs-outside 0.83, heterogeneity 0.14; core [0.903, 0.567, 1.0, 0.234] rim [0.697, 0.458, 0.95, 0.32]
  - track 676 at frame 176: holes 0, rim-vs-core 0.25, rim-vs-outside 0.79, heterogeneity 0.14; core [0.835, 0.632, 1.0, 0.128] rim [0.666, 0.537, 0.901, 0.253]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 206 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.79, rim/outside 2.78 (aggregate of 206 individuals; 1/206 membrane-like individually; rim level 0.695)
  - radial adaptation a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.895, rim/outside 1.93 (aggregate of 206 individuals; 11/206 membrane-like individually; rim level 0.544)
  - radial firing f(u): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.822, rim/outside 22.9 (aggregate of 206 individuals; 2/206 membrane-like individually; rim level 0.776)
  - radial synaptic resource r: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.44, rim/outside 0.894 (aggregate of 206 individuals; 15/206 membrane-like individually; rim level 0.416)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #465 (t=580, R_eq 4.55): none; #445 (t=540, R_eq 3.19): none; #486 (t=630, R_eq 3.29): none; #676 (t=880, R_eq 2.88): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 206 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
