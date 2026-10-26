# Evidence pack: wavepin-crawler-layer-noise (seed 0)

- world: `../world4.py`, family `crawler-phase-field`
- parent: None; mutation: self-made adsorbed layer s (made by the bound polarity protein, kp*phi*rho; Langmuir adsorption) that excludes a cargo c (kappa); Camley et al. 2017 crawler at low contractility rho*=0.2 with weak noise eta=2 on rho; optional sector cut at cut_t (WORLD_P) and linear-kinetics twin (KIN=1)
- run: 81 frames x 200 steps x dt 0.001 = time 16; grid [256, 256]; wall 424s; status ok
- command: `python -m labkit.run collective/contrib/wip-c31/world4.py --out collective/contrib/wip-c31/pack4_s0 --seeds 0 --frames 80 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 1, mean 3.7, max 30; occupancy final 0.22
- tracks: 36; persistent (alive >= 50% of run): 2; longest 43 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.36 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 26.4/time; max body lengths 1.6
- replication (lineage window K = 20 frames = time 4, default): splits 1, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 4, merge/split ratio 4, nucleations 0
- channel total drift (end/start - 1): [-0.2724, -0.7782, -0.757, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 23 at frame 21: holes 0, rim-vs-core 0.23, rim-vs-outside 1.19, heterogeneity 0.11; core [1.0, 0.663, 0.675, 0.098, 0.207] rim [0.899, 0.66, 0.603, 0.283, 0.156]
  - track 6 at frame 20: holes 0, rim-vs-core 0.43, rim-vs-outside 1.31, heterogeneity 0.13; core [0.998, 0.927, 0.939, 0.073, 0.2] rim [0.835, 0.925, 0.788, 0.425, 0.089]
  - track 35 at frame 62: holes 0, rim-vs-core 0.18, rim-vs-outside 1.07, heterogeneity 0.23; core [1.0, 0.253, 0.258, 0.127, 0.201] rim [0.958, 0.375, 0.365, 0.135, 0.271]
  - track 30 at frame 15: holes 0, rim-vs-core 0.26, rim-vs-outside 1.16, heterogeneity 0.11; core [1.0, 0.683, 0.695, 0.088, 0.152] rim [0.882, 0.68, 0.61, 0.301, 0.105]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 16 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial phi (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.986, rim/outside 13.9 (aggregate of 16 individuals; 0/16 membrane-like individually; rim level 0.985)
  - radial rho (polarity, inside): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.15, rim/outside 10.8 (aggregate of 16 individuals; 5/16 membrane-like individually; rim level 0.618)
  - radial s (layer species): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 3.52, rim/outside 9.51 (aggregate of 16 individuals; 12/16 membrane-like individually; rim level 0.438)  MEMBRANE-LIKE
  - radial c (cargo): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.14, rim/outside 4.33 (aggregate of 16 individuals; 2/16 membrane-like individually; rim level 0.211)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s (layer species)
- membrane-like channels per top track at mid-life: #23 (t=4.2, R_eq 26.81): ['s (layer species)']; #6 (t=4, R_eq 17.06): ['s (layer species)']; #35 (t=12.4, R_eq 68.33): ['rho (polarity, inside)']; #30 (t=3, R_eq 25.93): ['s (layer species)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
