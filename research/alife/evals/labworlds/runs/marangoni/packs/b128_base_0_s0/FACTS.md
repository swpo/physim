# Evidence pack: active-nematic-marangoni-noise (seed 0)

- world: `../../mg_noise.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni; mutation: dynamics noise sd 0.0 per sqrt(t): additive on ['phi', 'q1', 'q2', 's', 'c'], proportional on [], conserved (div of white flux) on []
- run: 101 frames x 100 steps x dt 0.05 = time 500; grid [128, 128]; wall 198s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/mg_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/packs/b128_base_0_s0 --seeds 0 --frames 100 --size 128 128 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.8286, 0.5702], min area 6 px

## Measurements
- components: final 28, mean 15.3, max 28; occupancy final 0.09
- tracks: 53; persistent (alive >= 50% of run): 13; longest 73 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.75 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [30, 28, 27], H1 [0, 0, 0]
- motion: 28 long-lived tracks moved >= 1 body length; max speed 0.385/time; max body lengths 7.3
- replication (lineage window K = 20 frames = time 100, default): splits 21, persistent splits 14 (0 more failed only because the siblings re-merged within K), max generation 3, merges 2, merge/split ratio 0.095, nucleations 9
- channel total drift (end/start - 1): [-0.5031, -0.4397, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 11 at frame 64: holes 0, rim-vs-core 0.76, rim-vs-outside 0.34, heterogeneity 0.24; core [0.953, 0.782, 0.432, 0.495] rim [0.739, 0.476, 0.892, 0.022]
  - track 12 at frame 64: holes 0, rim-vs-core 0.76, rim-vs-outside 0.39, heterogeneity 0.23; core [0.951, 0.889, 0.397, 0.555] rim [0.766, 0.603, 0.814, 0.025]
  - track 14 at frame 65: holes 0, rim-vs-core 0.74, rim-vs-outside 0.33, heterogeneity 0.25; core [0.964, 0.663, 0.409, 0.455] rim [0.747, 0.411, 0.897, 0.013]
  - track 35 at frame 90: holes 0, rim-vs-core 0.80, rim-vs-outside 0.37, heterogeneity 0.24; core [0.954, 0.825, 0.421, 0.498] rim [0.751, 0.515, 0.932, 0.013]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 107 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.804, rim/outside 4.56 (aggregate of 107 individuals; 0/107 membrane-like individually; rim level 0.718)
  - radial order |Q|: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.792, rim/outside 8.86 (aggregate of 107 individuals; 5/107 membrane-like individually; rim level 0.551)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.21, rim/outside 3.31 (aggregate of 107 individuals; 48/107 membrane-like individually; rim level 0.576)
  - radial cargo c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.446, rim/outside 2.27 (aggregate of 107 individuals; 16/107 membrane-like individually; rim level 0.158)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #11 (t=320, R_eq 4.11): none; #12 (t=320, R_eq 3.95): ['surfactant s']; #14 (t=325, R_eq 4.44): none; #35 (t=450, R_eq 3.99): ['surfactant s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 107 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
