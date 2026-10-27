# Evidence pack: active-nematic-marangoni-ladder (seed 104)

- world: `../../../../../../home/user/physim/research/alife/collective/contrib/20261026T2018-c45-marangoni-ladder/world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 1101s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2018-c45-marangoni-ladder/world.py --out /tmp/claude-0/ld/runs/ladder/seed104 --seeds 104 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.58 of robust range [-0.8279, 0.5988], min area 6 px

## Measurements
- components: final 18, mean 19.2, max 27; occupancy final 0.07
- tracks: 266; persistent (alive >= 50% of run): 0; longest 132 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [26, 18, 16], H1 [0, 0, 0]
- motion: 129 long-lived tracks moved >= 1 body length; max speed 0.366/time; max body lengths 8.4
- replication (lineage window K = 20 frames = time 100, default): splits 117, persistent splits 49 (0 more failed only because the siblings re-merged within K), max generation 9, merges 27, merge/split ratio 0.231, nucleations 8
- channel total drift (end/start - 1): [-0.4879, -0.5424, 3.6671, 3.7663, 3.8212]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 83 at frame 205: holes 0, rim-vs-core 0.47, rim-vs-outside 0.36, heterogeneity 0.10; core [0.928, 0.822, 0.008, 0.019, 0.428] rim [0.756, 0.569, 0.021, 0.041, 0.779]
  - track 138 at frame 286: holes 0, rim-vs-core 0.42, rim-vs-outside 0.29, heterogeneity 0.10; core [0.886, 0.496, 0.021, 0.011, 0.614] rim [0.727, 0.342, 0.039, 0.021, 0.967]
  - track 49 at frame 141: holes 0, rim-vs-core 0.62, rim-vs-outside 0.35, heterogeneity 0.15; core [0.966, 0.731, 0.467, 0.01, 0.012] rim [0.735, 0.481, 0.982, 0.026, 0.036]
  - track 244 at frame 390: holes 0, rim-vs-core 0.49, rim-vs-outside 0.31, heterogeneity 0.11; core [0.934, 0.555, 0.006, 0.579, 0.019] rim [0.737, 0.37, 0.012, 0.982, 0.043]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 129 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.801, rim/outside 4.23 (aggregate of 129 individuals; 0/129 membrane-like individually; rim level 0.693)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.804, rim/outside 7.81 (aggregate of 129 individuals; 15/129 membrane-like individually; rim level 0.504)
  - radial s0 (mar 20): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.14, rim/outside 2.83 (aggregate of 129 individuals; 32/129 membrane-like individually; rim level 0.176)
  - radial s1 (mar 40): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.31, rim/outside 3.04 (aggregate of 129 individuals; 34/129 membrane-like individually; rim level 0.195)
  - radial s2 (mar 60): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.09, rim/outside 3.07 (aggregate of 129 individuals; 41/129 membrane-like individually; rim level 0.318)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #83 (t=1025, R_eq 3.99): none; #138 (t=1430, R_eq 4.44): ['order |Q|']; #49 (t=705, R_eq 5.35): none; #244 (t=1950, R_eq 5.11): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 129 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
