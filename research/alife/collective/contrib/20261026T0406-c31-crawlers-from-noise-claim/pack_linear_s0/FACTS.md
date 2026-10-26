# Evidence pack: wavepin-crawler-layer-noise (seed 0)

- world: `../world4.py`, family `crawler-phase-field`
- parent: None; mutation: self-made adsorbed layer s (made by the bound polarity protein, kp*phi*rho; Langmuir adsorption) that excludes a cargo c (kappa); Camley et al. 2017 crawler at low contractility rho*=0.2 with weak noise eta=2 on rho; optional sector cut at cut_t (WORLD_P) and linear-kinetics twin (KIN=1)
- run: 81 frames x 200 steps x dt 0.001 = time 16; grid [256, 256]; wall 407s; status ok
- command: `python -m labkit.run collective/contrib/wip-c31/world4.py --out collective/contrib/wip-c31/pack4_lin_s0 --seeds 0 --frames 80 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 1, mean 1.8, max 30; occupancy final 0.06
- tracks: 32; persistent (alive >= 50% of run): 1; longest 81 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 1.12 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.0
- replication (lineage window K = 20 frames = time 4, default): splits 1, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [-0.7955, -0.8826, -0.8712, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 25 at frame 40: holes 0, rim-vs-core 0.18, rim-vs-outside 1.43, heterogeneity 0.14; core [1.0, 0.797, 0.818, 0.147, 0.63] rim [0.921, 0.785, 0.743, 0.275, 0.562]
  - track 15 at frame 5: holes 0, rim-vs-core 0.26, rim-vs-outside 1.31, heterogeneity 0.11; core [1.0, 0.879, 0.899, 0.053, 0.102] rim [0.861, 0.862, 0.763, 0.22, 0.081]
  - track 23 at frame 3: holes 0, rim-vs-core 0.21, rim-vs-outside 1.32, heterogeneity 0.09; core [1.0, 0.879, 0.898, 0.035, 0.055] rim [0.863, 0.87, 0.771, 0.129, 0.043]
  - track 31 at frame 4: holes 0, rim-vs-core 0.28, rim-vs-outside 1.28, heterogeneity 0.11; core [0.998, 0.875, 0.893, 0.036, 0.081] rim [0.832, 0.889, 0.762, 0.215, 0.061]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 6 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial phi (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 101 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 1)
  - radial rho (polarity, inside): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 80 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.79)
  - radial s (layer species): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 2.57, rim/outside 21.3 (aggregate of 6 individuals; 6/6 membrane-like individually; rim level 0.474)  MEMBRANE-LIKE
  - radial c (cargo): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.31, rim/outside 17.1 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.764)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s (layer species)
- membrane-like channels per top track at mid-life: #25 (t=8, R_eq 36.09): ['s (layer species)']; #15 (t=1, R_eq 20.9): ['s (layer species)']; #23 (t=0.6, R_eq 20.48): ['s (layer species)']; #31 (t=0.8, R_eq 17.56): ['s (layer species)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
