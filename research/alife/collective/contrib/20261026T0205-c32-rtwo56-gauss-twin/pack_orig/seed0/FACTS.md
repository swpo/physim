# Evidence pack: r-two56-none (seed 0)

- world: `../../world.py`, family `lenia`
- parent: screen:two#56; mutation: random 'two' channel/kernel graph
- run: 201 frames x 5 steps x dt 0.1 = time 100; grid [192, 192]; wall 9s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0205-c32-rtwo56-gauss-twin/world.py --out collective/contrib/20261026T0205-c32-rtwo56-gauss-twin/pack_orig --seeds 0 1 2 --frames 200 --no-movie`
- segmentation: matter > 0.35 of robust range [0.0, 2.0], min area 6 px

## Measurements
- components: final 8, mean 7.1, max 14; occupancy final 0.05
- tracks: 104; persistent (alive >= 50% of run): 4; longest 181 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.98 (1 = constant size)
- enclosures: components with a hole mean 4.55, final 7; holes at thresholds 0.2/0.35/0.5 final [3, 11, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [7, 7, 7], H1 [16, 0, 0]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 0.9
- replication (lineage window K = 20 frames = time 10, default): splits 38, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 15, merge/split ratio 0.395, nucleations 3
- channel total drift (end/start - 1): [-0.9032, -0.781]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 10 at frame 111: holes 1, rim-vs-core 0.75, rim-vs-outside 0.53, heterogeneity 0.47; core [0.857, 0.415] rim [0.186, 0.755]
  - track 13 at frame 101: holes 3, rim-vs-core 0.73, rim-vs-outside 0.46, heterogeneity 0.46; core [0.823, 0.459] rim [0.164, 0.765]
  - track 38 at frame 129: holes 0, rim-vs-core 0.70, rim-vs-outside 0.48, heterogeneity 0.47; core [0.795, 0.436] rim [0.17, 0.754]
  - track 78 at frame 145: holes 1, rim-vs-core 0.49, rim-vs-outside 0.53, heterogeneity 0.47; core [0.537, 0.357] rim [0.28, 0.778]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 44 components >= 12 px at frames [34, 67, 101, 133, 166, 200]):
  - radial A0: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 0.36, rim/outside 13.1 (aggregate of 44 individuals; 5/44 membrane-like individually; rim level 0.259)
  - radial A1: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 1.31, rim/outside 14.5 (aggregate of 44 individuals; 6/44 membrane-like individually; rim level 0.833)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #10 (t=55.5, R_eq 9.03): none; #13 (t=50.5, R_eq 8.41): none; #38 (t=64.5, R_eq 8.99): none; #78 (t=72.5, R_eq 9.01): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 4 of 44 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
