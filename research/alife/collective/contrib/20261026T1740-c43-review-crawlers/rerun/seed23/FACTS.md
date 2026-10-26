# Evidence pack: wavepin-crawler-layer-noise (seed 23)

- world: `../../world.py`, family `crawler-phase-field`
- parent: None; mutation: self-made adsorbed layer s (made by the bound polarity protein, kp*phi*rho; Langmuir adsorption) that excludes a cargo c (kappa); Camley et al. 2017 crawler at low contractility rho*=0.2 with weak noise eta=2 on rho; optional sector cut at cut_t (WORLD_P) and linear-kinetics twin (KIN=1)
- run: 81 frames x 200 steps x dt 0.001 = time 16; grid [256, 256]; wall 607s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1740-c43-review-crawlers/world.py --out collective/contrib/20261026T1740-c43-review-crawlers/rerun/seed23 --seeds 23 --frames 80 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 2, mean 4.9, max 21; occupancy final 0.16
- tracks: 26; persistent (alive >= 50% of run): 5; longest 81 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 9.22 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [2, 2, 2], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 20.1/time; max body lengths 2.7
- replication (lineage window K = 20 frames = time 4, default): splits 1, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 3, merge/split ratio 3, nucleations 0
- channel total drift (end/start - 1): [-0.459, -0.7896, -0.7669, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 18 at frame 40: holes 0, rim-vs-core 0.49, rim-vs-outside 1.33, heterogeneity 0.15; core [0.998, 0.929, 0.947, 0.064, 0.389] rim [0.824, 0.932, 0.79, 0.43, 0.16]
  - track 6 at frame 36: holes 0, rim-vs-core 0.31, rim-vs-outside 1.43, heterogeneity 0.14; core [0.997, 0.969, 0.98, 0.064, 0.36] rim [0.891, 0.964, 0.883, 0.297, 0.222]
  - track 7 at frame 31: holes 0, rim-vs-core 0.20, rim-vs-outside 1.12, heterogeneity 0.11; core [1.0, 0.541, 0.556, 0.108, 0.343] rim [0.912, 0.538, 0.504, 0.264, 0.278]
  - track 3 at frame 28: holes 0, rim-vs-core 0.47, rim-vs-outside 1.23, heterogeneity 0.14; core [0.998, 0.849, 0.87, 0.076, 0.329] rim [0.832, 0.839, 0.716, 0.44, 0.137]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 25 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial phi (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.992, rim/outside 16.9 (aggregate of 25 individuals; 0/25 membrane-like individually; rim level 0.992)
  - radial rho (polarity, inside): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.06, rim/outside 16.5 (aggregate of 25 individuals; 5/25 membrane-like individually; rim level 0.734)
  - radial s (layer species): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 5.65, rim/outside 11.3 (aggregate of 25 individuals; 24/25 membrane-like individually; rim level 0.589)  MEMBRANE-LIKE
  - radial c (cargo): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.17, rim/outside 5.92 (aggregate of 25 individuals; 4/25 membrane-like individually; rim level 0.355)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s (layer species)
- membrane-like channels per top track at mid-life: #18 (t=8, R_eq 14.95): ['s (layer species)']; #6 (t=7.2, R_eq 14.13): ['s (layer species)']; #7 (t=6.2, R_eq 30.6): ['s (layer species)']; #3 (t=5.6, R_eq 16.96): ['s (layer species)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
