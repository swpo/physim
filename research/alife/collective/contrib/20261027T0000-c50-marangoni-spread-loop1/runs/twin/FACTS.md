# Evidence pack: active-nematic-marangoni-spread (seed 500)

- world: `../../../world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 763s; status ok
- command: `python -m labkit.run /tmp/claude-0/sp/world.py --out /tmp/claude-0/sp/runs/twin/seed500 --seeds 500 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.64 of robust range [-1.0038, 0.5634], min area 6 px

## Measurements
- components: final 6, mean 16.0, max 25; occupancy final 0.03
- tracks: 134; persistent (alive >= 50% of run): 2; longest 305 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.89 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 6, 6], H1 [3, 0, 0]
- motion: 81 long-lived tracks moved >= 1 body length; max speed 0.346/time; max body lengths 12.2
- replication (lineage window K = 20 frames = time 100, default): splits 50, persistent splits 32 (0 more failed only because the siblings re-merged within K), max generation 5, merges 26, merge/split ratio 0.52, nucleations 9
- channel total drift (end/start - 1): [-0.8195, -0.8239, None, 3.8202, None, -0.2133]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 20 at frame 198: holes 0, rim-vs-core 0.54, rim-vs-outside 0.31, heterogeneity 0.10; core [0.962, 0.657, 0.47, 0.009, 0.003, 1.0] rim [0.792, 0.459, 0.94, 0.022, 0.006, 1.0]
  - track 64 at frame 242: holes 0, rim-vs-core 0.55, rim-vs-outside 0.33, heterogeneity 0.11; core [0.953, 0.807, 0.01, 0.474, 0.112, 1.0] rim [0.782, 0.538, 0.023, 0.905, 0.249, 1.0]
  - track 78 at frame 286: holes 0, rim-vs-core 0.50, rim-vs-outside 0.31, heterogeneity 0.09; core [0.942, 0.719, 0.586, 0.026, 0.009, 1.0] rim [0.776, 0.478, 0.991, 0.062, 0.02, 1.0]
  - track 113 at frame 339: holes 0, rim-vs-core 0.62, rim-vs-outside 0.34, heterogeneity 0.09; core [0.991, 0.788, 0.009, 0.242, 0.012, 1.0] rim [0.824, 0.484, 0.033, 0.758, 0.045, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 97 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.824, rim/outside 3.02 (aggregate of 97 individuals; 0/97 membrane-like individually; rim level 0.755)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.787, rim/outside 8.62 (aggregate of 97 individuals; 7/97 membrane-like individually; rim level 0.546)
  - radial s0 (mar 20): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.28, rim/outside 3.07 (aggregate of 97 individuals; 34/97 membrane-like individually; rim level 0.193)
  - radial s1 (mar 40): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.28, rim/outside 3.27 (aggregate of 97 individuals; 46/97 membrane-like individually; rim level 0.472)
  - radial s2 (mar 60): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.07, rim/outside 1.78 (aggregate of 97 individuals; 17/97 membrane-like individually; rim level 0.0526)
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1.02 (aggregate of 97 individuals; 1/97 membrane-like individually; rim level 0.988)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #20 (t=990, R_eq 4.18): ['order |Q|', 's1 (mar 40)']; #64 (t=1210, R_eq 4.37): none; #78 (t=1430, R_eq 4.44): none; #113 (t=1695, R_eq 2.46): ['s0 (mar 20)', 's1 (mar 40)', 's2 (mar 60)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
