# Evidence pack: fed-vortices (seed 2)

- world: `../../world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 1001 frames x 150 steps x dt 0.02 = time 3000; grid [128, 128]; wall 289s; status ok
- command: `python -m labkit.run collective/contrib/c53-fvc/world.py --out collective/contrib/c53-fvc/pack --seeds 0 1 2 --frames 1000 --spf 150 --no-movie`
- segmentation: matter > 0.29 of robust range [0.0, 0.2052], min area 6 px

## Measurements
- components: final 23, mean 28.9, max 38; occupancy final 0.13
- tracks: 305; persistent (alive >= 50% of run): 8; longest 979 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.93 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [29, 25, 21], H1 [0, 0, 0]
- motion: 167 long-lived tracks moved >= 1 body length; max speed 0.476/time; max body lengths 46.7
- replication (lineage window K = 20 frames = time 60, default): splits 93, persistent splits 42 (0 more failed only because the siblings re-merged within K), max generation 10, merges 85, merge/split ratio 0.914, nucleations 0
- channel total drift (end/start - 1): [-0.5904, 0.2086, -323.076, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 69 at frame 513: holes 0, rim-vs-core 0.79, rim-vs-outside 0.30, heterogeneity 0.21; core [0.826, 0.126, 0.926, 0.72] rim [0.396, 0.324, 0.702, 0.128]
  - track 107 at frame 597: holes 0, rim-vs-core 0.67, rim-vs-outside 0.32, heterogeneity 0.17; core [0.806, 0.101, 0.92, 0.628] rim [0.428, 0.327, 0.72, 0.162]
  - track 28 at frame 370: holes 0, rim-vs-core 0.46, rim-vs-outside 0.65, heterogeneity 0.21; core [0.846, 0.115, 0.936, 0.751] rim [0.599, 0.245, 0.806, 0.411]
  - track 278 at frame 933: holes 0, rim-vs-core 0.53, rim-vs-outside 0.56, heterogeneity 0.20; core [0.838, 0.133, 0.931, 0.762] rim [0.563, 0.226, 0.79, 0.348]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 163 components >= 12 px at frames [168, 336, 504, 664, 832, 1000]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.772, rim/outside 15.5 (aggregate of 163 individuals; 2/163 membrane-like individually; rim level 0.671)
  - radial fuel Y: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 9.5, rim/outside 0.765 (aggregate of 163 individuals; 0/163 membrane-like individually; rim level 0.472)
  - radial vorticity (signed): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.997, rim/outside 1.01 (aggregate of 163 individuals; 0/163 membrane-like individually; rim level 0.492)
  - radial eating: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.727, rim/outside 25.1 (aggregate of 163 individuals; 7/163 membrane-like individually; rim level 0.509)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #69 (t=1539, R_eq 4.44): none; #107 (t=1791, R_eq 5.23): none; #28 (t=1110, R_eq 4.51): none; #278 (t=2799, R_eq 3.7): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 163 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
