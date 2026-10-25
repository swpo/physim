# Evidence pack: fch-pchemoton-starve (seed 31)

- world: `../../20261025T0848-c02-fch-chemoton-claim/world_starve.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 300 steps x dt 0.01 = time 600; grid [192, 192]; wall 486s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0848-c02-fch-chemoton-claim/world_starve.py --out collective/contrib/20261025T1033-c10-review-chemoton/starve --seeds 31 --frames 200 --no-movie`
- segmentation: matter > 0.32 of robust range [-0.0257, 1.9326], min area 6 px

## Measurements
- components: final 4, mean 4.1, max 7; occupancy final 0.02
- tracks: 13; persistent (alive >= 50% of run): 4; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 5.50 (1 = constant size)
- enclosures: components with a hole mean 3.04, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [8, 8, 4], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.8
- replication (lineage window K = 20 frames = time 60, default): splits 3, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 3, merge/split ratio 1, nucleations 4
- channel total drift (end/start - 1): [-0.9054, -0.3738, -0.9948]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 101: holes 1, rim-vs-core 0.25, rim-vs-outside 0.63, heterogeneity 0.17; core [0.898, 0.005, 0.671] rim [0.738, 0.02, 0.476]
  - track 3 at frame 61: holes 5, rim-vs-core 0.21, rim-vs-outside 0.53, heterogeneity 0.16; core [0.843, 0.04, 0.546] rim [0.701, 0.064, 0.391]
  - track 2 at frame 61: holes 4, rim-vs-core 0.14, rim-vs-outside 0.58, heterogeneity 0.17; core [0.854, 0.062, 0.409] rim [0.719, 0.063, 0.423]
  - track 12 at frame 168: holes 1, rim-vs-core 0.17, rim-vs-outside 0.41, heterogeneity 0.05; core [0.868, 0.328, 0.0] rim [0.695, 0.327, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 25 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.22, rim/outside 12.8 (aggregate of 25 individuals; 7/25 membrane-like individually; rim level 0.698)
  - radial precursor P: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.34, rim/outside 0.792 (aggregate of 25 individuals; 0/25 membrane-like individually; rim level 0.369)
  - radial catalyst K: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.82, rim/outside 7.46 (aggregate of 25 individuals; 9/25 membrane-like individually; rim level 0.165)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): catalyst K
- membrane-like channels per top track at mid-life: #1 (t=303, R_eq 15.04, ring): ['amphiphile u+1', 'catalyst K']; #3 (t=183, R_eq 21.07): ['catalyst K']; #2 (t=183, R_eq 19.83): ['catalyst K']; #12 (t=504, R_eq 10.2, ring): ['amphiphile u+1']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 8 of 25 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
