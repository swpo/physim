# Evidence pack: cips-layered-divide (seed 0)

- world: `../../../20261026T1130-c40-cips-layered-divide-claim/world.py`, family `catalysis-induced-phase-separation`
- parent: collective/contrib/20261026T1025-c40-cips-turnover-divide-claim; mutation: c40 dividing CIPS world plus an amphiphile s made only by catalysis, adsorbing at the enzyme interface (drift up grad 4e(1-e)), decaying
- run: 201 frames x 1000 steps x dt 0.1 = time 20000; grid [192, 192]; wall 1191s; status ok
- command: `python -m labkit.run world.py --out pack/seed0 --seeds 0 --frames 200 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0215, 0.976], min area 6 px

## Measurements
- components: final 17, mean 12.3, max 17; occupancy final 0.09
- tracks: 28; persistent (alive >= 50% of run): 10; longest 199 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.36 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [17, 17, 17], H1 [0, 0, 0]
- motion: 11 long-lived tracks moved >= 1 body length; max speed 0.00333/time; max body lengths 1.9
- replication (lineage window K = 20 frames = time 2000, default): splits 11, persistent splits 11 (0 more failed only because the siblings re-merged within K), max generation 3, merges 0, merge/split ratio 0, nucleations 6
- channel total drift (end/start - 1): [-0.0, -0.5886, 0.6357, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.49, rim-vs-outside 0.63, heterogeneity 0.15; core [0.982, 0.935, 0.042, 0.078] rim [0.801, 0.718, 0.218, 0.436]
  - track 8 at frame 119: holes 0, rim-vs-core 0.38, rim-vs-outside 0.70, heterogeneity 0.16; core [0.972, 0.909, 0.051, 0.075] rim [0.83, 0.764, 0.172, 0.378]
  - track 9 at frame 119: holes 0, rim-vs-core 0.57, rim-vs-outside 0.59, heterogeneity 0.16; core [0.974, 0.916, 0.055, 0.077] rim [0.758, 0.694, 0.227, 0.526]
  - track 26 at frame 183: holes 0, rim-vs-core 0.54, rim-vs-outside 0.64, heterogeneity 0.16; core [0.991, 0.961, 0.08, 0.072] rim [0.79, 0.717, 0.258, 0.466]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 79 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial e: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.898, rim/outside 34.4 (aggregate of 79 individuals; 0/79 membrane-like individually; rim level 0.877)
  - radial p: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.875, rim/outside 12.4 (aggregate of 79 individuals; 0/79 membrane-like individually; rim level 0.84)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 22.2, rim/outside 0.654 (aggregate of 79 individuals; 0/79 membrane-like individually; rim level 0.498)
  - radial s: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 4.75, rim/outside 19.2 (aggregate of 79 individuals; 73/79 membrane-like individually; rim level 0.534)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s
- membrane-like channels per top track at mid-life: #0 (t=10100, R_eq 8.37): ['s']; #8 (t=11900, R_eq 8.9): ['s']; #9 (t=11900, R_eq 8.87): ['s']; #26 (t=18300, R_eq 7.02): ['s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
