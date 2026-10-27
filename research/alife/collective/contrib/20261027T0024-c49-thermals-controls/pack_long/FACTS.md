# Evidence pack: reacting-thermals (seed 0)

- world: `../world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 2001 frames x 25 steps x dt 0.04 = time 2000; grid [128, 128]; wall 179s; status ok
- command: `python -m labkit.run collective/contrib/c49wip2/world.py --out collective/contrib/c49wip2/pack_long --seeds 0 --frames 2000 --spf 25 --no-movie`
- segmentation: matter > 0.33 of robust range [0.0, 0.7543], min area 6 px

## Measurements
- components: final 27, mean 21.2, max 43; occupancy final 0.02
- tracks: 1682; persistent (alive >= 50% of run): 0; longest 320 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 30, 26], H1 [0, 0, 0]
- motion: 664 long-lived tracks moved >= 1 body length; max speed 1.28/time; max body lengths 42.6
- replication (lineage window K = 20 frames = time 20, default): splits 279, persistent splits 78 (0 more failed only because the siblings re-merged within K), max generation 8, merges 45, merge/split ratio 0.161, nucleations 1055
- channel total drift (end/start - 1): [-0.8695, -0.3368, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 761 at frame 1160: holes 0, rim-vs-core 0.23, rim-vs-outside 0.58, heterogeneity 0.14; core [0.93, 0.0, 0.464, 0.878] rim [0.753, 0.041, 0.513, 0.739]
  - track 1073 at frame 1445: holes 0, rim-vs-core 0.24, rim-vs-outside 0.47, heterogeneity 0.14; core [0.921, 0.0, 0.392, 0.861] rim [0.753, 0.026, 0.483, 0.723]
  - track 341 at frame 605: holes 0, rim-vs-core 0.21, rim-vs-outside 0.62, heterogeneity 0.15; core [0.954, 0.008, 0.522, 0.947] rim [0.796, 0.058, 0.5, 0.819]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 83 components >= 12 px at frames [336, 672, 1008, 1328, 1664, 2000]):
  - radial heat T: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.886, rim/outside 5.52 (aggregate of 83 individuals; 2/83 membrane-like individually; rim level 0.744)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 9.88, rim/outside 0.573 (aggregate of 83 individuals; 0/83 membrane-like individually; rim level 0.164)
  - radial vorticity: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.13, rim/outside 1.08 (aggregate of 83 individuals; 22/83 membrane-like individually; rim level 0.511)
  - radial burn r: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.909, rim/outside 6.82 (aggregate of 83 individuals; 5/83 membrane-like individually; rim level 0.72)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #761 (t=1160, R_eq 2.88): none; #1212 (t=1630, R_eq 1.78): ['vorticity']; #1073 (t=1445, R_eq 2.59): none; #341 (t=605, R_eq 2.26): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 83 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
