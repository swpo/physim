# Evidence pack: fch-pchemoton (seed 12)

- world: `../world.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 300 steps x dt 0.01 = time 600; grid [192, 192]; wall 356s; status ok
- command: `python -m labkit.run collective/contrib/wip-c27c/world.py --out collective/contrib/wip-c27c/rerun_s12 --seeds 12 --frames 200 --no-movie`
- segmentation: matter > 0.31 of robust range [-0.0237, 1.9657], min area 6 px

## Measurements
- components: final 2, mean 2.1, max 3; occupancy final 0.02
- tracks: 4; persistent (alive >= 50% of run): 2; longest 197 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 15.34 (1 = constant size)
- enclosures: components with a hole mean 1.83, final 2; holes at thresholds 0.2/0.35/0.5 final [2, 2, 2]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [2, 2, 2], H1 [2, 2, 2]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.4
- replication (lineage window K = 20 frames = time 60, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1, merge/split ratio n/a, nucleations 3
- channel total drift (end/start - 1): [-0.9904, 1.0, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 103: holes 1, rim-vs-core 0.20, rim-vs-outside 0.39, heterogeneity 0.04; core [0.872, 1.0, 0.0] rim [0.676, 1.0, 0.0]
  - track 3 at frame 111: holes 2, rim-vs-core 0.17, rim-vs-outside 0.46, heterogeneity 0.05; core [0.883, 1.0, 0.0] rim [0.715, 1.0, 0.0]
  - track 0 at frame 12: holes 0, rim-vs-core 0.15, rim-vs-outside 0.66, heterogeneity 0.07; core [1.0, 0.243, 0.307] rim [0.854, 0.244, 0.317]
  - track 1 at frame 12: holes 0, rim-vs-core 0.15, rim-vs-outside 0.66, heterogeneity 0.07; core [1.0, 0.245, 0.31] rim [0.855, 0.245, 0.321]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 12 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 2.61, rim/outside 17.2 (aggregate of 12 individuals; 11/12 membrane-like individually; rim level 0.74)  MEMBRANE-LIKE
  - radial precursor P: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 1, rim/outside 1 (aggregate of 12 individuals; 0/12 membrane-like individually; rim level 0.982)
  - radial catalyst K: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.998, rim/outside 1 (aggregate of 12 individuals; 0/12 membrane-like individually; rim level 0.0007)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): amphiphile u+1
- membrane-like channels per top track at mid-life: #2 (t=309, R_eq 10.23, ring): ['amphiphile u+1']; #3 (t=333, R_eq 15.31): none; #0 (t=36, R_eq 19.74): none; #1 (t=36, R_eq 19.75): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 12 of 12 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
