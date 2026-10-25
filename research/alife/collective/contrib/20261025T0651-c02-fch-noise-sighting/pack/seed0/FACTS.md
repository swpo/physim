# Evidence pack: fch-noise (seed 0)

- world: `world.py`, family `fch-bilayer`
- parent: None; mutation: FCH (Promislow benchmark parameters) started from a noisy solvent bath with amphiphile excess
- run: 151 frames x 100 steps x dt 0.01 = time 150; grid [256, 256]; wall 227s; status ok
- command: `python -m labkit.run collective/contrib/_wip_c02/world.py --out pack/seed0 --seeds 0 --frames 150 --no-movie`
- segmentation: matter > 0.32 of robust range [-0.0185, 1.9246], min area 6 px

## Measurements
- components: final 8, mean 8.3, max 9; occupancy final 0.08
- tracks: 10; persistent (alive >= 50% of run): 8; longest 150 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.85 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [24, 16, 8], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.2
- replication (lineage window K = 20 frames = time 20, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1, merge/split ratio n/a, nucleations 9
- channel total drift (end/start - 1): [0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 76: holes 0, rim-vs-core 0.23, rim-vs-outside 0.37, heterogeneity 0.15; core [0.832] rim [0.6]
  - track 2 at frame 76: holes 0, rim-vs-core 0.20, rim-vs-outside 0.42, heterogeneity 0.15; core [0.827] rim [0.627]
  - track 4 at frame 76: holes 0, rim-vs-core 0.29, rim-vs-outside 0.47, heterogeneity 0.15; core [0.943] rim [0.657]
  - track 5 at frame 76: holes 0, rim-vs-core 0.20, rim-vs-outside 0.41, heterogeneity 0.14; core [0.828] rim [0.628]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 49 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial u+1 (amphiphile): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.542, rim/outside 3.24 (aggregate of 49 individuals; 5/49 membrane-like individually; rim level 0.315)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=76, R_eq 12.55): none; #2 (t=76, R_eq 14.6): none; #4 (t=76, R_eq 14.38): none; #5 (t=76, R_eq 14.64): none

## Warnings
- radial: 5 of 49 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
