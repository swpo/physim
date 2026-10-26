# Evidence pack: wavepin-crawler-layer-noise (seed 2)

- world: `../../world.py`, family `crawler-phase-field`
- parent: None; mutation: self-made adsorbed layer s (made by the bound polarity protein, kp*phi*rho; Langmuir adsorption) that excludes a cargo c (kappa); Camley et al. 2017 crawler at low contractility rho*=0.2 with weak noise eta=2 on rho; optional sector cut at cut_t (WORLD_P) and linear-kinetics twin (KIN=1)
- run: 161 frames x 200 steps x dt 0.001 = time 32; grid [256, 256]; wall 1018s; status ok
- command: `python -m labkit.run collective/contrib/c39-crawl-long-wip/world.py --out collective/contrib/c39-crawl-long-wip/pack/seed2 --seeds 2 --frames 160 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 1, mean 2.2, max 24; occupancy final 0.29
- tracks: 32; persistent (alive >= 50% of run): 1; longest 109 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.11 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 26.4/time; max body lengths 4.1
- replication (lineage window K = 20 frames = time 4, default): splits 1, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 6, merge/split ratio 6, nucleations 0
- channel total drift (end/start - 1): [-0.032, -0.7347, -0.7076, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 31 at frame 106: holes 0, rim-vs-core 0.13, rim-vs-outside 1.02, heterogeneity 0.21; core [1.0, 0.203, 0.205, 0.122, 0.149] rim [0.978, 0.281, 0.276, 0.121, 0.217]
  - track 3 at frame 26: holes 0, rim-vs-core 0.11, rim-vs-outside 1.17, heterogeneity 0.10; core [1.0, 0.599, 0.604, 0.129, 0.13] rim [0.943, 0.593, 0.565, 0.211, 0.111]
  - track 21 at frame 16: holes 0, rim-vs-core 0.34, rim-vs-outside 1.34, heterogeneity 0.12; core [0.999, 0.902, 0.909, 0.077, 0.094] rim [0.866, 0.896, 0.783, 0.359, 0.054]
  - track 19 at frame 15: holes 0, rim-vs-core 0.28, rim-vs-outside 1.23, heterogeneity 0.11; core [1.0, 0.752, 0.759, 0.089, 0.088] rim [0.883, 0.745, 0.664, 0.319, 0.06]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 9 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial phi (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.956, rim/outside 11.6 (aggregate of 9 individuals; 0/9 membrane-like individually; rim level 0.956)
  - radial rho (polarity, inside): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.35, rim/outside 6.67 (aggregate of 9 individuals; 5/9 membrane-like individually; rim level 0.439)
  - radial s (layer species): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 2.17, rim/outside 5.79 (aggregate of 9 individuals; 3/9 membrane-like individually; rim level 0.292)  MEMBRANE-LIKE
  - radial c (cargo): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.17, rim/outside 2.86 (aggregate of 9 individuals; 4/9 membrane-like individually; rim level 0.157)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s (layer species)
- membrane-like channels per top track at mid-life: #31 (t=21.2, R_eq 78.54): ['rho (polarity, inside)', 'c (cargo)']; #3 (t=5.2, R_eq 33.55): ['s (layer species)']; #21 (t=3.2, R_eq 18.19): ['s (layer species)']; #19 (t=3, R_eq 23.12): ['s (layer species)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: for 5 of 9 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
