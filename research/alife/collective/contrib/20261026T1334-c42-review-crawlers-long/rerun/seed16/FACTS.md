# Evidence pack: wavepin-crawler-layer-noise (seed 16)

- world: `../../../20261026T1042-c39-crawlers-noise-long-claim/world.py`, family `crawler-phase-field`
- parent: None; mutation: self-made adsorbed layer s (made by the bound polarity protein, kp*phi*rho; Langmuir adsorption) that excludes a cargo c (kappa); Camley et al. 2017 crawler at low contractility rho*=0.2 with weak noise eta=2 on rho; optional sector cut at cut_t (WORLD_P) and linear-kinetics twin (KIN=1)
- run: 161 frames x 200 steps x dt 0.001 = time 32; grid [256, 256]; wall 1040s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1042-c39-crawlers-noise-long-claim/world.py --out collective/contrib/20261026T1334-c42-review-crawlers-long/rerun/seed16 --seeds 16 --frames 160 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 1, mean 2.6, max 30; occupancy final 0.22
- tracks: 34; persistent (alive >= 50% of run): 1; longest 84 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.29 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 24.4/time; max body lengths 3.0
- replication (lineage window K = 20 frames = time 4, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 4, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [-0.2691, -0.7736, -0.7521, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 24 at frame 42: holes 0, rim-vs-core 0.36, rim-vs-outside 1.21, heterogeneity 0.13; core [1.0, 0.765, 0.781, 0.092, 0.247] rim [0.862, 0.76, 0.67, 0.388, 0.139]
  - track 25 at frame 40: holes 0, rim-vs-core 0.44, rim-vs-outside 1.38, heterogeneity 0.13; core [0.998, 0.989, 0.994, 0.076, 0.234] rim [0.841, 0.985, 0.866, 0.444, 0.102]
  - track 33 at frame 122: holes 0, rim-vs-core 0.10, rim-vs-outside 1.02, heterogeneity 0.22; core [1.0, 0.27, 0.276, 0.128, 0.115] rim [0.975, 0.283, 0.28, 0.128, 0.21]
  - track 32 at frame 52: holes 0, rim-vs-core 0.14, rim-vs-outside 1.02, heterogeneity 0.23; core [1.0, 0.37, 0.378, 0.127, 0.126] rim [0.969, 0.292, 0.286, 0.144, 0.188]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 11 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial phi (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.998, rim/outside 33.5 (aggregate of 11 individuals; 0/11 membrane-like individually; rim level 0.998)
  - radial rho (polarity, inside): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.35, rim/outside 22.5 (aggregate of 11 individuals; 6/11 membrane-like individually; rim level 0.579)
  - radial s (layer species): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 3.2, rim/outside 12.1 (aggregate of 11 individuals; 5/11 membrane-like individually; rim level 0.42)  MEMBRANE-LIKE
  - radial c (cargo): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.2, rim/outside 3.01 (aggregate of 11 individuals; 4/11 membrane-like individually; rim level 0.208)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s (layer species)
- membrane-like channels per top track at mid-life: #24 (t=8.4, R_eq 21.5): ['s (layer species)']; #25 (t=8, R_eq 14.83): ['s (layer species)']; #33 (t=24.4, R_eq 68.59): ['rho (polarity, inside)', 'c (cargo)']; #32 (t=10.4, R_eq 61.79): ['rho (polarity, inside)', 'c (cargo)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
