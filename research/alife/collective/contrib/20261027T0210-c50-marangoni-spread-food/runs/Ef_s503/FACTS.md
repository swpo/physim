# Evidence pack: active-nematic-marangoni-spread-food (seed 503)

- world: `../../../world.py`, family `active-nematic`
- parent: collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; mutation: three heritable surfactant kinds with Marangoni coefficients 20/40/60 (majority-feedback production), in-run mutation between neighbouring kinds, trait-blind turnover
- run: 401 frames x 100 steps x dt 0.05 = time 2000; grid [128, 128]; wall 1084s; status ok
- command: `python -m labkit.run /tmp/claude-0/sp3/world.py --out /tmp/claude-0/sp3/runs/Ef/seed503 --seeds 503 --size 128 128 --frames 400 --no-movie`
- segmentation: matter > 0.66 of robust range [-1.0551, 0.5477], min area 6 px

## Measurements
- components: final 5, mean 8.0, max 17; occupancy final 0.02
- tracks: 104; persistent (alive >= 50% of run): 0; longest 146 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [5, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [5, 5, 5], H1 [0, 0, 0]
- motion: 48 long-lived tracks moved >= 1 body length; max speed 0.405/time; max body lengths 12.1
- replication (lineage window K = 20 frames = time 100, default): splits 42, persistent splits 21 (0 more failed only because the siblings re-merged within K), max generation 8, merges 12, merge/split ratio 0.286, nucleations 8
- channel total drift (end/start - 1): [-0.7959, -0.8645, None, 0.2821, None, -0.2625, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 79 at frame 329: holes 0, rim-vs-core 0.56, rim-vs-outside 0.37, heterogeneity 0.11; core [0.986, 0.921, 0.61, 0.0, 0.014, 1.0, 0.0] rim [0.807, 0.568, 1.0, 0.0, 0.035, 0.962, 0.0]
  - track 3 at frame 74: holes 0, rim-vs-core 0.54, rim-vs-outside 0.37, heterogeneity 0.08; core [0.986, 0.9, 0.0, 0.029, 0.671, 1.0, 0.0] rim [0.828, 0.485, 0.001, 0.061, 0.977, 1.0, 0.0]
  - track 82 at frame 333: holes 0, rim-vs-core 0.51, rim-vs-outside 0.35, heterogeneity 0.09; core [0.981, 0.858, 0.016, 0.579, 0.001, 1.0, 0.0] rim [0.836, 0.575, 0.039, 0.979, 0.002, 1.0, 0.0]
  - track 86 at frame 336: holes 0, rim-vs-core 0.54, rim-vs-outside 0.30, heterogeneity 0.09; core [0.973, 0.809, 0.045, 0.0, 0.661, 1.0, 0.0] rim [0.807, 0.422, 0.093, 0.001, 0.999, 1.0, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 43 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial phi (droplet): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.845, rim/outside 2.77 (aggregate of 43 individuals; 0/43 membrane-like individually; rim level 0.795)
  - radial order |Q|: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.808, rim/outside 8.51 (aggregate of 43 individuals; 2/43 membrane-like individually; rim level 0.622)
  - radial s0 (mar 20): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.38, rim/outside 3.01 (aggregate of 43 individuals; 11/43 membrane-like individually; rim level 0.26)
  - radial s1 (mar 40): peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.3, rim/outside 2.87 (aggregate of 43 individuals; 7/43 membrane-like individually; rim level 0.275)
  - radial s2 (mar 60): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.1, rim/outside 2.85 (aggregate of 43 individuals; 11/43 membrane-like individually; rim level 0.262)
  - radial chemostat target phi_b(x,t): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.996, rim/outside 1.04 (aggregate of 43 individuals; 0/43 membrane-like individually; rim level 0.996)
  - radial food patch: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 2.98, rim/outside 0.71 (aggregate of 43 individuals; 0/43 membrane-like individually; rim level 0.0385)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #79 (t=1645, R_eq 4.22): none; #3 (t=370, R_eq 3.39): ['s1 (mar 40)']; #82 (t=1665, R_eq 5.17): none; #86 (t=1680, R_eq 3.39): ['s0 (mar 20)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
