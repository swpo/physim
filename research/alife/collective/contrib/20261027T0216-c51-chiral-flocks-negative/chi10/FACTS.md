# Evidence pack: chiral-eating-flocks (seed 0)

- world: `../../w2.py`, family `polar-active-fluid`
- parent: None; mutation: -
- run: 301 frames x 40 steps x dt 0.25 = time 3000; grid [128, 128]; wall 20s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/77ac260a-0f32-5d82-b241-4f9c69dcdb08/scratchpad/tt/w2.py --out /tmp/claude-0/-home-user-physim/77ac260a-0f32-5d82-b241-4f9c69dcdb08/scratchpad/tt/packs/chi10 --seeds 0 --frames 300 --spf 40 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.5684], min area 6 px

## Measurements
- components: final 30, mean 24.6, max 34; occupancy final 0.39
- tracks: 1478; persistent (alive >= 50% of run): 9; longest 277 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.63 (1 = constant size)
- enclosures: components with a hole mean 0.12, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [35, 33, 33], H1 [3, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 20 frames = time 200, default): splits 492, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 2, merges 478, merge/split ratio 0.972, nucleations 3
- channel total drift (end/start - 1): [0.539, -0.4642, -0.2784, 2.0195]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 99 at frame 164: holes 0, rim-vs-core 0.31, rim-vs-outside 0.54, heterogeneity 0.13; core [0.684, 0.093, 0.854, 0.189] rim [0.54, 0.283, 0.658, 0.201]
  - track 170 at frame 187: holes 0, rim-vs-core 0.34, rim-vs-outside 0.51, heterogeneity 0.15; core [0.705, 0.092, 0.858, 0.514] rim [0.547, 0.283, 0.662, 0.394]
  - track 168 at frame 184: holes 0, rim-vs-core 0.34, rim-vs-outside 0.50, heterogeneity 0.14; core [0.677, 0.092, 0.85, 0.311] rim [0.534, 0.275, 0.659, 0.461]
  - track 203 at frame 192: holes 0, rim-vs-core 0.35, rim-vs-outside 0.52, heterogeneity 0.15; core [0.707, 0.082, 0.866, 0.618] rim [0.545, 0.277, 0.665, 0.482]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 159 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial density rho: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.01, rim/outside 2.97 (aggregate of 159 individuals; 3/159 membrane-like individually; rim level 0.641)
  - radial food c: peak at rho=1.55 (OUTSIDE the peak band 0.5-1.5), rim/core 5.41, rim/outside 0.99 (aggregate of 159 individuals; 1/159 membrane-like individually; rim level 0.498)
  - radial |p|: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.939, rim/outside 3.34 (aggregate of 159 individuals; 3/159 membrane-like individually; rim level 0.77)
  - radial p_x: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.977, rim/outside 1.06 (aggregate of 159 individuals; 0/159 membrane-like individually; rim level 0.523)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #99 (t=1640, R_eq 8.06): none; #170 (t=1870, R_eq 7.65): none; #168 (t=1840, R_eq 7.74): none; #203 (t=1920, R_eq 7.59): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 9 of 159 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
