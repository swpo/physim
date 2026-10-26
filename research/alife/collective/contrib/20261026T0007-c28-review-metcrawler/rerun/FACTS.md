# Evidence pack: wavepin-crawler-met (seed 3)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261025T2238-c22-metabolic-crawler-regrowth/world.py`, family `crawler-phase-field`
- parent: None; mutation: Camley et al. 2017 crawler at low contractility rho*=0.2 with weak noise eta=2 on rho; optional sector cut at cut_t (WORLD_P) and linear-kinetics twin (KIN=1)
- run: 151 frames x 200 steps x dt 0.001 = time 30; grid [256, 256]; wall 446s; status ok
- command: `python -m labkit.run collective/contrib/20261025T2238-c22-metabolic-crawler-regrowth/world.py --out /tmp/claude-0/c28mc/lk_met3 --seeds 3 --frames 150 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 1, mean 1.0, max 1; occupancy final 0.07
- tracks: 1; persistent (alive >= 50% of run): 1; longest 151 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 1.69 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 13.3/time; max body lengths 5.6
- replication (lineage window K = 20 frames = time 4, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [-0.2147, -0.4966, -0.4969, -0.069]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 76: holes 0, rim-vs-core 0.11, rim-vs-outside 1.12, heterogeneity 0.23; core [1.0, 0.479, 0.482, 0.044] rim [0.923, 0.554, 0.516, 0.032]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 6 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial phi (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.948, rim/outside 79.8 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.948)
  - radial rho (polarity, inside): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.8, rim/outside 41.9 (aggregate of 6 individuals; 4/6 membrane-like individually; rim level 0.468)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): rho (polarity, inside)
- membrane-like channels per top track at mid-life: #0 (t=15.2, R_eq 37.83): none

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
