# Evidence pack: reacting-thermals (seed 1)

- world: `../../world.py`, family `reactive-convection`
- parent: None; mutation: -
- run: 601 frames x 25 steps x dt 0.04 = time 600; grid [192, 192]; wall 160s; status ok
- command: `python -m labkit.run collective/contrib/c49wip2/world.py --out collective/contrib/c49wip2/pack_res15 --seeds 0 1 --size 192 192 --frames 600 --spf 25 --no-movie`
- segmentation: matter > 0.39 of robust range [0.0, 0.6421], min area 6 px

## Measurements
- components: final 36, mean 27.1, max 46; occupancy final 0.03
- tracks: 455; persistent (alive >= 50% of run): 0; longest 220 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.03, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [43, 39, 34], H1 [0, 0, 0]
- motion: 225 long-lived tracks moved >= 1 body length; max speed 1.43/time; max body lengths 34.9
- replication (lineage window K = 20 frames = time 20, default): splits 171, persistent splits 75 (0 more failed only because the siblings re-merged within K), max generation 8, merges 9, merge/split ratio 0.053, nucleations 66
- channel total drift (end/start - 1): [-0.799, -0.3614, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 270 at frame 449: holes 0, rim-vs-core 0.32, rim-vs-outside 0.55, heterogeneity 0.15; core [0.965, 0.058, 0.447, 0.985] rim [0.716, 0.121, 0.46, 0.793]
  - track 252 at frame 413: holes 0, rim-vs-core 0.23, rim-vs-outside 0.57, heterogeneity 0.12; core [0.944, 0.146, 0.302, 1.0] rim [0.75, 0.179, 0.323, 0.882]
  - track 169 at frame 297: holes 0, rim-vs-core 0.29, rim-vs-outside 0.43, heterogeneity 0.14; core [0.851, 0.105, 0.63, 0.939] rim [0.657, 0.138, 0.629, 0.724]
  - track 410 at frame 575: holes 0, rim-vs-core 0.23, rim-vs-outside 0.46, heterogeneity 0.14; core [0.902, 0.051, 0.472, 0.928] rim [0.726, 0.099, 0.469, 0.781]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 163 components >= 12 px at frames [101, 202, 303, 398, 499, 600]):
  - radial heat T: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.868, rim/outside 6.01 (aggregate of 163 individuals; 0/163 membrane-like individually; rim level 0.675)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 3.76, rim/outside 0.664 (aggregate of 163 individuals; 0/163 membrane-like individually; rim level 0.203)
  - radial vorticity: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.06, rim/outside 1.05 (aggregate of 163 individuals; 19/163 membrane-like individually; rim level 0.492)
  - radial burn r: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.899, rim/outside 8.27 (aggregate of 163 individuals; 2/163 membrane-like individually; rim level 0.687)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #270 (t=449, R_eq 3.43): none; #252 (t=413, R_eq 2.76): none; #169 (t=297, R_eq 2.52): none; #410 (t=575, R_eq 3.04): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 11 of 163 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
