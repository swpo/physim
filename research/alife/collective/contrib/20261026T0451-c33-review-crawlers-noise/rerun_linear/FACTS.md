# Evidence pack: wavepin-crawler-layer-noise (seed 7)

- world: `../../20261026T0406-c31-crawlers-from-noise-claim/world.py`, family `crawler-phase-field`
- parent: None; mutation: self-made adsorbed layer s (made by the bound polarity protein, kp*phi*rho; Langmuir adsorption) that excludes a cargo c (kappa); Camley et al. 2017 crawler at low contractility rho*=0.2 with weak noise eta=2 on rho; optional sector cut at cut_t (WORLD_P) and linear-kinetics twin (KIN=1)
- run: 81 frames x 200 steps x dt 0.001 = time 16; grid [256, 256]; wall 498s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0406-c31-crawlers-from-noise-claim/world.py --out collective/contrib/wip-c33-cn/rerun_linear --seeds 7 --frames 80 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 0, mean 1.2, max 29; occupancy final 0.00
- tracks: 29; persistent (alive >= 50% of run): 0; longest 39 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.2
- replication (lineage window K = 20 frames = time 4, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [-1.0, -1.0, -1.0, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 19: holes 0, rim-vs-core 0.11, rim-vs-outside 1.56, heterogeneity 0.15; core [1.0, 0.861, 0.889, 0.474, 0.75] rim [0.942, 0.864, 0.841, 0.518, 0.677]
  - track 14 at frame 3: holes 0, rim-vs-core 0.38, rim-vs-outside 1.27, heterogeneity 0.13; core [0.998, 0.861, 0.887, 0.118, 0.118] rim [0.836, 0.885, 0.769, 0.436, 0.093]
  - track 6 at frame 2: holes 0, rim-vs-core 0.26, rim-vs-outside 1.31, heterogeneity 0.12; core [0.999, 0.858, 0.886, 0.107, 0.078] rim [0.866, 0.865, 0.776, 0.294, 0.062]
  - track 10 at frame 2: holes 0, rim-vs-core 0.33, rim-vs-outside 1.26, heterogeneity 0.12; core [0.998, 0.866, 0.892, 0.097, 0.079] rim [0.836, 0.869, 0.754, 0.351, 0.06]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 2 components >= 12 px at frames [13, 27]):
  - radial phi (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 101 (aggregate of 2 individuals; 0/2 membrane-like individually; rim level 1)
  - radial rho (polarity, inside): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.996, rim/outside 87.7 (aggregate of 2 individuals; 0/2 membrane-like individually; rim level 0.867)
  - radial s (layer species): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 1.52, rim/outside 13.2 (aggregate of 2 individuals; 1/2 membrane-like individually; rim level 0.855)  MEMBRANE-LIKE
  - radial c (cargo): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.12, rim/outside 14.4 (aggregate of 2 individuals; 0/2 membrane-like individually; rim level 0.809)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s (layer species)
- membrane-like channels per top track at mid-life: #0 (t=3.8, R_eq 29.62): none; #14 (t=0.6, R_eq 17.91): ['s (layer species)']; #6 (t=0.4, R_eq 18.71): ['s (layer species)']; #10 (t=0.4, R_eq 17.68): ['s (layer species)']

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
