# Evidence pack: wavepin-crawler-layer-noise (seed 54)

- world: `../../../20261026T0406-c31-crawlers-from-noise-claim/world.py`, family `crawler-phase-field`
- parent: None; mutation: self-made adsorbed layer s (made by the bound polarity protein, kp*phi*rho; Langmuir adsorption) that excludes a cargo c (kappa); Camley et al. 2017 crawler at low contractility rho*=0.2 with weak noise eta=2 on rho; optional sector cut at cut_t (WORLD_P) and linear-kinetics twin (KIN=1)
- run: 81 frames x 200 steps x dt 0.001 = time 16; grid [256, 256]; wall 434s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0406-c31-crawlers-from-noise-claim/world.py --out collective/contrib/20261026T1745-c45-review-crawlers/rerun/seed54 --seeds 54 --frames 80 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 1, mean 2.5, max 27; occupancy final 0.31
- tracks: 32; persistent (alive >= 50% of run): 2; longest 60 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.16 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 23/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 4, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 5, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [0.0228, -0.7059, -0.6792, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 7 at frame 30: holes 0, rim-vs-core 0.36, rim-vs-outside 1.25, heterogeneity 0.13; core [1.0, 0.811, 0.817, 0.092, 0.237] rim [0.864, 0.806, 0.702, 0.388, 0.134]
  - track 30 at frame 37: holes 0, rim-vs-core 0.05, rim-vs-outside 1.02, heterogeneity 0.22; core [1.0, 0.258, 0.26, 0.135, 0.168] rim [0.977, 0.27, 0.264, 0.153, 0.21]
  - track 31 at frame 70: holes 0, rim-vs-core 0.20, rim-vs-outside 1.05, heterogeneity 0.22; core [1.0, 0.21, 0.212, 0.124, 0.196] rim [0.963, 0.336, 0.327, 0.132, 0.293]
  - track 27 at frame 9: holes 0, rim-vs-core 0.14, rim-vs-outside 1.03, heterogeneity 0.23; core [1.0, 0.357, 0.359, 0.076, 0.073] rim [0.932, 0.429, 0.404, 0.159, 0.09]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 11 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial phi (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.983, rim/outside 15.8 (aggregate of 11 individuals; 0/11 membrane-like individually; rim level 0.983)
  - radial rho (polarity, inside): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.3, rim/outside 12.1 (aggregate of 11 individuals; 6/11 membrane-like individually; rim level 0.507)
  - radial s (layer species): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 2.5, rim/outside 8.78 (aggregate of 11 individuals; 5/11 membrane-like individually; rim level 0.342)  MEMBRANE-LIKE
  - radial c (cargo): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.17, rim/outside 4 (aggregate of 11 individuals; 1/11 membrane-like individually; rim level 0.199)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s (layer species)
- membrane-like channels per top track at mid-life: #7 (t=6, R_eq 21.1): ['s (layer species)']; #30 (t=7.4, R_eq 77.24): ['rho (polarity, inside)']; #31 (t=14, R_eq 79.8): ['rho (polarity, inside)']; #27 (t=1.8, R_eq 40.12): ['rho (polarity, inside)', 's (layer species)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: for 5 of 11 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
