# Evidence pack: fch-pchemoton-starve (seed 31)

- world: `../../20261025T0848-c02-fch-chemoton-claim/world_starve.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 401 frames x 300 steps x dt 0.01 = time 1200; grid [192, 192]; wall 1068s; status ok
- command: `python -m labkit.run collective/contrib/20261025T0848-c02-fch-chemoton-claim/world_starve.py --out collective/contrib/20261025T1033-c10-review-chemoton/starve_long --seeds 31 --frames 400 --no-movie`
- segmentation: matter > 0.37 of robust range [-0.0257, 1.6824], min area 6 px

## Measurements
- components: final 4, mean 4.1, max 7; occupancy final 0.01
- tracks: 13; persistent (alive >= 50% of run): 4; longest 400 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 10.65 (1 = constant size)
- enclosures: components with a hole mean 1.52, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [5, 5, 4], H1 [0, 0, 0]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.0169/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 60, default): splits 3, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 3, merge/split ratio 1, nucleations 4
- channel total drift (end/start - 1): [-0.9995, -0.4942, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 1 at frame 202: holes 0, rim-vs-core 0.37, rim-vs-outside 0.34, heterogeneity 0.18; core [0.952, 0.067, 0.298] rim [0.676, 0.081, 0.057]
  - track 10 at frame 262: holes 0, rim-vs-core 0.28, rim-vs-outside 0.35, heterogeneity 0.05; core [0.963, 0.227, 0.0] rim [0.687, 0.227, 0.0]
  - track 11 at frame 262: holes 0, rim-vs-core 0.29, rim-vs-outside 0.34, heterogeneity 0.06; core [0.959, 0.226, 0.0] rim [0.671, 0.226, 0.0]
  - track 12 at frame 269: holes 0, rim-vs-core 0.26, rim-vs-outside 0.27, heterogeneity 0.06; core [0.936, 0.215, 0.0] rim [0.678, 0.214, 0.0]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 24 components >= 12 px at frames [67, 134, 202, 266, 333, 400]):
  - radial amphiphile u+1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.956, rim/outside 17.5 (aggregate of 24 individuals; 2/24 membrane-like individually; rim level 0.744)
  - radial precursor P: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.1, rim/outside 0.863 (aggregate of 24 individuals; 0/24 membrane-like individually; rim level 0.253)
  - radial catalyst K: peak at rho=0.85 (in the peak band 0.5-1.5), rim/core 2.79, rim/outside 5.32 (aggregate of 24 individuals; 6/24 membrane-like individually; rim level 0.0907)  MEMBRANE-LIKE
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): catalyst K
- membrane-like channels per top track at mid-life: #1 (t=606, R_eq 7.69): ['catalyst K']; #10 (t=786, R_eq 7.25): none; #11 (t=786, R_eq 7.33): none; #12 (t=807, R_eq 5.29): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 2 of 24 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
