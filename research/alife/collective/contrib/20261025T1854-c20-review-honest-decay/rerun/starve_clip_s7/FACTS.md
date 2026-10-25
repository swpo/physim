# Evidence pack: fch-pchemoton-starve-clip (seed 7)

- world: `../world_starve_clip.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 401 frames x 300 steps x dt 0.01 = time 1200; grid [192, 192]; wall 1407s; status ok
- command: `python -m labkit.run /tmp/c20dk/world_starve_clip.py --out /tmp/c20dk/starve_clip --seeds 7 --frames 400 --no-movie`
- segmentation: matter > 0.42 of robust range [-0.0455, 1.4974], min area 6 px

## Measurements
- components: final 1, mean 3.8, max 8; occupancy final 0.00
- tracks: 11; persistent (alive >= 50% of run): 5; longest 389 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 49.75 (1 = constant size)
- enclosures: components with a hole mean 0.99, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.6
- replication (lineage window K = 20 frames = time 60, default): splits 1, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 2, merge/split ratio 2, nucleations 6
- channel total drift (end/start - 1): [-1.4076, -0.5728, -0.9977]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 9 at frame 208: holes 0, rim-vs-core 0.67, rim-vs-outside 0.20, heterogeneity 0.19; core [0.918, 0.002, 0.726] rim [0.614, 0.025, 0.125]
  - track 1 at frame 141: holes 1, rim-vs-core 0.22, rim-vs-outside 0.28, heterogeneity 0.05; core [0.872, 0.477, 0.0] rim [0.652, 0.476, 0.0]
  - track 3 at frame 141: holes 1, rim-vs-core 0.22, rim-vs-outside 0.28, heterogeneity 0.05; core [0.875, 0.434, 0.0] rim [0.653, 0.433, 0.001]
  - track 4 at frame 141: holes 0, rim-vs-core 0.23, rim-vs-outside 0.34, heterogeneity 0.20; core [0.834, 0.05, 0.363] rim [0.656, 0.078, 0.213]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 22 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial amphiphile u+1: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.04, rim/outside 10.2 (aggregate of 22 individuals; 5/22 membrane-like individually; rim level 0.772)
  - radial precursor P: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.05, rim/outside 0.916 (aggregate of 22 individuals; 0/22 membrane-like individually; rim level 0.339)
  - radial catalyst K: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.592, rim/outside 4.63 (aggregate of 22 individuals; 3/22 membrane-like individually; rim level 0.134)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #9 (t=624, R_eq 4.65): none; #1 (t=423, R_eq 9.82, ring): ['amphiphile u+1']; #3 (t=423, R_eq 9.85, ring): ['amphiphile u+1']; #4 (t=423, R_eq 9.47): ['catalyst K']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 5 of 22 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
