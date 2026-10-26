# Evidence pack: wavepin-crawler-layer-noise (seed 2)

- world: `../world.py`, family `crawler-phase-field`
- parent: None; mutation: self-made adsorbed layer s (made by the bound polarity protein, kp*phi*rho; Langmuir adsorption) that excludes a cargo c (kappa); Camley et al. 2017 crawler at low contractility rho*=0.2 with weak noise eta=2 on rho; optional sector cut at cut_t (WORLD_P) and linear-kinetics twin (KIN=1)
- run: 71 frames x 200 steps x dt 0.001 = time 14; grid [256, 256]; wall 332s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0449-c32-review-crawl-nodiv/world.py --out collective/contrib/20261026T0449-c32-review-crawl-nodiv/pack_rs025 --seeds 2 --frames 70 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 2, mean 5.1, max 24; occupancy final 0.29
- tracks: 30; persistent (alive >= 50% of run): 5; longest 71 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 7.37 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [2, 2, 2], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 21.9/time; max body lengths 2.2
- replication (lineage window K = 20 frames = time 4, default): splits 1, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 4, merge/split ratio 4, nucleations 0
- channel total drift (end/start - 1): [-0.0378, -0.6804, -0.647, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 21 at frame 35: holes 0, rim-vs-core 0.49, rim-vs-outside 1.37, heterogeneity 0.14; core [0.998, 0.977, 0.99, 0.081, 0.332] rim [0.83, 0.975, 0.844, 0.47, 0.125]
  - track 3 at frame 32: holes 0, rim-vs-core 0.12, rim-vs-outside 1.17, heterogeneity 0.10; core [1.0, 0.564, 0.584, 0.108, 0.202] rim [0.942, 0.575, 0.56, 0.208, 0.178]
  - track 24 at frame 33: holes 0, rim-vs-core 0.25, rim-vs-outside 1.04, heterogeneity 0.23; core [1.0, 0.213, 0.22, 0.103, 0.173] rim [0.946, 0.377, 0.37, 0.189, 0.227]
  - track 27 at frame 43: holes 0, rim-vs-core 0.22, rim-vs-outside 1.09, heterogeneity 0.23; core [1.0, 0.308, 0.319, 0.123, 0.116] rim [0.946, 0.428, 0.42, 0.174, 0.244]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 26 components >= 12 px at frames [12, 23, 35, 47, 58, 70]):
  - radial phi (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.993, rim/outside 14 (aggregate of 26 individuals; 0/26 membrane-like individually; rim level 0.993)
  - radial rho (polarity, inside): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.03, rim/outside 12.7 (aggregate of 26 individuals; 5/26 membrane-like individually; rim level 0.629)
  - radial s (layer species): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 3.85, rim/outside 8.45 (aggregate of 26 individuals; 24/26 membrane-like individually; rim level 0.478)  MEMBRANE-LIKE
  - radial c (cargo): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.37, rim/outside 5.46 (aggregate of 26 individuals; 8/26 membrane-like individually; rim level 0.234)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s (layer species)
- membrane-like channels per top track at mid-life: #21 (t=7, R_eq 14.56): ['s (layer species)']; #3 (t=6.4, R_eq 31.73): ['s (layer species)']; #24 (t=6.6, R_eq 37.27): ['rho (polarity, inside)', 's (layer species)', 'c (cargo)']; #27 (t=8.6, R_eq 52.51): ['rho (polarity, inside)', 's (layer species)', 'c (cargo)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: for 1 of 26 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
