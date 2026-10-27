# Evidence pack: active-nematic-marangoni-distance-pays (seed 611)

- world: `../../../w2/world.py`, family `active-nematic`
- parent: collective/contrib/20261027T0000-c50-marangoni-spread-loop1/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 940s; status ok
- command: `python -m labkit.run /tmp/claude-0/c54/w2/world.py --out /tmp/claude-0/c54/runs/cdep/seed611 --seeds 611 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.64 of robust range [-1.0036, 0.5548], min area 6 px

## Measurements
- components: final 12, mean 11.0, max 18; occupancy final 0.03
- tracks: 88; persistent (alive >= 50% of run): 0; longest 142 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 12, 12], H1 [1, 0, 0]
- motion: 58 long-lived tracks moved >= 1 body length; max speed 0.384/time; max body lengths 9.4
- replication (lineage window K = 20 frames = time 100, default): splits 36, persistent splits 26 (0 more failed only because the siblings re-merged within K), max generation 6, merges 8, merge/split ratio 0.222, nucleations 8
- channel total drift (end/start - 1): [-0.9507, -0.7874, None, 10.7378, -0.9984, -0.323]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 39 at frame 235: holes 0, rim-vs-core 0.45, rim-vs-outside 0.41, heterogeneity 0.11; core [0.964, 0.842, 0.054, 0.455, 0.001, 0.921] rim [0.815, 0.62, 0.097, 0.812, 0.002, 0.885]
  - track 62 at frame 333: holes 0, rim-vs-core 0.56, rim-vs-outside 0.32, heterogeneity 0.10; core [0.97, 0.708, 0.02, 0.489, 0.0, 1.0] rim [0.79, 0.476, 0.038, 0.96, 0.001, 1.0]
  - track 31 at frame 141: holes 0, rim-vs-core 0.46, rim-vs-outside 0.36, heterogeneity 0.08; core [0.952, 0.855, 0.015, 0.452, 0.001, 1.0] rim [0.799, 0.603, 0.034, 0.808, 0.002, 1.0]
  - track 77 at frame 350: holes 0, rim-vs-core 0.52, rim-vs-outside 0.44, heterogeneity 0.09; core [0.986, 0.968, 0.028, 0.247, 0.001, 1.0] rim [0.829, 0.699, 0.063, 0.662, 0.001, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 68 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.835, rim/outside 3.03 (aggregate of 68 individuals; 0/68 membrane-like individually; rim level 0.778)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.778, rim/outside 8.67 (aggregate of 68 individuals; 2/68 membrane-like individually; rim level 0.622)
  - radial s0 (mar 20): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.6, rim/outside 2.86 (aggregate of 68 individuals; 37/68 membrane-like individually; rim level 0.0921)  MEMBRANE-LIKE
  - radial s1 (mar 40): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.36, rim/outside 3.52 (aggregate of 68 individuals; 40/68 membrane-like individually; rim level 0.636)
  - radial s2 (mar 60): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.68, rim/outside 1.61 (aggregate of 68 individuals; 11/68 membrane-like individually; rim level 0.0753)  MEMBRANE-LIKE
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.994, rim/outside 1.03 (aggregate of 68 individuals; 0/68 membrane-like individually; rim level 0.943)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s0 (mar 20), s2 (mar 60)
- membrane-like channels per top track at mid-life: #39 (t=1175, R_eq 3.99): none; #62 (t=1665, R_eq 4.48): none; #31 (t=705, R_eq 4.3): none; #77 (t=1750, R_eq 3.19): ['s0 (mar 20)', 's1 (mar 40)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
