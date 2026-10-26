# Evidence pack: cips-layered-divide (seed 0)

- world: `../world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1025-c40-cips-turnover-divide-claim; mutation: c40 dividing CIPS world plus an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 121 frames x 1000 steps x dt 0.1 = time 12000; grid [192, 192]; wall 1077s; status ok
- command: `python -m labkit.run /tmp/claude-0/-home-user-physim/1b1a770d-5b2c-5e4e-abc5-f6c6c2737e43/scratchpad/fpd/world.py --out /tmp/claude-0/-home-user-physim/1b1a770d-5b2c-5e4e-abc5-f6c6c2737e43/scratchpad/fpd/pack --seeds 0 --frames 120 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0222, 0.9759], min area 6 px

## Measurements
- components: final 16, mean 11.6, max 16; occupancy final 0.08
- tracks: 24; persistent (alive >= 50% of run): 10; longest 119 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.31 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [16, 16, 16], H1 [0, 0, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.0029/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 2000, default): splits 8, persistent splits 7 (0 more failed only because the siblings re-merged within K), max generation 2, merges 0, merge/split ratio 0, nucleations 8
- channel total drift (end/start - 1): [-0.0232, 0.5509, -0.0894, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 62: holes 0, rim-vs-core 0.58, rim-vs-outside 0.60, heterogeneity 0.16; core [0.982, 0.936, 0.041, 0.084] rim [0.767, 0.691, 0.226, 0.527]
  - track 3 at frame 63: holes 0, rim-vs-core 0.59, rim-vs-outside 0.59, heterogeneity 0.17; core [0.972, 0.914, 0.055, 0.08] rim [0.748, 0.688, 0.23, 0.551]
  - track 9 at frame 81: holes 0, rim-vs-core 0.55, rim-vs-outside 0.63, heterogeneity 0.16; core [0.988, 0.954, 0.056, 0.077] rim [0.782, 0.708, 0.239, 0.484]
  - track 20 at frame 110: holes 0, rim-vs-core 0.52, rim-vs-outside 0.65, heterogeneity 0.16; core [0.991, 0.962, 0.085, 0.069] rim [0.794, 0.72, 0.256, 0.451]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 76 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.909, rim/outside 38.2 (aggregate of 76 individuals; 0/76 membrane-like individually; rim level 0.894)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.879, rim/outside 12.7 (aggregate of 76 individuals; 0/76 membrane-like individually; rim level 0.85)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 27.9, rim/outside 0.651 (aggregate of 76 individuals; 0/76 membrane-like individually; rim level 0.49)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 5.25, rim/outside 21 (aggregate of 76 individuals; 72/76 membrane-like individually; rim level 0.556)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #0 (t=6200, R_eq 8.2): ['s']; #3 (t=6300, R_eq 8.48): ['s']; #9 (t=8100, R_eq 7.4): ['s']; #20 (t=11000, R_eq 6.68): ['s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
