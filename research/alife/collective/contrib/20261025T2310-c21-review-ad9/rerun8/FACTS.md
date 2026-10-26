# Evidence pack: ad9-ledger (seed 8)

- world: `../../../../threads/active-droplets/worlds/ad9-ledger/world.py`, family `phase-field`
- parent: ad7-gated (+ fisim-beyond-laplacian gated diffusion; identical-event RNG idea from fisim xcell-evo2-S); mutation: rung trait carried by catalyst; birth-coupled +-1 copy errors; Moran dilution; harmonic gate averaging; event ledger
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 296s; status ok
- command: `python -m labkit.run threads/active-droplets/worlds/ad9-ledger/world.py --out collective/contrib/20261025T2310-c21-review-ad9/rerun8 --seeds 8 --frames 200 --no-movie`
- segmentation: matter > 0.45 of robust range [-1.0483, 1.2803], min area 6 px

## Measurements
- components: final 12, mean 9.8, max 12; occupancy final 0.07
- tracks: 18; persistent (alive >= 50% of run): 12; longest 148 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.60 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 12, 12], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.000986/time; max body lengths 1.2
- replication (lineage window K = 20 frames = time 2000, default): splits 6, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [-0.0013, -0.3864, None, 0.7846, 1.7088]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 128: holes 0, rim-vs-core 0.76, rim-vs-outside 0.45, heterogeneity 0.14; core [0.947, 0.037, 0.221, 0.922, 1.0] rim [0.657, 0.196, 0.792, 0.534, 1.0]
  - track 7 at frame 128: holes 0, rim-vs-core 0.81, rim-vs-outside 0.49, heterogeneity 0.15; core [0.946, 0.036, 0.223, 0.923, 1.0] rim [0.643, 0.204, 0.824, 0.515, 1.0]
  - track 8 at frame 133: holes 0, rim-vs-core 0.78, rim-vs-outside 0.48, heterogeneity 0.15; core [0.947, 0.035, 0.224, 0.924, 1.0] rim [0.656, 0.201, 0.805, 0.529, 1.0]
  - track 9 at frame 133: holes 0, rim-vs-core 0.74, rim-vs-outside 0.48, heterogeneity 0.14; core [0.952, 0.038, 0.216, 0.924, 1.0] rim [0.673, 0.183, 0.768, 0.544, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 62 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.922, rim/outside 58.7 (aggregate of 62 individuals; 0/62 membrane-like individually; rim level 0.905)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 36.2, rim/outside 0.829 (aggregate of 62 individuals; 0/62 membrane-like individually; rim level 0.451)
  - radial psi (amphiphile): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 4.89, rim/outside 14.7 (aggregate of 62 individuals; 60/62 membrane-like individually; rim level 0.808)  MEMBRANE-LIKE
  - radial a (catalyst): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.895, rim/outside 78.6 (aggregate of 62 individuals; 0/62 membrane-like individually; rim level 0.88)
  - radial rung (kp index): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.99, rim/outside 65 (aggregate of 62 individuals; 0/62 membrane-like individually; rim level 0.99)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): psi (amphiphile)
- membrane-like channels per top track at mid-life: #6 (t=12800, R_eq 5.53): ['psi (amphiphile)']; #7 (t=12800, R_eq 5.61): ['psi (amphiphile)']; #8 (t=13300, R_eq 5.61): ['psi (amphiphile)']; #9 (t=13300, R_eq 5.23): ['psi (amphiphile)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
