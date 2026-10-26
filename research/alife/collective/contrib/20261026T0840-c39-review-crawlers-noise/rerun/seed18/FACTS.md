# Evidence pack: wavepin-crawler-layer-noise (seed 18)

- world: `../../../20261026T0406-c31-crawlers-from-noise-claim/world.py`, family `crawler-phase-field`
- parent: None; mutation: self-made adsorbed layer s (made by the bound polarity protein, kp*phi*rho; Langmuir adsorption) that excludes a cargo c (kappa); Camley et al. 2017 crawler at low contractility rho*=0.2 with weak noise eta=2 on rho; optional sector cut at cut_t (WORLD_P) and linear-kinetics twin (KIN=1)
- run: 81 frames x 200 steps x dt 0.001 = time 16; grid [256, 256]; wall 498s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0406-c31-crawlers-from-noise-claim/world.py --out collective/contrib/c39-rev-crawl-wip/rerun/seed18 --seeds 18 --frames 80 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 3, mean 4.4, max 35; occupancy final 0.28
- tracks: 43; persistent (alive >= 50% of run): 3; longest 81 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 1.44 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [3, 3, 3], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 24.5/time; max body lengths 2.4
- replication (lineage window K = 20 frames = time 4, default): splits 1, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 6, merge/split ratio 6, nucleations 0
- channel total drift (end/start - 1): [-0.0808, -0.6062, -0.5614, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 12 at frame 40: holes 0, rim-vs-core 0.19, rim-vs-outside 1.18, heterogeneity 0.11; core [1.0, 0.611, 0.62, 0.105, 0.313] rim [0.913, 0.615, 0.57, 0.253, 0.258]
  - track 38 at frame 42: holes 0, rim-vs-core 0.19, rim-vs-outside 1.15, heterogeneity 0.11; core [1.0, 0.582, 0.59, 0.109, 0.324] rim [0.913, 0.582, 0.538, 0.255, 0.27]
  - track 42 at frame 53: holes 0, rim-vs-core 0.11, rim-vs-outside 1.03, heterogeneity 0.24; core [1.0, 0.373, 0.378, 0.112, 0.171] rim [0.974, 0.31, 0.304, 0.124, 0.226]
  - track 37 at frame 13: holes 0, rim-vs-core 0.19, rim-vs-outside 1.17, heterogeneity 0.10; core [1.0, 0.65, 0.659, 0.085, 0.118] rim [0.902, 0.66, 0.603, 0.237, 0.092]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 21 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial phi (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 13.6 (aggregate of 21 individuals; 0/21 membrane-like individually; rim level 1)
  - radial rho (polarity, inside): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.12, rim/outside 11.5 (aggregate of 21 individuals; 5/21 membrane-like individually; rim level 0.559)
  - radial s (layer species): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 2.9, rim/outside 7.97 (aggregate of 21 individuals; 18/21 membrane-like individually; rim level 0.384)  MEMBRANE-LIKE
  - radial c (cargo): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.31, rim/outside 4.89 (aggregate of 21 individuals; 2/21 membrane-like individually; rim level 0.294)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s (layer species)
- membrane-like channels per top track at mid-life: #12 (t=8, R_eq 30.73): ['s (layer species)']; #38 (t=8.4, R_eq 32.96): ['s (layer species)']; #42 (t=10.6, R_eq 61.51): ['rho (polarity, inside)']; #37 (t=2.6, R_eq 27.82): ['s (layer species)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
