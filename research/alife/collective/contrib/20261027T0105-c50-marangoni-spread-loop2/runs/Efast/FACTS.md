# Evidence pack: active-nematic-marangoni-spread (seed 501)

- world: `../../../world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 705s; status ok
- command: `python -m labkit.run /tmp/claude-0/sp/world.py --out /tmp/claude-0/sp/runs/Efast/seed501 --seeds 501 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.63 of robust range [-0.9555, 0.5517], min area 6 px

## Measurements
- components: final 13, mean 14.8, max 23; occupancy final 0.05
- tracks: 162; persistent (alive >= 50% of run): 1; longest 232 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 3.73 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 14, 13], H1 [0, 0, 0]
- motion: 83 long-lived tracks moved >= 1 body length; max speed 0.513/time; max body lengths 14.4
- replication (lineage window K = 20 frames = time 100, default): splits 61, persistent splits 31 (0 more failed only because the siblings re-merged within K), max generation 5, merges 32, merge/split ratio 0.525, nucleations 9
- channel total drift (end/start - 1): [-0.6769, -0.7296, None, 5.3515, None, 0.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 93 at frame 286: holes 0, rim-vs-core 0.51, rim-vs-outside 0.29, heterogeneity 0.09; core [0.941, 0.576, 0.001, 0.026, 0.549, 1.0] rim [0.768, 0.36, 0.001, 0.043, 0.978, 1.0]
  - track 104 at frame 282: holes 0, rim-vs-core 0.60, rim-vs-outside 0.36, heterogeneity 0.10; core [0.964, 0.834, 0.018, 0.497, 0.01, 1.0] rim [0.788, 0.516, 0.041, 0.976, 0.024, 1.0]
  - track 113 at frame 303: holes 0, rim-vs-core 0.58, rim-vs-outside 0.36, heterogeneity 0.10; core [0.952, 0.833, 0.0, 0.522, 0.021, 1.0] rim [0.767, 0.517, 0.001, 0.973, 0.048, 1.0]
  - track 134 at frame 343: holes 0, rim-vs-core 0.57, rim-vs-outside 0.32, heterogeneity 0.09; core [0.945, 0.812, 0.001, 0.007, 0.537, 1.0] rim [0.767, 0.493, 0.003, 0.016, 0.978, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 92 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.824, rim/outside 3.09 (aggregate of 92 individuals; 0/92 membrane-like individually; rim level 0.737)
  - radial order |Q|: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.792, rim/outside 7.6 (aggregate of 92 individuals; 10/92 membrane-like individually; rim level 0.508)
  - radial s0 (mar 20): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.45, rim/outside 1.48 (aggregate of 92 individuals; 13/92 membrane-like individually; rim level 0.0826)
  - radial s1 (mar 40): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.14, rim/outside 2.93 (aggregate of 92 individuals; 38/92 membrane-like individually; rim level 0.372)
  - radial s2 (mar 60): peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.33, rim/outside 3.21 (aggregate of 92 individuals; 34/92 membrane-like individually; rim level 0.297)
  - radial chemostat target phi_b(x,t): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.997, rim/outside 1.02 (aggregate of 92 individuals; 0/92 membrane-like individually; rim level 0.981)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #93 (t=1430, R_eq 4.11): ['order |Q|']; #104 (t=1410, R_eq 3.52): none; #113 (t=1515, R_eq 3.61): ['s1 (mar 40)', 's2 (mar 60)']; #134 (t=1715, R_eq 3.99): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 92 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
