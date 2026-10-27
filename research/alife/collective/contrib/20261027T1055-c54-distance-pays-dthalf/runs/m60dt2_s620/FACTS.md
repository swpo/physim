# Evidence pack: active-nematic-marangoni-distance-pays (seed 620)

- world: `../../../w2/world.py`, family `active-nematic`
- parent: collective/contrib/20261027T0000-c50-marangoni-spread-loop1/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 200 steps x dt 0.05 = time 4000; grid [128, 128]; wall 2015s; status ok
- command: `python -m labkit.run /tmp/claude-0/c54/w2/world.py --out /tmp/claude-0/c54/runs/m60dt2/seed620 --seeds 620 --size 128 128 --frames 400 --spf 200 --no-movie`
- segmentation: matter > 0.67 of robust range [-1.0166, 0.495], min area 6 px

## Measurements
- components: final 7, mean 4.6, max 9; occupancy final 0.02
- tracks: 49; persistent (alive >= 50% of run): 0; longest 140 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 7, 7], H1 [1, 0, 0]
- motion: 28 long-lived tracks moved >= 1 body length; max speed 0.237/time; max body lengths 15.6
- replication (lineage window K = 20 frames = time 200, default): splits 21, persistent splits 12 (0 more failed only because the siblings re-merged within K), max generation 6, merges 3, merge/split ratio 0.143, nucleations 4
- channel total drift (end/start - 1): [-0.7706, -0.8781, None, None, 3.3938, -0.2209]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 94: holes 0, rim-vs-core 0.62, rim-vs-outside 0.48, heterogeneity 0.13; core [1.0, 0.992, 0.231, 0.231, 0.472, 1.0] rim [0.906, 0.734, 0.427, 0.427, 0.951, 1.0]
  - track 26 at frame 319: holes 0, rim-vs-core 0.36, rim-vs-outside 0.48, heterogeneity 0.20; core [1.0, 0.899, 0.256, 0.256, 0.661, 0.846] rim [0.91, 0.715, 0.384, 0.384, 0.886, 0.808]
  - track 29 at frame 333: holes 0, rim-vs-core 0.47, rim-vs-outside 0.24, heterogeneity 0.09; core [1.0, 0.338, 0.247, 0.247, 0.6, 1.0] rim [0.884, 0.226, 0.415, 0.415, 0.977, 1.0]
  - track 38 at frame 363: holes 0, rim-vs-core 0.60, rim-vs-outside 0.46, heterogeneity 0.13; core [0.998, 0.965, 0.229, 0.229, 0.521, 0.833] rim [0.896, 0.704, 0.427, 0.427, 0.968, 0.833]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 28 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.92, rim/outside 2.93 (aggregate of 28 individuals; 0/28 membrane-like individually; rim level 0.901)
  - radial order |Q|: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 0.831, rim/outside 9.65 (aggregate of 28 individuals; 0/28 membrane-like individually; rim level 0.768)
  - radial s0 (mar 20): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.6, rim/outside 3.48 (aggregate of 28 individuals; 20/28 membrane-like individually; rim level 0.392)  MEMBRANE-LIKE
  - radial s1 (mar 40): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.6, rim/outside 3.48 (aggregate of 28 individuals; 20/28 membrane-like individually; rim level 0.392)  MEMBRANE-LIKE
  - radial s2 (mar 60): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.58, rim/outside 3.45 (aggregate of 28 individuals; 21/28 membrane-like individually; rim level 0.811)  MEMBRANE-LIKE
  - radial chemostat target phi_b(x,t): peak at rho=1.45 (in the peak band 0.5-1.5), rim/core 1.01, rim/outside 1.01 (aggregate of 28 individuals; 0/28 membrane-like individually; rim level 0.889)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s0 (mar 20), s1 (mar 40), s2 (mar 60)
- membrane-like channels per top track at mid-life: #4 (t=940, R_eq 3.09): ['s0 (mar 20)', 's1 (mar 40)', 's2 (mar 60)']; #26 (t=3190, R_eq 3.52): ['s0 (mar 20)', 's1 (mar 40)']; #29 (t=3330, R_eq 2.26): ['s0 (mar 20)', 's1 (mar 40)', 's2 (mar 60)']; #38 (t=3630, R_eq 3.24): ['s0 (mar 20)', 's1 (mar 40)', 's2 (mar 60)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 28 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
