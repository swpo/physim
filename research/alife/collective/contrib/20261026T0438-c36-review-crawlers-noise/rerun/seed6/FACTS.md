# Evidence pack: wavepin-crawler-layer-noise (seed 6)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T0406-c31-crawlers-from-noise-claim/world.py`, family `crawler-phase-field`
- parent: None; mutation: self-made adsorbed layer s (made by the bound polarity protein, kp*phi*rho; Langmuir adsorption) that excludes a cargo c (kappa); Camley et al. 2017 crawler at low contractility rho*=0.2 with weak noise eta=2 on rho; optional sector cut at cut_t (WORLD_P) and linear-kinetics twin (KIN=1)
- run: 81 frames x 200 steps x dt 0.001 = time 16; grid [256, 256]; wall 678s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0406-c31-crawlers-from-noise-claim/world.py --out /tmp/claude-0/-home-user-physim/60e094ad-5b43-583e-8321-7611b63df58f/scratchpad/rev2/s6 --seeds 6 --frames 80 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 2, mean 4.9, max 22; occupancy final 0.31
- tracks: 30; persistent (alive >= 50% of run): 2; longest 81 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 1.22 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [2, 2, 2], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 25.4/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 4, default): splits 1, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 6, merge/split ratio 6, nucleations 0
- channel total drift (end/start - 1): [0.0211, -0.6929, -0.6619, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 14 at frame 40: holes 0, rim-vs-core 0.38, rim-vs-outside 1.26, heterogeneity 0.14; core [0.999, 0.812, 0.835, 0.083, 0.324] rim [0.862, 0.805, 0.714, 0.376, 0.175]
  - track 16 at frame 25: holes 0, rim-vs-core 0.45, rim-vs-outside 1.33, heterogeneity 0.13; core [0.998, 0.942, 0.961, 0.07, 0.22] rim [0.831, 0.937, 0.803, 0.431, 0.093]
  - track 23 at frame 19: holes 0, rim-vs-core 0.22, rim-vs-outside 1.11, heterogeneity 0.10; core [1.0, 0.577, 0.594, 0.099, 0.171] rim [0.9, 0.575, 0.532, 0.277, 0.131]
  - track 19 at frame 17: holes 0, rim-vs-core 0.20, rim-vs-outside 1.18, heterogeneity 0.11; core [1.0, 0.656, 0.675, 0.087, 0.162] rim [0.909, 0.657, 0.615, 0.249, 0.125]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 23 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial phi (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.981, rim/outside 13.2 (aggregate of 23 individuals; 0/23 membrane-like individually; rim level 0.981)
  - radial rho (polarity, inside): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.07, rim/outside 13.3 (aggregate of 23 individuals; 5/23 membrane-like individually; rim level 0.668)
  - radial s (layer species): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 4.72, rim/outside 8.95 (aggregate of 23 individuals; 17/23 membrane-like individually; rim level 0.512)  MEMBRANE-LIKE
  - radial c (cargo): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.11, rim/outside 3.78 (aggregate of 23 individuals; 1/23 membrane-like individually; rim level 0.224)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s (layer species)
- membrane-like channels per top track at mid-life: #14 (t=8, R_eq 18.81): ['s (layer species)']; #16 (t=5, R_eq 15.72): ['s (layer species)']; #23 (t=3.8, R_eq 29.77): ['s (layer species)']; #19 (t=3.4, R_eq 24.79): ['s (layer species)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: for 4 of 23 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
