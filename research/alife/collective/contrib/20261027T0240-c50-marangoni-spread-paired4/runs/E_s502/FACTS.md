# Evidence pack: active-nematic-marangoni-spread (seed 502)

- world: `../../../world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 1081s; status ok
- command: `python -m labkit.run /tmp/claude-0/sp/world.py --out /tmp/claude-0/sp/runs/E/seed502 --seeds 502 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.64 of robust range [-1.0007, 0.5636], min area 6 px

## Measurements
- components: final 13, mean 13.1, max 22; occupancy final 0.04
- tracks: 154; persistent (alive >= 50% of run): 1; longest 214 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.47 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 14, 13], H1 [0, 0, 0]
- motion: 76 long-lived tracks moved >= 1 body length; max speed 0.373/time; max body lengths 13.8
- replication (lineage window K = 20 frames = time 100, default): splits 59, persistent splits 29 (0 more failed only because the siblings re-merged within K), max generation 5, merges 29, merge/split ratio 0.492, nucleations 8
- channel total drift (end/start - 1): [-0.9144, -0.749, None, 7.071, None, -0.1876]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 54 at frame 212: holes 0, rim-vs-core 0.71, rim-vs-outside 0.34, heterogeneity 0.12; core [0.97, 0.788, 0.05, 0.409, 0.015, 1.0] rim [0.798, 0.399, 0.142, 0.966, 0.041, 1.0]
  - track 40 at frame 148: holes 0, rim-vs-core 0.47, rim-vs-outside 0.46, heterogeneity 0.09; core [0.972, 0.871, 0.003, 0.009, 0.564, 1.0] rim [0.826, 0.62, 0.008, 0.026, 0.935, 1.0]
  - track 64 at frame 205: holes 0, rim-vs-core 0.60, rim-vs-outside 0.41, heterogeneity 0.10; core [0.985, 0.959, 0.497, 0.011, 0.001, 1.0] rim [0.813, 0.681, 1.0, 0.04, 0.004, 1.0]
  - track 118 at frame 376: holes 0, rim-vs-core 0.49, rim-vs-outside 0.38, heterogeneity 0.09; core [0.971, 0.978, 0.645, 0.023, 0.013, 1.0] rim [0.792, 0.7, 1.0, 0.057, 0.029, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 81 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.83, rim/outside 2.95 (aggregate of 81 individuals; 0/81 membrane-like individually; rim level 0.751)
  - radial order |Q|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.779, rim/outside 8.13 (aggregate of 81 individuals; 6/81 membrane-like individually; rim level 0.558)
  - radial s0 (mar 20): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.23, rim/outside 2.77 (aggregate of 81 individuals; 18/81 membrane-like individually; rim level 0.102)
  - radial s1 (mar 40): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.23, rim/outside 3.07 (aggregate of 81 individuals; 39/81 membrane-like individually; rim level 0.496)
  - radial s2 (mar 60): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.3, rim/outside 2.59 (aggregate of 81 individuals; 16/81 membrane-like individually; rim level 0.12)
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.999, rim/outside 1.04 (aggregate of 81 individuals; 0/81 membrane-like individually; rim level 0.999)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #54 (t=1060, R_eq 2.71): ['s0 (mar 20)', 's1 (mar 40)', 's2 (mar 60)']; #40 (t=740, R_eq 3.61): none; #64 (t=1025, R_eq 3.78): ['s0 (mar 20)', 's1 (mar 40)']; #118 (t=1880, R_eq 4.51): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 81 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
