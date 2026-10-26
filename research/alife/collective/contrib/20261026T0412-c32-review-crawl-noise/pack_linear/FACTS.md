# Evidence pack: wavepin-crawler-layer-noise (seed 3)

- world: `../world.py`, family `crawler-phase-field`
- parent: None; mutation: self-made adsorbed layer s (made by the bound polarity protein, kp*phi*rho; Langmuir adsorption) that excludes a cargo c (kappa); Camley et al. 2017 crawler at low contractility rho*=0.2 with weak noise eta=2 on rho; optional sector cut at cut_t (WORLD_P) and linear-kinetics twin (KIN=1)
- run: 81 frames x 200 steps x dt 0.001 = time 16; grid [256, 256]; wall 344s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0412-c32-review-crawl-noise/world.py --out collective/contrib/20261026T0412-c32-review-crawl-noise/pack_linear --seeds 3 --frames 80 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 0, mean 1.5, max 30; occupancy final 0.00
- tracks: 30; persistent (alive >= 50% of run): 0; longest 27 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [0, 0, 0], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.1
- replication (lineage window K = 20 frames = time 4, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [-1.0, -1.0, -1.0, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 18 at frame 13: holes 0, rim-vs-core 0.25, rim-vs-outside 1.45, heterogeneity 0.16; core [1.0, 0.844, 0.872, 0.242, 0.639] rim [0.899, 0.852, 0.794, 0.423, 0.532]
  - track 0 at frame 13: holes 0, rim-vs-core 0.18, rim-vs-outside 1.50, heterogeneity 0.16; core [1.0, 0.862, 0.889, 0.233, 0.65] rim [0.935, 0.852, 0.823, 0.364, 0.572]
  - track 15 at frame 7: holes 0, rim-vs-core 0.28, rim-vs-outside 1.36, heterogeneity 0.14; core [1.0, 0.857, 0.885, 0.163, 0.343] rim [0.882, 0.852, 0.778, 0.385, 0.286]
  - track 1 at frame 6: holes 0, rim-vs-core 0.25, rim-vs-outside 1.37, heterogeneity 0.13; core [1.0, 0.848, 0.875, 0.156, 0.303] rim [0.885, 0.864, 0.792, 0.36, 0.252]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 3 components >= 12 px at frames [13]):
  - radial phi (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.998, rim/outside 101 (aggregate of 3 individuals; 0/3 membrane-like individually; rim level 0.998)
  - radial rho (polarity, inside): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.01, rim/outside 87 (aggregate of 3 individuals; 0/3 membrane-like individually; rim level 0.86)
  - radial s (layer species): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 3.15, rim/outside 12.4 (aggregate of 3 individuals; 3/3 membrane-like individually; rim level 0.827)  MEMBRANE-LIKE
  - radial c (cargo): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.16, rim/outside 11.8 (aggregate of 3 individuals; 0/3 membrane-like individually; rim level 0.825)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s (layer species)
- membrane-like channels per top track at mid-life: #18 (t=2.6, R_eq 28.2): ['s (layer species)']; #0 (t=2.6, R_eq 27.78): ['s (layer species)']; #15 (t=1.4, R_eq 24.46): ['s (layer species)']; #1 (t=1.2, R_eq 23.76): ['s (layer species)']

## Warnings
- no components at the end: matter died out or fell below threshold
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
