# Evidence pack: active-nematic-marangoni-spread (seed 510)

- world: `../../../collective/contrib/20261027T0000-c50-marangoni-spread-loop1/world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 869s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0000-c50-marangoni-spread-loop1/world.py --out /home/user/physim/research/alife/c56work/sp/twin --seeds 510 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.65 of robust range [-1.0056, 0.55], min area 6 px

## Measurements
- components: final 12, mean 14.7, max 26; occupancy final 0.04
- tracks: 146; persistent (alive >= 50% of run): 2; longest 238 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.76 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [13, 13, 13], H1 [0, 0, 0]
- motion: 82 long-lived tracks moved >= 1 body length; max speed 0.393/time; max body lengths 10.4
- replication (lineage window K = 20 frames = time 100, default): splits 57, persistent splits 34 (0 more failed only because the siblings re-merged within K), max generation 7, merges 23, merge/split ratio 0.404, nucleations 9
- channel total drift (end/start - 1): [-0.8034, -0.7478, None, 4.78, None, -0.216]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 44 at frame 182: holes 0, rim-vs-core 0.63, rim-vs-outside 0.37, heterogeneity 0.10; core [0.964, 0.907, 0.001, 0.445, 0.006, 1.0] rim [0.779, 0.56, 0.002, 0.93, 0.015, 1.0]
  - track 45 at frame 182: holes 0, rim-vs-core 0.57, rim-vs-outside 0.30, heterogeneity 0.10; core [0.959, 0.664, 0.007, 0.016, 0.476, 1.0] rim [0.767, 0.416, 0.016, 0.039, 0.948, 1.0]
  - track 103 at frame 313: holes 0, rim-vs-core 0.51, rim-vs-outside 0.38, heterogeneity 0.09; core [0.96, 0.921, 0.011, 0.366, 0.004, 1.0] rim [0.784, 0.629, 0.025, 0.744, 0.011, 1.0]
  - track 124 at frame 370: holes 0, rim-vs-core 0.23, rim-vs-outside 0.44, heterogeneity 0.10; core [0.939, 0.626, 0.013, 0.51, 0.02, 1.0] rim [0.854, 0.525, 0.019, 0.693, 0.029, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 93 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.822, rim/outside 3.07 (aggregate of 93 individuals; 0/93 membrane-like individually; rim level 0.763)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.771, rim/outside 9.24 (aggregate of 93 individuals; 4/93 membrane-like individually; rim level 0.582)
  - radial s0 (mar 20): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.08, rim/outside 2.76 (aggregate of 93 individuals; 32/93 membrane-like individually; rim level 0.128)
  - radial s1 (mar 40): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.49, rim/outside 3.38 (aggregate of 93 individuals; 48/93 membrane-like individually; rim level 0.416)
  - radial s2 (mar 60): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.33, rim/outside 3.01 (aggregate of 93 individuals; 33/93 membrane-like individually; rim level 0.201)
  - radial chemostat target phi_b(x,t): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.01, rim/outside 1.01 (aggregate of 93 individuals; 0/93 membrane-like individually; rim level 0.994)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #44 (t=910, R_eq 3.7): ['s1 (mar 40)']; #45 (t=910, R_eq 4.11): none; #103 (t=1565, R_eq 3.66): ['s0 (mar 20)', 's1 (mar 40)']; #124 (t=1850, R_eq 2.52): ['s0 (mar 20)', 's1 (mar 40)', 's2 (mar 60)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 93 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
