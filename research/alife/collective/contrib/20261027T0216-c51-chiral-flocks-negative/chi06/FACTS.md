# Evidence pack: chiral-eating-flocks (seed 0)

- world: `../../w2.py`, family `polar-active-fluid`
- parent: None; mutation: -
- run: 301 frames x 40 steps x dt 0.25 = time 3000; grid [128, 128]; wall 20s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/77ac260a-0f32-5d82-b241-4f9c69dcdb08/scratchpad/tt/w2.py --out /tmp/claude-0/-home-user-physim/77ac260a-0f32-5d82-b241-4f9c69dcdb08/scratchpad/tt/packs/chi06 --seeds 0 --frames 300 --spf 40 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.6805], min area 6 px

## Measurements
- components: final 16, mean 16.2, max 33; occupancy final 0.22
- tracks: 2547; persistent (alive >= 50% of run): 0; longest 13 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.12, final 0; holes at thresholds 0.2/0.35/0.5 final [2, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [20, 17, 11], H1 [1, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 2.7
- replication (lineage window K = 20 frames = time 200, default): splits 904, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 739, merge/split ratio 0.817, nucleations 41
- channel total drift (end/start - 1): [0.3255, -0.4094, -0.4068, -0.2782]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 56 at frame 10: holes 0, rim-vs-core 0.21, rim-vs-outside 0.40, heterogeneity 0.15; core [0.692, 0.189, 0.849, 0.563] rim [0.534, 0.266, 0.732, 0.543]
  - track 1905 at frame 229: holes 0, rim-vs-core 0.28, rim-vs-outside 0.55, heterogeneity 0.15; core [0.664, 0.071, 0.874, 0.145] rim [0.558, 0.247, 0.757, 0.302]
  - track 77 at frame 13: holes 0, rim-vs-core 0.28, rim-vs-outside 0.67, heterogeneity 0.13; core [0.681, 0.105, 0.871, 0.066] rim [0.587, 0.306, 0.75, 0.195]
  - track 83 at frame 13: holes 0, rim-vs-core 0.34, rim-vs-outside 0.67, heterogeneity 0.18; core [0.784, 0.054, 0.913, 0.199] rim [0.596, 0.292, 0.763, 0.246]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 95 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial density rho: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.966, rim/outside 2.76 (aggregate of 95 individuals; 3/95 membrane-like individually; rim level 0.499)
  - radial food c: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 3.57, rim/outside 0.844 (aggregate of 95 individuals; 0/95 membrane-like individually; rim level 0.458)
  - radial |p|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.929, rim/outside 3.09 (aggregate of 95 individuals; 1/95 membrane-like individually; rim level 0.696)
  - radial p_x: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.964, rim/outside 0.989 (aggregate of 95 individuals; 0/95 membrane-like individually; rim level 0.47)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #56 (t=100, R_eq 5.32): none; #1905 (t=2290, R_eq 9.56): none; #77 (t=130, R_eq 7.02): none; #83 (t=130, R_eq 7.05): none

## Warnings
- radial: 6 of 95 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
