# Evidence pack: wavepin-crawler-layer-noise (seed 14)

- world: `../../../20261026T0406-c31-crawlers-from-noise-claim/world.py`, family `crawler-phase-field`
- parent: None; mutation: self-made adsorbed layer s (made by the bound polarity protein, kp*phi*rho; Langmuir adsorption) that excludes a cargo c (kappa); Camley et al. 2017 crawler at low contractility rho*=0.2 with weak noise eta=2 on rho; optional sector cut at cut_t (WORLD_P) and linear-kinetics twin (KIN=1)
- run: 81 frames x 200 steps x dt 0.001 = time 16; grid [256, 256]; wall 518s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0406-c31-crawlers-from-noise-claim/world.py --out collective/contrib/20261026T1201-c42-review-crawlers-noise/rerun/seed14 --seeds 14 --frames 80 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 1, mean 2.9, max 32; occupancy final 0.28
- tracks: 36; persistent (alive >= 50% of run): 1; longest 50 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.10 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 26.7/time; max body lengths 1.9
- replication (lineage window K = 20 frames = time 4, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 4, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [-0.0903, -0.7401, -0.7135, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 35 at frame 56: holes 0, rim-vs-core 0.08, rim-vs-outside 1.01, heterogeneity 0.21; core [1.0, 0.238, 0.244, 0.133, 0.168] rim [0.974, 0.252, 0.249, 0.128, 0.243]
  - track 20 at frame 17: holes 0, rim-vs-core 0.32, rim-vs-outside 1.43, heterogeneity 0.13; core [0.998, 0.986, 0.992, 0.067, 0.145] rim [0.871, 0.99, 0.896, 0.338, 0.085]
  - track 12 at frame 15: holes 0, rim-vs-core 0.25, rim-vs-outside 1.13, heterogeneity 0.25; core [1.0, 0.665, 0.68, 0.09, 0.134] rim [0.901, 0.592, 0.549, 0.256, 0.179]
  - track 26 at frame 11: holes 0, rim-vs-core 0.23, rim-vs-outside 1.16, heterogeneity 0.10; core [1.0, 0.658, 0.676, 0.083, 0.095] rim [0.887, 0.668, 0.608, 0.273, 0.068]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 11 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial phi (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.996, rim/outside 26.3 (aggregate of 11 individuals; 0/11 membrane-like individually; rim level 0.996)
  - radial rho (polarity, inside): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.23, rim/outside 16.1 (aggregate of 11 individuals; 6/11 membrane-like individually; rim level 0.489)
  - radial s (layer species): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 2.34, rim/outside 9.39 (aggregate of 11 individuals; 5/11 membrane-like individually; rim level 0.327)  MEMBRANE-LIKE
  - radial c (cargo): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.23, rim/outside 3.93 (aggregate of 11 individuals; 3/11 membrane-like individually; rim level 0.169)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s (layer species)
- membrane-like channels per top track at mid-life: #35 (t=11.2, R_eq 76): ['rho (polarity, inside)']; #20 (t=3.4, R_eq 14.68): ['s (layer species)']; #12 (t=3, R_eq 28.75): ['s (layer species)', 'c (cargo)']; #26 (t=2.2, R_eq 25.67): ['s (layer species)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: for 4 of 11 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
