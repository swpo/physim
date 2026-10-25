# Evidence pack: nematic-fuelcell (seed 12)

- world: `../world.py`, family `active-nematic`
- parent: None; mutation: new class: CH droplets with internal Landau-de Gennes nematic order and extensile active stress, Brinkman-Stokes flow
- run: 201 frames x 100 steps x dt 0.05 = time 1000; grid [128, 128]; wall 370s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/rev4/world.py --out /tmp/claude-0/-home-user-physim/3b801bf0-17d3-5f80-b419-db17577ce992/scratchpad/rev4/world_s12 --seeds 12 --no-movie`
- segmentation: matter > 0.57 of robust range [-0.8531, 0.6368], min area 6 px

## Measurements
- components: final 23, mean 12.0, max 23; occupancy final 0.08
- tracks: 50; persistent (alive >= 50% of run): 5; longest 150 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 26.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [28, 24, 23], H1 [0, 0, 0]
- motion: 15 long-lived tracks moved >= 1 body length; max speed 0.0531/time; max body lengths 2.6
- replication (lineage window K = 20 frames = time 100, default): splits 21, persistent splits 16 (0 more failed only because the siblings re-merged within K), max generation 3, merges 2, merge/split ratio 0.095, nucleations 7
- channel total drift (end/start - 1): [-0.5083, -0.2416, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 91: holes 0, rim-vs-core 0.58, rim-vs-outside 0.74, heterogeneity 0.16; core [0.989, 0.906, 0.323, 0.926] rim [0.806, 0.555, 0.73, 0.79]
  - track 7 at frame 119: holes 0, rim-vs-core 0.61, rim-vs-outside 0.45, heterogeneity 0.17; core [0.953, 0.935, 0.402, 0.75] rim [0.714, 0.608, 0.826, 0.601]
  - track 6 at frame 79: holes 0, rim-vs-core 0.47, rim-vs-outside 0.75, heterogeneity 0.15; core [0.963, 0.869, 0.379, 0.914] rim [0.804, 0.642, 0.733, 0.786]
  - track 31 at frame 176: holes 0, rim-vs-core 0.22, rim-vs-outside 0.65, heterogeneity 0.16; core [0.942, 0.913, 0.448, 0.844] rim [0.852, 0.808, 0.602, 0.766]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 85 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.808, rim/outside 4.04 (aggregate of 85 individuals; 4/85 membrane-like individually; rim level 0.645)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.788, rim/outside 6 (aggregate of 85 individuals; 4/85 membrane-like individually; rim level 0.541)
  - radial shell s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.18, rim/outside 2.26 (aggregate of 85 individuals; 43/85 membrane-like individually; rim level 0.584)
  - radial fuel f: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.8, rim/outside 2.53 (aggregate of 85 individuals; 4/85 membrane-like individually; rim level 0.578)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #4 (t=455, R_eq 6.84): none; #7 (t=595, R_eq 3.66): ['shell s']; #6 (t=395, R_eq 6.36): none; #31 (t=880, R_eq 3.52): ['shell s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 11 of 85 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
