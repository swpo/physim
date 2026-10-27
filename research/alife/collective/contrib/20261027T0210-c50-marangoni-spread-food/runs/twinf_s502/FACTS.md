# Evidence pack: active-nematic-marangoni-spread-food (seed 502)

- world: `../../../world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 1017s; status ok
- command: `python -m labkit.run /tmp/claude-0/sp3/world.py --out /tmp/claude-0/sp3/runs/twinf/seed502 --seeds 502 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.65 of robust range [-1.0335, 0.545], min area 6 px

## Measurements
- components: final 6, mean 10.4, max 19; occupancy final 0.02
- tracks: 124; persistent (alive >= 50% of run): 0; longest 125 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [3, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 6, 5], H1 [0, 0, 0]
- motion: 72 long-lived tracks moved >= 1 body length; max speed 0.349/time; max body lengths 12.9
- replication (lineage window K = 20 frames = time 100, default): splits 55, persistent splits 30 (0 more failed only because the siblings re-merged within K), max generation 7, merges 8, merge/split ratio 0.145, nucleations 7
- channel total drift (end/start - 1): [-0.9262, -0.8778, None, 2.6901, None, -0.1876, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 16 at frame 108: holes 0, rim-vs-core 0.55, rim-vs-outside 0.38, heterogeneity 0.09; core [0.965, 0.905, 0.06, 0.522, 0.023, 1.0, 0.0] rim [0.797, 0.594, 0.101, 0.94, 0.048, 1.0, 0.0]
  - track 14 at frame 101: holes 0, rim-vs-core 0.57, rim-vs-outside 0.41, heterogeneity 0.09; core [0.98, 0.947, 0.024, 0.385, 0.001, 1.0, 0.0] rim [0.802, 0.651, 0.066, 0.836, 0.003, 1.0, 0.0]
  - track 51 at frame 212: holes 0, rim-vs-core 0.49, rim-vs-outside 0.47, heterogeneity 0.09; core [0.976, 0.929, 0.001, 0.003, 0.44, 1.0, 0.0] rim [0.841, 0.691, 0.002, 0.007, 0.851, 1.0, 0.0]
  - track 94 at frame 350: holes 0, rim-vs-core 0.70, rim-vs-outside 0.42, heterogeneity 0.09; core [0.99, 0.944, 0.002, 0.009, 0.302, 1.0, 0.0] rim [0.839, 0.605, 0.006, 0.036, 0.892, 1.0, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 68 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.837, rim/outside 2.67 (aggregate of 68 individuals; 0/68 membrane-like individually; rim level 0.77)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.764, rim/outside 8.15 (aggregate of 68 individuals; 5/68 membrane-like individually; rim level 0.58)
  - radial s0 (mar 20): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.32, rim/outside 1.34 (aggregate of 68 individuals; 13/68 membrane-like individually; rim level 0.0663)
  - radial s1 (mar 40): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.27, rim/outside 3.22 (aggregate of 68 individuals; 36/68 membrane-like individually; rim level 0.467)
  - radial s2 (mar 60): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.55, rim/outside 2.79 (aggregate of 68 individuals; 29/68 membrane-like individually; rim level 0.227)  MEMBRANE-LIKE
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1.02 (aggregate of 68 individuals; 0/68 membrane-like individually; rim level 0.988)
  - radial food patch: peak at rho=2.25 (OUTSIDE the peak band 0.5-1.5), rim/core 1.29, rim/outside 0.925 (aggregate of 68 individuals; 1/68 membrane-like individually; rim level 0.0956)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s2 (mar 60)
- membrane-like channels per top track at mid-life: #16 (t=540, R_eq 3.87): ['s2 (mar 60)']; #14 (t=505, R_eq 4.03): ['s0 (mar 20)', 's1 (mar 40)']; #51 (t=1060, R_eq 3.48): ['s2 (mar 60)']; #94 (t=1750, R_eq 3.04): ['s1 (mar 40)', 's2 (mar 60)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 68 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
