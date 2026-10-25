# Evidence pack: fch-pchemoton-starve (seed 2)

- world: `../../../../../../../home/user/physim/research/alife/collective/contrib/20261025T0848-c02-fch-chemoton-claim/world_starve.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 300 steps x dt 0.01 = time 600; grid [192, 192]; wall 709s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0848-c02-fch-chemoton-claim/world_starve.py --out collective/contrib/20261025T0848-c02-fch-chemoton-claim/pack_starve/seed2 --seeds 2 --frames 200 --no-movie`
- segmentation: matter > 0.31 of robust range [-0.024, 1.9701], min area 6 px

## Measurements
- components: final 3, mean 3.8, max 6; occupancy final 0.03
- tracks: 23; persistent (alive >= 50% of run): 2; longest 103 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 11.75 (1 = constant size)
- enclosures: components with a hole mean 2.30, final 3; holes at thresholds 0.2/0.35/0.5 final [0, 3, 3]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [3, 3, 3], H1 [3, 3, 3]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.1
- replication (lineage window K = 20 frames = time 60, default): splits 5, persistent splits 3 (0 more failed only because the siblings re-merged within K), max generation 1, merges 7, merge/split ratio 1.4, nucleations 3
- channel total drift (end/start - 1): [-0.9009, -0.2515, -0.9935]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 52: holes 5, rim-vs-core 0.13, rim-vs-outside 0.45, heterogeneity 0.05; core [0.82, 0.988, 0.0] rim [0.692, 0.986, 0.001]
  - track 13 at frame 69: holes 3, rim-vs-core 0.18, rim-vs-outside 0.58, heterogeneity 0.18; core [0.849, 0.067, 0.329] rim [0.709, 0.055, 0.445]
  - track 14 at frame 108: holes 0, rim-vs-core 0.17, rim-vs-outside 0.44, heterogeneity 0.09; core [0.856, 0.097, 0.285] rim [0.705, 0.104, 0.2]
  - track 15 at frame 108: holes 1, rim-vs-core 0.18, rim-vs-outside 0.20, heterogeneity 0.04; core [0.769, 0.042, 0.024] rim [0.594, 0.045, 0.043]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 23 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.29, rim/outside 4.82 (aggregate of 23 individuals; 8/23 membrane-like individually; rim level 0.7)
  - radial precursor P: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.19, rim/outside 0.806 (aggregate of 23 individuals; 0/23 membrane-like individually; rim level 0.378)
  - radial catalyst K: peak at rho=1.15 (in the peak band 0.5-1.5), rim/core 1.78, rim/outside 2.03 (aggregate of 23 individuals; 7/23 membrane-like individually; rim level 0.129)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): catalyst K
- membrane-like channels per top track at mid-life: #2 (t=156, R_eq 20.9): none; #13 (t=207, R_eq 19.09): ['catalyst K']; #14 (t=324, R_eq 19.03, ring): ['amphiphile u+1', 'catalyst K']; #15 (t=324, R_eq 12.57, ring): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 13 of 23 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
