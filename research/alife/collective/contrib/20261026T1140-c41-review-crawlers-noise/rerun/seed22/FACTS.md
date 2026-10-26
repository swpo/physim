# Evidence pack: wavepin-crawler-layer-noise (seed 22)

- world: `../../../20261026T0406-c31-crawlers-from-noise-claim/world.py`, family `crawler-phase-field`
- parent: None; mutation: self-made adsorbed layer s (made by the bound polarity protein, kp*phi*rho; Langmuir adsorption) that excludes a cargo c (kappa); Camley et al. 2017 crawler at low contractility rho*=0.2 with weak noise eta=2 on rho; optional sector cut at cut_t (WORLD_P) and linear-kinetics twin (KIN=1)
- run: 81 frames x 200 steps x dt 0.001 = time 16; grid [256, 256]; wall 557s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0406-c31-crawlers-from-noise-claim/world.py --out collective/contrib/20261026T1140-c41-review-crawlers-noise/rerun --seeds 21 22 --frames 80 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 1, mean 2.0, max 27; occupancy final 0.30
- tracks: 31; persistent (alive >= 50% of run): 1; longest 63 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.13 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 19.6/time; max body lengths 1.7
- replication (lineage window K = 20 frames = time 4, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 4, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [-0.0188, -0.718, -0.6915, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 30 at frame 49: holes 0, rim-vs-core 0.14, rim-vs-outside 1.03, heterogeneity 0.22; core [1.0, 0.175, 0.177, 0.078, 0.311] rim [0.965, 0.273, 0.265, 0.113, 0.313]
  - track 2 at frame 9: holes 0, rim-vs-core 0.27, rim-vs-outside 1.20, heterogeneity 0.23; core [1.0, 0.777, 0.781, 0.069, 0.094] rim [0.923, 0.628, 0.587, 0.145, 0.095]
  - track 8 at frame 8: holes 0, rim-vs-core 0.18, rim-vs-outside 1.17, heterogeneity 0.09; core [1.0, 0.649, 0.656, 0.092, 0.08] rim [0.901, 0.648, 0.589, 0.226, 0.061]
  - track 28 at frame 11: holes 0, rim-vs-core 0.06, rim-vs-outside 1.19, heterogeneity 0.22; core [1.0, 0.552, 0.557, 0.138, 0.098] rim [0.967, 0.531, 0.522, 0.147, 0.122]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 8 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial phi (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.93, rim/outside 13.2 (aggregate of 8 individuals; 0/8 membrane-like individually; rim level 0.923)
  - radial rho (polarity, inside): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.08, rim/outside 8.88 (aggregate of 8 individuals; 4/8 membrane-like individually; rim level 0.372)
  - radial s (layer species): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 1.21, rim/outside 5.7 (aggregate of 8 individuals; 3/8 membrane-like individually; rim level 0.187)
  - radial c (cargo): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.06, rim/outside 3.01 (aggregate of 8 individuals; 1/8 membrane-like individually; rim level 0.194)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #30 (t=9.8, R_eq 79.31): none; #2 (t=1.8, R_eq 34.03): ['s (layer species)']; #8 (t=1.6, R_eq 29.52): ['s (layer species)']; #28 (t=2.2, R_eq 58.1): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: for 5 of 8 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
