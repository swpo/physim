# Evidence pack: wavepin-crawler-layer-noise (seed 4)

- world: `../world.py`, family `crawler-phase-field`
- parent: None; mutation: self-made adsorbed layer s (made by the bound polarity protein, kp*phi*rho; Langmuir adsorption) that excludes a cargo c (kappa); Camley et al. 2017 crawler at low contractility rho*=0.2 with weak noise eta=2 on rho; optional sector cut at cut_t (WORLD_P) and linear-kinetics twin (KIN=1)
- run: 81 frames x 200 steps x dt 0.001 = time 16; grid [256, 256]; wall 369s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0412-c32-review-crawl-noise/world.py --out collective/contrib/20261026T0412-c32-review-crawl-noise/pack4 --seeds 4 --frames 80 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 1, mean 3.5, max 27; occupancy final 0.21
- tracks: 35; persistent (alive >= 50% of run): 1; longest 46 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.13 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 26.7/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 4, default): splits 1, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 6, merge/split ratio 6, nucleations 0
- channel total drift (end/start - 1): [-0.3041, -0.7776, -0.7558, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 28 at frame 24: holes 0, rim-vs-core 0.23, rim-vs-outside 1.14, heterogeneity 0.11; core [1.0, 0.613, 0.636, 0.104, 0.222] rim [0.901, 0.608, 0.568, 0.289, 0.169]
  - track 13 at frame 20: holes 0, rim-vs-core 0.42, rim-vs-outside 1.39, heterogeneity 0.13; core [0.998, 0.99, 0.996, 0.064, 0.184] rim [0.833, 0.989, 0.871, 0.418, 0.081]
  - track 34 at frame 64: holes 0, rim-vs-core 0.11, rim-vs-outside 1.01, heterogeneity 0.22; core [1.0, 0.328, 0.34, 0.124, 0.207] rim [0.972, 0.263, 0.262, 0.14, 0.24]
  - track 10 at frame 16: holes 0, rim-vs-core 0.43, rim-vs-outside 1.31, heterogeneity 0.13; core [0.998, 0.922, 0.948, 0.068, 0.155] rim [0.833, 0.915, 0.79, 0.419, 0.07]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 14 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial phi (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.984, rim/outside 21.6 (aggregate of 14 individuals; 0/14 membrane-like individually; rim level 0.984)
  - radial rho (polarity, inside): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.13, rim/outside 18.9 (aggregate of 14 individuals; 4/14 membrane-like individually; rim level 0.593)
  - radial s (layer species): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 3.49, rim/outside 11.5 (aggregate of 14 individuals; 9/14 membrane-like individually; rim level 0.442)  MEMBRANE-LIKE
  - radial c (cargo): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.16, rim/outside 4.17 (aggregate of 14 individuals; 2/14 membrane-like individually; rim level 0.192)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s (layer species)
- membrane-like channels per top track at mid-life: #28 (t=4.8, R_eq 27.69): ['s (layer species)']; #13 (t=4, R_eq 14.1): ['s (layer species)']; #34 (t=12.8, R_eq 66.72): ['rho (polarity, inside)']; #10 (t=3.2, R_eq 16.27): ['s (layer species)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
