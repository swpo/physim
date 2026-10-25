# Evidence pack: lcn (seed 4)

- world: `../world.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/rf-two56-mu0.01; mutation: closed nutrient ledger (losses return to food, no refill) + shell-gated food diffusion, full-domain noise
- run: 201 frames x 10 steps x dt 0.1 = time 200; grid [192, 192]; wall 22s; status ok
- command: `python -m labkit.run world.py --out pack --seeds 4 --frames 200 --no-movie`
- segmentation: matter > 0.30 of robust range [0.0, 0.9998], min area 6 px

## Measurements
- components: final 11, mean 6.5, max 12; occupancy final 0.14
- tracks: 58; persistent (alive >= 50% of run): 4; longest 155 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.98 (1 = constant size)
- enclosures: components with a hole mean 0.97, final 1; holes at thresholds 0.2/0.35/0.5 final [10, 5, 2]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [18, 11, 10], H1 [17, 11, 2]
- motion: 2 long-lived tracks moved >= 1 body length; max speed 5.71/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 20, default): splits 21, persistent splits 1 (0 more failed only because the siblings re-merged within K), max generation 1, merges 6, merge/split ratio 0.286, nucleations 1
- channel total drift (end/start - 1): [-0.7799, -0.7301, 0.091, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 17 at frame 124: holes 0, rim-vs-core 0.16, rim-vs-outside 1.07, heterogeneity 0.20; core [0.878, 0.297, 0.727, 0.185] rim [0.76, 0.193, 0.742, 0.178]
  - track 18 at frame 124: holes 0, rim-vs-core 0.12, rim-vs-outside 1.00, heterogeneity 0.20; core [0.886, 0.28, 0.751, 0.177] rim [0.779, 0.225, 0.757, 0.167]
  - track 20 at frame 124: holes 0, rim-vs-core 0.34, rim-vs-outside 0.93, heterogeneity 0.19; core [0.948, 0.247, 0.762, 0.159] rim [0.624, 0.151, 0.768, 0.157]
  - track 48 at frame 190: holes 0, rim-vs-core 0.19, rim-vs-outside 1.02, heterogeneity 0.23; core [0.874, 0.283, 0.049, 0.628] rim [0.762, 0.171, 0.151, 0.621]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 40 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A0: peak at rho=0.65 (in the peak band 0.5-1.5), rim/core 1.59, rim/outside 17.7 (aggregate of 40 individuals; 28/40 membrane-like individually; rim level 0.765)  MEMBRANE-LIKE
  - radial A1: peak at rho=1.15 (in the peak band 0.5-1.5), rim/core 1.19, rim/outside 3.75 (aggregate of 40 individuals; 8/40 membrane-like individually; rim level 0.716)
  - radial F: peak at rho=2.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.15, rim/outside 0.847 (aggregate of 40 individuals; 0/40 membrane-like individually; rim level 0.537)
  - radial W: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.943, rim/outside 1.44 (aggregate of 40 individuals; 1/40 membrane-like individually; rim level 0.428)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): A0
- membrane-like channels per top track at mid-life: #17 (t=124, R_eq 6.15): ['A0']; #18 (t=124, R_eq 6.15): ['A0']; #20 (t=124, R_eq 5.89): ['A0']; #48 (t=190, R_eq 6.13): ['A0', 'A1']

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 13 of 40 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- radial: for 1 of 40 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
