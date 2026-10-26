# Evidence pack: ad9-ledger (seed 5)

- world: `../../../../../../threads/active-droplets/worlds/ad9-ledger/world.py`, family `phase-field`
- parent: ad7-gated (+ fisim-beyond-laplacian gated diffusion; identical-event RNG idea from fisim xcell-evo2-S); mutation: rung trait carried by catalyst; birth-coupled +-1 copy errors; Moran dilution; harmonic gate averaging; event ledger
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 218s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad9-ledger/world.py --out collective/contrib/20261025T2322-c23-review-ad9/rerun/seed5 --seeds 5 --frames 200 --no-movie`
- segmentation: matter > 0.45 of robust range [-1.048, 1.2789], min area 6 px

## Measurements
- components: final 12, mean 9.5, max 12; occupancy final 0.07
- tracks: 21; persistent (alive >= 50% of run): 11; longest 199 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.74 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 12, 12], H1 [0, 0, 0]
- motion: 5 long-lived tracks moved >= 1 body length; max speed 0.00104/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 2000, default): splits 7, persistent splits 5 (0 more failed only because the siblings re-merged within K), max generation 1, merges 1, merge/split ratio 0.143, nucleations 0
- channel total drift (end/start - 1): [-0.0021, -0.3855, None, 0.783, 1.6785]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 8 at frame 101: holes 0, rim-vs-core 0.82, rim-vs-outside 0.50, heterogeneity 0.16; core [0.941, 0.042, 0.236, 0.911, 1.0] rim [0.618, 0.205, 0.836, 0.489, 1.0]
  - track 9 at frame 126: holes 0, rim-vs-core 0.47, rim-vs-outside 0.70, heterogeneity 0.15; core [0.94, 0.034, 0.238, 0.922, 1.0] rim [0.767, 0.14, 0.588, 0.685, 1.0]
  - track 10 at frame 126: holes 0, rim-vs-core 0.78, rim-vs-outside 0.48, heterogeneity 0.15; core [0.945, 0.037, 0.23, 0.92, 1.0] rim [0.645, 0.201, 0.811, 0.52, 1.0]
  - track 11 at frame 129: holes 0, rim-vs-core 0.79, rim-vs-outside 0.47, heterogeneity 0.15; core [0.946, 0.036, 0.229, 0.923, 1.0] rim [0.65, 0.199, 0.825, 0.523, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 61 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.931, rim/outside 61.8 (aggregate of 61 individuals; 0/61 membrane-like individually; rim level 0.919)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 42.8, rim/outside 0.836 (aggregate of 61 individuals; 0/61 membrane-like individually; rim level 0.447)
  - radial psi (amphiphile): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 5.11, rim/outside 15.2 (aggregate of 61 individuals; 61/61 membrane-like individually; rim level 0.825)  MEMBRANE-LIKE
  - radial a (catalyst): peak at rho=0.25 (OUTSIDE the peak band 0.5-1.5), rim/core 0.907, rim/outside 82.2 (aggregate of 61 individuals; 0/61 membrane-like individually; rim level 0.897)
  - radial rung (kp index): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 70.6 (aggregate of 61 individuals; 0/61 membrane-like individually; rim level 1)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): psi (amphiphile)
- membrane-like channels per top track at mid-life: #8 (t=10100, R_eq 5.41): ['psi (amphiphile)']; #9 (t=12600, R_eq 5.86): ['psi (amphiphile)']; #10 (t=12600, R_eq 5.56): ['psi (amphiphile)']; #11 (t=12900, R_eq 5.56): ['psi (amphiphile)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
