# Evidence pack: active-nematic-marangoni-distance-pays (seed 600)

- world: `../../../../../../home/user/physim/research/alife/collective/contrib/20261027T0540-c54-distance-pays-loop1/world.py`, family `active-nematic`
- parent: collective/contrib/20261027T0000-c50-marangoni-spread-loop1/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 859s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0540-c54-distance-pays-loop1/world.py --out /tmp/claude-0/c54/runs/glob/seed600 --seeds 600 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.65 of robust range [-1.0145, 0.5523], min area 6 px

## Measurements
- components: final 8, mean 9.7, max 14; occupancy final 0.02
- tracks: 66; persistent (alive >= 50% of run): 0; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 8, 8], H1 [0, 0, 0]
- motion: 45 long-lived tracks moved >= 1 body length; max speed 0.544/time; max body lengths 16.5
- replication (lineage window K = 20 frames = time 100, default): splits 27, persistent splits 17 (0 more failed only because the siblings re-merged within K), max generation 5, merges 7, merge/split ratio 0.259, nucleations 5
- channel total drift (end/start - 1): [-0.8398, -0.8472, None, 0.8681, None, -0.1929]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 38 at frame 303: holes 0, rim-vs-core 0.64, rim-vs-outside 0.36, heterogeneity 0.12; core [0.979, 0.908, 0.485, 0.016, 0.061, 0.964] rim [0.798, 0.576, 0.99, 0.043, 0.18, 0.964]
  - track 46 at frame 313: holes 0, rim-vs-core 0.64, rim-vs-outside 0.38, heterogeneity 0.12; core [0.978, 0.944, 0.042, 0.482, 0.015, 0.964] rim [0.798, 0.598, 0.118, 0.98, 0.04, 0.964]
  - track 26 at frame 212: holes 0, rim-vs-core 0.58, rim-vs-outside 0.36, heterogeneity 0.10; core [0.966, 0.888, 0.006, 0.453, 0.0, 0.964] rim [0.793, 0.575, 0.013, 0.909, 0.0, 0.964]
  - track 60 at frame 366: holes 0, rim-vs-core 0.60, rim-vs-outside 0.35, heterogeneity 0.10; core [0.976, 0.919, 0.021, 0.399, 0.003, 0.952] rim [0.804, 0.557, 0.054, 0.85, 0.006, 0.952]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 59 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.819, rim/outside 2.81 (aggregate of 59 individuals; 0/59 membrane-like individually; rim level 0.75)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.786, rim/outside 7.82 (aggregate of 59 individuals; 3/59 membrane-like individually; rim level 0.585)
  - radial s0 (mar 20): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.09, rim/outside 2.77 (aggregate of 59 individuals; 12/59 membrane-like individually; rim level 0.184)
  - radial s1 (mar 40): peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.23, rim/outside 3.16 (aggregate of 59 individuals; 24/59 membrane-like individually; rim level 0.421)
  - radial s2 (mar 60): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.37, rim/outside 2.15 (aggregate of 59 individuals; 9/59 membrane-like individually; rim level 0.126)
  - radial chemostat target phi_b(x,t): peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.999, rim/outside 1.02 (aggregate of 59 individuals; 0/59 membrane-like individually; rim level 0.964)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #38 (t=1515, R_eq 3.66): ['s0 (mar 20)', 's1 (mar 40)', 's2 (mar 60)']; #46 (t=1565, R_eq 4.58): ['s1 (mar 40)']; #26 (t=1060, R_eq 3.95): none; #60 (t=1830, R_eq 3.04): ['s0 (mar 20)', 's1 (mar 40)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 59 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
