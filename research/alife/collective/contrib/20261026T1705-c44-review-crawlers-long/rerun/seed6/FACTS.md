# Evidence pack: wavepin-crawler-layer-noise (seed 6)

- world: `../../world_claim.py`, family `crawler-phase-field`
- parent: None; mutation: self-made adsorbed layer s (made by the bound polarity protein, kp*phi*rho; Langmuir adsorption) that excludes a cargo c (kappa); Camley et al. 2017 crawler at low contractility rho*=0.2 with weak noise eta=2 on rho; optional sector cut at cut_t (WORLD_P) and linear-kinetics twin (KIN=1)
- run: 161 frames x 200 steps x dt 0.001 = time 32; grid [256, 256]; wall 1029s; status ok
- command: `python -m labkit.run world_claim.py --out rerun/seed6 --seeds 6 --frames 160 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 1, mean 3.0, max 22; occupancy final 0.31
- tracks: 31; persistent (alive >= 50% of run): 1; longest 91 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.08 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 24.9/time; max body lengths 2.4
- replication (lineage window K = 20 frames = time 4, default): splits 1, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 7, merge/split ratio 7, nucleations 0
- channel total drift (end/start - 1): [0.0296, -0.7216, -0.6936, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 14 at frame 46: holes 0, rim-vs-core 0.37, rim-vs-outside 1.31, heterogeneity 0.13; core [0.999, 0.848, 0.864, 0.088, 0.258] rim [0.864, 0.855, 0.754, 0.39, 0.141]
  - track 30 at frame 126: holes 0, rim-vs-core 0.31, rim-vs-outside 1.06, heterogeneity 0.21; core [1.0, 0.14, 0.142, 0.105, 0.161] rim [0.968, 0.351, 0.347, 0.123, 0.238]
  - track 16 at frame 26: holes 0, rim-vs-core 0.45, rim-vs-outside 1.36, heterogeneity 0.13; core [0.998, 0.967, 0.977, 0.076, 0.166] rim [0.833, 0.965, 0.828, 0.449, 0.07]
  - track 29 at frame 71: holes 0, rim-vs-core 0.23, rim-vs-outside 1.06, heterogeneity 0.22; core [1.0, 0.207, 0.211, 0.11, 0.142] rim [0.965, 0.362, 0.356, 0.126, 0.227]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 13 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial phi (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.985, rim/outside 15.4 (aggregate of 13 individuals; 0/13 membrane-like individually; rim level 0.985)
  - radial rho (polarity, inside): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.26, rim/outside 13.9 (aggregate of 13 individuals; 6/13 membrane-like individually; rim level 0.596)
  - radial s (layer species): peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 3.63, rim/outside 7.9 (aggregate of 13 individuals; 7/13 membrane-like individually; rim level 0.436)  MEMBRANE-LIKE
  - radial c (cargo): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.11, rim/outside 2.41 (aggregate of 13 individuals; 2/13 membrane-like individually; rim level 0.196)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s (layer species)
- membrane-like channels per top track at mid-life: #14 (t=9.2, R_eq 18.79): ['s (layer species)']; #30 (t=25.2, R_eq 80.86): ['rho (polarity, inside)']; #16 (t=5.2, R_eq 15.7): ['s (layer species)']; #29 (t=14.2, R_eq 77.04): ['rho (polarity, inside)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: for 5 of 13 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
