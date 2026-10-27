# Evidence pack: active-nematic-marangoni-distance-pays (seed 601)

- world: `../../../../../../home/user/physim/research/alife/collective/contrib/20261027T0540-c54-distance-pays-loop1/world.py`, family `active-nematic`
- parent: collective/contrib/20261027T0000-c50-marangoni-spread-loop1/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 897s; status ok
- command: `python -m labkit.run collective/contrib/20261027T0540-c54-distance-pays-loop1/world.py --out /tmp/claude-0/c54/runs/dep07/seed601 --seeds 601 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.64 of robust range [-1.0054, 0.5612], min area 6 px

## Measurements
- components: final 12, mean 10.6, max 21; occupancy final 0.04
- tracks: 79; persistent (alive >= 50% of run): 2; longest 210 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.89 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [15, 12, 12], H1 [2, 0, 0]
- motion: 48 long-lived tracks moved >= 1 body length; max speed 0.449/time; max body lengths 11.8
- replication (lineage window K = 20 frames = time 100, default): splits 31, persistent splits 21 (0 more failed only because the siblings re-merged within K), max generation 4, merges 5, merge/split ratio 0.161, nucleations 12
- channel total drift (end/start - 1): [-0.6304, -0.7443, None, 4.3115, None, -0.1186]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 20 at frame 134: holes 0, rim-vs-core 0.48, rim-vs-outside 0.32, heterogeneity 0.11; core [0.977, 0.487, 0.006, 0.477, 0.001, 1.0] rim [0.834, 0.317, 0.014, 0.905, 0.001, 1.0]
  - track 11 at frame 128: holes 0, rim-vs-core 0.44, rim-vs-outside 0.28, heterogeneity 0.09; core [0.962, 0.606, 0.002, 0.41, 0.0, 1.0] rim [0.808, 0.417, 0.005, 0.776, 0.001, 1.0]
  - track 19 at frame 121: holes 0, rim-vs-core 0.52, rim-vs-outside 0.34, heterogeneity 0.09; core [0.968, 0.791, 0.001, 0.407, 0.0, 1.0] rim [0.806, 0.518, 0.003, 0.823, 0.001, 1.0]
  - track 69 at frame 380: holes 0, rim-vs-core 0.67, rim-vs-outside 0.37, heterogeneity 0.12; core [0.977, 0.923, 0.052, 0.381, 0.002, 0.833] rim [0.772, 0.501, 0.135, 0.858, 0.005, 0.854]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 64 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.847, rim/outside 3.08 (aggregate of 64 individuals; 0/64 membrane-like individually; rim level 0.783)
  - radial order |Q|: peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.817, rim/outside 8.82 (aggregate of 64 individuals; 6/64 membrane-like individually; rim level 0.605)
  - radial s0 (mar 20): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.17, rim/outside 1.6 (aggregate of 64 individuals; 12/64 membrane-like individually; rim level 0.128)
  - radial s1 (mar 40): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.29, rim/outside 3.37 (aggregate of 64 individuals; 37/64 membrane-like individually; rim level 0.589)
  - radial s2 (mar 60): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.76, rim/outside 1.81 (aggregate of 64 individuals; 10/64 membrane-like individually; rim level 0.0525)  MEMBRANE-LIKE
  - radial chemostat target phi_b(x,t): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1.02 (aggregate of 64 individuals; 0/64 membrane-like individually; rim level 0.923)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s2 (mar 60)
- membrane-like channels per top track at mid-life: #20 (t=670, R_eq 4.79): ['order |Q|']; #11 (t=640, R_eq 4.26): none; #19 (t=605, R_eq 4.69): none; #69 (t=1900, R_eq 3.09): ['s0 (mar 20)', 's1 (mar 40)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 1 of 64 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
