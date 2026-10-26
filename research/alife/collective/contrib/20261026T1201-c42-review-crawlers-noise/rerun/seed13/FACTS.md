# Evidence pack: wavepin-crawler-layer-noise (seed 13)

- world: `../../../20261026T0406-c31-crawlers-from-noise-claim/world.py`, family `crawler-phase-field`
- parent: None; mutation: self-made adsorbed layer s (made by the bound polarity protein, kp*phi*rho; Langmuir adsorption) that excludes a cargo c (kappa); Camley et al. 2017 crawler at low contractility rho*=0.2 with weak noise eta=2 on rho; optional sector cut at cut_t (WORLD_P) and linear-kinetics twin (KIN=1)
- run: 81 frames x 200 steps x dt 0.001 = time 16; grid [256, 256]; wall 518s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0406-c31-crawlers-from-noise-claim/world.py --out collective/contrib/20261026T1201-c42-review-crawlers-noise/rerun/seed13 --seeds 13 --frames 80 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 1, mean 3.0, max 32; occupancy final 0.27
- tracks: 37; persistent (alive >= 50% of run): 1; longest 52 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.14 (1 = constant size)
- enclosures: components with a hole mean 0.02, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 26.5/time; max body lengths 2.0
- replication (lineage window K = 20 frames = time 4, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 5, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [-0.1086, -0.7411, -0.7149, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 36 at frame 55: holes 0, rim-vs-core 0.07, rim-vs-outside 1.01, heterogeneity 0.21; core [1.0, 0.248, 0.253, 0.128, 0.172] rim [0.973, 0.252, 0.248, 0.122, 0.235]
  - track 1 at frame 14: holes 0, rim-vs-core 0.21, rim-vs-outside 1.13, heterogeneity 0.10; core [1.0, 0.615, 0.626, 0.099, 0.125] rim [0.9, 0.605, 0.555, 0.268, 0.098]
  - track 12 at frame 12: holes 0, rim-vs-core 0.38, rim-vs-outside 1.34, heterogeneity 0.12; core [0.998, 0.945, 0.956, 0.063, 0.11] rim [0.841, 0.954, 0.823, 0.383, 0.054]
  - track 9 at frame 12: holes 0, rim-vs-core 0.39, rim-vs-outside 1.34, heterogeneity 0.12; core [0.998, 0.957, 0.967, 0.063, 0.11] rim [0.84, 0.955, 0.823, 0.384, 0.054]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 12 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial phi (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.967, rim/outside 14.6 (aggregate of 12 individuals; 0/12 membrane-like individually; rim level 0.967)
  - radial rho (polarity, inside): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.21, rim/outside 11.3 (aggregate of 12 individuals; 5/12 membrane-like individually; rim level 0.532)
  - radial s (layer species): peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 2.59, rim/outside 8.42 (aggregate of 12 individuals; 7/12 membrane-like individually; rim level 0.332)  MEMBRANE-LIKE
  - radial c (cargo): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.15, rim/outside 3.66 (aggregate of 12 individuals; 1/12 membrane-like individually; rim level 0.162)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s (layer species)
- membrane-like channels per top track at mid-life: #36 (t=11, R_eq 75.01): ['rho (polarity, inside)']; #1 (t=2.8, R_eq 29.81): ['s (layer species)']; #12 (t=2.4, R_eq 16.24): ['s (layer species)']; #9 (t=2.4, R_eq 16.12): ['s (layer species)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: for 3 of 12 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
