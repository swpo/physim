# Evidence pack: wavepin-crawler-layer-noise (seed 7)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T0406-c31-crawlers-from-noise-claim/world.py`, family `crawler-phase-field`
- parent: None; mutation: self-made adsorbed layer s (made by the bound polarity protein, kp*phi*rho; Langmuir adsorption) that excludes a cargo c (kappa); Camley et al. 2017 crawler at low contractility rho*=0.2 with weak noise eta=2 on rho; optional sector cut at cut_t (WORLD_P) and linear-kinetics twin (KIN=1)
- run: 71 frames x 200 steps x dt 0.001 = time 14; grid [256, 256]; wall 615s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0406-c31-crawlers-from-noise-claim/world.py --out /tmp/claude-0/-home-user-physim/60e094ad-5b43-583e-8321-7611b63df58f/scratchpad/rev5/rs0.3 --seeds 7 --frames 70 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 6, mean 7.0, max 29; occupancy final 0.20
- tracks: 30; persistent (alive >= 50% of run): 6; longest 71 frames; alive start-to-end: 5
- size of persistent tracks: max/min area ratio 1.77 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [6, 6, 6], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.1
- replication (lineage window K = 20 frames = time 4, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [-0.3257, -0.4778, -0.4169, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 35: holes 0, rim-vs-core 0.07, rim-vs-outside 1.27, heterogeneity 0.12; core [1.0, 0.566, 0.583, 0.13, 0.53] rim [0.963, 0.563, 0.558, 0.179, 0.519]
  - track 14 at frame 35: holes 0, rim-vs-core 0.24, rim-vs-outside 1.24, heterogeneity 0.13; core [1.0, 0.671, 0.691, 0.108, 0.489] rim [0.902, 0.668, 0.62, 0.281, 0.377]
  - track 18 at frame 35: holes 0, rim-vs-core 0.42, rim-vs-outside 1.39, heterogeneity 0.15; core [0.999, 0.915, 0.937, 0.079, 0.558] rim [0.863, 0.915, 0.814, 0.35, 0.299]
  - track 21 at frame 35: holes 0, rim-vs-core 0.43, rim-vs-outside 1.29, heterogeneity 0.15; core [1.0, 0.818, 0.841, 0.093, 0.586] rim [0.865, 0.813, 0.723, 0.372, 0.317]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 37 components >= 12 px at frames [12, 23, 35, 47, 58, 70]):
  - radial phi (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 12.5 (aggregate of 37 individuals; 0/37 membrane-like individually; rim level 1)
  - radial rho (polarity, inside): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 12.1 (aggregate of 37 individuals; 0/37 membrane-like individually; rim level 0.777)
  - radial s (layer species): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 4.58, rim/outside 9.93 (aggregate of 37 individuals; 37/37 membrane-like individually; rim level 0.553)  MEMBRANE-LIKE
  - radial c (cargo): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.24, rim/outside 6.97 (aggregate of 37 individuals; 2/37 membrane-like individually; rim level 0.638)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s (layer species)
- membrane-like channels per top track at mid-life: #0 (t=7, R_eq 40.29): ['s (layer species)', 'c (cargo)']; #14 (t=7, R_eq 29.68): ['s (layer species)']; #18 (t=7, R_eq 18.45): ['s (layer species)']; #21 (t=7, R_eq 21.95): ['s (layer species)']

## Warnings
- none

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
