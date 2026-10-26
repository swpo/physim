# Evidence pack: wavepin-crawler-layer-noise (seed 53)

- world: `../../../20261026T0406-c31-crawlers-from-noise-claim/world.py`, family `crawler-phase-field`
- parent: None; mutation: self-made adsorbed layer s (made by the bound polarity protein, kp*phi*rho; Langmuir adsorption) that excludes a cargo c (kappa); Camley et al. 2017 crawler at low contractility rho*=0.2 with weak noise eta=2 on rho; optional sector cut at cut_t (WORLD_P) and linear-kinetics twin (KIN=1)
- run: 81 frames x 200 steps x dt 0.001 = time 16; grid [256, 256]; wall 431s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0406-c31-crawlers-from-noise-claim/world.py --out collective/contrib/20261026T1745-c45-review-crawlers/rerun/seed53 --seeds 53 --frames 80 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 3, mean 3.7, max 26; occupancy final 0.12
- tracks: 26; persistent (alive >= 50% of run): 3; longest 81 frames; alive start-to-end: 3
- size of persistent tracks: max/min area ratio 1.96 (1 = constant size)
- enclosures: components with a hole mean 0.04, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [3, 3, 3], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.1
- replication (lineage window K = 20 frames = time 4, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [-0.6005, -0.7419, -0.7139, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 40: holes 0, rim-vs-core 0.14, rim-vs-outside 1.29, heterogeneity 0.13; core [1.0, 0.643, 0.661, 0.106, 0.594] rim [0.949, 0.624, 0.609, 0.197, 0.525]
  - track 7 at frame 40: holes 0, rim-vs-core 0.14, rim-vs-outside 1.34, heterogeneity 0.14; core [1.0, 0.671, 0.69, 0.103, 0.605] rim [0.943, 0.677, 0.657, 0.202, 0.526]
  - track 20 at frame 40: holes 0, rim-vs-core 0.43, rim-vs-outside 1.37, heterogeneity 0.15; core [1.0, 0.895, 0.916, 0.082, 0.608] rim [0.864, 0.886, 0.787, 0.357, 0.342]
  - track 1 at frame 7: holes 0, rim-vs-core 0.08, rim-vs-outside 0.92, heterogeneity 0.14; core [1.0, 0.106, 0.109, 0.075, 0.126] rim [0.956, 0.149, 0.144, 0.105, 0.132]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 19 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial phi (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 10.3 (aggregate of 19 individuals; 0/19 membrane-like individually; rim level 1)
  - radial rho (polarity, inside): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.996, rim/outside 9.84 (aggregate of 19 individuals; 0/19 membrane-like individually; rim level 0.699)
  - radial s (layer species): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 4.28, rim/outside 8.56 (aggregate of 19 individuals; 19/19 membrane-like individually; rim level 0.518)  MEMBRANE-LIKE
  - radial c (cargo): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.26, rim/outside 6.24 (aggregate of 19 individuals; 1/19 membrane-like individually; rim level 0.705)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s (layer species)
- membrane-like channels per top track at mid-life: #0 (t=8, R_eq 33.36): ['s (layer species)']; #7 (t=8, R_eq 30.81): ['s (layer species)']; #20 (t=8, R_eq 21.11): ['s (layer species)']; #1 (t=1.4, R_eq 44.46): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
