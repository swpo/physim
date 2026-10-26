# Evidence pack: wavepin-crawler-layer-noise (seed 1)

- world: `../../world.py`, family `crawler-phase-field`
- parent: None; mutation: self-made adsorbed layer s (made by the bound polarity protein, kp*phi*rho; Langmuir adsorption) that excludes a cargo c (kappa); Camley et al. 2017 crawler at low contractility rho*=0.2 with weak noise eta=2 on rho; optional sector cut at cut_t (WORLD_P) and linear-kinetics twin (KIN=1)
- run: 161 frames x 200 steps x dt 0.001 = time 32; grid [256, 256]; wall 1021s; status ok
- command: `python -m labkit.run collective/contrib/c39-crawl-long-wip/world.py --out collective/contrib/c39-crawl-long-wip/pack/seed1 --seeds 1 --frames 160 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 1, mean 2.3, max 32; occupancy final 0.27
- tracks: 36; persistent (alive >= 50% of run): 1; longest 85 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.06 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 24.1/time; max body lengths 3.6
- replication (lineage window K = 20 frames = time 4, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 4, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [-0.1257, -0.7459, -0.7205, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 35 at frame 118: holes 0, rim-vs-core 0.20, rim-vs-outside 1.00, heterogeneity 0.22; core [1.0, 0.369, 0.373, 0.139, 0.12] rim [0.977, 0.248, 0.242, 0.114, 0.191]
  - track 32 at frame 42: holes 0, rim-vs-core 0.21, rim-vs-outside 1.10, heterogeneity 0.25; core [1.0, 0.341, 0.344, 0.13, 0.094] rim [0.945, 0.461, 0.441, 0.181, 0.208]
  - track 34 at frame 55: holes 0, rim-vs-core 0.15, rim-vs-outside 1.04, heterogeneity 0.25; core [1.0, 0.402, 0.407, 0.142, 0.084] rim [0.964, 0.35, 0.339, 0.147, 0.199]
  - track 24 at frame 17: holes 0, rim-vs-core 0.15, rim-vs-outside 1.15, heterogeneity 0.10; core [1.0, 0.56, 0.566, 0.122, 0.092] rim [0.921, 0.577, 0.538, 0.251, 0.079]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 10 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial phi (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.966, rim/outside 11.4 (aggregate of 10 individuals; 0/10 membrane-like individually; rim level 0.966)
  - radial rho (polarity, inside): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.73, rim/outside 8.19 (aggregate of 10 individuals; 8/10 membrane-like individually; rim level 0.445)  MEMBRANE-LIKE
  - radial s (layer species): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 2.08, rim/outside 6.15 (aggregate of 10 individuals; 6/10 membrane-like individually; rim level 0.279)  MEMBRANE-LIKE
  - radial c (cargo): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.48, rim/outside 2.32 (aggregate of 10 individuals; 7/10 membrane-like individually; rim level 0.167)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): rho (polarity, inside), s (layer species)
- membrane-like channels per top track at mid-life: #35 (t=23.6, R_eq 74.56): ['rho (polarity, inside)', 'c (cargo)']; #32 (t=8.4, R_eq 51.49): ['rho (polarity, inside)', 's (layer species)', 'c (cargo)']; #34 (t=11, R_eq 51.85): ['rho (polarity, inside)', 's (layer species)', 'c (cargo)']; #24 (t=3.4, R_eq 34.23): ['s (layer species)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: for 4 of 10 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
