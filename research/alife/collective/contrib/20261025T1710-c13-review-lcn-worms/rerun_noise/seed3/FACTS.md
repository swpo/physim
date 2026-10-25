# Evidence pack: lcn (seed 3)

- world: `../../world.py`, family `lenia`
- parent: threads/lenia-multichannel/worlds/rf-two56-mu0.01; mutation: closed nutrient ledger (losses return to food, no refill) + shell-gated food diffusion, full-domain noise
- run: 301 frames x 50 steps x dt 0.1 = time 1500; grid [192, 192]; wall 161s; status ok
- command: `python -m labkit.run collective/contrib/20261025T1710-c13-review-lcn-worms/world.py --out collective/contrib/20261025T1710-c13-review-lcn-worms/rerun_noise/seed3 --seeds 3 --spf 50 --frames 300 --no-movie`
- segmentation: matter > 0.30 of robust range [0.0, 0.9998], min area 6 px

## Measurements
- components: final 27, mean 26.2, max 38; occupancy final 0.19
- tracks: 1422; persistent (alive >= 50% of run): 0; longest 85 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 10.76, final 6; holes at thresholds 0.2/0.35/0.5 final [12, 10, 11]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [44, 33, 27], H1 [29, 22, 7]
- motion: 1 long-lived tracks moved >= 1 body length; max speed 0.0302/time; max body lengths 1.1
- replication (lineage window K = 20 frames = time 100, default): splits 439, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 489, merge/split ratio 1.11, nucleations 18
- channel total drift (end/start - 1): [-0.69, -0.5105, -0.2155, None]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 12 at frame 53: holes 0, rim-vs-core 0.13, rim-vs-outside 1.00, heterogeneity 0.21; core [0.883, 0.291, 0.809, 0.074] rim [0.758, 0.242, 0.802, 0.078]
  - track 484 at frame 161: holes 0, rim-vs-core 0.12, rim-vs-outside 1.03, heterogeneity 0.22; core [0.876, 0.282, 0.684, 0.165] rim [0.77, 0.232, 0.684, 0.167]
  - track 338 at frame 134: holes 0, rim-vs-core 0.16, rim-vs-outside 1.05, heterogeneity 0.21; core [0.885, 0.297, 0.758, 0.089] rim [0.74, 0.221, 0.751, 0.093]
  - track 13 at frame 33: holes 0, rim-vs-core 0.18, rim-vs-outside 0.99, heterogeneity 0.20; core [0.893, 0.31, 0.883, 0.067] rim [0.74, 0.222, 0.888, 0.067]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 166 components >= 12 px at frames [50, 101, 151, 199, 250, 300]):
  - radial A0: peak at rho=0.45 (OUTSIDE the peak band 0.5-1.5), rim/core 1.39, rim/outside 11.9 (aggregate of 166 individuals; 95/166 membrane-like individually; rim level 0.746)
  - radial A1: peak at rho=1.15 (in the peak band 0.5-1.5), rim/core 1.4, rim/outside 2.25 (aggregate of 166 individuals; 37/166 membrane-like individually; rim level 0.7)
  - radial F: peak at rho=2.35 (OUTSIDE the peak band 0.5-1.5), rim/core 1.15, rim/outside 0.914 (aggregate of 166 individuals; 0/166 membrane-like individually; rim level 0.445)
  - radial W: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.956, rim/outside 1.14 (aggregate of 166 individuals; 0/166 membrane-like individually; rim level 0.461)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #12 (t=265, R_eq 6.18): ['A0']; #484 (t=805, R_eq 6.15): ['A0']; #338 (t=670, R_eq 6.18): ['A0']; #13 (t=165, R_eq 6.15): none

## Warnings
- matter fills >80% of the domain at some point: components may be one connected sea
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 36 of 166 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
