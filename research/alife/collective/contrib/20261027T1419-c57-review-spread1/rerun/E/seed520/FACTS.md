# Evidence pack: active-nematic-marangoni-spread (seed 520)

- world: `../../../20261027T0000-c50-marangoni-spread-loop1/world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 896s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0000-c50-marangoni-spread-loop1/world.py --out collective/contrib/c57-w7/E/seed520 --seeds 520 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.64 of robust range [-0.9951, 0.5604], min area 6 px

## Measurements
- components: final 10, mean 14.2, max 24; occupancy final 0.03
- tracks: 122; persistent (alive >= 50% of run): 1; longest 317 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.41 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [10, 10, 10], H1 [1, 0, 0]
- motion: 80 long-lived tracks moved >= 1 body length; max speed 0.726/time; max body lengths 11.2
- replication (lineage window K = 20 frames = time 100, default): splits 45, persistent splits 25 (0 more failed only because the siblings re-merged within K), max generation 5, merges 16, merge/split ratio 0.356, nucleations 16
- channel total drift (end/start - 1): [-0.7972, -0.7917, None, 3.0643, None, -0.1729]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 24 at frame 195: holes 0, rim-vs-core 0.56, rim-vs-outside 0.33, heterogeneity 0.10; core [0.953, 0.867, 0.059, 0.442, 0.007, 1.0] rim [0.776, 0.547, 0.127, 0.859, 0.016, 1.0]
  - track 63 at frame 229: holes 0, rim-vs-core 0.59, rim-vs-outside 0.37, heterogeneity 0.10; core [0.967, 0.88, 0.01, 0.458, 0.001, 1.0] rim [0.794, 0.571, 0.024, 0.935, 0.002, 1.0]
  - track 12 at frame 101: holes 0, rim-vs-core 0.61, rim-vs-outside 0.29, heterogeneity 0.11; core [0.952, 0.776, 0.007, 0.076, 0.543, 1.0] rim [0.775, 0.399, 0.016, 0.155, 0.975, 1.0]
  - track 115 at frame 387: holes 0, rim-vs-core 0.59, rim-vs-outside 0.38, heterogeneity 0.10; core [0.961, 0.844, 0.0, 0.017, 0.473, 1.0] rim [0.784, 0.538, 0.0, 0.04, 0.946, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 88 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.824, rim/outside 3.09 (aggregate of 88 individuals; 0/88 membrane-like individually; rim level 0.766)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.739, rim/outside 8.91 (aggregate of 88 individuals; 2/88 membrane-like individually; rim level 0.572)
  - radial s0 (mar 20): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.01, rim/outside 1.98 (aggregate of 88 individuals; 17/88 membrane-like individually; rim level 0.0642)
  - radial s1 (mar 40): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.37, rim/outside 3.28 (aggregate of 88 individuals; 48/88 membrane-like individually; rim level 0.477)
  - radial s2 (mar 60): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.45, rim/outside 3.19 (aggregate of 88 individuals; 33/88 membrane-like individually; rim level 0.229)
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1.04 (aggregate of 88 individuals; 0/88 membrane-like individually; rim level 0.992)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #24 (t=975, R_eq 3.66): ['s0 (mar 20)', 's1 (mar 40)']; #63 (t=1145, R_eq 3.52): ['s1 (mar 40)']; #12 (t=505, R_eq 3.04): ['s0 (mar 20)', 's1 (mar 40)', 's2 (mar 60)']; #115 (t=1935, R_eq 3.57): ['s1 (mar 40)', 's2 (mar 60)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 88 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
