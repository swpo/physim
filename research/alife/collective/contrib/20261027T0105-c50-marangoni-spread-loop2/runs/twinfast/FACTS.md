# Evidence pack: active-nematic-marangoni-spread (seed 501)

- world: `../../../world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 702s; status ok
- command: `python -m labkit.run /tmp/claude-0/sp/world.py --out /tmp/claude-0/sp/runs/twinfast/seed501 --seeds 501 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.63 of robust range [-0.9553, 0.5534], min area 6 px

## Measurements
- components: final 10, mean 15.0, max 23; occupancy final 0.04
- tracks: 125; persistent (alive >= 50% of run): 1; longest 228 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.90 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [14, 11, 10], H1 [0, 0, 0]
- motion: 75 long-lived tracks moved >= 1 body length; max speed 0.444/time; max body lengths 15.8
- replication (lineage window K = 20 frames = time 100, default): splits 48, persistent splits 28 (0 more failed only because the siblings re-merged within K), max generation 6, merges 19, merge/split ratio 0.396, nucleations 9
- channel total drift (end/start - 1): [-0.6769, -0.7149, None, 1.1076, None, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 16 at frame 148: holes 0, rim-vs-core 0.60, rim-vs-outside 0.36, heterogeneity 0.10; core [0.962, 0.903, 0.053, 0.011, 0.415, 1.0] rim [0.792, 0.586, 0.132, 0.031, 0.883, 1.0]
  - track 34 at frame 195: holes 0, rim-vs-core 0.57, rim-vs-outside 0.43, heterogeneity 0.10; core [0.958, 0.951, 0.033, 0.4, 0.012, 1.0] rim [0.753, 0.65, 0.079, 0.836, 0.023, 1.0]
  - track 62 at frame 299: holes 0, rim-vs-core 0.50, rim-vs-outside 0.38, heterogeneity 0.12; core [0.968, 0.704, 0.126, 0.017, 0.429, 1.0] rim [0.81, 0.506, 0.288, 0.048, 0.83, 1.0]
  - track 95 at frame 329: holes 0, rim-vs-core 0.55, rim-vs-outside 0.33, heterogeneity 0.12; core [0.951, 0.668, 0.042, 0.469, 0.034, 1.0] rim [0.757, 0.438, 0.094, 0.923, 0.075, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 95 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.798, rim/outside 3.15 (aggregate of 95 individuals; 0/95 membrane-like individually; rim level 0.721)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.747, rim/outside 8.16 (aggregate of 95 individuals; 5/95 membrane-like individually; rim level 0.547)
  - radial s0 (mar 20): peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 1.2, rim/outside 1.44 (aggregate of 95 individuals; 19/95 membrane-like individually; rim level 0.0617)
  - radial s1 (mar 40): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.42, rim/outside 3.29 (aggregate of 95 individuals; 41/95 membrane-like individually; rim level 0.381)
  - radial s2 (mar 60): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.17, rim/outside 3.1 (aggregate of 95 individuals; 35/95 membrane-like individually; rim level 0.299)
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.995, rim/outside 1.03 (aggregate of 95 individuals; 0/95 membrane-like individually; rim level 0.984)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #16 (t=740, R_eq 3.74): ['s0 (mar 20)']; #34 (t=975, R_eq 4.26): none; #62 (t=1495, R_eq 4.15): ['s1 (mar 40)', 's2 (mar 60)']; #95 (t=1645, R_eq 4.37): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 3 of 95 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
