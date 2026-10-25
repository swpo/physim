# Evidence pack: fch-pchemoton-res15 (seed 0)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T1048-c02-chemoton-res15/world_res15.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 600 steps x dt 0.005 = time 600; grid [288, 288]; wall 3198s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1048-c02-chemoton-res15/world_res15.py --out collective/contrib/20261025T1048-c02-chemoton-res15/pack_res15/seed0 --seeds 0 --frames 200 --no-movie`
- segmentation: matter > 0.31 of robust range [-0.0207, 1.988], min area 6 px

## Measurements
- components: final 4, mean 3.2, max 7; occupancy final 0.08
- tracks: 20; persistent (alive >= 50% of run): 2; longest 156 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.68 (1 = constant size)
- enclosures: components with a hole mean 1.12, final 1; holes at thresholds 0.2/0.35/0.5 final [0, 1, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [5, 4, 3], H1 [4, 3, 1]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.0
- replication (lineage window K = 20 frames = time 60, default): splits 6, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 4, merge/split ratio 0.667, nucleations 2
- channel total drift (end/start - 1): [-0.2939, 0.6259, -0.8642]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 15 at frame 123: holes 0, rim-vs-core 0.18, rim-vs-outside 0.47, heterogeneity 0.05; core [0.949, 0.996, 0.0] rim [0.769, 0.996, 0.0]
  - track 16 at frame 123: holes 0, rim-vs-core 0.29, rim-vs-outside 0.13, heterogeneity 0.06; core [0.863, 0.998, 0.0] rim [0.578, 0.998, 0.0]
  - track 13 at frame 81: holes 0, rim-vs-core 0.43, rim-vs-outside 0.65, heterogeneity 0.15; core [0.934, 0.0, 0.997] rim [0.765, 0.032, 0.604]
  - track 14 at frame 81: holes 2, rim-vs-core 0.15, rim-vs-outside 0.21, heterogeneity 0.07; core [0.761, 0.119, 0.049] rim [0.635, 0.093, 0.127]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 20 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.926, rim/outside 3.04 (aggregate of 20 individuals; 0/20 membrane-like individually; rim level 0.698)
  - radial precursor P: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.02, rim/outside 0.821 (aggregate of 20 individuals; 0/20 membrane-like individually; rim level 0.623)
  - radial catalyst K: peak at rho=1.25 (in the peak band 0.5-1.5), rim/core 4.42, rim/outside 2.9 (aggregate of 20 individuals; 6/20 membrane-like individually; rim level 0.159)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): catalyst K
- membrane-like channels per top track at mid-life: #15 (t=369, R_eq 22.39, ring): none; #16 (t=369, R_eq 8.31): none; #13 (t=243, R_eq 31.46, ring): ['catalyst K']; #14 (t=243, R_eq 25.82): ['catalyst K']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 9 of 20 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
