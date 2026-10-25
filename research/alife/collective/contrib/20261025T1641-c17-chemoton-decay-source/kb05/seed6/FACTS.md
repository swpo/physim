# Evidence pack: fch-pchemoton-kablate (seed 6)

- world: `../../world_kablate.py`, family `fch-bilayer`
- parent: collective/contrib/20261025T0651-c02-fch-noise-sighting/world.py; mutation: add a fed precursor, a bilayer-gated Gray-Scott-like catalyst that makes amphiphile, and amphiphile decay
- run: 201 frames x 300 steps x dt 0.01 = time 600; grid [192, 192]; wall 392s; status ok
- command: `python -m labkit.run collective/contrib/c17-kb-wip/world_kablate.py --out collective/contrib/c17-kb-wip/kb05/seed6 --seeds 6 --no-movie`
- segmentation: matter > 0.40 of robust range [-0.0201, 1.5323], min area 6 px

## Measurements
- components: final 5, mean 4.7, max 5; occupancy final 0.09
- tracks: 11; persistent (alive >= 50% of run): 5; longest 200 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.65 (1 = constant size)
- enclosures: components with a hole mean 0.97, final 1; holes at thresholds 0.2/0.35/0.5 final [0, 1, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [11, 8, 4], H1 [2, 2, 1]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 1.0
- replication (lineage window K = 20 frames = time 60, default): splits 2, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 2, merge/split ratio 1, nucleations 5
- channel total drift (end/start - 1): [-0.0654, 0.6164, -0.8597]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 0 at frame 101: holes 0, rim-vs-core 0.24, rim-vs-outside 0.45, heterogeneity 0.06; core [0.956, 0.947, 0.0] rim [0.714, 0.95, 0.001]
  - track 1 at frame 101: holes 0, rim-vs-core 0.50, rim-vs-outside 0.61, heterogeneity 0.17; core [0.95, 0.001, 0.952] rim [0.711, 0.03, 0.516]
  - track 4 at frame 101: holes 0, rim-vs-core 0.23, rim-vs-outside 0.34, heterogeneity 0.06; core [0.902, 0.989, 0.0] rim [0.674, 0.985, 0.0]
  - track 9 at frame 133: holes 0, rim-vs-core 0.15, rim-vs-outside 0.43, heterogeneity 0.05; core [0.858, 0.955, 0.0] rim [0.711, 0.954, 0.001]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 29 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial amphiphile u+1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.711, rim/outside 2.54 (aggregate of 29 individuals; 5/29 membrane-like individually; rim level 0.472)
  - radial precursor P: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.07, rim/outside 0.973 (aggregate of 29 individuals; 0/29 membrane-like individually; rim level 0.818)
  - radial catalyst K: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.415, rim/outside 1.94 (aggregate of 29 individuals; 0/29 membrane-like individually; rim level 0.049)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #0 (t=303, R_eq 11.4): none; #1 (t=303, R_eq 13.88): none; #4 (t=303, R_eq 9.77): none; #9 (t=399, R_eq 18.66, ring): ['amphiphile u+1']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 10 of 29 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
