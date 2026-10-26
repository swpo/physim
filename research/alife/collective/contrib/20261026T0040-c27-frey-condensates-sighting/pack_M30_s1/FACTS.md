# Evidence pack: frey-condensates (seed 1)

- world: `../world.py`, family `catalysis-induced-phase-separation`
- parent: Demarchi et al. 2023 (research/alife/LITERATURE.md 2.4.3); mutation: new operator in the ledger: Cahn-Hilliard enzyme condensates whose chemical potential is shifted by the substrate they consume (substrate-feedback self-propulsion)
- run: 101 frames x 1000 steps x dt 0.002 = time 200; grid [128, 128]; wall 284s; status ok
- command: `python -m labkit.run collective/contrib/wip-c27p/world.py --out collective/contrib/wip-c27p/pack_M30_s1 --seeds 1 --frames 100 --spf 1000 --no-movie`
- segmentation: matter > 0.49 of robust range [0.0102, 1.0001], min area 6 px

## Measurements
- components: final 6, mean 11.6, max 104; occupancy final 0.33
- tracks: 244; persistent (alive >= 50% of run): 1; longest 59 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.10 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [6, 6, 6], H1 [0, 0, 0]
- motion: 10 long-lived tracks moved >= 1 body length; max speed 0.841/time; max body lengths 3.3
- replication (lineage window K = 20 frames = time 40, default): splits 36, persistent splits 2 (0 more failed only because the siblings re-merged within K), max generation 1, merges 84, merge/split ratio 2.33, nucleations 105
- channel total drift (end/start - 1): [0.0, -0.7407]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 231 at frame 71: holes 0, rim-vs-core 0.10, rim-vs-outside 0.81, heterogeneity 0.09; core [0.98, 0.008] rim [0.891, 0.051]
  - track 237 at frame 78: holes 0, rim-vs-core 0.19, rim-vs-outside 0.61, heterogeneity 0.09; core [0.98, 0.02] rim [0.807, 0.087]
  - track 239 at frame 79: holes 0, rim-vs-core 0.15, rim-vs-outside 0.70, heterogeneity 0.08; core [0.98, 0.004] rim [0.839, 0.053]
  - track 240 at frame 79: holes 0, rim-vs-core 0.15, rim-vs-outside 0.69, heterogeneity 0.08; core [0.981, 0.014] rim [0.843, 0.063]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 49 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial condensate (1+phi)/2: peak at rho=0.15 (OUTSIDE the peak band 0.5-1.5), rim/core 0.848, rim/outside 3.9 (aggregate of 49 individuals; 4/49 membrane-like individually; rim level 0.713)
  - radial substrate s: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 2.79, rim/outside 0.86 (aggregate of 49 individuals; 0/49 membrane-like individually; rim level 0.184)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #231 (t=142, R_eq 26.18): none; #237 (t=156, R_eq 10.79): none; #239 (t=158, R_eq 15.65): none; #240 (t=158, R_eq 17.33): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 6 of 49 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
