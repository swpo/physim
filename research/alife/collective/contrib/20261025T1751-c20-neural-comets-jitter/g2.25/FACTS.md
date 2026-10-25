# Evidence pack: neural-field-dep (seed 3)

- world: `../../c20nfd/world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 8s; status ok
- command: `python -m labkit.run /tmp/c20nfd/world.py --out /tmp/c20jit/g2.25 --seeds 3 --spf 50 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 35, mean 40.8, max 74; occupancy final 0.09
- tracks: 888; persistent (alive >= 50% of run): 0; longest 70 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [35, 35, 35], H1 [0, 0, 0]
- motion: 117 long-lived tracks moved >= 1 body length; max speed 0.566/time; max body lengths 23.4
- replication (lineage window K = 20 frames = time 100, default): splits 353, persistent splits 19 (0 more failed only because the siblings re-merged within K), max generation 5, merges 103, merge/split ratio 0.292, nucleations 9
- channel total drift (end/start - 1): [-1.0, None, -0.5957, -0.1804]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 269 at frame 54: holes 0, rim-vs-core 0.29, rim-vs-outside 0.88, heterogeneity 0.17; core [0.936, 0.564, 1.0, 0.311] rim [0.697, 0.436, 0.934, 0.4]
  - track 366 at frame 82: holes 0, rim-vs-core 0.26, rim-vs-outside 0.91, heterogeneity 0.16; core [0.935, 0.45, 1.0, 0.327] rim [0.7, 0.361, 0.946, 0.381]
  - track 2 at frame 32: holes 0, rim-vs-core 0.28, rim-vs-outside 0.86, heterogeneity 0.15; core [0.934, 0.633, 1.0, 0.302] rim [0.713, 0.479, 0.97, 0.389]
  - track 759 at frame 183: holes 0, rim-vs-core 0.27, rim-vs-outside 0.87, heterogeneity 0.19; core [0.944, 0.453, 1.0, 0.489] rim [0.687, 0.455, 0.907, 0.515]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 220 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.805, rim/outside 2.98 (aggregate of 220 individuals; 0/220 membrane-like individually; rim level 0.704)
  - radial adaptation a: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.869, rim/outside 1.99 (aggregate of 220 individuals; 5/220 membrane-like individually; rim level 0.559)
  - radial firing f(u): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.871, rim/outside 26.5 (aggregate of 220 individuals; 2/220 membrane-like individually; rim level 0.816)
  - radial synaptic resource r: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.5, rim/outside 0.856 (aggregate of 220 individuals; 9/220 membrane-like individually; rim level 0.415)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #269 (t=270, R_eq 3.34): none; #366 (t=410, R_eq 3.19): none; #2 (t=160, R_eq 3.29): none; #759 (t=915, R_eq 3.48): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 9 of 220 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
