# Evidence pack: frey-condensates (seed 0)

- world: `../world.py`, family `catalysis-induced-phase-separation`
- parent: Demarchi et al. 2023 (research/alife/LITERATURE.md 2.4.3); mutation: new operator in the ledger: Cahn-Hilliard enzyme condensates whose chemical potential is shifted by the substrate they consume (substrate-feedback self-propulsion)
- run: 101 frames x 1000 steps x dt 0.002 = time 200; grid [128, 128]; wall 289s; status ok
- command: `python -m labkit.run collective/contrib/wip-c27r/world.py --out collective/contrib/wip-c27r/chi2 --seeds 0 --frames 100 --spf 1000 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.0059, 1.0049], min area 6 px

## Measurements
- components: final 4, mean 11.6, max 102; occupancy final 0.34
- tracks: 400; persistent (alive >= 50% of run): 0; longest 40 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 4, 4], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 1.08/time; max body lengths 3.4
- replication (lineage window K = 20 frames = time 40, default): splits 101, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 129, merge/split ratio 1.28, nucleations 111
- channel total drift (end/start - 1): [0.0, -0.7797]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 380 at frame 81: holes 0, rim-vs-core 0.17, rim-vs-outside 0.61, heterogeneity 0.10; core [0.98, 0.068] rim [0.81, 0.101]
  - track 394 at frame 89: holes 0, rim-vs-core 0.08, rim-vs-outside 0.79, heterogeneity 0.09; core [0.971, 0.053] rim [0.895, 0.076]
  - track 302 at frame 36: holes 0, rim-vs-core 0.17, rim-vs-outside 0.61, heterogeneity 0.10; core [0.976, 0.076] rim [0.811, 0.111]
  - track 368 at frame 63: holes 0, rim-vs-core 0.13, rim-vs-outside 0.68, heterogeneity 0.09; core [0.973, 0.063] rim [0.847, 0.1]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 47 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial condensate (1+phi)/2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.827, rim/outside 2.79 (aggregate of 47 individuals; 2/47 membrane-like individually; rim level 0.616)
  - radial substrate s: peak at rho=1.75 (OUTSIDE the peak band 0.5-1.5), rim/core 1.75, rim/outside 0.924 (aggregate of 47 individuals; 2/47 membrane-like individually; rim level 0.139)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #380 (t=162, R_eq 12.91): none; #394 (t=178, R_eq 22.92): none; #302 (t=72, R_eq 13.46): none; #368 (t=126, R_eq 17.79, ring): ['condensate (1+phi)/2']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 12 of 47 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
