# Evidence pack: frey-condensates (seed 3)

- world: `../../20261026T0055-c27-frey-no-division/world.py`, family `catalysis-induced-phase-separation`
- parent: Demarchi et al. 2023 (research/alife/LITERATURE.md 2.4.3); mutation: new operator in the ledger: Cahn-Hilliard enzyme condensates whose chemical potential is shifted by the substrate they consume (substrate-feedback self-propulsion)
- run: 101 frames x 1000 steps x dt 0.002 = time 200; grid [128, 128]; wall 383s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0055-c27-frey-no-division/world.py --out collective/contrib/20261026T0106-c25-review-frey/chi2_s3 --seeds 3 --frames 100 --spf 1000 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.0019, 0.9995], min area 6 px

## Measurements
- components: final 5, mean 11.4, max 102; occupancy final 0.34
- tracks: 377; persistent (alive >= 50% of run): 3; longest 70 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 2.38 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [5, 5, 5], H1 [0, 0, 0]
- motion: 9 long-lived tracks moved >= 1 body length; max speed 1.27/time; max body lengths 6.2
- replication (lineage window K = 20 frames = time 40, default): splits 96, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 123, merge/split ratio 1.28, nucleations 111
- channel total drift (end/start - 1): [0.0, -0.7778]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 350 at frame 66: holes 0, rim-vs-core 0.10, rim-vs-outside 0.75, heterogeneity 0.09; core [0.98, 0.052] rim [0.882, 0.08]
  - track 365 at frame 71: holes 0, rim-vs-core 0.15, rim-vs-outside 0.66, heterogeneity 0.09; core [0.991, 0.073] rim [0.847, 0.094]
  - track 367 at frame 72: holes 0, rim-vs-core 0.12, rim-vs-outside 0.71, heterogeneity 0.10; core [0.98, 0.059] rim [0.863, 0.088]
  - track 375 at frame 80: holes 0, rim-vs-core 0.22, rim-vs-outside 0.49, heterogeneity 0.10; core [0.978, 0.086] rim [0.76, 0.13]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 49 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial condensate (1+phi)/2: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.848, rim/outside 2.98 (aggregate of 49 individuals; 1/49 membrane-like individually; rim level 0.653)
  - radial substrate s: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 1.78, rim/outside 0.926 (aggregate of 49 individuals; 1/49 membrane-like individually; rim level 0.139)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #350 (t=132, R_eq 19.38): none; #365 (t=142, R_eq 11.66): none; #367 (t=144, R_eq 14.4): none; #375 (t=160, R_eq 8.14): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 10 of 49 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
