# Evidence pack: frey-condensates (seed 3)

- world: `../../20261026T0055-c27-frey-no-division/world.py`, family `catalysis-induced-phase-separation`
- parent: Demarchi et al. 2023 (research/alife/LITERATURE.md 2.4.3); mutation: new operator in the ledger: Cahn-Hilliard enzyme condensates whose chemical potential is shifted by the substrate they consume (substrate-feedback self-propulsion)
- run: 101 frames x 1000 steps x dt 0.002 = time 200; grid [128, 128]; wall 405s; status ok
- command: `python -m labkit.run collective/contrib/20261026T0055-c27-frey-no-division/world.py --out collective/contrib/20261026T0106-c25-review-frey/chi2_m04_s3 --seeds 3 --frames 100 --spf 1000 --no-movie`
- segmentation: matter > 0.50 of robust range [-0.0064, 1.0051], min area 6 px

## Measurements
- components: final 5, mean 12.1, max 71; occupancy final 0.28
- tracks: 298; persistent (alive >= 50% of run): 0; longest 40 frames; alive start-to-end: 0
- size of persistent tracks: max/min area ratio 0.00 (1 = constant size)
- enclosures: components with a hole mean 0.00, final 0; holes at thresholds 0.2/0.35/0.5 final [0, 0, 0]
- persistent homology of matter (final frame, tau 0.1/0.25/0.5): H0 [5, 5, 5], H1 [0, 0, 0]
- motion: 7 long-lived tracks moved >= 1 body length; max speed 1.23/time; max body lengths 10.1
- replication (lineage window K = 20 frames = time 40, default): splits 75, persistent splits 0 (0 more failed only because the siblings re-merged within K), max generation 0, merges 89, merge/split ratio 1.19, nucleations 76
- channel total drift (end/start - 1): [-0.0, -0.7549]
- internal organization of top tracks (normalized channel means; rim = outer layer):
  - track 146 at frame 29: holes 0, rim-vs-core 0.16, rim-vs-outside 0.62, heterogeneity 0.10; core [0.975, 0.062] rim [0.817, 0.108]
  - track 278 at frame 82: holes 0, rim-vs-core 0.15, rim-vs-outside 0.65, heterogeneity 0.11; core [0.98, 0.095] rim [0.836, 0.116]
  - track 275 at frame 80: holes 0, rim-vs-core 0.18, rim-vs-outside 0.37, heterogeneity 0.09; core [0.935, 0.118] rim [0.751, 0.128]
  - track 289 at frame 87: holes 0, rim-vs-core 0.16, rim-vs-outside 0.62, heterogeneity 0.10; core [0.981, 0.081] rim [0.823, 0.116]
- radial profiles (rho = r / R_eq around tracked centroids; fixed render scales; core rho<0.4, rim 0.6-1.3, outside 1.6-2.2; aggregate of 47 components >= 12 px at frames [17, 33, 50, 67, 83, 100]):
  - radial condensate (1+phi)/2: peak at rho=0.05 (OUTSIDE the peak band 0.5-1.5), rim/core 0.799, rim/outside 3.82 (aggregate of 47 individuals; 3/47 membrane-like individually; rim level 0.635)
  - radial substrate s: peak at rho=1.85 (OUTSIDE the peak band 0.5-1.5), rim/core 1.71, rim/outside 0.874 (aggregate of 47 individuals; 0/47 membrane-like individually; rim level 0.154)
- membrane-like channels (aggregate rim/core >= 1.5 and rim/outside >= 1.5; the peak position is not part of the test): none
- membrane-like channels per top track at mid-life: #146 (t=58, R_eq 13.85, ring): ['condensate (1+phi)/2']; #278 (t=164, R_eq 10.79): none; #275 (t=160, R_eq 5.35): none; #289 (t=174, R_eq 11.08): none

## Warnings
- a channel total changed by more than 50% (not conserved; may be fine if the model is open)
- radial: 7 of 47 aggregate members are rings (centroid outside their own mask): the threshold may cut individuals into a core and a separate ring, so one individual is counted twice and the ring's profile is centred on its hole; check radial.png and raise META smooth or set META matter so one component covers each individual

## Files
sheet.png, tracks.png, radial.png, lineage.png, timeseries.png, metrics.json

Measurements are screens, not verdicts: judge them against the images.
