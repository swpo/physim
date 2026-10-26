# Evidence pack: wavepin-crawler-layer-noise (seed 3)

- world: `../world.py`, family `crawler-phase-field`
- parent: None; mutation: self-made adsorbed layer s (made by the bound polarity protein, kp*phi*rho; Langmuir adsorption) that excludes a cargo c (kappa); Camley et al. 2017 crawler at low contractility rho*=0.2 with weak noise eta=2 on rho; optional sector cut at cut_t (WORLD_P) and linear-kinetics twin (KIN=1)
- run: 81 frames x 200 steps x dt 0.001 = time 16; grid [256, 256]; wall 371s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0412-c32-review-crawl-noise/world.py --out collective/contrib/20261026T0412-c32-review-crawl-noise/pack --seeds 3 --frames 80 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 1, mean 2.9, max 30; occupancy final 0.28
- tracks: 36; persistent (alive >= 50% of run): 1; longest 46 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.48 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 31.1/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 4, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 6, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [-0.0821, -0.7403, -0.7139, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 23: holes 0, rim-vs-core 0.16, rim-vs-outside 1.12, heterogeneity 0.10; core [1.0, 0.544, 0.559, 0.116, 0.195] rim [0.921, 0.547, 0.517, 0.245, 0.169]
  - track 35 at frame 63: holes 0, rim-vs-core 0.47, rim-vs-outside 1.08, heterogeneity 0.22; core [1.0, 0.054, 0.055, 0.086, 0.257] rim [0.976, 0.381, 0.383, 0.141, 0.23]
  - track 4 at frame 13: holes 0, rim-vs-core 0.49, rim-vs-outside 1.33, heterogeneity 0.11; core [0.994, 1.0, 1.0, 0.055, 0.113] rim [0.791, 1.0, 0.887, 0.485, 0.035]
  - track 30 at frame 13: holes 0, rim-vs-core 0.09, rim-vs-outside 1.26, heterogeneity 0.10; core [1.0, 0.667, 0.685, 0.116, 0.101] rim [0.945, 0.664, 0.645, 0.172, 0.091]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 12 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial phi (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.955, rim/outside 13.2 (aggregate of 12 individuals; 0/12 membrane-like individually; rim level 0.955)
  - radial rho (polarity, inside): peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.05, rim/outside 10.2 (aggregate of 12 individuals; 4/12 membrane-like individually; rim level 0.488)
  - radial s (layer species): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 2.31, rim/outside 7.24 (aggregate of 12 individuals; 6/12 membrane-like individually; rim level 0.317)  MEMBRANE-LIKE
  - radial c (cargo): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.07, rim/outside 3.51 (aggregate of 12 individuals; 1/12 membrane-like individually; rim level 0.166)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s (layer species)
- membrane-like channels per top track at mid-life: #1 (t=4.6, R_eq 33.29): ['s (layer species)']; #35 (t=12.6, R_eq 76.42): ['rho (polarity, inside)']; #4 (t=2.6, R_eq 13): ['s (layer species)']; #30 (t=2.6, R_eq 34.83): ['s (layer species)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: for 3 of 12 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
