# Evidence pack: wavepin-crawler-layer-noise (seed 24)

- world: `../../20261026T1042-c39-crawlers-noise-long-claim/world.py`, family `crawler-phase-field`
- parent: None; mutation: self-made adsorbed layer s (made by the bound polarity protein, kp*phi*rho; Langmuir adsorption) that excludes a cargo c (kappa); Camley et al. 2017 crawler at low contractility rho*=0.2 with weak noise eta=2 on rho; optional sector cut at cut_t (WORLD_P) and linear-kinetics twin (KIN=1)
- run: 161 frames x 200 steps x dt 0.001 = time 32; grid [256, 256]; wall 1057s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1042-c39-crawlers-noise-long-claim/world.py --out collective/contrib/20261026T1600-c41-review-crawlers-long/rerun24 --seeds 24 --frames 160 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 1, mean 2.3, max 29; occupancy final 0.30
- tracks: 34; persistent (alive >= 50% of run): 1; longest 122 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.11 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 23.9/time; max body lengths 4.1
- replication (lineage window K = 20 frames = time 4, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 5, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [-0.0203, -0.7271, -0.7012, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 33 at frame 99: holes 0, rim-vs-core 0.29, rim-vs-outside 1.05, heterogeneity 0.21; core [1.0, 0.133, 0.136, 0.107, 0.161] rim [0.974, 0.333, 0.332, 0.138, 0.205]
  - track 20 at frame 28: holes 0, rim-vs-core 0.45, rim-vs-outside 1.39, heterogeneity 0.13; core [0.998, 0.992, 0.996, 0.081, 0.177] rim [0.836, 0.991, 0.874, 0.47, 0.074]
  - track 3 at frame 19: holes 0, rim-vs-core 0.39, rim-vs-outside 1.21, heterogeneity 0.23; core [1.0, 0.347, 0.356, 0.096, 0.113] rim [0.948, 0.619, 0.605, 0.2, 0.101]
  - track 32 at frame 27: holes 0, rim-vs-core 0.09, rim-vs-outside 1.05, heterogeneity 0.22; core [1.0, 0.38, 0.389, 0.153, 0.119] rim [0.973, 0.33, 0.328, 0.171, 0.149]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 9 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial phi (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.996, rim/outside 20.4 (aggregate of 9 individuals; 0/9 membrane-like individually; rim level 0.996)
  - radial rho (polarity, inside): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.59, rim/outside 13.6 (aggregate of 9 individuals; 6/9 membrane-like individually; rim level 0.46)  MEMBRANE-LIKE
  - radial s (layer species): peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 2.42, rim/outside 7.54 (aggregate of 9 individuals; 3/9 membrane-like individually; rim level 0.305)  MEMBRANE-LIKE
  - radial c (cargo): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.26, rim/outside 1.98 (aggregate of 9 individuals; 4/9 membrane-like individually; rim level 0.193)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): rho (polarity, inside), s (layer species)
- membrane-like channels per top track at mid-life: #33 (t=19.8, R_eq 79.18): ['rho (polarity, inside)']; #20 (t=5.6, R_eq 14.44): ['s (layer species)']; #3 (t=3.8, R_eq 33.62): ['s (layer species)', 'c (cargo)']; #32 (t=5.4, R_eq 67.92): ['rho (polarity, inside)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: for 5 of 9 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
