# Evidence pack: active-nematic-marangoni-distance-pays (seed 620)

- world: `../../../w2/world.py`, family `active-nematic`
- parent: collective/contrib/20261027T0000-c50-marangoni-spread-loop1/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 1002s; status ok
- command: `python -m labkit.run /tmp/claude-0/c54/w2/world.py --out /tmp/claude-0/c54/runs/m60E/seed620 --seeds 620 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.67 of robust range [-1.0169, 0.5108], min area 6 px

## Measurements
- components: final 15, mean 9.2, max 16; occupancy final 0.04
- tracks: 121; persistent (alive >= 50% of run): 0; longest 199 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 15, 15], H1 [1, 0, 0]
- motion: 52 long-lived tracks moved >= 1 body length; max speed 0.485/time; max body lengths 11.9
- replication (lineage window K = 20 frames = time 100, default): splits 51, persistent splits 21 (0 more failed only because the siblings re-merged within K), max generation 8, merges 16, merge/split ratio 0.314, nucleations 3
- channel total drift (end/start - 1): [-0.721, -0.7644, None, None, 8.3983, -0.1831]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 50 at frame 303: holes 0, rim-vs-core 0.52, rim-vs-outside 0.42, heterogeneity 0.12; core [0.98, 0.954, 0.212, 0.212, 0.382, 1.0] rim [0.82, 0.701, 0.387, 0.387, 0.732, 1.0]
  - track 49 at frame 296: holes 0, rim-vs-core 0.40, rim-vs-outside 0.23, heterogeneity 0.09; core [0.955, 0.365, 0.13, 0.13, 0.644, 1.0] rim [0.792, 0.238, 0.204, 0.204, 0.967, 1.0]
  - track 10 at frame 108: holes 0, rim-vs-core 0.56, rim-vs-outside 0.41, heterogeneity 0.11; core [0.979, 0.936, 0.131, 0.131, 0.464, 1.0] rim [0.811, 0.64, 0.229, 0.229, 0.883, 1.0]
  - track 112 at frame 390: holes 0, rim-vs-core 0.65, rim-vs-outside 0.32, heterogeneity 0.13; core [0.982, 0.852, 0.197, 0.197, 0.457, 1.0] rim [0.802, 0.451, 0.325, 0.325, 0.902, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 60 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.855, rim/outside 2.76 (aggregate of 60 individuals; 0/60 membrane-like individually; rim level 0.772)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.8, rim/outside 7.87 (aggregate of 60 individuals; 5/60 membrane-like individually; rim level 0.562)
  - radial s0 (mar 20): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.26, rim/outside 3.18 (aggregate of 60 individuals; 22/60 membrane-like individually; rim level 0.247)
  - radial s1 (mar 40): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.26, rim/outside 3.18 (aggregate of 60 individuals; 22/60 membrane-like individually; rim level 0.247)
  - radial s2 (mar 60): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.22, rim/outside 3.37 (aggregate of 60 individuals; 25/60 membrane-like individually; rim level 0.668)
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1.03 (aggregate of 60 individuals; 0/60 membrane-like individually; rim level 1)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #50 (t=1515, R_eq 3.48): ['s0 (mar 20)', 's1 (mar 40)', 's2 (mar 60)']; #49 (t=1480, R_eq 4.55): ['order |Q|']; #10 (t=540, R_eq 3.57): ['s0 (mar 20)', 's1 (mar 40)', 's2 (mar 60)']; #112 (t=1950, R_eq 2.65): ['s0 (mar 20)', 's1 (mar 40)', 's2 (mar 60)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 60 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
