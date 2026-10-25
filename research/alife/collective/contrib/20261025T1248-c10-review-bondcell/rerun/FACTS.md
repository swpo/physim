# Evidence pack: bondcell (seed 3)

- world: `../../20261025T1104-c05-bondcell-rings-decay/world_small.py`, family `particle`
- parent: threads/particle-life/worlds/sporecell3-det; mutation: membrane particles form harmonic chain bonds (<=2 per particle); bonded M does not revert to core
- run: 141 frames x 50 steps x dt 0.02 = time 140; grid [128, 128]; wall 710s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1104-c05-bondcell-rings-decay/world_small.py --out collective/contrib/20261025T1248-c10-review-bondcell/rerun --seeds 3 --frames 140 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 9.7265], min area 6 px

## Measurements
- components: final 2, mean 1.4, max 3; occupancy final 0.01
- tracks: 28; persistent (alive >= 50% of run): 1; longest 94 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.30 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [2, 2, 1], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 2.78/time; max body lengths 19.4
- replication (lineage window K = 20 frames = time 20, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 28
- channel total drift (end/start - 1): [-0.7931, 4.0714, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 5 at frame 94: holes 0, rim-vs-core 0.21, rim-vs-outside 0.38, heterogeneity 0.11; core [0.035, 0.088, 0.801, 1.0] rim [0.036, 0.034, 1.0, 0.99]
  - track 8 at frame 111: holes 0, rim-vs-core 0.13, rim-vs-outside 0.14, heterogeneity 0.04; core [0.007, 0.0, 0.185, 1.0] rim [0.018, 0.0, 0.311, 1.0]
  - track 7 at frame 82: holes 0, rim-vs-core 0.06, rim-vs-outside 0.12, heterogeneity 0.02; core [0.017, 0.0, 0.035, 1.0] rim [0.028, 0.0, 0.089, 1.0]
  - track 14 at frame 115: holes 0, rim-vs-core 0.13, rim-vs-outside 0.12, heterogeneity 0.04; core [0.0, 1.0, 0.245, 0.0] rim [0.0, 1.0, 0.376, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 8 components >= 12 px at frames [47, 71, 93, 116, 140]):
  - radial F food: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.543, rim/outside 0.421 (aggregate of 8 individuals; 0/8 membrane-like individually; rim level 0.0187)
  - radial C0 core kind 0: peak at rho=0.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.05, rim/outside 1.7 (aggregate of 8 individuals; 0/8 membrane-like individually; rim level 0.22)
  - radial M membrane: peak at rho=1.15 (in the peak band 0.5-1.5), rim/core 2.89, rim/outside 5.49 (aggregate of 8 individuals; 5/8 membrane-like individually; rim level 0.861)  MEMBRANE-LIKE
  - radial C1 core kind 1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.943, rim/outside 12.7 (aggregate of 8 individuals; 0/8 membrane-like individually; rim level 0.875)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): M membrane
- membrane-like channels per top track at mid-life: #5 (t=94, R_eq 5.56): ['M membrane']; #8 (t=111, R_eq 2.88): none; #7 (t=82, R_eq 2.03): none; #14 (t=115, R_eq 2.82): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
