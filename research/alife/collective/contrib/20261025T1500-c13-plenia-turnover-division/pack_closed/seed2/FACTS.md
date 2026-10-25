# Evidence pack: particle-lenia (seed 2)

- world: `../../../20261025T1300-c13-particle-lenia-vesicles/world.py`, family `particle-lenia`
- parent: new class (Mordvintsev et al. 2022, Particle Lenia); mutation: none (benchmark model, many particles in a periodic box)
- run: 151 frames x 100 steps x dt 0.1 = time 1500; grid [128, 128]; wall 1023s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1300-c13-particle-lenia-vesicles/world.py --out collective/contrib/20261025T1500-c13-plenia-turnover-division/pack_closed --seeds 2 3 --spf 100 --frames 150 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 0.9502], min area 6 px

## Measurements
- components: final 58, mean 55.0, max 80; occupancy final 0.22
- tracks: 623; persistent (alive >= 50% of run): 20; longest 151 frames; alive start-to-end: 1
- size of persistent tracks: max/min area ratio 12.22 (1 = constant size)
- enclosures: components with a hole mean 23.54, final 17; holes at thresholds 0.2/0.35/0.5 final [14, 17, 2]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [61, 58, 11], H1 [39, 2, 0]
- motion: 125 long-lived tracks moved >= 1 body length; max speed 0.172/time; max body lengths 10.5
- replication (lineage window K = 20 frames = time 200, default): splits 121, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 139, merge/split ratio 1.15, nucleations 181
- channel total drift (end/start - 1): [0.0, 0.0, 1.2717]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 32 at frame 76: holes 0, rim-vs-core 0.28, rim-vs-outside 0.35, heterogeneity 0.22; core [0.668, 0.194, 0.518] rim [0.523, 0.307, 0.305]
  - track 107 at frame 77: holes 1, rim-vs-core 0.27, rim-vs-outside 0.44, heterogeneity 0.21; core [0.733, 0.267, 0.646] rim [0.555, 0.303, 0.441]
  - track 155 at frame 84: holes 1, rim-vs-core 0.35, rim-vs-outside 0.45, heterogeneity 0.20; core [0.676, 0.272, 0.71] rim [0.549, 0.273, 0.387]
  - track 422 at frame 117: holes 1, rim-vs-core 0.32, rim-vs-outside 0.48, heterogeneity 0.20; core [0.716, 0.216, 0.687] rim [0.542, 0.277, 0.431]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 318 components >= 12 px at frames [25, 50, 76, 100, 125, 150]):
  - radial particle density: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.56, rim/outside 5.84 (aggregate of 318 individuals; 211/318 membrane-like individually; rim level 0.653)  MEMBRANE-LIKE
  - radial U field: peak at rho=2.05 (OUTSIDE the peak band 0.5-1.5), rim/core 5.58, rim/outside 0.834 (aggregate of 318 individuals; 0/318 membrane-like individually; rim level 0.555)
  - radial G(U): peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.97, rim/outside 21.5 (aggregate of 318 individuals; 223/318 membrane-like individually; rim level 0.631)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): particle density, G(U)
- membrane-like channels per top track at mid-life: #32 (t=760, R_eq 4.85, ring): ['particle density', 'G(U)']; #107 (t=770, R_eq 4.37, ring): ['particle density', 'G(U)']; #155 (t=840, R_eq 4.48, ring): ['particle density', 'G(U)']; #422 (t=1170, R_eq 4.62, ring): ['particle density', 'G(U)']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 161 of 318 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, particles.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
