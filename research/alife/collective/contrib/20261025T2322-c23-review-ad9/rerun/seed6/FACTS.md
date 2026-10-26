# Evidence pack: ad9-ledger (seed 6)

- world: `../../../../../../threads/active-droplets/worlds/ad9-ledger/world.py`, family `phase-field`
- parent: ad7-gated (+ fisim-beyond-laplacian gated diffusion; identical-event RNG idea from fisim xcell-evo2-S); mutation: rung trait carried by catalyst; birth-coupled +-1 copy errors; Moran dilution; harmonic gate averaging; event ledger
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 218s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad9-ledger/world.py --out collective/contrib/20261025T2322-c23-review-ad9/rerun/seed6 --seeds 6 --frames 200 --no-movie`
- segmentation: matter > 0.45 of robust range [-1.0484, 1.2716], min area 6 px

## Measurements
- components: final 12, mean 9.7, max 12; occupancy final 0.07
- tracks: 21; persistent (alive >= 50% of run): 12; longest 155 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.61 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 12, 12], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.000775/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 2000, default): splits 7, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 1, merges 1, merge/split ratio 0.143, nucleations 0
- channel total drift (end/start - 1): [-0.0017, -0.3857, None, 0.7785, 1.7331]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 9 at frame 124: holes 0, rim-vs-core 0.82, rim-vs-outside 0.50, heterogeneity 0.16; core [0.939, 0.04, 0.238, 0.913, 0.837] rim [0.619, 0.226, 0.836, 0.491, 0.837]
  - track 10 at frame 124: holes 0, rim-vs-core 0.82, rim-vs-outside 0.50, heterogeneity 0.16; core [0.939, 0.042, 0.24, 0.91, 0.837] rim [0.615, 0.223, 0.835, 0.486, 0.837]
  - track 11 at frame 129: holes 0, rim-vs-core 0.80, rim-vs-outside 0.50, heterogeneity 0.15; core [0.946, 0.041, 0.223, 0.917, 0.837] rim [0.629, 0.208, 0.806, 0.499, 0.837]
  - track 12 at frame 129: holes 0, rim-vs-core 0.47, rim-vs-outside 0.67, heterogeneity 0.15; core [0.943, 0.042, 0.232, 0.912, 0.837] rim [0.758, 0.141, 0.577, 0.67, 0.837]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 62 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.921, rim/outside 58.2 (aggregate of 62 individuals; 0/62 membrane-like individually; rim level 0.902)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 35.4, rim/outside 0.829 (aggregate of 62 individuals; 0/62 membrane-like individually; rim level 0.463)
  - radial psi (amphiphile): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 4.94, rim/outside 14.9 (aggregate of 62 individuals; 61/62 membrane-like individually; rim level 0.81)  MEMBRANE-LIKE
  - radial a (catalyst): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.891, rim/outside 82.6 (aggregate of 62 individuals; 0/62 membrane-like individually; rim level 0.876)
  - radial rung (kp index): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.993, rim/outside 66.3 (aggregate of 62 individuals; 0/62 membrane-like individually; rim level 0.851)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): psi (amphiphile)
- membrane-like channels per top track at mid-life: #9 (t=12400, R_eq 5.84): ['psi (amphiphile)']; #10 (t=12400, R_eq 5.75): ['psi (amphiphile)']; #11 (t=12900, R_eq 5.53): ['psi (amphiphile)']; #12 (t=12900, R_eq 5.59): ['psi (amphiphile)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
