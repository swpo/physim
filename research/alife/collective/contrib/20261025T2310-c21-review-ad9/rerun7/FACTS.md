# Evidence pack: ad9-ledger (seed 7)

- world: `../../../../threads/active-droplets/worlds/ad9-ledger/world.py`, family `phase-field`
- parent: ad7-gated (+ fisim-beyond-laplacian gated diffusion; identical-event RNG idea from fisim xcell-evo2-S); mutation: rung trait carried by catalyst; birth-coupled +-1 copy errors; Moran dilution; harmonic gate averaging; event ledger
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 296s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad9-ledger/world.py --out collective/contrib/20261025T2310-c21-review-ad9/rerun7 --seeds 7 --frames 200 --no-movie`
- segmentation: matter > 0.45 of robust range [-1.0499, 1.2728], min area 6 px

## Measurements
- components: final 12, mean 8.7, max 12; occupancy final 0.07
- tracks: 21; persistent (alive >= 50% of run): 10; longest 197 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.80 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 12, 12], H1 [0, 0, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.00104/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 2000, default): splits 8, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [-0.0129, -0.3954, None, 0.6841, 1.5804]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 103: holes 0, rim-vs-core 0.81, rim-vs-outside 0.48, heterogeneity 0.15; core [0.938, 0.04, 0.24, 0.913, 1.0] rim [0.634, 0.212, 0.84, 0.505, 1.0]
  - track 6 at frame 103: holes 0, rim-vs-core 0.55, rim-vs-outside 0.63, heterogeneity 0.15; core [0.961, 0.032, 0.205, 0.938, 1.0] rim [0.756, 0.144, 0.619, 0.655, 1.0]
  - track 7 at frame 126: holes 0, rim-vs-core 0.63, rim-vs-outside 0.85, heterogeneity 0.15; core [0.976, 0.01, 0.16, 0.983, 1.0] rim [0.755, 0.156, 0.626, 0.656, 1.0]
  - track 8 at frame 126: holes 0, rim-vs-core 0.80, rim-vs-outside 0.48, heterogeneity 0.15; core [0.947, 0.034, 0.229, 0.926, 1.0] rim [0.656, 0.211, 0.828, 0.527, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 57 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.927, rim/outside 50.1 (aggregate of 57 individuals; 0/57 membrane-like individually; rim level 0.914)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 43.1, rim/outside 0.831 (aggregate of 57 individuals; 0/57 membrane-like individually; rim level 0.455)
  - radial psi (amphiphile): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 4.85, rim/outside 13.9 (aggregate of 57 individuals; 57/57 membrane-like individually; rim level 0.783)  MEMBRANE-LIKE
  - radial a (catalyst): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.896, rim/outside 68.4 (aggregate of 57 individuals; 0/57 membrane-like individually; rim level 0.886)
  - radial rung (kp index): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 52.9 (aggregate of 57 individuals; 0/57 membrane-like individually; rim level 1)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): psi (amphiphile)
- membrane-like channels per top track at mid-life: #5 (t=10300, R_eq 5.7): ['psi (amphiphile)']; #6 (t=10300, R_eq 5.38): ['psi (amphiphile)']; #7 (t=12600, R_eq 6.02): ['psi (amphiphile)']; #8 (t=12600, R_eq 5.84): ['psi (amphiphile)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
