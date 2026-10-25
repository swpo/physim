# Evidence pack: fch-pchemoton-starve-clip (seed 0)

- world: `../../world_starve_clip.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 300 steps x dt 0.01 = time 600; grid [192, 192]; wall 376s; status ok
- command: `python -m labkit.run world_starve_clip.py --out starve_clip --seeds 0 2 --no-movie`
- segmentation: matter > 0.33 of robust range [-0.0262, 1.8952], min area 6 px

## Measurements
- components: final 3, mean 3.1, max 6; occupancy final 0.01
- tracks: 10; persistent (alive >= 50% of run): 3; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 43.42 (1 = constant size)
- enclosures: components with a hole mean 2.21, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [3, 3, 3], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 60, default): splits 1, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 3, merge/split ratio 3, nucleations 4
- channel total drift (end/start - 1): [-1.1046, -0.3514, -0.9899]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 1, rim-vs-core 0.20, rim-vs-outside 0.43, heterogeneity 0.06; core [0.911, 0.891, 0.001] rim [0.709, 0.885, 0.004]
  - track 3 at frame 101: holes 1, rim-vs-core 0.18, rim-vs-outside 0.60, heterogeneity 0.17; core [0.882, 0.003, 0.586] rim [0.728, 0.011, 0.5]
  - track 9 at frame 109: holes 4, rim-vs-core 0.11, rim-vs-outside 0.47, heterogeneity 0.10; core [0.753, 0.039, 0.021] rim [0.694, 0.072, 0.113]
  - track 1 at frame 8: holes 0, rim-vs-core 0.18, rim-vs-outside 0.58, heterogeneity 0.06; core [1.0, 0.127, 0.209] rim [0.816, 0.128, 0.208]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 18 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.36, rim/outside 13.5 (aggregate of 18 individuals; 7/18 membrane-like individually; rim level 0.733)
  - radial precursor P: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.28, rim/outside 0.842 (aggregate of 18 individuals; 0/18 membrane-like individually; rim level 0.393)
  - radial catalyst K: peak at rho=0.55 (in the peak band 0.5-1.5), rim/core 1.09, rim/outside 5.19 (aggregate of 18 individuals; 6/18 membrane-like individually; rim level 0.191)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=303, R_eq 12.54, ring): ['amphiphile u+1']; #3 (t=303, R_eq 15.08, ring): ['amphiphile u+1']; #9 (t=327, R_eq 24.82): ['catalyst K']; #1 (t=24, R_eq 14.64): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 8 of 18 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
