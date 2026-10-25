# Evidence pack: neural-field-dep (seed 7)

- world: `../world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 30 steps x dt 0.1 = time 600; grid [128, 128]; wall 3s; status ok
- command: `python -m labkit.run world.py --out g2.75 --seeds 7 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 44, mean 40.0, max 69; occupancy final 0.11
- tracks: 646; persistent (alive >= 50% of run): 3; longest 112 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.38 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [44, 44, 44], H1 [0, 0, 0]
- motion: 129 long-lived tracks moved >= 1 body length; max speed 0.618/time; max body lengths 25.2
- replication (lineage window K = 20 frames = time 60, default): splits 250, persistent splits 28 (0 more failed only because the siblings re-merged within K), max generation 4, merges 96, merge/split ratio 0.384, nucleations 6
- channel total drift (end/start - 1): [1.0, None, -0.4623, -0.1983]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 254 at frame 76: holes 0, rim-vs-core 0.26, rim-vs-outside 0.88, heterogeneity 0.15; core [0.898, 0.566, 1.0, 0.171] rim [0.67, 0.482, 0.924, 0.226]
  - track 242 at frame 72: holes 0, rim-vs-core 0.17, rim-vs-outside 0.93, heterogeneity 0.16; core [0.89, 0.48, 1.0, 0.235] rim [0.727, 0.473, 0.943, 0.259]
  - track 368 at frame 114: holes 0, rim-vs-core 0.30, rim-vs-outside 0.87, heterogeneity 0.17; core [0.916, 0.6, 1.0, 0.393] rim [0.671, 0.507, 0.888, 0.483]
  - track 555 at frame 182: holes 0, rim-vs-core 0.20, rim-vs-outside 0.86, heterogeneity 0.12; core [0.916, 0.556, 1.0, 0.209] rim [0.726, 0.503, 0.982, 0.254]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 223 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.79, rim/outside 2.88 (aggregate of 223 individuals; 0/223 membrane-like individually; rim level 0.712)
  - radial adaptation a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.866, rim/outside 1.92 (aggregate of 223 individuals; 1/223 membrane-like individually; rim level 0.536)
  - radial firing f(u): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.848, rim/outside 29.8 (aggregate of 223 individuals; 0/223 membrane-like individually; rim level 0.82)
  - radial synaptic resource r: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.48, rim/outside 0.894 (aggregate of 223 individuals; 9/223 membrane-like individually; rim level 0.414)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #254 (t=228, R_eq 2.99): none; #242 (t=216, R_eq 3.48): none; #368 (t=342, R_eq 3.39): none; #555 (t=546, R_eq 2.82): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 223 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
