# Evidence pack: wavepin-crawler-layer-noise (seed 5)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T0406-c31-crawlers-from-noise-claim/world.py`, family `crawler-phase-field`
- parent: None; mutation: self-made adsorbed layer s (made by the bound polarity protein, kp*phi*rho; Langmuir adsorption) that excludes a cargo c (kappa); Camley et al. 2017 crawler at low contractility rho*=0.2 with weak noise eta=2 on rho; optional sector cut at cut_t (WORLD_P) and linear-kinetics twin (KIN=1)
- run: 81 frames x 200 steps x dt 0.001 = time 16; grid [256, 256]; wall 676s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0406-c31-crawlers-from-noise-claim/world.py --out /tmp/claude-0/-home-user-physim/60e094ad-5b43-583e-8321-7611b63df58f/scratchpad/rev2/s5 --seeds 5 --frames 80 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 2, mean 4.3, max 25; occupancy final 0.30
- tracks: 30; persistent (alive >= 50% of run): 3; longest 81 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 1.52 (1 = constant size)
- enclosures: components with a hole mean 0.04, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [2, 2, 2], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 34.7/time; max body lengths 1.6
- replication (lineage window K = 20 frames = time 4, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 5, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [-0.0077, -0.6887, -0.6563, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 23 at frame 40: holes 0, rim-vs-core 0.47, rim-vs-outside 1.33, heterogeneity 0.14; core [0.998, 0.946, 0.957, 0.076, 0.298] rim [0.832, 0.941, 0.801, 0.444, 0.123]
  - track 1 at frame 29: holes 0, rim-vs-core 0.19, rim-vs-outside 1.14, heterogeneity 0.11; core [1.0, 0.587, 0.597, 0.107, 0.203] rim [0.911, 0.586, 0.543, 0.264, 0.165]
  - track 0 at frame 27: holes 0, rim-vs-core 0.18, rim-vs-outside 1.23, heterogeneity 0.12; core [1.0, 0.694, 0.706, 0.089, 0.196] rim [0.925, 0.697, 0.656, 0.241, 0.151]
  - track 16 at frame 15: holes 0, rim-vs-core 0.13, rim-vs-outside 1.09, heterogeneity 0.22; core [1.0, 0.419, 0.427, 0.119, 0.076] rim [0.934, 0.503, 0.479, 0.175, 0.104]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 22 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial phi (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.97, rim/outside 7.74 (aggregate of 22 individuals; 0/22 membrane-like individually; rim level 0.97)
  - radial rho (polarity, inside): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.11, rim/outside 7.6 (aggregate of 22 individuals; 5/22 membrane-like individually; rim level 0.625)
  - radial s (layer species): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 3.82, rim/outside 7.13 (aggregate of 22 individuals; 19/22 membrane-like individually; rim level 0.467)  MEMBRANE-LIKE
  - radial c (cargo): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.19, rim/outside 3.52 (aggregate of 22 individuals; 4/22 membrane-like individually; rim level 0.225)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s (layer species)
- membrane-like channels per top track at mid-life: #23 (t=8, R_eq 16.36): ['s (layer species)']; #1 (t=5.8, R_eq 30.55): ['s (layer species)']; #0 (t=5.4, R_eq 24.32): ['s (layer species)']; #16 (t=3, R_eq 44.76): ['rho (polarity, inside)', 's (layer species)', 'c (cargo)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: for 2 of 22 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
