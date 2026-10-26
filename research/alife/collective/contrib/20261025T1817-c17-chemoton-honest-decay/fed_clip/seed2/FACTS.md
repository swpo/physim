# Evidence pack: fch-pchemoton-clip (seed 2)

- world: `../../world_clip.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 300 steps x dt 0.01 = time 600; grid [192, 192]; wall 359s; status ok
- command: `python -m labkit.run world_clip.py --out fed_clip --seeds 0 2 --no-movie`
- segmentation: matter > 0.31 of robust range [-0.0208, 1.97], min area 6 px

## Measurements
- components: final 6, mean 4.8, max 6; occupancy final 0.09
- tracks: 23; persistent (alive >= 50% of run): 6; longest 140 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.21 (1 = constant size)
- enclosures: components with a hole mean 1.61, final 1; holes at thresholds 0.2/0.35/0.5 final [0, 1, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [6, 6, 3], H1 [4, 4, 2]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.2
- replication (lineage window K = 20 frames = time 60, default): splits 6, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 5, merge/split ratio 0.833, nucleations 3
- channel total drift (end/start - 1): [-0.1338, 0.4412, -0.7967]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 14 at frame 131: holes 0, rim-vs-core 0.33, rim-vs-outside 0.60, heterogeneity 0.15; core [0.855, 0.006, 0.812] rim [0.707, 0.04, 0.522]
  - track 15 at frame 131: holes 1, rim-vs-core 0.18, rim-vs-outside 0.19, heterogeneity 0.06; core [0.763, 0.118, 0.036] rim [0.585, 0.104, 0.076]
  - track 19 at frame 141: holes 0, rim-vs-core 0.16, rim-vs-outside 0.42, heterogeneity 0.05; core [0.864, 0.975, 0.0] rim [0.699, 0.973, 0.001]
  - track 20 at frame 141: holes 0, rim-vs-core 0.26, rim-vs-outside 0.09, heterogeneity 0.06; core [0.775, 0.981, 0.0] rim [0.511, 0.981, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 31 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.913, rim/outside 2.47 (aggregate of 31 individuals; 5/31 membrane-like individually; rim level 0.632)
  - radial precursor P: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.06, rim/outside 0.753 (aggregate of 31 individuals; 0/31 membrane-like individually; rim level 0.406)
  - radial catalyst K: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 5.15, rim/outside 2.05 (aggregate of 31 individuals; 10/31 membrane-like individually; rim level 0.26)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): catalyst K
- membrane-like channels per top track at mid-life: #14 (t=393, R_eq 18.84, ring): ['amphiphile u+1', 'catalyst K']; #15 (t=393, R_eq 12.41, ring): none; #19 (t=423, R_eq 14.94, ring): none; #20 (t=423, R_eq 5.53): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 18 of 31 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
