# Evidence pack: fch-pchemoton-res15 (seed 8)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261025T1048-c02-chemoton-res15/world_res15.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 600 steps x dt 0.005 = time 600; grid [288, 288]; wall 2006s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1048-c02-chemoton-res15/world_res15.py --out /tmp/claude-0/c11rev23/res15 --seeds 8 --frames 200 --no-movie`
- segmentation: matter > 0.31 of robust range [-0.0207, 1.9886], min area 6 px

## Measurements
- components: final 4, mean 3.5, max 5; occupancy final 0.07
- tracks: 21; persistent (alive >= 50% of run): 4; longest 154 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 6.58 (1 = constant size)
- enclosures: components with a hole mean 1.23, final 1; holes at thresholds 0.2/0.35/0.5 final [1, 1, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 4, 3], H1 [3, 3, 2]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.1
- replication (lineage window K = 20 frames = time 60, default): splits 7, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 5, merge/split ratio 0.714, nucleations 2
- channel total drift (end/start - 1): [-0.3614, 0.6509, -0.8736]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 16 at frame 124: holes 0, rim-vs-core 0.38, rim-vs-outside 0.67, heterogeneity 0.16; core [0.938, 0.001, 0.939] rim [0.773, 0.033, 0.595]
  - track 17 at frame 124: holes 1, rim-vs-core 0.20, rim-vs-outside 0.25, heterogeneity 0.07; core [0.856, 0.102, 0.051] rim [0.666, 0.09, 0.098]
  - track 19 at frame 129: holes 0, rim-vs-core 0.18, rim-vs-outside 0.46, heterogeneity 0.05; core [0.947, 0.99, 0.0] rim [0.766, 0.99, 0.0]
  - track 20 at frame 129: holes 0, rim-vs-core 0.29, rim-vs-outside 0.13, heterogeneity 0.06; core [0.862, 0.992, 0.0] rim [0.574, 0.992, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 22 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.14, rim/outside 2.28 (aggregate of 22 individuals; 6/22 membrane-like individually; rim level 0.694)
  - radial precursor P: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.986, rim/outside 0.822 (aggregate of 22 individuals; 0/22 membrane-like individually; rim level 0.541)
  - radial catalyst K: peak at rho=1.15 (in the peak band 0.5-1.5), rim/core 6.97, rim/outside 1.96 (aggregate of 22 individuals; 5/22 membrane-like individually; rim level 0.271)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): catalyst K
- membrane-like channels per top track at mid-life: #16 (t=372, R_eq 28.93, ring): ['amphiphile u+1', 'catalyst K']; #17 (t=372, R_eq 19.4, ring): none; #19 (t=387, R_eq 22.5, ring): none; #20 (t=387, R_eq 8.39): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 17 of 22 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
