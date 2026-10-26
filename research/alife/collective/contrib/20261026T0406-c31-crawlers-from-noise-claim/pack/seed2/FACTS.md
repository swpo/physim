# Evidence pack: wavepin-crawler-layer-noise (seed 2)

- world: `../world4.py`, family `crawler-phase-field`
- parent: None; mutation: self-made adsorbed layer s (made by the bound polarity protein, kp*phi*rho; Langmuir adsorption) that excludes a cargo c (kappa); Camley et al. 2017 crawler at low contractility rho*=0.2 with weak noise eta=2 on rho; optional sector cut at cut_t (WORLD_P) and linear-kinetics twin (KIN=1)
- run: 81 frames x 200 steps x dt 0.001 = time 16; grid [256, 256]; wall 413s; status ok
- command: `python -m labkit.run collective/contrib/wip-c31/world4.py --out collective/contrib/wip-c31/pack4_s2 --seeds 2 --frames 80 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 1, mean 3.4, max 24; occupancy final 0.30
- tracks: 32; persistent (alive >= 50% of run): 1; longest 52 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.62 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 33/time; max body lengths 1.4
- replication (lineage window K = 20 frames = time 4, default): splits 1, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 6, merge/split ratio 6, nucleations 0
- channel total drift (end/start - 1): [-0.0267, -0.7464, -0.7209, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 3 at frame 26: holes 0, rim-vs-core 0.11, rim-vs-outside 1.17, heterogeneity 0.10; core [1.0, 0.589, 0.599, 0.122, 0.186] rim [0.943, 0.584, 0.559, 0.202, 0.158]
  - track 21 at frame 16: holes 0, rim-vs-core 0.33, rim-vs-outside 1.33, heterogeneity 0.12; core [0.999, 0.888, 0.901, 0.073, 0.134] rim [0.866, 0.882, 0.776, 0.344, 0.077]
  - track 19 at frame 15: holes 0, rim-vs-core 0.27, rim-vs-outside 1.22, heterogeneity 0.11; core [1.0, 0.74, 0.752, 0.084, 0.126] rim [0.883, 0.733, 0.658, 0.306, 0.086]
  - track 31 at frame 66: holes 0, rim-vs-core 0.28, rim-vs-outside 1.05, heterogeneity 0.23; core [1.0, 0.116, 0.118, 0.086, 0.216] rim [0.981, 0.315, 0.313, 0.118, 0.236]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 15 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial phi (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.962, rim/outside 9.16 (aggregate of 15 individuals; 0/15 membrane-like individually; rim level 0.962)
  - radial rho (polarity, inside): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.09, rim/outside 7.01 (aggregate of 15 individuals; 5/15 membrane-like individually; rim level 0.548)
  - radial s (layer species): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 2.87, rim/outside 6.5 (aggregate of 15 individuals; 10/15 membrane-like individually; rim level 0.369)  MEMBRANE-LIKE
  - radial c (cargo): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.15, rim/outside 3.45 (aggregate of 15 individuals; 3/15 membrane-like individually; rim level 0.167)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s (layer species)
- membrane-like channels per top track at mid-life: #3 (t=5.2, R_eq 33.55): ['s (layer species)']; #21 (t=3.2, R_eq 18.19): ['s (layer species)']; #19 (t=3, R_eq 23.12): ['s (layer species)']; #31 (t=13.2, R_eq 77.92): ['rho (polarity, inside)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: for 3 of 15 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
