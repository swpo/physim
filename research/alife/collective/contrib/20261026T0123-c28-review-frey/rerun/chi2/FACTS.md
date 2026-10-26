# Evidence pack: frey-condensates (seed 4)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261026T0055-c27-frey-no-division/world.py`, family `catalysis-induced-phase-separation`
- parent: Demarchi et al. 2023 (research/alife/LITERATURE.md 2.4.3); mutation: new operator in the ledger: Cahn-Hilliard enzyme condensates whose chemical potential is shifted by the substrate they consume (substrate-feedback self-propulsion)
- run: 101 frames x 1000 steps x dt 0.002 = time 200; grid [128, 128]; wall 286s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0055-c27-frey-no-division/world.py --out /tmp/claude-0/c28fr/chi2 --seeds 4 --frames 100 --spf 1000 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.0032, 1.0031], min area 6 px

## Measurements
- components: final 9, mean 13.3, max 103; occupancy final 0.34
- tracks: 437; persistent (alive >= 50% of run): 1; longest 51 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 1.98 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [9, 9, 9], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 0.993/time; max body lengths 4.0
- replication (lineage window K = 20 frames = time 40, default): splits 116, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 138, merge/split ratio 1.19, nucleations 109
- channel total drift (end/start - 1): [0.0, -0.7802]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 402 at frame 75: holes 0, rim-vs-core 0.17, rim-vs-outside 0.62, heterogeneity 0.10; core [0.979, 0.062] rim [0.818, 0.099]
  - track 416 at frame 84: holes 0, rim-vs-core 0.13, rim-vs-outside 0.70, heterogeneity 0.10; core [0.976, 0.045] rim [0.856, 0.091]
  - track 420 at frame 84: holes 0, rim-vs-core 0.14, rim-vs-outside 0.69, heterogeneity 0.10; core [0.973, 0.049] rim [0.845, 0.096]
  - track 409 at frame 71: holes 0, rim-vs-core 0.13, rim-vs-outside 0.70, heterogeneity 0.10; core [0.981, 0.065] rim [0.853, 0.097]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 62 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial condensate (1+phi)/2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.751, rim/outside 2.5 (aggregate of 62 individuals; 2/62 membrane-like individually; rim level 0.625)
  - radial substrate s: peak at rho=2.15 (OUTSIDE the peak band 0.5-1.5), rim/core 1.9, rim/outside 0.947 (aggregate of 62 individuals; 1/62 membrane-like individually; rim level 0.138)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #402 (t=150, R_eq 13.87): none; #416 (t=168, R_eq 16.55): none; #420 (t=168, R_eq 16.45): none; #409 (t=142, R_eq 16.64, ring): ['substrate s']

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 7 of 62 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
