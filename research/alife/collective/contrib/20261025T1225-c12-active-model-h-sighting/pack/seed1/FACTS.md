# Evidence pack: active-model-h (seed 1)

- world: `../../world.py`, family `active-model-h`
- parent: None; mutation: -
- run: 161 frames x 250 steps x dt 0.05 = time 2000; grid [128, 128]; wall 615s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1225-c12-active-model-h-sighting/world.py --out collective/contrib/20261025T1225-c12-active-model-h-sighting/pack --seeds 0 1 --frames 160 --spf 250 --no-movie`
- segmentation: matter > 0.22 of robust range [0.0577, 2.0342], min area 6 px

## Measurements
- components: final 66, mean 58.7, max 100; occupancy final 0.37
- tracks: 166; persistent (alive >= 50% of run): 67; longest 130 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 9.83 (1 = constant size)
- enclosures: components with a hole mean 0.14, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [68, 67, 67], H1 [0, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.4
- replication (lineage window K = 20 frames = time 250, default): splits 53, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 9, merge/split ratio 0.17, nucleations 0
- channel total drift (end/start - 1): [0.0, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 2 at frame 95: holes 0, rim-vs-core 0.48, rim-vs-outside 0.20, heterogeneity 0.23; core [0.797, 0.268] rim [0.33, 0.352]
  - track 4 at frame 97: holes 0, rim-vs-core 0.49, rim-vs-outside 0.22, heterogeneity 0.21; core [0.825, 0.325] rim [0.344, 0.388]
  - track 6 at frame 97: holes 0, rim-vs-core 0.48, rim-vs-outside 0.20, heterogeneity 0.21; core [0.809, 0.382] rim [0.333, 0.422]
  - track 159 at frame 114: holes 0, rim-vs-core 0.48, rim-vs-outside 0.20, heterogeneity 0.20; core [0.805, 0.235] rim [0.334, 0.316]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 392 components >= 12 px at frames [27, 54, 81, 106, 133, 160]):
  - radial phi + 1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.733, rim/outside 5.52 (aggregate of 392 individuals; 0/392 membrane-like individually; rim level 0.688)
  - radial flow speed |u|: peak at rho=0.75 (in the peak band 0.5-1.5), rim/core 1.57, rim/outside 1.43 (aggregate of 392 individuals; 162/392 membrane-like individually; rim level 0.426)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #2 (t=1187.5, R_eq 5.11): none; #4 (t=1212.5, R_eq 5.61): none; #6 (t=1212.5, R_eq 5.56): ['flow speed |u|']; #159 (t=1425, R_eq 5.26): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- radial: 1 of 392 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- radial: for 1 of 392 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
