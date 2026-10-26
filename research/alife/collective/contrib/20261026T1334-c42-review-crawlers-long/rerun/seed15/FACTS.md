# Evidence pack: wavepin-crawler-layer-noise (seed 15)

- world: `../../../20261026T1042-c39-crawlers-noise-long-claim/world.py`, family `crawler-phase-field`
- parent: None; mutation: self-made adsorbed layer s (made by the bound polarity protein, kp*phi*rho; Langmuir adsorption) that excludes a cargo c (kappa); Camley et al. 2017 crawler at low contractility rho*=0.2 with weak noise eta=2 on rho; optional sector cut at cut_t (WORLD_P) and linear-kinetics twin (KIN=1)
- run: 161 frames x 200 steps x dt 0.001 = time 32; grid [256, 256]; wall 1040s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1042-c39-crawlers-noise-long-claim/world.py --out collective/contrib/20261026T1334-c42-review-crawlers-long/rerun/seed15 --seeds 15 --frames 160 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 1, mean 2.5, max 23; occupancy final 0.16
- tracks: 26; persistent (alive >= 50% of run): 2; longest 95 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 126.87 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 18.7/time; max body lengths 5.4
- replication (lineage window K = 20 frames = time 4, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 3, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [-0.4866, -0.8092, -0.7915, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 23 at frame 48: holes 0, rim-vs-core 0.19, rim-vs-outside 1.14, heterogeneity 0.26; core [1.0, 0.497, 0.502, 0.101, 0.158] rim [0.921, 0.556, 0.518, 0.215, 0.266]
  - track 17 at frame 40: holes 0, rim-vs-core 0.19, rim-vs-outside 1.24, heterogeneity 0.12; core [1.0, 0.712, 0.719, 0.098, 0.257] rim [0.924, 0.701, 0.655, 0.25, 0.2]
  - track 24 at frame 56: holes 0, rim-vs-core 0.45, rim-vs-outside 1.07, heterogeneity 0.28; core [1.0, 0.71, 0.716, 0.129, 0.119] rim [0.956, 0.426, 0.407, 0.17, 0.275]
  - track 25 at frame 129: holes 0, rim-vs-core 0.22, rim-vs-outside 1.09, heterogeneity 0.24; core [1.0, 0.567, 0.573, 0.137, 0.151] rim [0.963, 0.429, 0.418, 0.137, 0.203]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 12 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial phi (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.975, rim/outside 11.9 (aggregate of 12 individuals; 0/12 membrane-like individually; rim level 0.972)
  - radial rho (polarity, inside): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.39, rim/outside 9.69 (aggregate of 12 individuals; 7/12 membrane-like individually; rim level 0.447)
  - radial s (layer species): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 2.55, rim/outside 5.22 (aggregate of 12 individuals; 10/12 membrane-like individually; rim level 0.371)  MEMBRANE-LIKE
  - radial c (cargo): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.55, rim/outside 3.96 (aggregate of 12 individuals; 7/12 membrane-like individually; rim level 0.301)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s (layer species), c (cargo)
- membrane-like channels per top track at mid-life: #23 (t=9.6, R_eq 35.21): ['s (layer species)', 'c (cargo)']; #17 (t=8, R_eq 24.99): ['s (layer species)']; #24 (t=11.2, R_eq 39.71): ['s (layer species)', 'c (cargo)']; #25 (t=25.8, R_eq 56.61): ['rho (polarity, inside)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
