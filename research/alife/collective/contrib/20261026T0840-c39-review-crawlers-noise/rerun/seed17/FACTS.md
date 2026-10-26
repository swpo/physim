# Evidence pack: wavepin-crawler-layer-noise (seed 17)

- world: `../../../20261026T0406-c31-crawlers-from-noise-claim/world.py`, family `crawler-phase-field`
- parent: None; mutation: self-made adsorbed layer s (made by the bound polarity protein, kp*phi*rho; Langmuir adsorption) that excludes a cargo c (kappa); Camley et al. 2017 crawler at low contractility rho*=0.2 with weak noise eta=2 on rho; optional sector cut at cut_t (WORLD_P) and linear-kinetics twin (KIN=1)
- run: 81 frames x 200 steps x dt 0.001 = time 16; grid [256, 256]; wall 498s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0406-c31-crawlers-from-noise-claim/world.py --out collective/contrib/c39-rev-crawl-wip/rerun/seed17 --seeds 17 --frames 80 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 1, mean 2.1, max 30; occupancy final 0.28
- tracks: 37; persistent (alive >= 50% of run): 1; longest 62 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.07 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 28.7/time; max body lengths 2.6
- replication (lineage window K = 20 frames = time 4, default): splits 1, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 6, merge/split ratio 6, nucleations 0
- channel total drift (end/start - 1): [-0.0687, -0.7446, -0.7209, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 36 at frame 50: holes 0, rim-vs-core 0.43, rim-vs-outside 1.10, heterogeneity 0.22; core [1.0, 0.106, 0.107, 0.111, 0.224] rim [0.969, 0.413, 0.407, 0.147, 0.261]
  - track 26 at frame 9: holes 0, rim-vs-core 0.19, rim-vs-outside 1.18, heterogeneity 0.10; core [1.0, 0.649, 0.657, 0.093, 0.096] rim [0.9, 0.657, 0.598, 0.244, 0.075]
  - track 3 at frame 9: holes 0, rim-vs-core 0.20, rim-vs-outside 1.30, heterogeneity 0.11; core [0.999, 0.806, 0.814, 0.07, 0.098] rim [0.911, 0.804, 0.741, 0.235, 0.073]
  - track 24 at frame 4: holes 0, rim-vs-core 0.34, rim-vs-outside 1.33, heterogeneity 0.09; core [0.994, 1.0, 1.0, 0.031, 0.041] rim [0.792, 1.0, 0.908, 0.289, 0.019]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 8 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial phi (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.932, rim/outside 12.2 (aggregate of 8 individuals; 0/8 membrane-like individually; rim level 0.93)
  - radial rho (polarity, inside): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.49, rim/outside 8.75 (aggregate of 8 individuals; 5/8 membrane-like individually; rim level 0.414)
  - radial s (layer species): peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 1.69, rim/outside 6.27 (aggregate of 8 individuals; 2/8 membrane-like individually; rim level 0.231)  MEMBRANE-LIKE
  - radial c (cargo): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.09, rim/outside 2.63 (aggregate of 8 individuals; 0/8 membrane-like individually; rim level 0.185)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s (layer species)
- membrane-like channels per top track at mid-life: #36 (t=10, R_eq 76.68): ['rho (polarity, inside)']; #26 (t=1.8, R_eq 28.29): ['s (layer species)']; #3 (t=1.8, R_eq 21): ['s (layer species)']; #24 (t=0.8, R_eq 12.53): ['s (layer species)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: for 5 of 8 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
