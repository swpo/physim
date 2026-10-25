# Evidence pack: fch-pchemoton-starve (seed 8)

- world: `../../../../../home/user/physim/research/alife/collective/contrib/20261025T0848-c02-fch-chemoton-claim/world_starve.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 300 steps x dt 0.01 = time 600; grid [192, 192]; wall 383s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0848-c02-fch-chemoton-claim/world_starve.py --out /tmp/claude-0/c28fch/starve --seeds 7 8 --frames 200 --no-movie`
- segmentation: matter > 0.36 of robust range [-0.0231, 1.7088], min area 6 px

## Measurements
- components: final 5, mean 5.0, max 6; occupancy final 0.02
- tracks: 7; persistent (alive >= 50% of run): 5; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 10.89 (1 = constant size)
- enclosures: components with a hole mean 0.95, final 1; holes at thresholds 0.2/0.35/0.5 final [1, 1, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [6, 5, 5], H1 [1, 1, 1]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.4
- replication (lineage window K = 20 frames = time 60, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 1, merge/split ratio n/a, nucleations 6
- channel total drift (end/start - 1): [-0.9177, -0.431, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 101: holes 0, rim-vs-core 0.24, rim-vs-outside 0.40, heterogeneity 0.06; core [0.903, 0.911, 0.001] rim [0.663, 0.91, 0.002]
  - track 3 at frame 101: holes 0, rim-vs-core 0.52, rim-vs-outside 0.64, heterogeneity 0.17; core [0.928, 0.0, 0.934] rim [0.711, 0.014, 0.464]
  - track 4 at frame 101: holes 0, rim-vs-core 0.55, rim-vs-outside 0.53, heterogeneity 0.17; core [0.909, 0.0, 0.888] rim [0.665, 0.016, 0.391]
  - track 5 at frame 101: holes 0, rim-vs-core 0.53, rim-vs-outside 0.44, heterogeneity 0.21; core [0.88, 0.007, 0.75] rim [0.661, 0.067, 0.276]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 30 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.714, rim/outside 5.88 (aggregate of 30 individuals; 2/30 membrane-like individually; rim level 0.474)
  - radial precursor P: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.33, rim/outside 0.874 (aggregate of 30 individuals; 0/30 membrane-like individually; rim level 0.354)
  - radial catalyst K: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.442, rim/outside 2.19 (aggregate of 30 individuals; 1/30 membrane-like individually; rim level 0.0671)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=303, R_eq 11.58): none; #3 (t=303, R_eq 15.13, ring): none; #4 (t=303, R_eq 13.39): none; #5 (t=303, R_eq 13.13): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 30 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
