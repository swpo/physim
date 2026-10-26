# Evidence pack: frey-condensates (seed 4)

- world: `../../../../home/user/physim/research/alife/collective/contrib/20261026T0055-c27-frey-no-division/world.py`, family `catalysis-induced-phase-separation`
- parent: Demarchi et al. 2023 (research/alife/LITERATURE.md 2.4.3); mutation: new operator in the ledger: Cahn-Hilliard enzyme condensates whose chemical potential is shifted by the substrate they consume (substrate-feedback self-propulsion)
- run: 101 frames x 1000 steps x dt 0.002 = time 200; grid [128, 128]; wall 290s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0055-c27-frey-no-division/world.py --out /tmp/claude-0/c28fr/chi2_m04 --seeds 4 --frames 100 --spf 1000 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.0081, 1.0052], min area 6 px

## Measurements
- components: final 4, mean 10.3, max 69; occupancy final 0.29
- tracks: 285; persistent (alive >= 50% of run): 0; longest 28 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [4, 4, 4], H1 [0, 0, 0]
- motion: 4 long-lived tracks moved >= 1 body length; max speed 1.09/time; max body lengths 4.1
- replication (lineage window K = 20 frames = time 40, default): splits 75, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 76, merge/split ratio 1.01, nucleations 77
- channel total drift (end/start - 1): [-0.0, -0.758]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 167 at frame 26: holes 0, rim-vs-core 0.24, rim-vs-outside 0.49, heterogeneity 0.10; core [0.97, 0.062] rim [0.736, 0.103]
  - track 178 at frame 27: holes 0, rim-vs-core 0.16, rim-vs-outside 0.56, heterogeneity 0.10; core [0.985, 0.092] rim [0.827, 0.108]
  - track 208 at frame 31: holes 0, rim-vs-core 0.23, rim-vs-outside 0.48, heterogeneity 0.10; core [0.973, 0.069] rim [0.747, 0.111]
  - track 228 at frame 38: holes 0, rim-vs-core 0.14, rim-vs-outside 0.69, heterogeneity 0.09; core [0.98, 0.056] rim [0.849, 0.091]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 40 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial condensate (1+phi)/2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.819, rim/outside 3.07 (aggregate of 40 individuals; 5/40 membrane-like individually; rim level 0.607)
  - radial substrate s: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 1.7, rim/outside 0.913 (aggregate of 40 individuals; 0/40 membrane-like individually; rim level 0.153)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #167 (t=52, R_eq 9.36): none; #178 (t=54, R_eq 8.5): none; #208 (t=62, R_eq 9.97): none; #228 (t=76, R_eq 14.61): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 9 of 40 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
