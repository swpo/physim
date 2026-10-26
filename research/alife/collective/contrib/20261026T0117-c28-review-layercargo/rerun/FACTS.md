# Evidence pack: wavepin-crawler-layer-cargo (seed 3)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261026T0101-c31-layer-holds-cargo/world2.py`, family `crawler-phase-field`
- parent: None; mutation: self-made adsorbed layer s (kp*phi, Langmuir adsorption) that excludes a cargo c (kappa); Camley et al. 2017 crawler at low contractility rho*=0.2 with weak noise eta=2 on rho; optional sector cut at cut_t (WORLD_P) and linear-kinetics twin (KIN=1)
- run: 61 frames x 200 steps x dt 0.001 = time 12; grid [256, 256]; wall 317s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0101-c31-layer-holds-cargo/world2.py --out /tmp/claude-0/c28lc/lk --seeds 3 --frames 60 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 1, mean 1.0, max 1; occupancy final 0.11
- tracks: 1; persistent (alive >= 50% of run): 1; longest 61 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 1.19 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 21.1/time; max body lengths 3.1
- replication (lineage window K = 20 frames = time 4, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [0.159, -0.3819, -0.3816, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 30: holes 0, rim-vs-core 0.51, rim-vs-outside 1.18, heterogeneity 0.27; core [1.0, 0.159, 0.16, 0.189, 0.193] rim [0.962, 0.529, 0.514, 0.19, 0.215]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 6 components >= 12 px at frames [10, 20, 30, 40, 50, 60]):
  - radial phi (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 101 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 1)
  - radial rho (polarity, inside): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.5, rim/outside 46 (aggregate of 6 individuals; 6/6 membrane-like individually; rim level 0.45)  MEMBRANE-LIKE
  - radial s (layer species): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 1.9, rim/outside 15.8 (aggregate of 6 individuals; 6/6 membrane-like individually; rim level 0.388)  MEMBRANE-LIKE
  - radial c (cargo): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.72, rim/outside 17.3 (aggregate of 6 individuals; 5/6 membrane-like individually; rim level 0.33)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): rho (polarity, inside), s (layer species), c (cargo)
- membrane-like channels per top track at mid-life: #0 (t=6, R_eq 46.82): ['rho (polarity, inside)', 's (layer species)', 'c (cargo)']

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
