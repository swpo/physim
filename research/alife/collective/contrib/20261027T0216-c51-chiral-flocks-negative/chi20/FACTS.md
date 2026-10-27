# Evidence pack: chiral-eating-flocks (seed 0)

- world: `../../w2.py`, family `polar-active-fluid`
- parent: None; mutation: -
- run: 301 frames x 40 steps x dt 0.25 = time 3000; grid [128, 128]; wall 20s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/77ac260a-0f32-5d82-b241-4f9c69dcdb08/scratchpad/tt/w2.py --out /tmp/claude-0/-home-user-physim/77ac260a-0f32-5d82-b241-4f9c69dcdb08/scratchpad/tt/packs/chi20 --seeds 0 --frames 300 --spf 40 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.5249], min area 6 px

## Measurements
- components: final 63, mean 49.5, max 63; occupancy final 0.42
- tracks: 432; persistent (alive >= 50% of run): 46; longest 293 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.59 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [64, 64, 63], H1 [30, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 20 frames = time 200, default): splits 139, persistent splits 22 (0 more failed only because the siblings re-merged within K), max generation 3, merges 93, merge/split ratio 0.669, nucleations 2
- channel total drift (end/start - 1): [0.6576, -0.4997, -0.2432, 3.1092]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 83 at frame 154: holes 0, rim-vs-core 0.42, rim-vs-outside 0.56, heterogeneity 0.13; core [0.823, 0.078, 0.907, 0.282] rim [0.576, 0.269, 0.625, 0.312]
  - track 126 at frame 161: holes 0, rim-vs-core 0.37, rim-vs-outside 0.57, heterogeneity 0.12; core [0.78, 0.096, 0.885, 0.034] rim [0.579, 0.258, 0.646, 0.163]
  - track 127 at frame 161: holes 0, rim-vs-core 0.44, rim-vs-outside 0.56, heterogeneity 0.14; core [0.849, 0.074, 0.914, 0.332] rim [0.579, 0.262, 0.63, 0.351]
  - track 264 at frame 189: holes 0, rim-vs-core 0.42, rim-vs-outside 0.54, heterogeneity 0.13; core [0.831, 0.082, 0.906, 0.654] rim [0.573, 0.268, 0.624, 0.642]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 321 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial density rho: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.867, rim/outside 2.91 (aggregate of 321 individuals; 2/321 membrane-like individually; rim level 0.739)
  - radial food c: peak at rho=1.55 (OUTSIDE the peak band 0.5-1.5), rim/core 8.46, rim/outside 1.05 (aggregate of 321 individuals; 0/321 membrane-like individually; rim level 0.461)
  - radial |p|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.857, rim/outside 3.13 (aggregate of 321 individuals; 1/321 membrane-like individually; rim level 0.798)
  - radial p_x: peak at rho=1.55 (OUTSIDE the peak band 0.5-1.5), rim/core 1.04, rim/outside 1 (aggregate of 321 individuals; 0/321 membrane-like individually; rim level 0.489)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #83 (t=1540, R_eq 6.68): none; #126 (t=1610, R_eq 6.98): none; #127 (t=1610, R_eq 6.02): none; #264 (t=1890, R_eq 6.36): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 321 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
