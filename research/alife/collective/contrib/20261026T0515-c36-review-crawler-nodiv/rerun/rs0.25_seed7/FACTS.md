# Evidence pack: wavepin-crawler-layer-noise (seed 7)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261026T0406-c31-crawlers-from-noise-claim/world.py`, family `crawler-phase-field`
- parent: None; mutation: self-made adsorbed layer s (made by the bound polarity protein, kp*phi*rho; Langmuir adsorption) that excludes a cargo c (kappa); Camley et al. 2017 crawler at low contractility rho*=0.2 with weak noise eta=2 on rho; optional sector cut at cut_t (WORLD_P) and linear-kinetics twin (KIN=1)
- run: 71 frames x 200 steps x dt 0.001 = time 14; grid [256, 256]; wall 618s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0406-c31-crawlers-from-noise-claim/world.py --out /tmp/claude-0/-home-user-physim/60e094ad-5b43-583e-8321-7611b63df58f/scratchpad/rev5/rs0.25 --seeds 7 --frames 70 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 2, mean 5.3, max 29; occupancy final 0.25
- tracks: 35; persistent (alive >= 50% of run): 4; longest 71 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 3.70 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [2, 2, 2], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 23.9/time; max body lengths 1.3
- replication (lineage window K = 20 frames = time 4, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 6, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [-0.1712, -0.699, -0.6651, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 18 at frame 35: holes 0, rim-vs-core 0.36, rim-vs-outside 1.23, heterogeneity 0.13; core [0.999, 0.771, 0.795, 0.084, 0.281] rim [0.863, 0.775, 0.69, 0.369, 0.153]
  - track 3 at frame 21: holes 0, rim-vs-core 0.42, rim-vs-outside 1.37, heterogeneity 0.13; core [0.998, 0.969, 0.984, 0.064, 0.178] rim [0.834, 0.97, 0.841, 0.407, 0.076]
  - track 2 at frame 21: holes 0, rim-vs-core 0.54, rim-vs-outside 1.29, heterogeneity 0.13; core [0.994, 0.981, 0.99, 0.066, 0.179] rim [0.792, 0.982, 0.818, 0.513, 0.047]
  - track 29 at frame 19: holes 0, rim-vs-core 0.32, rim-vs-outside 1.17, heterogeneity 0.11; core [1.0, 0.716, 0.738, 0.081, 0.169] rim [0.867, 0.715, 0.64, 0.342, 0.098]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 25 components >= 12 px at frames [12, 23, 35, 47, 58, 70]):
  - radial phi (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.985, rim/outside 18 (aggregate of 25 individuals; 0/25 membrane-like individually; rim level 0.985)
  - radial rho (polarity, inside): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.09, rim/outside 17.6 (aggregate of 25 individuals; 6/25 membrane-like individually; rim level 0.686)
  - radial s (layer species): peak at rho=0.95 (in the peak band 0.5-1.5), rim/core 4.83, rim/outside 10.9 (aggregate of 25 individuals; 21/25 membrane-like individually; rim level 0.53)  MEMBRANE-LIKE
  - radial c (cargo): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.13, rim/outside 5.37 (aggregate of 25 individuals; 1/25 membrane-like individually; rim level 0.22)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): s (layer species)
- membrane-like channels per top track at mid-life: #18 (t=7, R_eq 19.31): ['s (layer species)']; #3 (t=4.2, R_eq 14.07): ['s (layer species)']; #2 (t=4.2, R_eq 13.79): ['s (layer species)']; #29 (t=3.8, R_eq 21.35): ['s (layer species)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
