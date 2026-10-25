# Evidence pack: fch-pchemoton-kablate (seed 5)

- world: `../../world_kablate.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 300 steps x dt 0.01 = time 600; grid [192, 192]; wall 364s; status ok
- command: `python -m labkit.run collective/contrib/c17-chemoton-wip/world_kablate.py --out collective/contrib/c17-chemoton-wip/rerun_kablate/seed5 --seeds 5 --no-movie`
- segmentation: matter > 0.36 of robust range [-0.0258, 1.7267], min area 6 px

## Measurements
- components: final 6, mean 6.0, max 6; occupancy final 0.01
- tracks: 6; persistent (alive >= 50% of run): 6; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 13.38 (1 = constant size)
- enclosures: components with a hole mean 0.74, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [6, 6, 6], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.7
- replication (lineage window K = 20 frames = time 60, default): splits 0, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 0, merge/split ratio n/a, nucleations 6
- channel total drift (end/start - 1): [-0.9664, 1.0, -1.0]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.15, rim-vs-outside 0.40, heterogeneity 0.07; core [0.799, 0.965, 0.0] rim [0.65, 0.966, 0.001]
  - track 1 at frame 101: holes 0, rim-vs-core 0.28, rim-vs-outside 0.29, heterogeneity 0.06; core [0.876, 0.989, 0.0] rim [0.595, 0.989, 0.0]
  - track 2 at frame 101: holes 0, rim-vs-core 0.29, rim-vs-outside 0.29, heterogeneity 0.06; core [0.88, 0.963, 0.001] rim [0.593, 0.963, 0.002]
  - track 3 at frame 101: holes 1, rim-vs-core 0.14, rim-vs-outside 0.46, heterogeneity 0.07; core [0.827, 0.891, 0.003] rim [0.686, 0.882, 0.007]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 36 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.824, rim/outside 8.48 (aggregate of 36 individuals; 4/36 membrane-like individually; rim level 0.604)
  - radial precursor P: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.02, rim/outside 0.99 (aggregate of 36 individuals; 0/36 membrane-like individually; rim level 0.917)
  - radial catalyst K: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.662, rim/outside 1.77 (aggregate of 36 individuals; 0/36 membrane-like individually; rim level 0.0321)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=303, R_eq 10.63): none; #1 (t=303, R_eq 8.02): none; #2 (t=303, R_eq 8.04): none; #3 (t=303, R_eq 14.14, ring): ['amphiphile u+1']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 36 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
