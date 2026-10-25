# Evidence pack: fch-pchemoton-starve (seed 3)

- world: `../../20261025T0848-c02-fch-chemoton-claim/world_starve.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 300 steps x dt 0.01 = time 600; grid [192, 192]; wall 372s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0848-c02-fch-chemoton-claim/world_starve.py --out collective/contrib/20261025T0920-c01-review-chemoton/starve --seeds 3 --frames 200 --no-movie`
- segmentation: matter > 0.31 of robust range [-0.0239, 1.968], min area 6 px

## Measurements
- components: final 3, mean 3.3, max 7; occupancy final 0.03
- tracks: 27; persistent (alive >= 50% of run): 1; longest 185 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 4.88 (1 = constant size)
- enclosures: components with a hole mean 2.41, final 3; holes at thresholds 0.2/0.35/0.5 final [0, 3, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 7, 3], H1 [3, 3, 1]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.3
- replication (lineage window K = 20 frames = time 60, default): splits 8, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 7, merge/split ratio 0.875, nucleations 3
- channel total drift (end/start - 1): [-0.9033, 0.0018, -0.988]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 109: holes 1, rim-vs-core 0.21, rim-vs-outside 0.39, heterogeneity 0.05; core [0.874, 0.958, 0.0] rim [0.666, 0.957, 0.0]
  - track 14 at frame 69: holes 3, rim-vs-core 0.15, rim-vs-outside 0.60, heterogeneity 0.18; core [0.826, 0.056, 0.487] rim [0.699, 0.045, 0.57]
  - track 1 at frame 39: holes 7, rim-vs-core 0.01, rim-vs-outside 0.45, heterogeneity 0.05; core [0.667, 0.947, 0.0] rim [0.667, 0.942, 0.001]
  - track 25 at frame 166: holes 1, rim-vs-core 0.19, rim-vs-outside 0.39, heterogeneity 0.05; core [0.858, 0.603, 0.0] rim [0.663, 0.604, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 20 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.38, rim/outside 9.42 (aggregate of 20 individuals; 10/20 membrane-like individually; rim level 0.72)
  - radial precursor P: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.1, rim/outside 0.91 (aggregate of 20 individuals; 0/20 membrane-like individually; rim level 0.604)
  - radial catalyst K: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.49, rim/outside 4.56 (aggregate of 20 individuals; 4/20 membrane-like individually; rim level 0.133)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #10 (t=327, R_eq 12.02, ring): ['amphiphile u+1']; #14 (t=207, R_eq 19.64): ['catalyst K']; #1 (t=117, R_eq 25.51): none; #25 (t=498, R_eq 10.81, ring): ['amphiphile u+1']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 13 of 20 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
