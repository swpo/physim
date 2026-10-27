# Evidence pack: fed-vortices (seed 10)

- world: `../../world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 151 frames x 150 steps x dt 0.02 = time 450; grid [128, 128]; wall 43s; status ok
- command: `python -m labkit.run collective/contrib/c53-fvc/world.py --out collective/contrib/c53-fvc/screen --seeds 3 4 5 6 7 8 9 10 --frames 150 --spf 150 --no-movie`
- segmentation: matter > 0.29 of robust range [0.0, 0.2086], min area 6 px

## Measurements
- components: final 37, mean 38.0, max 46; occupancy final 0.13
- tracks: 91; persistent (alive >= 50% of run): 33; longest 151 frames; alive start-to-end: 17
- size of persistent tracks: max/min area ratio 7.11 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [38, 37, 35], H1 [0, 0, 0]
- motion: 50 long-lived tracks moved >= 1 body length; max speed 0.287/time; max body lengths 14.9
- replication (lineage window K = 20 frames = time 60, default): splits 18, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 2, merges 9, merge/split ratio 0.5, nucleations 0
- channel total drift (end/start - 1): [-0.5548, 0.1467, 46.7779, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 76: holes 0, rim-vs-core 0.66, rim-vs-outside 0.29, heterogeneity 0.18; core [0.762, 0.124, 0.082, 0.59] rim [0.394, 0.333, 0.275, 0.127]
  - track 2 at frame 76: holes 0, rim-vs-core 0.67, rim-vs-outside 0.33, heterogeneity 0.18; core [0.805, 0.11, 0.062, 0.656] rim [0.437, 0.32, 0.252, 0.176]
  - track 4 at frame 76: holes 0, rim-vs-core 0.72, rim-vs-outside 0.29, heterogeneity 0.19; core [0.796, 0.11, 0.908, 0.63] rim [0.389, 0.332, 0.693, 0.125]
  - track 74 at frame 96: holes 0, rim-vs-core 0.68, rim-vs-outside 0.27, heterogeneity 0.18; core [0.761, 0.121, 0.89, 0.577] rim [0.377, 0.35, 0.687, 0.113]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 227 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.73, rim/outside 16.4 (aggregate of 227 individuals; 1/227 membrane-like individually; rim level 0.67)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 10.3, rim/outside 0.783 (aggregate of 227 individuals; 0/227 membrane-like individually; rim level 0.496)
  - radial vorticity (signed): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.01, rim/outside 1.01 (aggregate of 227 individuals; 0/227 membrane-like individually; rim level 0.495)
  - radial eating: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.632, rim/outside 29.2 (aggregate of 227 individuals; 5/227 membrane-like individually; rim level 0.508)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=228, R_eq 5.23): none; #2 (t=228, R_eq 4.51): none; #4 (t=228, R_eq 4.75): none; #74 (t=288, R_eq 5.11): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 227 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
