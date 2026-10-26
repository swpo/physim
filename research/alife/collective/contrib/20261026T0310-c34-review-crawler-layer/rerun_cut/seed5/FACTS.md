# Evidence pack: wavepin-crawler-layer-cargo-rho (seed 5)

- world: `../../../20261026T0243-c31-crawler-layer-repair-claim/world.py`, family `crawler-phase-field`
- parent: None; mutation: self-made adsorbed layer s (made by the bound polarity protein, kp*phi*rho; Langmuir adsorption) that excludes a cargo c (kappa); Camley et al. 2017 crawler at low contractility rho*=0.2 with weak noise eta=2 on rho; optional sector cut at cut_t (WORLD_P) and linear-kinetics twin (KIN=1)
- run: 101 frames x 200 steps x dt 0.001 = time 20; grid [256, 256]; wall 566s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0243-c31-crawler-layer-repair-claim/world.py --out collective/contrib/20261026T0310-c34-review-crawler-layer/rerun_cut/seed5 --seeds 5 --frames 100 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 1, mean 1.0, max 1; occupancy final 0.05
- tracks: 1; persistent (alive >= 50% of run): 1; longest 101 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 2.48 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 5.48/time; max body lengths 1.6
- replication (lineage window K = 20 frames = time 4, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [-0.4007, -0.5771, -0.5761, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 50: holes 0, rim-vs-core 0.11, rim-vs-outside 1.25, heterogeneity 0.14; core [1.0, 0.636, 0.642, 0.163, 0.366] rim [0.937, 0.632, 0.598, 0.239, 0.397]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 6 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial phi (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 101 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 1)
  - radial rho (polarity, inside): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.4, rim/outside 53.6 (aggregate of 6 individuals; 2/6 membrane-like individually; rim level 0.526)
  - radial s (layer species): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 1.9, rim/outside 15.9 (aggregate of 6 individuals; 6/6 membrane-like individually; rim level 0.338)  MEMBRANE-LIKE
  - radial c (cargo): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.63, rim/outside 9.04 (aggregate of 6 individuals; 5/6 membrane-like individually; rim level 0.382)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s (layer species), c (cargo)
- membrane-like channels per top track at mid-life: #0 (t=10, R_eq 37.39): ['s (layer species)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
