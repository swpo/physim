# Evidence pack: ad9-ledger (seed 4)

- world: `../../world.py`, family `phase-field`
- parent: ad7-gated (+ fisim-beyond-laplacian gated diffusion; identical-event RNG idea from fisim xcell-evo2-S); mutation: rung trait carried by catalyst; birth-coupled +-1 copy errors; Moran dilution; harmonic gate averaging; event ledger
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 229s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0512-c32-review-ad9/world.py --out collective/contrib/20261026T0512-c32-review-ad9/pack --seeds 3 4 --frames 200 --no-movie`
- segmentation: matter > 0.45 of robust range [-1.0542, 1.2878], min area 6 px

## Measurements
- components: final 12, mean 9.4, max 12; occupancy final 0.08
- tracks: 23; persistent (alive >= 50% of run): 9; longest 201 frames; alive start-to-end: 2
- size of persistent tracks: max/min area ratio 1.86 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [13, 12, 12], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 0.000945/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 2000, default): splits 8, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 3, merges 1, merge/split ratio 0.125, nucleations 0
- channel total drift (end/start - 1): [0.0109, -0.4174, None, 0.913, 1.6642]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 4 at frame 101: holes 0, rim-vs-core 0.79, rim-vs-outside 0.47, heterogeneity 0.15; core [0.93, 0.042, 0.237, 0.912, 1.0] rim [0.638, 0.204, 0.834, 0.513, 1.0]
  - track 5 at frame 101: holes 0, rim-vs-core 0.80, rim-vs-outside 0.47, heterogeneity 0.15; core [0.938, 0.042, 0.241, 0.914, 1.0] rim [0.636, 0.208, 0.845, 0.51, 1.0]
  - track 10 at frame 126: holes 0, rim-vs-core 0.77, rim-vs-outside 0.48, heterogeneity 0.14; core [0.95, 0.032, 0.223, 0.933, 1.0] rim [0.673, 0.197, 0.807, 0.547, 1.0]
  - track 19 at frame 188: holes 0, rim-vs-core 0.39, rim-vs-outside 0.93, heterogeneity 0.13; core [0.992, 0.016, 0.105, 0.977, 0.805] rim [0.818, 0.096, 0.351, 0.746, 0.805]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 59 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.911, rim/outside 51.7 (aggregate of 59 individuals; 0/59 membrane-like individually; rim level 0.89)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 35, rim/outside 0.814 (aggregate of 59 individuals; 0/59 membrane-like individually; rim level 0.428)
  - radial psi (amphiphile): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 4.56, rim/outside 14 (aggregate of 59 individuals; 57/59 membrane-like individually; rim level 0.736)  MEMBRANE-LIKE
  - radial a (catalyst): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.884, rim/outside 78 (aggregate of 59 individuals; 0/59 membrane-like individually; rim level 0.866)
  - radial rung (kp index): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.989, rim/outside 63.7 (aggregate of 59 individuals; 0/59 membrane-like individually; rim level 0.959)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): psi (amphiphile)
- membrane-like channels per top track at mid-life: #4 (t=10100, R_eq 5.67): ['psi (amphiphile)']; #5 (t=10100, R_eq 5.59): ['psi (amphiphile)']; #10 (t=12600, R_eq 5.7): ['psi (amphiphile)']; #19 (t=18800, R_eq 6.21): ['psi (amphiphile)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
