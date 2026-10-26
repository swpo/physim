# Evidence pack: ad9-ledger (seed 3)

- world: `../../world.py`, family `phase-field`
- parent: ad7-gated (+ fisim-beyond-laplacian gated diffusion; identical-event RNG idea from fisim xcell-evo2-S); mutation: rung trait carried by catalyst; birth-coupled +-1 copy errors; Moran dilution; harmonic gate averaging; event ledger
- run: 201 frames x 200 steps x dt 0.5 = time 20000; grid [128, 128]; wall 228s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0512-c32-review-ad9/world.py --out collective/contrib/20261026T0512-c32-review-ad9/pack --seeds 3 4 --frames 200 --no-movie`
- segmentation: matter > 0.45 of robust range [-1.0483, 1.28], min area 6 px

## Measurements
- components: final 12, mean 9.8, max 12; occupancy final 0.07
- tracks: 18; persistent (alive >= 50% of run): 11; longest 156 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.71 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 12, 12], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.00106/time; max body lengths 1.5
- replication (lineage window K = 20 frames = time 2000, default): splits 6, persistent splits 6 (0 more failed only because the siblings re-merged within K), max generation 1, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [0.0014, -0.393, None, 0.8194, 1.7183]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 6 at frame 123: holes 0, rim-vs-core 0.83, rim-vs-outside 0.48, heterogeneity 0.15; core [0.939, 0.038, 0.245, 0.916, 1.0] rim [0.626, 0.224, 0.869, 0.498, 1.0]
  - track 7 at frame 123: holes 0, rim-vs-core 0.79, rim-vs-outside 0.47, heterogeneity 0.15; core [0.947, 0.037, 0.23, 0.923, 1.0] rim [0.657, 0.201, 0.824, 0.53, 1.0]
  - track 8 at frame 133: holes 0, rim-vs-core 0.80, rim-vs-outside 0.48, heterogeneity 0.15; core [0.947, 0.036, 0.227, 0.923, 1.0] rim [0.646, 0.204, 0.829, 0.518, 1.0]
  - track 9 at frame 133: holes 0, rim-vs-core 0.84, rim-vs-outside 0.48, heterogeneity 0.16; core [0.938, 0.04, 0.244, 0.913, 1.0] rim [0.615, 0.225, 0.867, 0.489, 1.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 62 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial phi (droplet material): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.922, rim/outside 52 (aggregate of 62 individuals; 0/62 membrane-like individually; rim level 0.904)
  - radial u (fuel): peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 35.2, rim/outside 0.831 (aggregate of 62 individuals; 0/62 membrane-like individually; rim level 0.448)
  - radial psi (amphiphile): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 4.82, rim/outside 14.5 (aggregate of 62 individuals; 61/62 membrane-like individually; rim level 0.81)  MEMBRANE-LIKE
  - radial a (catalyst): peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.897, rim/outside 68.9 (aggregate of 62 individuals; 0/62 membrane-like individually; rim level 0.88)
  - radial rung (kp index): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.985, rim/outside 50.7 (aggregate of 62 individuals; 0/62 membrane-like individually; rim level 0.985)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): psi (amphiphile)
- membrane-like channels per top track at mid-life: #6 (t=12300, R_eq 5.86): ['psi (amphiphile)']; #7 (t=12300, R_eq 5.61): ['psi (amphiphile)']; #8 (t=13300, R_eq 5.61): ['psi (amphiphile)']; #9 (t=13300, R_eq 5.81): ['psi (amphiphile)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
