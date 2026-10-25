# Evidence pack: particle-lenia (seed 3)

- world: `../../../20261025T1300-c13-particle-lenia-vesicles/world.py`, family `particle-lenia`
- parent: new class (Mordvintsev et al. 2022, Particle Lenia); mutation: none (benchmark model, many particles in a periodic box)
- run: 151 frames x 100 steps x dt 0.1 = time 1500; grid [128, 128]; wall 873s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1300-c13-particle-lenia-vesicles/world.py --out collective/contrib/20261025T1500-c13-plenia-turnover-division/pack_closed --seeds 2 3 --spf 100 --frames 150 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.962], min area 6 px

## Measurements
- components: final 61, mean 55.3, max 84; occupancy final 0.22
- tracks: 659; persistent (alive >= 50% of run): 20; longest 136 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 12.00 (1 = constant size)
- enclosures: components with a hole mean 16.52, final 18; holes at thresholds 0.2/0.35/0.5 final [8, 18, 4]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [61, 53, 21], H1 [44, 3, 0]
- motion: 120 long-lived tracks moved >= 1 body length; max speed 0.163/time; max body lengths 15.6
- replication (lineage window K = 20 frames = time 200, default): splits 121, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 1, merges 142, merge/split ratio 1.17, nucleations 205
- channel total drift (end/start - 1): [0.0, 0.0, 1.7158]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 163 at frame 83: holes 0, rim-vs-core 0.26, rim-vs-outside 0.42, heterogeneity 0.22; core [0.689, 0.112, 0.423] rim [0.507, 0.297, 0.389]
  - track 103 at frame 69: holes 1, rim-vs-core 0.29, rim-vs-outside 0.41, heterogeneity 0.19; core [0.682, 0.172, 0.653] rim [0.496, 0.254, 0.448]
  - track 190 at frame 87: holes 1, rim-vs-core 0.39, rim-vs-outside 0.43, heterogeneity 0.20; core [0.726, 0.192, 0.681] rim [0.497, 0.274, 0.377]
  - track 398 at frame 96: holes 1, rim-vs-core 0.36, rim-vs-outside 0.38, heterogeneity 0.20; core [0.744, 0.19, 0.682] rim [0.523, 0.242, 0.397]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 337 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial particle density: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.51, rim/outside 6.27 (aggregate of 337 individuals; 210/337 membrane-like individually; rim level 0.685)  MEMBRANE-LIKE
  - radial U field: peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 5.4, rim/outside 0.788 (aggregate of 337 individuals; 1/337 membrane-like individually; rim level 0.521)
  - radial G(U): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.92, rim/outside 15.4 (aggregate of 337 individuals; 230/337 membrane-like individually; rim level 0.607)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): particle density, G(U)
- membrane-like channels per top track at mid-life: #163 (t=830, R_eq 4.62): ['particle density', 'G(U)']; #103 (t=690, R_eq 4.55, ring): ['particle density', 'G(U)']; #190 (t=870, R_eq 4.58, ring): ['particle density', 'G(U)']; #398 (t=960, R_eq 4.65, ring): ['particle density', 'G(U)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 121 of 337 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
