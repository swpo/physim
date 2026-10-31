# Evidence pack: active-nematic-marangoni-noise (seed 1)

- world: `../../mg_noise.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni; mutation: dynamics noise sd 0.03 per sqrt(t): additive on ['phi', 'q1', 'q2', 's', 'c'], proportional on [], conserved (div of white flux) on []
- run: 101 frames x 100 steps x dt 0.05 = time 500; grid [128, 128]; wall 207s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/mg_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/packs/b128_plain_0.03_s1 --seeds 1 --frames 100 --size 128 128 --no-movie`
- segmentation: matter > 0.60 of robust range [-0.8338, 0.5577], min area 6 px

## Measurements
- components: final 28, mean 17.0, max 29; occupancy final 0.08
- tracks: 73; persistent (alive >= 50% of run): 3; longest 81 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 10.29 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [29, 28, 27], H1 [0, 0, 0]
- motion: 39 long-lived tracks moved >= 1 body length; max speed 0.314/time; max body lengths 6.8
- replication (lineage window K = 20 frames = time 100, default): splits 26, persistent splits 14 (0 more failed only because the siblings re-merged within K), max generation 3, merges 10, merge/split ratio 0.385, nucleations 11
- channel total drift (end/start - 1): [-0.4988, -0.3207, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 60: holes 0, rim-vs-core 0.71, rim-vs-outside 0.43, heterogeneity 0.22; core [0.947, 0.966, 0.423, 0.528] rim [0.774, 0.777, 0.865, 0.029]
  - track 13 at frame 66: holes 0, rim-vs-core 0.72, rim-vs-outside 0.38, heterogeneity 0.23; core [0.954, 0.887, 0.393, 0.476] rim [0.753, 0.585, 0.813, 0.014]
  - track 22 at frame 70: holes 0, rim-vs-core 0.73, rim-vs-outside 0.30, heterogeneity 0.23; core [0.974, 0.652, 0.359, 0.502] rim [0.763, 0.392, 0.79, 0.02]
  - track 55 at frame 86: holes 0, rim-vs-core 0.76, rim-vs-outside 0.34, heterogeneity 0.24; core [0.978, 0.765, 0.356, 0.401] rim [0.762, 0.404, 0.848, 0.011]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 114 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.805, rim/outside 4.17 (aggregate of 114 individuals; 0/114 membrane-like individually; rim level 0.709)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.777, rim/outside 6.09 (aggregate of 114 individuals; 9/114 membrane-like individually; rim level 0.51)
  - radial surfactant s: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.19, rim/outside 2.88 (aggregate of 114 individuals; 46/114 membrane-like individually; rim level 0.582)
  - radial cargo c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.476, rim/outside 1.56 (aggregate of 114 individuals; 24/114 membrane-like individually; rim level 0.151)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #8 (t=300, R_eq 4.65): none; #13 (t=330, R_eq 3.99): ['surfactant s']; #22 (t=350, R_eq 3.57): ['surfactant s']; #55 (t=430, R_eq 2.76): ['surfactant s']

## Warnings
- radial: 6 of 114 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
