# Evidence pack: particle-lenia-turnover (seed 7)

- world: `../../world.py`, family `particle-lenia`
- parent: collective/contrib/20261025T1300-c13-particle-lenia-vesicles/world.py; mutation: particle turnover: random feed of new particles plus decay of every particle (c13)
- run: 151 frames x 100 steps x dt 0.1 = time 1500; grid [128, 128]; wall 1212s; status ok
- command: `python -m labkit.run scratch/c14/rev_pl/world.py --out scratch/c14/rev_pl/pack/seed7 --seeds 7 --spf 100 --frames 150 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0001, 0.9462], min area 6 px

## Measurements
- components: final 66, mean 57.2, max 86; occupancy final 0.24
- tracks: 566; persistent (alive >= 50% of run): 19; longest 124 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 13.29 (1 = constant size)
- enclosures: components with a hole mean 17.99, final 33; holes at thresholds 0.2/0.35/0.5 final [3, 33, 3]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [69, 66, 49], H1 [80, 8, 0]
- motion: 143 long-lived tracks moved >= 1 body length; max speed 0.219/time; max body lengths 16.6
- replication (lineage window K = 20 frames = time 200, default): splits 80, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 95, merge/split ratio 1.19, nucleations 237
- channel total drift (end/start - 1): [-0.0363, -0.0363, 1.506]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 177 at frame 89: holes 0, rim-vs-core 0.20, rim-vs-outside 0.53, heterogeneity 0.21; core [0.717, 0.162, 0.682] rim [0.617, 0.315, 0.607]
  - track 182 at frame 89: holes 1, rim-vs-core 0.30, rim-vs-outside 0.44, heterogeneity 0.18; core [0.736, 0.155, 0.73] rim [0.478, 0.222, 0.585]
  - track 171 at frame 87: holes 0, rim-vs-core 0.22, rim-vs-outside 0.49, heterogeneity 0.20; core [0.655, 0.136, 0.578] rim [0.556, 0.325, 0.521]
  - track 261 at frame 101: holes 0, rim-vs-core 0.30, rim-vs-outside 0.55, heterogeneity 0.19; core [0.736, 0.145, 0.649] rim [0.548, 0.333, 0.509]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 355 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial particle density: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.53, rim/outside 6.13 (aggregate of 355 individuals; 217/355 membrane-like individually; rim level 0.694)  MEMBRANE-LIKE
  - radial U field: peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 6.54, rim/outside 0.772 (aggregate of 355 individuals; 0/355 membrane-like individually; rim level 0.518)
  - radial G(U): peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.96, rim/outside 25.8 (aggregate of 355 individuals; 260/355 membrane-like individually; rim level 0.677)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): particle density, G(U)
- membrane-like channels per top track at mid-life: #177 (t=890, R_eq 5.59): ['G(U)']; #182 (t=890, R_eq 4.18): ['G(U)']; #171 (t=870, R_eq 4.37): ['particle density', 'G(U)']; #261 (t=1010, R_eq 4.58): ['G(U)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 116 of 355 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
