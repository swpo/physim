# Evidence pack: wavepin-crawler-layer-noise (seed 0)

- world: `../../world.py`, family `crawler-phase-field`
- parent: None; mutation: self-made adsorbed layer s (made by the bound polarity protein, kp*phi*rho; Langmuir adsorption) that excludes a cargo c (kappa); Camley et al. 2017 crawler at low contractility rho*=0.2 with weak noise eta=2 on rho; optional sector cut at cut_t (WORLD_P) and linear-kinetics twin (KIN=1)
- run: 161 frames x 200 steps x dt 0.001 = time 32; grid [256, 256]; wall 1014s; status ok
- command: `python -m labkit.run collective/contrib/c39-crawl-long-wip/world.py --out collective/contrib/c39-crawl-long-wip/pack/seed0 --seeds 0 --frames 160 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 1, mean 2.4, max 30; occupancy final 0.22
- tracks: 36; persistent (alive >= 50% of run): 1; longest 118 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.14 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 24.4/time; max body lengths 4.7
- replication (lineage window K = 20 frames = time 4, default): splits 1, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 4, merge/split ratio 4, nucleations 0
- channel total drift (end/start - 1): [-0.2762, -0.7791, -0.7578, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 35 at frame 102: holes 0, rim-vs-core 0.10, rim-vs-outside 1.02, heterogeneity 0.23; core [1.0, 0.295, 0.298, 0.133, 0.153] rim [0.97, 0.293, 0.284, 0.122, 0.249]
  - track 23 at frame 22: holes 0, rim-vs-core 0.23, rim-vs-outside 1.19, heterogeneity 0.11; core [1.0, 0.672, 0.68, 0.106, 0.153] rim [0.899, 0.674, 0.613, 0.299, 0.115]
  - track 6 at frame 20: holes 0, rim-vs-core 0.44, rim-vs-outside 1.32, heterogeneity 0.13; core [0.998, 0.938, 0.945, 0.078, 0.141] rim [0.835, 0.936, 0.794, 0.445, 0.063]
  - track 30 at frame 15: holes 0, rim-vs-core 0.27, rim-vs-outside 1.17, heterogeneity 0.11; core [1.0, 0.693, 0.701, 0.094, 0.107] rim [0.882, 0.689, 0.615, 0.317, 0.074]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 9 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial phi (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.978, rim/outside 25.8 (aggregate of 9 individuals; 0/9 membrane-like individually; rim level 0.978)
  - radial rho (polarity, inside): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.59, rim/outside 15.3 (aggregate of 9 individuals; 6/9 membrane-like individually; rim level 0.481)  MEMBRANE-LIKE
  - radial s (layer species): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 2.33, rim/outside 10.2 (aggregate of 9 individuals; 4/9 membrane-like individually; rim level 0.316)  MEMBRANE-LIKE
  - radial c (cargo): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.21, rim/outside 3.05 (aggregate of 9 individuals; 5/9 membrane-like individually; rim level 0.183)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): rho (polarity, inside), s (layer species)
- membrane-like channels per top track at mid-life: #35 (t=20.4, R_eq 67.89): ['rho (polarity, inside)', 'c (cargo)']; #23 (t=4.4, R_eq 26.8): ['s (layer species)']; #6 (t=4, R_eq 17.06): ['s (layer species)']; #30 (t=3, R_eq 25.93): ['s (layer species)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
