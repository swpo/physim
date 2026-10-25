# Evidence pack: wavepin-crawler-r2 (seed 7)

- world: `../world.py`, family `crawler-phase-field`
- parent: None; mutation: Camley et al. 2017 crawler at low contractility rho*=0.2 with weak noise eta=2 on rho; optional sector cut at cut_t (WORLD_P) and linear-kinetics twin (KIN=1)
- run: 91 frames x 200 steps x dt 0.001 = time 18; grid [384, 384]; wall 536s; status ok
- command: `python -m labkit.run collective/contrib/wip-c27h/world.py --out collective/contrib/wip-c27h/rerun_N384 --seeds 7 --frames 90 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 7 px

## Measurements
- components: final 1, mean 1.0, max 1; occupancy final 0.07
- tracks: 1; persistent (alive >= 50% of run): 1; longest 91 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 1.66 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 21.5/time; max body lengths 3.5
- replication (lineage window K = 20 frames = time 4, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [-0.2391, -0.5067, -0.5049]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 45: holes 0, rim-vs-core 0.16, rim-vs-outside 1.01, heterogeneity 0.30; core [1.0, 0.474, 0.478] rim [0.951, 0.376, 0.355]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 6 components >= 14 px at frames [15, 30, 45, 60, 75, 90]):
  - radial phi (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.966, rim/outside 97.5 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.966)
  - radial rho (polarity, inside): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.47, rim/outside 45.7 (aggregate of 6 individuals; 4/6 membrane-like individually; rim level 0.447)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=9, R_eq 57.21): ['rho (polarity, inside)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
