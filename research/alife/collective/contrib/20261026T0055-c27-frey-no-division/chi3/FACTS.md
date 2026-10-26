# Evidence pack: frey-condensates (seed 0)

- world: `../world.py`, family `catalysis-induced-phase-separation`
- parent: Demarchi et al. 2023 (research/alife/LITERATURE.md 2.4.3); mutation: new operator in the ledger: Cahn-Hilliard enzyme condensates whose chemical potential is shifted by the substrate they consume (substrate-feedback self-propulsion)
- run: 101 frames x 1000 steps x dt 0.002 = time 200; grid [128, 128]; wall 290s; status ok
- command: `python -m labkit.run collective/contrib/wip-c27r/world.py --out collective/contrib/wip-c27r/chi3 --seeds 0 --frames 100 --spf 1000 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.0216, 1.0165], min area 6 px

## Measurements
- components: final 1, mean 9.5, max 104; occupancy final 0.34
- tracks: 476; persistent (alive >= 50% of run): 0; longest 14 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.01, final 1; holes at thresholds 0.2/0.35/0.5 final [1, 1, 1]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [1, 1, 1], H1 [1, 1, 1]
- motion: 0 long-lived tracks moved >= 1 body length; max speed 0/time; max body lengths 5.0
- replication (lineage window K = 20 frames = time 40, default): splits 137, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 147, merge/split ratio 1.07, nucleations 132
- channel total drift (end/start - 1): [0.0, -0.791]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 406 at frame 39: holes 0, rim-vs-core 0.22, rim-vs-outside 0.32, heterogeneity 0.09; core [0.923, 0.093] rim [0.7, 0.103]
  - track 352 at frame 25: holes 0, rim-vs-core 0.15, rim-vs-outside 0.60, heterogeneity 0.09; core [0.962, 0.054] rim [0.813, 0.081]
  - track 418 at frame 41: holes 0, rim-vs-core 0.11, rim-vs-outside 0.70, heterogeneity 0.09; core [0.958, 0.038] rim [0.855, 0.07]
  - track 417 at frame 40: holes 0, rim-vs-core 0.10, rim-vs-outside 0.73, heterogeneity 0.09; core [0.97, 0.058] rim [0.867, 0.075]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 31 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial condensate (1+phi)/2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.822, rim/outside 2.31 (aggregate of 31 individuals; 2/31 membrane-like individually; rim level 0.568)
  - radial substrate s: peak at rho=1.95 (OUTSIDE the peak band 0.5-1.5), rim/core 1.36, rim/outside 0.91 (aggregate of 31 individuals; 0/31 membrane-like individually; rim level 0.116)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #406 (t=78, R_eq 4.89): none; #352 (t=50, R_eq 10.79): none; #418 (t=82, R_eq 19.25, ring): none; #417 (t=80, R_eq 22.6, ring): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 8 of 31 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual
- radial: for 4 of 31 aggregate members less than half of the outside band (rho 1.6-2.2) was sampled (window capped on this grid, or an open boundary): their rim/outside is unreliable, and the aggregate outside level comes mostly from the smaller members

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
