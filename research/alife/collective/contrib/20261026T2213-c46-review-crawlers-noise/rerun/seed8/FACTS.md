# Evidence pack: wavepin-crawler-layer-noise (seed 8)

- world: `../../../20261026T0406-c31-crawlers-from-noise-claim/world.py`, family `crawler-phase-field`
- parent: None; mutation: self-made adsorbed layer s (made by the bound polarity protein, kp*phi*rho; Langmuir adsorption) that excludes a cargo c (kappa); Camley et al. 2017 crawler at low contractility rho*=0.2 with weak noise eta=2 on rho; optional sector cut at cut_t (WORLD_P) and linear-kinetics twin (KIN=1)
- run: 81 frames x 200 steps x dt 0.001 = time 16; grid [256, 256]; wall 409s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0406-c31-crawlers-from-noise-claim/world.py --out collective/contrib/20261026T2213-c46-review-crawlers-noise/rerun/seed8 --seeds 8 --frames 80 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 1, mean 2.7, max 25; occupancy final 0.31
- tracks: 30; persistent (alive >= 50% of run): 1; longest 47 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.12 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 26.5/time; max body lengths 1.7
- replication (lineage window K = 20 frames = time 4, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 5, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [0.0314, -0.7299, -0.7044, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 29 at frame 57: holes 0, rim-vs-core 0.33, rim-vs-outside 1.07, heterogeneity 0.22; core [1.0, 0.121, 0.123, 0.101, 0.261] rim [0.974, 0.353, 0.349, 0.144, 0.248]
  - track 22 at frame 17: holes 0, rim-vs-core 0.21, rim-vs-outside 1.13, heterogeneity 0.11; core [1.0, 0.603, 0.613, 0.101, 0.175] rim [0.903, 0.605, 0.556, 0.277, 0.141]
  - track 17 at frame 16: holes 0, rim-vs-core 0.17, rim-vs-outside 1.14, heterogeneity 0.10; core [1.0, 0.592, 0.602, 0.11, 0.15] rim [0.914, 0.593, 0.551, 0.25, 0.122]
  - track 19 at frame 14: holes 0, rim-vs-core 0.41, rim-vs-outside 1.35, heterogeneity 0.13; core [0.998, 0.956, 0.965, 0.065, 0.139] rim [0.835, 0.958, 0.821, 0.409, 0.065]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 12 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial phi (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.961, rim/outside 8.21 (aggregate of 12 individuals; 0/12 membrane-like individually; rim level 0.96)
  - radial rho (polarity, inside): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.14, rim/outside 6.15 (aggregate of 12 individuals; 5/12 membrane-like individually; rim level 0.495)
  - radial s (layer species): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 2.66, rim/outside 6.43 (aggregate of 12 individuals; 6/12 membrane-like individually; rim level 0.345)  MEMBRANE-LIKE
  - radial c (cargo): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.09, rim/outside 2.31 (aggregate of 12 individuals; 0/12 membrane-like individually; rim level 0.201)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s (layer species)
- membrane-like channels per top track at mid-life: #29 (t=11.4, R_eq 80.95): ['rho (polarity, inside)']; #22 (t=3.4, R_eq 28.6): ['s (layer species)']; #17 (t=3.2, R_eq 32.15): ['s (layer species)']; #19 (t=2.8, R_eq 16.09): ['s (layer species)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: for 4 of 12 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
