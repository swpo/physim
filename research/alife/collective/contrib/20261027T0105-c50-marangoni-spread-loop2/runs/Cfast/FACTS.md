# Evidence pack: active-nematic-marangoni-spread (seed 501)

- world: `../../../world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 1031s; status ok
- command: `python -m labkit.run /tmp/claude-0/sp/world.py --out /tmp/claude-0/sp/runs/Cfast/seed501 --seeds 501 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.64 of robust range [-0.9427, 0.5339], min area 6 px

## Measurements
- components: final 4, mean 6.9, max 17; occupancy final 0.01
- tracks: 103; persistent (alive >= 50% of run): 0; longest 132 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 4, 4], H1 [0, 0, 0]
- motion: 55 long-lived tracks moved >= 1 body length; max speed 0.553/time; max body lengths 16.1
- replication (lineage window K = 20 frames = time 100, default): splits 44, persistent splits 22 (0 more failed only because the siblings re-merged within K), max generation 6, merges 7, merge/split ratio 0.159, nucleations 8
- channel total drift (end/start - 1): [-0.6801, -0.8989, None, 1.7531, None, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 26 at frame 128: holes 0, rim-vs-core 0.71, rim-vs-outside 0.36, heterogeneity 0.16; core [0.975, 0.735, 0.391, 0.537, 0.012, 1.0] rim [0.787, 0.497, 0.86, 0.982, 0.028, 1.0]
  - track 27 at frame 121: holes 0, rim-vs-core 0.26, rim-vs-outside 0.44, heterogeneity 0.05; core [0.986, 0.981, 1.0, 0.017, 0.012, 1.0] rim [0.808, 0.796, 1.0, 0.043, 0.033, 1.0]
  - track 30 at frame 131: holes 0, rim-vs-core 0.59, rim-vs-outside 0.35, heterogeneity 0.12; core [0.983, 0.772, 0.179, 0.457, 0.006, 1.0] rim [0.814, 0.544, 0.42, 0.919, 0.014, 1.0]
  - track 99 at frame 387: holes 0, rim-vs-core 0.49, rim-vs-outside 0.37, heterogeneity 0.09; core [0.965, 0.865, 0.0, 0.58, 0.0, 1.0] rim [0.807, 0.611, 0.0, 0.972, 0.0, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 40 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.815, rim/outside 3.12 (aggregate of 40 individuals; 0/40 membrane-like individually; rim level 0.754)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.85, rim/outside 7.69 (aggregate of 40 individuals; 1/40 membrane-like individually; rim level 0.634)
  - radial s0 (mar 20): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.951, rim/outside 1.47 (aggregate of 40 individuals; 5/40 membrane-like individually; rim level 0.0519)
  - radial s1 (mar 40): peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.3, rim/outside 3.2 (aggregate of 40 individuals; 18/40 membrane-like individually; rim level 0.585)
  - radial s2 (mar 60): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.846, rim/outside 2.36 (aggregate of 40 individuals; 6/40 membrane-like individually; rim level 0.0999)
  - radial chemostat target phi_b(x,t): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.02, rim/outside 1.01 (aggregate of 40 individuals; 0/40 membrane-like individually; rim level 0.992)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #26 (t=640, R_eq 4.65): ['order |Q|']; #27 (t=605, R_eq 4.22): ['s1 (mar 40)', 's2 (mar 60)']; #30 (t=655, R_eq 4.33): none; #99 (t=1935, R_eq 4.65): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 40 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
