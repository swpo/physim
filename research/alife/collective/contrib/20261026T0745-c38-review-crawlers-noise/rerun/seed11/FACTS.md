# Evidence pack: wavepin-crawler-layer-noise (seed 11)

- world: `../../../20261026T0406-c31-crawlers-from-noise-claim/world.py`, family `crawler-phase-field`
- parent: None; mutation: self-made adsorbed layer s (made by the bound polarity protein, kp*phi*rho; Langmuir adsorption) that excludes a cargo c (kappa); Camley et al. 2017 crawler at low contractility rho*=0.2 with weak noise eta=2 on rho; optional sector cut at cut_t (WORLD_P) and linear-kinetics twin (KIN=1)
- run: 81 frames x 200 steps x dt 0.001 = time 16; grid [256, 256]; wall 684s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0406-c31-crawlers-from-noise-claim/world.py --out collective/contrib/20261026T0745-c38-review-crawlers-noise/rerun/seed11 --seeds 11 --frames 80 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 3, mean 4.5, max 36; occupancy final 0.15
- tracks: 36; persistent (alive >= 50% of run): 3; longest 81 frames; alive start-to-end: 3
- size of persistent tracks: max/min area ratio 1.83 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [3, 3, 3], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 17.2/time; max body lengths 4.2
- replication (lineage window K = 20 frames = time 4, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [-0.5037, -0.7225, -0.6933, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 40: holes 0, rim-vs-core 0.21, rim-vs-outside 1.12, heterogeneity 0.26; core [1.0, 0.434, 0.449, 0.102, 0.174] rim [0.921, 0.525, 0.5, 0.229, 0.268]
  - track 1 at frame 40: holes 0, rim-vs-core 0.33, rim-vs-outside 1.33, heterogeneity 0.14; core [0.999, 0.884, 0.912, 0.075, 0.252] rim [0.872, 0.884, 0.798, 0.343, 0.148]
  - track 11 at frame 40: holes 0, rim-vs-core 0.18, rim-vs-outside 1.10, heterogeneity 0.26; core [1.0, 0.445, 0.46, 0.111, 0.135] rim [0.929, 0.476, 0.457, 0.207, 0.271]
  - track 29 at frame 15: holes 0, rim-vs-core 0.50, rim-vs-outside 1.30, heterogeneity 0.12; core [0.994, 0.992, 0.996, 0.058, 0.113] rim [0.794, 0.991, 0.845, 0.482, 0.034]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 22 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial phi (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.999, rim/outside 22.4 (aggregate of 22 individuals; 0/22 membrane-like individually; rim level 0.999)
  - radial rho (polarity, inside): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.11, rim/outside 17.3 (aggregate of 22 individuals; 4/22 membrane-like individually; rim level 0.636)
  - radial s (layer species): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 4.05, rim/outside 10.4 (aggregate of 22 individuals; 22/22 membrane-like individually; rim level 0.461)  MEMBRANE-LIKE
  - radial c (cargo): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.74, rim/outside 6.59 (aggregate of 22 individuals; 12/22 membrane-like individually; rim level 0.263)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s (layer species), c (cargo)
- membrane-like channels per top track at mid-life: #0 (t=8, R_eq 34.53): ['rho (polarity, inside)', 's (layer species)', 'c (cargo)']; #1 (t=8, R_eq 17.19): ['s (layer species)']; #11 (t=8, R_eq 40.57): ['s (layer species)', 'c (cargo)']; #29 (t=3, R_eq 13.98): ['s (layer species)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
