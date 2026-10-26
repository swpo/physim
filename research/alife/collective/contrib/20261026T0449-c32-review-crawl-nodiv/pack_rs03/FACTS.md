# Evidence pack: wavepin-crawler-layer-noise (seed 2)

- world: `../world.py`, family `crawler-phase-field`
- parent: None; mutation: self-made adsorbed layer s (made by the bound polarity protein, kp*phi*rho; Langmuir adsorption) that excludes a cargo c (kappa); Camley et al. 2017 crawler at low contractility rho*=0.2 with weak noise eta=2 on rho; optional sector cut at cut_t (WORLD_P) and linear-kinetics twin (KIN=1)
- run: 71 frames x 200 steps x dt 0.001 = time 14; grid [256, 256]; wall 332s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0449-c32-review-crawl-nodiv/world.py --out collective/contrib/20261026T0449-c32-review-crawl-nodiv/pack_rs03 --seeds 2 --frames 70 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 2, mean 4.9, max 24; occupancy final 0.27
- tracks: 31; persistent (alive >= 50% of run): 4; longest 70 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 8.88 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [2, 2, 2], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 20 frames = time 4, default): splits 1, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 5, merge/split ratio 5, nucleations 0
- channel total drift (end/start - 1): [-0.1206, -0.6052, -0.5648, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 26 at frame 36: holes 0, rim-vs-core 0.28, rim-vs-outside 1.27, heterogeneity 0.12; core [1.0, 0.774, 0.792, 0.094, 0.264] rim [0.886, 0.777, 0.705, 0.312, 0.174]
  - track 19 at frame 27: holes 0, rim-vs-core 0.47, rim-vs-outside 1.32, heterogeneity 0.14; core [0.998, 0.939, 0.954, 0.085, 0.296] rim [0.83, 0.932, 0.793, 0.457, 0.114]
  - track 24 at frame 26: holes 0, rim-vs-core 0.09, rim-vs-outside 1.20, heterogeneity 0.10; core [1.0, 0.581, 0.594, 0.124, 0.187] rim [0.955, 0.582, 0.569, 0.196, 0.172]
  - track 21 at frame 21: holes 0, rim-vs-core 0.42, rim-vs-outside 1.35, heterogeneity 0.12; core [0.998, 0.965, 0.977, 0.072, 0.172] rim [0.832, 0.96, 0.825, 0.413, 0.072]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 25 components >= 12 px at frames [12, 23, 35, 47, 58, 70]):
  - radial phi (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 9.93 (aggregate of 25 individuals; 0/25 membrane-like individually; rim level 1)
  - radial rho (polarity, inside): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.04, rim/outside 9.66 (aggregate of 25 individuals; 3/25 membrane-like individually; rim level 0.7)
  - radial s (layer species): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 3.5, rim/outside 7.87 (aggregate of 25 individuals; 20/25 membrane-like individually; rim level 0.479)  MEMBRANE-LIKE
  - radial c (cargo): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.24, rim/outside 5.64 (aggregate of 25 individuals; 3/25 membrane-like individually; rim level 0.243)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s (layer species)
- membrane-like channels per top track at mid-life: #26 (t=7.2, R_eq 23.32): ['s (layer species)']; #19 (t=5.4, R_eq 17.72): ['s (layer species)']; #24 (t=5.2, R_eq 38.75): ['s (layer species)']; #21 (t=4.2, R_eq 16.83): ['s (layer species)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
