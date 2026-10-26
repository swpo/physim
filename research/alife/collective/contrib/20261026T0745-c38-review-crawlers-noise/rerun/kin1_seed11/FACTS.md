# Evidence pack: wavepin-crawler-layer-noise (seed 11)

- world: `../../../20261026T0406-c31-crawlers-from-noise-claim/world.py`, family `crawler-phase-field`
- parent: None; mutation: self-made adsorbed layer s (made by the bound polarity protein, kp*phi*rho; Langmuir adsorption) that excludes a cargo c (kappa); Camley et al. 2017 crawler at low contractility rho*=0.2 with weak noise eta=2 on rho; optional sector cut at cut_t (WORLD_P) and linear-kinetics twin (KIN=1)
- run: 81 frames x 200 steps x dt 0.001 = time 16; grid [256, 256]; wall 647s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0406-c31-crawlers-from-noise-claim/world.py --out collective/contrib/20261026T0745-c38-review-crawlers-noise/rerun/kin1_seed11 --seeds 11 --frames 80 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 0, mean 1.4, max 36; occupancy final 0.00
- tracks: 36; persistent (alive >= 50% of run): 0; longest 27 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.0
- replication (lineage window K = 20 frames = time 4, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [-1.0, -1.0, -1.0, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 11 at frame 13: holes 0, rim-vs-core 0.18, rim-vs-outside 1.50, heterogeneity 0.16; core [1.0, 0.853, 0.878, 0.26, 0.69] rim [0.937, 0.85, 0.821, 0.391, 0.594]
  - track 16 at frame 12: holes 0, rim-vs-core 0.23, rim-vs-outside 1.45, heterogeneity 0.15; core [1.0, 0.847, 0.871, 0.266, 0.625] rim [0.902, 0.85, 0.79, 0.435, 0.527]
  - track 0 at frame 8: holes 0, rim-vs-core 0.18, rim-vs-outside 1.42, heterogeneity 0.14; core [1.0, 0.861, 0.884, 0.199, 0.418] rim [0.927, 0.86, 0.822, 0.346, 0.361]
  - track 12 at frame 2: holes 0, rim-vs-core 0.23, rim-vs-outside 1.31, heterogeneity 0.11; core [0.999, 0.866, 0.889, 0.076, 0.102] rim [0.862, 0.864, 0.769, 0.221, 0.08]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 3 components >= 12 px at frames [13]):
  - radial phi (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 101 (aggregate of 3 individuals; 0/3 membrane-like individually; rim level 1)
  - radial rho (polarity, inside): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.992, rim/outside 86.8 (aggregate of 3 individuals; 0/3 membrane-like individually; rim level 0.858)
  - radial s (layer species): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 2.61, rim/outside 17.6 (aggregate of 3 individuals; 3/3 membrane-like individually; rim level 0.837)  MEMBRANE-LIKE
  - radial c (cargo): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.33, rim/outside 14.7 (aggregate of 3 individuals; 0/3 membrane-like individually; rim level 0.882)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s (layer species)
- membrane-like channels per top track at mid-life: #11 (t=2.6, R_eq 28.11): ['s (layer species)']; #16 (t=2.4, R_eq 27.63): ['s (layer species)']; #0 (t=1.6, R_eq 25.49): ['s (layer species)']; #12 (t=0.4, R_eq 18.46): ['s (layer species)']

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
