# Evidence pack: wavepin-crawler-layer-noise (seed 56)

- world: `../../../20261026T1042-c39-crawlers-noise-long-claim/world.py`, family `crawler-phase-field`
- parent: None; mutation: self-made adsorbed layer s (made by the bound polarity protein, kp*phi*rho; Langmuir adsorption) that excludes a cargo c (kappa); Camley et al. 2017 crawler at low contractility rho*=0.2 with weak noise eta=2 on rho; optional sector cut at cut_t (WORLD_P) and linear-kinetics twin (KIN=1)
- run: 161 frames x 200 steps x dt 0.001 = time 32; grid [256, 256]; wall 838s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1042-c39-crawlers-noise-long-claim/world.py --out collective/contrib/20261026T1735-c45-review-crawlers-long/rerun/seed56 --seeds 56 --frames 160 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 1, mean 1.8, max 31; occupancy final 0.29
- tracks: 38; persistent (alive >= 50% of run): 1; longest 131 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.10 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 24.9/time; max body lengths 4.7
- replication (lineage window K = 20 frames = time 4, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 7, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [-0.0566, -0.7398, -0.7134, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 37 at frame 95: holes 0, rim-vs-core 0.06, rim-vs-outside 1.01, heterogeneity 0.22; core [1.0, 0.278, 0.281, 0.118, 0.177] rim [0.975, 0.268, 0.261, 0.135, 0.22]
  - track 2 at frame 15: holes 0, rim-vs-core 0.16, rim-vs-outside 1.21, heterogeneity 0.11; core [1.0, 0.668, 0.674, 0.105, 0.099] rim [0.924, 0.671, 0.626, 0.237, 0.083]
  - track 11 at frame 11: holes 0, rim-vs-core 0.33, rim-vs-outside 1.27, heterogeneity 0.12; core [0.999, 0.826, 0.834, 0.076, 0.076] rim [0.861, 0.827, 0.719, 0.347, 0.046]
  - track 9 at frame 8: holes 0, rim-vs-core 0.23, rim-vs-outside 1.24, heterogeneity 0.10; core [1.0, 0.759, 0.766, 0.074, 0.054] rim [0.886, 0.757, 0.677, 0.253, 0.039]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 7 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial phi (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.968, rim/outside 24.3 (aggregate of 7 individuals; 0/7 membrane-like individually; rim level 0.968)
  - radial rho (polarity, inside): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.5, rim/outside 11.2 (aggregate of 7 individuals; 6/7 membrane-like individually; rim level 0.37)  MEMBRANE-LIKE
  - radial s (layer species): peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 1.4, rim/outside 6.84 (aggregate of 7 individuals; 1/7 membrane-like individually; rim level 0.187)
  - radial c (cargo): peak at rho=1.15 (in the peak band 0.5-1.5), rim/core 1.28, rim/outside 2.37 (aggregate of 7 individuals; 4/7 membrane-like individually; rim level 0.192)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): rho (polarity, inside)
- membrane-like channels per top track at mid-life: #37 (t=19, R_eq 77.32): ['rho (polarity, inside)', 'c (cargo)']; #2 (t=3, R_eq 26.86): ['s (layer species)']; #11 (t=2.2, R_eq 20.4): ['s (layer species)']; #9 (t=1.6, R_eq 22.74): ['s (layer species)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: for 5 of 7 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
