# Evidence pack: particle-lenia (seed 1)

- world: `../world.py`, family `particle-lenia`
- parent: new class (Mordvintsev et al. 2022, Particle Lenia); mutation: none (benchmark model, many particles in a periodic box)
- run: 121 frames x 50 steps x dt 0.1 = time 600; grid [128, 128]; wall 418s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1300-c13-particle-lenia-vesicles/world.py --out collective/contrib/20261025T1300-c13-particle-lenia-vesicles/pack --seeds 1 --frames 120 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0001, 0.9358], min area 6 px

## Measurements
- components: final 57, mean 54.8, max 85; occupancy final 0.22
- tracks: 396; persistent (alive >= 50% of run): 37; longest 119 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 13.83 (1 = constant size)
- enclosures: components with a hole mean 20.15, final 25; holes at thresholds 0.2/0.35/0.5 final [9, 25, 3]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [63, 55, 23], H1 [51, 4, 0]
- motion: 89 long-lived tracks moved >= 1 body length; max speed 0.235/time; max body lengths 8.9
- replication (lineage window K = 20 frames = time 100, default): splits 56, persistent splits 4 (0 more failed only because the siblings re-merged within K), max generation 1, merges 76, merge/split ratio 1.36, nucleations 129
- channel total drift (end/start - 1): [0.0, 0.0, 1.5563]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 100 at frame 62: holes 0, rim-vs-core 0.28, rim-vs-outside 0.37, heterogeneity 0.21; core [0.711, 0.247, 0.617] rim [0.527, 0.276, 0.414]
  - track 102 at frame 62: holes 1, rim-vs-core 0.31, rim-vs-outside 0.33, heterogeneity 0.22; core [0.641, 0.192, 0.508] rim [0.497, 0.321, 0.272]
  - track 87 at frame 59: holes 1, rim-vs-core 0.23, rim-vs-outside 0.40, heterogeneity 0.22; core [0.698, 0.223, 0.545] rim [0.524, 0.305, 0.413]
  - track 199 at frame 78: holes 1, rim-vs-core 0.20, rim-vs-outside 0.39, heterogeneity 0.21; core [0.663, 0.084, 0.368] rim [0.53, 0.21, 0.436]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 330 components >= 12 px at frames [20, 40, 61, 80, 100, 120]):
  - radial particle density: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.48, rim/outside 5.78 (aggregate of 330 individuals; 202/330 membrane-like individually; rim level 0.663)
  - radial U field: peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 5.96, rim/outside 0.829 (aggregate of 330 individuals; 0/330 membrane-like individually; rim level 0.545)
  - radial G(U): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.89, rim/outside 22.5 (aggregate of 330 individuals; 221/330 membrane-like individually; rim level 0.653)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): G(U)
- membrane-like channels per top track at mid-life: #100 (t=310, R_eq 4.48, ring): ['particle density', 'G(U)']; #102 (t=310, R_eq 4.85, ring): ['particle density', 'G(U)']; #87 (t=295, R_eq 4.22, ring): ['particle density', 'G(U)']; #199 (t=390, R_eq 4.48, ring): ['particle density', 'G(U)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 137 of 330 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
