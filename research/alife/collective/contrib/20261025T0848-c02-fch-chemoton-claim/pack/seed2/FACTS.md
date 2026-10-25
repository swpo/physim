# Evidence pack: fch-pchemoton (seed 2)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T0848-c02-fch-chemoton-claim/world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 300 steps x dt 0.01 = time 600; grid [192, 192]; wall 728s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0848-c02-fch-chemoton-claim/world.py --out collective/contrib/20261025T0848-c02-fch-chemoton-claim/pack/seed2 --seeds 2 --frames 200 --no-movie`
- segmentation: matter > 0.31 of robust range [-0.0207, 1.9701], min area 6 px

## Measurements
- components: final 5, mean 4.2, max 6; occupancy final 0.10
- tracks: 18; persistent (alive >= 50% of run): 4; longest 183 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 11.75 (1 = constant size)
- enclosures: components with a hole mean 2.25, final 2; holes at thresholds 0.2/0.35/0.5 final [4, 4, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 6, 4], H1 [6, 6, 3]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.1
- replication (lineage window K = 20 frames = time 60, default): splits 4, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 4, merge/split ratio 1, nucleations 3
- channel total drift (end/start - 1): [0.0891, 0.3642, -0.767]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 13 at frame 109: holes 3, rim-vs-core 0.13, rim-vs-outside 0.58, heterogeneity 0.18; core [0.824, 0.057, 0.44] rim [0.702, 0.057, 0.404]
  - track 14 at frame 133: holes 0, rim-vs-core 0.32, rim-vs-outside 0.58, heterogeneity 0.15; core [0.839, 0.008, 0.786] rim [0.692, 0.042, 0.504]
  - track 15 at frame 133: holes 1, rim-vs-core 0.19, rim-vs-outside 0.22, heterogeneity 0.06; core [0.768, 0.128, 0.037] rim [0.586, 0.115, 0.073]
  - track 2 at frame 54: holes 4, rim-vs-core 0.15, rim-vs-outside 0.44, heterogeneity 0.05; core [0.827, 0.985, 0.0] rim [0.681, 0.985, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 26 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.08, rim/outside 3.27 (aggregate of 26 individuals; 5/26 membrane-like individually; rim level 0.616)
  - radial precursor P: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.05, rim/outside 0.728 (aggregate of 26 individuals; 0/26 membrane-like individually; rim level 0.44)
  - radial catalyst K: peak at rho=1.15 (in the peak band 0.5-1.5), rim/core 4.66, rim/outside 2.26 (aggregate of 26 individuals; 10/26 membrane-like individually; rim level 0.241)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): catalyst K
- membrane-like channels per top track at mid-life: #13 (t=327, R_eq 18.88): ['catalyst K']; #14 (t=399, R_eq 19.64, ring): ['amphiphile u+1', 'catalyst K']; #15 (t=399, R_eq 13.32, ring): none; #2 (t=162, R_eq 20.51): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 13 of 26 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
