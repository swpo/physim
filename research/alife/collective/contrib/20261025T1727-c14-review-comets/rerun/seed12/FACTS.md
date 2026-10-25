# Evidence pack: neural-field-dep (seed 12)

- world: `../../world.py`, family `neural-field`
- parent: None; mutation: c20 neural-field comets plus synaptic depression: the coupling output is scaled by a resource r that firing depletes and that recovers on time tr
- run: 201 frames x 50 steps x dt 0.1 = time 1000; grid [128, 128]; wall 6s; status ok
- command: `python -m labkit.run scratch/c14/rev_nc/world.py --out scratch/c14/rev_nc/pack --seeds 11 12 --spf 50 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 34, mean 42.1, max 74; occupancy final 0.09
- tracks: 892; persistent (alive >= 50% of run): 0; longest 83 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [34, 34, 34], H1 [0, 0, 0]
- motion: 120 long-lived tracks moved >= 1 body length; max speed 0.577/time; max body lengths 26.6
- replication (lineage window K = 20 frames = time 100, default): splits 360, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 3, merges 96, merge/split ratio 0.267, nucleations 6
- channel total drift (end/start - 1): [-1.0, None, -0.635, -0.1682]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 547 at frame 138: holes 0, rim-vs-core 0.26, rim-vs-outside 0.90, heterogeneity 0.17; core [0.918, 0.538, 1.0, 0.313] rim [0.688, 0.467, 0.915, 0.376]
  - track 629 at frame 156: holes 0, rim-vs-core 0.24, rim-vs-outside 0.89, heterogeneity 0.16; core [0.898, 0.46, 1.0, 0.392] rim [0.677, 0.42, 0.925, 0.429]
  - track 479 at frame 109: holes 0, rim-vs-core 0.24, rim-vs-outside 0.92, heterogeneity 0.16; core [0.91, 0.588, 1.0, 0.384] rim [0.695, 0.508, 0.942, 0.405]
  - track 830 at frame 190: holes 0, rim-vs-core 0.27, rim-vs-outside 0.86, heterogeneity 0.17; core [0.902, 0.578, 1.0, 0.37] rim [0.676, 0.495, 0.909, 0.451]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 233 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial activity u: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.791, rim/outside 3 (aggregate of 233 individuals; 0/233 membrane-like individually; rim level 0.714)
  - radial adaptation a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.875, rim/outside 1.96 (aggregate of 233 individuals; 9/233 membrane-like individually; rim level 0.548)
  - radial firing f(u): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.86, rim/outside 30.7 (aggregate of 233 individuals; 1/233 membrane-like individually; rim level 0.834)
  - radial synaptic resource r: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.46, rim/outside 0.875 (aggregate of 233 individuals; 7/233 membrane-like individually; rim level 0.413)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #547 (t=690, R_eq 3.48): none; #629 (t=780, R_eq 4.98): none; #479 (t=545, R_eq 2.59): none; #830 (t=950, R_eq 3.83): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 233 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
