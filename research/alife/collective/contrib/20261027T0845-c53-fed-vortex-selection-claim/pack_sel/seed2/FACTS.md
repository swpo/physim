# Evidence pack: fed-vortices (seed 2)

- world: `../../world.py`, family `fed-vortex`
- parent: None; mutation: -
- run: 1501 frames x 150 steps x dt 0.02 = time 4500; grid [128, 128]; wall 847s; status ok
- command: `python -m labkit.run collective/contrib/c53-fvh/world.py --out collective/contrib/c53-fvh/pack_sel --seeds 1 2 --frames 1500 --spf 150 --no-movie`
- segmentation: matter > 0.28 of robust range [0.0, 0.2139], min area 6 px

## Measurements
- components: final 36, mean 34.8, max 48; occupancy final 0.22
- tracks: 1723; persistent (alive >= 50% of run): 0; longest 409 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 1; holes at thresholds 0.2/0.35/0.5 final [0, 1, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [47, 41, 36], H1 [0, 0, 0]
- motion: 656 long-lived tracks moved >= 1 body length; max speed 0.819/time; max body lengths 52.3
- replication (lineage window K = 20 frames = time 60, default): splits 591, persistent splits 117 (0 more failed only because the siblings re-merged within K), max generation 19, merges 528, merge/split ratio 0.893, nucleations 0
- channel total drift (end/start - 1): [-0.3245, -0.0315, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 68 at frame 227: holes 0, rim-vs-core 0.68, rim-vs-outside 0.38, heterogeneity 0.16; core [0.799, 0.143, 0.906, 0.003] rim [0.408, 0.369, 0.403, 0.001]
  - track 42 at frame 189: holes 0, rim-vs-core 0.64, rim-vs-outside 0.38, heterogeneity 0.15; core [0.782, 0.136, 0.91, 0.003] rim [0.416, 0.346, 0.428, 0.002]
  - track 33 at frame 176: holes 0, rim-vs-core 0.70, rim-vs-outside 0.37, heterogeneity 0.16; core [0.809, 0.155, 0.899, 0.001] rim [0.388, 0.364, 0.381, 0.001]
  - track 1585 at frame 1450: holes 0, rim-vs-core 0.59, rim-vs-outside 0.28, heterogeneity 0.16; core [0.769, 0.191, 0.349, 0.602] rim [0.362, 0.32, 0.141, 0.244]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 210 components >= 12 px at frames [252, 504, 756, 996, 1248, 1500]):
  - radial |vorticity|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.713, rim/outside 8.44 (aggregate of 210 individuals; 1/210 membrane-like individually; rim level 0.577)
  - radial fuel Y: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 6.2, rim/outside 0.803 (aggregate of 210 individuals; 0/210 membrane-like individually; rim level 0.451)
  - radial label a: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.743, rim/outside 9.32 (aggregate of 210 individuals; 4/210 membrane-like individually; rim level 0.29)
  - radial label b: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.681, rim/outside 8.14 (aggregate of 210 individuals; 3/210 membrane-like individually; rim level 0.423)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #68 (t=681, R_eq 4.75): none; #42 (t=567, R_eq 4.69): none; #33 (t=528, R_eq 4.26): none; #1585 (t=4350, R_eq 3.57): none

## Warnings
- radial: 5 of 210 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
