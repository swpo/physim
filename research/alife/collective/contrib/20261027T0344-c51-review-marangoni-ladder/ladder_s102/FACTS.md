# Evidence pack: active-nematic-marangoni-ladder (seed 102)

- world: `../../20261026T2018-c45-marangoni-ladder/world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 656s; status ok
- command: `python -m labkit.run collective/contrib/20261026T2018-c45-marangoni-ladder/world.py --out collective/contrib/20261027T0344-c51-review-marangoni-ladder/ladder_s102 --seeds 102 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.58 of robust range [-0.8289, 0.5968], min area 6 px

## Measurements
- components: final 23, mean 18.5, max 27; occupancy final 0.08
- tracks: 263; persistent (alive >= 50% of run): 0; longest 130 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [28, 23, 23], H1 [1, 0, 0]
- motion: 117 long-lived tracks moved >= 1 body length; max speed 0.433/time; max body lengths 10.9
- replication (lineage window K = 20 frames = time 100, default): splits 114, persistent splits 50 (0 more failed only because the siblings re-merged within K), max generation 10, merges 27, merge/split ratio 0.237, nucleations 5
- channel total drift (end/start - 1): [-0.4886, -0.5122, 2.864, 4.2865, 8.1204]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 141 at frame 276: holes 0, rim-vs-core 0.67, rim-vs-outside 0.42, heterogeneity 0.14; core [0.96, 0.941, 0.013, 0.424, 0.025] rim [0.741, 0.626, 0.033, 0.976, 0.073]
  - track 78 at frame 188: holes 0, rim-vs-core 0.68, rim-vs-outside 0.41, heterogeneity 0.14; core [0.974, 0.926, 0.325, 0.018, 0.002] rim [0.776, 0.617, 0.898, 0.063, 0.007]
  - track 88 at frame 208: holes 0, rim-vs-core 0.64, rim-vs-outside 0.35, heterogeneity 0.14; core [0.972, 0.766, 0.375, 0.014, 0.003] rim [0.759, 0.517, 0.92, 0.042, 0.007]
  - track 253 at frame 383: holes 0, rim-vs-core 0.59, rim-vs-outside 0.39, heterogeneity 0.12; core [0.931, 0.807, 0.005, 0.014, 0.486] rim [0.729, 0.498, 0.01, 0.033, 0.944]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 123 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.791, rim/outside 4.22 (aggregate of 123 individuals; 0/123 membrane-like individually; rim level 0.678)
  - radial order |Q|: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.811, rim/outside 7.63 (aggregate of 123 individuals; 13/123 membrane-like individually; rim level 0.501)
  - radial s0 (mar 20): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.01, rim/outside 2.86 (aggregate of 123 individuals; 24/123 membrane-like individually; rim level 0.171)
  - radial s1 (mar 40): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.21, rim/outside 3.12 (aggregate of 123 individuals; 35/123 membrane-like individually; rim level 0.262)
  - radial s2 (mar 60): peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.09, rim/outside 2.87 (aggregate of 123 individuals; 23/123 membrane-like individually; rim level 0.24)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #141 (t=1380, R_eq 4.58): ['s0 (mar 20)', 's2 (mar 60)']; #78 (t=940, R_eq 4.58): none; #88 (t=1040, R_eq 4.37): ['s0 (mar 20)', 's1 (mar 40)']; #253 (t=1915, R_eq 3.74): ['s1 (mar 40)', 's2 (mar 60)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 123 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
