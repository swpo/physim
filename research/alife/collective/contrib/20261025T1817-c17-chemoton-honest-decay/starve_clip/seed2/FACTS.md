# Evidence pack: fch-pchemoton-starve-clip (seed 2)

- world: `../../world_starve_clip.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 300 steps x dt 0.01 = time 600; grid [192, 192]; wall 364s; status ok
- command: `python -m labkit.run world_starve_clip.py --out starve_clip --seeds 0 2 --no-movie`
- segmentation: matter > 0.31 of robust range [-0.0261, 1.97], min area 6 px

## Measurements
- components: final 3, mean 3.8, max 6; occupancy final 0.01
- tracks: 25; persistent (alive >= 50% of run): 1; longest 140 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 12.55 (1 = constant size)
- enclosures: components with a hole mean 1.66, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [3, 3, 3], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.1
- replication (lineage window K = 20 frames = time 60, default): splits 6, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 7, merge/split ratio 1.17, nucleations 3
- channel total drift (end/start - 1): [-1.1106, -0.1779, -0.9997]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 14 at frame 131: holes 0, rim-vs-core 0.15, rim-vs-outside 0.39, heterogeneity 0.05; core [0.825, 0.481, 0.0] rim [0.672, 0.482, 0.0]
  - track 13 at frame 59: holes 3, rim-vs-core 0.17, rim-vs-outside 0.59, heterogeneity 0.17; core [0.871, 0.037, 0.499] rim [0.705, 0.048, 0.495]
  - track 15 at frame 101: holes 1, rim-vs-core 0.18, rim-vs-outside 0.20, heterogeneity 0.06; core [0.754, 0.011, 0.052] rim [0.578, 0.008, 0.101]
  - track 23 at frame 163: holes 1, rim-vs-core 0.20, rim-vs-outside 0.26, heterogeneity 0.04; core [0.782, 0.482, 0.0] rim [0.586, 0.482, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 23 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.03, rim/outside 4.46 (aggregate of 23 individuals; 4/23 membrane-like individually; rim level 0.664)
  - radial precursor P: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.16, rim/outside 0.816 (aggregate of 23 individuals; 0/23 membrane-like individually; rim level 0.407)
  - radial catalyst K: peak at rho=1.05 (in the peak band 0.5-1.5), rim/core 2.32, rim/outside 2.14 (aggregate of 23 individuals; 6/23 membrane-like individually; rim level 0.162)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): catalyst K
- membrane-like channels per top track at mid-life: #14 (t=393, R_eq 14.28, ring): none; #13 (t=177, R_eq 18.05): ['catalyst K']; #15 (t=303, R_eq 12.51, ring): none; #23 (t=489, R_eq 9.41, ring): ['amphiphile u+1']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 9 of 23 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
