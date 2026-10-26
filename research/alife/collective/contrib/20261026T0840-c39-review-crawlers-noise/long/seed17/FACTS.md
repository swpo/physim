# Evidence pack: wavepin-crawler-layer-noise (seed 17)

- world: `../../../20261026T0406-c31-crawlers-from-noise-claim/world.py`, family `crawler-phase-field`
- parent: None; mutation: self-made adsorbed layer s (made by the bound polarity protein, kp*phi*rho; Langmuir adsorption) that excludes a cargo c (kappa); Camley et al. 2017 crawler at low contractility rho*=0.2 with weak noise eta=2 on rho; optional sector cut at cut_t (WORLD_P) and linear-kinetics twin (KIN=1)
- run: 161 frames x 200 steps x dt 0.001 = time 32; grid [256, 256]; wall 997s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0406-c31-crawlers-from-noise-claim/world.py --out collective/contrib/c39-rev-crawl-wip/long/seed17 --seeds 17 --frames 160 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 1, mean 1.6, max 30; occupancy final 0.28
- tracks: 37; persistent (alive >= 50% of run): 1; longest 142 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.08 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 25.9/time; max body lengths 5.4
- replication (lineage window K = 20 frames = time 4, default): splits 1, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 6, merge/split ratio 6, nucleations 0
- channel total drift (end/start - 1): [-0.071, -0.7457, -0.7219, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 36 at frame 90: holes 0, rim-vs-core 0.25, rim-vs-outside 1.06, heterogeneity 0.22; core [1.0, 0.198, 0.199, 0.124, 0.166] rim [0.963, 0.359, 0.349, 0.136, 0.273]
  - track 26 at frame 9: holes 0, rim-vs-core 0.19, rim-vs-outside 1.18, heterogeneity 0.10; core [1.0, 0.655, 0.661, 0.095, 0.07] rim [0.9, 0.662, 0.601, 0.25, 0.055]
  - track 3 at frame 9: holes 0, rim-vs-core 0.21, rim-vs-outside 1.30, heterogeneity 0.11; core [0.999, 0.813, 0.819, 0.072, 0.072] rim [0.911, 0.811, 0.745, 0.24, 0.054]
  - track 24 at frame 4: holes 0, rim-vs-core 0.35, rim-vs-outside 1.33, heterogeneity 0.09; core [0.994, 1.0, 1.0, 0.032, 0.03] rim [0.792, 1.0, 0.91, 0.298, 0.014]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 6 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial phi (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.93, rim/outside 62.1 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.928)
  - radial rho (polarity, inside): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 5.05, rim/outside 31.8 (aggregate of 6 individuals; 6/6 membrane-like individually; rim level 0.317)  MEMBRANE-LIKE
  - radial s (layer species): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.15, rim/outside 8.61 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.144)
  - radial c (cargo): peak at rho=1.15 (in the peak band 0.5-1.5), rim/core 1.5, rim/outside 2 (aggregate of 6 individuals; 4/6 membrane-like individually; rim level 0.243)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): rho (polarity, inside)
- membrane-like channels per top track at mid-life: #36 (t=18, R_eq 76.82): ['rho (polarity, inside)', 'c (cargo)']; #26 (t=1.8, R_eq 28.29): ['s (layer species)']; #3 (t=1.8, R_eq 21): ['s (layer species)']; #24 (t=0.8, R_eq 12.53): ['s (layer species)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: for 6 of 6 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
