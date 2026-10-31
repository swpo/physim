# Evidence pack: active-nematic-marangoni-noise (seed 0)

- world: `../../mg_noise.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni; mutation: dynamics noise sd 0.01 per sqrt(t): additive on ['q1', 'q2'], proportional on ['s', 'c'], conserved (div of white flux) on ['phi']
- run: 101 frames x 100 steps x dt 0.05 = time 500; grid [128, 128]; wall 229s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/mg_noise.py --out /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni/packs/b128_phys_0.01_s0 --seeds 0 --frames 100 --size 128 128 --no-movie`
- segmentation: matter > 0.60 of robust range [-0.8314, 0.5596], min area 6 px

## Measurements
- components: final 31, mean 16.3, max 31; occupancy final 0.08
- tracks: 66; persistent (alive >= 50% of run): 9; longest 71 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.46 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [31, 31, 30], H1 [0, 0, 0]
- motion: 25 long-lived tracks moved >= 1 body length; max speed 0.294/time; max body lengths 6.3
- replication (lineage window K = 20 frames = time 100, default): splits 26, persistent splits 15 (0 more failed only because the siblings re-merged within K), max generation 3, merges 4, merge/split ratio 0.154, nucleations 9
- channel total drift (end/start - 1): [-0.5031, -0.3976, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 14 at frame 65: holes 0, rim-vs-core 0.82, rim-vs-outside 0.40, heterogeneity 0.25; core [0.962, 0.888, 0.378, 0.587] rim [0.767, 0.575, 0.854, 0.024]
  - track 16 at frame 68: holes 0, rim-vs-core 0.77, rim-vs-outside 0.41, heterogeneity 0.24; core [0.952, 0.936, 0.425, 0.495] rim [0.741, 0.625, 0.893, 0.021]
  - track 17 at frame 68: holes 0, rim-vs-core 0.94, rim-vs-outside 0.42, heterogeneity 0.24; core [0.966, 0.917, 0.399, 0.716] rim [0.762, 0.618, 0.912, 0.02]
  - track 34 at frame 79: holes 0, rim-vs-core 0.74, rim-vs-outside 0.37, heterogeneity 0.23; core [0.965, 0.837, 0.386, 0.476] rim [0.773, 0.543, 0.856, 0.031]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 115 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.807, rim/outside 4.52 (aggregate of 115 individuals; 0/115 membrane-like individually; rim level 0.74)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.764, rim/outside 8.61 (aggregate of 115 individuals; 5/115 membrane-like individually; rim level 0.569)
  - radial surfactant s: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.37, rim/outside 3.31 (aggregate of 115 individuals; 63/115 membrane-like individually; rim level 0.595)
  - radial cargo c: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.376, rim/outside 2.08 (aggregate of 115 individuals; 8/115 membrane-like individually; rim level 0.158)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #14 (t=325, R_eq 3.39): ['surfactant s']; #16 (t=340, R_eq 4.03): none; #17 (t=340, R_eq 3.78): ['surfactant s']; #34 (t=395, R_eq 3.95): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 115 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
