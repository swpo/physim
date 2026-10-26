# Evidence pack: wavepin-crawler-layer-noise (seed 21)

- world: `../../../20261026T0406-c31-crawlers-from-noise-claim/world.py`, family `crawler-phase-field`
- parent: None; mutation: self-made adsorbed layer s (made by the bound polarity protein, kp*phi*rho; Langmuir adsorption) that excludes a cargo c (kappa); Camley et al. 2017 crawler at low contractility rho*=0.2 with weak noise eta=2 on rho; optional sector cut at cut_t (WORLD_P) and linear-kinetics twin (KIN=1)
- run: 81 frames x 200 steps x dt 0.001 = time 16; grid [256, 256]; wall 583s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0406-c31-crawlers-from-noise-claim/world.py --out collective/contrib/20261026T1140-c41-review-crawlers-noise/rerun --seeds 21 22 --frames 80 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 1, mean 3.7, max 33; occupancy final 0.25
- tracks: 39; persistent (alive >= 50% of run): 1; longest 64 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.92 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 14.5/time; max body lengths 3.1
- replication (lineage window K = 20 frames = time 4, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 6, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [-0.156, -0.7003, -0.6689, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 32: holes 0, rim-vs-core 0.14, rim-vs-outside 1.13, heterogeneity 0.24; core [1.0, 0.465, 0.479, 0.104, 0.17] rim [0.942, 0.528, 0.513, 0.196, 0.211]
  - track 0 at frame 20: holes 0, rim-vs-core 0.43, rim-vs-outside 1.35, heterogeneity 0.13; core [0.998, 0.954, 0.972, 0.069, 0.147] rim [0.833, 0.959, 0.828, 0.429, 0.064]
  - track 8 at frame 14: holes 0, rim-vs-core 0.27, rim-vs-outside 1.20, heterogeneity 0.11; core [1.0, 0.716, 0.737, 0.08, 0.107] rim [0.881, 0.71, 0.646, 0.296, 0.073]
  - track 37 at frame 52: holes 0, rim-vs-core 0.29, rim-vs-outside 1.08, heterogeneity 0.22; core [1.0, 0.191, 0.197, 0.124, 0.139] rim [0.962, 0.389, 0.387, 0.154, 0.216]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 14 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial phi (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.987, rim/outside 14.6 (aggregate of 14 individuals; 0/14 membrane-like individually; rim level 0.987)
  - radial rho (polarity, inside): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.29, rim/outside 10.6 (aggregate of 14 individuals; 6/14 membrane-like individually; rim level 0.52)
  - radial s (layer species): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 2.61, rim/outside 7.86 (aggregate of 14 individuals; 9/14 membrane-like individually; rim level 0.343)  MEMBRANE-LIKE
  - radial c (cargo): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.44, rim/outside 4.03 (aggregate of 14 individuals; 5/14 membrane-like individually; rim level 0.18)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s (layer species)
- membrane-like channels per top track at mid-life: #6 (t=6.4, R_eq 33.58): ['s (layer species)', 'c (cargo)']; #0 (t=4, R_eq 15.07): ['s (layer species)']; #8 (t=2.8, R_eq 22.23): ['s (layer species)']; #37 (t=10.4, R_eq 63.13): ['rho (polarity, inside)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
