# Evidence pack: active-nematic-marangoni-spread (seed 500)

- world: `../../../world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 769s; status ok
- command: `python -m labkit.run /tmp/claude-0/sp/world.py --out /tmp/claude-0/sp/runs/off/seed500 --seeds 500 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.64 of robust range [-0.9982, 0.5659], min area 6 px

## Measurements
- components: final 5, mean 9.9, max 15; occupancy final 0.01
- tracks: 85; persistent (alive >= 50% of run): 1; longest 207 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.12 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [6, 6, 5], H1 [2, 0, 0]
- motion: 45 long-lived tracks moved >= 1 body length; max speed 0.0786/time; max body lengths 4.5
- replication (lineage window K = 20 frames = time 100, default): splits 35, persistent splits 23 (0 more failed only because the siblings re-merged within K), max generation 7, merges 7, merge/split ratio 0.2, nucleations 8
- channel total drift (end/start - 1): [-0.8195, -0.8824, None, 1.4994, None, -0.2133]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 9 at frame 131: holes 0, rim-vs-core 0.56, rim-vs-outside 0.40, heterogeneity 0.09; core [0.981, 0.98, 0.0, 0.373, 0.007, 1.0] rim [0.79, 0.699, 0.0, 0.818, 0.015, 1.0]
  - track 53 at frame 329: holes 0, rim-vs-core 0.54, rim-vs-outside 0.33, heterogeneity 0.09; core [0.975, 0.896, 0.01, 0.445, 0.013, 1.0] rim [0.817, 0.625, 0.024, 0.889, 0.023, 1.0]
  - track 29 at frame 182: holes 0, rim-vs-core 0.47, rim-vs-outside 0.34, heterogeneity 0.08; core [0.96, 0.857, 0.004, 0.493, 0.002, 1.0] rim [0.801, 0.602, 0.007, 0.849, 0.003, 1.0]
  - track 76 at frame 356: holes 0, rim-vs-core 0.43, rim-vs-outside 0.32, heterogeneity 0.11; core [0.986, 0.788, 0.706, 0.012, 0.073, 1.0] rim [0.814, 0.545, 1.0, 0.031, 0.186, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 58 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.86, rim/outside 2.98 (aggregate of 58 individuals; 0/58 membrane-like individually; rim level 0.794)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.836, rim/outside 7.02 (aggregate of 58 individuals; 2/58 membrane-like individually; rim level 0.684)
  - radial s0 (mar 20): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.67, rim/outside 2.89 (aggregate of 58 individuals; 22/58 membrane-like individually; rim level 0.173)  MEMBRANE-LIKE
  - radial s1 (mar 40): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.49, rim/outside 3.16 (aggregate of 58 individuals; 40/58 membrane-like individually; rim level 0.572)
  - radial s2 (mar 60): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.12, rim/outside 2.68 (aggregate of 58 individuals; 23/58 membrane-like individually; rim level 0.0997)
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1.04 (aggregate of 58 individuals; 0/58 membrane-like individually; rim level 1)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s0 (mar 20)
- membrane-like channels per top track at mid-life: #9 (t=655, R_eq 3.04): ['s1 (mar 40)', 's2 (mar 60)']; #53 (t=1645, R_eq 2.99): ['s0 (mar 20)', 's1 (mar 40)', 's2 (mar 60)']; #29 (t=910, R_eq 3.61): none; #76 (t=1780, R_eq 4.07): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 58 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
