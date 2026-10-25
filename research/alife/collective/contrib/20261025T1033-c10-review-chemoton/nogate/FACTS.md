# Evidence pack: fch-pchemoton (seed 31)

- world: `../world_ctl.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 300 steps x dt 0.01 = time 600; grid [192, 192]; wall 498s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1033-c10-review-chemoton/world_ctl.py --out collective/contrib/20261025T1033-c10-review-chemoton/nogate --seeds 31 --frames 200 --no-movie`
- segmentation: matter > 0.32 of robust range [-0.0258, 1.9332], min area 6 px

## Measurements
- components: final 4, mean 4.1, max 6; occupancy final 0.01
- tracks: 19; persistent (alive >= 50% of run): 4; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 10.85 (1 = constant size)
- enclosures: components with a hole mean 1.64, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [6, 6, 4], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 60, default): splits 5, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 5, merge/split ratio 1, nucleations 4
- channel total drift (end/start - 1): [-0.9905, 1.0, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 101: holes 1, rim-vs-core 0.21, rim-vs-outside 0.26, heterogeneity 0.04; core [0.788, 1.0, 0.0] rim [0.579, 1.0, 0.0]
  - track 16 at frame 129: holes 0, rim-vs-core 0.28, rim-vs-outside 0.31, heterogeneity 0.06; core [0.905, 1.0, 0.0] rim [0.62, 1.0, 0.0]
  - track 17 at frame 131: holes 0, rim-vs-core 0.23, rim-vs-outside 0.36, heterogeneity 0.06; core [0.899, 1.0, 0.0] rim [0.668, 1.0, 0.0]
  - track 18 at frame 133: holes 0, rim-vs-core 0.28, rim-vs-outside 0.31, heterogeneity 0.06; core [0.902, 1.0, 0.0] rim [0.621, 1.0, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 24 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.15, rim/outside 18.3 (aggregate of 24 individuals; 8/24 membrane-like individually; rim level 0.688)
  - radial precursor P: flat profile (no radial structure; level 0.982; aggregate of 24 individuals)
  - radial catalyst K: flat profile (no radial structure; level 0.0006; aggregate of 24 individuals)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #1 (t=303, R_eq 9.77, ring): ['amphiphile u+1']; #16 (t=387, R_eq 7.59): none; #17 (t=393, R_eq 7.57): none; #18 (t=399, R_eq 7.53): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 8 of 24 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
