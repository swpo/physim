# Evidence pack: active-nematic-marangoni-distance-pays (seed 602)

- world: `../../../../../../home/user/physim/research/alife/collective/contrib/20261027T0540-c54-distance-pays-loop1/world.py`, family `active-nematic`
- parent: collective/contrib/20261027T0000-c50-marangoni-spread-loop1/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 902s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0540-c54-distance-pays-loop1/world.py --out /tmp/claude-0/c54/runs/E/seed602 --seeds 602 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.65 of robust range [-1.0036, 0.5503], min area 6 px

## Measurements
- components: final 10, mean 11.3, max 20; occupancy final 0.03
- tracks: 111; persistent (alive >= 50% of run): 1; longest 235 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 7.10 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 10, 9], H1 [1, 0, 0]
- motion: 66 long-lived tracks moved >= 1 body length; max speed 0.577/time; max body lengths 10.1
- replication (lineage window K = 20 frames = time 100, default): splits 48, persistent splits 33 (0 more failed only because the siblings re-merged within K), max generation 8, merges 15, merge/split ratio 0.312, nucleations 2
- channel total drift (end/start - 1): [-0.8864, -0.7824, None, 2.208, None, -0.3021]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 158: holes 0, rim-vs-core 0.35, rim-vs-outside 0.41, heterogeneity 0.07; core [0.982, 0.961, 0.912, 0.017, 0.001, 1.0] rim [0.802, 0.68, 1.0, 0.047, 0.002, 1.0]
  - track 69 at frame 292: holes 0, rim-vs-core 0.41, rim-vs-outside 0.24, heterogeneity 0.06; core [0.933, 0.288, 0.01, 0.444, 0.035, 1.0] rim [0.762, 0.187, 0.019, 0.804, 0.068, 1.0]
  - track 40 at frame 171: holes 0, rim-vs-core 0.57, rim-vs-outside 0.31, heterogeneity 0.11; core [0.975, 0.613, 0.006, 0.464, 0.003, 1.0] rim [0.791, 0.419, 0.015, 0.964, 0.008, 1.0]
  - track 95 at frame 353: holes 0, rim-vs-core 0.41, rim-vs-outside 0.31, heterogeneity 0.12; core [0.956, 0.757, 0.042, 0.018, 1.0, 1.0] rim [0.791, 0.485, 0.091, 0.04, 1.0, 0.741]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 74 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.831, rim/outside 2.98 (aggregate of 74 individuals; 0/74 membrane-like individually; rim level 0.761)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.789, rim/outside 8.39 (aggregate of 74 individuals; 4/74 membrane-like individually; rim level 0.583)
  - radial s0 (mar 20): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.55, rim/outside 2.4 (aggregate of 74 individuals; 23/74 membrane-like individually; rim level 0.134)  MEMBRANE-LIKE
  - radial s1 (mar 40): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.2, rim/outside 3.19 (aggregate of 74 individuals; 34/74 membrane-like individually; rim level 0.511)
  - radial s2 (mar 60): peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.49, rim/outside 2.23 (aggregate of 74 individuals; 17/74 membrane-like individually; rim level 0.121)
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.997, rim/outside 1.03 (aggregate of 74 individuals; 0/74 membrane-like individually; rim level 0.992)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s0 (mar 20)
- membrane-like channels per top track at mid-life: #8 (t=790, R_eq 3.78): ['s1 (mar 40)']; #69 (t=1460, R_eq 2.33): ['s0 (mar 20)', 's1 (mar 40)', 's2 (mar 60)']; #40 (t=855, R_eq 4.33): none; #95 (t=1765, R_eq 4.07): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 74 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
