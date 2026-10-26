# Evidence pack: wavepin-crawler-layer-noise (seed 1)

- world: `../world4.py`, family `crawler-phase-field`
- parent: None; mutation: self-made adsorbed layer s (made by the bound polarity protein, kp*phi*rho; Langmuir adsorption) that excludes a cargo c (kappa); Camley et al. 2017 crawler at low contractility rho*=0.2 with weak noise eta=2 on rho; optional sector cut at cut_t (WORLD_P) and linear-kinetics twin (KIN=1)
- run: 81 frames x 200 steps x dt 0.001 = time 16; grid [256, 256]; wall 409s; status ok
- command: `python -m labkit.run collective/contrib/wip-c31/world4.py --out collective/contrib/wip-c31/pack4_nosrc_s1 --seeds 1 --frames 80 --no-movie`
- segmentation: matter > 0.50 of robust range [0.0, 1.0], min area 6 px

## Measurements
- components: final 1, mean 3.5, max 32; occupancy final 0.27
- tracks: 36; persistent (alive >= 50% of run): 2; longest 70 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.27 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 3 long-lived tracks moved >= 1 body length; max speed 24.1/time; max body lengths 3.6
- replication (lineage window K = 20 frames = time 4, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 4, merge/split ratio n/a, nucleations 0
- channel total drift (end/start - 1): [-0.1113, -0.8012, -0.7812, None, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 32 at frame 41: holes 0, rim-vs-core 0.17, rim-vs-outside 1.09, heterogeneity 0.20; core [1.0, 0.331, 0.337, 0.0, 0.569] rim [0.946, 0.448, 0.432, 0.0, 0.504]
  - track 34 at frame 55: holes 0, rim-vs-core 0.11, rim-vs-outside 1.04, heterogeneity 0.21; core [1.0, 0.393, 0.4, 0.0, 0.6] rim [0.964, 0.342, 0.333, 0.0, 0.661]
  - track 24 at frame 17: holes 0, rim-vs-core 0.15, rim-vs-outside 1.14, heterogeneity 0.06; core [1.0, 0.547, 0.557, 0.0, 0.466] rim [0.921, 0.564, 0.529, 0.0, 0.341]
  - track 2 at frame 15: holes 0, rim-vs-core 0.14, rim-vs-outside 1.10, heterogeneity 0.17; core [1.0, 0.479, 0.487, 0.0, 0.385] rim [0.923, 0.518, 0.487, 0.0, 0.271]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 15 components >= 12 px at frames [13, 27, 40, 53, 67, 80]):
  - radial phi (cell): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.955, rim/outside 8.35 (aggregate of 15 individuals; 0/15 membrane-like individually; rim level 0.955)
  - radial rho (polarity, inside): peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 1.46, rim/outside 7.37 (aggregate of 15 individuals; 10/15 membrane-like individually; rim level 0.495)
  - radial s (layer species): flat profile (no radial structure; level 0; aggregate of 15 individuals)
  - radial c (cargo): peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.897, rim/outside 1.6 (aggregate of 15 individuals; 0/15 membrane-like individually; rim level 0.514)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #32 (t=8.2, R_eq 51.42): ['rho (polarity, inside)']; #34 (t=11, R_eq 51.85): ['rho (polarity, inside)']; #24 (t=3.4, R_eq 34.23): none; #2 (t=3, R_eq 36.82): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: for 1 of 15 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
