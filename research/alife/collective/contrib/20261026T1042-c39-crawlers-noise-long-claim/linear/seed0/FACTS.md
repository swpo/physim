# Evidence pack: wavepin-crawler-layer-noise (seed 0)

- world: `../../world.py`, family `crawler-phase-field`
- parent: None; mutation: self-made adsorbed layer s (made by the bound polarity protein, kp*phi*rho; Langmuir adsorption) that excludes a cargo c (kappa); Camley et al. 2017 crawler at low contractility rho*=0.2 with weak noise eta=2 on rho; optional sector cut at cut_t (WORLD_P) and linear-kinetics twin (KIN=1)
- run: 161 frames x 200 steps x dt 0.001 = time 32; grid [256, 256]; wall 933s; status ok
- command: `python -m labkit.run collective/contrib/c39-crawl-long-wip/world.py --out collective/contrib/c39-crawl-long-wip/linear/seed0 --seeds 0 --frames 160 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 1, mean 1.4, max 30; occupancy final 0.06
- tracks: 32; persistent (alive >= 50% of run): 1; longest 161 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 1.12 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.0
- replication (lineage window K = 20 frames = time 4, default): splits 1, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio 0, nucleations 0
- channel total drift (end/start - 1): [-0.7956, -0.8818, -0.8704, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 25 at frame 81: holes 0, rim-vs-core 0.18, rim-vs-outside 1.49, heterogeneity 0.15; core [1.0, 0.818, 0.83, 0.14, 0.721] rim [0.922, 0.824, 0.772, 0.266, 0.643]
  - track 15 at frame 5: holes 0, rim-vs-core 0.25, rim-vs-outside 1.34, heterogeneity 0.10; core [1.0, 0.907, 0.918, 0.05, 0.077] rim [0.861, 0.892, 0.784, 0.208, 0.061]
  - track 23 at frame 3: holes 0, rim-vs-core 0.21, rim-vs-outside 1.35, heterogeneity 0.09; core [1.0, 0.907, 0.917, 0.033, 0.041] rim [0.863, 0.899, 0.791, 0.122, 0.032]
  - track 31 at frame 4: holes 0, rim-vs-core 0.27, rim-vs-outside 1.30, heterogeneity 0.10; core [0.998, 0.903, 0.913, 0.034, 0.061] rim [0.832, 0.917, 0.782, 0.203, 0.046]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 6 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial phi (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 101 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 1)
  - radial rho (polarity, inside): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 83.4 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.824)
  - radial s (layer species): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 2.64, rim/outside 22.4 (aggregate of 6 individuals; 6/6 membrane-like individually; rim level 0.472)  MEMBRANE-LIKE
  - radial c (cargo): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.34, rim/outside 16.3 (aggregate of 6 individuals; 0/6 membrane-like individually; rim level 0.84)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s (layer species)
- membrane-like channels per top track at mid-life: #25 (t=16.2, R_eq 36.09): ['s (layer species)']; #15 (t=1, R_eq 20.9): ['s (layer species)']; #23 (t=0.6, R_eq 20.48): ['s (layer species)']; #31 (t=0.8, R_eq 17.56): ['s (layer species)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
