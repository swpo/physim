# Evidence pack: fch-pchemoton-clip (seed 7)

- world: `../world_clip.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 401 frames x 300 steps x dt 0.01 = time 1200; grid [192, 192]; wall 1407s; status ok
- command: `python -m labkit.run /tmp/c20dk/world_clip.py --out /tmp/c20dk/clip --seeds 7 --frames 400 --no-movie`
- segmentation: matter > 0.40 of robust range [-0.0204, 1.5185], min area 6 px

## Measurements
- components: final 5, mean 5.0, max 8; occupancy final 0.07
- tracks: 11; persistent (alive >= 50% of run): 5; longest 400 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.20 (1 = constant size)
- enclosures: components with a hole mean 2.91, final 3; holes at thresholds 0.2/0.35/0.5 final [4, 4, 4]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [12, 10, 9], H1 [4, 4, 2]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.0225/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 60, default): splits 1, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 2, merge/split ratio 2, nucleations 6
- channel total drift (end/start - 1): [-0.252, 0.5616, -0.8423]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 202: holes 1, rim-vs-core 0.19, rim-vs-outside 0.39, heterogeneity 0.06; core [0.863, 0.949, 0.0] rim [0.668, 0.946, 0.001]
  - track 3 at frame 202: holes 1, rim-vs-core 0.20, rim-vs-outside 0.39, heterogeneity 0.06; core [0.871, 0.907, 0.001] rim [0.669, 0.906, 0.003]
  - track 4 at frame 202: holes 0, rim-vs-core 0.22, rim-vs-outside 0.53, heterogeneity 0.20; core [0.834, 0.021, 0.57] rim [0.669, 0.055, 0.429]
  - track 9 at frame 208: holes 2, rim-vs-core 0.22, rim-vs-outside 0.57, heterogeneity 0.17; core [0.874, 0.04, 0.545] rim [0.711, 0.051, 0.402]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 30 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial amphiphile u+1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.32, rim/outside 19.9 (aggregate of 30 individuals; 12/30 membrane-like individually; rim level 0.628)
  - radial precursor P: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.07, rim/outside 0.863 (aggregate of 30 individuals; 0/30 membrane-like individually; rim level 0.635)
  - radial catalyst K: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.46, rim/outside 4.39 (aggregate of 30 individuals; 10/30 membrane-like individually; rim level 0.135)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): catalyst K
- membrane-like channels per top track at mid-life: #1 (t=606, R_eq 13.51, ring): ['amphiphile u+1']; #3 (t=606, R_eq 13.79, ring): ['amphiphile u+1']; #4 (t=606, R_eq 10.49): ['catalyst K']; #9 (t=624, R_eq 17.54): ['catalyst K']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 12 of 30 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
