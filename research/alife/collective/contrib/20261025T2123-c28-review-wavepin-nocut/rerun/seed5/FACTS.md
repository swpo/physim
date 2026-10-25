# Evidence pack: wavepin-crawler (seed 5)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/20261025T1915-c22-wavepin-front-cut-no-repair/world.py`, family `crawler-phase-field`
- parent: None; mutation: Camley et al. 2017 wave-pinning crawler; optional sector cut and linear-kinetics twin
- run: 81 frames x 200 steps x dt 0.001 = time 16; grid [256, 256]; wall 200s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1915-c22-wavepin-front-cut-no-repair/world.py --out /tmp/claude-0/c28wp/lk_front30 --seeds 5 6 --frames 80 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 1, mean 1.0, max 1; occupancy final 0.09
- tracks: 1; persistent (alive >= 50% of run): 1; longest 81 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 1.48 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 7.65/time; max body lengths 1.6
- replication (lineage window K = 20 frames = time 4, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [-0.0518, -0.1259, -0.1252]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 40: holes 0, rim-vs-core 0.50, rim-vs-outside 1.32, heterogeneity 0.32; core [1.0, 0.349, 0.35] rim [0.95, 0.72, 0.687]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 6 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial phi (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.893, rim/outside 53.1 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.892)
  - radial rho (polarity, inside): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.43, rim/outside 35.6 (aggregate of 6 individuals; 4/6 membrane-like individually; rim level 0.591)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=8, R_eq 45.72): ['rho (polarity, inside)']

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
