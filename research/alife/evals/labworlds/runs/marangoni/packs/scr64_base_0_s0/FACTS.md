# Evidence pack: active-nematic-marangoni-noise (seed 0)

- world: `../../mg_noise.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni; mutation: dynamics noise sd 0.0 per sqrt(t): additive on ['phi', 'q1', 'q2', 's', 'c'], proportional on [], conserved (div of white flux) on []
- run: 101 frames x 100 steps x dt 0.05 = time 500; grid [64, 64]; wall 48s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/mg_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/packs/scr64_base_0_s0 --seeds 0 --frames 100 --size 64 64 --no-movie`
- segmentation: matter > 0.59 of robust range [-0.8359, 0.5816], min area 6 px

## Measurements
- components: final 8, mean 5.2, max 9; occupancy final 0.09
- tracks: 16; persistent (alive >= 50% of run): 4; longest 74 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.71 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 8, 8], H1 [0, 0, 0]
- motion: 10 long-lived tracks moved >= 1 body length; max speed 0.224/time; max body lengths 3.6
- replication (lineage window K = 20 frames = time 100, default): splits 6, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 2, merges 1, merge/split ratio 0.167, nucleations 3
- channel total drift (end/start - 1): [-0.4868, -0.3919, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 64: holes 0, rim-vs-core 0.73, rim-vs-outside 0.32, heterogeneity 0.25; core [0.945, 0.61, 0.44, 0.436] rim [0.722, 0.369, 0.932, 0.009]
  - track 5 at frame 69: holes 0, rim-vs-core 0.59, rim-vs-outside 0.32, heterogeneity 0.21; core [0.918, 0.674, 0.442, 0.339] rim [0.717, 0.429, 0.821, 0.008]
  - track 6 at frame 69: holes 0, rim-vs-core 0.78, rim-vs-outside 0.35, heterogeneity 0.24; core [0.966, 0.736, 0.364, 0.475] rim [0.766, 0.452, 0.889, 0.012]
  - track 9 at frame 78: holes 0, rim-vs-core 0.66, rim-vs-outside 0.41, heterogeneity 0.23; core [0.946, 0.906, 0.373, 0.444] rim [0.762, 0.592, 0.769, 0.069]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 34 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.812, rim/outside 4.68 (aggregate of 34 individuals; 0/34 membrane-like individually; rim level 0.721)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.785, rim/outside 9.06 (aggregate of 34 individuals; 0/34 membrane-like individually; rim level 0.558)
  - radial surfactant s: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.19, rim/outside 3.24 (aggregate of 34 individuals; 17/34 membrane-like individually; rim level 0.569)
  - radial cargo c: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.514, rim/outside 2.54 (aggregate of 34 individuals; 5/34 membrane-like individually; rim level 0.15)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #3 (t=320, R_eq 4.44): ['order |Q|']; #5 (t=345, R_eq 4.51): none; #6 (t=345, R_eq 4.07): none; #9 (t=390, R_eq 3.87): ['surfactant s']

## Warnings
- radial: 1 of 34 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
