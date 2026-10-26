# Evidence pack: wavepin-crawler-layer-noise (seed 6)

- world: `../../../20261026T0406-c31-crawlers-from-noise-claim/world.py`, family `crawler-phase-field`
- parent: None; mutation: self-made adsorbed layer s (made by the bound polarity protein, kp*phi*rho; Langmuir adsorption) that excludes a cargo c (kappa); Camley et al. 2017 crawler at low contractility rho*=0.2 with weak noise eta=2 on rho; optional sector cut at cut_t (WORLD_P) and linear-kinetics twin (KIN=1)
- run: 81 frames x 200 steps x dt 0.001 = time 16; grid [256, 256]; wall 487s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0406-c31-crawlers-from-noise-claim/world.py --out collective/contrib/20261026T0620-c34-review-crawlers-noise/linear/seed6 --seeds 6 --frames 80 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 1, mean 1.7, max 22; occupancy final 0.08
- tracks: 24; persistent (alive >= 50% of run): 1; longest 81 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 1.17 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.0
- replication (lineage window K = 20 frames = time 4, default): splits 1, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [-0.7434, -0.8634, -0.8492, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 40: holes 0, rim-vs-core 0.10, rim-vs-outside 1.46, heterogeneity 0.14; core [1.0, 0.755, 0.777, 0.14, 0.616] rim [0.956, 0.759, 0.748, 0.215, 0.571]
  - track 23 at frame 5: holes 0, rim-vs-core 0.22, rim-vs-outside 1.35, heterogeneity 0.10; core [1.0, 0.885, 0.906, 0.049, 0.095] rim [0.865, 0.901, 0.806, 0.197, 0.076]
  - track 19 at frame 4: holes 0, rim-vs-core 0.19, rim-vs-outside 1.35, heterogeneity 0.10; core [1.0, 0.889, 0.91, 0.045, 0.075] rim [0.876, 0.893, 0.808, 0.15, 0.061]
  - track 4 at frame 3: holes 0, rim-vs-core 0.13, rim-vs-outside 1.40, heterogeneity 0.09; core [0.999, 0.9, 0.921, 0.037, 0.056] rim [0.911, 0.897, 0.841, 0.099, 0.048]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 6 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial phi (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 101 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 1)
  - radial rho (polarity, inside): peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 76.2 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.752)
  - radial s (layer species): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 2.19, rim/outside 20.3 (aggregate of 6 individuals; 6/6 membrane-like individually; rim level 0.401)  MEMBRANE-LIKE
  - radial c (cargo): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.34, rim/outside 17.8 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.742)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s (layer species)
- membrane-like channels per top track at mid-life: #0 (t=8, R_eq 40.32): ['s (layer species)']; #23 (t=1, R_eq 20.83): ['s (layer species)']; #19 (t=0.8, R_eq 20.73): ['s (layer species)']; #4 (t=0.6, R_eq 20.57): ['s (layer species)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
