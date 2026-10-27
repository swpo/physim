# Evidence pack: wavepin-crawler-layer-noise (seed 7)

- world: `../../../20261026T0406-c31-crawlers-from-noise-claim/world.py`, family `crawler-phase-field`
- parent: None; mutation: self-made adsorbed layer s (made by the bound polarity protein, kp*phi*rho; Langmuir adsorption) that excludes a cargo c (kappa); Camley et al. 2017 crawler at low contractility rho*=0.2 with weak noise eta=2 on rho; optional sector cut at cut_t (WORLD_P) and linear-kinetics twin (KIN=1)
- run: 81 frames x 200 steps x dt 0.001 = time 16; grid [256, 256]; wall 402s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0406-c31-crawlers-from-noise-claim/world.py --out collective/contrib/20261026T2213-c46-review-crawlers-noise/rerun/seed7 --seeds 7 --frames 80 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 2, mean 4.0, max 29; occupancy final 0.26
- tracks: 36; persistent (alive >= 50% of run): 2; longest 81 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 1.23 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [2, 2, 2], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 24.2/time; max body lengths 2.0
- replication (lineage window K = 20 frames = time 4, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 7, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [-0.1407, -0.7237, -0.6929, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 40: holes 0, rim-vs-core 0.45, rim-vs-outside 1.35, heterogeneity 0.14; core [0.998, 0.967, 0.98, 0.069, 0.238] rim [0.835, 0.961, 0.831, 0.434, 0.102]
  - track 35 at frame 54: holes 0, rim-vs-core 0.35, rim-vs-outside 1.05, heterogeneity 0.22; core [1.0, 0.063, 0.065, 0.092, 0.182] rim [0.978, 0.308, 0.31, 0.136, 0.194]
  - track 29 at frame 13: holes 0, rim-vs-core 0.25, rim-vs-outside 1.18, heterogeneity 0.11; core [1.0, 0.686, 0.706, 0.08, 0.098] rim [0.888, 0.684, 0.626, 0.285, 0.068]
  - track 31 at frame 15: holes 0, rim-vs-core 0.20, rim-vs-outside 1.14, heterogeneity 0.17; core [1.0, 0.641, 0.659, 0.116, 0.098] rim [0.91, 0.587, 0.551, 0.24, 0.113]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 17 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial phi (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.989, rim/outside 24 (aggregate of 17 individuals; 0/17 membrane-like individually; rim level 0.989)
  - radial rho (polarity, inside): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.03, rim/outside 20 (aggregate of 17 individuals; 4/17 membrane-like individually; rim level 0.677)
  - radial s (layer species): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 4.2, rim/outside 12 (aggregate of 17 individuals; 12/17 membrane-like individually; rim level 0.504)  MEMBRANE-LIKE
  - radial c (cargo): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.14, rim/outside 5 (aggregate of 17 individuals; 3/17 membrane-like individually; rim level 0.168)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s (layer species)
- membrane-like channels per top track at mid-life: #2 (t=8, R_eq 14.34): ['s (layer species)']; #35 (t=10.8, R_eq 71.96): ['rho (polarity, inside)']; #29 (t=2.6, R_eq 22.36): ['s (layer species)']; #31 (t=3, R_eq 33.07): ['s (layer species)', 'c (cargo)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
