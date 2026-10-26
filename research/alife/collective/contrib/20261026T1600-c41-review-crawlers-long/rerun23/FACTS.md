# Evidence pack: wavepin-crawler-layer-noise (seed 23)

- world: `../../20261026T1042-c39-crawlers-noise-long-claim/world.py`, family `crawler-phase-field`
- parent: None; mutation: self-made adsorbed layer s (made by the bound polarity protein, kp*phi*rho; Langmuir adsorption) that excludes a cargo c (kappa); Camley et al. 2017 crawler at low contractility rho*=0.2 with weak noise eta=2 on rho; optional sector cut at cut_t (WORLD_P) and linear-kinetics twin (KIN=1)
- run: 161 frames x 200 steps x dt 0.001 = time 32; grid [256, 256]; wall 1052s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1042-c39-crawlers-noise-long-claim/world.py --out collective/contrib/20261026T1600-c41-review-crawlers-long/rerun23 --seeds 23 --frames 160 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 1, mean 3.0, max 21; occupancy final 0.17
- tracks: 27; persistent (alive >= 50% of run): 1; longest 84 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.35 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 26.2/time; max body lengths 3.3
- replication (lineage window K = 20 frames = time 4, default): splits 1, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 4, merge/split ratio 4, nucleations 0
- channel total drift (end/start - 1): [-0.4434, -0.8113, -0.7917, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 18 at frame 42: holes 0, rim-vs-core 0.47, rim-vs-outside 1.36, heterogeneity 0.14; core [0.998, 0.967, 0.982, 0.07, 0.257] rim [0.824, 0.961, 0.824, 0.455, 0.106]
  - track 26 at frame 122: holes 0, rim-vs-core 0.17, rim-vs-outside 1.01, heterogeneity 0.23; core [1.0, 0.345, 0.356, 0.142, 0.101] rim [0.97, 0.285, 0.282, 0.125, 0.238]
  - track 6 at frame 36: holes 0, rim-vs-core 0.30, rim-vs-outside 1.44, heterogeneity 0.13; core [0.997, 0.986, 0.994, 0.07, 0.232] rim [0.891, 0.983, 0.907, 0.316, 0.143]
  - track 7 at frame 31: holes 0, rim-vs-core 0.20, rim-vs-outside 1.12, heterogeneity 0.11; core [1.0, 0.562, 0.58, 0.118, 0.221] rim [0.912, 0.559, 0.526, 0.28, 0.179]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 15 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial phi (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.999, rim/outside 17.2 (aggregate of 15 individuals; 0/15 membrane-like individually; rim level 0.999)
  - radial rho (polarity, inside): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.17, rim/outside 14.6 (aggregate of 15 individuals; 6/15 membrane-like individually; rim level 0.662)
  - radial s (layer species): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 4.55, rim/outside 10.7 (aggregate of 15 individuals; 15/15 membrane-like individually; rim level 0.555)  MEMBRANE-LIKE
  - radial c (cargo): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.3, rim/outside 4.46 (aggregate of 15 individuals; 6/15 membrane-like individually; rim level 0.252)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s (layer species)
- membrane-like channels per top track at mid-life: #18 (t=8.4, R_eq 14.94): ['s (layer species)']; #26 (t=24.4, R_eq 59.25): ['rho (polarity, inside)', 's (layer species)', 'c (cargo)']; #6 (t=7.2, R_eq 14.13): ['s (layer species)']; #7 (t=6.2, R_eq 30.6): ['s (layer species)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
