# Evidence pack: fed-vortices (seed 4)

- world: `../../world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 151 frames x 150 steps x dt 0.02 = time 450; grid [128, 128]; wall 43s; status ok
- command: `python -m labkit.run collective/contrib/c53-fvc/world.py --out collective/contrib/c53-fvc/screen --seeds 3 4 5 6 7 8 9 10 --frames 150 --spf 150 --no-movie`
- segmentation: matter > 0.29 of robust range [0.0, 0.2082], min area 6 px

## Measurements
- components: final 28, mean 31.9, max 39; occupancy final 0.13
- tracks: 100; persistent (alive >= 50% of run): 28; longest 151 frames; alive start-to-end: 9
- size of persistent tracks: max/min area ratio 9.11 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 30, 28], H1 [0, 0, 0]
- motion: 39 long-lived tracks moved >= 1 body length; max speed 0.293/time; max body lengths 17.6
- replication (lineage window K = 20 frames = time 60, default): splits 25, persistent splits 8 (0 more failed only because the siblings re-merged within K), max generation 2, merges 12, merge/split ratio 0.48, nucleations 0
- channel total drift (end/start - 1): [-0.5757, 0.1833, 689.8499, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 76: holes 0, rim-vs-core 0.73, rim-vs-outside 0.28, heterogeneity 0.19; core [0.808, 0.112, 0.913, 0.655] rim [0.405, 0.327, 0.697, 0.134]
  - track 1 at frame 76: holes 0, rim-vs-core 0.64, rim-vs-outside 0.33, heterogeneity 0.16; core [0.811, 0.094, 0.045, 0.642] rim [0.454, 0.299, 0.232, 0.184]
  - track 4 at frame 76: holes 0, rim-vs-core 0.75, rim-vs-outside 0.31, heterogeneity 0.19; core [0.821, 0.129, 0.918, 0.726] rim [0.422, 0.288, 0.707, 0.151]
  - track 87 at frame 127: holes 0, rim-vs-core 0.78, rim-vs-outside 0.29, heterogeneity 0.20; core [0.803, 0.183, 0.059, 0.735] rim [0.389, 0.344, 0.267, 0.129]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 189 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.747, rim/outside 15.3 (aggregate of 189 individuals; 1/189 membrane-like individually; rim level 0.679)
  - radial fuel Y: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 9.82, rim/outside 0.78 (aggregate of 189 individuals; 0/189 membrane-like individually; rim level 0.485)
  - radial vorticity (signed): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.953, rim/outside 1.09 (aggregate of 189 individuals; 0/189 membrane-like individually; rim level 0.524)
  - radial eating: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.67, rim/outside 26.1 (aggregate of 189 individuals; 3/189 membrane-like individually; rim level 0.522)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=228, R_eq 4.72): none; #1 (t=228, R_eq 4.72): none; #4 (t=228, R_eq 3.7): none; #87 (t=381, R_eq 3.83): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 189 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
