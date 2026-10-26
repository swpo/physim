# Evidence pack: wavepin-crawler-layer-noise (seed 55)

- world: `../../../20261026T1042-c39-crawlers-noise-long-claim/world.py`, family `crawler-phase-field`
- parent: None; mutation: self-made adsorbed layer s (made by the bound polarity protein, kp*phi*rho; Langmuir adsorption) that excludes a cargo c (kappa); Camley et al. 2017 crawler at low contractility rho*=0.2 with weak noise eta=2 on rho; optional sector cut at cut_t (WORLD_P) and linear-kinetics twin (KIN=1)
- run: 161 frames x 200 steps x dt 0.001 = time 32; grid [256, 256]; wall 843s; status ok
- command: `python -m labkit.run collective/contrib/20261026T1042-c39-crawlers-noise-long-claim/world.py --out collective/contrib/20261026T1735-c45-review-crawlers-long/rerun/seed55 --seeds 55 --frames 160 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 1, mean 2.1, max 24; occupancy final 0.31
- tracks: 30; persistent (alive >= 50% of run): 1; longest 101 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.04 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 25.9/time; max body lengths 3.6
- replication (lineage window K = 20 frames = time 4, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 6, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [0.0202, -0.7285, -0.7005, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 29 at frame 110: holes 0, rim-vs-core 0.17, rim-vs-outside 1.03, heterogeneity 0.21; core [1.0, 0.199, 0.201, 0.13, 0.137] rim [0.973, 0.305, 0.299, 0.117, 0.228]
  - track 11 at frame 30: holes 0, rim-vs-core 0.23, rim-vs-outside 1.18, heterogeneity 0.11; core [1.0, 0.657, 0.664, 0.111, 0.175] rim [0.9, 0.662, 0.603, 0.306, 0.131]
  - track 13 at frame 26: holes 0, rim-vs-core 0.29, rim-vs-outside 1.24, heterogeneity 0.12; core [1.0, 0.767, 0.776, 0.099, 0.159] rim [0.886, 0.758, 0.679, 0.34, 0.105]
  - track 27 at frame 34: holes 0, rim-vs-core 0.22, rim-vs-outside 1.08, heterogeneity 0.22; core [1.0, 0.236, 0.239, 0.137, 0.11] rim [0.965, 0.393, 0.384, 0.147, 0.166]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 9 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial phi (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.998, rim/outside 21.9 (aggregate of 9 individuals; 0/9 membrane-like individually; rim level 0.998)
  - radial rho (polarity, inside): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.61, rim/outside 13.4 (aggregate of 9 individuals; 6/9 membrane-like individually; rim level 0.438)  MEMBRANE-LIKE
  - radial s (layer species): peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 1.99, rim/outside 7.82 (aggregate of 9 individuals; 3/9 membrane-like individually; rim level 0.278)  MEMBRANE-LIKE
  - radial c (cargo): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.2, rim/outside 2.52 (aggregate of 9 individuals; 4/9 membrane-like individually; rim level 0.183)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): rho (polarity, inside), s (layer species)
- membrane-like channels per top track at mid-life: #29 (t=22, R_eq 80.18): ['rho (polarity, inside)', 'c (cargo)']; #11 (t=6, R_eq 27.37): ['s (layer species)']; #13 (t=5.2, R_eq 22.34): ['s (layer species)']; #27 (t=6.8, R_eq 70.83): ['rho (polarity, inside)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: for 5 of 9 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
