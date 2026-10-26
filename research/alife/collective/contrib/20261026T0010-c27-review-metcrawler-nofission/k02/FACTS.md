# Evidence pack: wavepin-crawler-met (seed 3)

- world: `../world.py`, family `crawler-phase-field`
- parent: None; mutation: Camley et al. 2017 crawler at low contractility rho*=0.2 with weak noise eta=2 on rho; optional sector cut at cut_t (WORLD_P) and linear-kinetics twin (KIN=1)
- run: 301 frames x 200 steps x dt 0.001 = time 60; grid [300, 300]; wall 1215s; status ok
- command: `python -m labkit.run collective/contrib/wip-c27o/world.py --out collective/contrib/wip-c27o/k02 --seeds 3 --frames 300 --size 300 300 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 1, mean 1.0, max 1; occupancy final 0.19
- tracks: 1; persistent (alive >= 50% of run): 1; longest 301 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 3.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 22.2/time; max body lengths 11.4
- replication (lineage window K = 20 frames = time 4, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [1.9881, 0.1072, 0.1072, -0.1662]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 151: holes 0, rim-vs-core 0.22, rim-vs-outside 1.07, heterogeneity 0.21; core [1.0, 0.233, 0.234, 0.113] rim [0.958, 0.392, 0.378, 0.062]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 6 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial phi (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 101 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 1)
  - radial rho (polarity, inside): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 4.92, rim/outside 37.4 (aggregate of 6 individuals; 6/6 membrane-like individually; rim level 0.364)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): rho (polarity, inside)
- membrane-like channels per top track at mid-life: #0 (t=30.2, R_eq 68.29): ['rho (polarity, inside)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
