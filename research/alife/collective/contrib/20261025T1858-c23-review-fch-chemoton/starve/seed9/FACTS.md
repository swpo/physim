# Evidence pack: fch-pchemoton-starve (seed 9)

- world: `../../../../20261025T0848-c02-fch-chemoton-claim/world_starve.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 300 steps x dt 0.01 = time 600; grid [192, 192]; wall 333s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0848-c02-fch-chemoton-claim/world_starve.py --out collective/contrib/20261025T1858-c23-review-fch-chemoton/starve/seed9 --seeds 9 --frames 200 --no-movie`
- segmentation: matter > 0.31 of robust range [-0.0239, 1.9614], min area 6 px

## Measurements
- components: final 3, mean 3.6, max 7; occupancy final 0.03
- tracks: 32; persistent (alive >= 50% of run): 2; longest 124 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.44 (1 = constant size)
- enclosures: components with a hole mean 2.46, final 3; holes at thresholds 0.2/0.35/0.5 final [0, 3, 2]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [5, 5, 3], H1 [3, 3, 2]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.1
- replication (lineage window K = 20 frames = time 60, default): splits 10, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 10, merge/split ratio 1, nucleations 3
- channel total drift (end/start - 1): [-0.9045, -0.4168, -0.9967]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 64: holes 5, rim-vs-core 0.18, rim-vs-outside 0.58, heterogeneity 0.17; core [0.874, 0.087, 0.274] rim [0.749, 0.072, 0.4]
  - track 12 at frame 69: holes 3, rim-vs-core 0.18, rim-vs-outside 0.61, heterogeneity 0.18; core [0.909, 0.089, 0.32] rim [0.765, 0.069, 0.419]
  - track 17 at frame 108: holes 0, rim-vs-core 0.17, rim-vs-outside 0.47, heterogeneity 0.08; core [0.918, 0.093, 0.18] rim [0.76, 0.1, 0.132]
  - track 18 at frame 108: holes 1, rim-vs-core 0.19, rim-vs-outside 0.22, heterogeneity 0.05; core [0.831, 0.05, 0.019] rim [0.639, 0.053, 0.033]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 22 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.29, rim/outside 5.68 (aggregate of 22 individuals; 8/22 membrane-like individually; rim level 0.731)
  - radial precursor P: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.6, rim/outside 0.679 (aggregate of 22 individuals; 0/22 membrane-like individually; rim level 0.259)
  - radial catalyst K: peak at rho=1.15 (in the peak band 0.5-1.5), rim/core 1.66, rim/outside 2.57 (aggregate of 22 individuals; 9/22 membrane-like individually; rim level 0.148)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): catalyst K
- membrane-like channels per top track at mid-life: #2 (t=192, R_eq 21.8): ['catalyst K']; #12 (t=207, R_eq 20.43): ['catalyst K']; #17 (t=324, R_eq 19.1, ring): ['amphiphile u+1', 'catalyst K']; #18 (t=324, R_eq 12.7, ring): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 12 of 22 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
